"""
Default instances for dynamic runs.

Typically, developers will only run one digital worker on a Python
runtime, and it is tricky to initialize an object and pass that object
instance down into other files in a project for a custom decorator.
This package provides a set of default instances of objects and contexts
for dynamic runs.

This file initializes a shared `ReportBuilder` and `Recorder` for
individual steps and sub steps to share, then creates a default
`MainContext` named `supervise`, a decorator to annotate steps
called `step`, and a `StepContext` named `substep`.
"""

import pathlib
import warnings
from typing import Union

from supervisor.main_context import MainContext
from supervisor.recorder import Recorder
from supervisor.reporting.report_builder import ReportBuilder
from supervisor.step_context import StepContext
from supervisor.step_decorator_factory import create_step_decorator

report_builder = ReportBuilder()
#: A shared `ReportBuilder` for steps and sub-steps to add step reports to
recorder = Recorder()
#: A shared `Recorder` for steps and sub-steps to record messages to

step = create_step_decorator(report_builder, recorder)
#: Use this decorator on your own functions to mark what workflow step each
#: Python function is matched to.

fail_step = report_builder.fail_step
set_step_status = report_builder.set_step_status


#: Expose the report builder's ability to override a step's status as a top-level
#: call.


# noinspection PyPep8Naming
class step_scope(StepContext):
    def __init__(self, *id_args):
        """
        A default `StepContext` that uses the root level `report_builder` and `recorder`.

        Args:
            *id_args: The list of integers that represent the step ID.
        """
        super().__init__(report_builder, recorder, *id_args)


# noinspection PyPep8Naming
class substep(step_scope):
    """The deprecated version of `step_scope`."""

    def __init__(self, *id_args):
        warnings.simplefilter("once", DeprecationWarning)
        warnings.warn(
            f"`{self.__class__.__name__}` has been renamed to `step_scope`. Please use that class name instead.",
            DeprecationWarning,
            stacklevel=2,
        )
        warnings.simplefilter("default", DeprecationWarning)
        super().__init__(*id_args)


# noinspection PyPep8Naming
class supervise(MainContext):
    def __init__(
        self,
        manifest: Union[str, pathlib.Path] = "manifest.yaml",
        output_dir: Union[str, pathlib.Path] = "output/",
        *args,
        **kwargs,
    ):
        """
        A default `MainContext` that uses the root level `report_builder` and `recorder`.

        Args:
            *args: Extra arguments to the `MainContext` constructor.
            **kwargs: Extra keyword arguments to the `MainContext` constructor.
            manifest (str): The digital worker's manifest definition
            output_dir (str): Where the work report and drift report will
                be written to
        """
        super().__init__(
            report_builder=report_builder,
            recorder=recorder,
            manifest=manifest,
            output_dir=output_dir,
            *args,
            **kwargs,
        )
