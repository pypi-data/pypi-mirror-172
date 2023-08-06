from __future__ import annotations

import datetime
import json
import math
import pathlib
import time
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional, Union

import isodate

from supervisor.__version__ import __version__
from supervisor.annotations import RunResult
from supervisor.manifest import Manifest, Step, StepStatus, StepType
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


class Reporter:
    def __init__(self, manifest: Optional[Manifest] = None) -> None:
        """
        Reporter — Responsible for logging the runtime of the digital
        worker process, producing a detailed `Work Report`.

        The Work Report is a structured log in the form of JSON which adheres to the
        [Report Schema](schemas/report.schema.json) defined and documented in the
        [Schema Library](https://github.com/Thoughtful-Automation/schemas)

        Attributes:
            self.report (Report): The report to write after a worker is complete.
        """
        self.report = Report(manifest=manifest)

        # Start the clock on the report timer
        self.start_time = time.perf_counter()

    def report_step(
        self,
        step: Step,
        result: RunResult,
        message_log: List[str],
        data_log: List[Dict[str, Any]],
    ) -> None:
        """
        Report on an executed workflow step. Creates a step report, and appends
        that report to `self.report`'s workflow.

        Args:
            step (Step): The step that was executed.
            result (RunResult): The result of running the step
            message_log (List[str]): The messages recorded during step execution.
            data_log (List[Dict[str, Any]]): The data logs recorded during step
                execution.
        """
        new_step_report = StepReport(
            step_id=step.step_id,
            step_type=step.step_type,
            status=result.status,
            title=step.title,
            description=step.description,
            start_time=result.start,
            end_time=result.end,
            duration=result.duration,
            args=result.input,
            outputs=result.output,
            message_log=message_log,
            data_log=data_log,
        )
        self.report.workflow.append(new_step_report)

    def end_report(self) -> Report:
        """
        End the report and calculate the duration.

        Returns:
            Report: The final report.
        """
        end_time = time.perf_counter()
        end_timestamp = datetime.datetime.utcnow()
        self.report.end_time = end_timestamp

        duration_seconds = end_time - self.start_time
        duration_delta = datetime.timedelta(seconds=duration_seconds)
        self.report.duration = duration_delta

        failed_steps = [
            s for s in self.report.workflow if s.status != StepStatus.COMPLETE
        ]
        self.report.status = (
            WorkerStatus.ERROR if failed_steps else WorkerStatus.COMPLETE
        )
        return self.report


def _time_delta_to_ms(delta: datetime.timedelta) -> int:
    """
    Converts a timedelta into integer milliseconds.

    Args:
        delta: The time duration.

    Returns:
        The millisecond conversion of the timedelta as an int rounded up.
    """
    return math.ceil(delta.total_seconds() * 1000)
