import threading
import hashlib
import os
import json
import time

class CodePushServer:
    """
    Production-level code push server with bundle versioning, metadata, rollback, and notification hooks.
    """
    def __init__(self, storage_dir):
        self.storage_dir = storage_dir
        self.lock = threading.Lock()
        os.makedirs(self.storage_dir, exist_ok=True)
        self.meta_file = os.path.join(self.storage_dir, "bundles.json")
        if not os.path.exists(self.meta_file):
            with open(self.meta_file, "w") as f:
                json.dump({}, f)
        self.hooks = {"on_upload": [], "on_rollback": []}

    def _load_metadata(self):
        with self.lock:
            with open(self.meta_file, "r") as f:
                return json.load(f)

    def _save_metadata(self, meta):
        with self.lock:
            with open(self.meta_file, "w") as f:
                json.dump(meta, f, indent=2)

    def upload_bundle(self, bundle_name, bundle_bytes, metadata=None):
        bundle_hash = hashlib.sha256(bundle_bytes).hexdigest()
        bundle_path = os.path.join(self.storage_dir, bundle_hash + ".bundle")
        with self.lock, open(bundle_path, "wb") as f:
            f.write(bundle_bytes)
        meta = self._load_metadata()
        meta.setdefault(bundle_name, [])
        entry = {
            "hash": bundle_hash,
            "filename": bundle_hash + ".bundle",
            "uploaded": time.time(),
            "metadata": metadata or {},
            "active": True
        }
        # Mark previous as inactive
        for e in meta[bundle_name]:
            e["active"] = False
        meta[bundle_name].append(entry)
        self._save_metadata(meta)
        for cb in self.hooks["on_upload"]:
            try:
                cb(bundle_name, entry)
            except Exception as e:
                print(f"[CodePushServer] Upload hook failed: {e}")
        return bundle_hash

    def get_bundle(self, bundle_name):
        meta = self._load_metadata()
        entries = meta.get(bundle_name, [])
        for entry in reversed(entries):
            if entry.get("active"):
                bundle_path = os.path.join(self.storage_dir, entry["filename"])
                if os.path.isfile(bundle_path):
                    with open(bundle_path, "rb") as f:
                        return f.read()
        return None

    def get_metadata(self, bundle_name, include_all=False):
        meta = self._load_metadata()
        entries = meta.get(bundle_name, [])
        if include_all:
            return entries
        for entry in reversed(entries):
            if entry.get("active"):
                return entry
        return {}

    def list_bundles(self):
        meta = self._load_metadata()
        return list(meta.keys())

    def rollback(self, bundle_name, to_hash):
        meta = self._load_metadata()
        entries = meta.get(bundle_name, [])
        found = False
        for entry in entries:
            entry["active"] = (entry["hash"] == to_hash)
            if entry["active"]:
                found = True
        self._save_metadata(meta)
        if found:
            for cb in self.hooks["on_rollback"]:
                try:
                    cb(bundle_name, to_hash)
                except Exception as e:
                    print(f"[CodePushServer] Rollback hook failed: {e}")
        return found

    def register_hook(self, event, callback):
        if event in self.hooks:
            self.hooks[event].append(callback)

class CodePushClient:
    def __init__(self, server, current_bundle):
        self.server = server
        self.current_bundle = current_bundle

    def check_for_update(self):
        available = self.server.list_bundles()
        if self.current_bundle not in available:
            return None
        my_meta = self.server.get_metadata(self.current_bundle)
        all_meta = self.server.get_metadata(self.current_bundle, include_all=True)
        latest = max(all_meta, key=lambda e: e.get("uploaded", 0))
        if not my_meta or my_meta["hash"] != latest["hash"]:
            return latest
        return None

    def download_update(self, bundle_name):
        return self.server.get_bundle(bundle_name)