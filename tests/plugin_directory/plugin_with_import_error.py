"""Example of a plug-in that will crash because of an import error"""

import non_existent_package  # noqa
import pyplugs


@pyplugs.register
def a_plugin():
    """A plug-in that will not work, due to an import error"""
    return "I wish"
