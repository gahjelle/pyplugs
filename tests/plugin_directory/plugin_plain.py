"""Module doc-string
"""

# PyPlugs imports
import pyplugs


@pyplugs.register
def plugin_plain():
    """A plain plugin

    This is the plain docstring.
    """
    return "plain"
