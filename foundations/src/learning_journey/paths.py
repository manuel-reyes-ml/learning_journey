"""Single source of truth for filesystem locations. Import, never recompute."""

from __future__ import annotations

import os
from functools import cache
from pathlib import Path
from typing import Final

__all__ = [
    "DATA_DIR",
    "FOUNDATIONS_DIR",
    "PROJECT_ROOT",
    "SQL_DIR",
]

# uv.lock lives only at the workspace root (members share it), and it is
# copied into Docker images, unlike .git. Keep .git as the fallback marker.
_ROOT_MARKERS: Final[tuple[str, ...]] = ("uv.lock", ".git")


# @cache = @lru_cache(maxsize=None)
# Both come from functools and do memoization: the first call with some arguments runs the
# function and stores the result, keyed by those arguments. Later calls with the same
# arguments return the stored result without running the function again.
#
# Prefer @cache on Python ≥ 3.9, and use lru_cache(maxsize=N) when arguments vary and
# memory must be bounded.
@cache
def project_root() -> Path:
    """Repo root: LJ_PROJECT_ROOT env var, else first parent containing a marker."""
    # The 'walrus' operator := assigns a value and gives that value back in the same expression.
    # A normal = is a statement, so it can't sit inside an if or a while.
    # Our code below is the same as:
    #   override = os.environ.get("LJ_PROJECT_ROOT")   # str, or None if not set
    #   if override:                                   # None and "" are both falsy
    #       return Path(override).resolve()
    if override := os.environ.get("LJ_PROJECT_ROOT"):
        return Path(override).resolve()
    for parent in Path(__file__).resolve().parents:
        if any((parent / marker).exists() for marker in _ROOT_MARKERS):
            return parent
    raise RuntimeError(
        f"No project root marker {_ROOT_MARKERS} found above {__file__}; set LJ_PROJECT_ROOT."
    )


# This is the same “define paths once in a module, import everywhere” pattern
PROJECT_ROOT: Final[Path] = project_root()
FOUNDATIONS_DIR: Final[Path] = PROJECT_ROOT / "foundations"
DATA_DIR: Final[Path] = FOUNDATIONS_DIR / "data"
SQL_DIR: Final[Path] = FOUNDATIONS_DIR / "sql"
