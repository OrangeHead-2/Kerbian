# KerbianCore Ecosystem Manager

Unified, high-level interface to find, install, and run plugins from both the
community registry and your in-memory hub.

## Example

```python
from kerbiancore.ecosystem.manager import EcosystemManager

eco = EcosystemManager()

# List everything
print(eco.list_all())

# Install a plugin from the registry (downloaded and loaded)
eco.install_plugin("hello")

# Add a plugin to the hub at runtime
def my_plugin(arg):
    print(f"My plugin: {arg}")

eco.hub.add_plugin("my_plugin", my_plugin)
eco.run_plugin("my_plugin", "Test argument")
```

- Searches hub first, then registry (and auto-installs if needed).
- Registry plugins must provide a raw .py file or entrypoint.

---

- Advanced: You can swap out the registry, hub, or installer if you want to use your own implementations.
- See `kerbiancore/ecosystem/registry.py`, `hub.py`, and `installer.py` for details.

---