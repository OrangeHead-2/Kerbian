"""
KerbianCore i18n Catalog

- In-memory and on-disk catalog management
- Hot-reload support, custom backend loading
"""

import json
import threading
from typing import Dict, Optional, Callable

class Catalog:
    def __init__(self, data: Optional[Dict[str, str]] = None, backend_loader: Optional[Callable] = None, filename: Optional[str] = None):
        self.data = data or {}
        self.filename = filename
        self.backend_loader = backend_loader
        self.lock = threading.Lock()

    def get(self, key: str) -> Optional[str]:
        with self.lock:
            return self.data.get(key)

    def set(self, key: str, val: str):
        with self.lock:
            self.data[key] = val

    def load(self):
        if self.backend_loader:
            self.data = self.backend_loader()
        elif self.filename:
            with open(self.filename, "r", encoding="utf-8") as f:
                self.data = json.load(f)

    def save(self):
        if self.filename:
            with open(self.filename, "w", encoding="utf-8") as f:
                json.dump(self.data, f, ensure_ascii=False, indent=2)

    def reload(self):
        self.load()

    @classmethod
    def from_file(cls, filename: str):
        catalog = cls(filename=filename)
        catalog.load()
        return catalog

# Usage:
# cat = Catalog.from_file("en.json")
# cat.get("hello")