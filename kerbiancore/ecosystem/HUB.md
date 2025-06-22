# KerbianCore Plugin Hub

A lightweight in-memory "hub" for plugins/components registered at runtime.  
Use this for testing or rapid prototyping before publishing to the formal registry.

## Usage

```python
from kerbiancore.ecosystem.hub import KerbianHub

hub = KerbianHub()

def my_plugin_main(arg):
    print(f"My plugin called with {arg}")

hub.add_plugin("my_plugin", my_plugin_main)
hub.run_plugin("my_plugin", "Hello World")
print(hub.list_plugins())
```

- **add_plugin(name, plugin)**: Register a plugin by name (callable or object with `entrypoint`)
- **get_plugin(name)**: Get the plugin
- **run_plugin(name, ...)**: Run the plugin with args
- **list_plugins()**: List all names

---

- For persistent and sharable plugins, see the registry (`registry.py`)
- For auto-installing plugins from URLs or files, see the installer (`installer.py`)

---