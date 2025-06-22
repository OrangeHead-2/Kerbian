import socket
import json
import threading
import datetime
import time

class Logger:
    def __init__(self):
        self.logs = []

    def log(self, level, message, context=None):
        entry = {
            "timestamp": datetime.datetime.utcnow().isoformat(),
            "level": level,
            "message": message,
            "context": context or {}
        }
        self.logs.append(entry)
        print(f"[{entry['timestamp']}][{level}] {message} {entry['context'] if context else ''}")

    def error(self, message, context=None):
        self.log("ERROR", message, context)

    def info(self, message, context=None):
        self.log("INFO", message, context)

    def warn(self, message, context=None):
        self.log("WARN", message, context)

    def debug(self, message, context=None):
        self.log("DEBUG", message, context)

class NativeModuleRegistry:
    def __init__(self):
        self._modules = {}

    def register(self, name, handler):
        self._modules[name] = handler

    def handle_call(self, msg, bridge_client):
        module_name = msg.get("target")
        method = msg.get("method")
        args = msg.get("args", {})
        handler = self._modules.get(module_name)
        if handler is None:
            bridge_client.logger.error(f"No registered native module: {module_name}")
            if "id" in msg:
                error_msg = {
                    "type": "error",
                    "id": msg["id"],
                    "error_type": "NativeModuleNotFound",
                    "message": f"No such native module: {module_name}",
                    "details": {}
                }
                with bridge_client.lock:
                    bridge_client.sock.sendall((json.dumps(error_msg) + "\n").encode())
            return
        try:
            # Support both dict (for kwargs) and list (for args)
            if isinstance(args, dict):
                response = getattr(handler, method)(**args)
            elif isinstance(args, list):
                response = getattr(handler, method)(*args)
            else:
                response = getattr(handler, method)(args)
            if "id" in msg:
                resp_msg = {
                    "type": "response",
                    "id": msg["id"],
                    "result": response
                }
                with bridge_client.lock:
                    bridge_client.sock.sendall((json.dumps(resp_msg) + "\n").encode())
        except Exception as e:
            bridge_client.logger.error(f"Error in native module {module_name}.{method}", {"exception": str(e)})
            if "id" in msg:
                error_msg = {
                    "type": "error",
                    "id": msg["id"],
                    "error_type": "NativeModuleError",
                    "message": f"Exception in {module_name}.{method}: {e}",
                    "details": {}
                }
                with bridge_client.lock:
                    bridge_client.sock.sendall((json.dumps(error_msg) + "\n").encode())

class NativeBridgeClient:
    def __init__(self, host="localhost", port=8123):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((host, port))
        self.lock = threading.Lock()
        self._responses = {}
        self._event_handlers = {}
        self.logger = Logger()
        self.module_registry = NativeModuleRegistry()
        self._listening = True
        self._listen_thread = threading.Thread(target=self._listen, daemon=True)
        self._listen_thread.start()

    def _listen(self):
        buf = b""
        while self._listening:
            try:
                chunk = self.sock.recv(4096)
                if not chunk:
                    break
                buf += chunk
                while b"\n" in buf:
                    line, buf = buf.split(b"\n", 1)
                    if not line.strip():
                        continue
                    try:
                        msg = json.loads(line.decode())
                    except Exception as e:
                        self.logger.error("Failed to decode JSON from native bridge", {"exception": str(e)})
                        continue
                    if msg.get("type") == "response" and "id" in msg:
                        self._responses[msg["id"]] = msg["result"]
                    elif msg.get("type") == "event":
                        self._route_event(msg)
                    elif msg.get("type") == "error":
                        self.logger.error(msg.get("message", "Unknown error"), msg.get("details"))
                    elif msg.get("type") == "call":
                        self._handle_native_call(msg)
            except Exception as err:
                self.logger.error("Exception in _listen loop", {"exception": str(err)})

    def call(self, target, method, args):
        call_id = id(args) ^ int(datetime.datetime.utcnow().timestamp() * 1000)
        msg = {
            "type": "call",
            "target": target,
            "method": method,
            "args": args,
            "id": call_id
        }
        with self.lock:
            self.sock.sendall((json.dumps(msg) + "\n").encode())
        waited = 0
        while True:
            if call_id in self._responses:
                return self._responses.pop(call_id)
            time.sleep(0.01)
            waited += 0.01
            # Optional: timeout after 10 seconds
            if waited > 10.0:
                raise TimeoutError(f"Timeout waiting for response for call_id {call_id}")

    def on_event(self, event, handler):
        self._event_handlers[event] = handler

    def _route_event(self, msg):
        event = msg.get("event")
        handler = self._event_handlers.get(event)
        if handler:
            try:
                handler(msg.get("view_id"), msg.get("data"))
            except Exception as e:
                self.logger.error(f"Error in event handler for {event}", {"exception": str(e)})

    def report_error(self, errtype, message, details=None):
        msg = {
            "type": "error",
            "error_type": errtype,
            "message": message,
            "details": details or {}
        }
        with self.lock:
            self.sock.sendall((json.dumps(msg) + "\n").encode())

    def register_module(self, name, obj):
        self.module_registry.register(name, obj)

    def _handle_native_call(self, msg):
        self.module_registry.handle_call(msg, self)

    def close(self):
        self._listening = False
        try:
            self.sock.close()
        except Exception:
            pass

class Widget:
    def __init__(self, bridge, type_, props):
        self.bridge = bridge
        self.type = type_
        self.props = dict(props) if props else {}
        self.view_id = self.bridge.call("UIManager", "create_view", {"type": self.type, "props": self.props})

    def update(self, new_props):
        self.props.update(new_props)
        self.bridge.call("UIManager", "update_view", {"view_id": self.view_id, "props": self.props})

    def remove(self):
        self.bridge.call("UIManager", "remove_view", {"view_id": self.view_id})