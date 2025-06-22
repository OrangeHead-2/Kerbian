import threading
import time
import json

class KerbianAnalytics:
    def __init__(self, cache_max=1000, auto_flush_interval=None):
        self.events = []
        self.lock = threading.Lock()
        self.providers = {}
        self.cache_max = cache_max
        self.auto_flush_interval = auto_flush_interval
        if auto_flush_interval:
            self._start_auto_flush()

    def register_provider(self, name, func):
        self.providers[name] = func

    def unregister_provider(self, name):
        self.providers.pop(name, None)

    def track_event(self, event_name, properties=None, user_id=None, timestamp=None, session_id=None, tags=None):
        evt = {
            "event": event_name,
            "properties": properties or {},
            "user_id": user_id,
            "timestamp": timestamp or time.time(),
            "session_id": session_id,
            "tags": tags or []
        }
        with self.lock:
            self.events.append(evt)
            if len(self.events) > self.cache_max:
                self.events.pop(0)
        for name, func in list(self.providers.items()):
            try:
                func(evt)
            except Exception as e:
                print(f"[Analytics] Provider {name} failed: {e}")

    def flush(self):
        with self.lock:
            self.events.clear()

    def get_events(self, limit=None, event_name=None, user_id=None):
        with self.lock:
            results = self.events[-limit:] if limit else list(self.events)
            if event_name:
                results = [e for e in results if e["event"] == event_name]
            if user_id:
                results = [e for e in results if e["user_id"] == user_id]
            return results

    def export_events_json(self):
        with self.lock:
            return json.dumps(self.events, ensure_ascii=False, indent=2)

    def import_events_json(self, json_str):
        data = json.loads(json_str)
        with self.lock:
            self.events.extend(data)
            self.events = self.events[-self.cache_max:]

    def _start_auto_flush(self):
        import threading
        def flush_loop():
            while True:
                time.sleep(self.auto_flush_interval)
                self.flush()
        t = threading.Thread(target=flush_loop, daemon=True)
        t.start()