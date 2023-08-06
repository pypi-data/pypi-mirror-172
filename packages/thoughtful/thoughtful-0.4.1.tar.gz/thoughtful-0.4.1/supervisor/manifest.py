from __future__ import annotations

from enum import Enum
from typing import Any, Dict, List, Optional, TypeVar
from uuid import UUID, uuid4

from pydantic import BaseModel, Field, validator
from pydantic_yaml import VersionedYamlModel


class StepType(str, Enum):
    """
    StepType — by default, steps run in sequential order.

    A conditional step will determine the _next step at runtime based on the
    step_outputs of that step.

    If a step defines a `when_true` or `when_false` (a string of the next
    step id) then that step is considered conditional. After a conditional step
    is executed, the workflow iterator will compare the return value to
    the proceed_to[bool] value. If no value is provided to those properties,
    the next step in the sequence is executed.
    """

    SEQUENTIAL = "sequential"
    CONDITIONAL = "conditional"
    BRANCH = "branch"
    UNKNOWN = "unknown"


class StepStatus(str, Enum):
    """
    StepStatus — The status of the current state of the step.

    READY: The step is locked and loaded
    RUNNING: The step is currently running
    COMPLETE: The step has completed
    RETRY: The step has failed, and will be retried
    ERROR: The step has failed
    """

    READY = "ready"
    RUNNING = "running"
    COMPLETE = "complete"
    RETRYING = "retrying"
    ERROR = "error"


StepId = TypeVar("StepId", bound=str)


class Step(BaseModel):
    """
    A step to execute in a manifest workflow.

        uid (UUID) = Field(default_factory=uuid4)
        step_id (str): The ID of the step.
        title (str): The name of the step.
        description (str): A description of the step.
        steps (List[Step]): A list of children steps. Empty list if no children.
        when_false (str, optional): The next step ID if the previous step
            returned `False`. Defaults to None.
        when_true (str, optional): The next step ID if the previous step
            returned `True`. Defaults to None.
    """

    uid: UUID = Field(default_factory=uuid4)
    step_id: str
    step_type: StepType
    title: str
    description: Optional[str]
    steps: Optional[List[Step]] = None
    branches: Optional[Dict[Any, Any]]
    when_false: Optional[str]
    when_true: Optional[str]

    # PyCharm can't recognize that `@validator` creates a class method
    # noinspection PyMethodParameters
    @validator("steps", pre=True, always=True)
    def set_steps(cls, steps):
        return steps or []

    @classmethod
    def to_flat_dict(cls, steps: List[Step]) -> Dict[str, Step]:
        """
        Creates a flat dictionary of a list of steps, where each step's children
        is added to the flat dictionary.

        Args:
            steps (List[Step]): The steps to flatten.

        Returns:
            Dict[str, Step]: The steps as a flat dict. The keys are the step IDs
                and the values are the ``Step``s.
        """

        flat = {}
        for step in steps:
            flat[step.step_id] = step
            child_values = Step.to_flat_dict(step.steps)
            flat.update(child_values)

        return flat

    @property
    def has_children(self) -> bool:
        """
        Says whether this instance has children ``Step``s.

        Returns:
            bool: True if this instance has children, False otherwise.

        """
        return True if self.steps and len(self.steps) else False


class Manifest(BaseModel):
    """
    A digital worker manifest, typically read from a `manifest.yaml` file.
    Attributes:
        uid (str): The ID of the manifest.
        name (str): The name of the manifest.
        description (str): Manifest description.
        author (str): Who wrote the manifest.
        source (str): Where the manifest came from.
        workflow (List[Step]): The list of steps to execute.
        steps_by_id (dict): The same ``Step``s as `self.workflow`, but as a
            dictionary, where the keys are the ``Step`` IDs.
    """

    uid: str
    name: str
    description: str
    author: Optional[str]
    source: str
    workflow: List
    steps_by_id: Optional[Dict]  # This will get set after model initialization

    def set_steps_by_id(self):
        self.steps_by_id = Step.to_flat_dict(self.workflow)

    def __json__(self) -> dict[str, Any]:
        """
        Returns the values of this instance as a dictionary that are needed
        for a report.
        Returns:
            dict: The JSON-able dictionary (of only primitives) representation
                of this instance.
        """
        # Only return the keys we want in the report
        keys = ["uid", "name", "description", "author", "source"]
        value = {k: v for k, v in self.__dict__.items() if k in keys}
        return value
