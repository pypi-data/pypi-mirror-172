from __future__ import annotations

from types import TracebackType
from typing import Optional, Type, Union

from supervisor.dynamic.report_builder import ReportBuilder, StepReportBuilder
from supervisor.dynamic.timer import Timer
from supervisor.manifest import StepStatus
from supervisor.recorder import Recorder


class StepContext:
    def __init__(self, builder: ReportBuilder, record: Recorder, *id_args):
        """
        A context manager for a step that is running inside of another step.
        This is an alternative to `@step` decorator when you don't want
        to write an entire function for a step.

        Args:
            builder: Where the step report will be written.
            record: Where messages and data logs will be written.
            *id_args: The numbers of the step, such as "1, 1"
        """
        self.uuid = ".".join([str(n) for n in id_args])
        self.report_builder = builder
        self.recorder = record
        self.timer = Timer()
        self._status_override: Optional[StepStatus] = None

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
            if exc_type:
                step_status = StepStatus.ERROR
            else:
                step_status = StepStatus.COMPLETE

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
        )
        self.report_builder.workflow.append(new_report)

        # Return False so that any exceptions inside this context
        # are still raised after this function ends
        return False

    def error(self) -> None:
        """
        Sets the status of this step to `StepStatus.ERROR` in its `StepReport`.
        """
        self.set_status(StepStatus.ERROR)

    def set_status(self, status: Union[str, StepStatus]) -> None:
        """Override a step to be in the status of `status`"""
        # Convert the status to the correct type if necessary
        safe_status = StepStatus(status)
        self._status_override = safe_status


if __name__ == "__main__":
    report_builder = ReportBuilder()
    recorder = Recorder()

    substep = StepContext

    with substep(report_builder, recorder, 1) as s:
        print("hello world")

        with substep(report_builder, recorder, 1, 1) as s2:
            print("inner step")

    print(report_builder.workflow)
