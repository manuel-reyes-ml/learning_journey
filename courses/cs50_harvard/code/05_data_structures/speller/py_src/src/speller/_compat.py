"""Cross-version compatibility dispatcher.

Examines ``sys.version_info`` at import time and re-exports the appropriate
implementation from either _compat_py314 or _compat_py312. Downstream code
imports from here and remains version-agnostic.

This is the ONLY module that knows about Python version differences. The
rest of the package treats t-string availability as a feature flag:
    from speller._compat import HAS_TSTRINGS, format_log_event
"""

# =============================================================================
# IMPORTS
# =============================================================================

from __future__ import annotations

import sys

# Both ruff and mypy understand sys.version_info >= (3, 14) as a version-narrowing check —
# that's the line that keeps them quiet without # type: ignore everywhere.
HAS_TSTRINGS: bool = sys.version_info >= (3, 14)

if HAS_TSTRINGS:
    from speller._compat_py314 import format_log_event, template_to_msg_extras
else:
    from speller._compat_py312 import format_log_event, template_to_msg_extras

# =============================================================================
# EXPORTS
# =============================================================================

__all__ = ["HAS_TSTRINGS", "format_log_event", "template_to_msg_extras"]