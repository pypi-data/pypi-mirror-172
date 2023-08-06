import warnings

from supervisor.manifest import Manifest


def load(filename, loader=None) -> Manifest:
    """
    Deprecated method of loading a manifest from a YAML file.

    Args:
        filename: The name of the .yaml file.
        loader: (Unused but kept for backwards compatibility.

    Returns:
        A manifest from the loaded file
    """
    # Turn off warning filter and print a deprecation warning
    warnings.simplefilter("once", DeprecationWarning)
    warnings.warn(
        f"{__name__}.{load.__name__} is deprecated and will be removed in a "
        + "future release. Use Manifest.from_file instead.",
        category=DeprecationWarning,
    )

    return Manifest.from_file(filename)
