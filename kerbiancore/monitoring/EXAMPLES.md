# KerbianCore Monitoring — Usage Examples

## Error Handling

```python
from kerbiancore.monitoring.core import ErrorContext, KerbianError

with ErrorContext():
    risky_function()
```

## Logger

```python
from kerbiancore.monitoring.logger import Logger, FileSink

logger = Logger("my.app")
logger.set_context(app="kerbian", session="abc123")
logger.info("This is an info log")
logger.error("Oops!", code=500)
logger.add_sink(FileSink("myapp.log"))
```

## Metrics

```python
from kerbiancore.monitoring.monitor import Counter, Gauge, Histogram, Timer

hits = Counter("hits")
hits.inc()
gauge = Gauge("memory")
gauge.set(1024)

hist = Histogram("latency", buckets=[0.1, 0.5, 1])
hist.observe(0.3)

timer = Timer("db_query")
def query():
    ...
timer.time(query)
```

## Alerts

```python
from kerbiancore.monitoring.alerts import Rule, AlertManager, PrintChannel

def disk_space_low():
    free = 50  # MB
    return (free < 100, f"Disk space low: {free}MB left")

AlertManager.add_rule(Rule("disk_low", disk_space_low, PrintChannel()))
AlertManager.run_periodic(30)  # Check every 30 seconds
```

## Tracing

```python
from kerbiancore.monitoring.trace import Tracer, print_exporter

tracer = Tracer(exporter=print_exporter)
@tracer.trace("handler")
def my_handler():
    ...
```