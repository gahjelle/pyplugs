"""A plug-in that will be sorted before other plug-ins"""
# PyPlugs imports
import pyplugs


@pyplugs.register(sort_value=-10)
def plugin_first():
    """This function should sort before other plug-in functions"""
    return "first"
