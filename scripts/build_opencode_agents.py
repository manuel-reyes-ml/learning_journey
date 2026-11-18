""" """

# =============================================================================
# IMPORTS
# =============================================================================

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Final

# =============================================================================
# MODULE CONFIGURATION
# =============================================================================
# =====================================================
# Constants
# =====================================================

ROOT: Final[Path] = Path(__file__).resolve().parents[1]
TEMPLATE_DIR: Final[Path] = ROOT / ".github" / "docs" / "prompts" / "opencode-agents"
OUTPUT_DIR: Final[Path] = ROOT / ".opencode" / "agents"

# One marker string, used both to stamp files and to recognise them later. Keeping it
# in a single constant means the orphan check can never drift from the banner text.
GENERATED_MARK: Final[str] = "GENERATED FILE - DO NOT EDIT"

BANNER: Final[str] = (
    "<!-- " + GENERATED_MARK + ".\n"
    "     Template: .github/docs/prompts/opencode-agents/{name}.md\n"
    "     Rebuild:  make opencode-agents\n"
    "     OpenCode 2.x does not expand {{file:...}} in agent files (ADR-001 §14),\n"
    "     so the included text below is a full copy, not a reference.\n"
    "-->\n"
)

# A whole line that is only an include, e.g. `{file:./.cursor/rules/x.mdc}`.
# An include written mid-sentence is left alone on purpose: prose may *mention* the
# syntax, and only a line of its own was ever meant as an import.
INCLUDE_LINE: Final[re.Pattern[str]] = re.compile(r"^\{file:(?P<path>[^{}\s]+)\}$")

# `---` + YAML + `---` at the very top of a file. DOTALL lets `.` cross newlines;
# the lazy `.*?` stops at the FIRST closing fence, not the last one in the file.
FRONTMATTER: Final[re.Pattern[str]] = re.compile(r"\A---\n(?P<yaml>.*?)\n---\n", re.DOTALL)


class AgentBuildError(Exception):
    """A template or one of its includes cannot be rendered."""


@dataclass(frozen=True, slots=True, kw_only=True)
class Rendered:
    """One finished output file, ready to be written or compared."""

    template: Path
    output: Path
    content: str
    includes: tuple[Path, ...]


# =============================================================================
# HELPER FUNCTIONS
# =============================================================================


def strip_frontmatter(text: str) -> str:
    """Return `text` without a leading YAML frontmatter block, if it has one.

    Parameters
    ----------
    text : str
        Full contents of an included file.

    Returns
    -------
    str
        The body only. Cursor's `description:` / `globs:` / `alwaysApply:` fields
        steer Cursor's own loader; inside an OpenCode prompt they are noise.
    """
    match = FRONTMATTER.match(text)
    return text[match.end() :] if match else text


def resolve_include(raw: str, root: Path, template: Path) -> Path:
    """Turn the path inside `{file:...}` into a checked file path.

    Parameters
    ----------
    raw : str
        The path exactly as written in the template, e.g. `./.cursor/rules/x.mdc`.
    root : Path
        Repository root. Includes are resolved against it, not against the template's
        own folder, so a template can move without its includes breaking.
    template : Path
        Template being rendered; used in error messages only.

    Returns
    -------
    Path
        Absolute path to an existing file inside `root`.

    Raises
    ------
    AgentBuildError
        If the path is absolute, home-relative, escapes the repo, or is not a file.
    """
    if raw.startswith(("/", "~")):
        raise AgentBuildError(f"{template.name}: include must be repo-relative: {raw}")

    path = (root / raw).resolve()
    # `is_relative_to` is the cheap containment test: `../../etc/passwd` resolves
    # outside the root and is rejected before anything is read.
    if not path.is_relative_to(root.resolve()):
        raise AgentBuildError(f"{template.name} include escapes the repository: {raw}")
    if not path.is_file():
        raise AgentBuildError(f"{template.name}: include not found: {raw}")
    return path


def load_include(path: Path, template: Path) -> str:
    """Read one included file and return the text to inline.

    Raises
    ------
    AgentBuildError
        If the file is empty after its frontmatter is removed, or itself contains an
        include line (nesting is unsupported, so it fails instead of half-working).
    """
    body = strip_frontmatter(path.read_text(encoding="utf-8")).strip()
    if not body:
        raise AgentBuildError(f"{template.name}: include is empty: {path.name}")
    for line in body.splitlines():
        if INCLUDE_LINE.match(line.strip()):
            raise AgentBuildError(
                f"{template.name}: nested include in {path.name} is no supported: {line.strip()}"
            )
    return body


# =============================================================================
# CORE FUNCTIONS
# =============================================================================


def render(template: Path, root: Path, output_dir: Path) -> Rendered:
    """Render one template into the content of its generated agent file.

    Parameters
    ----------
    template : Path
        Template file; its name becomes the agent ID.
    root : Path
        Repository root for resolving includes and for display paths.
    output_dir : Path
        Folder the generated file belongs in.

    Returns
    -------
    Rendered
        Output path, full file content and the files that were inlined.

    Raises
    ------
    AgentBuildError
        If the template has no frontmatter or any include fails a check.
    """
    text = template.read_text(encoding="utf-8")
    match = FRONTMATTER.match(text)
    if not match:
        raise AgentBuildError(f"{template.name}: template must start with --- frontmatter")

    frontmatter = match.group("yaml")
    body_lines: list[str] = []
    includes: list[Path] = []

    for line in text[match.end() :].splitlines():
        include = INCLUDE_LINE.match(line.strip())
        if include is None:
            body_lines.append(line)
            continue
        path = resolve_include(include.group("path"), root, template)
        shown = path.relative_to(root.resolve()).as_posix()
        includes.append(path)
        # Provenance markers: when an agent quotes a rule, these say where it lives.
        body_lines.append(f"<!-- begin include: {shown} -->")
        body_lines.append(load_include(path, template))
        body_lines.append(f"<!-- end include: {shown} -->")

    body = "\n".join(body_lines).strip()
    content = f"---\n{frontmatter}\n---\n" + BANNER.format(name=template.stem) + "\n" + body + "\n"
    return Rendered(
        template=template,
        output=output_dir / template.name,
        content=content,
        includes=tuple(includes),
    )


def templates(template_dir: Path) -> list[Path]:
    """Return every template, sorted so output order is stable across machines."""
    if not template_dir.is_dir():
        raise AgentBuildError(f"template folder not found: {template_dir}")
    found = sorted(template_dir.glob("*.md"))
    if not found:
        raise AgentBuildError(f"not templates in {template_dir}")
    return found


def orphans(expected: set[Path], output_dir: Path) -> list[Path]:
    """Return generated agent files whose template no longer exists.

    Only files carrying GENERATED_MARK are reported, so a hand-written agent kept
    directly in `.opencode/agents/` is never flagged.
    """
    if not output_dir.is_dir():
        return []
    return [
        path
        for path in sorted(output_dir.glob("*.md"))
        if path not in expected and GENERATED_MARK in path.read_text(encoding="utf-8")
    ]


def build(
    root: Path,
    template_dir: Path,
    output_dir: Path,
    *,
    check: bool = False,
    show: bool = False,
) -> int:
    """Render all templates, then write, verify or list them.

    Returns
    -------
    int
        Process exit code: 0 on success, 1 on any error, stale file or orphan.
    """
    # Render everything before writing anything: one broken include must not leave
    # half the agents regenerated and half stale.
    try:
        rendered = [render(t, root, output_dir) for t in templates(template_dir)]
    except AgentBuildError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        print("nothing was written", file=sys.stderr)
        return 1

    def rel(path: Path) -> str:
        return path.resolve().relative_to(root.resolve()).as_posix()

    if show:
        for item in rendered:
            print(f"{rel(item.template)} -> {rel(item.output)}")
            for include in item.includes:
                print(f"     + {rel(include)}")
        return 0

    left_over = orphans({r.output for r in rendered}, output_dir)

    if check:
        stale = [
            rel(r.output)
            for r in rendered
            if (r.output.read_text(encoding="utf-8") if r.output.exists() else "") != r.content
        ]
        if stale:
            print("STALE - run `make opencode-agents`:", file=sys.stderr)
            for stale_path in stale:
                print(f"    {stale_path}", file=sys.stderr)
        if left_over:
            # An orphan still loads as a live agent, so it fails rather than warns.
            print("ORPHANED - generated agents with no template. Delete them:", file=sys.stderr)
            for orphan_path in left_over:
                print(f"    {rel(orphan_path)}", file=sys.stderr)
        if stale or left_over:
            return 1
        print("all generated OpenCode agent files are up to date")
        return 0

    output_dir.mkdir(parents=True, exist_ok=True)
    for item in rendered:
        item.output.write_text(item.content, encoding="utf-8")
        print(f"wrote {rel(item.output)}")
    if left_over:
        print("WARNING: generated agents with no template (delete by hand):", file=sys.stderr)
        for orphan_path in left_over:
            print(f"    {rel(orphan_path)}", file=sys.stderr)
    return 0


# =============================================================================
# MAIN FUNCTION
# =============================================================================


def main(argv: list[str] | None = None) -> int:
    """Parse arguments and run the build against the real repository."""
    parser = argparse.ArgumentParser(
        description="Build .opencode/agents/ from templates by inlining {file:...} lines."
    )
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--check", action="store_true", help="exit 1 if any file is stale")
    mode.add_argument("--list", action="store_true", help="print template -> output + includes")
    args = parser.parse_args(argv)
    return build(
        ROOT,
        TEMPLATE_DIR,
        OUTPUT_DIR,
        check=args.check,
        show=args.show,
    )


# =============================================================================
# MAIN GUARD
# =============================================================================


if __name__ == "__main__":
    sys.exit(main())
