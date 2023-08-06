from makeit.core import Reporter, TaskEvent
import tqdm


class TqdmExecutionReporter(Reporter):
    """ Tqdm wrapper when a lot of tasks are being executed.
        Shows progress-bar
    """

    def __init__(self):
        self.bar = None

    def on_dag_start(self, dag_name: str, total_number_of_tasks: int):
        self.bar = tqdm.tqdm(total=total_number_of_tasks, desc=dag_name)

    def report_task_event(self, event: TaskEvent, task_name: str, reason: str):
        if event in [TaskEvent.DONE, TaskEvent.SKIP, TaskEvent.FAILURE, TaskEvent.IGNORE]:
            self.bar.update()
