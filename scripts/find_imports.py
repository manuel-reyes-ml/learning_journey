""" """

# =============================================================================
# IMPORTS
# =============================================================================

import ast
import sys
from pathlib import Path

# =============================================================================
# MODULE CONFIGURATION
# =============================================================================
# =====================================================
# Constants
# =====================================================

SKIP: set[str] = {".venv", "venv", ".git", "node_modules", "build", "dist"}
local: set[str] = {p.name for p in Path(".").iterdir() if p.is_dir()} | {
    p.stem for p in Path(".").glob("*.py")
}
found: dict[str, set[str]] = {}


# =============================================================================
# CORE FUNCTIONS
# =============================================================================


def scan(source: str, origin: str) -> None:
    try:
        tree = ast.parse(source)
    except SyntaxError:
        return

    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            names = [a.name for a in node.names]
        elif isinstance(node, ast.ImportFrom) and node.level == 0 and node.module:
            names = [node.module]
        else:
            continue

        for name in names:
            top = name.split(".")[0]
            if top not in sys.stdlib_module_names and top not in local:
                found.setdefault(top, set()).add(origin)
