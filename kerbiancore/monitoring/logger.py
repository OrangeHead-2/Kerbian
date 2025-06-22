"""
KerbianCore Logger:
- Hierarchical loggers
- Multiple levels
- Structured/color logs
- Async/buffered, multiple sinks
- Context/trace injection
"""

import sys
import time
import threading
import queue
from datetime import datetime

LOG_LEVELS = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
LOG_COLORS = {
    "DEBUG": "\033[94m",
    "INFO": "\033[92m",
    "WARNING": "\033[93m",
    "ERROR": "\033[91m",
    "CRITICAL": "\033[95m",
    "END": "\033[0m"
}

class LogRecord:
    def __init__(self, level, msg, name, fields=None, exc_info=None, trace_id=None):
        self.timestamp = datetime.utcnow()
        self.level = level
        self.msg = msg
        self.name = name
        self.fields = fields or {}
        self.exc_info = exc_info
        self.trace_id = trace_id

class LogSink:
    def emit(self, record: LogRecord):
        raise NotImplementedError

class ConsoleSink(LogSink):
    def emit(self, record: LogRecord):
        color = LOG_COLORS.get(record.level, "")
        end = LOG_COLORS["END"]
        fields = (" ".join(f"{k}={v}" for k, v in record.fields.items()) if record.fields else "")
        trace = f"[trace={record.trace_id}]" if record.trace_id else ""
        print(f"{color}{record.timestamp:%Y-%m-%d %H:%M:%S} [{record.level}] {record.name}{trace}: {record.msg} {fields}{end}")
        if record.exc_info:
            import traceback
            traceback.print_exception(*record.exc_info)

class FileSink(LogSink):
    def __init__(self, fname):
        self.fname = fname
        self.lock = threading.Lock()
    def emit(self, record: LogRecord):
        with self.lock, open(self.fname, "a") as f:
            fields = (" ".join(f"{k}={v}" for k, v in record.fields.items()) if record.fields else "")
            trace = f"[trace={record.trace_id}]" if record.trace_id else ""
            print(f"{record.timestamp:%Y-%m-%d %H:%M:%S} [{record.level}] {record.name}{trace}: {record.msg} {fields}", file=f)
            if record.exc_info:
                import traceback
                traceback.print_exception(*record.exc_info, file=f)

class Logger:
    _instances = {}
    _global_config = {
        "level": "DEBUG",
        "sinks": [ConsoleSink()],
        "async": False,
        "context": {},
    }
    _queue = queue.Queue()
    _worker = None

    def __new__(cls, name):
        if name not in cls._instances:
            inst = super().__new__(cls)
            inst.name = name
            inst.level = cls._global_config["level"]
            inst.sinks = list(cls._global_config["sinks"])
            inst.context = dict(cls._global_config["context"])
            cls._instances[name] = inst
        return cls._instances[name]

    @classmethod
    def configure(cls, level=None, sinks=None, async_mode=None, context=None):
        if level: cls._global_config["level"] = level
        if sinks: cls._global_config["sinks"] = sinks
        if async_mode is not None: cls._global_config["async"] = async_mode
        if context: cls._global_config["context"] = context
        for inst in cls._instances.values():
            inst.level = cls._global_config["level"]
            inst.sinks = list(cls._global_config["sinks"])
            inst.context = dict(cls._global_config["context"])
        if cls._global_config["async"] and not cls._worker:
            cls._worker = threading.Thread(target=cls._log_worker, daemon=True)
            cls._worker.start()

    @classmethod
    def _log_worker(cls):
        while True:
            rec, sinks = cls._queue.get()
            for sink in sinks:
                sink.emit(rec)

    def _should_log(self, level):
        return LOG_LEVELS.index(level) >= LOG_LEVELS.index(self.level)

    def _log(self, level, msg, **fields):
        if not self._should_log(level): return
        record = LogRecord(level, msg, self.name, fields={**self.context, **fields}, trace_id=self.context.get("trace_id"))
        sinks = self.sinks
        if self._global_config["async"]:
            Logger._queue.put((record, sinks))
        else:
            for sink in sinks:
                sink.emit(record)

    def debug(self, msg, **fields): self._log("DEBUG", msg, **fields)
    def info(self, msg, **fields): self._log("INFO", msg, **fields)
    def warning(self, msg, **fields): self._log("WARNING", msg, **fields)
    def error(self, msg, **fields): self._log("ERROR", msg, **fields)
    def critical(self, msg, **fields): self._log("CRITICAL", msg, **fields)
    def exception(self, msg, **fields):
        import sys
        exc_info = sys.exc_info()
        self._log("ERROR", msg, exc_info=exc_info, **fields)

    def add_sink(self, sink): self.sinks.append(sink)
    def set_level(self, level): self.level = level
    def set_context(self, **ctx): self.context.update(ctx)

# Dynamic config from env or file could be added here (not shown)