class Plugin:
    def __init__(self, name, version, description, author, entrypoint):
        self.name = name
        self.version = version
        self.description = description
        self.author = author
        self.entrypoint = entrypoint
        self.enabled = True

    def run(self, *args, **kwargs):
        if self.enabled and callable(self.entrypoint):
            return self.entrypoint(*args, **kwargs)
        raise RuntimeError("Plugin is disabled or invalid.")

class PluginManager:
    def __init__(self):
        self.plugins = {}

    def register(self, plugin: Plugin):
        self.plugins[plugin.name] = plugin

    def enable(self, name):
        if name in self.plugins:
            self.plugins[name].enabled = True

    def disable(self, name):
        if name in self.plugins:
            self.plugins[name].enabled = False

    def run(self, name, *args, **kwargs):
        if name in self.plugins:
            return self.plugins[name].run(*args, **kwargs)
        raise RuntimeError(f"Plugin {name} not found.")

    def list_plugins(self):
        return [
            {
                "name": p.name,
                "version": p.version,
                "description": p.description,
                "author": p.author,
                "enabled": p.enabled
            }
            for p in self.plugins.values()
        ]