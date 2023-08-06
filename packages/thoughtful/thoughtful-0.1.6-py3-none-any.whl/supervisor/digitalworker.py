import os
import sys
import time
import typing as t

# typing.TypedDict introduced in python 3.8
# https://docs.python.org/3/library/typing.html#typing.TypedDict
if sys.version_info < (3, 8):
    from typing_extensions import typing as t
else:
    import typing as t

from supervisor import Supervisor


class WorkerConfig(t.TypedDict):
    """
    WorkerConfig is a TypedDict that defines the structure of the DigitalWorker
    class config.

    `Manifest` file defaults to `project_root/manifest.yaml`, when the DigitalWorker
    subclass is instantiated in a root module (usually, `project_root/task.py`).
    """

    manifest_path: str
    """ The directory path to the manifest file. Defaults to same directory as the root
    DigitalWorker subclass."""

    manifest_filetype: str
    """ The filetype of the manifest file. Defaults to 'yaml'. Can be
    .yml, .manifest_json or .ini"""

    manifest_filename: str
    """Defaults to `manifest`. Not recommended to change this."""

    output_dir: str
    """ The directory path to the output directory. Defaults to same directory
    as the digital worker subclass"""

    screenshots_dir: t.Optional[str]
    """The directory path to output screenshots. Defaults to 'screenshots'"""


class DigitalWorker():
    """
    DigitalWorker Abstract Base Class — Used to define the interface of a
    digital worker.

    Examples usage:

    """
    supervisor: 'Supervisor'
    report: dict

    # Internal config options
    _config: WorkerConfig

    def __init__(self) -> None:
        """Starts the workflow on initialization.
        """
        self.config = self.__configure__()  # loads default config
        self.__beforerun__()
        time.sleep(1)
        self.supervisor = Supervisor(self)
        time.sleep(1)
        self.supervisor.start()

    @property
    def config(self) -> WorkerConfig:
        """Gets the config"""
        return self._config

    @config.setter
    def config(self, config: WorkerConfig) -> None:
        """Sets the config, using default values."""
        dw_dir: str = os.getcwd()  # inspect.getfile(self.__class__)
        self._config = WorkerConfig({
            # defaults
            'manifest_filetype': 'yaml',
            'manifest_filename': 'manifest',
            'manifest_path': dw_dir + 'manifest',
            'output_dir': dw_dir + 'output',
            'screenshots_dir': dw_dir + 'screenshots',

            # override defaults
            **config
        })

    @config.deleter
    def config(self):
        """Deletes the custom configuration. It uses the config setter, which
        will only reset the default values, and not the core _config.
        """
        self.config = {}

    def __beforerun__(self) -> None:
        """Setup a digital worker prior to starting.

        The __beforerun__ method can be used to setup an instance of the digital
        worker with implimentation configuration details and other properties
        to be accessed in later step methods.

        You can also use this method to process the initial state before the
        digital worker is started.
        """

    def __configure__(self) -> dict:
        """Configure a digital worker prior to loading the manifest file.

        The __configure__ method can be used to configure an instance of the
        digital worker with implimentation configuration details to override
        the default values.

        Optional Values:

            manifest_path
                typically,a DigitalWorker task file is created in the root dir.
                use this to configure the path to the manifest file.

            # can adjust this to be .yml, .json, .ini
            'manifest_filetype': "yaml",
            'manifest_filename': "manifest",

            # override the above configuration with any of the given fields

        example:

            >>> class MyDigitalWorker(DigitalWorker):
            >>>     # configure the digital worker with a custom manifest path
            >>>     def __configure__(self):
            >>>         return {
            >>>             'manifest_path': '/home/user/digitalworker/',
            >>>             'manifest_filetype': 'yaml', # default
            >>>             'manifest_filename': 'manifest' # default
            >>>         }
        """
        return {}

    def __take_screenshot__(self, _: str) -> None:
        """Override this method to take a screenshot of the current step"""
