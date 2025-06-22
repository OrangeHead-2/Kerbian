"""
Example: Metrics and health checks with KerbianCore
"""

from kerbiancore.monitoring.monitor import Counter, Gauge, Histogram, Timer, HealthCheck

# Metrics
requests = Counter("requests_served")
requests.inc(3)

memory = Gauge("memory_used_mb")
memory.set(512)

latency = Histogram("request_latency", buckets=[0.1, 0.5, 1, 2])
latency.observe(0.7)

timer = Timer("work_timer")
import time
def work():
    time.sleep(0.2)
timer.time(work)

# Health check
HealthCheck("memory", lambda: (memory.get() < 1024, f"Memory OK: {memory.get()}MB"))

print("Metrics example completed.")
print("Counter:", requests.get())
print("Gauge:", memory.get())
print("Histogram:", latency.get())
print("Timer average:", timer.average())
print("Health checks:", HealthCheck.run_all())