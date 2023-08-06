from __future__ import annotations

import json
import pathlib
from collections import defaultdict
from enum import Enum
from typing import Any, Dict, List, Optional, TypeVar, Union

import pydantic
import yaml
from pydantic import validator
from pydantic_yaml import YamlModel


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
    # Use "unknown" for steps indicated by the dev that aren't in the manifest
    UNKNOWN = "unknown"


StepId = TypeVar("StepId", bound=str)


class RecordStatusColumns(YamlModel):
    """
    Columns is a list of column names that are used to display the
    output of a step in a table.
    """

    succeeded: Optional[str]
    """The name of the column that contains the succeeded records."""
    failed: Optional[str]
    """The name of the column that contains the failed records."""
    warning: Optional[str]
    """The name of the column that contains the warning records."""


class Step(YamlModel):
    """
    A step to execute in a manifest workflow.
    """

    step_id: str
    """The ID of the step."""
    step_type: StepType
    """The type of step."""
    title: str
    """The name of the step."""
    description: Optional[str]
    """A description of the step."""
    steps: Optional[List[Step]] = None
    """A list of children steps. Empty list if no children."""
    branches: Optional[Dict[Any, Any]]
    """A dictionary of branches to execute."""
    when_false: Optional[str]
    """The next step ID if the previous step returned `False`."""
    when_true: Optional[str]
    """The next step ID if the previous step returned `True`."""
    columns: Optional[RecordStatusColumns]
    """The columns to display in the UI for record statuses. If none, it will
    use manifest defaults."""

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
                and the values are the ``Step`` s.
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
        Says whether this instance has children ``Step`` s.

        Returns:
            bool: True if this instance has children, False otherwise.

        """
        return True if self.steps and len(self.steps) else False


class Manifest(YamlModel):
    """
    A digital worker manifest, typically read from a `manifest.yaml` file.
    """

    uid: str
    """The ID of the manifest."""
    name: str
    """The name of the manifest."""
    description: str
    """Manifest description."""
    author: Optional[str]
    """Who wrote the manifest."""
    source: str
    """Where the manifest came from."""
    columns: Optional[RecordStatusColumns]
    """The columns to display in the UI for record statuses. If none, it
    will use defaults."""
    workflow: List[Step]
    """The list of steps to execute."""
    steps_by_id: Optional[Dict]
    """The same ``Step`` s as `self.workflow`, but as a dictionary, where the
    keys are the ``Step`` IDs."""

    def set_steps_by_id(self) -> None:
        """
        After loading from a YAML/dict, this function creates a dictionary
        that maps step IDs to steps.
        """
        self.steps_by_id = Step.to_flat_dict(self.workflow)

    @classmethod
    def from_file(cls, filename: Union[str, pathlib.Path]) -> Manifest:
        """
        Creates an instance of this class from a YAML file.

        Args:
            filename: The name of the manifest .yaml file.

        Returns:
            Manifest: The new Manifest instance.
        """
        # Load the manifest using the base class importer
        try:
            manifest_in_flight = cls.parse_file(str(filename))
        except pydantic.error_wrappers.ValidationError as ex:
            errors = ex.errors()
            error_message = f"Invalid manifest file with {len(errors)} validation error(s) at the root level\n{_pretty_errors_string(errors)}"
            raise ValueError(error_message) from ex

        # The base importer loads the steps as dicts, so convert them into
        # proper steps
        step_dicts = manifest_in_flight.workflow
        final_steps: List[Step] = cls._load_manifest_file_steps(step_dicts)
        manifest_in_flight.workflow = final_steps
        manifest_in_flight.set_steps_by_id()

        return manifest_in_flight

    @classmethod
    def yaml_to_json(
        cls,
        manifest_path: Union[str, pathlib.Path],
        json_path: Union[str, pathlib.Path],
    ) -> None:
        """
        Converts a YAML manifest into a JSON manifest by converting the raw YAML
        contents into a JSON dictionary. This function is "dumb" and just writes
        the direct-to-JSON version of the YAML file.

        Args:
            manifest_path: The manifest YAML to consume.
            json_path: The output file to write the JSON payload to.
        """
        with manifest_path.open("r") as f:
            manifest_yaml = yaml.safe_load(f)

        with pathlib.Path(json_path).open("w") as json_path:
            json.dump(manifest_yaml, json_path)

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

    # Private implementation

    @classmethod
    def _load_manifest_file_steps(cls, step_dicts: List[dict]) -> List[Step]:
        """
        Creates a list of Step instances based on a list of steps in dictionary
        format (usually loaded from a raw YAML file).

        Args:
            step_dicts: The steps as dictionaries to parse.

        Returns:
            List[Step]: The new Step instances.

        """
        successful_steps = []
        # Keep track of errors for specific step IDs, and also errors for any
        # steps that don't have a step ID
        errors_for_step_ids: dict[str, List[Any]] = defaultdict(list)
        errors_for_unknown_steps: List[Any] = []

        # Try parsing each step
        for step_dict in step_dicts:
            try:
                new_step = Step.parse_obj(step_dict)
                successful_steps.append(new_step)
            except pydantic.ValidationError as ex:
                errors = ex.errors()
                if "step_id" in step_dict:
                    _id = step_dict["step_id"]
                    errors_for_step_ids[_id].extend(errors)
                else:
                    errors_for_unknown_steps.append(errors)

        # Back out if there's no errors
        if not (errors_for_step_ids or errors_for_unknown_steps):
            return successful_steps

        # Otherwise, build the pretty print error string
        message = "Manifest step(s) are invalid"
        for step_id, errors in errors_for_step_ids.items():
            message += f"\nstep id: {step_id}\n"
            message += _pretty_errors_string(errors, indent=4)

        for index, step_errors in enumerate(errors_for_unknown_steps):
            message += f"\nunknown step {index + 1} (no step ID found)\n"
            message += _pretty_errors_string(step_errors, indent=4)

        raise ValueError(message)


def _pretty_errors_string(errors: list, indent: int = 0) -> str:
    """
    A custom string formatter for pydantic errors.

    See Also:
        The original implementation of this (with a slightly different format)
        is here - https://github.com/samuelcolvin/pydantic/blob/8846ec4685e749b93907081450f592060eeb99b1/pydantic/error_wrappers.py#L82-L83
    """

    def pretty_error(error: dict) -> str:
        loc_str = " -> ".join(str(ll) for ll in error["loc"])
        spacer = " " * indent
        return f'{spacer}{loc_str}\n    {spacer}{error["msg"]}'

    return "\n".join(pretty_error(err) for err in errors)
