from __future__ import annotations

import datetime
import time
from dataclasses import dataclass
from typing import Callable, Dict, Optional, Type, TypeVar

from supervisor.manifest import StepStatus


@dataclass
class RunResult:
    """
    The result of running an ``Annotation``

    Attributes:
        start (datetime.datetime): When the run started (wall clock time).
        end (datetime.datetime): When the run ended (wall clock time).
        duration (float): How long the run took in CPU seconds.
        status (StepStatus): The result status of the run.
        output (dict, optional): The output from the function run.
        input (dict, optional): The inputs to the function run as kwargs.
    """

    start: datetime.datetime
    end: datetime.datetime
    duration: datetime.timedelta
    status: StepStatus
    output: Optional[Dict]
    input: Optional[Dict]

    @classmethod
    def empty_result(cls) -> RunResult:
        """
        Represents a no-op function run result.

        Returns:
            RunResult: An empty ``RunResult``.
        """
        now = datetime.datetime.now()
        return cls(
            start=now,
            end=now,
            duration=datetime.timedelta(seconds=0),
            status=StepStatus.COMPLETE,
            output=None,
            input=None,
        )


@dataclass
class Annotation:
    """
    A function in a ``DigitalWorker`` class that's associated with a manifest
    step based on its `uuid`.

    Attributes:
        uuid (str): The ID of the step associated with this ``Annotation``.
        func (Callable): The function to run.
    """

    uuid: str
    func: Callable

    def run(self, parent_context: object, func_kwargs: dict) -> RunResult:
        """
        Runs an annotated function.

        Args:
            parent_context (DigitalWorker): This is the class instance that's
                the parent of ``self.func``.
            func_kwargs (dict): The input kwargs for the function.

        Returns:
            RunResult: The output and metadata from running the function.
        """
        if type(func_kwargs) != dict:
            raise TypeError("Must pass in a dictionary to func")

        # Keep this loop close; time how long the annotated function takes
        start_timestamp = datetime.datetime.utcnow()
        timer_start = time.perf_counter()
        func_result = self.func(parent_context, **func_kwargs)
        timer_end = time.perf_counter()
        end_timestamp = datetime.datetime.utcnow()

        duration_seconds = timer_end - timer_start
        duration_delta = datetime.timedelta(seconds=duration_seconds)
        status = StepStatus.COMPLETE

        return RunResult(
            start=start_timestamp,
            input=func_kwargs,
            output=func_result,
            status=status,
            duration=duration_delta,
            end=end_timestamp,
        )


AnnotationsById = TypeVar("AnnotationsById", bound=Dict[str, Annotation])


class AnnotatableMeta(type):
    """
    A metaclass to detect annotated methods when a class is created.

    This class factory adds a property ``AnnotatableMetaClass.steps_attr_name``
    to any classes that use this metaclass, and the value is a list of
    ``Annotation``s.
    """

    annotated_func_attr_name = "__annot__"
    """
    Callables that are items in this class with this attribute name are
    considered annotated.
    """

    steps_attr_name = "__steps__"
    """
    The attribute name for a sub class that contains the step annotations.
    """

    def __new__(mcs: Type[type], name: str, bases: tuple, attrs: dict) -> type:
        """
        Creates a new class (the class itself, not the instance), with a new
        property to hold the list of ``Annotation``s.

        Args:
            name (str): The name of the class to be created.
            bases (tuple): The parent classes.
            attrs (dict): The attributes to add to the class.
        """
        # Create a place to hold annotations
        new_annotations: AnnotationsById = dict()

        # Search every parent class for pre-existing annotations property
        for base in bases:
            attribute_to_find = AnnotatableMeta.steps_attr_name
            default_value = {}
            updated_steps = getattr(base, attribute_to_find, default_value)
            new_annotations.update(updated_steps)

        # Search for Annotations in existing attributes
        for name, member in attrs.items():
            # For every member of the new class to create, check if it is
            # annotated by checking for the attribute name on the member
            attribute_to_find = AnnotatableMeta.annotated_func_attr_name
            default_attribute_value = None
            meta: Annotation = getattr(
                member, attribute_to_find, default_attribute_value
            )
            if meta is not None:
                # Record the new annotation
                new_annotations[meta.uuid] = meta

        # Add the annotations to the attributes for the new class to create
        new_attribute_to_add = AnnotatableMeta.steps_attr_name
        attrs[new_attribute_to_add] = new_annotations
        return type.__new__(mcs, name, bases, attrs)


class Annotatable(metaclass=AnnotatableMeta):
    """
    A base class that uses `AnnotatableMetaClass` to detect annotated methods
    when the class is created.
    """

    # noinspection PyPropertyDefinition
    @property
    def __steps__(self) -> AnnotationsById:
        """
        The annotations that indicate which functions in this class instance
        are steps in a manifest to run.

        The metaclass sets this property automatically, but its declared here
        to play nice with PyCharm and other type checkers. This is a "promise"
        that any subclass of this will have this property.
        """
        pass  # pragma: no cover
