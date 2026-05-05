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
    # Runtime on 3.14+: actually imports the real Template
    from speller._compat_py314 import (
        Interpolation,
        Template,
        format_log_event,
        template_to_msg_extras,
    )
else:
    # This defines a class that:
    #   ✅ Exists, so Template is a valid name in the namespace
    #   ✅ Can be referenced in def f(t: Template) annotations without crashing
    #   ✅ Can be used as the second argument to isinstance(x, Template) without crashing
    #   ❌ Has no methods, no attributes, no behavior
    #   ❌ Is never instantiated by any code in the program
    class Template:
        # Why __slots__ = ()?
        # Pure hygiene, two reasons:
        #   1. Memory — declares the class has no instance attributes, saves a few bytes per
        #   (never-created) instance. Insignificant here, but a free correctness statement.
        #   2. Signaling intent — it tells the next developer reading the code "this class has no
        #   data; don't try to add any." The empty tuple says "yes, I really meant zero attributes."
        __slots__ = ()

    class Interpolation:
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


# Avoiding heavy imports just for types. If you only need pandas.DataFrame for a type annotation,
# importing pandas at runtime adds 200ms to your CLI startup:
#   from typing import TYPE_CHECKING
#   if TYPE_CHECKING:
#       import pandas as pd          # mypy needs it; runtime doesn't
#
#   def summarize(df: "pd.DataFrame") -> dict: ...   # runtime never imports pandas
#
# The cleanest way to avoid the quotes is from __future__ import annotations at the top of the file —
# it makes every annotation lazy by default.

# Walk through what happens when a downstream file does from speller._compat import Template:
# ┌────────────────────────────────────────────────────────────────┐
# │  Type checker's view (TYPE_CHECKING is True)                   │
# │  ─────────────────────────────────────────                     │
# │  Template = string.templatelib.Template  (the real one)        │
# │  → all annotations type-check correctly                        │
# │  → all isinstance() calls type-check correctly                 │
# │  → zero "possibly unbound" warnings                            │
# └────────────────────────────────────────────────────────────────┘

# ┌────────────────────────────────────────────────────────────────┐
# │  Python 3.14 runtime view                                      │
# │  ─────────────────────────────                                 │
# │  TYPE_CHECKING is False → skip first branch                    │
# │  sys.version_info >= (3,14) is True → import real Template     │
# │  Template = string.templatelib.Template  (the real one)        │
# │  → isinstance works as expected                                │
# │  → format_log_event returns a real Template                    │
# └────────────────────────────────────────────────────────────────┘

# ┌────────────────────────────────────────────────────────────────┐
# │  Python 3.12 runtime view                                      │
# │  ─────────────────────────────                                 │
# │  TYPE_CHECKING is False → skip first branch                    │
# │  sys.version_info >= (3,14) is False → skip second branch      │
# │  fall into else: define empty sentinel class                   │
# │  Template = <speller._compat.Template, empty class>            │
# │  → isinstance(anything_real, Template) is always False         │
# │  → no crashes, no defensive code anywhere downstream           │
# └────────────────────────────────────────────────────────────────┘
# Three audiences, three views, one source file. That's the production-grade idea.
