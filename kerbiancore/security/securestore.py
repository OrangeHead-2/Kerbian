import os
import base64

class SecureStore:
    def __init__(self, store_file):
        self.store_file = store_file
        self.data = {}
        self._load()

    def _load(self):
        if os.path.exists(self.store_file):
            with open(self.store_file, "rb") as f:
                raw = f.read()
                if raw:
                    decoded = base64.b64decode(raw)
                    lines = decoded.decode("utf-8").splitlines()
                    for line in lines:
                        if "=" in line:
                            k, v = line.split("=", 1)
                            self.data[k] = v

    def _save(self):
        lines = [f"{k}={v}" for k, v in self.data.items()]
        encoded = base64.b64encode("\n".join(lines).encode("utf-8"))
        with open(self.store_file, "wb") as f:
            f.write(encoded)

    def set(self, key, value):
        self.data[key] = value
        self._save()

    def get(self, key, default=None):
        return self.data.get(key, default)

    def remove(self, key):
        if key in self.data:
            del self.data[key]
            self._save()

    def list_keys(self):
        return list(self.data.keys())

def audit_secure_store(store: SecureStore):
    issues = []
    if not os.path.exists(store.store_file):
        issues.append("Store file does not exist.")
    else:
        perms = oct(os.stat(store.store_file).st_mode)[-3:]
        if perms not in ("600", "400"):
            issues.append("Store file permissions should be 600 or 400.")
    if len(store.data) == 0:
        issues.append("Store is empty.")
    return issues