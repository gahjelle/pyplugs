"""Example of a plug-in consisting of several parts."""

# PyPlugs imports
import pyplugs


@pyplugs.register
def plugin_default() -> str:
    """Register this function first inside the plugin file. It will be the default."""
    return "default"


@pyplugs.register
def plugin_next() -> str:
    """Register the next part of the plug-in."""
    return "next"


@pyplugs.register
def plugin_final() -> str:
    """Register the final part of the plug-in."""
    return "final"
