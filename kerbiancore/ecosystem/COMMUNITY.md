# KerbianCore Community Plugins & Registry Guide

KerbianCore supports a registry for public and private plugins.

## Using the Registry

```python
from kerbiancore.ecosystem.registry import PluginRegistry

reg = PluginRegistry()
reg.register(
    name="hello",
    url="https://github.com/yourname/kerbiancore-plugin-hello",
    description="A plugin that says hello",
    author="yourname",
    tags=["hello", "community"]
)
print(reg.list_plugins())
```

## Community Plugin Template

```python
from kerbiancore.ecosystem.community import example_community_greet_plugin

plugin = example_community_greet_plugin()
print(plugin["name"], plugin["description"])
plugin["entrypoint"]("KerbianCore user")
```

---

## Sharing Your Plugin

1. Make your plugin with a standard entrypoint (a callable).
2. Register it in the registry, and publish your repo.
3. Submit your plugin to the KerbianCore community index.
4. (Optional) Tag it with categories for discoverability.

---

- See `kerbiancore/ecosystem/registry.py` for implementation.
- See `kerbiancore/ecosystem/community.py` for templating.

---