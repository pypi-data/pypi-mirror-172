unicode = str

# Exception Handling for Supervisor Exceptions
# as well as Digital Worker Exceptions.
#
# https://runestone.academy/runestone/books/published/thinkcspy/Debugging/KnowyourerrorMessages.html
# Message         Number Percent
# ParseError:     4999   54.74%
# TypeError:      1305   14.29%
# NameError:      1009   14.05%
# ValueError:     893    9.78%
# URIError:       334    3.66%
# TokenError:     244    2.67%
# SyntaxError:    227    2.49%
# TimeLimitError: 44     0.48%
# IndentationError:28    0.31%
# AttributeError:  27    0.30%
# ImportError:     16    0.18%
# IndexError:      6     0.07%
#
# Exception hierarchy —
# The class hierarchy for built-in exceptions is:
#
#    BaseException
#     +-- SystemExit
#     +-- KeyboardInterrupt
#     +-- GeneratorExit
#     +-- Exception
#          +-- StopIteration
#          +-- StopAsyncIteration
#          +-- ArithmeticError
#          |    +-- FloatingPointError
#          |    +-- OverflowError
#          |    +-- ZeroDivisionError
#          +-- AssertionError
#          +-- AttributeError
#          +-- BufferError
#          +-- EOFError
#          +-- ImportError
#          |    +-- ModuleNotFoundError
#          +-- LookupError
#          |    +-- IndexError
#          |    +-- KeyError
#          +-- MemoryError
#          +-- NameError
#          |    +-- UnboundLocalError
#          +-- OSError
#          |    +-- BlockingIOError
#          |    +-- ChildProcessError
#          |    +-- ConnectionError
#          |    |    +-- BrokenPipeError
#          |    |    +-- ConnectionAbortedError
#          |    |    +-- ConnectionRefusedError
#          |    |    +-- ConnectionResetError
#          |    +-- FileExistsError
#          |    +-- FileNotFoundError
#          |    +-- InterruptedError
#          |    +-- IsADirectoryError
#          |    +-- NotADirectoryError
#          |    +-- PermissionError
#          |    +-- ProcessLookupError
#          |    +-- TimeoutError
#          +-- ReferenceError
#          +-- RuntimeError
#          |    +-- NotImplementedError
#          |    +-- RecursionError
#          +-- SyntaxError
#          |    +-- IndentationError
#          |         +-- TabError
#          +-- SystemError
#          +-- TypeError
#          +-- ValueError
#          |    +-- UnicodeError
#          |         +-- UnicodeDecodeError
#          |         +-- UnicodeEncodeError
#          |         +-- UnicodeTranslateError
#          +-- Warning
#               +-- DeprecationWarning
#               +-- PendingDeprecationWarning
#               +-- RuntimeWarning
#               +-- SyntaxWarning
#               +-- UserWarning
#               +-- FutureWarning
#               +-- ImportWarning
#               +-- UnicodeWarning
#               +-- BytesWarning
#               +-- EncodingWarning
#               +-- ResourceWarning


class _SupervisorError(Exception):
    """
    Base class for Supervisor errors.
    Do not raise this method but use more specific child errors below.
    """

    def __init__(self, message='', details=''):
        Exception.__init__(self, message)
        self.details = details

    @property
    def message(self):
        return unicode(self)


class CriticalError(_SupervisorError):
    """
    Reserved for Errors that should never slip into production.
    This is pretty much same as 'Internal Error' and should of course never happen.
    """


class ManifestError(_SupervisorError):
    """
    Used when the provided test data is invalid.
    ManifestErrors are not caught by keywords that run other keywords
    (e.g. `Run Keyword And Expect Error`).
    """


class SchemaError(ManifestError):
    """
    Used when variable does not exist.
    SchemaErrors are caught by keywords that run other keywords
    (e.g. `Run Keyword And Expect Error`).
    """
