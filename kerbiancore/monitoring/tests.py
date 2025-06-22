"""
KerbianCore Monitoring: Basic Unit Tests.
"""

from kerbiancore.monitoring.core import KerbianError, ValidationError, ErrorContext, exception_guard
from kerbiancore.monitoring.logger import Logger, ConsoleSink, FileSink
from kerbiancore.monitoring.monitor import Counter, Gauge, Histogram, Timer, HealthCheck, Uptime
from kerbiancore.monitoring.alerts import Rule, AlertManager, PrintChannel
from kerbiancore.monitoring.trace import Tracer, print_exporter

def test_error_handling():
    try:
        raise ValidationError("fail!")
    except KerbianError:
        pass

    with ErrorContext(reraise=False):
        raise KerbianError("Context test")

    @exception_guard(reraise=False)
    def bad():
        raise KerbianError()
    bad()

def test_logger_basic():
    logger = Logger("test.module")
    logger.info("Test info")
    logger.debug("Test debug", foo=1)
    logger.error("Test error", bar="err")
    # Add file sink, log to file
    logger.add_sink(FileSink("test.log"))
    logger.warning("File sink test")
    import os
    os.remove("test.log")

def test_metrics():
    c = Counter("hits")
    c.inc()
    assert c.get() == 1
    g = Gauge("mem")
    g.set(5)
    g.inc(3)
    g.dec(2)
    assert g.get() == 6
    h = Histogram("hist", buckets=[1, 2, 5])
    h.observe(1.5)
    h.observe(0.5)
    assert sum(cnt for b, cnt in h.get()) == 2
    t = Timer("t")
    t.observe(0.2)
    assert t.average() > 0

def test_health_uptime():
    HealthCheck("test", lambda: (True, "OK"))
    res = HealthCheck.run_all()
    assert "test" in res
    assert res["test"][0] is True
    assert Uptime.seconds() >= 0

def test_alerts():
    count = {"val": 0}
    def check():
        count["val"] += 1
        return (count["val"] >= 2, "Threshold reached")
    rule = Rule("test", check, PrintChannel(), suppress_secs=0)
    AlertManager.add_rule(rule)
    AlertManager.check_all()
    AlertManager.check_all()  # Should print alert only once per check

def test_tracing():
    tracer = Tracer(exporter=print_exporter)
    @tracer.trace("test-span")
    def foo():
        return 42
    assert foo() == 42

if __name__ == "__main__":
    test_error_handling()
    test_logger_basic()
    test_metrics()
    test_health_uptime()
    test_alerts()
    test_tracing()
    print("All monitoring tests passed.")