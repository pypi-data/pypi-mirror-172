from enum import Enum


class Status(str, Enum):
    """
    Status — The status of whatever is being tracked — step, entire flow, record.

    SUCCEEDED: The item has completed successfully.
    WARNING: The item finished, but requires attention
    FAILED: The item has failed
    SKIPPED: The item was skipped
    """

    SUCCEEDED = "succeeded"
    FAILED = "failed"
    WARNING = "warning"
