import time
import typing as t

from . import __version__
from .decorators import singleton
from .helpers.time import timestamp

if t.TYPE_CHECKING:
    from .step import StepReport


@singleton
class Reporter:
    """The Reporter is responsible for logging the runtime of the digital
    worker process (producing a `Report`).
    """

    report: dict
    state_cache: list

    # internal timer
    _start_time: float
    _end_time: float

    def __init__(self) -> None:
        self.state_cache = []
        self.report = {
            "version": "N/A",
            "duration": None,
            "timestamp": timestamp(),
            "workflow": [],
            "supervisor_version": f"{__version__}",
        }

        # start the clock on the report timer
        self._start_time = time.perf_counter()

    def merge_manifest(self, manifest: dict):
        """
        Add manifest values to the worker field
        """

        # todo: add 'contributors', and 'maintainers'
        self.report["worker"] = {
            key: manifest.get(key) for key in [
                "uid",
                "name",
                "description",
                "source",
                "author",
            ]
        }

    def report_step(self, step_report: "StepReport") -> None:
        """Report on an executed workflow step"""
        self.report["workflow"].append(step_report)

    def _flush_state(self) -> dict:
        """
        Reset the state, while returning the previous results.
        """
        state = self.state_cache.copy()
        self.state_cache.clear()
        return state

    def record(self, data: any, title: str = "", description: str = "") -> any:
        """
        Record data to the state cache, which will be logged
        for the current step.

        You can optionally supply a title to describe the data
        """
        if title == "":
            self.state_cache.append(data)
        else:
            self.state_cache.append({
                data: data,
                title: title,
                description: description
            })

        # returns data reference, for dictionaries, lists, etc. These can be
        # updated continuously throughout the current step but will not
        # persist past that step.
        return data

    def record_transformation(self, before: any, after: any) -> None:
        """
        Record data transformations to the state cache, which will be
        logged for the current step
        """
        self.state_cache.append({before: before, after: after})

    def end_report(self):
        """
        End the report and calculate the duration
        """
        self._end_time = time.perf_counter()
        self.report["duration"] = self._end_time - self._start_time

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
