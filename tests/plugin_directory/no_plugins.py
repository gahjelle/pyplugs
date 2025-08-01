"""Example of a module that is not a plug-in as no functions are registered."""


def not_a_plugin() -> str:
    """Don't register the function, so it's not a plug-in."""
    return "nope"
