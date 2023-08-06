"""
This module holds the logic for the runtime storage and generation of the
run report. It contains metadata about the two main entities in the run report:
the run as a whole and its children, the steps.
"""

from __future__ import annotations

import datetime
import json
import math
import pathlib
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Union

import isodate

from supervisor.__version__ import __version__
from supervisor.recorder import DataLog, MessageLog
from supervisor.reporting.record import Record
from supervisor.reporting.status import Status


@dataclass
class StepReport:
    """
    A step report is a representation of a step's execution. This dataclass
    contains all the information that will be stored in the run report. There
    are an arbitrary number of steps reports that will be contained in the
    workflow of any given run report.
    """

    step_id: str
    """
    str: The ID of the step.
    """

    status: Status
    """
    Status: The status of the step.
    """

    start_time: datetime.datetime
    """
    datetime.datetime: The start time of the step.
    """

    end_time: datetime.datetime
    """
    datetime.datetime: The end time of the step.
    """

    duration: datetime.timedelta
    """
    datetime.timedelta: The duration of the step.
    """

    message_log: MessageLog = field(default_factory=list)
    """
    MessageLog: Log of messages from the recorder object.
    """

    data_log: DataLog = field(default_factory=list)
    """
    DataLog: Log of changes to data from the recorder object.
    """

    record: Optional[Record] = None
    """
    Record, optional: The record of the step, if any.
    """

    def __json__(self) -> Dict[str, Any]:
        return {
            "step_id": self.step_id,
            "step_status": self.status.value,
            "start_time": self.start_time.isoformat(),
            "end_time": self.end_time.isoformat(),
            "duration": isodate.duration_isoformat(self.duration),
            "duration_in_ms": _time_delta_to_ms(self.duration),
            "data_log": self.data_log,
            "message_log": self.message_log,
            "record": self.record.__json__() if self.record else None,
        }


@dataclass
class Report:
    """
    Report: A report is a representation of a run's execution. This dataclass
    contains all the information that will be stored in the run report,
    including a list of the steps that were executed. This is the parent
    class of the run report, and as such will only ever be one per run report.
    """

    supervisor_version = str(__version__)
    """
    str: The version of the supervisor that generated the report.
    """

    workflow: List[StepReport] = field(default_factory=list)
    """
    List[StepReport]: The list of steps that were executed.
    """

    start_time: datetime.datetime = field(default=datetime.datetime.utcnow())
    """
    datetime.datetime: The start time of the run.
    """

    end_time: datetime.datetime = field(default=datetime.datetime.utcnow())
    """
    datetime.datetime: The end time of the run.
    """

    duration: datetime.timedelta = field(default=datetime.timedelta(seconds=0))
    """
    datetime.timedelta: The duration of the run.
    """

    status: Optional[Status] = None
    """
    Status, optional: The status of the run.
    """

    def __json__(self) -> Dict[str, Any]:
        return {
            "supervisor_version": self.supervisor_version,
            "workflow": [step.__json__() for step in self.workflow],
            "start_time": self.start_time.isoformat(),
            "end_time": self.end_time.isoformat(),
            "duration": isodate.duration_isoformat(self.duration),
            "duration_in_ms": _time_delta_to_ms(self.duration),
            "status": self.status.value,
        }

    def write(self, filename: Union[str, pathlib.Path]) -> None:
        """
        Write the report as a JSON object to a file.

        Args:
            filename: Where to write the file.
        """
        path = (
            filename if isinstance(filename, pathlib.Path) else pathlib.Path(filename)
        )

        with path.open("w") as out:
            report_dict = self.__json__()
            json.dump(report_dict, out)


def _time_delta_to_ms(delta: datetime.timedelta) -> int:
    """
    Converts a timedelta into integer milliseconds.

    Args:
        delta: The time duration.

    Returns:
        The millisecond conversion of the timedelta as an int rounded up.
    """
    return math.ceil(delta.total_seconds() * 1000)
