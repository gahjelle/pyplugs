"""PyPlugs, decorator based plug-in architecture for Python.

See {url} for more information.

Current maintainers:
--------------------

{maintainers}
"""

# Standard library imports
from datetime import date as _date
from datetime import datetime as _datetime
from datetime import timezone as _timezone
from typing import NamedTuple as _NamedTuple

# PyPlugs imports
from pyplugs._exceptions import (
    PyPlugsError,
    UnknownPackageError,
    UnknownPluginError,
    UnknownPluginFunctionError,
)
from pyplugs._plugins import (
    PluginInfo,
    call,
    call_factory,
    call_typed,
    exists,
    exists_factory,
    funcs,
    funcs_factory,
    get,
    get_factory,
    get_typed,
    info,
    info_factory,
    labels,
    labels_factory,
    names,
    names_factory,
    register,
)

__all__ = [
    "PluginInfo",
    "PyPlugsError",
    "UnknownPackageError",
    "UnknownPluginError",
    "UnknownPluginFunctionError",
    "call",
    "call_factory",
    "call_typed",
    "exists",
    "exists_factory",
    "funcs",
    "funcs_factory",
    "get",
    "get_factory",
    "get_typed",
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
__version__ = "0.5.4"


# Homepage for PyPlugs
__url__ = "https://pyplugs.readthedocs.io/"


# Authors/maintainers of PyPlugs
class _Author(_NamedTuple):
    """Representation of Authors."""

    name: str
    email: str
    start: _date
    end: _date


_AUTHORS = [
    _Author("Geir Arne Hjelle", "geirarne@gmail.com", _date(2019, 4, 1), _date.max)
]

_today = _datetime.now(tz=_timezone.utc).date()
__author__ = ", ".join(a.name for a in _AUTHORS if a.start < _today < a.end)
__contact__ = ", ".join(a.email for a in _AUTHORS if a.start < _today < a.end)


# Update doc with info about maintainers
def _update_doc(doc: str) -> str:
    """Add information to doc-string.

    Args:
        doc:  The doc-string to update.

    Returns:
        The updated doc-string.

    """
    # Maintainers
    maintainer_list = [
        f"+ {a.name} <{a.email}>" for a in _AUTHORS if a.start < _today < a.end
    ]
    maintainers = "\n".join(maintainer_list)

    # Add to doc-string
    return doc.format(maintainers=maintainers, url=__url__)


__doc__ = _update_doc(__doc__ if __doc__ is not None else "")
