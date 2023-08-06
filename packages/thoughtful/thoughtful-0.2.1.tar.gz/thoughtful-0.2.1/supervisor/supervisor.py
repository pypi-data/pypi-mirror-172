from __future__ import annotations

import datetime
import json
import pathlib
import pprint
from typing import Optional, Tuple

from supervisor.state_machine import MachineState, Node, StateMachine

from .annotations import Annotation, RunResult
from .digital_worker import DigitalWorker
from .manifest import Manifest, Step
from .recorder import Recorder
from .reporter import Reporter
from .yaml import load_yaml


class Supervisor:
    def __init__(
        self,
        worker: DigitalWorker,
        reporter: Optional[Reporter] = None,
        manifest: Optional[Manifest] = None,
        screenshot_path: Optional[pathlib.Path] = None,
        output_path: Optional[pathlib.Path] = None,
        print_step_reports: bool = False,
        print_final_report: bool = False,
    ):
        """
        The supervisor is the digital worker's workflow organizer. It is the
        floor supervisor of a factory's assembly line. It is responsible for
        the order of step flow, and using the Reporter to report the results
        of each step.

        Handles all the primary logic, flow, and reporting for the worker.
        """
        # New properties from constructor args
        self.worker: DigitalWorker = worker
        self.manifest = manifest if manifest else Supervisor.default_manifest()
        self.reporter = reporter if reporter else Reporter()
        self.reporter.report["worker"] = self.manifest.to_report()
        self.screenshot_path = (
            screenshot_path if screenshot_path else pathlib.Path.cwd() / "screenshots"
        )
        self.output_path = output_path if output_path else pathlib.Path.cwd() / "output"
        self.print_step_reports = print_step_reports
        self.print_final_report = print_final_report

        # Other new properties
        self.state_machine = StateMachine.from_steps(self.manifest.workflow)

    def run(self) -> dict:
        """Start a digital workers 'shift' by iterating through its workflow
        and executing each step.

        Each step function is a decorated function which already contains the
        logic for reporting that step. The workflow simply handles the order
        of execution, and pairing the manifest workflow definition with the
        DigitalWorker's implementation step methods (tagged by step_id)
        """

        previous_result = RunResult.empty_result()
        current_node = self.state_machine.next()
        while current_node:
            # Find the step and annotation for the node, and run it
            step, annot = self._node_setup(current_node)
            result = self._node_run(step, annot, previous_result)
            self._node_teardown(step, result)

            # Set up the next iteration and find the next node to run
            if step.is_conditional:
                # Fail out if a conditional step returns a non-boolean
                if type(result.output) != bool:
                    raise TypeError("Output of conditional step must be boolean")
                predicate = result.output
            else:
                predicate = None
            previous_result = result
            current_node = self.state_machine.next(predicate=predicate)

        # Tear down run
        self.worker.__on_exit__()
        self._finish_report()
        return self.reporter.report

    def _finish_report(self) -> None:
        """End the digital workers 'shift' by closing the report and saving it
        to the output directory."""

        # finalize the report
        self.reporter.end_report()

        # Print the report
        if self.print_final_report:
            pprint.pprint(self.reporter.report)

        self.output_path.mkdir(parents=True, exist_ok=True)
        report_path = self._safe_report_path()
        if self.print_final_report:
            print("Writing report to {}".format(report_path))
        self.reporter.write(str(report_path))

    @classmethod
    def default_manifest(cls):
        default_path = pathlib.Path.cwd() / "manifest.yaml"
        return load_yaml(default_path)

    def __repr__(self) -> str:
        return "<{}(worker={})>".format(self.__class__.__name__, self.worker)

    def __str__(self):
        return f"{self.__class__.__name__} for '{self.manifest.name}' digital worker"

    # Private implementation
    def _node_setup(self, current_node: Node) -> Tuple[Step, Optional[Annotation]]:
        # Grab the step
        step = self.manifest.steps_by_id[current_node.uuid]

        # Grab the annotation
        if (step.step_id not in self.worker.__steps__) and step.has_children:
            annot = None
        else:
            annot = self.worker.__steps__[step.step_id]
        return step, annot

    def _node_run(
        self, step: Step, annot: Annotation, previous_result: RunResult
    ) -> RunResult:
        # Run the annotation
        if self.print_step_reports:
            print(f"Invoking step '{step.title}'")

        if not annot:
            return RunResult.empty_result()

        # Ignore previous results that weren't dicts
        if type(previous_result.output) == dict:
            formed_input = previous_result.output
        else:
            formed_input = {}
        return annot.run(self.worker, formed_input)

    def _node_teardown(self, step: Step, result: RunResult) -> None:
        # Node teardown
        self.worker.__take_screenshot__(step.step_id)

        # Report step
        self.reporter.report_step(step, result, self.worker.recorder)

        # Reset the logger for the default_next step
        self.worker.recorder = Recorder()

        if self.print_step_reports:
            step_report = self.reporter.report["workflow"][-1]
            step_report_json = json.dumps(step_report, indent=2)
            print("AnnotationRunner work report: {}".format(step_report_json))

    def _safe_report_path(self) -> pathlib.Path:
        timestamp = datetime.datetime.utcnow().isoformat()
        filename = f"workreport-{timestamp}.json"
        # Remove any characters from the timestamp that OSes don't like
        invalid_chars = [":", "*", "?", '"', "<", ">" "|", "'"]
        for char in invalid_chars:
            filename = filename.replace(char, "_")

        return self.output_path / filename
