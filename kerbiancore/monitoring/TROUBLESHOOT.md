# KerbianCore Monitoring — Troubleshooting

## Logging Issues

- **No logs appearing:**  
  Check logger level and sinks. Ensure your logger is configured and not filtered by level.
- **Async logs missing:**  
  If using async logging, make sure your program does not exit before the background thread flushes logs.
- **File logs not written:**  
  Check permissions for your log file. FileSink must be able to write.

## Metrics Issues

- **Counters/Gauges not updating:**  
  Make sure you are calling `.inc()`, `.set()` methods and not overwriting your metric objects.
- **Health checks always failing:**  
  Check your health check logic. Return `(True, msg)` for healthy, `(False, msg)` for unhealthy.

## Alerts

- **Alerts not firing:**  
  Confirm your rule function returns `(True, "msg")` when it should alert.
  Check `suppress_secs` is not set too high.

## Tracing

- **No traces exported:**  
  Make sure the tracer is initialized with a valid exporter, and that your code is running inside traced functions.

## General

- **Threading issues:**  
  Many components use background threads. If your app exits immediately, logs/alerts may not flush.
- **Resource usage:**  
  For very high log/metric volumes, consider batching or forwarding to a remote aggregator.

---

For further help, see [kerbiancore/monitoring/README.md](./README.md)