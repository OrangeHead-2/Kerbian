"""
KerbianCore Device: Background Tasks

- Background task scheduler
- Constraints (network, battery, idle)
- Job queue, retries, periodic/deferred tasks
"""

import threading
import time
from typing import Callable, Dict, Any, Optional, List

class BackgroundTask:
    def __init__(self, fn: Callable, interval: Optional[int] = None, constraints: Optional[Dict] = None, retries=0, defer_to_idle=False):
        self.fn = fn
        self.interval = interval  # seconds, None = run once
        self.constraints = constraints or {}
        self.retries = retries
        self.defer_to_idle = defer_to_idle
        self.running = False

    def run(self):
        try:
            if self._check_constraints():
                self.fn()
                return True
        except Exception:
            if self.retries > 0:
                self.retries -= 1
                return False
        return False

    def _check_constraints(self):
        """
        Check runtime constraints (network, battery, idle, etc.).
        Must be implemented per platform.
        """
        # For production: integrate with OS APIs to enforce constraints.
        return True

class BackgroundScheduler:
    def __init__(self):
        self.tasks: List[BackgroundTask] = []
        self.lock = threading.Lock()
        self._stop = False

    def add_task(self, task: BackgroundTask):
        with self.lock:
            self.tasks.append(task)

    def remove_task(self, task: BackgroundTask):
        with self.lock:
            self.tasks.remove(task)

    def start(self):
        def loop():
            while not self._stop:
                with self.lock:
                    for task in list(self.tasks):
                        if task.interval is not None:
                            if not hasattr(task, "_last_run"):
                                task._last_run = 0
                            now = time.time()
                            if now - task._last_run >= task.interval:
                                task.run()
                                task._last_run = now
                        else:
                            if not hasattr(task, "_ran") or not task._ran:
                                if task.run():
                                    task._ran = True
                time.sleep(1)
        threading.Thread(target=loop, daemon=True).start()

    def stop(self):
        self._stop = True