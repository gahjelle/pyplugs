"""PyPlugs, decorator based plug-in architecture for Python

See {url} for more information.

Current maintainers:
--------------------

{maintainers}
"""

# Standard library imports
from datetime import date as _date
from collections import namedtuple as _namedtuple

# Include PyPlugs functions at top level
from pyplugs._plugins import *  # noqa
from pyplugs._exceptions import *  # noqa

# Version of PyPlugs.
#
# This is automatically set using the bumpversion tool
__version__ = "0.2.2"


# Homepage for PyPlugs
__url__ = "https://pyplugs.readthedocs.io/"


# Authors/maintainers of Pyplugs
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


__doc__ = _update_doc(__doc__)
