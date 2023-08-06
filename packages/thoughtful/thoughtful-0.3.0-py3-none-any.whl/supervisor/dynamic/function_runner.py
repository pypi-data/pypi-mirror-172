from __future__ import annotations

import datetime
import functools
import json
import time
from typing import Any, Callable, Dict, List

from supervisor.dynamic.drift_report import DriftReport
from supervisor.dynamic.report_builder import DynamicStepReportBuilder
from supervisor.dynamic.report_builder import DynamicWorkReportBuilder
from supervisor.manifest import Manifest
from supervisor.recorder import Recorder


class FunctionRunner:
    def __init__(self, report_builder: DynamicWorkReportBuilder):
        """
        Wraps steps in a digital worker to create a work report of the worker's
        execution. Provides a decorator--`self.step_decorator`--to add onto
        functions to mark what step in a DW workflow the Python function is
        executing.

        Attributes:
            self.report_builder (DynamicWorkReportBuilder): Writes the work report as functions
                decorated by this instance's `step_decorator` property are
                called.
            self.recorder (Recorder): A recorder.
        """
        self.report_builder = report_builder
        self.recorder = Recorder()

    def finish_reports(self, manifest: Manifest) -> tuple:
        work_report = self.report_builder.to_report(manifest)
        drift_report = DriftReport.from_dw_run(manifest, work_report)
        return work_report, drift_report

    @property
    def step_decorator(self) -> Any:
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
            step_id = self._step_id_from_args(id_args)

            # The decorator to grab the function callable itself
            def inner_decorator(fn):
                # And the wrapper around the function to call it with its
                # args and kwargs arguments
                @functools.wraps(fn)
                def wrapper(*fn_args, **fn_kwargs):
                    return self._run_wrapped_func(fn, step_id, *fn_args, **fn_kwargs)

                return wrapper

            return inner_decorator

        return returned_decorator

    def _run_wrapped_func(
        self, fn: Callable, step_id: str, *args: List, **kwargs: Dict
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

        # Time the function
        start_timestamp = datetime.datetime.utcnow()
        start = time.perf_counter()
        fn_result = fn(*args, **kwargs)
        end = time.perf_counter()
        end_timestamp = datetime.datetime.utcnow()

        duration_seconds = end - start
        duration_delta = datetime.timedelta(seconds=duration_seconds)

        # Combine the linear args and keyword args into one dict
        args_as_dict = {"": args} if args else {}
        all_inputs = {**args_as_dict, **kwargs}

        safe_args = to_safe_jsonable(all_inputs)
        safe_outputs = to_safe_jsonable(fn_result)

        # Create a new step report
        new_report = DynamicStepReportBuilder(
            step_id=step_id,
            start_time=start_timestamp,
            end_time=end_timestamp,
            duration=duration_delta,
            args=safe_args,
            outputs=safe_outputs,
            message_log=self.recorder.messages,
            data_log=self.recorder.data,
        )
        self.report_builder.workflow.append(new_report)

        # Reset the recorder for the next step
        self.recorder.messages = []
        self.recorder.data = []

        # Passthrough the function's returned data back up
        return fn_result

    @staticmethod
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
