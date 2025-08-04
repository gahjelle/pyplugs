"""Tests for PyPlugs.

Based on the Pytest test runner
"""

# Standard library imports
from pathlib import Path

# Third party imports
import pytest

# PyPlugs imports
import pyplugs


@pytest.fixture
def plugin_package() -> str:
    """Name of the test plugin package."""
    test_plugins = Path(__file__).parent / "plugin_directory"
    relative = test_plugins.relative_to(Path.cwd())

    return ".".join(relative.parts)


#
# Tests
#
def test_package_not_empty(plugin_package: str) -> None:
    """Test that names() finds some plugins in package."""
    plugins = pyplugs.names(plugin_package)
    assert len(plugins) > 0


def test_package_empty() -> None:
    """Test that names() does not find any plugins in the pyplugs-package."""
    lib_plugins = pyplugs.names("pyplugs")
    assert len(lib_plugins) == 0


def test_list_funcs(plugin_package: str) -> None:
    """Test that funcs() finds some plugins in package."""
    plugins = pyplugs.funcs(plugin_package, "plugin_parts")
    assert len(plugins) == 3


def test_list_funcs_without_label(plugin_package: str) -> None:
    """Test that funcs() finds all plugins without a label."""
    plugins = pyplugs.funcs(plugin_package, "plugin_labels")
    assert len(plugins) == 2


def test_list_funcs_with_label(plugin_package: str) -> None:
    """Test that funcs() can filter plugins with a label."""
    plugins = pyplugs.funcs(plugin_package, "plugin_labels", label="label")
    assert len(plugins) == 2


def test_list_labels(plugin_package: str) -> None:
    """Test that labels() can list all labels in a package."""
    labels = pyplugs.labels(plugin_package, "plugin_labels")
    assert labels == {"label", "another_label"}


def test_list_labels_empty(plugin_package: str) -> None:
    """Test that labels() correctly list no labels for unlabeled plugins."""
    labels = pyplugs.labels(plugin_package, "plugin_parts")
    assert labels == set()


def test_package_non_existing() -> None:
    """Test that a non-existent package raises an appropriate error."""
    with pytest.raises(pyplugs.UnknownPackageError):
        pyplugs.names("pyplugs.non_existent")


def test_plugin_exists(plugin_package: str) -> None:
    """Test that an existing plugin returns its own plugin name."""
    plugin_name = pyplugs.names(plugin_package)[0]
    assert pyplugs.info(plugin_package, plugin_name).plugin_name == plugin_name


@pytest.mark.parametrize("plugin_name", ["no_plugins", "non_existent"])
def test_plugin_not_exists(plugin_package: str, plugin_name: str) -> None:
    """Test that a non-existing plugin raises UnknownPluginError.

    Tests both for an existing module (no_plugins) and a non-existent module
    (non_existent).
    """
    with pytest.raises(pyplugs.UnknownPluginError):
        pyplugs.info(plugin_package, plugin_name)


def test_info(plugin_package: str) -> None:
    """Test that the info gives information about a plugin."""
    plugin_info = pyplugs.info(plugin_package, "plugin_plain")
    assert isinstance(plugin_info, pyplugs.PluginInfo)
    assert plugin_info.func() == "plain"


def test_info_with_label(plugin_package: str) -> None:
    """Test that the info gives information about a labeled plugin."""
    plugin_info = pyplugs.info(plugin_package, "plugin_labels", label="label")
    assert isinstance(plugin_info, pyplugs.PluginInfo)
    assert plugin_info.func_name == "plugin_first_label"


def test_info_with_wrong_label(plugin_package: str) -> None:
    """Test that info() raises error when label is wrong."""
    with pytest.raises(pyplugs.UnknownPluginFunctionError):
        pyplugs.info(plugin_package, "plugin_labels", label="wrong_label")


def test_info_with_function_with_wrong_label(plugin_package: str) -> None:
    """Test that info() is strict about matching label to function."""
    with pytest.raises(pyplugs.UnknownPluginFunctionError):
        pyplugs.info(plugin_package, "plugin_labels", func="plugin_one", label="label")


def test_info_with_no_plugins(plugin_package: str) -> None:
    """Test that info() raises a proper error when there are no plugins available."""
    with pytest.raises(pyplugs.UnknownPluginError):
        pyplugs.info(plugin_package, "no_plugins")


def test_exists(plugin_package: str) -> None:
    """Test that exists() function correctly identifies existing plugins."""
    assert pyplugs.exists(plugin_package, "plugin_parts") is True
    assert pyplugs.exists(plugin_package, "no_plugins") is False
    assert pyplugs.exists(plugin_package, "non_existent") is False


def test_exists_on_non_existing_package() -> None:
    """Test that exists() correctly returns False for non-existing packages."""
    assert pyplugs.exists("non_existent_package", "plugin_parts") is False
    assert pyplugs.exists("non_existent_package", "non_existent") is False


def test_call_existing_plugin(plugin_package: str) -> None:
    """Test that calling a test-plugin works, and returns a string."""
    plugin_name = pyplugs.names(plugin_package)[0]
    return_value = pyplugs.call(plugin_package, plugin_name)
    assert isinstance(return_value, str)


def test_call_non_existing_plugin() -> None:
    """Test that calling a non-existing plugin raises an error."""
    with pytest.raises(pyplugs.UnknownPluginError):
        pyplugs.call("pyplugs", "non_existent")


def test_call_with_label(plugin_package: str) -> None:
    """Test that labels are accounted for when calling plugins."""
    assert pyplugs.call(plugin_package, "plugin_labels", label="label") == "first"


def test_ordered_plugin(plugin_package: str) -> None:
    """Test that order of plugins can be customized."""
    plugin_names = pyplugs.names(plugin_package)
    assert plugin_names[0] == "plugin_first"
    assert plugin_names[-1] == "plugin_last"


def test_default_part(plugin_package: str) -> None:
    """Test that first registered function in a plugin is called by default."""
    plugin_name = "plugin_parts"
    default = pyplugs.call(plugin_package, plugin_name)
    explicit = pyplugs.call(plugin_package, plugin_name, func="plugin_default")
    assert default == explicit


def test_call_non_existing_func(plugin_package: str) -> None:
    """Test that calling a non-existing plug-in function raises an error."""
    plugin_name = "plugin_parts"
    func_name = "non_existent"
    with pytest.raises(pyplugs.UnknownPluginFunctionError):
        pyplugs.call(plugin_package, plugin_name, func=func_name)


def test_short_doc(plugin_package: str) -> None:
    """Test that we can retrieve the short docstring from a plugin."""
    plugin_name = "plugin_plain"
    doc = pyplugs.info(plugin_package, plugin_name).description
    assert doc == "Register a plain plugin."


def test_long_doc(plugin_package: str) -> None:
    """Test that we can retrieve the long docstring from a plugin."""
    plugin_name = "plugin_plain"
    doc = pyplugs.info(plugin_package, plugin_name).doc
    assert doc == "This is the plain docstring."


def test_names_factory(plugin_package: str) -> None:
    """Test that the names factory can retrieve names in package."""
    names = pyplugs.names_factory(plugin_package)
    factory_names = names()
    pyplugs_names = pyplugs.names(plugin_package)
    assert factory_names == pyplugs_names


def test_funcs_factory(plugin_package: str) -> None:
    """Test that the funcs factory can retrieve funcs within plugin."""
    plugin_name = "plugin_parts"
    funcs = pyplugs.funcs_factory(plugin_package)
    factory_funcs = funcs(plugin_name)
    pyplugs_funcs = pyplugs.funcs(plugin_package, plugin_name)
    assert factory_funcs == pyplugs_funcs


def test_labels_factory(plugin_package: str) -> None:
    """Test that the labels factory can retrieve labels within plugin."""
    plugin_name = "plugin_labels"
    labels = pyplugs.labels_factory(plugin_package)
    factory_labels = labels(plugin_name)
    pyplugs_labels = pyplugs.labels(plugin_package, plugin_name)
    assert factory_labels == pyplugs_labels


def test_info_factory(plugin_package: str) -> None:
    """Test that the info factory can retrieve info in package."""
    plugin_name = "plugin_parts"
    info = pyplugs.info_factory(plugin_package)
    factory_info = info(plugin_name)
    pyplugs_info = pyplugs.info(plugin_package, plugin=plugin_name)
    assert factory_info == pyplugs_info


def test_exists_factory(plugin_package: str) -> None:
    """Test that the exists factory can check for plugins in a package."""
    exists = pyplugs.exists_factory(plugin_package)
    assert exists("plugin_parts") is True
    assert exists("no_plugins") is False
    assert exists("non_existent") is False


def test_get_factory(plugin_package: str) -> None:
    """Test that the get factory can retrieve get in package."""
    plugin_name = "plugin_parts"
    get = pyplugs.get_factory(plugin_package)
    factory_get = get(plugin_name)
    pyplugs_get = pyplugs.get(plugin_package, plugin=plugin_name)
    assert factory_get == pyplugs_get


def test_call_factory(plugin_package: str) -> None:
    """Test that the call factory can retrieve call in package."""
    plugin_name = "plugin_parts"
    call = pyplugs.call_factory(plugin_package)
    factory_call = call(plugin_name)
    pyplugs_call = pyplugs.call(plugin_package, plugin=plugin_name)
    assert factory_call == pyplugs_call


def test_typed(plugin_package: str) -> None:
    """Test that typed functions can be called."""
    type_checker_test_get_typed(plugin_package)
    type_checker_test_call_typed(plugin_package)
    type_checker_test_call_typed_with_complex_type(plugin_package)


def type_checker_test_get_typed(plugin_package: str) -> str:
    """Test that get_typed can be called. Return a value to type check.

    This function is not called by pytest, but checked by the type checker.
    """
    plugin_name = "plugin_types"
    func = pyplugs.get_typed(
        plugin_package, plugin_name, func="plugin_string", _return_type=str()
    )
    return func()


def type_checker_test_call_typed(plugin_package: str) -> str:
    """Test that call_typed can be called. Return a value to type check.

    This function is not called by pytest, but checked by the type checker.
    """
    plugin_name = "plugin_types"
    value = pyplugs.call_typed(
        plugin_package, plugin_name, func="plugin_string", _return_type=str()
    )
    assert isinstance(value, str)
    return value


def type_checker_test_call_typed_with_complex_type(
    plugin_package: str,
) -> tuple[str, int]:
    """Test that call_typed can be given a complex return type.

    This function is not called by pytest, but checked by the type checker.
    """
    plugin_name = "plugin_types"
    value = pyplugs.call_typed(
        plugin_package, plugin_name, func="plugin_tuple", _return_type=(str(), int())
    )
    assert isinstance(value, tuple)
    assert isinstance(value[0], str)
    assert isinstance(value[1], int)
    return value
