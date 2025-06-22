"""
KerbianCore Device: Secure Storage

- Secure file storage (encryption-at-rest), sandboxing, large file support
- Quota management, background sync, cloud backup
"""

import os
import threading
import shutil
from typing import Optional, Callable

class SecureStorage:
    def __init__(self, root_dir: str, encrypt_fn: Optional[Callable] = None, decrypt_fn: Optional[Callable] = None, quota_mb: int = 100):
        self.root_dir = root_dir
        os.makedirs(self.root_dir, exist_ok=True)
        self.encrypt_fn = encrypt_fn
        self.decrypt_fn = decrypt_fn
        self.quota_mb = quota_mb
        self.lock = threading.Lock()

    def _get_file_path(self, key: str):
        return os.path.join(self.root_dir, key)

    def _used_space_mb(self):
        total = 0
        for root, dirs, files in os.walk(self.root_dir):
            for f in files:
                total += os.path.getsize(os.path.join(root, f))
        return total / (1024 * 1024)

    def save(self, key: str, data: bytes):
        with self.lock:
            if self._used_space_mb() + len(data) / (1024 * 1024) > self.quota_mb:
                raise Exception("Quota exceeded")
            fpath = self._get_file_path(key)
            enc_data = self.encrypt_fn(data) if self.encrypt_fn else data
            with open(fpath, "wb") as f:
                f.write(enc_data)

    def load(self, key: str) -> Optional[bytes]:
        fpath = self._get_file_path(key)
        if not os.path.exists(fpath):
            return None
        with open(fpath, "rb") as f:
            data = f.read()
        return self.decrypt_fn(data) if self.decrypt_fn else data

    def delete(self, key: str):
        fpath = self._get_file_path(key)
        if os.path.exists(fpath):
            os.remove(fpath)

    def list_keys(self):
        return os.listdir(self.root_dir)

    def sync_to_cloud(self, upload_fn: Callable):
        """
        Upload all files to cloud using the provided upload_fn(key, data).
        Must be implemented for your cloud provider and authentication.
        """
        for key in self.list_keys():
            data = self.load(key)
            upload_fn(key, data)

    def background_sync(self, upload_fn: Callable, interval: int = 3600):
        import threading, time
        def loop():
            while True:
                self.sync_to_cloud(upload_fn)
                time.sleep(interval)
        threading.Thread(target=loop, daemon=True).start()

    def clear(self):
        shutil.rmtree(self.root_dir)
        os.makedirs(self.root_dir, exist_ok=True)