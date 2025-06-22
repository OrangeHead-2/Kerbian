# KerbianCore Monitoring — Configuration Guide

## Logging Configuration

You can configure the logger globally at runtime:

```python
from kerbiancore.monitoring.logger import Logger, FileSink, ConsoleSink
from kerbiancore.monitoring.sinks import TCPSink, HTTPSink

Logger.configure(
    level="INFO",
    sinks=[ConsoleSink(), FileSink("myapp.log"), TCPSink("loghost", 9000)],
    async_mode=True,
    context={"env": "prod", "app": "kerbian"}
)
```

- **level:** Minimum level to log ("DEBUG", "INFO", ...)
- **sinks:** List of sinks (console, file, TCP, etc.)
- **async_mode:** If True, logs are queued and written in a background thread
- **context:** Fields added to every log record (e.g., app, environment, trace_id)

## Metrics/Health Configuration

- Create your own counters/gauges/histograms dynamically.
- Register health checks for any service:

```python
from kerbiancore.monitoring.monitor import HealthCheck

HealthCheck("redis", lambda: redis_connection.ping() is True)
HealthCheck("uptime", lambda: (True, f"Uptime {Uptime.seconds():.2f}s"))
```

## Alerting

- Register new rules and channels at runtime:

```python
from kerbiancore.monitoring.alerts import Rule, AlertManager
from kerbiancore.monitoring.alerts import PrintChannel

def cpu_high():
    return (cpu_usage() > 90, f"CPU usage high: {cpu_usage()}%")

AlertManager.add_rule(Rule("cpu_high", cpu_high, PrintChannel(), suppress_secs=300))
```

- Implement your own `AlertChannel` for custom notification (email, Slack, SMS).

## Tracing

- Use the `Tracer` and `Span` for distributed tracing.
- Provide your exporter for trace data (to DB, file, HTTP, etc).

---

## Example: Advanced Setup

```python
from kerbiancore.monitoring.logger import Logger, FileSink
from kerbiancore.monitoring.sinks import HTTPSink, BufferingSink

Logger.configure(
    level="DEBUG",
    sinks=[
        FileSink("prod.log"),
        BufferingSink(HTTPSink("https://logserver/api/logs"), batch_size=20)
    ],
    async_mode=True,
    context={"service": "coreapi"}
)
```

---