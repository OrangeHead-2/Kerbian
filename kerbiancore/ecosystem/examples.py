"""
Example: End-to-end plugin workflow using the KerbianCore ecosystem.
"""

from kerbiancore.ecosystem.registry import PluginRegistry
from kerbiancore.ecosystem.hub import KerbianHub
from kerbiancore.ecosystem.installer import PluginInstaller
from kerbiancore.ecosystem.manager import EcosystemManager

# 1. Register a plugin in the registry (would usually be in a separate process)
registry = PluginRegistry()
registry.register(
    name="echo_plugin",
    url="https://raw.githubusercontent.com/example/kerbiancore-plugins/main/echo_plugin.py",
    description="Echoes back any input.",
    author="community",
    tags=["utility", "echo"]
)

# 2. Use the ecosystem manager to install and run the plugin from the registry
eco = EcosystemManager(registry=registry)

# This would download and dynamically import the plugin, then add it to the hub
try:
    module = eco.install_plugin("echo_plugin")
    print("Plugin installed:", module)
except Exception as e:
    print("Installation failed:", e)

# 3. List all available plugins from registry and hub
print("All plugins:", eco.list_all())

# 4. Add a runtime plugin directly to the hub (local, for testing/prototyping)
def runtime_plugin(name):
    print(f"Runtime plugin received: {name}")

eco.hub.add_plugin("runtime_plugin", runtime_plugin)

# 5. Run both registry and hub plugins
eco.run_plugin("runtime_plugin", "KerbianCore user")

# If the registry plugin defines an entrypoint, it can be called as well:
# eco.run_plugin("echo_plugin", "Hello from registry")