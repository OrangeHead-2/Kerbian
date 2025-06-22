"""
KerbianCore Monitoring: Log Filters and Formatters

- LevelFilter: filter logs below a threshold
- FieldFilter: filter logs based on extra fields (user, session, etc)
- RegexFilter: filter (allow or deny) logs matching a regex in msg or fields
- Formatter: custom log message formatting (plain, JSON, custom)
"""

import re
import json

class LevelFilter:
    def __init__(self, min_level, levels=None):
        self.min_level = min_level
        self.levels = levels or ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
    def allow(self, record):
        return self.levels.index(record.level) >= self.levels.index(self.min_level)

class FieldFilter:
    def __init__(self, field, value):
        self.field = field
        self.value = value
    def allow(self, record):
        return record.fields.get(self.field) == self.value

class RegexFilter:
    def __init__(self, pattern, field=None):
        self.pattern = re.compile(pattern)
        self.field = field
    def allow(self, record):
        if self.field:
            val = str(record.fields.get(self.field, ""))
        else:
            val = record.msg
        return bool(self.pattern.search(val))

class Formatter:
    def __init__(self, fmt="{timestamp} [{level}] {name}: {msg} {fields}", json_mode=False):
        self.fmt = fmt
        self.json_mode = json_mode
    def format(self, record):
        fs = " ".join(f"{k}={v}" for k, v in record.fields.items()) if record.fields else ""
        if self.json_mode:
            return json.dumps({
                "timestamp": record.timestamp.isoformat(),
                "level": record.level,
                "name": record.name,
                "msg": record.msg,
                "fields": record.fields,
            })
        else:
            return self.fmt.format(
                timestamp=record.timestamp,
                level=record.level,
                name=record.name,
                msg=record.msg,
                fields=fs,
            )