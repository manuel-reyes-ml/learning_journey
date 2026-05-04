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
from typing import TYPE_CHECKING

# Both ruff and mypy understand sys.version_info >= (3, 14) as a version-narrowing check —
# that's the line that keeps them quiet without # type: ignore everywhere.
HAS_TSTRINGS: bool = sys.version_info >= (3, 14)

if TYPE_CHECKING:
    # Type checkers always see the real stdlib types - no narrowing needed.
    from string.templatelib import Interpolation, Template
    
    from speller._compat_py314 import format_log_event, template_to_msg_extras
    
elif HAS_TSTRINGS:
    from speller._compat_py314 import (
        Interpolation,
        Template,
        format_log_event,
        template_to_msg_extras,
    )
else:
    # Runtime on <3.14: sentinel classes. isinstance(x, Template) is always
    # False because nothing can ever be an instance - string.templatelib
    # doesn´t exist, so no real Template can enter the program.
    class Template:  # noqa: D101
        __slots__ = ()
        
    class Interpolation:  # noqa: D101
        __slots__ = ()
        
    from speller._compat_py312 import format_log_event, template_to_msg_extras

# =============================================================================
# EXPORTS
# =============================================================================

__all__ = [
    "HAS_TSTRINGS",
    "Interpolation",
    "Template",
    "format_log_event",
    "template_to_msg_extras",
]