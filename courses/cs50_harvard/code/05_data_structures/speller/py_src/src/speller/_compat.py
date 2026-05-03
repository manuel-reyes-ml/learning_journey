"""
"""

# =============================================================================
# IMPORTS
# =============================================================================

from __future__ import annotations

import sys

HAS_TSTRINGS: bool = sys.version_info >= (3, 14)

if HAS_TSTRINGS:
    from speller._compat_py314 import format_log_event, template_to_msg_extras
else:
    from speller._compat_py312 import format_log_event, template_to_msg_extras

# =============================================================================
# EXPORTS
# =============================================================================

__all__ = ["HAS_TSTRINGS", "format_log_event", "template_to_msg_extras"]