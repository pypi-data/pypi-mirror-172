import datetime
import json
import time

import isodate

from . import __version__
from .annotations import RunResult
from .manifest import Step
from .recorder import Recorder


class Reporter:
    def __init__(self) -> None:
        """
        Reporter — Responsible for logging the runtime of the digital
        worker process, producing a detailed `Work Report`.

        The Work Report is a structured log in the form of JSON which adheres to the
        [Report Schema](schemas/report.schema.json) defined and documented in the
        [Schema Library](https://github.com/Thoughtful-Automation/schemas)

        Attributes:
            self.report (dict): The report to write after a worker is complete.
        """
        self.report = {
            "version": "N/A",
            "timestamp": datetime.datetime.utcnow().isoformat(),
            "workflow": [],
            "supervisor_version": f"{__version__}",
        }

        # Start the clock on the report timer
        self.start_time = time.perf_counter()

    def write(self, filename: str) -> None:
        """
        Write the report to a file.

        Args:
            filename: Where to write the file.

        Returns:
            None
        """
        with open(filename, "w") as out:
            json.dump(self.report, out)

    def report_step(self, step: Step, result: RunResult, log: Recorder) -> None:
        """
        Report on an executed workflow step. Creates a step report, and appends
        that report to `self.report`'s workflow.

        Args:
            step (Step): The step that was executed.
            result (RunResult): The result of running the step
            log (Recorder): The logs from the `DigitalWorker` running the step.

        Returns:
            None
        """

        step_report = {
            "step_id": step.step_id,
            "step_type": step.step_type,
            "step_status": result.status,
            "title": step.title,
            "description": step.description,
            "start_time": result.start.isoformat(),
            "end_time": result.end.isoformat(),
            "duration": isodate.duration_isoformat(result.duration),
            "args": result.input if result.input else {},
            "returned": result.output,
            "data_log": log.data,
            "message_log": log.messages,
        }
        self.report["workflow"].append(step_report)

    def end_report(self) -> None:
        """
        End the report and calculate the duration.
        """
        end_time = time.perf_counter()
        duration_seconds = end_time - self.start_time
        duration_delta = datetime.timedelta(seconds=duration_seconds)
        self.report["duration"] = isodate.duration_isoformat(duration_delta)
