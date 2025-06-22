import requests
import importlib.util
import sys
import os
import threading

class LiveCodePush:
    def __init__(self, endpoint, bundle_dir=".kerbian_bundles"):
        self.endpoint = endpoint
        self.bundle_dir = bundle_dir
        os.makedirs(bundle_dir, exist_ok=True)

    def check_for_update(self, current_version):
        r = requests.get(f"{self.endpoint}/latest?version={current_version}", timeout=5)
        if r.status_code == 200 and r.json().get("update_available"):
            bundle_url = r.json()["bundle_url"]
            return bundle_url
        return None

    def download_and_apply(self, bundle_url):
        bundle_path = os.path.join(self.bundle_dir, os.path.basename(bundle_url))
        with requests.get(bundle_url, stream=True) as r:
            r.raise_for_status()
            with open(bundle_path, "wb") as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)
        self._reload_bundle(bundle_path)

    def _reload_bundle(self, bundle_path):
        # Assume bundle_path is a .py file or .zip of .py files
        if bundle_path.endswith(".py"):
            spec = importlib.util.spec_from_file_location("kerbian_live_bundle", bundle_path)
            module = importlib.util.module_from_spec(spec)
            sys.modules["kerbian_live_bundle"] = module
            spec.loader.exec_module(module)
        elif bundle_path.endswith(".zip"):
            import zipimport
            importer = zipimport.zipimporter(bundle_path)
            importer.load_module("kerbian_live_bundle")

    def start_polling(self, current_version, interval=60):
        def poll():
            while True:
                bundle_url = self.check_for_update(current_version)
                if bundle_url:
                    self.download_and_apply(bundle_url)
                import time; time.sleep(interval)
        t = threading.Thread(target=poll, daemon=True)
        t.start()