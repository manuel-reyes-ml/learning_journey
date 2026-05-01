"""PEP 750 t-string log formatter. Requires Python 3.14+."""

# =============================================================================
# IMPORTS
# =============================================================================

from __future__ import annotations

from string.templatelib import Interpolation, Template


# =============================================================================
# CORE FUNCTION
# =============================================================================

def format_log_event(event: str, **kwargs: object) -> Template:
    