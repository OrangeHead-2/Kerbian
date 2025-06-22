import os, json
from cryptography.fernet import Fernet

class SecureStorage:
    def __init__(self, key):
        self.key = key
        self.cipher = Fernet(key)

    def set_item(self, k, v):
        enc = self.cipher.encrypt(v.encode())
        with open(self._file(k), 'wb') as f:
            f.write(enc)

    def get_item(self, k):
        try:
            with open(self._file(k), 'rb') as f:
                return self.cipher.decrypt(f.read()).decode()
        except Exception:
            return None

    def _file(self, k):
        return os.path.expanduser(f"~/.kerbian_secure_{k}")