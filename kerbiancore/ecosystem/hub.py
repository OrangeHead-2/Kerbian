class KerbianHub:
    """
    A simple registry for community plugins/components in memory.
    """
    def __init__(self):
        self.plugins = {}

    def add_plugin(self, name, plugin):
        self.plugins[name] = plugin

    def get_plugin(self, name):
        return self.plugins.get(name)

    def remove_plugin(self, name):
        if name in self.plugins:
            del self.plugins[name]

    def list_plugins(self):
        return list(self.plugins.keys())

    def run_plugin(self, name, *args, **kwargs):
        plugin = self.get_plugin(name)
        if plugin:
            entrypoint = getattr(plugin, "entrypoint", None)
            if not entrypoint and callable(plugin):
                entrypoint = plugin
            if callable(entrypoint):
                return entrypoint(*args, **kwargs)
            raise RuntimeError(f"Plugin {name} has no callable entrypoint.")
        else:
            raise RuntimeError(f"Plugin {name} not found.")