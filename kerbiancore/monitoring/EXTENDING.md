# KerbianCore Monitoring — Extending the System

KerbianCore Monitoring is designed to be flexible and extensible. Here’s how you can add your own log sinks, alert channels, health checks, and trace exporters.

---

## Custom Log Sink

To create a new log sink (e.g., send logs to a database):

```python
from kerbiancore.monitoring.logger import LogRecord, LogSink

class MyDBSink(LogSink):
    def emit(self, record: LogRecord):
        # Insert record into your DB
        save_to_db(dict(
            timestamp=record.timestamp.isoformat(),
            level=record.level,
            name=record.name,
            msg=record.msg,
            fields=record.fields,
        ))

# Usage:
from kerbiancore.monitoring.logger import Logger
Logger.configure(sinks=[MyDBSink()])
```

---

## Custom Alert Channel

Send alerts to a custom service (e.g., your own push notification server):

```python
from kerbiancore.monitoring.alerts import AlertChannel

class PushChannel(AlertChannel):
    def send(self, subject, body):
        push_notify(subject=subject, message=body)

# Usage:
from kerbiancore.monitoring.alerts import Rule, AlertManager

AlertManager.add_rule(Rule("custom_rule", my_check_fn, PushChannel()))
```

---

## Custom Health Check

Register a custom health check:

```python
from kerbiancore.monitoring.monitor import HealthCheck

def db_health():
    try:
        return (db.ping() == "OK", "DB OK")
    except Exception as e:
        return (False, f"DB error: {e}")

HealthCheck("db", db_health)
```

---

## Custom Trace Exporter

Export traces to your own backend:

```python
from kerbiancore.monitoring.trace import Tracer

def my_trace_exporter(span):
    requests.post("https://mytracing.example/api/spans", json=span.to_dict())

tracer = Tracer(exporter=my_trace_exporter)
```

---

## Adding Metrics

Custom metric types (subclass `Counter`, `Gauge`, etc.) for special logic:

```python
from kerbiancore.monitoring.monitor import Counter

class ResettableCounter(Counter):
    def reset(self):
        with self.lock:
            self.value = 0

mycounter = ResettableCounter("special")
mycounter.inc(5)
mycounter.reset()
```

---

## More

- You can combine multiple sinks with `MultiSink`.
- Buffer or batch logs with `BufferingSink`.
- Create periodic background health/alert checks.
- Use context fields (trace/session/user) for log enrichment.
- Write integration plugins for other KerbianCore modules.

---