import os
from cryptography.fernet import Fernet

class SecretsManager:
    def __init__(self, secret_file=".kerbian_secret"):
        self.secret_file = secret_file
        if not os.path.exists(secret_file):
            key = Fernet.generate_key()
            with open(secret_file, "wb") as f:
                f.write(key)
        else:
            with open(secret_file, "rb") as f:
                key = f.read()
        self.cipher = Fernet(key)

    def set(self, k, v):
        enc = self.cipher.encrypt(v.encode())
        with open(f"{self.secret_file}.{k}", "wb") as f:
            f.write(enc)

    def get(self, k):
        try:
            with open(f"{self.secret_file}.{k}", "rb") as f:
                return self.cipher.decrypt(f.read()).decode()
        except Exception:
            return None