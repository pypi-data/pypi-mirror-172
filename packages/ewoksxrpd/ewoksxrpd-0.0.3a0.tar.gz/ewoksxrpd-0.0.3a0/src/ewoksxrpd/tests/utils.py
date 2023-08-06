from typing import List, Mapping, Optional
from ewoksorange.bindings.taskwrapper import execute_ewoks_owwidget


def execute_task(
    task_class,
    widget_class,
    inputs: Optional[List[Mapping]] = None,
    widget: Optional[bool] = None,
    timeout: int = 3,
) -> dict:
    """Execute the task (use the orange widget or ewoks task class) and return the results"""
    if widget:
        return execute_ewoks_owwidget(widget_class, inputs=inputs, timeout=timeout)
    else:
        task = task_class(inputs=inputs)
        task.execute()
        return task.output_values
