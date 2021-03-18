"""Example of a plug-in consisting of several parts"""
# PyPlugs imports
import pyplugs


@pyplugs.register
def plugin_default():
    """The first registered function inside a plug-in will be called by default"""
    return "default"


@pyplugs.register
def plugin_next():
    """This is the next part of the plug-in"""
    return "next"


@pyplugs.register
def plugin_final():
    """This is the final part of the plug-in"""
    return "final"
