from ..step import Step, StepId
from .cache import WorkflowCache
from .errors import WorkflowCacheError


class WorkflowFactory():
    """
    Workflow Factory - Processes stepdocs from the Manifest, and creates
    an adds each step, in the order in which they are defined by the workflow,
    to the workflow cache for being processed through the workflow iterator.
    """

    cache: WorkflowCache

    def __init__(self, workdoc, cache):
        """
        Create a new WorkflowFactory instance.
        """
        self.cache = cache
        self.process(workdoc)

    def process(self, workdoc: dict) -> None:
        """Provided a manifest workdoc dict, this method will create a
        priority queue of steps to be executed."""

        # Process the manifest by iterating over it's steps and mapping those
        # steps to the steps available in the manifest.
        for macro_step in workdoc:
            self.create_step(macro_step)

        # for good measure, ensure that there are no additional cached
        # steps in the workflow, which would mean there is some kind of
        # inconsistency in the manifest vs the digital worker's implimentation
        if Step.get_cache_size():
            raise WorkflowCacheError(
                "DigitalWorker contains implimentation step methods " +
                "that are not in the manifest: " + f"{Step.get_cache_ids()}")

        # Create an immutable copy of the steps as a master queue
        # for refreshing the flow on conditional steps.
        # self.cache.save(self._temp)

    def create_step(self, stepdoc: dict) -> None:
        """Creates a new `Step` instance with the step_id, title, description, etc
        from a manifest, and match it with the digital workers implimentation
        methods. `fn_required` is used to determine if the step should
        complain if a method is not found. While macrosteps are not required
        at runtime, all other steps should have an implimentation step,
        otherwise something is out of sync."""
        step_id: StepId = str(stepdoc.get("step_id"))
        children = stepdoc.get("steps", [])

        # Add step to the workflow cache
        self.cache.add(Step(step_id, stepdoc))

        # This is a recursive process, as every step may have a list of children
        # steps and each of those may contain more, so this calls itself anytime
        # it finds a list of children steps. This must be done after the parent
        # step is added to the cache, otherwise the order won't be maintained.
        for child in children:
            self.create_step(child)
