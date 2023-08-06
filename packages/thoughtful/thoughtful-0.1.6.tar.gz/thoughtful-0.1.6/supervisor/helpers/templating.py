"""utils/templating.py - Helper functions for working with template strings"""
from chevron import render


def process_template(template: str, args: dict) -> str:
    """Compile a template string into a data-infused string.

    Args:
        template (str): The template string.
        **args: The keyword arguments to pass to the template processor.

    Returns:
        (function): The compiled template function.

    Example:
        >>> process_template('Hello, {{# name }}!', name='World')
        >>> Hello, World!
    """
    return render(template, args)
