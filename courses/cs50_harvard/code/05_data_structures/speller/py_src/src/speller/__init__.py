"""
"""
# Adding public API exports makes the package more professional

from __future__ import annotations
import logging
import sys

try:
    from speller.main import main
except ImportError as e:
    sys.exit(f"Error: cannot find relative modules.\nDetails: {e}")
    

__all__ = ["main"]


logging.getLogger(__name__).addHandler(logging.NullHandler())
# This does exactly **one thing**: it silences the warning `"No handlers
# could be found for logger 'speller'"` when someone imports your package
# but doesn't configure logging themselves.

# Without it, if your code calls `logger.warning("file not found")` and the user
# of your package hasn't set up any logging, Python prints an ugly warning to
# stderr. `NullHandler` is a "black hole" — it catches log messages and discards
# them silently.

# The key idea is **separation of concerns**:
#   - the *library* (your `speller` package) should never decide *where* logs go. 
#   - That's the *application's* job. This is why LangChain, scikit-learn, and Airflow
#     all use this same pattern in their `__init__.py`.