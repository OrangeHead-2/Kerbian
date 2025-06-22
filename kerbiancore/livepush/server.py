"""
LivePush Server

- Secure code bundle storage and versioning
- Patch/delta support (only send diffs)
- Rollback system
- Authentication and permission layers
"""

import os
import hashlib
import json
import threading
from typing import Dict, Optional, List, Tuple
from kerbiancore.livepush.protocol import compute_patch, apply_patch, sign_data, verify_signature

class AuthManager:
    """Simple in-memory user/token permission system."""
    def __init__(self):
        self.tokens = {}  # token -> {"user": ..., "scopes": [...]}
        self.lock = threading.Lock()

    def add_token(self, token: str, user: str, scopes: List[str]):
        with self.lock:
            self.tokens[token] = {"user": user, "scopes": scopes}

    def check(self, token: str, scope: str):
        with self.lock:
            return token in self.tokens and scope in self.tokens[token]["scopes"]

class BundleStore:
    """Stores code bundles and patch history."""
    def __init__(self, storage_dir: str):
        self.dir = storage_dir
        os.makedirs(self.dir, exist_ok=True)
        self.manifest = os.path.join(self.dir, "manifest.json")
        self._load_manifest()

    def _load_manifest(self):
        if os.path.exists(self.manifest):
            with open(self.manifest, "r", encoding="utf-8") as f:
                self.versions = json.load(f)
        else:
            self.versions = []  # List of {"version": ..., "hash": ..., "path": ...}

    def _save_manifest(self):
        with open(self.manifest, "w", encoding="utf-8") as f:
            json.dump(self.versions, f, indent=2)

    def add_bundle(self, bundle_path: str, version: str):
        with open(bundle_path, "rb") as f:
            data = f.read()
            h = hashlib.sha256(data).hexdigest()
        out_path = os.path.join(self.dir, f"bundle_{version}.tar.gz")
        os.rename(bundle_path, out_path)
        self.versions.append({"version": version, "hash": h, "path": out_path})
        self._save_manifest()

    def get_latest(self):
        return self.versions[-1] if self.versions else None

    def get_bundle(self, version: str):
        for b in self.versions:
            if b["version"] == version:
                return b
        return None

    def rollback(self, target_version: str):
        idx = next((i for i, b in enumerate(self.versions) if b["version"] == target_version), None)
        if idx is not None:
            self.versions = self.versions[:idx+1]
            self._save_manifest()
            return True
        return False

    def get_patch(self, from_version: str, to_version: str) -> Optional[bytes]:
        from_bundle = self.get_bundle(from_version)
        to_bundle = self.get_bundle(to_version)
        if not from_bundle or not to_bundle:
            return None
        with open(from_bundle["path"], "rb") as f0, open(to_bundle["path"], "rb") as f1:
            return compute_patch(f0.read(), f1.read())

class LivePushServer:
    def __init__(self, storage_dir: str, secret_key: bytes):
        self.auth = AuthManager()
        self.bundles = BundleStore(storage_dir)
        self.secret_key = secret_key

    def upload_bundle(self, token: str, bundle_path: str, version: str):
        if not self.auth.check(token, "upload"):
            raise PermissionError("Not allowed")
        self.bundles.add_bundle(bundle_path, version)

    def get_patch(self, token: str, from_version: str, to_version: str):
        if not self.auth.check(token, "download"):
            raise PermissionError("Not allowed")
        patch = self.bundles.get_patch(from_version, to_version)
        sig = sign_data(patch, self.secret_key)
        return patch, sig

    def rollback(self, token: str, target_version: str):
        if not self.auth.check(token, "admin"):
            raise PermissionError("Not allowed")
        return self.bundles.rollback(target_version)

    def get_latest_version(self):
        return self.bundles.get_latest()

# Simple REST or gRPC server wrapper could be added for actual network service.