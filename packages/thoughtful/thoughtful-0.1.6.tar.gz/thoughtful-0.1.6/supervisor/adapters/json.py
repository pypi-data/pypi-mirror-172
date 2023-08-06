"""JSON Utilities"""
import json
from urllib.request import urlopen

from ..helpers.utils import methoddispatch


class JSON:
    """
    JSON Utility

    Loads, parses, writes, stores and otherwise
    works with JSON Objects and JSON files
    """

    _source: dict
    """Stores the dictionary source of the JSON for later saving"""

    #@singledispatchmethod
    @methoddispatch
    def __init__(self, x):
        x_type = type(x)
        raise NotImplementedError(f"""
            Supervisor::JSON utility module must be a string of a path to a local JSON file,
            a dictionary, or you must use the static method `JSON.load_from_url(url)`.

            Type given: {x_type}
        """)

    @__init__.register
    def _(self, file_path: str):
        """
        Initialize JSON from a file path
        """
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(self._dump, f)
            self._source = json.loads(self._dump)

    @__init__.register
    def _(self, dictionary: dict):
        """
        Initialize JSON from a dictionary
        """
        self._source = dictionary

    @staticmethod
    def load_from_url(url: str) -> 'JSON':
        """
        Loads JSON from remote url
        """
        response = urlopen(url)
        return JSON(response.read())

    def write_to_disk(self, file_name: str):
        """
        Write JSON to disk
        """
        with open(file_name, 'w') as outfile:
            json.dump(self._source, outfile)

    def keys(self):
        """Returns the keys through a `dict_keys` object.

        >>> JSON({"a": "anteater", "b": "bumblebee"}).keys()
        dict_keys(["a","b"])
        """
        return self._source.keys()

    def values(self):
        """
        Returns the dictionary values through a `dict_values` object.

        >>> JSON({"a": "anteater", "b": "bumblebee"}).values()
        dict_values(["anteater", "bumblebee"])
        """
        return self._source.values()

    def items(self):
        """
        Returns both the keys and values through a `dict_items` object.

        >>> JSON({"a": "anteater", "b": "bumblebee"}).items()
        dict_items([("a","anteater"),("b","bumblebee")])
        """
        return self._source.items()

    def read_from_file(self, source):
        """
        Print each line from a JSON file
        """
        with open(source, encoding='utf-8') as f:
            for line in f:
                print(line.read_line())

    def get(self, key: str, default=None):
        return self._source[key] or default

    def print(self) -> 0:
        print(json.dumps(self._source, indent=4, sort_keys=True))
