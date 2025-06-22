import sys
import traceback

class KerbianErrorReporter:
    def __init__(self, logger):
        self.logger = logger

    def report(self, error_type, message, context=None, exc_info=None):
        tb = None
        if exc_info is not None:
            tb = ''.join(traceback.format_exception(*exc_info))
        elif sys.exc_info()[0]:
            tb = ''.join(traceback.format_exception(*sys.exc_info()))
        else:
            tb = None

        error_entry = {
            "type": error_type,
            "message": message,
            "traceback": tb,
            "context": context or {}
        }
        self.logger.error(f"{error_type}: {message}", {**(context or {}), "traceback": tb})
        if getattr(self.logger, "monitoring_client", None):
            try:
                self.logger.monitoring_client.send_error(error_entry)
            except Exception as e:
                print(f"[KerbianErrorReporter] Monitoring send failed: {e}", file=sys.stderr)
        return error_entry