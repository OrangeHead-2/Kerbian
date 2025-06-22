"""
KerbianCore Build/Release module init.
"""

from .core import *
try:
    from .template_android import *
except ImportError:
    pass
try:
    from .template_ios import *
except ImportError:
    pass