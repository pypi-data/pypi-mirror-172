import typing as t
from collections import deque

from ..step import Step, StepId, StepStatus, StepType
from .cache import WorkflowCache
from .errors import WorkflowEngineError
from .factory import WorkflowFactory


# Workflow ==================================================================-->
#
# The `Supervisor` looks to `Workflow` to parse the manifest workflow
# configuration, and handle execution flow and mapping.
class Workflow:
    """
    The `Supervisor` looks to `Workflow` to parse the manifest workflow
    configuration, and handle execution flow and mapping.
    """

    active_step: Step
    """ The step currently being executed or last executed prior to the next
    being invoked"""

    _workdoc: dict
    # Original workflow documentation from the manifest

    _cache: WorkflowCache
    # sorted master steps

    _cache: WorkflowCache
    # sorted master steps

    _queue: t.List[Step]

    # deque stack

    def __init__(self, workdoc: dict):
        """Initialize a workflow with the manifest workflow documentation."""
        self._workdoc = workdoc
        self._cache = WorkflowCache()
        self._factory = WorkflowFactory(workdoc, self._cache)
        self._master = self._cache.master

    def done(self):
        """Determines if all work has been completed"""
        return len(self._queue) == 0

    def __iter__(self):
        """The it erator interface

        Example:
            >>> workflow = {
                    step_id: {'step_id': 1, 'title': 'Step Title'},
                    step_id: {'step_id': 2, 'title': 'Step Title'},
                }
            >>> work = iter(Workflow(workflow))
            >>> next(work)
            <Step: step_id: step_1, title: Step 1, description: Step 1 description>
            >>> next(work)
            <Step: step_id: step_2, title: Step 2, description: Step 2 description>

        Returns: self
        """
        self._queue = deque(self._master)
        return self

    def __next__(self) -> Step:
        """The iterator interface for `next`

        Example:
            >>> workflow = {
                    step_id: {'step_id': 1, 'title': 'Step Title'},
                    step_id: {'step_id': 2, 'title': 'Step Title'},
                }
            >>> work = iter(Workflow(workflow))
            >>> next(work)
            <Step: step_id: step_1, title: Step 1, description: Step 1 description>
            >>> next(work)
            <Step: step_id: step_2, title: Step 2, description: Step 2 description>
        """

        try:
            step = self._queue.popleft()
        except IndexError:
            raise WorkflowEngineError(
                "Trying to determine next step, but there is no next step." +
                "Please check the `DigitalWorker` implementation, and the manifest."
                + "If this is a bug in `Supervisor`, please report it.")
        return step

    def validate(self, step: Step) -> None:
        if step.step_status != StepStatus.COMPLETE:
            raise WorkflowEngineError(
                'Trying to determine next step before the current step has ' +
                'finished executing. This is likely a bug in Supervisor.')
        # If the step that just ran was a conditional step,
        # we need to reset the queue and start from the step id
        # defined for that result.
        if step.step_type == StepType.CONDITIONAL:
            next_step_id: StepId = step.conditional_result()
            if next_step_id:
                next_step_index = self._cache.index_of(next_step_id)
                self.refresh(next_step_index)

    def refresh(self, index: int) -> None:
        """
        Refresh the workflow queue.

        :param index: The index of the step to start from.
        """
        self._queue = deque(self._master[index:])

    def __len__(self) -> int:
        """This returns the total number of steps in the workflow"""
        return self._cache.length()

    def __repr__(self) -> str:
        return f"DigitalWorkflow: Steps={self._cache.master}"
