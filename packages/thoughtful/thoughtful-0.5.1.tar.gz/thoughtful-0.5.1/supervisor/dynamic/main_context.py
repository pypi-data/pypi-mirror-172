from __future__ import annotations

import datetime
import pathlib
from typing import Callable, Optional, Union

from supervisor.dynamic.drift_report import DriftReport
from supervisor.dynamic.report_builder import ReportBuilder
from supervisor.manifest import Manifest
from supervisor.recorder import Recorder


class MainContext:
    def __init__(
        self,
        report_builder: ReportBuilder,
        recorder: Recorder,
        manifest: Union[str, pathlib.Path],
        output_dir: Union[str, pathlib.Path],
        callback: Optional[Callable] = None,
    ):
        """
        Supervises an entire digital worker run and generates a work report
        and drift report for the run from the digital worker's manifest.

        You can optionally specify a callback function that will be run when
        this context is finished via the `callback` param in the constructor. A
        callback is a function that is invoked with three parameters: the
        current context (as the `MainContext` instance), the `Report`, and
        the `DriftReport` generated from this digital worker's run.

        For example:

        ```python
        def print_work_report(
            ctx: MainContext,
            work_report: Report,
            drift_report: DriftReport
        ):
            print(work_report.__json__())

        def main()
            # ...
            pass

        with supervise(callback=print_work_report):
            main()
        ```

        Args:
            report_builder (ReportBuilder): Where step reports will be sent to
            recorder (Recorder): Where messages and data logs will be sent to
            manifest (str): The digital worker's manifest definition
            output_dir (str): Where the work report and drift report will
                be written to
            callback (callable, optional): a function that is invoked with three
                parameters: the current context (as the `MainContext` instance),
                the `Report`, and the `DriftReport` generated from this digital
                worker's run.
        """
        self.report_builder = report_builder
        self.recorder = recorder
        self.manifest_path = pathlib.Path(manifest)
        self.output_path = pathlib.Path(output_dir)
        self.callback = callback

    def __enter__(self) -> MainContext:
        """
        Logic for when this context is first started.

        Returns:
            MainContext: This instance.
        """
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> bool:
        """
        Runs when the context is about to close, whether caused
        by a raised Exception or now.

        Returns:
            bool: True if the parent caller should ignore the
                Exception raised before entering this function
                (if any), False otherwise.
        """
        manifest = Manifest.from_file(self.manifest_path)
        work_report = self.report_builder.to_report(manifest)
        drift_report = DriftReport.from_dw_run(manifest, work_report)

        # Create the output directory if it doesn't already exist
        self.output_path.mkdir(parents=True, exist_ok=True)

        # Write the work report
        work_report_path = self._safe_report_path(file_prefix="workreport")
        work_report.write(work_report_path)

        # Write the drift report
        drift_report_path = self._safe_report_path(file_prefix="driftreport")
        drift_report.write(drift_report_path)

        # Run the user-defined callback
        if self.callback:
            self.callback(self, work_report, drift_report)

        # Explicitly return false so that the parent caller above
        # this context sees the exception (if any)
        return False

    def _safe_report_path(self, file_prefix: str) -> pathlib.Path:
        """
        A ``pathlib.Path`` instance that points to a new work report writable
        location that is safe across all OSes.

        Returns:
            pathlib.Path: The path to the new report to be written.
        """
        timestamp = datetime.datetime.now().strftime("%Y-%m-%dT%H%M%S")
        filename = f"{file_prefix}-{timestamp}.json"

        # Remove any characters from the timestamp that OSes don't like
        invalid_chars = [":", "*", "?", '"', "<", ">" "|", "'"]
        for char in invalid_chars:
            filename = filename.replace(char, "_")

        return self.output_path / filename
