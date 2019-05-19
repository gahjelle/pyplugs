"""Exceptions for the Pyplugs package

Custom exceptions used by Pyplugs for more helpful error messages
"""


class PyplugsException(Exception):
    """Base class for all Pyplugs exceptions"""


class UnknownPackageError(PyplugsException):
    """Pyplugs could not import the given package"""


class UnknownPluginError(PyplugsException):
    """Pyplugs could not locate the given plugin"""


class UnknownPluginFunctionError(PyplugsException):
    """Pyplugs could not locate the given function within a plugin"""
