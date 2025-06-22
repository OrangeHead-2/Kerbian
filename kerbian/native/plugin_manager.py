import importlib
import pkgutil

class PluginManager:
    def __init__(self):
        self.plugins = {}

    def load_plugins(self, package):
        for finder, name, ispkg in pkgutil.iter_modules(package.__path__):
            mod = importlib.import_module(f"{package.__name__}.{name}")
            if hasattr(mod, "register"):
                self.plugins[name] = mod.register()

    def get_plugin(self, name):
        return self.plugins.get(name)

plugin_manager = PluginManager()