from __future__ import annotations

import datetime
import pathlib
from typing import Union

from supervisor import yaml_loader
from supervisor.dynamic.drift_report import DriftReport
from supervisor.dynamic.report_builder import ReportBuilder
from supervisor.recorder import Recorder


class MainContext:
    def __init__(
        self,
        report_builder: ReportBuilder,
        recorder: Recorder,
        manifest: Union[str, pathlib.Path],
        output_dir: Union[str, pathlib.Path],
    ):
        """
        Supervises an entire digital worker run, generates a work report
        from the digital worker's manifest, and
        Args:
            report_builder: Where step reports will be sent to
            recorder: Where messages and data logs will be sent to
            manifest: The digital worker's manifest definition
            output_dir: Where the work report and drift report will
                be written to
        """
        self.report_builder = report_builder
        self.recorder = recorder
        self.manifest_path = pathlib.Path(manifest)
        self.output_path = pathlib.Path(output_dir)

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
        manifest = yaml_loader.load(self.manifest_path)
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
