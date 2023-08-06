from pyconfs import Configuration


def load_from_file(file: str) -> dict:
    """Load a configuration file as a dictionary

    Args:
        file (str): The file to load.

    Returns:
        dict: The loaded config.
    """
    return Configuration.from_file(file).as_dict()


def load_from_string(conf: str) -> dict:
    """Load a configuration string as a dictionary

    Args:
        conf (str): configuration string

    Returns:
        dict: The loaded config.
    """
    return Configuration.from_string(conf).as_dict()
