import threading
import datetime
import sys

class KerbianLogger:
    LEVELS = ("DEBUG", "INFO", "WARN", "ERROR", "CRITICAL")

    def __init__(self, monitoring_client=None):
        self.log_entries = []
        self.lock = threading.Lock()
        self.monitoring_client = monitoring_client

    def log(self, level, message, context=None):
        if level not in self.LEVELS:
            raise ValueError(f"Invalid log level: {level}")
        entry = {
            "timestamp": datetime.datetime.utcnow().isoformat(),
            "level": level,
            "message": str(message),
            "context": context or {}
        }
        with self.lock:
            self.log_entries.append(entry)
        print(f"[{entry['timestamp']}][{level}] {entry['message']} {entry['context']}")
        if self.monitoring_client:
            try:
                self.monitoring_client.send_log(entry)
            except Exception as e:
                print(f"[KerbianLogger] Monitoring send failed: {e}", file=sys.stderr)

    def debug(self, msg, ctx=None):    self.log("DEBUG", msg, ctx)
    def info(self, msg, ctx=None):     self.log("INFO", msg, ctx)
    def warn(self, msg, ctx=None):     self.log("WARN", msg, ctx)
    def error(self, msg, ctx=None):    self.log("ERROR", msg, ctx)
    def critical(self, msg, ctx=None): self.log("CRITICAL", msg, ctx)

    def get_entries(self, level=None):
        with self.lock:
            if level:
                return [e for e in self.log_entries if e["level"] == level]
            return list(self.log_entries)