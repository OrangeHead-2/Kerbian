import threading
import time

class BackgroundTaskManager:
    def __init__(self):
        self.tasks = []
        self.threads = []
        self.lock = threading.Lock()
        self.running = True
        self.named_tasks = {}

    def add_task(self, func, interval_sec, initial_delay=0, run_on_start=False, name=None, args=(), kwargs=None):
        if kwargs is None:
            kwargs = {}
        def loop():
            if initial_delay > 0:
                time.sleep(initial_delay)
            if run_on_start:
                try:
                    func(*args, **kwargs)
                except Exception as e:
                    print(f"[Background] Exception in task: {e}")
            while self.running:
                try:
                    func(*args, **kwargs)
                except Exception as e:
                    print(f"[Background] Exception in task: {e}")
                time.sleep(interval_sec)
        thread = threading.Thread(target=loop, daemon=True)
        with self.lock:
            self.tasks.append((func, interval_sec, name))
            self.threads.append(thread)
            if name:
                self.named_tasks[name] = thread
        thread.start()

    def stop_all(self):
        self.running = False
        with self.lock:
            for t in self.threads:
                if t.is_alive():
                    t.join(timeout=0.1)

    def stop_task(self, name):
        with self.lock:
            t = self.named_tasks.get(name)
            if t and t.is_alive():
                # This will not forcibly kill the thread,
                # but you can set a flag in the task closure to exit.
                print(f"[Background] Requesting graceful stop for task: {name}")

    def list_tasks(self):
        with self.lock:
            return [
                {"name": name or getattr(f, "__name__", str(f)), "interval_sec": i}
                for (f, i, name) in self.tasks
            ]