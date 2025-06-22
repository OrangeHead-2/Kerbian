# KerbianCore Monitoring — Testing Guide

This guide covers strategies and tips for testing your monitoring, logging, metrics, alerts, and tracing code in KerbianCore.

---

## 1. Error Handling

- **Unit Test:**
  - Raise each custom error and ensure it is caught as expected.
  - Test the global error handler by triggering uncaught exceptions.
  - Test the `ErrorContext` context manager with and without logger.

```python
from kerbiancore.monitoring.core import KerbianError, ErrorContext

def test_kerbian_error():
    try:
        raise KerbianError("fail!")
    except KerbianError:
        assert True

def test_error_context():
    with ErrorContext(reraise=False):
        raise KerbianError()
```

---

## 2. Logging

- **Unit Test:**
  - Log at each level, verify output (or file).
  - Add and remove sinks, test async mode.
  - Test context injection and dynamic config.
  - Use `FileSink` and check file contents.

```python
from kerbiancore.monitoring.logger import Logger, FileSink

def test_logger_levels():
    logger = Logger("test")
    logger.debug("debug")
    logger.info("info")
    logger.error("error")

def test_file_sink(tmp_path):
    file = tmp_path / "log.txt"
    logger = Logger("testfile")
    logger.add_sink(FileSink(str(file)))
    logger.info("file test")
    assert "file test" in file.read_text()
```

---

## 3. Metrics

- **Unit Test:**
  - Increment counters, gauges, and observe histograms/timers.
  - Register and run health checks, check return values.

```python
from kerbiancore.monitoring.monitor import Counter, HealthCheck

def test_counter():
    c = Counter("mycounter")
    c.inc(2)
    assert c.get() == 2

def test_health():
    HealthCheck("test_health", lambda: (True, "ok"))
    res = HealthCheck.run_all()
    assert res["test_health"][0] is True
```

---

## 4. Alerts

- **Unit Test:**
  - Register a rule and channel, verify alert is triggered.
  - Test suppression interval.

```python
from kerbiancore.monitoring.alerts import Rule, AlertManager, PrintChannel

def always_trigger():
    return (True, "Always triggers")
rule = Rule("always", always_trigger, PrintChannel(), suppress_secs=0)
AlertManager.add_rule(rule)
AlertManager.check_all()  # Should print alert
```

---

## 5. Tracing

- **Unit Test:**
  - Create tracer, trace a function, verify exporter is called.

```python
from kerbiancore.monitoring.trace import Tracer

events = []
def exporter(span): events.append(span.to_dict())
tracer = Tracer(exporter=exporter)

@tracer.trace("unit")
def foo(): return 1

foo()
assert events and events[0]["name"] == "unit"
```

---

**Tip:**  
Use the provided `kerbiancore/monitoring/tests.py` as a template for broader coverage and integration tests.

---