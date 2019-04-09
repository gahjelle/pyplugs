"""Decorators for registering plugins

"""

# Standard library imports
import functools
import importlib
import pathlib
import sys
import textwrap
from typing import Callable, Dict
from typing import NamedTuple

# Type aliases
PackageName = str
PluginName = str
FuncName = str

# Only expose decorated functions to the outside
__all__ = []


def expose(func):
    """Add function to __all__ so it will be exposed at the top level"""
    __all__.append(func.__name__)
    return func


class PluginInfo(NamedTuple):
    """Information about one plug-in"""

    package_name: PackageName
    plugin_name: PluginName
    func_name: FuncName
    func: Callable
    description: str
    doc: str
    module_doc: str
    sort_value: int


# Dictionary with information about all registered plug-ins
_PLUGINS: Dict[PackageName, Dict[PluginName, Dict[FuncName, PluginInfo]]] = dict()


@expose
def register(_func: Callable = None, *, sort_value: int = 0) -> Callable:
    """Decorator for registering a new plug-in"""

    def decorator_register(func):
        package_name, _, plugin_name = func.__module__.rpartition(".")
        description, _, doc = (func.__doc__ or "").partition("\n\n")
        func_name = func.__name__
        module_doc = sys.modules[func.__module__].__doc__

        pkg_info = _PLUGINS.setdefault(package_name, dict())
        plugin_info = pkg_info.setdefault(plugin_name, dict())
        plugin_info[func_name] = PluginInfo(
            package_name=package_name,
            plugin_name=plugin_name,
            func_name=func_name,
            func=func,
            description=description,
            doc=textwrap.dedent(doc),
            module_doc=module_doc,
            sort_value=sort_value,
        )
        return func

    if _func is None:
        return decorator_register
    else:
        return decorator_register(_func)


@expose
def names(package):
    """List all plug-ins in one package"""
    _import_all(package)
    return sorted(_PLUGINS[package].keys())


@expose
def funcs(package, plugin):
    """List all functions in one plug-in"""
    _import(package, plugin)
    plugin_info = _PLUGINS[package][plugin]
    return list(plugin_info.keys())


@expose
def info(package, plugin, func=None):
    """Get information about a plug-in"""
    _import(package, plugin)

    plugin_info = _PLUGINS[package][plugin]
    func = next(iter(plugin_info.keys())) if func is None else func
    return plugin_info[func]


@expose
def get(package, plugin, func=None):
    """Get a given plugin"""
    return info(package, plugin, func).func


@expose
def call(package, plugin, func=None, *args, **kwargs):
    """Call the given plugin"""
    plugin_func = get(package, plugin, func)
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
def funcs_factory(package):
    """Create a funcs() function for one package"""
    return functools.partial(funcs, package)


@expose
def info_factory(package):
    """Create a info() function for one package"""
    return functools.partial(info, package)


@expose
def get_factory(package):
    """Create a get() function for one package"""
    return functools.partial(get, package)


@expose
def call_factory(package):
    """Create a call() function for one package"""
    return functools.partial(call, package)
