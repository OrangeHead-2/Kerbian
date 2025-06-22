# KerbianCore Monitoring

Production-grade error handling, logging, metrics, alerting, and distributed tracing for your apps.

---

## Features

- **Error Handling:** Unified error base classes, global error handler, context managers, decorators
- **Logging:** Hierarchical loggers, colorized/structured/async logs, flexible sinks, context/tracing support
- **Metrics:** Counters, gauges, histograms, timers, health checks, uptime, heartbeats
- **Alerts:** Rule-based alerting, anomaly detection, multi-channel, escalation/suppression
- **Tracing:** Distributed tracing, span/context propagation, exporters

---

## Quickstart

```python
from kerbiancore.monitoring.logger import Logger
logger = Logger("my.module")
logger.info("App started", user="alice")
logger.error("Something failed", code=500)

from kerbiancore.monitoring.core import ErrorContext
with ErrorContext(logger):
    risky_operation()
```

---

## Advanced Logging

- Add sinks: `logger.add_sink(FileSink("my.log"))`
- Structured/context: `logger.set_context(session="abc123")`
- Async: `Logger.configure(async_mode=True)`

---

## Metrics & Health

```python
from kerbiancore.monitoring.monitor import Counter, HealthCheck
hits = Counter("hits")
hits.inc()
HealthCheck("db", lambda: db.is_alive())
```

---

## Alerting

```python
from kerbiancore.monitoring.alerts import Rule, AlertManager, PrintChannel
def disk_low(): return (disk_free() < 100, "Low disk space")
AlertManager.add_rule(Rule("disk_space", disk_low, PrintChannel()))
AlertManager.run_periodic(10)
```

---

## Tracing

```python
from kerbiancore.monitoring.trace import Tracer, print_exporter
tracer = Tracer(exporter=print_exporter)
@tracer.trace("myfunc")
def myfunc(): ...
```

---

## Extending

- Write your own log sinks (subclass `LogSink`)
- Custom alert channels (subclass `AlertChannel`)
- Pluggable health checks, exporters, metrics

---