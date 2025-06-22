import threading
import socket
import json

class KerbianMonitoringClient:
    def __init__(self, host="localhost", port=8124):
        self.host = host
        self.port = port
        self.lock = threading.Lock()

    def _send(self, endpoint, entry):
        request_body = json.dumps(entry)
        request = (
            f"POST {endpoint} HTTP/1.1\r\n"
            f"Host: {self.host}\r\n"
            "Content-Type: application/json\r\n"
            f"Content-Length: {len(request_body)}\r\n"
            "Connection: close\r\n"
            "\r\n"
            f"{request_body}"
        )
        with self.lock:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            try:
                sock.connect((self.host, self.port))
                sock.sendall(request.encode("utf-8"))
                sock.settimeout(1.0)
                try:
                    sock.recv(1024)
                except Exception:
                    pass
            except Exception as e:
                print(f"[KerbianMonitoringClient] Could not send to monitor: {e}")
            finally:
                try:
                    sock.close()
                except Exception:
                    pass

    def send_log(self, log_entry):
        self._send("/log", log_entry)

    def send_error(self, error_entry):
        self._send("/error", error_entry)