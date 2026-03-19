"""
"""
# Adding public API exports makes the package more professional

from __future__ import annotations

import logging


# Library logging pattern: stay silent unless the application configures
# logging. The CLI entry point (__main__.py) calls config_logging() to
# acivate console/file handlers.
logging.getLogger(__name__).addHandler(logging.NullHandler())

# Package metadata
__version__ = "1.0.0"



# __init__.py (runs on import)     → "What does this package OFFER to other code?"
# __main__.py (runs on execution)  → "What happens when someone RUNS this package from the terminal?"

# No ImportError sys.exit() on __init__.py because it kills any program that imports the package
