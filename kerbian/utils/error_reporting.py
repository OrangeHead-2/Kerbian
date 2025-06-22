import requests

def report_error(exc, context=None):
    # Example: POST to error reporting API/Sentry/etc.
    data = {
        "error": str(exc),
        "context": context or {}
    }
    try:
        requests.post("https://errors.mycompany.com/report", json=data, timeout=2)
    except Exception:
        pass