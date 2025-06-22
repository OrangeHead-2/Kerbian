"""
KerbianCore Monitoring Core:
- Unified error/exception base classes
- Global error handler
- Exception context managers and decorators
"""

import sys
import threading
import traceback

class KerbianError(Exception):
    """Base for all KerbianCore errors."""
    pass

class ValidationError(KerbianError):
    """For validation-related failures."""
    pass

class MonitoringError(KerbianError):
    """For monitoring/logging/metrics issues."""
    pass

class ErrorContext:
    """Context manager for capturing and logging exceptions."""
    def __init__(self, logger=None, reraise=True):
        self.logger = logger
        self.reraise = reraise

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        if exc:
            if self.logger:
                self.logger.error("Captured exception", exc_info=(exc_type, exc, tb))
            else:
                print("Captured exception:", exc_type, exc)
                traceback.print_tb(tb)
            return not self.reraise # Suppress if not reraise
        return False

def handle_uncaught(exc_type, exc, tb):
    print("KerbianCore: Uncaught exception:", exc_type.__name__, exc)
    traceback.print_tb(tb)

def install_global_handler():
    """Install as sys.excepthook and threading exception hook."""
    sys.excepthook = handle_uncaught
    if hasattr(threading, "excepthook"):
        threading.excepthook = lambda args: handle_uncaught(args.exc_type, args.exc_value, args.exc_traceback)

def exception_guard(logger=None, reraise=True):
    """Decorator to capture and log exceptions in functions."""
    def decorator(func):
        def wrapper(*a, **kw):
            try:
                return func(*a, **kw)
            except Exception as e:
                if logger:
                    logger.error(f"Exception in {func.__name__}", exc_info=True)
                else:
                    print(f"Exception in {func.__name__}:", e)
                    traceback.print_exc()
                if reraise:
                    raise
        return wrapper
    return decorator

# Optionally install global handler at import
# install_global_handler()