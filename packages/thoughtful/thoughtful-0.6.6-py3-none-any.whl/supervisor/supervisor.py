from __future__ import annotations

import datetime
import json
import pathlib
from typing import Optional, Tuple

from .annotations import Annotation, RunResult
from .deprecated_markers import DeprecatedBecauseNonDynamic
from .digital_worker import DigitalWorker
from .manifest import Manifest, Step
from .recorder import Recorder
from .reporter import Report, Reporter
from .state_machine import Node, StateMachine
from .yaml_loader import load


class Supervisor(DeprecatedBecauseNonDynamic):
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

        Args:
            worker (DigitalWorker): The worker to supervise.
            reporter (Reporter, optional): Maintains the work report that
                is written during worker execution. Defaults to None.
            manifest (Manifest, optional): The manifest of the digital worker
                to supervise. Typically, this is constructed from a YAML file.
                Defaults to None.
            screenshot_path (pathlib.Path): Where screenshots are written to.
            output_path (pathlib.Path): Where the work report will be written
                to.
            print_step_reports (bool): If True, print each step report to
                stdout after each step is run. If False, silence these step
                reports in stdout.
            print_final_report (bool): If True, print the final work report
                to stdout after the worker is executed. If False, silence
                the work report in stdout.

        Attributes:
            worker (DigitalWorker): The worker to execute.
            manifest (Manifest): The digital worker's design document.
            reporter (Reporter): The work report maintainer.
            screenshot_path (pathlib.Path): Where screenshots are written to.
            output_path (pathlib.Path): Where the work report will be written
                to.
            print_step_reports (bool): If True, print each step report to
                stdout after each step is run. If False, silence these step
                reports in stdout.
            print_final_report (bool): If True, print the final work report
                to stdout after the worker is executed. If False, silence
                the work report in stdout.
            state_machine (StateMachine): Determines the order of steps to
                be executed.
        """
        super().__init__()
        if worker is None:
            raise ValueError("Cannot have a None worker")
        if not isinstance(worker, DigitalWorker):
            _type = type(worker)
            raise TypeError(f"worker must be a DigitalWorker (got {_type})")

        # New properties from constructor args
        self.worker: DigitalWorker = worker
        self.manifest = manifest if manifest else Supervisor.default_manifest()
        self.reporter = reporter if reporter else Reporter(manifest=manifest)
        self.screenshot_path = (
            screenshot_path if screenshot_path else pathlib.Path.cwd() / "screenshots"
        )
        self.output_path = output_path if output_path else pathlib.Path.cwd() / "output"
        self.print_step_reports = print_step_reports
        self.print_final_report = print_final_report

        # Other new properties
        self.state_machine = StateMachine.from_steps(self.manifest.workflow)

    def run(self) -> Report:
        """
        Start a digital workers 'shift' by iterating through its workflow
        and executing each step.

        Each step function is a decorated function which already contains the
        logic for reporting that step. The workflow simply handles the order
        of execution, and pairing the manifest workflow definition with the
        DigitalWorker's implementation step methods (tagged by step_id).

        Returns:
            dict: The work report.
        """

        previous_result = RunResult.empty_result()
        current_node = self.state_machine.next()
        while current_node:
            # Find the step and annotation for the node, and run it
            step, annot = self._node_setup(current_node)
            if self.print_step_reports:
                print(f"Invoking step '{step.title}'")

            # Run and finalize the node
            result = self._node_run(annot, previous_result)
            self._node_teardown(step, result)

            # Set up the next iteration and find the next node to run -> add branching logic
            if step.step_type == "conditional" or step.step_type == "branch":
                predicate = result.output
            else:
                predicate = None

            previous_result = result
            current_node = self.state_machine.next(predicate=predicate)

        # Tear down run
        self.worker.__on_exit__()
        self._finish_report()
        return self.reporter.report

    @classmethod
    def default_manifest(cls) -> Manifest:
        """
        A default manifest to load for a new instance of this class, if none is
        provided.

        Returns:
           Manifest: The new manifest, loaded from the default location.
        """
        default_path = pathlib.Path.cwd() / "manifest.yaml"
        return load(default_path)

    def __repr__(self) -> str:
        return "<{}(worker={})>".format(self.__class__.__name__, self.worker)

    def __str__(self):
        return f"{self.__class__.__name__} for '{self.manifest.name}' digital worker"

    # Private implementation
    def _node_setup(self, current_node: Node) -> Tuple[Step, Optional[Annotation]]:
        """
        Prepares a node to be executed by finding the ``Step`` and
        ``Annotation`` associated with the ``Node``.

        Args:
            current_node (Node): The current node.

        Returns:
            tuple: The step (and possibly the corresponding annotation) based
                on the node's ID.
        """
        # Grab the step
        step = self.manifest.steps_by_id[current_node.uuid]

        # Grab the annotation
        if (step.step_id not in self.worker.__steps__) and step.has_children:
            annot = None
        else:
            annot = self.worker.__steps__[step.step_id]
        return step, annot

    def _node_run(self, annot: Annotation, previous_result: RunResult) -> RunResult:
        """
        Executes an ``Annotation`` and returns the result.

        Args:
            annot (Annotation): The annotation to be run.
            previous_result (RunResult): The result of the last run.

        Returns:
            RunResult: The result of running this step.
        """
        if not annot:
            return RunResult.empty_result()

        # Ignore previous results that weren't dicts
        if type(previous_result.output) == dict:
            formed_input = previous_result.output
        else:
            formed_input = {}
        return annot.run(self.worker, formed_input)

    def _node_teardown(self, step: Step, result: RunResult) -> None:
        """
        Finalizes the running of a node by taking a screenshot, writing the
        results of the run to the report, and clearing out the `worker`'s
        ``Recorder`` for the next step.

        Args:
            step (Step): The step associated with the ``Annotation`` that was
                executed.
            result (RunResult): The result of running the ``Annotation``.
        """
        # Record a screenshot
        self.worker.__take_screenshot__(step.step_id)
        # Report step
        # Deep copy the logs, because we'll replace the recorder instance
        # next
        messages, data = self.worker.recorder.copy_logs()
        self.reporter.report_step(step, result, message_log=messages, data_log=data)

        # Reset the logger for the default_next step
        self.worker.recorder = Recorder()

        if self.print_step_reports:
            step_report = self.reporter.report.workflow[-1]
            step_report_json = json.dumps(step_report.__json__(), indent=2)
            print("AnnotationRunner work report: {}".format(step_report_json))

    def _finish_report(self) -> None:
        """
        End the digital workers 'shift' by closing the report and saving it
        to the output directory.
        """

        # Finalize the report
        final_report = self.reporter.end_report()

        # Print the report
        if self.print_final_report:
            json_str = json.dumps(final_report.__json__(), indent=2)
            print(json_str)

        self.output_path.mkdir(parents=True, exist_ok=True)
        report_path = self._safe_report_path()
        if self.print_final_report:
            print("Writing report to {}".format(report_path))
        final_report.write(str(report_path))

    def _safe_report_path(self) -> pathlib.Path:
        """
        A ``pathlib.Path`` instance that points to a new work report writable
        location that is safe across all OSes.

        Returns:
            pathlib.Path: The path to the new report to be written.
        """
        timestamp = datetime.datetime.utcnow().isoformat()
        filename = f"workreport-{timestamp}.json"
        # Remove any characters from the timestamp that OSes don't like
        invalid_chars = [":", "*", "?", '"', "<", ">" "|", "'"]
        for char in invalid_chars:
            filename = filename.replace(char, "_")

        return self.output_path / filename
