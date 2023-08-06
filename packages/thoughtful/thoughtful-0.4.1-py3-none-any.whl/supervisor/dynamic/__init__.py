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
called `step`, and a `SubStepContext` named `substep`.
"""

from supervisor.dynamic import substep_context
from supervisor.dynamic.main_context import MainContext
from supervisor.dynamic.report_builder import ReportBuilder
from supervisor.dynamic.step_decorator_factory import create_step_decorator
from supervisor.dynamic.substep_context import SubStepContext
from supervisor.recorder import Recorder

report_builder = ReportBuilder()
#: A shared `ReportBuilder` for steps and sub-steps to add step reports to
recorder = Recorder()
#: A shared `Recorder` for steps and sub-steps to record messages to


step = create_step_decorator(report_builder, recorder)
#: Expose the decorator and report_builder for the default instance


#: Use this decorator on your own functions to mark what workflow step each
#: Python function is matched to.


# noinspection PyPep8Naming
class substep(SubStepContext):
    def __init__(self, *id_args):
        """
        A default `SubStepContext` that uses the root level `report_builder` and `recorder`.

        Args:
            *id_args: The list of integers that represent the step ID.
        """
        super().__init__(report_builder, recorder, *id_args)


# noinspection PyPep8Naming
class supervise(MainContext):
    def __init__(self, *args, **kwargs):
        """
        A default `MainContext` that uses the root level `report_builder` and `recorder`.

        Args:
            *args: Extra arguments to the `MainContext` constructor.
            **kwargs: Extra keyword arguments to the `MainContext` constructor.
        """
        super().__init__(
            report_builder=report_builder, recorder=recorder, *args, **kwargs
        )
