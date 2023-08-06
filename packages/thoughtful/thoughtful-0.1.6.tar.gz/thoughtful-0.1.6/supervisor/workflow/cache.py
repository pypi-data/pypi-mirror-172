import typing as t

from ..step import Step, StepId


class WorkflowCache(object):
    """
    A cache of steps for the workflow engine.
    """
    _count: int
    # keeps tabs on the index of each assertion

    master: t.Tuple[Step]
    """Master list of steps preserved for refreshing queue on conditional steps."""

    reference: t.Dict[StepId, t.Tuple[int, str]]
    """A fast index and step-type reference for the master list of all steps."""

    def __init__(self):
        self.reset()

    def add(self, step: Step) -> None:
        """
        Index a step in the cache.

        :param step: Step to index
        """
        self.reference[step.step_id] = (self._count, step.step_type)
        self.master += (step,)
        self._count += 1

    def reset(self) -> None:
        """
        Clear the cache.
        """
        self._count = 0
        self.master = ()
        self.reference = {}

    def index_of(self, step_id: StepId) -> int:
        index, _ = self.reference[step_id]
        return index

    def length(self) -> int:
        """Determines if all work has been completed"""
        return len(self.master)
