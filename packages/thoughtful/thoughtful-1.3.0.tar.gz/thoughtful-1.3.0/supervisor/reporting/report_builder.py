from __future__ import annotations

import datetime
import time
from collections import defaultdict
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Union

from supervisor.manifest import StepId, StepStatus
from supervisor.recorder import DataLog, MessageLog
from supervisor.reporting.record import Record
from supervisor.reporting.report import Report, StepReport, WorkerStatus
from supervisor.reporting.status import Status
from supervisor.reporting.timer import Timer


@dataclass
class StepReportBuilder:
    """
    Builds a dynamic digital worker step.
    """

    step_id: str
    start_time: datetime.datetime
    end_time: datetime.datetime
    duration: datetime.timedelta
    status: StepStatus
    args: Dict[str, Any] = field(default_factory=dict)
    outputs: Optional[Dict] = None
    message_log: MessageLog = field(default_factory=list)
    data_log: DataLog = field(default_factory=list)
    record: Optional[Record] = None

    def to_report(self) -> StepReport:
        """
        A final report on this step's execution.

        Returns:
            StepReport: A final report on this step's execution.
        """

        # Build the report
        return StepReport(
            step_id=self.step_id,
            status=self.status,
            start_time=self.start_time,
            end_time=self.end_time,
            duration=self.duration,
            args=self.args,
            outputs=self.outputs,
            message_log=self.message_log,
            data_log=self.data_log,
            record=self.record,
        )


RecordId = str


@dataclass
class ReportBuilder:
    """
    A work report builder that creates a new work report as a digital worker
    is executed.
    """

    timer: Timer = field(default_factory=Timer)
    workflow: List[StepReportBuilder] = field(default_factory=list)
    timer_start: float = time.perf_counter()
    status: Optional[WorkerStatus] = None
    # These steps will be overridden with the specified status when the
    # `Report` is written
    _step_statuses_to_override: Dict[StepId, StepStatus] = field(default_factory=dict)
    _record_statuses_to_override: Dict[StepId, Dict[RecordId, Status]] = field(
        default_factory=lambda: defaultdict(dict)
    )

    def __post_init__(self):
        self.timer.start()

    def fail_step(self, step_id: str) -> None:
        """Override a step to be in the `StepStatus.ERROR` state."""
        self.set_step_status(step_id=step_id, status=StepStatus.ERROR)

    def set_step_status(self, step_id: str, status: Union[StepStatus, str]) -> None:
        """Override a step to be in the status of `status`"""
        # Convert the status to the correct type if necessary
        safe_status = StepStatus(status)
        self._step_statuses_to_override[step_id] = safe_status

    def set_record_status(
        self, step_id: str, record_id: str, status: Union[Status, str]
    ) -> None:
        """
        Override a record to be in the status of `status`.

        Args:
            step_id: The step id a specific step that contains this record.
            record_id: The id of the record to override.
            status: The status to override the record to.
        """
        # Convert the status to the correct type if necessary
        safe_status = Status(status)
        self._record_statuses_to_override[step_id][record_id] = safe_status

    def to_report(self) -> Report:
        """
        Convert supervisor workflow to work report.

        Returns:
            Report: The finalized work report.
        """
        timed = self.timer.end()

        # Update step reports with any overridden statuses
        steps = [x.to_report() for x in self.workflow]
        for step_report in steps:
            # Update step statuses
            if step_report.step_id in self._step_statuses_to_override:
                new_status = self._step_statuses_to_override[step_report.step_id]
                step_report.status = new_status
            # Update the record statuses
            if step_report.step_id in self._record_statuses_to_override:
                records = self._record_statuses_to_override[step_report.step_id]
                if step_report.record.record_id in records:
                    new_status = records[step_report.record.record_id]
                    step_report.record.status = new_status

        return Report(
            start_time=timed.start,
            end_time=timed.end,
            duration=timed.duration,
            workflow=steps,
            status=self.status,
        )
