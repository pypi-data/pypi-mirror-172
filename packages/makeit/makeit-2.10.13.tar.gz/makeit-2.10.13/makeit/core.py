import asyncio
import collections
import dataclasses
import inspect
import itertools
import json
import multiprocessing
import pathlib
import hashlib
import datetime
import enum
import graphlib
import abc
import sys
import traceback
import warnings
from types import ModuleType
from typing import Any, Dict, Iterable, List, Set, Type, Pattern, IO, Callable, TextIO


def md5(s: str) -> str:
    return hashlib.md5(s.encode('utf-8')).hexdigest()


class MakeItError(Exception):
    """ Raised when a task is not correctly defined """
    pass


class ChildProcessException(Exception):
    pass


class _Node(abc.ABC):
    def label(self) -> str:
        raise NotImplementedError()


class Artifact(_Node):
    def fingerprint(self) -> str | None:
        """This string representation is used to check if artifact has changed"""
        raise NotImplementedError()

    def exists(self) -> bool:
        """For file-like objects -- if not exists, need to recalculate"""
        raise NotImplementedError()

    def modification_time(self) -> datetime.datetime:
        """For file-like objects"""
        raise NotImplementedError()

    def label(self) -> str:
        """Identifying label."""
        raise NotImplementedError()


class Task(_Node, abc.ABC):
    def label(self) -> str:
        """ This label uniquely describes the task """
        raise NotImplementedError()

    def dependencies(self) -> Iterable[Artifact]:
        """ Return list of artifacts this task depends on """
        return []

    def runtime_dependencies(self) -> Iterable[Artifact]:
        """ Dependencies that are known during execution of dag only """
        return []

    def task_dependencies(self) -> Iterable[str | Pattern[str] | 'Task']:
        """ Implicit task dependencies that are not expressed via artifacts """
        return []

    def targets(self) -> Iterable[Artifact]:
        """ Return list of targets of the task """
        return []

    def execute(self):
        """ Users implement this method for synchronous/multiprocess execution """
        raise NotImplementedError()

    async def a_execute(self):
        """ Users implement this method for asynchronous execution """
        raise NotImplementedError()

    def __repr__(self):
        return f'{self.__class__.__module__}.{self.__class__.__name__}("{self.label()}")'


class Dependency:
    pass


class Target:
    pass

# ----------------------------------------------------------------------------------------------------------------------


class AbstractFileChecker:
    def fingerprint(self, path: pathlib.Path) -> str:
        raise NotImplementedError()


class MD5Checker(AbstractFileChecker):
    def fingerprint(self, path: pathlib.Path):
        with path.open("rb") as f:
            file_hash = hashlib.md5()
            while chunk := f.read(8192):
                file_hash.update(chunk)

        return f"{self.__class__.__name__}: {file_hash.hexdigest()}"


class TimeChecker(AbstractFileChecker):
    def __init__(self, use_datetime=False):
        self.use_datetime = use_datetime

    def fingerprint(self, path: pathlib.Path) -> str:
        m = path.stat().st_mtime
        if self.use_datetime:
            fp = datetime.datetime.fromtimestamp(m, tz=datetime.timezone.utc)
        else:
            fp = m

        return f"{self.__class__.__name__}: {fp}"


class ExistsChecker(AbstractFileChecker):
    def fingerprint(self, path: pathlib.Path) -> str:
        return f"{self.__class__.__name__}"


class File(Artifact):
    def __init__(self, path: pathlib.Path | str, checker: AbstractFileChecker = MD5Checker(),
                 label: str | None = None):
        self._path = pathlib.Path(path)
        self._checker = checker

        if label is not None:
            self._label = label
        else:
            self._label = f'{self.__class__.__module__}.{self.__class__.__name__}' \
                          f'({self._path})'

    @property
    def path(self):
        return self._path

    def fingerprint(self) -> str:
        return self._checker.fingerprint(self._path)

    def exists(self) -> bool:
        return self._path.exists() and self._path.is_file()

    def modification_time(self) -> datetime.datetime:
        m = self._path.stat().st_mtime
        return datetime.datetime.fromtimestamp(m, tz=datetime.timezone.utc)

    def label(self) -> str:
        return self._label

    def __repr__(self):
        return self._label


class SourceCode(Artifact, Dependency):
    """ This artifact tracks source code of a class, module, callable using the `inspect` library """

    _types_registry = {}  # cache seen types

    def __init__(self, *args: Type | ModuleType | Callable):
        self.classes = list(args)

    def fingerprint(self) -> str:
        sources = [self.__class__._getsource(_) for _ in self.classes]
        return hashlib.md5("\n\n".join(sources).encode('utf-8')).hexdigest()

    @classmethod
    def _getsource(cls, tp):
        if tp not in cls._types_registry:
            cls._types_registry[tp] = inspect.getsource(tp)

        return cls._types_registry[tp]

    def exists(self) -> bool:
        return True

    def modification_time(self) -> datetime.datetime:
        raise NotImplementedError("This type of artifact does not support modification time")

    def label(self) -> str:
        return f"{self.__class__.__module__}.{self.__class__.__name__}" \
               f"({', '.join(f'{c.__module__}.{c.__name__}' for c in self.classes)})"

    def __repr__(self):
        return self.label()

# ----------------------------------------------------------------------------------------------------------------------


class _DepGraph:
    def __init__(self, dep_graph: Dict[str, List[str]], label2node: Dict[str, _Node]):
        """

        :param dep_graph: dictionary from node to a list if its dependencies (as in graphlib.TopologicalSorter)
        :param label2node:
        """
        self.dep_graph = dep_graph
        self.label2node = label2node

    def subgraph(self, labels: Set[str]) -> '_DepGraph':
        front = labels

        res = collections.defaultdict(list)

        while front:
            new_front = set()
            for f in front:
                assert f not in res
                if f in self.dep_graph:
                    res[f] = self.dep_graph[f]
                    new_front.update(self.dep_graph[f])
            front = new_front

        return _DepGraph(res, self.label2node)  # TODO: fix me

    def all_nodes(self):
        res = set()

        for k, v in self.dep_graph.items():
            res.update([k])
            res.update(v)

        return res

    def edges(self):
        """
        Yields pairs of the form (head, tail), where head depends on tail.
        head <- tail
        """
        for k, v_ in self.dep_graph.items():
            for v in v_:
                yield k, v


@dataclasses.dataclass
class _Artifact:
    """ Internal artifact representation """

    label: str

    obj: Artifact

    def fingerprint(self):
        return self.obj.fingerprint()

    def exists(self):
        return self.obj.exists()


@dataclasses.dataclass
class _Task:
    """ Internal task representation """

    label: str

    deps: dict[str, Artifact]
    tars: dict[str, Artifact]

    obj: Task

    def execute(self):
        self.obj.execute()


class DAG:
    def __init__(self, name: str):
        self.name = name

        self.tasks = {}  # type: dict[str, _Task]
        self.name2obj = {}  # type: dict[str, _Artifact | _Task]

    def __str__(self):
        return f'{self.__class__.__module__}.{self.__class__.__name__}(' \
               f'"{self.name}")'

    def _register(self, a: Artifact) -> _Artifact:
        label = a.label()

        if label in self.name2obj:
            return self.name2obj[label]

        _a = _Artifact(label=label, obj=a)

        self.name2obj[label] = _a

        return _a

    def add(self, _task: Task):
        label = _task.label

        if inspect.ismethod(label):
            label = label()

        if label is None:
            raise MakeItError(f"{label} does not implement method label()")

        if label in self.tasks:
            raise MakeItError(f"{label} is already in DAG {self}")

        deps = list(_task.dependencies())
        tars = list(_task.targets())

        deps_ = [self._register(_) for _ in deps]
        tars_ = [self._register(_) for _ in tars]

        _t = _Task(
            label=label,
            deps={_.label: _.obj for _ in deps_},
            tars={_.label: _.obj for _ in tars_},
            obj=_task
        )

        self.name2obj[label] = _t
        self.tasks[label] = _t

    def select_tasks(self, reg: Pattern[str]):
        for label, task in self.tasks:
            if reg.match(label):
                yield task

    def create_dep_graph(self) -> _DepGraph:
        graph = collections.defaultdict(list)

        for t in self.tasks.values():
            for dep in t.deps:
                graph[t.label].append(dep)

            for tar in t.tars:
                graph[tar].append(t.label)

            for task_dep in t.obj.task_dependencies():
                if isinstance(task_dep, Task):
                    task_dep_labels = (task_dep.label(), )
                elif isinstance(task_dep, str):
                    other = self.name2obj.get(task_dep, None)
                    if not isinstance(other, _Task):
                        raise MakeItError(f"{task_dep} is not a task label")
                    task_dep_labels = (other.label, )
                else:  # regular expression
                    task_dep_labels = self.select_tasks(task_dep)

                graph[t.label].extend(task_dep_labels)

            if t.label not in graph:
                graph[t.label] = []

        return _DepGraph(graph, self._create_label2obj())

    def _create_label2obj(self) -> Dict[str, _Node]:
        res = dict()

        for o in self.name2obj.values():
            res[o.label] = o.obj

        return res

# ----------------------------------------------------------------------------------------------------------------------


class AbstractBackend(abc.ABC):
    def set(self, dag_name: str, kind: str, label: str, something: str | dict) -> None:
        raise NotImplementedError()

    def get(self, dag_name: str, kind: str, label: str) -> str | dict | None:
        raise NotImplementedError()

    def flush(self):
        raise NotImplementedError()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        raise NotImplementedError()


class DictBackend(AbstractBackend):
    def __init__(self, file: str | None | IO | pathlib.Path,
                 autocommit=False, commit_on_failure=True):
        self.file = file
        self.d = dict()
        self.autocommit = autocommit
        self.commit_on_failure = commit_on_failure

        if file is not None:
            if isinstance(file, (str, pathlib.Path)):
                try:
                    with open(file, encoding='utf-8', mode='r') as fp:
                        self.d = json.load(fp)
                except FileNotFoundError:
                    pass
            else:
                file.seek(0)
                self.d = json.load(file)

    def _get_key(self, *args, create=False):
        c = self.d

        for step in args:
            if create and step not in c:
                c[step] = {}

            c = c[step]

        return c

    def set(self, dag_name: str, kind: str, label: str, something: str | dict) -> None:
        c = self._get_key(dag_name, kind, create=True)
        c[label] = something

    def get(self, dag_name: str, kind: str, label: str) -> str | dict | None:
        try:
            return self._get_key(dag_name, kind, label)
        except KeyError:
            return None

    def flush(self):
        if self.file is not None:
            if isinstance(self.file, (str, pathlib.Path)):
                with open(self.file, encoding='utf-8', mode='w') as fp:
                    json.dump(self.d, fp, indent=' ', ensure_ascii=False)
            else:
                self.file.seek(0)
                json.dump(self.d, self.file, indent=' ', ensure_ascii=False)

    def __exit__(self, exc_type, exc_val, exc_tb):
        if (exc_val is None) or self.commit_on_failure:
            self.flush()

# ----------------------------------------------------------------------------------------------------------------------


class TaskEvent(enum.Enum):
    SKIP = 1
    IGNORE = 2
    EXECUTE = 3
    DONE = 4
    FAILURE = 5


class Reporter:
    def report_task_event(self, event: TaskEvent, task_name: str, reason: str | None):
        pass

    def on_dag_start(self, dag_name: str, total_number_of_tasks: int):
        pass

    def on_dag_end(self):
        pass


class LogReporter(Reporter):
    def __init__(self, logger):
        self.logger = logger
        self.dag_name = None

        super(LogReporter, self).__init__()

    def report_task_event(self, event: TaskEvent, task_name: str, reason: str):
        self.logger.info(f"{event.name: >7}: {task_name}: {reason}")

    def on_dag_start(self, dag_name: str, total_number_of_tasks: int):
        self.dag_name = dag_name

        self.logger.info(f" START: {self.dag_name}")

    def on_dag_end(self):
        self.logger.info(f"  DONE: {self.dag_name}")


class SimpleReporter(Reporter):
    def __init__(self, min_level: TaskEvent | None = None, max_task_name_len=40,
                 stream: TextIO | None = sys.stderr):
        import colorama
        colorama.init()

        self.max_task_name_len = max_task_name_len
        self.stream = stream

        if min_level is None:
            self.min_level = 0
        else:
            self.min_level = min_level.value

        _task_event_format = ("<green>{time}</green> | "
                              "<event>{event: <8}</event> | "
                              "<cyan>{percent: >10}</cyan> | "
                              "<event>{task: <%s}</event> | "
                              "<event>{message}</event>"
                              ) % self.max_task_name_len

        _dag_event_format = ("<green>{time}</green> | "
                             "<yellow>{event: <8}</yellow> | "
                             "<yellow>{took: >10}</yellow> | "
                             "<yellow>{message}</yellow>")

        self.dag_event_format = self._subs_colors(_dag_event_format)
        self.task_event_format: dict[TaskEvent, str] = {
            event: self._subs_colors(_task_event_format, style)
            for event, style in [
                (TaskEvent.SKIP, ["blue", "bold", ]),
                (TaskEvent.IGNORE, ["blue", "bold", ]),
                (TaskEvent.EXECUTE, ["green", ]),
                (TaskEvent.DONE, ["green", "bold", ]),
                (TaskEvent.FAILURE, ["red", "bold", ]),
            ]
        }

        self.dag_name = None

        self.total_number_of_tasks = 0
        self.number_of_visited_tasks = 0

        self.started_dag_at: datetime.datetime | None = None

        super(SimpleReporter, self).__init__()

    def _subs_colors(self, fmt: str, event_style: list[str] = None):
        # Substitute colors like <green>, etc. with colorama colors
        import colorama

        s = fmt

        if event_style:
            open_ = "".join(f"<{_}>" for _ in event_style)
            s = s.replace("<event>", open_)

        for name, c in self._colors_and_styles().items():
            s = s.replace(f"<{name}>", c)
            s = s.replace(f"</{name}>", colorama.Style.RESET_ALL)

        s = s.replace("</event>", colorama.Style.RESET_ALL)

        return s

    @staticmethod
    def _colors_and_styles():
        import colorama
        return {
            'yellow': colorama.Fore.YELLOW,
            'blue': colorama.Fore.BLUE,
            'green': colorama.Fore.GREEN,
            'cyan': colorama.Fore.CYAN,
            'bold': colorama.Style.BRIGHT,
            'red': colorama.Back.RED
        }

    def report_task_event(self, event: TaskEvent, task_name: str, reason: str):
        # self.logger.info(f"{event.name: >7}: {task_name}: {reason}")

        if event in [TaskEvent.SKIP, TaskEvent.IGNORE, TaskEvent.DONE, TaskEvent.FAILURE]:
            self.number_of_visited_tasks += 1

        if event.value < self.min_level:
            return

        fmt = self.task_event_format[event]

        percent = self.number_of_visited_tasks / self.total_number_of_tasks

        if len(task_name) > self.max_task_name_len:
            task_name = task_name[:self.max_task_name_len - 3] + "..."

        s = fmt.format(
            time=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            event=event.name,
            percent=f"{percent:6.1%}",
            message=reason,
            task=task_name
        )

        if self.stream is not None:
            print(s, file=self.stream)

    def on_dag_start(self, dag_name: str, total_number_of_tasks: int):
        self.dag_name = dag_name
        self.total_number_of_tasks = max(total_number_of_tasks, 1)
        self.number_of_visited_tasks = 0
        self.started_dag_at = datetime.datetime.now()

        s = self.dag_event_format.format(
            time=self.started_dag_at.strftime("%Y-%m-%d %H:%M:%S"),
            event='START',
            took='',
            message=self.dag_name
        )

        if self.stream is not None:
            print(s, file=self.stream)

    def on_dag_end(self):
        now = datetime.datetime.now()
        took_sec = (now - self.started_dag_at).seconds

        s = self.dag_event_format.format(
                time=now.strftime("%Y-%m-%d %H:%M:%S"),
                event='DONE',
                took=f"{took_sec:.1f} sec",
                message=self.dag_name
            )

        if self.stream is not None:
            print(s, file=self.stream)

# ----------------------------------------------------------------------------------------------------------------------


class _CachedFingerprint:
    """ Cached fingerprint """

    def __init__(self):
        self._cached_fingerprints = {}

    def get_fingerprint(self, label: str, a: Artifact):
        if label not in self._cached_fingerprints:
            self._cached_fingerprints[label] = a.fingerprint()

        return self._cached_fingerprints[label]

    def invalidate(self, label: str):
        if label in self._cached_fingerprints:
            del self._cached_fingerprints[label]

# ----------------------------------------------------------------------------------------------------------------------


@dataclasses.dataclass
class _NeedExecuteDecision:
    decision: bool
    reason: str | None

    def __bool__(self):
        return self.decision


class ExecutionAdviser:
    def __init__(self, dag_name: str, backend: AbstractBackend | None):
        self._dag_name = dag_name
        self._backend = backend

    @property
    def dag_name(self):
        return self._dag_name

    @property
    def backend(self):
        return self._backend

    def need_execute(self, task: _Task) -> _NeedExecuteDecision:
        raise NotImplementedError()

    def task_has_been_executed(self, task: _Task):
        """ This method is called after a successful execution of the task.
            Clients can store data in the backend.
        """
        raise NotImplementedError()


class EAAlwaysRun(ExecutionAdviser):
    def need_execute(self, task: _Task) -> _NeedExecuteDecision:
        return _NeedExecuteDecision(True, "always execute")

    def task_has_been_executed(self, task: _Task):
        pass


class EACheckExists(ExecutionAdviser):
    """ Check if targets exist """
    always_execute_if_no_targets = True

    def need_execute(self, task: _Task):
        if self.always_execute_if_no_targets and not task.tars:
            return _NeedExecuteDecision(True, f"has no targets")

        for label, tar in task.tars.items():
            if not tar.exists():
                return _NeedExecuteDecision(True, f"{label} does not exist")

        return _NeedExecuteDecision(False, "up-to-date")

    def task_has_been_executed(self, task: _Task):
        pass


class EARunOnChange(ExecutionAdviser):
    """ Run if dependencies have changed """

    def __init__(self, dag_name: str, backend: AbstractBackend,
                 capture_only=False, execute_all=False, strict_checks=True,
                 test_targets_fingerprints=False):
        """
            capture_only -- do not run tasks, calculate fingerprints and store in the backend
            execute_all -- run all tasks, disregard all previous calculations
            strict_checks -- check that tasks create all required artifacts and that artifacts exists before
            test_targets_fingerprints -- run task if targets have changed (i.e. externally)
        """
        assert isinstance(capture_only, bool)
        assert isinstance(execute_all, bool)
        assert isinstance(strict_checks, bool)
        assert isinstance(test_targets_fingerprints, bool)

        super(EARunOnChange, self).__init__(dag_name, backend)
        self._fp = _CachedFingerprint()

        self.strict_checks = strict_checks
        self.capture_only = capture_only
        self.execute_all = execute_all
        self.test_targets_fingerprints = test_targets_fingerprints

        assert not capture_only or not execute_all, "Only one flags can be set"

    def need_execute(self, task: _Task):
        if self.capture_only:
            self._store_signature(task)
            return _NeedExecuteDecision(False, "capturing fingerprints")

        if self.execute_all:
            return _NeedExecuteDecision(True, "executing all")

        if self.strict_checks:
            for label, a in task.deps.items():
                if not a.exists():
                    raise MakeItError(f"dependency {label} for {task.label} does not exist."
                                      " Set `strict_checks` flag to false, if this check is not desired.")

        prev = self.backend.get(
            self.dag_name,
            self.__class__.__name__,
            task.label,
        )

        if prev is None:
            return _NeedExecuteDecision(True, "executing for the first time")

        for label, a in task.deps.items():
            if label not in prev:
                return _NeedExecuteDecision(True, f"no previous fingerprint in backend: {label}")

            __prev = prev[label]
            __curr = self._fp.get_fingerprint(label, a)
            if __prev != __curr:
                return _NeedExecuteDecision(True, f"dependency has changed: {label}: {__prev} != {__curr}")

        for label, a in task.tars.items():
            if not a.exists():
                return _NeedExecuteDecision(True, f"target does not exist: {label}")

            if self.test_targets_fingerprints:
                if label not in prev:
                    return _NeedExecuteDecision(True, f"target fingerprint is missing from backend: {label}")

                __prev = prev[label]
                __curr = self._fp.get_fingerprint(label, a)
                if __prev != __curr:
                    return _NeedExecuteDecision(True, f"target was changed: {label}: {__prev} != {__curr}")

        return _NeedExecuteDecision(False, "up-to-date")

    def _store_signature(self, task: _Task):
        if self.test_targets_fingerprints:
            aas = itertools.chain(task.deps.items(), task.tars.items())
        else:
            aas = task.deps.items()

        self.backend.set(
            self.dag_name,
            self.__class__.__name__,
            task.label,
            {
                label: self._fp.get_fingerprint(label, a)
                for label, a in aas
            }
        )

    def task_has_been_executed(self, task: _Task):
        self._store_signature(task)

        if self.strict_checks:
            for t, obj in task.tars.items():
                if not obj.exists():
                    raise MakeItError(f"Error in task {task.label}: target {t} has not been created."
                                      " Set `strict_checks` flag to false, if this check is not desired.")

        # invalidate cache
        for t in task.tars:
            self._fp.invalidate(t)


@dataclasses.dataclass
class ExecutionResult:
    executed_tasks: list[Task]
    skipped_tasks: list[Task]


class SimpleExecution:
    def __init__(self, dag: DAG, advisor: ExecutionAdviser, reporter: Reporter):
        self.dag = dag
        self.reporter = reporter
        self.advisor = advisor

    def execute(self) -> ExecutionResult:
        result = ExecutionResult([], [])

        graph = self.dag.create_dep_graph()

        # if targets is not None:
        #     graph = graph.subgraph(set(_.label() for _ in targets))

        ts = graphlib.TopologicalSorter(graph.dep_graph)
        ts.prepare()

        self.reporter.on_dag_start(self.dag.name, len(self.dag.tasks))

        unseen_nodes = set(self.dag.name2obj.keys())

        while ts.is_active():
            nodes = ts.get_ready()

            for name in nodes:
                if name in self.dag.tasks:
                    task = self.dag.tasks[name]

                    runtime_deps = {rd.label(): rd for rd in task.obj.runtime_dependencies()}

                    if unseen_nodes.intersection(runtime_deps.items()):
                        raise MakeItError(f"{name}'s runtime dependency depends on an unseen artifact")

                    task.deps.update(runtime_deps)

                    _ne = self.advisor.need_execute(task)

                    if _ne:
                        self.reporter.report_task_event(TaskEvent.EXECUTE, name, _ne.reason)

                        task.obj.execute()

                        self.advisor.task_has_been_executed(task)
                        self.reporter.report_task_event(TaskEvent.DONE, name, "done")
                        result.executed_tasks.append(self.dag.name2obj[name].obj)

                    else:
                        self.reporter.report_task_event(TaskEvent.SKIP, name, _ne.reason)
                        result.skipped_tasks.append(self.dag.name2obj[name].obj)

                ts.done(name)
                unseen_nodes.remove(name)

        self.reporter.on_dag_end()

        return result


class AIOExecution:
    def __init__(self, dag: DAG, advisor: ExecutionAdviser, reporter: Reporter,
                 max_queue_size=20, max_concurrent_workers=20):
        self.dag = dag
        self.reporter = reporter
        self.advisor = advisor

        self.graph = self.dag.create_dep_graph()
        self.ts = graphlib.TopologicalSorter(self.graph.dep_graph)
        self.ts.prepare()

        self.max_concurrent_workers = max_concurrent_workers
        self.max_queue_size = max_queue_size

    async def consume(self, q: asyncio.Queue):
        while True:
            task = await q.get()  # type: _Task
            await task.obj.a_execute()
            self.advisor.task_has_been_executed(task)
            self.reporter.report_task_event(TaskEvent.DONE, task.label, "done")
            self.ts.done(task.label)

            q.task_done()

    async def produce(self, q: asyncio.Queue):
        while self.ts.is_active():
            await asyncio.sleep(0)

            nodes = self.ts.get_ready()

            for n in nodes:
                if n in self.dag.tasks:
                    task = self.dag.tasks[n]

                    _ne = self.advisor.need_execute(task)
                    if _ne:
                        self.reporter.report_task_event(TaskEvent.EXECUTE, n, _ne.reason)
                        await q.put(task)
                    else:
                        self.reporter.report_task_event(TaskEvent.SKIP, n, _ne.reason)
                        self.ts.done(n)
                else:
                    self.ts.done(n)

    async def execute(self):
        self.reporter.on_dag_start(self.dag.name, len(self.dag.tasks))

        q = asyncio.Queue(maxsize=self.max_queue_size)
        prod = asyncio.create_task(self.produce(q))
        consumers = [asyncio.create_task(self.consume(q)) for _ in range(self.max_concurrent_workers)]

        await asyncio.gather(prod)
        await q.join()

        for c in consumers:
            c.cancel()

        self.reporter.on_dag_end()


class MultiprocessExecution:
    _SENTINEL = None

    @dataclasses.dataclass
    class _Traceback:
        tb_str: str
        task: str
        message: str

    def __init__(self, dag: DAG, advisor: ExecutionAdviser, reporter: Reporter,
                 max_concurrent_workers):
        self.dag = dag
        self.reporter = reporter
        self.advisor = advisor

        self.graph = self.dag.create_dep_graph()
        self.ts = graphlib.TopologicalSorter(self.graph.dep_graph)
        self.ts.prepare()

        if max_concurrent_workers <= 0:
            max_concurrent_workers = multiprocessing.cpu_count()

        self.max_concurrent_workers = max_concurrent_workers

    @staticmethod
    def consume(queue_tasks: multiprocessing.Queue, queue_done_tasks: multiprocessing.Queue):
        while True:
            task = queue_tasks.get(block=True)  # type: _Task

            if task == MultiprocessExecution._SENTINEL:
                return

            try:
                task.obj.execute()
            except Exception as exc:
                tb_str = traceback.format_exc()

                queue_done_tasks.put(
                    MultiprocessExecution._Traceback(tb_str, task=task.label, message=str(exc)),
                    block=True
                )

                return  # we are done

            queue_done_tasks.put(task.label, block=True)

    def execute(self) -> ExecutionResult:
        self.reporter.on_dag_start(self.dag.name, len(self.dag.tasks))

        queue_tasks = multiprocessing.Queue()
        queue_done_tasks = multiprocessing.Queue()

        consumers = [
            multiprocessing.Process(target=self.consume, args=(queue_tasks, queue_done_tasks),
                                    name=f"Consumer #{_}")
            for _ in range(self.max_concurrent_workers)
        ]

        for p in consumers:
            p.start()

        try:
            while self.ts.is_active():
                nodes = self.ts.get_ready()

                if nodes:
                    for n in nodes:
                        if n in self.dag.tasks:
                            task = self.dag.tasks[n]

                            _ne = self.advisor.need_execute(task)

                            if _ne:
                                self.reporter.report_task_event(TaskEvent.EXECUTE, n, _ne.reason)
                                queue_tasks.put(task)
                            else:
                                self.reporter.report_task_event(TaskEvent.SKIP, n, _ne.reason)
                                self.ts.done(n)
                        else:
                            self.ts.done(n)
                else:
                    label = queue_done_tasks.get(block=True)

                    if isinstance(label, MultiprocessExecution._Traceback):
                        self.reporter.report_task_event(TaskEvent.FAILURE, label.task, repr(label.message))
                        raise ChildProcessException(label.tb_str)

                    task = self.dag.tasks[label]
                    self.advisor.task_has_been_executed(task)
                    self.reporter.report_task_event(TaskEvent.DONE, label, "done")
                    self.ts.done(label)

            for _ in consumers:
                queue_tasks.put(MultiprocessExecution._SENTINEL)

            for _ in consumers:
                _.join()
                _.close()

            self.reporter.on_dag_end()

        except:
            # something went wrong here. Terminate everything and stop
            for _ in consumers:
                _.terminate()
                _.join()
                _.close()

            raise


def execute(dag: DAG, backend: AbstractBackend | None, advisor_class: Type[ExecutionAdviser],
            reporter: Reporter | None = SimpleReporter()):

    if reporter is None:
        reporter = Reporter()  # does nothing

    if backend is None:
        backend = DictBackend(None)

    advisor = advisor_class(dag.name, backend)
    _ex = SimpleExecution(dag, advisor, reporter)

    with backend:
        return _ex.execute()


def execute_on_change(tasks: Iterable[Task],
                      backend: IO | str | pathlib.Path | None = "makeit.json",
                      reporter: Reporter | None = SimpleReporter(),
                      dag_name: str = "main",
                      capture_only: bool = False,
                      execute_all: bool = False,
                      test_targets_fingerprints: bool = False,
                      strict: bool = True,
                      commit_on_failure: bool = True,
                      ):
    """ Execute task if on of the following is true:
        - task hasn't been executed before
        - task's dependencies has changed (md5 has changed)
        - one of the task's targets is missing
        - task has no dependencies

        File `backend` serves as a storage for execution. Creates one, if it does not exist.

        `Reporter` is used to log DAG execution, default implementation prints out colorized output to stderr.
        None can be used to make it silent.

        Set `dag_name` if you have several dags in one project, and you want to avoid names clashing.

        If parameter `capture_only` is set, tasks are not executed, only fingerprints are captured
            and stored in the backend. Can not be set simultaneously with execute_all.

        If parameter `execute_all` is set, all fingerprints are disregarded, everything will be executed.
            The advantage over `execute_always` is that all fingerprints are stored in the backend.

        Parameter `test_targets_fingerprints` controls checking of targets fingerprints. If it is set and
            a target has been modified externally, the task will be executed.

        Parameter `strict` controls tasks execution. If target is not created or dependency does not exist,
            exception is raised.

        Backend is always flushed to the disc (db, network, etc.) after a successful execution ("committed").
            However, if an exception is raised, then this behaviour is controlled by `commit_on_failure` parameter.
            Transaction idiom: if you want to do execute "everything or nothing", you can set this flag to False.
    """

    dag = DAG(dag_name)

    for t in tasks:
        dag.add(t)

    if reporter is None:
        reporter = Reporter()  # does nothing

    backend = DictBackend(backend, commit_on_failure=commit_on_failure)

    advisor = EARunOnChange(
        dag_name=dag_name,
        backend=backend,
        capture_only=capture_only,
        execute_all=execute_all,
        strict_checks=strict,
        test_targets_fingerprints=test_targets_fingerprints
    )
    _ex = SimpleExecution(dag, advisor, reporter)

    with backend:
        return _ex.execute()


def mp_execute_on_change(tasks: list[Task | Any],
                         backend: IO | str | pathlib.Path | None = "makeit.json",
                         reporter: Reporter | None = SimpleReporter(),
                         dag_name: str = "main",
                         n_jobs: int = -1,
                         execute_all: bool = False,
                         test_targets_fingerprints: bool = False,
                         strict: bool = True,
                         commit_on_failure: bool = True):

    """ Multiprocessing version of the function `execute_on_change`. See all details there.

        Parameter `n_jobs` controls the number of spawned worker-processes.
        Set it to -1 to use all available cores.
    """

    dag = DAG(dag_name)

    for t in tasks:
        dag.add(t)

    if reporter is None:
        reporter = Reporter()  # does nothing

    backend = DictBackend(backend, commit_on_failure=commit_on_failure)
    advisor = EARunOnChange(dag_name, backend, capture_only=False,
                            execute_all=execute_all, test_targets_fingerprints=test_targets_fingerprints,
                            strict_checks=strict)
    _ex = MultiprocessExecution(dag, advisor, reporter, max_concurrent_workers=n_jobs)

    with backend:
        return _ex.execute()


def aio_execute_on_change(tasks: list[Task | Any],
                          backend: IO | str | pathlib.Path | None = "makeit.json",
                          reporter: Reporter | None = SimpleReporter(),
                          dag_name: str = "main",
                          max_queue_size=20,
                          max_concurrent_workers=20,
                          execute_all=False,
                          test_targets_fingerprints=False,
                          strict=True,
                          commit_on_failure: bool = True,
                          debug=None):
    """ Additional to `execute_on_change` parameters:
        max_queue_size -- Size of the execution queue. Set it accordingly to the available resources.
        max_concurrent_workers -- Maximal number of async workers. Set it accordingly to the available resources.
        debug -- parameter is passed to `asyncio.run` function
    """

    dag = DAG(dag_name)

    for t in tasks:
        dag.add(t)

    if reporter is None:
        reporter = Reporter()  # does nothing

    backend = DictBackend(backend, commit_on_failure=commit_on_failure)
    advisor = EARunOnChange(dag_name, backend, capture_only=False, execute_all=execute_all,
                            test_targets_fingerprints=test_targets_fingerprints,
                            strict_checks=strict)

    _ex = AIOExecution(dag, advisor, reporter,
                       max_queue_size=max_queue_size, max_concurrent_workers=max_concurrent_workers)

    with backend:
        asyncio.run(_ex.execute(), debug=debug)


def execute_always(tasks: list[Task | Any],
                   reporter: Reporter | None = SimpleReporter(),
                   dag_name: str = "main"):

    dag = DAG(dag_name)

    for t in tasks:
        dag.add(t)

    if reporter is None:
        reporter = Reporter()  # does nothing

    backend = None
    advisor = EAAlwaysRun(dag_name, backend)
    _ex = SimpleExecution(dag, advisor, reporter)

    return _ex.execute()


def _load_artifact_object(dc_instance, o, _field_type):
    if isinstance(o, Artifact):
        yield o
    elif isinstance(o, (list, tuple)):
        for _ in o:
            yield from _load_artifact_object(dc_instance, _, type)
    else:
        # search in type registry
        for _type in o.__class__.mro():
            if _type in _dataclass_task_type_registry:
                yield _dataclass_task_type_registry[_type](o)
                break
        else:
            raise MakeItError(f"Could not load object {o} as Artifact."
                              " Did you forget to register it?")


class DataclassTask(Task):
    """ Wrapper for tasks-as-dataclasses: simple way to implement a task.

        A dataclass can inherit from this class to be endowed with
        `dependencies`, `targets` functions and other functionality.
    """

    verbose = False
    depends_on_source_code_of_self = True  # if set, creates automatic source-code artifact on self

    def __new__(cls, *args, **kwargs):
        """ Convert to dataclass if it is not a dataclass yet """
        if dataclasses.is_dataclass(cls):
            return super().__new__(cls)
        else:
            # default params are ok
            cls = dataclasses.dataclass(cls)

            return super().__new__(cls)

    def label(self):
        mixed = self.__str__()

        if 'object at 0x' in mixed:
            raise MakeItError("One of the DataclassTask's parameters does not implement __repr__.")

        if self.verbose:
            return mixed
        else:
            return f"{self.__class__.__name__}__{md5(mixed)}"

    def md5(self, suffix=""):
        """ Generate md5 of this task in the format
            ClassName__md5hash + suffix.

            Use it when a target name/path should be generated based on all parameters of the task,
            so that targets do not clash.
        """
        assert dataclasses.is_dataclass(self), "DataclassTask works only with dataclasses"

        if suffix:
            if not suffix.startswith("."):
                raise MakeItError(f"Suffix should start with `.`")

        return f"{self.__class__.__name__}__{md5(self.__str__())}{suffix}"

    def dependencies(self) -> Iterable[Artifact]:
        assert dataclasses.is_dataclass(self), "DataclassTask works only with dataclasses"

        for field in dataclasses.fields(self):
            obj = getattr(self, field.name)

            if field.type | Dependency == field.type or isinstance(obj, Dependency):
                yield from _load_artifact_object(self, obj, field.type)
            elif field.type | Target == field.type or isinstance(obj, Target):
                pass  # skip targets
            elif isinstance(obj, Artifact):
                raise MakeItError(f"Artifact {obj} must be annotated with Dependency or Target mark")

        yield from self.extra_dependencies()

        if self.depends_on_source_code_of_self:
            sc = SourceCode(self.__class__)

            try:
                sc.fingerprint()
                yield sc
            except OSError:
                warnings.warn(f"It is not possible to retrieve source code of {self.__class__}."
                              " Task will not be executed on changes of the source code.")
            except TypeError:
                pass

    def extra_dependencies(self) -> Iterable[Artifact]:
        """ Implement this method to generate additional dependencies """
        return []

    def targets(self) -> Iterable[Artifact]:
        assert dataclasses.is_dataclass(self), "DataclassTask works only with dataclasses"

        for field in dataclasses.fields(self):
            obj = getattr(self, field.name)

            if field.type | Target == field.type or isinstance(obj, Target):
                yield from _load_artifact_object(self, obj, field.type)
            elif field.type | Dependency == field.type or isinstance(obj, Dependency):
                pass  # skip dependencies
            elif isinstance(obj, Artifact):
                raise MakeItError(f"Artifact {obj} must be annotated with Dependency or Target mark")

        yield from self.extra_targets()

    def extra_targets(self) -> Iterable[Artifact]:
        """ Implement this method to generate additional targets """
        return []

    def parameters(self):
        """ Yields all other fields, that don't fall into dependency or target categories.
            Main usage case: plotting graph in graphviz
        """
        assert dataclasses.is_dataclass(self), "DataclassTask works only with dataclasses"

        for field in dataclasses.fields(self):
            obj = getattr(self, field.name)

            if field.type | Target == field.type or isinstance(obj, Target):
                pass  # skip targets
            elif field.type | Dependency == field.type or isinstance(obj, Dependency):
                pass  # skip dependencies
            elif isinstance(obj, Artifact):
                pass
            else:
                yield field.name, field.type, obj

    def execute(self):
        raise NotImplementedError()

    async def a_execute(self):
        pass


_dataclass_task_type_registry = {}


def register_type(type_: Type, constructor: Callable[[Any], Artifact]):
    """ Registry of external types for dataclasses.
        Sometimes it is more convenient to use domain types, rather than bare Artifacts.
        pathlib.Path is a good example. This registry makes it possible to automatically convert external types into
        according artifacts. For example
        ``` register_type(pathlib.Path, lambda _: File(_, checker=MD5Checker()) ```
        makes a File object with MD5 checker out of every Path object (which is marked with Target or Dependency flag).
    """
    _dataclass_task_type_registry[type_] = constructor


_parameter_type_registry = {}


# register default types
register_type(pathlib.Path, constructor=lambda _: File(_, MD5Checker()))
