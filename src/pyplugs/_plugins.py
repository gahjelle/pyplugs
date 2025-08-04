"""Decorators for registering plugins."""

# Standard library imports
import contextlib
import functools
import importlib
import sys
import textwrap
from collections.abc import Callable
from importlib import resources
from typing import Any, NamedTuple, ParamSpec, Protocol, TypeVar, overload

# PyPlugs imports
from pyplugs import _exceptions

__all__ = [
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


class PluginInfo(NamedTuple):
    """Information about one plug-in."""

    package_name: str
    plugin_name: str
    func_name: str
    func: Callable[..., Any]
    description: str
    doc: str
    module_doc: str
    sort_value: int
    label: str | None


# Type aliases
P = ParamSpec("P")
T = TypeVar("T")


class InfoFactoryInterface(Protocol):
    """Protocol for defining the callable interface of get_factory()."""

    def __call__(self, plugin: str, func: str | None = None) -> PluginInfo:
        """Specify that func is optional."""
        ...  # pragma: nocover


class GetFactoryInterface(Protocol):
    """Protocol for defining the callable interface of get_factory()."""

    def __call__(self, plugin: str, func: str | None = None) -> Callable[..., Any]:
        """Specify that func is optional."""
        ...  # pragma: nocover


# Dictionary with information about all registered plug-ins
_PLUGINS: dict[str, dict[str, dict[str, PluginInfo]]] = {}


@overload
def register(
    *, sort_value: int, label: str | None
) -> Callable[[Callable[P, T]], Callable[P, T]]: ...  # pragma: nocover


@overload
def register(
    *, sort_value: int
) -> Callable[[Callable[P, T]], Callable[P, T]]: ...  # pragma: nocover


@overload
def register(
    *, label: str
) -> Callable[[Callable[P, T]], Callable[P, T]]: ...  # pragma: nocover


@overload
def register(_func: Callable[P, T]) -> Callable[P, T]: ...  # pragma: nocover


def register(
    _func: Callable[P, T] | None = None,
    *,
    sort_value: int = 0,
    label: str | None = None,
) -> Callable[..., T | Callable[P, T]]:
    """Register a new plug-in."""

    def decorator_register(func: Callable[P, T]) -> Callable[P, T]:
        """Store information about the given function."""
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

    return decorator_register(_func)


def names(package: str) -> list[str]:
    """List all plug-ins in one package."""
    _import_all(package)
    return sorted(_PLUGINS[package].keys(), key=lambda p: info(package, p).sort_value)


def funcs(package: str, plugin: str, label: str | None = None) -> list[str]:
    """List all functions in one plug-in."""
    _import(package, plugin)
    plugin_info = _PLUGINS[package][plugin]
    return [k for k, v in plugin_info.items() if v.label == label]


def labels(package: str, plugin: str) -> set[str]:
    """List all labels in one plug-in."""
    _import(package, plugin)
    plugin_info = _PLUGINS[package][plugin]
    return {p.label for p in plugin_info.values() if p.label is not None}


def info(
    package: str, plugin: str, func: str | None = None, label: str | None = None
) -> PluginInfo:
    """Get information about a plug-in."""
    _import(package, plugin)

    try:
        plugin_info = _PLUGINS[package][plugin]
    except KeyError:
        raise _exceptions.UnknownPluginError(package, plugin) from None

    if func is None:
        func = next(iter([*funcs(package, plugin, label=label), ""]))

    try:
        func_info = plugin_info[func]
    except KeyError:
        raise _exceptions.UnknownPluginFunctionError(package, plugin, func) from None

    if func_info.label != label:
        raise _exceptions.UnknownPluginFunctionError(package, plugin, func, label=label)

    return func_info


def exists(package: str, plugin: str) -> bool:
    """Check if a given plugin exists."""
    if package in _PLUGINS and plugin in _PLUGINS[package]:
        return True

    try:
        _import(package, plugin)
    except (_exceptions.UnknownPluginError, _exceptions.UnknownPackageError):
        return False
    else:
        return package in _PLUGINS and plugin in _PLUGINS[package]


def get(
    package: str, plugin: str, func: str | None = None, label: str | None = None
) -> Callable[..., Any]:
    """Get a given plugin."""
    return info(package, plugin, func=func, label=label).func


def get_typed(
    package: str,
    plugin: str,
    _return_type: T,
    func: str | None = None,
    label: str | None = None,
) -> Callable[..., T]:
    """Get a given plugin. The _return_type help type checkers enforce return types."""
    return get(package, plugin, func=func, label=label)


def call(
    package: str,
    plugin: str,
    func: str | None = None,
    label: str | None = None,
    *args: Any,  # noqa: ANN401
    **kwargs: Any,  # noqa: ANN401
) -> Any:  # noqa: ANN401
    """Call the given plugin."""
    plugin_func = get(package, plugin, func=func, label=label)
    return plugin_func(*args, **kwargs)


def call_typed(
    package: str,
    plugin: str,
    _return_type: T,
    func: str | None = None,
    label: str | None = None,
    *args: Any,  # noqa: ANN401
    **kwargs: Any,  # noqa: ANN401
) -> T:
    """Call the given plugin, expect a given return type."""
    plugin_func = get_typed(
        package, plugin, _return_type=_return_type, func=func, label=label
    )
    return plugin_func(*args, **kwargs)


def _import(package: str, plugin: str) -> None:
    """Import the given plugin file from a package."""
    if package in _PLUGINS and plugin in _PLUGINS[package]:
        return

    plugin_module = f"{package}.{plugin}"
    try:
        importlib.import_module(plugin_module)
    except ImportError as err:
        if repr(plugin_module) in err.msg:
            raise _exceptions.UnknownPluginError(package, plugin) from None
        if repr(package) in err.msg:
            raise _exceptions.UnknownPackageError(package) from None
        raise  # pragma: nocover


def _import_all(package: str) -> None:
    """Import all plugins in a package."""
    try:
        all_resources = [path.name for path in resources.files(package).iterdir()]
    except ImportError as err:
        raise _exceptions.UnknownPackageError(package) from err

    # Note that we have tried to import the package by adding it to _PLUGINS
    _PLUGINS.setdefault(package, {})

    # Loop through all Python files in the directories of the package
    plugins = [
        r[:-3] for r in all_resources if r.endswith(".py") and not r.startswith("_")
    ]
    for plugin in plugins:
        with contextlib.suppress(ImportError):
            # Don't let errors in one plugin, affect the others
            _import(package, plugin)


def names_factory(package: str) -> Callable[[], list[str]]:
    """Create a names() function for one package."""
    return functools.partial(names, package)


def funcs_factory(package: str) -> Callable[[str], list[str]]:
    """Create a funcs() function for one package."""
    return functools.partial(funcs, package)


def labels_factory(package: str) -> Callable[[str], set[str]]:
    """Create a labels() function for one package."""
    return functools.partial(labels, package)


def info_factory(package: str) -> InfoFactoryInterface:
    """Create a info() function for one package."""
    return functools.partial(info, package)


def exists_factory(package: str) -> Callable[[str], bool]:
    """Create an exists() function for one package."""
    return functools.partial(exists, package)


def get_factory(package: str) -> GetFactoryInterface:
    """Create a get() function for one package."""
    return functools.partial(get, package)


def call_factory(package: str) -> Callable[..., Any]:
    """Create a call() function for one package."""
    return functools.partial(call, package)
