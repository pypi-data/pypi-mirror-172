"""
This module contains the code for the MainContext class. This class is
a context manager that supervises the execution of the main body of the process.

On entrance, it will verify the process manifest.

Upon exit, it will convert the step report into the run report. It will also
evaluate the ultimate status of the process—success if no exceptions were
raised, failure otherwise.

Without this context, the output manifest and run report would not be
generated at the end of the process.
"""

from __future__ import annotations

import datetime
import logging
import pathlib
from types import TracebackType
from typing import Callable, Optional, Type, Union

from supervisor.manifest import Manifest
from supervisor.recorder import Recorder
from supervisor.reporting.report_builder import ReportBuilder
from supervisor.reporting.status import Status

logger = logging.getLogger(__name__)


class MainContext:
    """
    Supervises an entire digital worker run and generates a work report
    and drift report for the run from the digital worker's manifest.

    You can optionally specify a callback function that will be run when
    this context is finished via the `callback` param in the constructor. A
    callback is a function that is invoked with two parameters: the
    current context (as the `MainContext` instance) and the `Report`
    generated from this digital worker's run.

    For example:

    .. code-block:: python

        def print_work_report(
            ctx: MainContext,
            work_report: Report
        ):
            print(work_report.__json__())

        def main()
            # ...

        with supervise(callback=print_work_report):
            main()
    """

    def __init__(
        self,
        report_builder: ReportBuilder,
        recorder: Recorder,
        manifest: Union[str, pathlib.Path],
        output_dir: Union[str, pathlib.Path],
        callback: Optional[Callable] = None,
    ):
        """
        Args:
            report_builder (ReportBuilder): A ReportBuilder object that will
                receive the step reports and provide the run report.
            recorder (Recorder): A Recorder object that will record optional
                messages and logs throughout the process execution.
            manifest (str, Path): A pathlike object that points to the manifest
                file for the process.
            output_dir (str, Path): A pathlike object that points to the output
                directory for the process. This will receive the run report and
                output manifest.
            callback (callable, optional): a function that is invoked with three
                parameters: the current context (as the `MainContext` instance)
                and the `Report` generated from this digital worker's run.
        """
        self.report_builder = report_builder
        self.recorder = recorder
        self.manifest_path = pathlib.Path(manifest)
        self.output_path = pathlib.Path(output_dir)
        self.callback = callback

    def __enter__(self) -> MainContext:
        """
        Logic for when this context is first started. Attempts to load the
        manifest and returns itself as the context.

        Returns:
            MainContext: This instance.
        """
        # Check if the manifest exists and warn if it doesn't
        if self.manifest_path.exists():
            # Check if manifest is valid, and warn if it isn't
            try:
                _ = Manifest.from_file(self.manifest_path)
            except Exception as e:
                logger.exception("warning: could not read manifest")
        else:
            logger.warning(f"{self.manifest_path=} does not exist")
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
        self.report_builder.status = Status.FAILED if exc_type else Status.SUCCEEDED
        work_report = self.report_builder.to_report()

        # Create the output directory if it doesn't already exist
        self.output_path.mkdir(parents=True, exist_ok=True)

        # Write the work report
        work_report_path = self._safe_report_path(file_prefix="run-report")
        work_report.write(work_report_path)

        # Write the manifest back out as a JSON file
        manifest_json_path = self.output_path / "manifest.json"
        Manifest.yaml_to_json(self.manifest_path, manifest_json_path)

        # Run the user-defined callback
        if self.callback:
            self.callback(self, work_report)

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
