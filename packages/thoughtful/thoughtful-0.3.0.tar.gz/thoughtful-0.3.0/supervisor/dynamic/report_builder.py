from __future__ import annotations

import datetime
import time
import warnings
from contextlib import suppress
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

from supervisor.manifest import Manifest, Step, StepStatus, StepType
from supervisor.recorder import DataLog, MessageLog
from supervisor.reporter import Report, StepReport


@dataclass
class DynamicStepReportBuilder:
    """
    Builds a dynamic digital worker step.
    """

    step_id: str
    start_time: datetime.datetime
    end_time: datetime.datetime
    duration: datetime.timedelta
    args: Dict[str, Any] = field(default_factory=dict)
    outputs: Optional[Dict] = None
    message_log: MessageLog = field(default_factory=list)
    data_log: DataLog = field(default_factory=list)

    def to_report(self, manifest: Manifest) -> StepReport:
        """
        Populate missing fields in the report with those from its `manifest`.

        Args:
            manifest: The digital worker's manifest.

        Returns:
            StepReport: A final report on this step's execution.
        """
        # Find the corresponding step in the manifest workflow
        # if it exists
        # noinspection PyUnusedLocal
        step: Optional[Step] = None
        with suppress(KeyError):
            step = manifest.steps_by_id[self.step_id]

        # Build the report
        return StepReport(
            step_id=self.step_id,
            step_type=step.step_type if step else StepType.UNKNOWN,
            status=StepStatus.COMPLETE,
            title=step.title if step else "unknown",
            description=step.description if step else "unknown",
            start_time=self.start_time,
            end_time=self.end_time,
            duration=self.duration,
            args=self.args,
            outputs=self.outputs,
            message_log=self.message_log,
            data_log=self.data_log,
        )


@dataclass
class DynamicWorkReportBuilder:
    """
    A work report builder that creates a new work report as a digital worker
    is executed.
    """

    start_time = datetime.datetime.utcnow()
    end_time = datetime.datetime.utcnow()
    duration = datetime.timedelta(seconds=0)
    workflow: List[DynamicStepReportBuilder] = field(default_factory=list)
    timer_start: float = time.perf_counter()

    def end(self) -> None:
        """
        Finalize the report.
        """

        # Calculate the end time at the beginning
        timer_end = time.perf_counter()
        self.end_time = datetime.datetime.utcnow()

        # Set start = end if start wasn't set
        if not self.timer_start:
            warnings.warn("Report timer was never started, using end time")
            self.timer_start = timer_end
        if not self.start_time:
            warnings.warn("Report doesn't have start timestamp, using end timestamp")
            self.start_time = self.end_time

        # Calculate duration as timedelta between timer values
        duration_seconds = timer_end - self.timer_start
        self.duration = datetime.timedelta(seconds=duration_seconds)

    def to_report(self, manifest: Manifest) -> Report:
        """
        Populate fields in the work report using fields from the `manifest`.

        Args:
            manifest: The digital worker's manifest.

        Returns:
            Report: The finalized work report.
        """
        steps = [x.to_report(manifest) for x in self.workflow]
        return Report(
            start_time=self.start_time,
            end_time=self.end_time,
            duration=self.duration,
            workflow=steps,
            manifest=manifest,
        )
