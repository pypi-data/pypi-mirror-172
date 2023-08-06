import time
import typing as t
from enum import Enum
from functools import wraps

from .helpers.time import timestamp
from .reporting.stepreport import StepReport

Func = t.TypeVar('Func', bound=t.Callable[..., t.Any])
StepId = t.TypeVar('StepId', bound=str)
StepReturn = t.TypeVar('StepReturn', bound=t.Optional[dict])


class StepType(str, Enum):
    """StepType — by default, steps run in sequential order.

    A conditional step will determine the next step at runtime based on the
    result of that step.

    If a step defines a `when_true` or `when_false` (a string of the next
    step id) then that step is considered conditional. After a conditional step
    is executed, the workflow iterator will compare the return value to
    the proceed_to[bool] value. If no value is provided to the """
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


class StepError(Exception):
    pass


# Workflow Step =============================================================-->
#
# The step class is used to represent a single step within a digital worker
# flow. This logs the manifest step_id, title, description, and execution
# order for the step (including, timestamps, exceptions, return values etc)
class Step:
    """
    The step class is used to represent a single step within a digital worker
    flow. This logs the manifest step_id, title, description, and execution
    order for the step (including, timestamps, exceptions, return values etc)

    Using the @step decorator within a @digitalworker, an
    implementation step function is queued within the Supervisors Workflow
    and executed via via an instantiation of this class.

    Example:
        >>> @step(1, 1) # new Step class is instantiated, and added to the workflow
        >>> def step_1_1(ctx):
        >>>     pass
        ...
        # >>> print(Supervisor().workflow)
        >>> [1.1: <Step>]
    """
    stepdoc: dict
    """The step definintion from the manifest"""

    report: StepReport
    """Dictionary storing all the report values for the runtime of this step"""

    strids: t.List[str]
    """The ID as a list of strings
    example: ["1", "1", "2"]"""

    intids: t.List[int]
    """The ID as a list of integers
    example: [1, 1, 2]"""

    is_macro: bool
    """flag macros"""

    priority: float
    """"Priority is used for sorting.
    It's the step id in 0-1 integer form, i.e, `"1.1.1"` -> `0.111`"""

    func: t.Callable
    """The implimentation function to be invoked in the workflow"""

    _call_count: int
    """The number of times this step has been invoked"""

    # function cache - stored on the class level
    # for all digital worker implimentation step methods
    # Note: this only works until we need to run multiple digital workers
    # or supervisors within the same process. In which case we'll either need
    # to store these in a global instance cache per dw/sup or flag func's with
    # a unique id per dw/sup instance.
    _fn_cache: t.Dict[str, t.Callable] = {}
    """ Function Cache Repository — Class Property — This stores all
    implimentation methods. The `@step()` decorator is used to tag implimentation
    steps, and cache a reference to that function in this dict.

    Because decorators are executed when the digital worker class is defined,
    the supervisor instance has not yet been initialized and therefor this must
    be a class level cache."""

    # Duration timers

    _start_time: float
    _end_time: float

    # Sequence Logic properties

    # Step ID's for the next step to run for conditional steps
    when: t.Dict[bool, str]

    # Report aliasing
    # TODO: clean this up by overriding this class getter function and peeking
    # report before looking at theseclas pope

    @property
    def sid(self) -> str:
        """Alias to step.report.step_id'"""
        return self.report.get('step_id')

    @sid.setter
    def sid(self, uid: str) -> None:
        """Alias for setting step.report.step_id'"""
        self.report.set('step_id', uid)

    @property
    def step_type(self) -> StepType:
        """Alias to step.report.step_type'"""
        return self.report.get('step_type', None)

    @step_type.setter
    def step_type(self, step_type: StepType) -> None:
        """Alias for setting step.report.step_type'"""
        self.report['step_type'] = step_type

    @property
    def step_status(self) -> StepStatus:
        """Alias to step.report.step_status'"""
        return self.report.get('step_status')

    @step_status.setter
    def step_status(self, step_status: StepStatus) -> None:
        """Alias for setting step.report.step_status'"""
        self.report['step_status'] = step_status

    def __init__(self,
                 step_id: str,
                 stepdoc: dict,
                 fn: t.Callable = None) -> None:
        """
        Create step and prepopulate manifest details
        """

        # Note: When retrieving from `stepdoc`, use `get` with a default
        # value to avoid getting a KeyError, (do not assume required values
        # here as that is the job of the schema).
        self._identify(step_id)
        self._call_count = 0
        self.stepdoc = stepdoc
        self.func = fn or self.get_func()
        self.prepare()

    def prepare(self) -> None:
        """
        Prepare the step for execution.
        """
        # get the report started
        self.report = StepReport({
            'step_id': self.step_id,
            'step_type': self._set_type(),
            'title': self.stepdoc.get('title', ''),
            'description': self.stepdoc.get('description', ''),
            'step_status': StepStatus.READY,
        })

    def reset(self):
        """Reset a step that may have previously been executed"""
        self.report.clear()
        self.prepare()

    def _set_type(self) -> StepType:
        when_true = self.stepdoc.get('when_true', False)
        when_false = self.stepdoc.get('when_false', False)

        if when_true or when_false:
            step_type = StepType.CONDITIONAL
            self.when = {}
        else:
            step_type = StepType.SEQUENTIAL

        if when_true:
            self.when[True] = str(when_true)
        if when_false:
            self.when[False] = str(when_false)

        return step_type

    # @singledispatchmethod
    def __call__(self, ctx, **kwargs) -> dict:
        """
        This class represents a single step function within a digital worker
        flow. Therefor, at the end of the day, it's essentially a glorified
        function. Because of that, it can be invoked just like any other
        function.

        Example:
            >>> step1 = Step(1, 1)
            >>> step1()
        """
        self.step_status = StepStatus.RUNNING
        self._call_count += 1

        # should always be immediately before the call
        self._before_call(**kwargs)

        # Try calling the original function given by the @digitalworker
        # try:
        self.report['returned'] = self.func(ctx, **kwargs)

        # If there's an exception, record it
        # todo: handle errors and warnings

        # should always be immediately after the call
        self._after_call()

        # mark complete, at the very end
        self.step_status = StepStatus.COMPLETE

        return self.report.get('returned')

    def conditional_result(self) -> t.Optional[str]:
        """Gets the next step ID on conditional steps"""
        res = self.report.get('returned')
        return self.when.get(res)

    def _identify(self, step_id: str):
        """
        Generates an identifier for a given step on initialization.

        Example:
            >>> step = Step("1.2.3") # exec's _identify
            # >>> print(step.step_id)
            prints "1.2.3"
            # >>> print(step.intids)
            prints [1, 2, 3]
            # >>> print(step.strids)
            prints ["1", "2", "3"]

        """
        self.step_id = step_id
        self.strids = strids = step_id.split('.')
        self.intids = intids = [int(i) for i in strids]

        # using the step id (1.2.3) stitch together
        # a float value that will represent its priority weight
        # i.e., 1.2.3 is 0.123, 2.2 is 0.22, etc
        priority = '0.'
        for s in strids:
            priority += s
        self.priority = float(priority)

        # macro steps are the root level steps, so the id will be a single
        # integer, i.e., [1] and not [1, 2, 3]
        self.is_macro = len(intids) == 1

    def _before_call(self, **args) -> None:
        # This is called before the step function is called to log relevant
        # information about the step.
        # print(f"Invoking step __call__: {self.step_id}")
        self._record_args(**args)

        # always last (for accuracy reasons)
        self.report["timestamp"] = timestamp()
        self._start_time = time.perf_counter()

    def _after_call(self) -> None:
        # Record any pre-execution information about the step. This is called
        # after the step function is called to log relevant information about
        # the step.

        # always first (for accuracy reasons)
        self._end_time = time.perf_counter()
        self._record_duration()

        # print(f"Finishing step __call__: {self.step_id}")

    def _record_duration(self) -> None:
        self.report['duration'] = self._end_time - self._start_time

    def _record_exception(self, e: Exception) -> None:
        if self.report.get('caught_exceptions') is None:
            self.report['caught_exceptions'] = []
        self.report['caught_exceptions'] = [type(e)]

    def _record_warning(self, e: Warning) -> None:
        if self.report.get('warnings') is None:
            self.report['warnings'] = []
        self.report['warnings'] = [type(e)]

    def _record_args(self, **args) -> None:
        self.report['args'] = args or {}

    # Dunder properties

    def __repr__(self) -> str:
        """Debugging representation of the step"""
        step_type = 'MacroStep' if self.is_macro else 'Step'
        title = self.report.get('title')
        return f'<{step_type}-{self.step_id} :: {title} :: called: {self._call_count}>'

    def __str__(self) -> str:
        """String representation of the step"""
        return self.report.get('title')

    def __eq__(self, other: 'Step') -> bool:
        """Step comparison (==)"""
        return False if type(self) != type(
            other) else self.step_id == other.step_id

    def __ne__(self, other: 'Step') -> bool:
        """Step comparison (!=)"""
        return not self.__eq__(other)

    def __lt__(self, o: 'Step') -> bool:
        """Step comparison (<)"""
        # Using the intids ([1, 1, 2]), we can compare the step to another step
        # be asserting whether each level is equal or less than.
        return False if type(self) != type(o) else self.priority < o.priority

    def __le__(self, other: 'Step') -> bool:
        """Step comparison (<=)"""
        return self.__lt__(other) or self.__eq__(other)

    def __gt__(self, other: 'Step') -> bool:
        """Step comparison (>)"""
        return not self.__le__(other)

    def __ge__(self, other: 'Step') -> bool:
        """Step comparison (>=)"""
        return not self.__lt__(other)

    def get_func(self) -> t.Callable:
        """Add the implimentation function to the step instance using
        the class method of the same name"""

        # Macro steps are optional implimentation methods, we use a lambda
        # that simply returns an arguments if provided
        fn = Step.get_cache_func(self.step_id)

        # If function is not callable, raise an exception.
        if not callable(fn):
            if not self.is_macro:
                raise StepError(
                    f"No step method found for step_id: {self.step_id}. \n" +
                    "Refer to your Digital Worker's manifest.yaml for \n"
                    f"details regarding step {self.step_id} and add \n"
                    "a new implimentation method to your DigitalWorker\n\n"
                    f"Functions left in cache: {Step.get_cache_ids()}")

            fn = lambda _, **kwargs: kwargs

        return fn

    @classmethod
    def get_cache_func(cls, id: str, default=None) -> t.Callable:
        """Pop function from class cache.
        Returns the function associated with the given id,
        removing it from the cache."""
        return cls._fn_cache.pop(id, default)

    @classmethod
    def cache_func(cls, id: str, fn: t.Callable) -> t.Callable:
        """Store function in class` cache.
        Returns the function associated with the given id."""
        cls._fn_cache[id] = fn
        return cls._fn_cache[id]

    @classmethod
    def cache_is_empty(cls) -> bool:
        """Returns True if the class function cache is empty."""
        return cls._fn_cache.__len__() == 0

    @classmethod
    def get_cache_size(cls) -> int:
        """Returns the size of the class function cache."""
        return cls._fn_cache.__len__()

    @classmethod
    def get_cache_ids(cls) ->...:
        """Returns the ids of the class function cache."""
        return cls._fn_cache.keys()


class step(object):
    """
    @step(*ids) — Step decorator

    This step decorator is used to mark a function— within a digital worker
    class (`DigitalWorker`)— as a step function. It instantiates a
    `Step` class and queues the step within the Supervisor's `Workflow`.

    Example:
        >>> @step(1, 1) # step 1.1
        ... def step_1_1(attr1, attr2):
        ...     pass
    """
    _id: str

    def __init__(self, *step_id: int):
        """
        Handle the step id that is given to the decorator
        """
        self._id = '.'.join(str(i) for i in step_id)

        # print(f"(__init__) :: Instantiated Step() :: {self._step.step_id}")

    def __call__(self, func: Func) -> Func:
        """
        Handle step function by wrapping the original method/function
        """

        @wraps(func)
        def func_wrapper(ref, *args, **kwargs):
            # wrapped function which is called at runtime with
            # the arguments of the previous function. *args and **kwargs
            # may or may not be empty. The first argument `ref` is the
            # digital workers class instance (or `self`)
            return func(ref, *args, **kwargs)

        # Store a 'secret' string which must be included in the
        # wrapper
        # func_wrapper.secret = self._secret()

        # Cache this step's function in the class' cache
        fn = Step.cache_func(self._id, func_wrapper)

        # print(f"(__call__) Configured Step() function :: {self._step.step_id}")
        return fn
