"""Decorators for registering plugins

"""

# Standard library imports
import functools
import importlib
import pathlib
import textwrap
from typing import Callable, Dict
from typing import NamedTuple

# Type aliases
PackageName = str
PluginName = str

# Only expose decorated functions outside
__all__ = []


def expose(func):
    """Add function to __all__ so it will be exposed at the top level"""
    __all__.append(func.__name__)
    return func


class PluginInfo(NamedTuple):
    """Information about one plug-in"""

    name: PluginName
    func: Callable
    description: str
    doc: str
    sort_value: int


# Dictionary with information about all registered plug-ins
_PLUGINS: Dict[PackageName, Dict[PluginName, PluginInfo]] = dict()


@expose
def register(_func: Callable = None, *, sort_value: int = 0) -> Callable:
    """Decorator for registering a new plug-in"""

    def decorator_register(func):
        package_name, _, plugin_name = func.__module__.rpartition(".")
        description, _, doc = (func.__doc__ or "").partition("\n\n")

        pkg_info = _PLUGINS.setdefault(package_name, dict())
        pkg_info[plugin_name] = PluginInfo(
            name=plugin_name,
            func=func,
            description=description,
            doc=textwrap.dedent(doc),
            sort_value=sort_value,
        )

    if _func is None:
        return decorator_register
    else:
        return decorator_register(_func)


@expose
def names(package):
    """List all plugins in one package"""
    _import_all(package)
    return sorted(_PLUGINS[package])


@expose
def info(package, plugin):
    """Get information about a plug-in"""
    _import(package, plugin)
    return _PLUGINS[package][plugin]


@expose
def get(package, plugin):
    """Get a given plugin"""
    return info(package, plugin).func


@expose
def call(package, plugin, *args, **kwargs):
    """Call the given plugin"""
    plugin_func = get(package, plugin)
    return plugin_func(*args, **kwargs)


def _import(package, plugin):
    """Import the given plugin file from a package"""
    importlib.import_module(f"{package}.{plugin}")


def _import_all(package):
    """Import all plugins in a package"""
    pkg = importlib.import_module(package)
    pkg_paths = [pathlib.Path(p) for p in pkg.__path__]
    for pkg_path in pkg_paths:
        for path in pkg_path.iterdir():
            plugin = path.stem
            if not plugin.startswith("_"):
                _import(package, plugin)


@expose
def names_factory(package):
    """Create a names() function for one package"""
    return functools.partial(names, package)


@expose
def get_factory(package):
    """Create a get() function for one package"""
    return functools.partial(get, package)


@expose
def call_factory(package):
    """Create a call() function for one package"""
    return functools.partial(call, package)
