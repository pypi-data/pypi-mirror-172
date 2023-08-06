"""
Default instances for dynamic runs.

Typically, developers will only run one digital worker on a Python
runtime, and it is tricky to initialize an object and pass that object
instance down into other files in a project for a custom decorator.
This package provides a set of default instances of objects and contexts
for dynamic runs.

This file initializes a shared `ReportBuilder` and `Recorder` for
individual steps and sub steps to share, then creates:

    - a default ``MainContext`` named ``supervise``,
    - a decorator to annotate steps called ``step``,
    - a ``StepContext`` named ``step_context``,
    - a function to set step statuses called ``set_step_status``,
    - and a function to set record statuses called ``set_record_status``.

See the quickstart for, well, quickstarts on each of these methods.
"""

import pathlib
import warnings
from typing import Optional, Union

from supervisor.main_context import MainContext
from supervisor.recorder import Recorder
from supervisor.reporting.report_builder import ReportBuilder
from supervisor.step_context import StepContext
from supervisor.step_decorator_factory import create_step_decorator

#: A shared ``ReportBuilder`` for steps and step contexts to add step reports
#: to.
report_builder = ReportBuilder()

#: A shared ``Recorder`` for steps and step contexts to record messages to.
recorder = Recorder()

#: Use this decorator on your own functions to mark what workflow step each
#: Python function is matched to.
step = create_step_decorator(report_builder, recorder)

#: Use this function to mark a step as failed.
#: This is just a shortcut for ``set_step_status(step_id, "failed")``.
#: Exposes ``report_builder.fail_step``.
fail_step = report_builder.fail_step

#: Expose the report builder's ability to override a step's status as a
#: top-level call. Exposes ``report_builder.set_step_status``.
set_step_status = report_builder.set_step_status

#: Expose the report builder's ability to override a step's record's status as a
#: top-level call. Exposes ``report_builder.set_record_status``.
set_record_status = report_builder.set_record_status


# noinspection PyPep8Naming
class step_scope(StepContext):
    """
    It's a context manager that provides a scope for a step using the
    aforementioned default instances of ``report_builder`` and ``recorder``.
    """

    def __init__(self, *step_id, record_id: Optional[str] = None):
        """
        A default `StepContext` that uses the root level `report_builder` and
        `recorder`.

        Args:
            *step_id: The list of integers that represent the step ID.
            record_id: An optional ID of the record being actively processed
        """
        super().__init__(report_builder, recorder, *step_id, record_id=record_id)


# noinspection PyPep8Naming
class substep(step_scope):
    """
    The deprecated version of ``step_scope``.
    """

    def __init__(self, *step_id):
        warnings.simplefilter("once", DeprecationWarning)
        warnings.warn(
            f"`{self.__class__.__name__}` has been renamed to `step_scope`. "
            f"Please use that class name instead.",
            DeprecationWarning,
            stacklevel=2,
        )
        warnings.simplefilter("default", DeprecationWarning)
        super().__init__(*step_id)


# noinspection PyPep8Naming
class supervise(MainContext):
    """
    It's a context manager that provides a scope for the main context using the
    aforementioned default instances of ``report_builder`` and ``recorder``.
    """

    def __init__(
        self,
        manifest: Union[str, pathlib.Path] = "manifest.yaml",
        output_dir: Union[str, pathlib.Path] = "output/",
        *args,
        **kwargs,
    ):
        """
        A default `MainContext` that uses the root level `report_builder` and
        `recorder`.

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
