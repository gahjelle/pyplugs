"""Example of a plug-in consisting of several parts"""

# PyPlugs imports
import pyplugs


@pyplugs.register
def plugin_one() -> str:
    """One regular plug-in function"""
    return "one"


@pyplugs.register
def plugin_two() -> str:
    """A second regular plug-in function"""
    return "two"


@pyplugs.register(label="label")
def plugin_first_label() -> str:
    """A labeled plug-in function"""
    return "first"


@pyplugs.register(label="label")
def plugin_second_label() -> str:
    """Another labeled plug-in function"""
    return "second"


@pyplugs.register(label="another_label")
def plugin_final_label() -> str:
    """A plug-in function with a different label"""
    return "final"
