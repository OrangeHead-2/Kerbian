"""
KerbianCore Monitoring:
- Metrics: counters, gauges, histograms, timers
- Health checks
- Uptime, heartbeats, event hooks
"""

import time
import threading
from collections import defaultdict

class Counter:
    def __init__(self, name):
        self.name = name
        self.value = 0
        self.lock = threading.Lock()
    def inc(self, n=1):
        with self.lock:
            self.value += n
    def get(self):
        return self.value

class Gauge:
    def __init__(self, name):
        self.name = name
        self.value = 0
        self.lock = threading.Lock()
    def set(self, v):
        with self.lock:
            self.value = v
    def inc(self, n=1):
        with self.lock:
            self.value += n
    def dec(self, n=1):
        with self.lock:
            self.value -= n
    def get(self):
        return self.value

class Histogram:
    def __init__(self, name, buckets=None):
        self.name = name
        self.buckets = buckets or [0.1, 0.5, 1, 2, 5, 10, float('inf')]
        self.counts = [0] * len(self.buckets)
        self.lock = threading.Lock()
    def observe(self, v):
        with self.lock:
            for i, b in enumerate(self.buckets):
                if v <= b:
                    self.counts[i] += 1
                    break
    def get(self):
        return list(zip(self.buckets, self.counts))

class Timer:
    def __init__(self, name):
        self.name = name
        self.times = []
        self.lock = threading.Lock()
    def time(self, fn, *a, **kw):
        start = time.time()
        try:
            return fn(*a, **kw)
        finally:
            dur = time.time() - start
            with self.lock:
                self.times.append(dur)
    def observe(self, seconds):
        with self.lock:
            self.times.append(seconds)
    def average(self):
        with self.lock:
            return sum(self.times) / len(self.times) if self.times else 0

class HealthCheck:
    """Pluggable health check."""
    registry = {}
    def __init__(self, name, fn):
        self.name = name
        self.fn = fn
        HealthCheck.registry[name] = self
    def run(self):
        try:
            return self.fn()
        except Exception as e:
            return False, str(e)
    @classmethod
    def run_all(cls):
        return {name: hc.run() for name, hc in cls.registry.items()}

class Uptime:
    start = time.time()
    @classmethod
    def seconds(cls): return time.time() - cls.start

class Heartbeat:
    def __init__(self, interval, fn):
        self.interval = interval
        self.fn = fn
        self._stop = threading.Event()
        self._thread = threading.Thread(target=self._run, daemon=True)
    def start(self):
        self._thread.start()
    def stop(self):
        self._stop.set()
    def _run(self):
        while not self._stop.is_set():
            time.sleep(self.interval)
            self.fn()

# Usage: register metrics, create health checks, fire heartbeats