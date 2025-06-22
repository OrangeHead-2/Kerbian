"""
LivePush Monitoring

- Usage tracking, error collection, analytics for update success/failure
"""

import threading
from typing import Dict, List
import time

class Monitor:
    def __init__(self):
        self.lock = threading.Lock()
        self.stats = {
            "update_success": 0,
            "update_failure": 0,
            "rollbacks": 0,
            "clients": set(),
            "errors": []
        }
        self.events: List[Dict] = []

    def record_update(self, client_id: str, success: bool):
        with self.lock:
            self.stats["clients"].add(client_id)
            if success:
                self.stats["update_success"] += 1
            else:
                self.stats["update_failure"] += 1
            self.events.append({"type": "update", "client": client_id, "success": success, "ts": time.time()})

    def record_rollback(self, client_id: str):
        with self.lock:
            self.stats["rollbacks"] += 1
            self.events.append({"type": "rollback", "client": client_id, "ts": time.time()})

    def record_error(self, error: str, client_id: str = None):
        with self.lock:
            self.stats["errors"].append(error)
            self.events.append({"type": "error", "client": client_id, "error": error, "ts": time.time()})

    def get_summary(self):
        with self.lock:
            return dict(self.stats, clients=list(self.stats["clients"]))

    def get_events(self, since_ts: float = 0):
        with self.lock:
            return [e for e in self.events if e["ts"] > since_ts]

# The Monitor instance could be shared by server and CLI for analytics.