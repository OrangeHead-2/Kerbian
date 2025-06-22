import http.server
import socketserver
import json
import threading

class KerbianLogStore:
    def __init__(self):
        self.logs = []
        self.errors = []
        self.lock = threading.Lock()
    def add_log(self, entry):
        with self.lock:
            self.logs.append(entry)
    def add_error(self, entry):
        with self.lock:
            self.errors.append(entry)
    def get_logs(self):
        with self.lock:
            return list(self.logs)
    def get_errors(self):
        with self.lock:
            return list(self.errors)

LOG_STORE = KerbianLogStore()

class RequestHandler(http.server.BaseHTTPRequestHandler):
    def _send_json(self, obj, code=200):
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(obj).encode("utf-8"))

    def do_POST(self):
        content_length = int(self.headers.get("Content-Length", 0))
        data = self.rfile.read(content_length)
        try:
            payload = json.loads(data.decode())
        except Exception:
            self._send_json({"error": "invalid json"}, code=400)
            return
        if self.path == "/log":
            LOG_STORE.add_log(payload)
            self._send_json({"status": "ok"})
        elif self.path == "/error":
            LOG_STORE.add_error(payload)
            self._send_json({"status": "ok"})
        else:
            self._send_json({"error": "unknown endpoint"}, code=404)

    def do_GET(self):
        if self.path == "/logs":
            self._send_json(LOG_STORE.get_logs())
        elif self.path == "/errors":
            self._send_json(LOG_STORE.get_errors())
        else:
            self._send_json({"error": "unknown endpoint"}, code=404)

def run_monitoring_server(port=8124):
    server = socketserver.ThreadingTCPServer(("", port), RequestHandler)
    t = threading.Thread(target=server.serve_forever, daemon=True)
    t.start()
    print(f"[KerbianMonitor] Listening on port {port}")
    return server