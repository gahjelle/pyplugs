"""A plug-in that will be sorted after other plug-ins"""
# PyPlugs imports
import pyplugs


@pyplugs.register(sort_value=10)
def plugin_last():
    """This function should sort after other plug-in functions"""
    return "last"
