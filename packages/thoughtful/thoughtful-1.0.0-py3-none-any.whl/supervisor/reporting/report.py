from __future__ import annotations

import datetime
import json
import math
import pathlib
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional, Union

import isodate

from supervisor.__version__ import __version__
from supervisor.manifest import Manifest, StepStatus, StepType
from supervisor.recorder import DataLog, MessageLog


@dataclass
class StepReport:
    step_id: str
    step_type: StepType
    status: StepStatus
    title: str
    description: str
    start_time: datetime.datetime
    end_time: datetime.datetime
    duration: datetime.timedelta
    args: Dict[str, Any] = field(default_factory=dict)
    outputs: Optional[Dict] = None
    message_log: MessageLog = field(default_factory=list)
    data_log: DataLog = field(default_factory=list)

    def __json__(self) -> Dict[str, Any]:
        return {
            "step_id": self.step_id,
            "step_type": self.step_type.value,
            "step_status": self.status.value,
            "title": self.title,
            "description": self.description,
            "start_time": self.start_time.isoformat(),
            "end_time": self.end_time.isoformat(),
            "duration": isodate.duration_isoformat(self.duration),
            "duration_in_ms": _time_delta_to_ms(self.duration),
            "args": self.args,
            "returned": self.outputs,
            "data_log": self.data_log,
            "message_log": self.message_log,
        }


class WorkerStatus(str, Enum):
    """The final status of the digital worker run."""

    COMPLETE = "complete"
    WARNING = "warning"
    ERROR = "error"


@dataclass
class Report:
    supervisor_version = str(__version__)
    workflow: List[StepReport] = field(default_factory=list)
    start_time: datetime.datetime = field(default=datetime.datetime.utcnow())
    end_time: datetime.datetime = field(default=datetime.datetime.utcnow())
    duration: datetime.timedelta = field(default=datetime.timedelta(seconds=0))
    status: Optional[WorkerStatus] = None
    manifest: Optional[Manifest] = None

    def __json__(self) -> Dict[str, Any]:
        return {
            "supervisor_version": self.supervisor_version,
            "workflow": [step.__json__() for step in self.workflow],
            "start_time": self.start_time.isoformat(),
            "end_time": self.end_time.isoformat(),
            "duration": isodate.duration_isoformat(self.duration),
            "duration_in_ms": _time_delta_to_ms(self.duration),
            "worker": self.manifest.__json__() if self.manifest else None,
            "status": self.status.value,
        }

    def write(self, filename: Union[str, pathlib.Path]) -> None:
        """
        Write the report as a JSON object to a file.

        Args:
            filename: Where to write the file.
        """
        if not isinstance(filename, pathlib.Path):
            path = pathlib.Path(filename)
        else:
            path = filename

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
