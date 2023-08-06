from __future__ import annotations

import warnings
from types import TracebackType
from typing import Optional, Type, Union

from supervisor.recorder import Recorder
from supervisor.reporting.record import Record
from supervisor.reporting.report_builder import ReportBuilder, StepReportBuilder
from supervisor.reporting.status import Status
from supervisor.reporting.timer import Timer


class StepContext:
    def __init__(
        self,
        builder: ReportBuilder,
        record: Recorder,
        *id_args,
        record_id: Optional[str] = None,
    ):
        """
        A context manager for a step that is running inside another step.
        This is an alternative to `@step` decorator when you don't want
        to write an entire function for a step.

        Args:
            builder: Where the step report will be written.
            record: Where messages and data logs will be written.
            *id_args: The numbers of the step, such as "1, 1"
            record_id: An optional ID of the record being actively processed
        """
        self.uuid = ".".join([str(n) for n in id_args])
        self.report_builder = builder
        self.recorder = record
        self.timer = Timer()
        self._status_override: Optional[Status] = None
        self.record_id: Optional[str] = record_id
        self._record_status_override: Optional[Status] = None

    def __enter__(self):
        """
        Logic for when this context is first started.

        Returns:
            MainContext: This instance.
        """
        self.timer.start()
        return self

    def __exit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_val: Optional[BaseException],
        exc_tb: Optional[TracebackType],
    ) -> bool:
        """
        Runs when the context is about to close, whether caused
        by a raised Exception or now.

        Returns:
            bool: True if the parent caller should ignore the
                Exception raised before entering this function
                (if any), False otherwise.
        """
        timed_info = self.timer.end()
        if self._status_override:
            step_status = self._status_override
        else:
            step_status = Status.FAILED if exc_type else Status.SUCCEEDED

        if self._record_status_override:
            record_status = self._record_status_override
        else:
            record_status = Status.FAILED if exc_type else Status.SUCCEEDED

        record = Record(self.record_id, record_status) if self.record_id else None

        new_report = StepReportBuilder(
            step_id=self.uuid,
            start_time=timed_info.start,
            end_time=timed_info.end,
            duration=timed_info.duration,
            status=step_status,
            args={},
            outputs=None,
            message_log=self.recorder.messages,
            data_log=self.recorder.data,
            record=record,
        )

        self.report_builder.workflow.append(new_report)
        return False

    def error(self) -> None:
        """
        Sets the status of this step to `Status.FAILED` in its `StepReport`.
        """
        self.set_status(Status.FAILED)

    def set_status(self, status: Union[str, Status]) -> None:
        """Override a step to be in the status of `status`"""
        # Convert the status to the correct type if necessary
        safe_status = Status(status)
        self._status_override = safe_status

    def set_record_status(self, status: Union[str, Status]) -> None:
        """Override a step record to be in the status of `status`"""
        # Convert the status to the correct type if necessary
        if not self.record_id:
            warnings.warn(
                "Setting a record status for a step without "
                "a record ID will have no effect",
                UserWarning,
            )
        safe_status = Status(status)
        self._record_status_override = safe_status


if __name__ == "__main__":
    report_builder = ReportBuilder()
    recorder = Recorder()

    substep = StepContext

    with substep(report_builder, recorder, 1) as s:
        print("hello world")

        with substep(report_builder, recorder, 1, 1) as s2:
            print("inner step")

    print(report_builder.workflow)
