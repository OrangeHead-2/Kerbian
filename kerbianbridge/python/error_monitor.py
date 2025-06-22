import requests

class ErrorMonitor:
    def __init__(self, endpoint):
        self.endpoint = endpoint.rstrip('/')

    def report_log(self, log_entry):
        try:
            resp = requests.post(f"{self.endpoint}/log", json=log_entry)
            resp.raise_for_status()
        except Exception as e:
            print(f"Failed to report log: {e}")

    def report_error(self, error_entry):
        try:
            resp = requests.post(f"{self.endpoint}/error", json=error_entry)
            resp.raise_for_status()
        except Exception as e:
            print(f"Failed to report error: {e}")