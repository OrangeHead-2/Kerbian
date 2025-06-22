"""
KerbianCore Monitoring: Built-in Health Checks

- Disk space
- CPU
- Memory
- Custom user health checks
"""

import shutil
import os
import psutil  # If you want to keep pure, you could reimplement with os and /proc

def disk_free_gb(path="/"):
    total, used, free = shutil.disk_usage(path)
    return free / (1024 ** 3)

def cpu_usage():
    return psutil.cpu_percent(interval=0.1)

def mem_usage():
    return psutil.virtual_memory().percent

def register_builtin_health_checks():
    from .monitor import HealthCheck
    HealthCheck("disk", lambda: (disk_free_gb() > 1, f"Free disk: {disk_free_gb():.2f}GB"))
    HealthCheck("cpu", lambda: (cpu_usage() < 90, f"CPU: {cpu_usage():.1f}%"))
    HealthCheck("memory", lambda: (mem_usage() < 90, f"Memory: {mem_usage():.1f}%"))

# Usage: register_builtin_health_checks()