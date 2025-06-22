"""
KerbianCore Monitoring: Utility functions

- Stack trace formatting
- Trace ID/session ID generator
- Time helpers
"""

import uuid
import time
import traceback

def gen_trace_id():
    return uuid.uuid4().hex

def gen_session_id():
    return uuid.uuid4().hex

def now_utc():
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())

def format_exception(exc_info=None):
    if exc_info is None:
        exc_info = sys.exc_info()
    return "".join(traceback.format_exception(*exc_info))

def short_stack():
    return traceback.format_stack(limit=4)