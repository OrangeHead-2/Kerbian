# KerbianCore Plugins Module

Develop, register, and use plugins to extend KerbianCore functionality.

## Features

- Plugin class for defining plugins
- PluginManager for registration, lookup, execution
- Example plugin registry index

## Example

```python
from kerbiancore.plugins.ecosystem import Plugin, PluginManager

def say_hello(name): return f"Hello, {name}!"
plugin = Plugin("hello", "1.0", "Greets", "dev", say_hello)
mgr = PluginManager()
mgr.register(plugin)
print(mgr.run("hello", "World"))
```

---