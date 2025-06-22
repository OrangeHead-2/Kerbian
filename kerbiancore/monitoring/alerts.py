"""
KerbianCore Alerts:
- Rule-based alerting, anomaly detection
- Multiple channels (email, webhook, Slack, etc.)
- Escalation, suppression
"""

import threading
import time

class AlertChannel:
    def send(self, subject, body):
        raise NotImplementedError

class PrintChannel(AlertChannel):
    def send(self, subject, body):
        print(f"[ALERT] {subject}\n{body}")

class Rule:
    def __init__(self, name, check_fn, channel, threshold=None, suppress_secs=60):
        self.name = name
        self.check_fn = check_fn
        self.channel = channel
        self.threshold = threshold
        self.suppress_secs = suppress_secs
        self._last_alert = 0
        self.lock = threading.Lock()

    def evaluate(self):
        """Run the check, send alert if triggered and not suppressed."""
        try:
            triggered, msg = self.check_fn()
        except Exception as e:
            triggered, msg = True, f"Rule error: {e}"
        if triggered:
            now = time.time()
            with self.lock:
                if now - self._last_alert >= self.suppress_secs:
                    self.channel.send(f"Rule Triggered: {self.name}", msg)
                    self._last_alert = now

class AlertManager:
    rules = []

    @classmethod
    def add_rule(cls, rule):
        cls.rules.append(rule)

    @classmethod
    def check_all(cls):
        for rule in cls.rules:
            rule.evaluate()

    @classmethod
    def run_periodic(cls, interval=10):
        def loop():
            while True:
                cls.check_all()
                time.sleep(interval)
        t = threading.Thread(target=loop, daemon=True)
        t.start()

# Example: Add rules, run AlertManager.run_periodic()