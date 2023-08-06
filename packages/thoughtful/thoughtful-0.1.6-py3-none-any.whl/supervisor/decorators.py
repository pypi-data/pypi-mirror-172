import functools


def singleton(cls):
    """Constrain a class a Singleton class (only one instance)

    Example:
        >>> @singleton
        >>> class Foo:
        >>>     def __new__(cls):
        >>>         cls.x = 10
        >>>         return object.__new__(cls)

        >>>     def __init__(self):
        >>>         assert self.x == 10
        >>>         self.x = 15

        >>> assert Foo().x == 15
        >>> Foo().x = 20
        >>> assert Foo().x == 20
    """

    cls.__new_original__ = cls.__new__

    @functools.wraps(cls.__new__)
    def singleton_new(cls, *args, **kw):
        it = cls.__dict__.get('__it__')
        if it is not None:
            return it

        cls.__it__ = it = cls.__new_original__(cls, *args, **kw)
        it.__init_original__(*args, **kw)
        return it

    cls.__new__ = singleton_new
    cls.__init_original__ = cls.__init__
    cls.__init__ = object.__init__

    return cls


def trackable(name, obj, base):
    """
    Creates a trackable state machine class
    """

    def func_logger(func):

        def wrapped(self, *args, **kwargs):
            before = base(self)
            result = func(self, *args, **kwargs)
            after = base(self)
            if before != after:
                obj.revisions[name].append(after)
            return result

        return wrapped

    methods = (type(list.append), type(list.__setitem__))
    skip = set(['__iter__', '__len__', '__getattribute__'])

    class TrackableMeta(type):

        def __new__(cls, name, bases, dct):
            for attr in dir(base):
                if attr not in skip:
                    func = getattr(base, attr)
                    if isinstance(func, methods):
                        dct[attr] = func_logger(func)
            return type.__new__(cls, name, bases, dct)

    class TrackableObject(base):
        __metaclass__ = TrackableMeta

    return TrackableObject()


def debug(func):
    """Print the function signature and return value"""

    @functools.wraps(func)
    def wrapper_debug(*args, **kwargs):
        args_repr = [repr(a) for a in args]
        kwargs_repr = [f'{k}={v!r}' for k, v in kwargs.items()]
        signature = ', '.join(args_repr + kwargs_repr)
        print(f'Calling {func.__name__}({signature})')
        value = func(*args, **kwargs)
        print(f'{func.__name__!r} returned {value!r}')
        return value

    return wrapper_debug
