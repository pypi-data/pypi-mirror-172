import datetime
import json
import time

from . import __version__
from .annotations import RunResult
from .manifest import Step
from .recorder import Recorder


class Reporter:
    """
    Reporter — Responsible for logging the runtime of the digital
    worker process, producing a detailed `Work Report`.

    The Work Report is a structured log in the form of JSON which adheres to the
    [Report Schema](schemas/report.schema.json) defined and documented in the
    [Schema Library](https://github.com/Thoughtful-Automation/schemas)
    """

    def __init__(self) -> None:
        self.report = {
            "version": "N/A",
            "duration": None,
            "timestamp": datetime.datetime.utcnow().isoformat(),
            "workflow": [],
            "supervisor_version": f"{__version__}",
        }

        # start the clock on the report timer
        self.start_time = time.perf_counter()

    def write(self, filename: str) -> None:
        with open(filename, "w") as out:
            json.dump(self.report, out)

    def report_step(self, step: Step, result: RunResult, log: Recorder) -> None:
        """Report on an executed workflow step"""
        step_report = {
            "step_id": step.step_id,
            "step_type": step.step_type,
            "step_status": result.status,
            "title": step.title,
            "description": step.description,
            "start_time": result.start.isoformat(),
            "end_time": result.end.isoformat(),
            "args": result.input if result.input else {},
            "returned": result.output,
            "data_log": log.data,
            "message_log": log.messages,
        }
        self.report["workflow"].append(step_report)

    def end_report(self):
        """
        End the report and calculate the duration
        """
        end_time = time.perf_counter()
        self.report["duration"] = end_time - self.start_time

    def get_workflow_length(self) -> int:
        """Returns the length of workflow steps recorded

        Keep in mind, the currently executing step has not yet been recorded
        so if the 5th record is being run, the length of steps recorded will
        be 4"""
        return len(self.report.get("workflow"))

    def __snapshot__(self):
        """
        Take a snapshot of the report and return it
        """
        return self.report
