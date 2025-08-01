"""Exceptions for the PyPlugs package.

Custom exceptions used by PyPlugs for more helpful error messages
"""

__all__ = [
    "PyPlugsError",
    "UnknownPackageError",
    "UnknownPluginError",
    "UnknownPluginFunctionError",
]


class PyPlugsError(Exception):
    """Base class for all PyPlugs exceptions."""


class UnknownPackageError(PyPlugsError):
    """PyPlugs could not import the given package."""

    def __init__(self, package: str) -> None:
        """Set a consistent error message."""
        super().__init__(f"package '{package}' doesn't exist.")


class UnknownPluginError(PyPlugsError):
    """PyPlugs could not locate the given plugin."""

    def __init__(self, package: str, plugin: str) -> None:
        """Set a consistent error message."""
        super().__init__(
            f"couldn't find plug-in '{plugin}' inside '{package}'. "
            "Register functions with @pyplugs.register to create a plug-in."
        )


class UnknownPluginFunctionError(PyPlugsError):
    """PyPlugs could not locate the given function within a plugin."""

    def __init__(
        self, package: str, plugin: str, func: str, label: str | None = None
    ) -> None:
        """Set a consistent error message."""
        if label is None:
            super().__init__(
                f"couldn't find function '{func}' inside '{package}.{plugin}'. "
                "Use @pyplugs.register to register plug-in functions."
            )
        else:
            super().__init__(
                f"couldn't find function '{func}' inside '{package}.{plugin}' "
                f"with label '{label}. "
                "Use @pyplugs.register to register plug-in functions."
            )
