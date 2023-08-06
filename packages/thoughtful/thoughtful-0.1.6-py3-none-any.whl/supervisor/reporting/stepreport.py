import sys

# typing.TypedDict introduced in python 3.8
# https://docs.python.org/3/library/typing.html#typing.TypedDict
if sys.version_info < (3, 8):
    from typing_extensions import typing as t
else:
    import typing as t

if t.TYPE_CHECKING:
    from ..step import StepId, StepReturn, StepStatus, StepType


class StepReport(t.TypedDict):
    """Fields for Step Reporting. At runtime, this is just a dictionary."""

    # stepdoc (manifest) details

    step_type: 'StepType'
    """Step Type"""

    step_id: 'StepId'
    """Stores the id of the step
    example: '1.1.2'"""

    step_status: 'StepStatus'
    """Runtime Status indicator"""

    title: str
    """The step Title"""

    description: str
    """The step description"""

    # runtime fields

    timestamp: str
    """UTC Timestamp of when this step was invoked"""

    duration: str
    """The duration of this step in seconds"""

    state: t.List[any]
    """The state property tracks state changes during the runtime of this step"""

    args: dict
    """Arguments defined at the start of this step"""

    returned: 'StepReturn'
    """The data returned from this step"""

    # Log any errors, exceptions, and warnings —
    #
    # We should strive to catch all potential errors, and append them to this
    # list. If an exception/error is thrown unexpectedly and breaks the
    # digitalworker, it should be logged in `fatal_error`.
    #
    # Warnings are a place for future ai to log information that is not
    # necessarily a breaking issue, but is something that should be noted.

    caught_exception: t.List[Exception]
    """Errors that occur during the execution owf this step. This should always
    be empty, unless there is a bug that a developer must squash."""

    fatal_error: t.Type[Exception]
    """Fatal errors are errors that occur unexpectedly during the execution of
    a step that causes a digital worker to stop all execution.
    """
    # Note: Long-term, in order to prevent a chaotic issues that processed
    # real-production data, but failed mid-way through execution— therefor,
    # creating a situation where a digital worker cannot finish it's work—
    # because the first set of steps are already processed.

    warnings: t.List[Warning]
    """Warnings are messages that could be an issue, maybe even an error, but
    are not necessarily a problem with the digitalworker. In fact, it could be
    messages about something that is theoretically handled properly by the code
    but could be a business-process issue."""
