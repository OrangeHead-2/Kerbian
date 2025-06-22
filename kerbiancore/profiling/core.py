import time
import threading

class ProfileResult:
    def __init__(self, name, duration, start_time, end_time, call_count):
        self.name = name
        self.duration = duration
        self.start_time = start_time
        self.end_time = end_time
        self.call_count = call_count

    def as_dict(self):
        return {
            "name": self.name,
            "duration": self.duration,
            "start_time": self.start_time,
            "end_time": self.end_time,
            "call_count": self.call_count
        }

class Profiler:
    def __init__(self):
        self.data = {}
        self.lock = threading.Lock()

    def profile(self, name):
        def decorator(func):
            def wrapper(*args, **kwargs):
                start = time.time()
                result = func(*args, **kwargs)
                end = time.time()
                duration = end - start
                with self.lock:
                    entry = self.data.setdefault(name, {"total_time": 0, "call_count": 0, "start": start, "end": end})
                    entry["total_time"] += duration
                    entry["call_count"] += 1
                    entry["end"] = end
                return result
            return wrapper
        return decorator

    def start_section(self, name):
        t = time.time()
        with self.lock:
            entry = self.data.setdefault(name, {"total_time": 0, "call_count": 0, "start": t, "end": t})
            entry["__section_start"] = t

    def end_section(self, name):
        t = time.time()
        with self.lock:
            entry = self.data.get(name)
            if entry and "__section_start" in entry:
                duration = t - entry["__section_start"]
                entry["total_time"] += duration
                entry["call_count"] += 1
                entry["end"] = t
                del entry["__section_start"]

    def results(self):
        with self.lock:
            return [
                ProfileResult(
                    name=k,
                    duration=v["total_time"],
                    start_time=v["start"],
                    end_time=v["end"],
                    call_count=v["call_count"]
                )
                for k, v in self.data.items()
            ]

    def print_report(self):
        for res in self.results():
            print(f"{res.name}: {res.duration:.4f}s ({res.call_count} calls)")