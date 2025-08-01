"""A plug-in that will be sorted before other plug-ins."""

# PyPlugs imports
import pyplugs


@pyplugs.register(sort_value=-10)
def plugin_first() -> str:
    """Add a sort value so this function sorts before other plug-in functions."""
    return "first"
