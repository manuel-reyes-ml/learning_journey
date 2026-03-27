"""
"""
# Adding public API exports makes the package more professional

from __future__ import annotations

import logging


# Library logging pattern: stay silent unless the application configures
# logging. The CLI entry point (__main__.py) calls configure_logging() to
# acivate console/file handlers.
logging.getLogger(__name__).addHandler(logging.NullHandler())

# Package metadata
__version__ = "1.0.0"


# Trigger backend registration. Any import of the package guarantees
# all @register_class decorators have run.
#
# The as _dicts_module form is just a way of being explicit about your
# intent. It tellsthe next developer (or future you):
#
# "I imported this for its side effects only. I am not going to call _dicts_module.anything().
# The leading underscore means: don't touch this."
from speller import dictionaries as _dicts_module  # noqa: F401

# The # noqa: F401 comment tells ruff/flake8 "yes, I know I didn't use this
#import — it's intentional." This is a well-known Python pattern for plugin registration.


# __init__.py (runs on import)     → "What does this package OFFER to other code?"
# __main__.py (runs on execution)  → "What happens when someone RUNS this package from the terminal?"

# No ImportError sys.exit() on __init__.py because it kills any progrsam that imports the package


# =============================================================================
# THE UNDERSCORE CONVENTION
# =============================================================================

# _x = "internal variable"       # don't use outside this module
# __x = "name-mangled"           # don't use outside this class
# _MyClass                       # internal class
# _helper_function()             # internal function
# import something as _something # imported for side effects only
