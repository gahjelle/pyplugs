"""Plugins with interesting return types."""

# PyPlugs imports
import pyplugs


@pyplugs.register
def plugin_string() -> str:
    """Return a string."""
    return "string"


@pyplugs.register
def plugin_integer() -> int:
    """Return an integer."""
    return 28


@pyplugs.register
def plugin_tuple() -> tuple[str, int]:
    """Return a tuple consisting of a string and an integer."""
    return "string", 28
