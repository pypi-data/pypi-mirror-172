"""
Timestamp convenience functions
"""
from datetime import datetime


def timestamp() -> str:
    """
    Current date/time in utc iso format
    """
    return datetime.utcnow().isoformat()


def timestamp_from(*args, **kwargs) -> str:
    """
Datetime from any value accepted by the `datetime` constructor, returned in ISO format.

    `datetime(year, month, day[, hour[, minute[, second[, microsecond[,tzinfo]]]]])`
    """
    return datetime(*args, **kwargs).isoformat()


def unix() -> str:
    """
    Current date/time in utc string format
    """
    return datetime.utcnow().strftime("%s")


def unix_from_timestamp(timestamp: float) -> str:
    """
    Unix timestamp from any value accepted by the `datetime` constructor.
    """
    return datetime.utcfromtimestamp(timestamp).strftime("%s")


def unix_from_iso(iso: str) -> str:
    """
    Unix timestamp from any value accepted by the `datetime` constructor.
    """
    return datetime.fromisoformat(iso).strftime("%s")
