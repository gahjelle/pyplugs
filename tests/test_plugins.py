"""Tests for Pyplugs

Based on the Pytest test runner
"""
# Standard library imports
import pathlib

# Third party imports
import pytest

# Pyplugs imports
import pyplugs


@pytest.fixture
def tmpfile(tmpdir):
    """A temporary file that can be read"""
    file_path = tmpdir.join("test")
    file_path.write("Temporary test file")

    return file_path


@pytest.fixture
def plugin_package():
    """Name of the test plugin package"""
    plugins = pathlib.Path(__file__).parent / "plugin_directory"
    relative = plugins.relative_to(pathlib.Path.cwd())

    return ".".join(relative.parts)


#
# Tests
#
def test_package_not_empty(plugin_package):
    """Test that names() finds some plugins in package"""
    plugins = pyplugs.names(plugin_package)
    assert len(plugins) > 0


def test_package_empty():
    """Test that names() does not find any plugins in the pyplugs-package"""
    lib_plugins = pyplugs.names("pyplugs")
    assert len(lib_plugins) == 0


def test_list_funcs(plugin_package):
    """Test that funcs() finds some plugins in package"""
    plugins = pyplugs.funcs(plugin_package, "plugin_parts")
    assert len(plugins) == 3


def test_package_non_existing():
    """Test that a non-existent package raises an appropriate error"""
    with pytest.raises(pyplugs.UnknownPackageError):
        pyplugs.names("pyplugs.non_existent")


def test_plugin_exists(plugin_package):
    """Test that an existing plugin returns its own plugin name"""
    plugin_name = pyplugs.names(plugin_package)[0]
    assert pyplugs.info(plugin_package, plugin_name).plugin_name == plugin_name


@pytest.mark.parametrize("plugin_name", ["no_plugins", "non_existent"])
def test_plugin_not_exists(plugin_package, plugin_name):
    """Test that a non-existing plugin raises UnknownPluginError

    Tests both for an existing module (no_plugins) and a non-existent module
    (non_existent).
    """
    with pytest.raises(pyplugs.UnknownPluginError):
        pyplugs.info(plugin_package, plugin_name)


def test_exists(plugin_package):
    """Test that exists() function correctly identifies existing plugins"""
    assert pyplugs.exists(plugin_package, "plugin_parts") is True
    assert pyplugs.exists(plugin_package, "no_plugins") is False
    assert pyplugs.exists(plugin_package, "non_existent") is False


def test_call_existing_plugin(plugin_package):
    """Test that calling a test-plugin works, and returns a string"""
    plugin_name = pyplugs.names(plugin_package)[0]
    return_value = pyplugs.call(plugin_package, plugin_name)
    assert isinstance(return_value, str)


def test_call_non_existing_plugin():
    """Test that calling a non-existing plugin raises an error"""
    with pytest.raises(pyplugs.UnknownPluginError):
        pyplugs.call("pyplugs", "non_existent")


def test_ordered_plugin(plugin_package):
    """Test that order of plugins can be customized"""
    plugin_names = pyplugs.names(plugin_package)
    assert plugin_names[0] == "plugin_first"
    assert plugin_names[-1] == "plugin_last"


def test_default_part(plugin_package):
    """Test that first registered function in a plugin is called by default"""
    plugin_name = "plugin_parts"
    default = pyplugs.call(plugin_package, plugin_name)
    explicit = pyplugs.call(plugin_package, plugin_name, func="plugin_default")
    assert default == explicit


def test_call_non_existing_func(plugin_package):
    """Test that calling a non-existing plug-in function raises an error"""
    plugin_name = "plugin_parts"
    func_name = "non_existent"
    with pytest.raises(pyplugs.UnknownPluginFunctionError):
        pyplugs.call(plugin_package, plugin_name, func=func_name)


def test_short_doc(plugin_package):
    """Test that we can retrieve the short docstring from a plugin"""
    plugin_name = "plugin_plain"
    doc = pyplugs.info(plugin_package, plugin_name).description
    assert doc == "A plain plugin"


def test_long_doc(plugin_package):
    """Test that we can retrieve the long docstring from a plugin"""
    plugin_name = "plugin_plain"
    doc = pyplugs.info(plugin_package, plugin_name).doc
    assert doc == "This is the plain docstring."


def test_names_factory(plugin_package):
    """Test that the names factory can retrieve names in package"""
    names = pyplugs.names_factory(plugin_package)
    factory_names = names()
    pyplugs_names = pyplugs.names(plugin_package)
    assert factory_names == pyplugs_names


def test_funcs_factory(plugin_package):
    """Test that the funcs factory can retrieve funcs within plugin"""
    plugin_name = "plugin_parts"
    funcs = pyplugs.funcs_factory(plugin_package)
    factory_funcs = funcs(plugin_name)
    pyplugs_funcs = pyplugs.funcs(plugin_package, plugin_name)
    assert factory_funcs == pyplugs_funcs


def test_info_factory(plugin_package):
    """Test that the info factory can retrieve info in package"""
    plugin_name = "plugin_parts"
    info = pyplugs.info_factory(plugin_package)
    factory_info = info(plugin_name)
    pyplugs_info = pyplugs.info(plugin_package, plugin=plugin_name)
    assert factory_info == pyplugs_info


def test_exists_factory(plugin_package):
    """Test that the exists factory can check for plugins in a package"""
    exists = pyplugs.exists_factory(plugin_package)
    assert exists("plugin_parts") is True
    assert exists("no_plugins") is False
    assert exists("non_existent") is False


def test_get_factory(plugin_package):
    """Test that the get factory can retrieve get in package"""
    plugin_name = "plugin_parts"
    get = pyplugs.get_factory(plugin_package)
    factory_get = get(plugin_name)
    pyplugs_get = pyplugs.get(plugin_package, plugin=plugin_name)
    assert factory_get == pyplugs_get


def test_call_factory(plugin_package):
    """Test that the call factory can retrieve call in package"""
    plugin_name = "plugin_parts"
    call = pyplugs.call_factory(plugin_package)
    factory_call = call(plugin_name)
    pyplugs_call = pyplugs.call(plugin_package, plugin=plugin_name)
    assert factory_call == pyplugs_call
