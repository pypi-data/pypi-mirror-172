"""helper/exceptions/loader_exceptions.py— YAML/JSON Loader exceptions"""
import yaml

YAML_TAB_PROBLEM = "found character '\\t' that cannot start any token"


class LoaderError(Exception):
    """Base class for exceptions raised when loading yaml/json/etc.
    """


class NotFoundError(LoaderError):
    """A requested value could not be found in the configuration trees.
    """


class ConfigValueError(LoaderError):
    """The value in the configuration is illegal.
    """


class ConfigTypeError(ConfigValueError):
    """The value in the configuration did not match the expected type.
    """


class ConfigTemplateError(LoaderError):
    """Base class for exceptions raised because of an invalid template.
    """


class ConfigReadError(LoaderError):
    """A configuration file could not be read.
    """

    def __init__(self, filename, reason=None):
        self.filename = filename
        self.reason = reason

        message = u'file {0} could not be read'.format(filename)
        if (isinstance(reason, yaml.scanner.ScannerError) and
                reason.problem == YAML_TAB_PROBLEM):
            # Special-case error message for tab indentation in YAML markup.
            message += u': found tab character at line {0}, column {1}'.format(
                reason.problem_mark.line + 1,
                reason.problem_mark.column + 1,
            )
        elif reason:
            # Generic error message uses exception's message.
            message += u': {0}'.format(reason)

        super(ConfigReadError, self).__init__(message)
