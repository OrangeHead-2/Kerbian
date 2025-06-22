import os, json

class Config:
    def __init__(self, config_path="kerbian.config.json"):
        if os.path.exists(config_path):
            with open(config_path, "r") as f:
                self.data = json.load(f)
        else:
            self.data = {}

    def get(self, key, default=None):
        return os.environ.get(key) or self.data.get(key, default)