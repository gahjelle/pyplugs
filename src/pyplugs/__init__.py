"""PyPlugs, decorator based plug-in architecture for Python

See {url} for more information.

Current maintainers:
--------------------

{maintainers}
"""

# Standard library imports
from collections import namedtuple as _namedtuple
from datetime import date as _date

# PyPlugs imports
from pyplugs._exceptions import (
    PyPlugsException,
    UnknownPackageError,
    UnknownPluginError,
    UnknownPluginFunctionError,
)
from pyplugs._plugins import (
    PluginInfo,
    call,
    call_factory,
    exists,
    exists_factory,
    funcs,
    funcs_factory,
    get,
    get_factory,
    info,
    info_factory,
    labels,
    labels_factory,
    names,
    names_factory,
    register,
)

__all__ = [
    "PyPlugsException",
    "UnknownPackageError",
    "UnknownPluginError",
    "UnknownPluginFunctionError",
    "PluginInfo",
    "call",
    "call_factory",
    "exists",
    "exists_factory",
    "funcs",
    "funcs_factory",
    "get",
    "get_factory",
    "info",
    "info_factory",
    "labels",
    "labels_factory",
    "names",
    "names_factory",
    "register",
]

# Version of PyPlugs.
#
# This is automatically set using the bumpver tool
__version__ = "0.5.1"


# Homepage for PyPlugs
__url__ = "https://pyplugs.readthedocs.io/"


# Authors/maintainers of PyPlugs
_Author = _namedtuple("_Author", ["name", "email", "start", "end"])
_AUTHORS = [
    _Author("Geir Arne Hjelle", "geirarne@gmail.com", _date(2019, 4, 1), _date.max)
]

__author__ = ", ".join(a.name for a in _AUTHORS if a.start < _date.today() < a.end)
__contact__ = ", ".join(a.email for a in _AUTHORS if a.start < _date.today() < a.end)


# Update doc with info about maintainers
def _update_doc(doc: str) -> str:
    """Add information to doc-string

    Args:
        doc:  The doc-string to update.

    Returns:
        The updated doc-string.
    """
    # Maintainers
    maintainer_list = [
        f"+ {a.name} <{a.email}>" for a in _AUTHORS if a.start < _date.today() < a.end
    ]
    maintainers = "\n".join(maintainer_list)

    # Add to doc-string
    return doc.format(maintainers=maintainers, url=__url__)


__doc__ = _update_doc(__doc__ if __doc__ is not None else "")
