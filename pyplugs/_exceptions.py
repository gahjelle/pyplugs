"""Exceptions for the PyPlugs package

Custom exceptions used by PyPlugs for more helpful error messages
"""


class PyPlugsException(Exception):
    """Base class for all PyPlugs exceptions"""


class UnknownPackageError(PyPlugsException):
    """PyPlugs could not import the given package"""


class UnknownPluginError(PyPlugsException):
    """PyPlugs could not locate the given plugin"""


class UnknownPluginFunctionError(PyPlugsException):
    """PyPlugs could not locate the given function within a plugin"""
