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

# The pieces of Path(__file__).resolve().parents[1]:
#   > Path(__file__) — the path to this .py file.
#   > .resolve() — make it absolute and follow any shortcuts (symlinks).
#     Always do this before climbing, so .parent climbs the real folders.
#   > .parents[1] — the same as .parent.parent, just tidier. parents[0] is
#     the folder holding the file (scripts/); parents[1] is one above that (the repo).
#
# Note that Path(".") prints as just . — it's a relative path. You only see where it actually
# points after .resolve() or Path.cwd(), which is exactly why this bug hides so well.

# Path(".") means wherever your terminal is standing when you run the command —
# the current working directory. It knows nothing about your project,
# and nothing about where the script file lives.
# Path(__file__) means wherever this file lives on disk. It's anchored to the file
# itself, so it gives the same answer no matter where you run it from.
#
# iterdir() -> Everything directly inside — files and folders, one level, no filter
#   > Open the top drawer and look at what's in it. Don't open anything inside.
# glob("*.py") -> Pattern match, this level only
#   > Open the top drawer, pick out only the things matching the pattern.
# glob("*/*.py") -> Exactly one folder down
local: set[str] = {p.name for p in Path(".").iterdir() if p.is_dir()} | {
    p.stem for p in Path(".").glob("*.py")
}
found: dict[str, set[str]] = {}


# =============================================================================
# CORE FUNCTIONS
# =============================================================================


def scan(source: str, origin: str) -> None:
    # ast.parse() -> Characters become words, words become a tree
    try:
        tree = ast.parse(source)
    except SyntaxError:
        return

    # ast.walk visits one row at a time, top to bottom: Module first, then both boxes
    # on the second row, then all three on the third row, and so on. It finishes a
    # whole generation of the family tree before moving to the next one.
    #
    # ast.walk doesn't find anything by itself. It just visits every box and hands
    # each one to you. The finding is your question — isinstance(node, ast.Import)
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            names = [a.name for a in node.names]
        elif isinstance(node, ast.ImportFrom) and node.level == 0 and node.module:
            names = [node.module]
        else:
            continue

        for name in names:
            top = name.split(".")[0]
            # stdlib_module_names -> A frozenset, not a list. A set can't be changed,
            # and checking "pandas" in it is instant no matter how big it is.
            # A list would check all 300 names one at a time.
            # Top-level names only. os is there; os.path isn't. That's why the script
            # does name.split(".")[0] first — it turns os.path into os before asking.
            if top not in sys.stdlib_module_names and top not in local:
                found.setdefault(top, set()).add(origin)


# Now that you're on uv, every repo has a pyproject.toml at its root, which makes it the
# perfect landmark. This works in a notebook, in a script, and in a test, from any subfolder.
def find_project_root(start: Path | None = None) -> Path:
    """Return the nearest ancestor directory containing ``pyproject.toml``."""
    here = (start or Path.cwd()).resolve()

    for folder in (here, *here.parents):
        if (folder / "pyproject.toml").exists():
            return folder
    raise FileNotFoundError(f"No pyproject.toml found above {here}")


# =============================================================================
# MAIN FUNCTION
# =============================================================================


def main(argv: list[str] | None = None) -> int:
    # rglob() -> Every level, all the way down
    #   > open every drawer, and every box inside every drawer, and pull out
    #     everything matching. The r means recursive — it keeps going deeper.
    #     rglob("*.py") is exactly the same as glob("**/*.py").
    for path in find_project_root().rglob("*"):
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
                "".join(c.get("source", [])) for c in cells if c.get("cell_type") == "code"
            )
            code = "\n".join(
                ln for ln in code.splitlines() if not ln.lstrip().startswith(("%", "!"))
            )
            scan(code, str(path))

    for mod in sorted(found):
        print(f"{mod:<20} {len(found[mod]):>3} file(s)")

    return 0


# =============================================================================
# MAIN GUARD
# =============================================================================


if __name__ == "__main__":
    sys.exit(main())
