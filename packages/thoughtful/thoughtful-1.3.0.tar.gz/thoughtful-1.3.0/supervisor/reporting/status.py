from enum import Enum


class Status(str, Enum):
    SUCCEEDED = "succeeded"
    FAILED = "failed"
    WARNING = "warning"
    SKIPPED = "skipped"
