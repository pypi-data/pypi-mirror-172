from __future__ import annotations

from enum import Enum
from typing import Any, Dict, List, Optional, TypeVar
from uuid import UUID, uuid4

from pydantic import BaseModel, Extra, Field, ValidationError, constr, validator
from pydantic_yaml import SemVer, VersionedYamlModel


# use in init to get manifest, filter through 'steps' if available into new step models
class Manifest(VersionedYamlModel):
    class Config:
        min_version = "1.0.0"
        max_version = "1.9.0"

    uid: str
    name: str
    description: str
    author: str
    source: str
    version: SemVer
    workflow: List
    steps_by_id: Optional[Dict] = None

    def set_steps_by_id(self):
        self.steps_by_id = Step.to_flat_dict(self.workflow)

    def to_report(self) -> dict[str, Any]:
        """
        Returns the values of this instance as a dictionary that are needed
        for a report.
        """
        # Only return the keys we want in the report
        keys = ["uid", "name", "description", "author", "source"]
        value = {k: v for k, v in self.__dict__.items() if k in keys}
        return value

    # @classmethod - issue replacing directly with classmethod
    # def from_yaml(cls, path: t.Union[pathlib.Path, str]) -> Manifest:
    #     yaml_data = pyconfs.Configuration.from_file(path).as_dict()
    #     return cls(**yaml_data)


class Step(BaseModel):
    # add additional constraints on these fields
    uid: UUID = Field(default_factory=uuid4)
    step_id: str
    title: str
    description: str
    steps: Optional[List[Step]] = None
    when_false: Optional[str]
    when_true: Optional[str]

    @validator("steps", pre=True, always=True)
    def set_steps(cls, steps):
        return steps or []

    @classmethod
    def to_flat_dict(cls, steps: List[Step]) -> Dict[str, Step]:
        flat = {}
        for step in steps:
            flat[step.step_id] = step
            child_values = Step.to_flat_dict(step.steps)
            flat.update(child_values)

        return flat

    @classmethod
    def from_manifest(cls, step_doc: dict) -> Step:
        return cls(**step_doc)

    @property
    def has_children(self) -> bool:
        return True if self.steps and len(self.steps) else False

    @property
    def is_conditional(self) -> bool:
        return (self.when_true is not None) or (self.when_false is not None)

    @property
    def step_type(self) -> StepType:
        if self.is_conditional:
            return StepType.CONDITIONAL
        return StepType.SEQUENTIAL

    def next_from_condition(self, condition: bool) -> str:
        if not self.is_conditional:
            raise RuntimeError("This step is not conditional")
        if type(condition) is not bool:
            raise TypeError("condition must be bool")

        next_id = self.when_true if condition else self.when_false
        if next_id is None:
            raise RuntimeError("Either your when_true or when_false is invalid")
        return next_id


class StepType(str, Enum):
    """StepType — by default, steps run in sequential order.

    A conditional step will determine the default_next step at runtime based on the
    step_outputs of that step.

    If a step defines a `when_true` or `when_false` (a string of the default_next
    step id) then that step is considered conditional. After a conditional step
    is executed, the workflow iterator will compare the return value to
    the proceed_to[bool] value. If no value is provided to the"""

    SEQUENTIAL = "sequential"
    CONDITIONAL = "conditional"


class StepStatus(str, Enum):
    """StepStatus — The status of the current state of the step.

    READY: The step is locked and loaded
    RUNNING: The step is currently running
    COMPLETE: The step has completed
    RETRY: The step has failed, and will be retried
    ERROR: The step has failed"""

    READY = "ready"
    RUNNING = "running"
    COMPLETE = "complete"
    RETRYING = "retrying"
    ERROR = "error"


StepId = TypeVar("StepId", bound=str)
