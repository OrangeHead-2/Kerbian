"""
LivePush Client

- Secure download, signature verification, patch/apply logic
- Update hooks, rollback, atomic update/swap
- Background update checks, staged rollout, A/B testing
"""

import os
import hashlib
import shutil
from typing import Callable, Optional
from kerbiancore.livepush.protocol import apply_patch, verify_signature

class LivePushClient:
    def __init__(self, server_api, bundle_dir: str, pubkey: bytes):
        self.server = server_api  # Should have get_patch, get_latest_version
        self.bundle_dir = bundle_dir
        self.pubkey = pubkey
        self.current_version = self._detect_current_version()
        self.hooks = {"pre_update": [], "post_update": [], "on_error": []}

    def _detect_current_version(self) -> Optional[str]:
        verfile = os.path.join(self.bundle_dir, "version.txt")
        if os.path.exists(verfile):
            with open(verfile, "r") as f:
                return f.read().strip()
        return None

    def add_hook(self, hook_type: str, fn: Callable):
        if hook_type in self.hooks:
            self.hooks[hook_type].append(fn)

    def run_hooks(self, hook_type: str, *args, **kwargs):
        for fn in self.hooks.get(hook_type, []):
            try:
                fn(*args, **kwargs)
            except Exception as e:
                print(f"Hook error: {e}")

    def update(self, token: str):
        latest = self.server.get_latest_version()
        if not latest or latest["version"] == self.current_version:
            return False  # Up to date
        patch, sig = self.server.get_patch(token, self.current_version, latest["version"])
        if not verify_signature(patch, sig, self.pubkey):
            self.run_hooks("on_error", "Signature verification failed")
            return False
        tmp_file = os.path.join(self.bundle_dir, "bundle.tmp")
        apply_patch(os.path.join(self.bundle_dir, f"bundle_{self.current_version}.tar.gz"), patch, tmp_file)
        self.run_hooks("pre_update", self.current_version, latest["version"])
        # Atomic swap
        final_file = os.path.join(self.bundle_dir, f"bundle_{latest['version']}.tar.gz")
        shutil.move(tmp_file, final_file)
        with open(os.path.join(self.bundle_dir, "version.txt"), "w") as f:
            f.write(latest["version"])
        self.current_version = latest["version"]
        self.run_hooks("post_update", self.current_version)
        return True

    def rollback(self, version: str):
        # Switch back to a previous version atomically
        bundle_file = os.path.join(self.bundle_dir, f"bundle_{version}.tar.gz")
        if not os.path.exists(bundle_file):
            self.run_hooks("on_error", "Rollback version not found")
            return False
        with open(os.path.join(self.bundle_dir, "version.txt"), "w") as f:
            f.write(version)
        self.current_version = version
        return True

    def background_check(self, token: str, interval_sec: int = 60):
        import time, threading
        def loop():
            while True:
                try:
                    self.update(token)
                except Exception as e:
                    self.run_hooks("on_error", str(e))
                time.sleep(interval_sec)
        t = threading.Thread(target=loop, daemon=True)
        t.start()

    # Staged rollout and A/B testing could be added with custom server APIs.

# Example: see README.md for integration.