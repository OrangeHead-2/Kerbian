import importlib.util
import os
import sys

class PluginInstaller:
    """
    Handles installation/loading of local or remote plugin modules.
    For remote plugins: expects a Python file at the given URL.
    For local plugins: expects a .py file path.
    """

    @staticmethod
    def install_local(path, plugin_name=None):
        """Dynamically load a local plugin Python file and return its module."""
        plugin_name = plugin_name or os.path.splitext(os.path.basename(path))[0]
        spec = importlib.util.spec_from_file_location(plugin_name, path)
        if not spec:
            raise ImportError(f"Could not load spec for {path}")
        module = importlib.util.module_from_spec(spec)
        sys.modules[plugin_name] = module
        spec.loader.exec_module(module)
        return module

    @staticmethod
    def install_remote(url, plugin_name):
        """Download a Python file from a URL and load it as a module."""
        import urllib.request
        import tempfile
        with urllib.request.urlopen(url) as response:
            code = response.read()
        with tempfile.NamedTemporaryFile(suffix=".py", delete=False) as tmp:
            tmp.write(code)
            tmp_path = tmp.name
        try:
            mod = PluginInstaller.install_local(tmp_path, plugin_name)
        finally:
            os.remove(tmp_path)
        return mod