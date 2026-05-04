"""Cross-version compatibility dispatcher.

Routes Template/Interpolation imports based on Python version. Type
checkers see the real types unconditionally via TYPE_CHECKING; runtime
gets either the real classes (3.14+) or sentinel classes (<3.14) whose
isinstance() checks always return False, allowing isinstance-guarded
code paths to fall through harmlessly.
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

# Mypy walks through the TYPE_CHECKING block (which it pretends is True) and stops there —
# it sees Template got imported, it's happy. The other branches it skips. At runtime, Python
# skips the TYPE_CHECKING block (which is genuinely False) and falls into one of the other
# two branches. Each audience sees what they need.
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