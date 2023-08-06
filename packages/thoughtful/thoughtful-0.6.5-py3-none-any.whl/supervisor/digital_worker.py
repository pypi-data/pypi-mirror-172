from supervisor.annotations import Annotatable
from supervisor.deprecated_markers import DeprecatedBecauseNonDynamic
from supervisor.manifest import StepId
from supervisor.recorder import Recorder


class DigitalWorker(Annotatable, DeprecatedBecauseNonDynamic):
    def __init__(self):
        """
        A digital worker to be run by Supervisor.

        Attributes:
            self.recorder (Recorder): Use this to record logs and data during
                step runs.
        """
        self.recorder = Recorder()

    def __take_screenshot__(self, step_id: StepId) -> None:
        """Override this method to take a screenshot of the current step"""
        pass

    def __on_exit__(self) -> None:
        """
        Override this method to perform any cleanup actions before exiting.
        """
        pass
