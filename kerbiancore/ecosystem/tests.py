"""
KerbianCore Ecosystem: Unit Tests for Registry, Hub, Installer, Manager
"""

from kerbiancore.ecosystem.registry import PluginRegistry
from kerbiancore.ecosystem.hub import KerbianHub
from kerbiancore.ecosystem.installer import PluginInstaller
from kerbiancore.ecosystem.manager import EcosystemManager

def test_registry_register_and_list():
    reg = PluginRegistry(registry_file="test_plugins.json")
    reg.register(
        name="test_plugin",
        url="https://example.com/test_plugin.py",
        description="Test plugin for registry.",
        author="tester",
        tags=["test"]
    )
    plugins = reg.list_plugins()
    assert "test_plugin" in plugins
    assert plugins["test_plugin"]["author"] == "tester"
    reg.remove("test_plugin")
    assert "test_plugin" not in reg.list_plugins()
    import os
    os.remove("test_plugins.json")

def test_hub_add_and_run():
    hub = KerbianHub()
    def sample(arg):
        return f"Got {arg}"
    hub.add_plugin("sample", sample)
    assert "sample" in hub.list_plugins()
    assert hub.run_plugin("sample", "OK") == "Got OK"

def test_installer_local(tmp_path):
    # Create a dummy plugin file
    plugin_code = "def entrypoint(arg):\n    return 'Echo: ' + str(arg)\n"
    plugin_file = tmp_path / "dummy_plugin.py"
    plugin_file.write_text(plugin_code)
    mod = PluginInstaller.install_local(str(plugin_file), "dummy_plugin")
    assert hasattr(mod, "entrypoint")
    assert mod.entrypoint("hello") == "Echo: hello"

def test_manager_run_plugin():
    eco = EcosystemManager()
    def plug_func(x): return x * 2
    eco.hub.add_plugin("doubler", plug_func)
    assert eco.run_plugin("doubler", 5) == 10

if __name__ == "__main__":
    test_registry_register_and_list()
    test_hub_add_and_run()
    # The installer test requires pytest tmp_path or similar,
    # so skip it in a standalone run.
    test_manager_run_plugin()
    print("All tests passed.")