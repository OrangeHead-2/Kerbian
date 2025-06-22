# KerbianCore Ecosystem Example Usage

## Registering a Plugin (Registry)

```python
from kerbiancore.ecosystem.registry import PluginRegistry

reg = PluginRegistry()
reg.register(
    name="my_plugin",
    url="https://github.com/youruser/yourrepo/raw/main/my_plugin.py",
    description="A simple plugin",
    author="you",
    tags=["example"]
)
```

## Installing and Running Plugins (Manager & Hub)

```python
from kerbiancore.ecosystem.manager import EcosystemManager

eco = EcosystemManager()
eco.install_plugin("my_plugin")  # Downloads and loads from registry if available
eco.run_plugin("my_plugin", "argument")
```

## Adding a Runtime Plugin (In-Memory Hub)

```python
def simple_plugin(arg):
    print(f"Simple plugin got: {arg}")

eco.hub.add_plugin("simple_plugin", simple_plugin)
eco.run_plugin("simple_plugin", "test")
```

## Listing All Plugins

```python
print(eco.list_all())
```

---

- Use `kerbiancore/ecosystem/registry.py` for persistent plugin storage.
- Use `kerbiancore/ecosystem/hub.py` for dynamic plugins during runtime or testing.
- Use `kerbiancore/ecosystem/installer.py` for loading plugins from local or remote files.
- Use `kerbiancore/ecosystem/manager.py` for unified, high-level management.

---