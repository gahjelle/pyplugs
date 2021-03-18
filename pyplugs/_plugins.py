"""Decorators for registering plugins

"""

# Standard library imports
import functools
import importlib
import sys
import textwrap
from typing import (
    Any,
    Callable,
    Dict,
    List,
    NamedTuple,
    Optional,
    Set,
    TypeVar,
    overload,
)

# PyPlugs imports
from pyplugs import _exceptions

# Use backport of importlib.resources if necessary
try:
    # Standard library imports
    from importlib import resources
except ImportError:  # pragma: nocover
    # Third party imports
    import importlib_resources as resources  # type: ignore


# Type aliases
T = TypeVar("T")
Plugin = Callable[..., Any]


# Only expose decorated functions to the outside
__all__ = []


def expose(func: Callable[..., T]) -> Callable[..., T]:
    """Add function to __all__ so it will be exposed at the top level"""
    __all__.append(func.__name__)
    return func


@expose
class PluginInfo(NamedTuple):
    """Information about one plug-in"""

    package_name: str
    plugin_name: str
    func_name: str
    func: Plugin
    description: str
    doc: str
    module_doc: str
    sort_value: float
    label: Optional[str]


# Dictionary with information about all registered plug-ins
_PLUGINS: Dict[str, Dict[str, Dict[str, PluginInfo]]] = {}


@overload
def register(
    func: None, *, sort_value: float, label: Optional[str]
) -> Callable[[Plugin], Plugin]:
    """Signature for using decorator with parameters"""
    ...  # pragma: nocover


@overload
def register(func: Plugin) -> Plugin:
    """Signature for using decorator without parameters"""
    ...  # pragma: nocover


@expose
def register(
    _func: Optional[Plugin] = None,
    *,
    sort_value: float = 0,
    label: Optional[str] = None,
) -> Callable[..., Any]:
    """Decorator for registering a new plug-in"""

    def decorator_register(func: Callable[..., T]) -> Callable[..., T]:
        """Store information about the given function"""
        package_name, _, plugin_name = func.__module__.rpartition(".")
        description, _, doc = (func.__doc__ or "").partition("\n\n")
        func_name = func.__name__
        module_doc = sys.modules[func.__module__].__doc__ or ""

        pkg_info = _PLUGINS.setdefault(package_name, {})
        plugin_info = pkg_info.setdefault(plugin_name, {})
        plugin_info[func_name] = PluginInfo(
            package_name=package_name,
            plugin_name=plugin_name,
            func_name=func_name,
            func=func,
            description=description,
            doc=textwrap.dedent(doc).strip(),
            module_doc=module_doc,
            sort_value=sort_value,
            label=label,
        )
        return func

    if _func is None:
        return decorator_register
    else:
        return decorator_register(_func)


@expose
def names(package: str) -> List[str]:
    """List all plug-ins in one package"""
    _import_all(package)
    return sorted(_PLUGINS[package].keys(), key=lambda p: info(package, p).sort_value)


@expose
def funcs(package: str, plugin: str, label: Optional[str] = None) -> List[str]:
    """List all functions in one plug-in"""
    _import(package, plugin)
    plugin_info = _PLUGINS[package][plugin]
    return [k for k, v in plugin_info.items() if v.label == label]


@expose
def labels(package: str, plugin: str) -> Set[str]:
    """List all labels in one plug-in"""
    _import(package, plugin)
    plugin_info = _PLUGINS[package][plugin]
    return {p.label for p in plugin_info.values() if p.label is not None}


@expose
def info(
    package: str, plugin: str, func: Optional[str] = None, label: Optional[str] = None
) -> PluginInfo:
    """Get information about a plug-in"""
    _import(package, plugin)

    try:
        plugin_info = _PLUGINS[package][plugin]
    except KeyError:
        raise _exceptions.UnknownPluginError(
            f"Could not find any plug-in named {plugin!r} inside {package!r}. "
            "Use @pyplugs.register to register functions as plug-ins"
        )

    if func is None:
        func = next(iter(funcs(package, plugin, label=label) + [""]))

    try:
        func_info = plugin_info[func]
    except KeyError:
        raise _exceptions.UnknownPluginFunctionError(
            f"Could not find any function named {func!r} inside '{package}.{plugin}'. "
            "Use @pyplugs.register to register plug-in functions"
        )

    if func_info.label != label:
        raise _exceptions.UnknownPluginFunctionError(
            f"Could not find '{package}.{plugin}.{func}' with label '{label}'. "
            "Use @pyplugs.register to register plug-in functions"
        )

    return func_info


@expose
def exists(package: str, plugin: str) -> bool:
    """Check if a given plugin exists"""
    if package in _PLUGINS and plugin in _PLUGINS[package]:
        return True

    try:
        _import(package, plugin)
    except (_exceptions.UnknownPluginError, _exceptions.UnknownPackageError):
        return False
    else:
        return package in _PLUGINS and plugin in _PLUGINS[package]


@expose
def get(
    package: str, plugin: str, func: Optional[str] = None, label: Optional[str] = None
) -> Plugin:
    """Get a given plugin"""
    return info(package, plugin, func=func, label=label).func


@expose
def call(
    package: str,
    plugin: str,
    func: Optional[str] = None,
    label: Optional[str] = None,
    *args: Any,
    **kwargs: Any,
) -> Any:
    """Call the given plugin"""
    plugin_func = get(package, plugin, func=func, label=label)
    return plugin_func(*args, **kwargs)


def _import(package: str, plugin: str) -> None:
    """Import the given plugin file from a package"""
    if package in _PLUGINS and plugin in _PLUGINS[package]:
        return

    plugin_module = f"{package}.{plugin}"
    try:
        importlib.import_module(plugin_module)
    except ImportError as err:
        if repr(plugin_module) in err.msg:  # type: ignore
            raise _exceptions.UnknownPluginError(
                f"Plugin {plugin!r} not found in {package!r}"
            ) from None
        elif repr(package) in err.msg:  # type: ignore
            raise _exceptions.UnknownPackageError(
                f"Package {package!r} does not exist"
            ) from None
        raise


def _import_all(package: str) -> None:
    """Import all plugins in a package"""
    try:
        all_resources = resources.contents(package)  # type: ignore
    except ImportError as err:
        raise _exceptions.UnknownPackageError(err) from None

    # Note that we have tried to import the package by adding it to _PLUGINS
    _PLUGINS.setdefault(package, {})

    # Loop through all Python files in the directories of the package
    plugins = [
        r[:-3] for r in all_resources if r.endswith(".py") and not r.startswith("_")
    ]
    for plugin in plugins:
        try:
            _import(package, plugin)
        except ImportError:
            pass  # Don't let errors in one plugin, affect the others


@expose
def names_factory(package: str) -> Callable[[], List[str]]:
    """Create a names() function for one package"""
    return functools.partial(names, package)


@expose
def funcs_factory(package: str) -> Callable[[str], List[str]]:
    """Create a funcs() function for one package"""
    return functools.partial(funcs, package)


@expose
def labels_factory(package: str) -> Callable[[str], Set[str]]:
    """Create a labels() function for one package"""
    return functools.partial(labels, package)


@expose
def info_factory(package: str) -> Callable[[str, Optional[str]], PluginInfo]:
    """Create a info() function for one package"""
    return functools.partial(info, package)


@expose
def exists_factory(package: str) -> Callable[[str], bool]:
    """Create an exists() function for one package"""
    return functools.partial(exists, package)


@expose
def get_factory(package: str) -> Callable[[str, Optional[str]], Plugin]:
    """Create a get() function for one package"""
    return functools.partial(get, package)


@expose
def call_factory(package: str) -> Callable[..., Any]:
    """Create a call() function for one package"""
    return functools.partial(call, package)
