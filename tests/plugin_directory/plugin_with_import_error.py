import non_existent_package  # noqa
import pyplugs


@pyplugs.register
def a_plugin():
    """A plugin that will not work, due to import error"""
    return "I wish"
