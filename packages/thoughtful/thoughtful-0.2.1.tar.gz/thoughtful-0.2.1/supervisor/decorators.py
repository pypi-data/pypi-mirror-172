from supervisor import annotations


def step(*args):
    """
    Decorator that adds an `Annotation` property to the decorated callable.

    `args` are the list of numbers (or a single UUID) to tie the decorated
    callable to a manifest.
    """

    def wrap(func):
        _id = ".".join([str(i) for i in args])
        new_annot = annotations.Annotation(uuid=_id, func=func)
        setattr(func, annotations.Annotatable.annotated_func_attr_name, new_annot)
        return func

    return wrap
