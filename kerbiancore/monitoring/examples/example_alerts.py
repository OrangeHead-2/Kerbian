"""
Example: Rule-based alerting with KerbianCore
"""

from kerbiancore.monitoring.alerts import Rule, AlertManager, PrintChannel

def high_load():
    load = 95
    return (load > 90, f"High load detected: {load}%")

AlertManager.add_rule(Rule("load_alert", high_load, PrintChannel(), suppress_secs=10))
AlertManager.check_all()

print("Alert example completed.")