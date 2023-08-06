import warnings
from typing import Callable

from supervisor.annotations import Annotatable, Annotation
from supervisor.deprecated_markers import deprecate_non_dynamic


def step(*args) -> Callable:
    """
    Declares that a function is associated with a step in a manifest PDD. This
    is done by adding a new property to the callable

    Args:
        *args: The list of numbers (or a single UUID) to represent a step ID.

    Returns:
        Callable: The decorated function.
    """
    deprecate_non_dynamic()

    def wrap(func):
        _id = ".".join([str(i) for i in args])
        new_annot = Annotation(uuid=_id, func=func)
        setattr(func, Annotatable.annotated_func_attr_name, new_annot)
        return func

    return wrap
