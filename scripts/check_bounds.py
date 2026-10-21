"""Report dependency specifiers with no upper bound, and suggest `uv add` fixes.

Run from the workspace root:

    uv run python scripts/check_bounds.py            # report + suggested commands
    uv run python scripts/check_bounds.py -m   # also list major jumps a bulk upgrade would take

Read-only: it never edits pyproject.toml or uv.lock. Copy the commands it prints
after reviewing them.
"""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
import tomllib
from pathlib import Path

from packaging.requirements import Requirement
from packaging.version import Version

ROOT: Path = Path.cwd()


def next_major(v: Version) -> str:
    """Return the exclusive ceiling uv's `--bounds major` would write (Cargo-style for 0.x)."""
    if v.major > 0:
        return f"{v.major + 1}.0"
    if v.minor > 0:
        return f"0.{v.minor + 1}"
    return f"0.0.{v.micro + 1}"


def is_major_jump(old: Version, new: Version) -> bool:
    """True if `new` crosses the ceiling `next_major(old)` would set."""
    return new >= Version(next_major(old))


def locked_versions() -> dict[str, Version]:
    """Map each package name in uv.lock to its locked version."""
    lock = tomllib.loads((ROOT / "uv.lock").read_text(encoding="utf-8"))
    return {p["name"]: Version(p["version"]) for p in lock["package"] if "version" in p}


def member_files() -> list[Path]:
    """Return the root pyproject.toml plus every workspace member's."""
    root = tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))
    members = root.get("tool", {}).get("uv", {}).get("workspace", {}).get("members", [])
    return [ROOT / "pyproject.toml", *(ROOT / m / "pyproject.toml" for m in members)]


def sections(data: dict) -> list[tuple[str, list]]:
    """Yield (uv add flag, requirement list) for every dependency section."""
    out: list[tuple[str, list]] = [("", data.get("project", {}).get("dependencies", []))]

    for extra, reqs in data.get("project", {}).get("optional-dependencies", {}).items():
        out.append((f"--optional {extra}", reqs))
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
