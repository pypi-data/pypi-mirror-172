from __future__ import annotations

import functools
import json
from typing import Any, Callable, Dict, List, Optional

from supervisor.dynamic.report_builder import ReportBuilder, StepReportBuilder
from supervisor.dynamic.timer import Timer
from supervisor.manifest import StepStatus
from supervisor.recorder import Recorder


def create_step_decorator(
    report_builder: ReportBuilder, recorder: Recorder
) -> Callable:
    """
    A decorator to mark a function as the implementation of a step in a
    digital worker's manifest.

    Note that the return type here is `Any`, because proper type hinting
    for decorators is not yet obvious. PEP 612 specifies a way to type
    hint decorators starting in 3.10, but this project supports >= 3.7. See
    more here: https://stackoverflow.com/a/68290080/2597913.

    Returns:
        Any: A decorator to attach to functions.
    """

    # The decorator to be returned as the property
    # This handles the inputs to the decorator itself
    def returned_decorator(*id_args):
        step_id = _step_id_from_args(id_args)

        # The decorator to grab the function callable itself
        def inner_decorator(fn):
            # And the wrapper around the function to call it with its
            # args and kwargs arguments
            @functools.wraps(fn)
            def wrapper(*fn_args, **fn_kwargs):
                return _run_wrapped_func(
                    fn, step_id, report_builder, recorder, *fn_args, **fn_kwargs
                )

            return wrapper

        return inner_decorator

    return returned_decorator


def _run_wrapped_func(
    fn: Callable,
    step_id: str,
    report_builder: ReportBuilder,
    recorder: Recorder,
    *fn_args: List,
    **fn_kwargs: Dict,
) -> Any:
    """
    Runs `fn` with the given args `args` and `kwargs`, times how long it
    takes to run, and records the execution of this function under `step_id`
    in the work report.

    Args:
    fn (Callable): The function to run.
    step_id (str): The ID of the step representing the function to
    execute.
    *args (List): The input arguments to the function.
    **kwargs (Dict): The input keyword arguments to the function.

    Returns:
    Any: Whatever is returned by executing the function
    """

    """Set up the step"""
    caught_exception: Optional[Exception] = None
    step_final_status: StepStatus

    # Time the function
    func_timer = Timer()
    func_timer.start()

    """Run the step"""
    try:
        fn_result = fn(*fn_args, **fn_kwargs)
        step_final_status = StepStatus.COMPLETE
    except Exception as ex:
        fn_result = None
        caught_exception = ex
        step_final_status = StepStatus.ERROR
    timer_result = func_timer.end()

    """Step teardown"""
    # Combine the linear args and keyword args into one dict
    args_as_dict = {"": fn_args} if fn_args else {}
    all_inputs = {**args_as_dict, **fn_kwargs}

    safe_args = to_safe_jsonable(all_inputs)
    safe_outputs = to_safe_jsonable(fn_result)

    # Create a new step report
    new_report = StepReportBuilder(
        step_id=step_id,
        start_time=timer_result.start,
        end_time=timer_result.end,
        duration=timer_result.duration,
        status=step_final_status,
        args=safe_args,
        outputs=safe_outputs,
        message_log=recorder.messages,
        data_log=recorder.data,
    )
    report_builder.workflow.append(new_report)

    # Reset the recorder for the next step
    recorder.messages = []
    recorder.data = []

    """Passthrough the step's return value or raised exception"""
    # If the step failed and raised an exception, raise that instead
    # of returning None
    if caught_exception:
        raise caught_exception

    # Passthrough the function's returned data back up
    return fn_result


def _step_id_from_args(args: tuple) -> str:
    """
    Joins decorator number args into a step ID string.

    Args:
    args (tuple): The arguments to the decorator.

    Returns:
    str: The step ID.
    """
    return ".".join([str(arg) for arg in args])


def to_safe_jsonable(value: Any) -> Any:
    """
    Returns a version of `value` that can be converted into JSON
    format using the `json` library.

    Args:
        value: The value to ensure is safe to JSON serialize.

    Returns:
        Any: The JSON safe value
    """
    try:
        json.dumps(value)
        return value
    except TypeError:
        # Continue parsing below
        pass

    # Check if object has a .__json__() method
    json_attribute = getattr(value, "__json__", None)
    if callable(json_attribute):
        return value.__json__()

    if type(value) is list:
        return [to_safe_jsonable(i) for i in value]
    if type(value) is tuple:
        return tuple(to_safe_jsonable(i) for i in value)
    if type(value) is dict:
        return {k: to_safe_jsonable(v) for k, v in value.items()}

    # Use the raw string as a last resort
    return str(value)
