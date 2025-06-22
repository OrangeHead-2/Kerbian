"""
KerbianCore main package init.
Provides: high-level imports for the core modules.
"""

# Expose key modules at the package level
from . import testing
from . import buildrelease
from . import profiling
from . import security
from . import plugins
from . import cicd
from . import ecosystem

__version__ = "0.1.0"