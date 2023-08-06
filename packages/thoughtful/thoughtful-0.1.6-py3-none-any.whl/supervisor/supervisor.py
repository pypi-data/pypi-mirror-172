from __future__ import annotations

import json
import pathlib
import typing as t

from .adapters.confs import load_from_file
from .adapters.json import JSON
from .helpers import utils
from .helpers.time import timestamp
from .reporter import Reporter
from .step import Step
from .workflow.engine import Workflow

if t.TYPE_CHECKING:
    from .digitalworker import DigitalWorker


class SupervisorError(Exception):
    """Supervisor Error"""


class ManifestError(SupervisorError):
    """A supervisor:manifest error"""


# Supervisor ================================================================-->
#
# The supervisor is the digital workers workflow organizer. It is the floor
# supervisor of a factories assembly line. It is responsible for the order
# of step flow, and using the Reporter to report the results of each step.
class Supervisor:
    """
    A Supervisor is automatically instantiated within a DigitalWorker, and handles
    all the primary logic, flow, and reporting for the worker.
    """

    # reference to the digital worker's manifest dict accessed via `manifest`
    # property (and loaded from manifest.yaml)
    _manifest: dict

    # Reference to the digital worker instance
    _digitalworker: "DigitalWorker"

    _active_return: any
    """The active steps return value"""

    workflow: "Workflow"
    """workflow cache heap  —  a class property works for now,  but if we need
    multiple supervisor instances in the future, we will need to this might
    need to become a dictionary somehow delimited by  `DigitalWorker`  or
    whatever  the  multiplier is.  (This,  assuming in the future we have
    multiple digital workers working together)"""

    reporter: Reporter
    """`Reporter` handles collection of all manifest and runtime data and
    generating a JSON resport"""

    @property
    def manifest(self) -> dict:
        """Load manifest

        Uses digitalworker.config.manifest_path to load the manifest file
        """

        # load manifest if this is the first time we're trying
        # to access the manifest file. This will load self.manifest with
        # the manifest dict, so we can return it directly from there.
        if not self._manifest:
            self._load_manifest()
        return self._manifest

    @manifest.setter
    def manifest(self, _) -> dict:
        raise ManifestError("manifest should not be written to directly")

    def __init__(self, worker: "DigitalWorker"):
        self.signature = timestamp()
        self._digitalworker = worker
        self._active_return = None
        self._manifest = None

        self.reporter = Reporter()
        self.reporter.merge_manifest(self.manifest)

        # Create workflow
        manifest_workflow = self.manifest.get("workflow")
        self.workflow = Workflow(manifest_workflow)

    def _load_manifest(self):
        # Load the digital workers manifest file from disk
        conf = self._digitalworker.config
        file = f"{conf['manifest_path']}/{conf['manifest_filename']}.{conf['manifest_filetype']}"
        self._manifest = load_from_file(file)

    def start(self) -> None:
        """Start a digital workers 'shift' by iterating through it's workflow
        and executing each step.

        Each step function is a decorated function which already contains the
        logic for reporting that step. The workflow simply handles the order
        of execution, and pairing the manifest workflow definition with the
        DigitalWorker's implimentation step methods (tagged by step_id)
        """

        workflow = iter(self.workflow)
        while not workflow.done():
            step = next(workflow)
            self.invoke_step(step)

            step_report = self.reporter.report["workflow"][-1]
            step_report_json = json.dumps(step_report, indent=2)
            print("Step work report: {}".format(step_report_json))

            workflow.validate(step)

        self.end()

    def end(self) -> None:
        """End the digital workers 'shift' by closing the report and saving it
        to the output directory."""

        self.reporter.end_report()
        import pprint
        pprint.pprint(self.reporter.report)
        output_dir: str = self._digitalworker.config['output_dir']
        print("ALLL THE CONFIGS")
        print(self._digitalworker.config)
        path = pathlib.Path(output_dir)
        path.mkdir(parents=True, exist_ok=True)
        report_filename = path / utils.safe_path(
            f'workreport-{timestamp()}.json')
        print("writing report to {}".format(report_filename))

        JSON(self.reporter.report).write_to_disk(report_filename)

    def invoke_step(self, step: Step) -> None:
        """Invoke a step function, along with the arguments returned
        from the previous step, if any.

        This wraps the step function
        with reporting meta-data, performance monitoring, and error
        handling. It's wrapped in a try/except block to catch any
        exceptions and report them

        Args:
            step (Step): The step class wrapping this step function.
            **args: The keyword arguments returned from the previous step.

        """
        # TODO: find next step
        # TODO: create a way to report on warnings, errors, and exceptionsexit
        print(f"Running DigitalWorker Step :: {step}")
        #/ returned = (step(self._digitalworker, )
        #/             if type(kwargs) is dict else step(self._digitalworker))
        returned = step(
            self._digitalworker,
            **(dict(**self._active_return) if self._active_return else {}))

        # Defer to DW for method of screencapture
        self._digitalworker.__take_screenshot__(step.step_id)

        # Report step
        self.reporter.report_step(step.report)

        # cache return values for use in the next step
        self._active_return = returned if type(returned) is dict else None

        return self._active_return

    def __str__(self):
        return f"<Supervisor: for DigitalWorker {self.manifest.get('title')}>"
