class WorkflowException(Exception):
    """A base workflow exception"""


class WorkflowEngineError(WorkflowException):
    """A workflow:engine error"""


class WorkflowCacheError(WorkflowException):
    """A workflow:cache error"""


class WorkflowFactoryError(WorkflowException):
    """A workflow:factory error"""
