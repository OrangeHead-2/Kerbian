"""
KerbianCore Monitoring: Additional Log Sinks

- TCPSink: Send logs over TCP
- UDPSink: Send logs over UDP
- HTTPSink: Send logs over HTTP POST
- BufferingSink: Buffer logs for batch/async delivery
- MultiSink: Aggregate multiple sinks as one
"""

import socket
import threading
import json
import requests

class TCPSink:
    def __init__(self, host, port):
        self.addr = (host, port)
        self.lock = threading.Lock()
    def emit(self, record):
        msg = json.dumps(record.__dict__) + "\n"
        with self.lock, socket.create_connection(self.addr) as sock:
            sock.sendall(msg.encode("utf-8"))

class UDPSink:
    def __init__(self, host, port):
        self.addr = (host, port)
    def emit(self, record):
        msg = json.dumps(record.__dict__) + "\n"
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.sendto(msg.encode("utf-8"), self.addr)
        sock.close()

class HTTPSink:
    def __init__(self, url):
        self.url = url
    def emit(self, record):
        try:
            requests.post(self.url, json=record.__dict__, timeout=2)
        except Exception:
            pass  # Optionally queue for retry

class BufferingSink:
    def __init__(self, sink, batch_size=10):
        self.sink = sink
        self.batch = []
        self.lock = threading.Lock()
        self.batch_size = batch_size
    def emit(self, record):
        with self.lock:
            self.batch.append(record)
            if len(self.batch) >= self.batch_size:
                self.flush()
    def flush(self):
        with self.lock:
            for r in self.batch:
                self.sink.emit(r)
            self.batch.clear()

class MultiSink:
    def __init__(self, sinks):
        self.sinks = sinks
    def emit(self, record):
        for s in self.sinks:
            s.emit(record)