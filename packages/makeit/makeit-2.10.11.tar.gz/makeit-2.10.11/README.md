# MAKE IT!
GNU Make for applications.

- Extensible execution model language
- Expressive and concise task description language
- Task are not deferred to remote
- Build-in async support

## Rationale
Rethinking of Doit package.

## Similar libraries -- what's different
See Luigi, Airflow, doit.

## Main concepts

Two main concepts of the library are Task and Artifact.
A task depends on artifacts and produces artifacts.

The use of artifacts is twofold. First, artifacts are used to build a graph (DAG) of the execution.
On the other side, artifacts' fingerprints (i.e., md5) are used to define weather task should be run or not.

## Task definition
The simplest way to define a task is to derive a dataclass class from makeit.DataclassTask
and implement method `execute`, as in the example below.

The class makeit.DataclassTask closely interweaves with the standard dataclasses library,
allowing users to benefit from a rich dataclasses support from IDEs.

One implicit dependency is the source code if a task (obtained by inspect.getsource(task.__class__)),
if variable DataclassTask.depends_on_source_code_of_self is set (it is set by default).
However, this is not available in the environments like Jupyter.

```python
import dataclasses
from makeit import File, Dependency, Target, DataclassTask
from pathlib import Path

@dataclasses.dataclass
class Process(DataclassTask):  # derive from DataclassTask -- this adds required and additional functions like dependencies, ...
    input_1: Path | Dependency  # this is a file dependency
    input_2: Path | Dependency  # many dependencies are possible
    many_files: list[Path] | Dependency  # and even list of dependencies allowed

    parameter: float  # this is a parameter -- not a dependency or a target
                      # however, it is used in label() method (via dataclasses method __str__),
                      # therefore it helps to parametrize tasks.
                      # See also method DataclassTask.md5 -- it is helpful for creating unique target names.

    target: File | Target  # many targets are possible as well
    
    target_2: File | Target = None  # this can be initialized in the dataclasses default method __post_init__

    class_variable = 12  # this is a class variable -- makeit disregards it, as dataclasses does.
    
    def __post_init__(self):
        # our task has parameters (parameter: float)
        # -- so it is better to save results into a unique target (file in this example)
        # DataclassTask.md5 is roughly equivalent to md5hash(str(self)).
        self.target_2 = Path('datafolder') / self.md5(".csv")

    def execute(self):
        # Implement task's logic
        text = self.input_1.read_text() + self.input_2.read_text()
        self.target.path.write_text(text)
```

## Tasks execution
The simplest way to execute tasks is to use the function `execute_on_change`:
```python
from makeit import execute_on_change

tasks = [...]
execute_on_change(tasks, backend="makeit.json")
```

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


## Execution reporting
There is a build-in logging execution reporter.

Example with `TqdmReporter`

```python
from makeit.core import Reporter, TaskEvent


class TqdmReporter(Reporter):
    def report_task_event(self, event: TaskEvent, task_name: str, reason: str | None):
        pass

    def on_dag_start(self, dag_name: str, total_number_of_tasks: int):
        pass

    def on_dag_end(self):
        pass
```

## Using graphviz to plot DAG
```python
from makeit.contrib.graphviz import render_online, create_dot

tasks = [...]

dot = create_dot(tasks)  # graphviz.Digraph can be rendered to pdf, png, ...
render_online(dot, 'https://...')  # ... or simply drawn online
```
Some remarks:
- dotted lines connect task with its parameters
- file artifacts are marked by a folder-shaped box
- green or red color denote weather file exists or not
- labels are shortened as much as possible in order to get readable picture


## Advanced tasks execution
Use `makeit.mp_execute_on_change` to run tasks in multiprocessing. This function has almoust the 
same signature as `execute_on_change`, however it has additional parameter `n_jobs` controlling number of
worker processes.

Use `makeit.aio_execute_on_change` to 
run async tasks (in this case method `async def a_execute(self)` should be implemented instead).
This function has also own specific parameters controlling queue size and number of async tasks.

## Advanced task definition
Registering a type conversion.

Subclass directly from `makeit.core.Task` and implement all needed abstract methods.

Extra dependencies/targets. Task dependencies.

## Typical workflows

| Workflow  | Description                                         | Backend role                                                    |
|-----------|-----------------------------------------------------|-----------------------------------------------------------------|
| Make      | Execute task if targets are older than dependencies | -                                                               |
| "Luigi"   | Execute task if and only if target does not exist   | -                                                               |
| Make 2.0  | Execute task if dependency has changed              | Fingerprint is stored in backend, i.e. MD5 or modification time |
| Luigi 2.0 | Pickup new files from folder, parse and process     | Backend remembers which files have been already seen            |
| Always    | Execute all tasks (in correct order)                | -                                                               |

### Make
Compare files' timestamps, if dependencies are newer than targets then recalculate the targets.

### "Luigi"
Run task if and only if targets are absent.

