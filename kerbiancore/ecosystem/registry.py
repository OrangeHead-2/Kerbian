import json
import os

class PluginRegistry:
    def __init__(self, registry_file="kerbiancore_plugins.json"):
        self.registry_file = registry_file
        self.plugins = {}
        self.load()

    def load(self):
        if os.path.exists(self.registry_file):
            with open(self.registry_file, "r") as f:
                self.plugins = json.load(f)
        else:
            self.plugins = {}

    def save(self):
        with open(self.registry_file, "w") as f:
            json.dump(self.plugins, f, indent=2)

    def register(self, name, url, description="", author="", tags=None):
        self.plugins[name] = {
            "url": url,
            "description": description,
            "author": author,
            "tags": tags or []
        }
        self.save()

    def remove(self, name):
        if name in self.plugins:
            del self.plugins[name]
            self.save()

    def list_plugins(self, tag=None):
        if tag:
            return {k: v for k, v in self.plugins.items() if tag in v.get("tags", [])}
        return dict(self.plugins)

    def get(self, name):
        return self.plugins.get(name)