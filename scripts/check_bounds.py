"""Report dependency specifiers with no upper bound, and suggest `uv add` fixes.

Run from the workspace root:

    uv run python scripts/check_bounds.py            # report + suggested commands
    uv run python scripts/check_bounds.py --majors   # + major jumps a bulk upgrade would take

Read-only: it never edits pyproject.toml or uv.lock. Copy the commands it prints
after reviewing them.

Running examples used in the comments below (real values from learning_journey):
- EXAMPLE A  `requests>=2.34.2` in the root project (learning-journey), locked at 2.34.2.
- EXAMPLE B  `ruff>=0.4` in cs50-speller's `dev` extra, locked at 0.16.7 (a 0.x package).
- EXAMPLE C  `filelock 3.32.6 -> 4.2.4`, a transitive package a bulk upgrade would move.
"""

# Makes every type hint a lazy string, so `list[Path]` or `X | None` never fails at import time.
# Your AGENTS.md requires it as the first code line of every module.
from __future__ import annotations

# --- Standard library (ships with Python, nothing to install) -------------------------------------
import argparse  # Reads command-line flags. Here: `--majors`, so `--majors` → args.majors = True.
import re  # Regular expressions: pattern matching on text, e.g. finding "Update X vA -> vB".
import subprocess  # Runs another program (here: `uv lock ...`) and captures what it prints.
import sys  # Gives `sys.exit(code)`: 0 tells the shell "success", anything else "failure".
import tomllib  # Parses TOML (pyproject.toml, uv.lock) into Python dicts. Read-only, 3.11+.
from pathlib import Path  # Object-oriented file paths: Path("a") / "b" → a/b on any OS.

# --- Third-party: `packaging` is the PyPA library pip and uv's ecosystem use for versions --------
# Requirement: parses a dependency string into parts.
#   Requirement("requests>=2.34.2") → .name = "requests", .specifier = SpecifierSet(">=2.34.2")
# Version: a comparable version object, so versions compare as numbers, not text.
#   Version("2.10") > Version("2.9") is True, while the strings compare "2.10" < "2.9" (wrong).
from packaging.requirements import Requirement
from packaging.version import Version

# The folder you ran the script from. It must be the workspace root (where uv.lock lives).
# 'cwd' means Current Working Directory
ROOT: Path = Path.cwd()


def next_major(v: Version) -> str:
    """Return the exclusive ceiling uv's `--bounds major` would write (Cargo-style for 0.x)."""
    # Normal packages (1.0 and up): the first number is the major. Bump it, reset the rest.
    # EXAMPLE A: Version("2.34.2").major = 2 → returns "3.0" → ceiling `<3.0`.
    if v.major > 0:
        return f"{v.major + 1}.0"
    # 0.x packages: by convention the MINOR number acts as the major (any 0.16 → 0.17 may break).
    # EXAMPLE B: Version("0.16.7") → major 0, minor 16 → returns "0.17" → ceiling `<0.17`.
    #            That is why ruff needs a manual `<1.0` instead (see the chat notes).
    if v.minor > 0:
        return f"0.{v.minor + 1}"

    # 0.0.x packages: even the patch number may break. Version("0.0.3") → "0.0.4".
    return f"0.0.{v.micro + 1}"


def is_major_jump(old: Version, new: Version) -> bool:
    """True if `new` crosses the ceiling `next_major(old)` would set."""
    # EXAMPLE C: old 3.32.6 → next_major = "4.0"; new 4.2.4 >= 4.0 → True (major jump).
    #            old 3.32.6, new 3.32.7 → 3.32.7 >= 4.0 is False (safe patch update).
    return new >= Version(next_major(old))


def locked_versions() -> dict[str, Version]:
    """Map each package name in uv.lock to its locked version."""
    # read_text() → the whole file as one string; tomllib.loads() → nested dict.
    # uv.lock stores every package as a [[package]] table, so lock["package"] is a list of dicts:
    #   [{"name": "requests", "version": "2.34.2", "source": {...}, ...}, ...]
    lock = tomllib.loads((ROOT / "uv.lock").read_text(encoding="utf-8"))

    # Dict comprehension: one entry per package. The `if "version" in p` guard skips entries
    # without a version (some editable/virtual workspace entries).
    # EXAMPLE A: {"name": "requests", "version": "2.34.2"} → "requests": Version("2.34.2")
    return {p["name"]: Version(p["version"]) for p in lock["package"] if "version" in p}


def member_files() -> list[Path]:
    """Return the root pyproject.toml plus every workspace member's."""
    # Chained .get(key, {}) walks root["tool"]["uv"]["workspace"]["members"] without crashing
    # if a level is missing (a non-workspace repo just gets an empty list).
    # Here: ["llm-api-smoke-test", "courses/.../speller/py_src", "foundations"]
    root = tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))
    members = root.get("tool", {}).get("uv", {}).get("workspace", {}).get("members", [])

    # `*(...)` unpacks a generator into the list, so the result is flat:
    #   [ROOT/pyproject.toml, ROOT/llm-api-smoke-test/pyproject.toml, ...]
    return [ROOT / "pyproject.toml", *(ROOT / m / "pyproject.toml" for m in members)]


def sections(data: dict) -> list[tuple[str, list]]:
    """Yield (uv add flag, requirement list) for every dependency section."""
    # 1) Runtime dependencies → [project] dependencies. `uv add` needs no extra flag.
    #    EXAMPLE A lands here: ("", ["beautifulsoup4>=4.15.0", ..., "requests>=2.34.2", ...])
    out: list[tuple[str, list]] = [("", data.get("project", {}).get("dependencies", []))]

    # 2) Extras → [project.optional-dependencies]. `uv add --optional <name>` targets them.
    #    EXAMPLE B lands here: ("--optional dev", ["mypy>=1.0", "ruff>=0.4", ...]) (speller).
    for extra, reqs in data.get("project", {}).get("optional-dependencies", {}).items():
        out.append((f"--optional {extra}", reqs))

    # 3) Dependency groups → [dependency-groups]. `uv add --group <name>` targets them.
    #    Groups may contain {include-group = "test"} tables, which are not requirement strings,
    #    so `isinstance(r, str)` keeps only the strings:
    #    dev = [{include-group = "test"}, "ruff>=0.5,<1.0"]  →  ["ruff>=0.5,<1.0"]
    for group, reqs in data.get("dependency-groups", {}).items():
        out.append((f"--group {group}", [r for r in reqs if isinstance(r, str)]))

    return out


def report(locked: dict[str, Version]) -> int:
    """Print every requirement without a ceiling and the command that would add one."""
    found = 0
    for path in member_files():
        data = tomllib.loads(path.read_text(encoding="utf-8"))
        name = data["project"]["name"]
        for flag, reqs in sections(data):
            for raw in reqs:
                req = Requirement(raw)
                ops = {s.operator for s in req.specifier}
                if ops & {"<", "<=", "==", "-=", "==="}:
                    continue  # alreay bounded
                pkg = re.sub(r"[-_.]+", "-", req.name).lower()
                v = locked.get(pkg)
                if v is None:
                    continue
                found += 1
                floor = str(req.specifier).lstrip(">=") or str(v)
                new = f"{req.name}>={floor},<{next_major(v)}"
                pkg_flag = "" if path.parent == ROOT else f"--package {name}"
                print(f"# {name:<20} {raw:<28} locked {v}")
                print(f'uv add {pkg_flag}{flag + " " if flag else ""}"{new}" --no-sync\n')
    print(f"{found} requirement(s) without an upper bound.")

    return found


def majors() -> None:
    """List major jumps (direct or transitive) a bulk `uv lock --upgrade` would take."""
    out = subprocess.run(
        ["uv", "lock", "--upgrade", "--dry-run"], capture_output=True, text=True, check=True
    ).stderr
    hits = []
    for m in re.finditer(r"Update (\S+) v(\S+) -> v(\S+)", out):
        pkg, old, new = m.group(1), Version(m.group(2)), Version(m.group(3))
        if is_major_jump(old, new):
            hits.append(f"   {pkg:<24} {old} -> {new}")
    print("\nMajor jumps in a bulk upgrade (uv lock --upgrade --dry-run:)")
    print("\n".join(hits) if hits else "    none")


def main() -> int:
    """Entry point."""
    parser = argparse.ArgumentParser(
        description=__doc__.splitlines()[0] if __doc__ is not None else ""
    )
    parser.add_argument(
        "--majors",
        "-m",
        action="store_true",
        help="also list major jumps",
    )
    args = parser.parse_args()

    report(locked_versions())
    if args.majors:
        majors()

    return 0


if __name__ == "__main__":
    sys.exit(main())
