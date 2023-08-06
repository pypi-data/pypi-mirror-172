import datetime
import json
import pathlib
from typing import Union

from supervisor import yaml
from supervisor.dynamic.function_runner import FunctionRunner


class SuperviseContext:
    def __init__(
        self,
        runner: FunctionRunner,
        manifest: Union[str, pathlib.Path] = "manifest.yaml",
        output_dir: Union[str, pathlib.Path] = "output/",
    ):
        self.runner = runner
        self.manifest_path = pathlib.Path(manifest)
        self.output_path = pathlib.Path(output_dir)

    def __enter__(self):
        pass

    def __exit__(self, exc_type, exc_val, exc_tb):
        manifest = yaml.load_yaml(self.manifest_path)
        work_report, drift_report = self.runner.finish_reports(manifest)

        # Write the work report
        work_report_path = self._safe_report_path(file_prefix="workreport")
        work_json = json.dumps(work_report.__json__())
        with work_report_path.open("w") as f:
            f.write(work_json)

        # Write the drift report
        drift_report_path = self._safe_report_path(file_prefix="driftreport")
        drift_json = json.dumps(drift_report.__json__())
        with drift_report_path.open("w") as f:
            f.write(drift_json)

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
