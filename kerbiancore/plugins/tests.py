"""
Unit tests for kerbiancore.plugins.ecosystem module.
"""

from kerbiancore.plugins.ecosystem import Plugin, PluginManager

def test_plugin_register_and_run():
    def greet(name): return f"Hi {name}"
    plug = Plugin("greeter", "1.0", "Greets", "dev", greet)
    mgr = PluginManager()
    mgr.register(plug)
    assert "greeter" in mgr.list_plugins()
    result = mgr.run("greeter", "Sam")
    assert result == "Hi Sam"

def test_plugin_disable_enable():
    def test_func(): return "X"
    plug = Plugin("x", "1.0", "desc", "dev", test_func)
    mgr = PluginManager()
    mgr.register(plug)
    mgr.disable("x")
    try:
        mgr.run("x")
        assert False, "Should not run a disabled plugin"
    except RuntimeError:
        pass
    mgr.enable("x")
    assert mgr.run("x") == "X"

if __name__ == "__main__":
    test_plugin_register_and_run()
    test_plugin_disable_enable()
    print("Plugins tests passed.")