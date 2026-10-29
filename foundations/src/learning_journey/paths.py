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


@cache
def project_root() -> Path:
    """Repo root: LJ_PROJECT_ROOT env var, else first parent containing a marker."""
    if override := os.environ.get("LJ_PROJECT_ROOT"):
        return Path(override).resolve()
    for parent in Path(__file__).resolve().parents:
        if any((parent / marker).exists() for marker in _ROOT_MARKERS):
            return parent
    raise RuntimeError(
        f"No project root marker {_ROOT_MARKERS} found above {__file__}; set LJ_PROJECT_ROOT."
    )


PROJECT_ROOT: Final[Path] = project_root()
FOUNDATIONS_DIR: Final[Path] = PROJECT_ROOT / "foundations"
DATA_DIR: Final[Path] = FOUNDATIONS_DIR / "data"
SQL_DIR: Final[Path] = FOUNDATIONS_DIR / "sql"
