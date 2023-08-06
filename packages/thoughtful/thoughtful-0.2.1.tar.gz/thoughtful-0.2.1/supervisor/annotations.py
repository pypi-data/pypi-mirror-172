from __future__ import annotations

import datetime
import sys
import time
from dataclasses import dataclass
from typing import Callable, Dict, Optional, TypeVar

from supervisor.manifest import StepStatus


@dataclass
class RunResult:
    start: datetime.datetime
    end: datetime.datetime
    duration: float
    status: StepStatus
    output: Optional[Dict]
    input: Optional[Dict]

    @classmethod
    def empty_result(cls) -> RunResult:
        now = datetime.datetime.now()
        return cls(
            start=now,
            end=now,
            duration=0,
            status=StepStatus.COMPLETE,
            output=None,
            input=None,
        )


@dataclass
class Annotation:
    uuid: str
    func: Callable

    def run(self, parent_context: object, func_kwargs: dict) -> RunResult:
        if type(func_kwargs) != dict:
            raise TypeError("Must pass in a dictionary to func")

        # Keep this loop close; time how long the annotated function takes
        start_timestamp = datetime.datetime.utcnow()
        timer_start = time.perf_counter()
        func_result = self.func(parent_context, **func_kwargs)
        timer_end = time.perf_counter()
        end_timestamp = datetime.datetime.utcnow()

        duration = timer_end - timer_start
        status = StepStatus.COMPLETE

        return RunResult(
            start=start_timestamp,
            input=func_kwargs,
            output=func_result,
            status=status,
            duration=duration,
            end=end_timestamp,
        )


AnnotationsById = TypeVar("AnnotationsById", bound=Dict[str, Annotation])


class AnnotatableMetaClass(type):
    """
    A metaclass to detect annotated methods when a class is created.
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
        new_steps_dict: AnnotationsById = dict()

        # inherit bases exposed methods
        for base in bases:
            updated_steps = getattr(base, AnnotatableMetaClass.steps_attr_name, {})
            new_steps_dict.update(updated_steps)

        for name, member in attrs.items():
            # For every member of the new class to create, check if it is
            # annotated by checking for the attribute name on the member
            meta: Annotation = getattr(
                member, AnnotatableMetaClass.annotated_func_attr_name, None
            )
            if meta is not None:
                new_steps_dict[meta.uuid] = meta

        attrs[AnnotatableMetaClass.steps_attr_name] = new_steps_dict
        return type.__new__(mcs, name, bases, attrs)


class Annotatable(metaclass=AnnotatableMetaClass):
    """
    A base class that uses `AnnotatableMetaClass` to detect annotated methods
    when the class is created.
    """

    @property
    def __steps__(self) -> AnnotationsById:
        """
        The annotations that indicate which functions in this class instance
        are steps in a manifest to run.

        The metaclass sets this property automatically, but its declared here
        to play nice with PyCharm and other type checkers. This is a "promise"
        that any subclass of this will have this property.
        """
        step_attr = AnnotatableMetaClass.steps_attr_name
        default_value = {}

        if step_attr in self.__dict__:
            return getattr(self, step_attr, default_value)
        return default_value
