# updated dispatch decorator
import pathlib
from functools import singledispatch, update_wrapper
from typing import Union


def methoddispatch(func):
    """Method added for compatibility - replaced later version of python @singledispatchmethod decorator"""
    dispatcher = singledispatch(func)

    def wrapper(*args, **kw):
        return dispatcher.dispatch(args[1].__class__)(*args, **kw)

    wrapper.register = dispatcher.register
    update_wrapper(wrapper, func)
    return wrapper


def safe_path(path: Union[str, pathlib.Path]) -> pathlib.Path:
    filename = str(path)
    invalid_chars = [':', '*', '?', '"', '<', '>' '|', "'"]
    for char in invalid_chars:
        filename = filename.replace(char, '_')
    return pathlib.Path(filename)
