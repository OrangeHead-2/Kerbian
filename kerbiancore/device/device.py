import uuid
import time
import platform
import os
import socket

class KerbianDevice:
    def __init__(self):
        self._id = self._get_device_id()
        self._os = platform.system()
        self._model = self._get_model()
        self._version = self._get_version()
        self._hostname = socket.gethostname()
        self._boot_time = time.time()

    def _get_device_id(self):
        path = os.path.expanduser("~/.kerbian_device_id")
        if os.path.exists(path):
            with open(path, "r") as f:
                return f.read().strip()
        uid = str(uuid.uuid4())
        try:
            with open(path, "w") as f:
                f.write(uid)
        except Exception:
            pass
        return uid

    def _get_model(self):
        return platform.machine() or "unknown"

    def _get_version(self):
        return platform.version() or "unknown"

    def device_id(self):
        return self._id

    def os(self):
        return self._os

    def model(self):
        return self._model

    def version(self):
        return self._version

    def current_time(self):
        return int(time.time())

    def hostname(self):
        return self._hostname

    def boot_time(self):
        return self._boot_time

    def uptime(self):
        return int(time.time() - self._boot_time)

    def info(self):
        return {
            "device_id": self._id,
            "os": self._os,
            "model": self._model,
            "version": self._version,
            "hostname": self._hostname,
            "boot_time": self._boot_time,
            "uptime_sec": self.uptime(),
            "current_time": self.current_time()
        }