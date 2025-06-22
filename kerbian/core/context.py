from typing import Any

class Context:
    def __init__(self, default_value: Any = None):
        self.default_value = default_value
        self._value = default_value

    def set(self, value: Any):
        self._value = value

    def get(self):
        return self._value