"""
"""

from __future__ import annotations

from pathlib import Path
import pytest

from speller.config import ExitCode

# Import internal helpers for direct testing.
# Underscore-prefixed functions are "internal" by convention but
# still importable — the underscore is a HINT, not enforcement.
# Testing private functions is acceptable when they contain
# significant logic worth verifying independently.
from speller.__main__ import _build_parser, _validate_paths, main


# =============================================================================
# ARGUMENT PARSER
# =============================================================================

