from collections import OrderedDict

import yaml
from supervisor.manifest import Manifest, Step
from yaml.dumper import SafeDumper
from yaml.loader import SafeLoader

YAML_TAB_PROBLEM = "found character '\\t' that cannot start any token"


class LoaderError(Exception):
    """Base class for exceptions raised when loading yaml/json/etc."""


class ConfigReadError(LoaderError):
    """A configuration file could not be read."""

    def __init__(self, filename, reason=None):
        self.filename = filename
        self.reason = reason

        message = "file {0} could not be read".format(filename)
        if (
            isinstance(reason, yaml.scanner.ScannerError)
            and reason.problem == YAML_TAB_PROBLEM
        ):
            # Special-case error message for tab indentation in YAML markup.
            message += ": found tab character at line {0}, column {1}".format(
                reason.problem_mark.line + 1,
                reason.problem_mark.column + 1,
            )
        elif reason:
            # Generic error message uses exception's message.
            message += ": {0}".format(reason)

        super(ConfigReadError, self).__init__(message)


class Loader(SafeLoader):
    """A yaml loader adapter. This loader deviates from the official
    YAML spec in a few convenient ways:
    - All strings as are Unicode objects.
    - All maps are OrderedDicts.
    - Strings can begin with % without quotation.
    """

    # All strings should be Unicode objects, regardless of contents.
    def _construct_unicode(self, node):
        return self.construct_scalar(node)

    def construct_yaml_map(self, node):

        mapping = OrderedDict()
        if isinstance(node, yaml.MappingNode):
            self.flatten_mapping(node)

        for key_node, value_node in node.value:
            key = self.construct_object(key_node)

            if key == "workflow":
                value = self.construct_sequence(value_node)
            else:
                value = self.construct_object(value_node, deep=False)

            mapping[key] = value

        manifest = Manifest(**mapping)
        # add temporary method
        manifest.set_steps_by_id()
        yield manifest

    def construct_step(self, node, deep=True):
        if isinstance(node, yaml.MappingNode):
            self.flatten_mapping(node)
        mapping = OrderedDict()
        for key_node, value_node in node.value:
            key = self.construct_object(key_node, deep=deep)

            try:
                hash(key)
            except TypeError as exc:
                raise yaml.constructor.ConstructorError(
                    "while constructing a mapping",
                    node.start_mark,
                    "found unacceptable key (%s)" % exc,
                    key_node.start_mark,
                )

            if key == "steps":
                value = self.construct_sequence(value_node)
            else:
                value = self.construct_object(value_node, deep=deep)

            mapping[key] = value

        mapping = Step(**mapping)
        Step.update_forward_refs()
        return mapping

    # Allow bare strings to begin with %. Directives are still detected.
    def check_plain(self):
        plain = super(Loader, self).check_plain()
        return plain or self.peek() == "%"

    def construct_sequence(self, node, deep=True):
        if not isinstance(node, yaml.SequenceNode):
            raise yaml.ConstructorError(
                None,
                None,
                "expected a sequence node, but found %s" % node.id,
                node.start_mark,
            )
        result = [self.construct_step(child, deep=True) for child in node.value]
        Step.update_forward_refs()
        return result

    @staticmethod
    def add_constructors(loader):
        """Modify a PyYAML Loader class to add extra constructors for strings
        and maps. Call this method on a custom Loader class to make it behave
        like Confuse's own Loader
        """
        loader.add_constructor("tag:yaml.org,2002:str", Loader._construct_unicode)
        loader.add_constructor("tag:yaml.org,2002:map", Loader.construct_yaml_map)
        loader.add_constructor("tag:yaml.org,2002:omap", Loader.construct_yaml_map)


Loader.add_constructors(Loader)


def load_yaml(filename, loader=Loader):
    """Read a YAML document from a file. If the file cannot be read or
    parsed, a ConfigReadError is raised.
    loader is the PyYAML Loader class to use to parse the YAML. By default,
    this is Confuse's own Loader class, which is like SafeLoader with
    extra constructors.
    """
    try:
        with open(filename, "rb") as f:
            return yaml.load(f, Loader=loader)
    except (IOError, yaml.error.YAMLError) as exc:

        raise ConfigReadError(filename, exc)


def test_load_yaml(filename, loader=Loader):
    """For testing purposes - load yaml str"""
    return yaml.load(filename, Loader=loader)
