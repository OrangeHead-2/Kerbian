class EcosystemManager:
    """
    Unified manager for registry, hub, and installer.
    Use this to search, install, and invoke plugins from all sources.
    """
    def __init__(self, registry=None, hub=None, installer=None):
        from kerbiancore.ecosystem.registry import PluginRegistry
        from kerbiancore.ecosystem.hub import KerbianHub
        from kerbiancore.ecosystem.installer import PluginInstaller

        self.registry = registry or PluginRegistry()
        self.hub = hub or KerbianHub()
        self.installer = installer or PluginInstaller()

    def list_all(self, tag=None):
        reg_plugins = self.registry.list_plugins(tag=tag)
        hub_plugins = self.hub.list_plugins()
        return {
            "registry": reg_plugins,
            "hub": hub_plugins
        }

    def install_plugin(self, name, source="registry"):
        """
        Install a plugin by name from registry or hub.
        If from registry, downloads and loads code.
        If from hub, returns the plugin object.
        """
        if source == "registry":
            info = self.registry.get(name)
            if not info:
                raise ValueError(f"Plugin '{name}' not found in registry.")
            url = info["url"]
            module = self.installer.install_remote(url, name)
            # Optionally add to hub for runtime use
            self.hub.add_plugin(name, module)
            return module
        elif source == "hub":
            plugin = self.hub.get_plugin(name)
            if not plugin:
                raise ValueError(f"Plugin '{name}' not found in hub.")
            return plugin
        else:
            raise ValueError("Unknown source for plugin: " + source)

    def run_plugin(self, name, *args, **kwargs):
        """
        Run a plugin by name (searches hub first, then registry & installs if needed).
        """
        # Try hub first
        plugin = self.hub.get_plugin(name)
        if plugin:
            entrypoint = getattr(plugin, "entrypoint", None)
            if not entrypoint and callable(plugin):
                entrypoint = plugin
            if callable(entrypoint):
                return entrypoint(*args, **kwargs)
        # Try registry
        info = self.registry.get(name)
        if info:
            module = self.installer.install_remote(info["url"], name)
            self.hub.add_plugin(name, module)
            entrypoint = getattr(module, "entrypoint", None)
            if not entrypoint and callable(module):
                entrypoint = module
            if callable(entrypoint):
                return entrypoint(*args, **kwargs)
        raise RuntimeError(f"Plugin {name} not found in hub or registry.")