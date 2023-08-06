"""
Default instances for dynamic runs.

Typically, developers will only run one digital worker on a Python
runtime, and it is tricky to initialize an object and pass that object
instance down into other files in a project for a custom decorator.
This package provides a set of default instances of objects and contexts
for dynamic runs.

If desired, you can create your own instances of these objects like
``FunctionRunner`` and ``SuperviseContext``, particularly if you want
to run unit tests against multiple digital workers.
"""

from supervisor.dynamic.function_runner import FunctionRunner
from supervisor.dynamic.report_builder import DynamicWorkReportBuilder
from supervisor.dynamic.supervise_context import SuperviseContext

_DEFAULT_REPORT_BUILDER = DynamicWorkReportBuilder()
_DEFAULT_RUNNER = FunctionRunner(report_builder=_DEFAULT_REPORT_BUILDER)

# Expose the decorator and report_builder for the default instance
step = _DEFAULT_RUNNER.step_decorator
#: Use this decorator on your own functions to mark what workflow step each
#: Python function is matched to.

reporter = _DEFAULT_RUNNER.report_builder
#: The default ``Reporter`` instance for your dynamic digital worker.

recorder = _DEFAULT_RUNNER.recorder
#: The default ``Recorder`` instance for your dynamic digital worker.


# noinspection PyPep8Naming
class supervise(SuperviseContext):
    def __init__(self, *args, **kwargs):
        super().__init__(runner=_DEFAULT_RUNNER, *args, **kwargs)
