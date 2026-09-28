""" """

# =============================================================================
# IMPORTS
# =============================================================================

import ast
import json
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


# =============================================================================
# MAIN FUNCTION
# =============================================================================


def main(argv: list[str] | None = None) -> None:
    for path in Path(".").rglob("*"):
        if SKIP & set(path.parts):
            continue
        if path.suffix == ".py":
            scan(path.read_text(errors="ignore"), str(path))
        elif path.suffix == ".ipynb":
            try:
                cells = json.loads(path.read_text(errors="ignore")).get("cells", [])
            except json.JSONDecodeError:
                continue
            code = "\n".join(
                "".join(c.get("source", []) for c in cells if c.get("cell_type") == "code")
            )
            code = "\n".join(
                ln for ln in code.splitlines() if not ln.lstrip().startswith(("%", "!"))
            )
            scan(code, str(path))

    for mod in sorted(found):
        print(f"{mod:<20} {len(found[mod]):>3} file(s)")
