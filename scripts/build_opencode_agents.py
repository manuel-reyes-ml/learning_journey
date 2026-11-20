#!/usr/bin/env python3
"""Generate the BODY of each `.opencode/agents/*.md` from shared prompts and rules.

WHY THIS SCRIPT EXISTS
----------------------
OpenCode 2.x does **not** expand `{file:...}` inside a Markdown agent body. Probed
directly on 2026-11-18 (ADR-001 §14): `docs-sync`, launched as a real subagent and
told not to read any files, quoted both of its import lines back verbatim and could
name neither its own role nor its rule's globs. A non-empty body also *replaces*
OpenCode's base prompt, so every custom agent was running on `AGENTS.md` plus its
one-line description and nothing else. Permissions were unaffected: OpenCode
enforces them itself, so no agent gained any power, it just lost its instructions.

The config `instructions` list *does* load (same probe day), but it applies to every
agent, so it cannot carry a rule that belongs to one agent. The text has to be in
the agent file itself — hence generation.

ONE FILE PER AGENT, TWO OWNERS
------------------------------
Each agent file has a hand-edited top and a generated bottom:

  .opencode/agents/<name>.md
    ---
    frontmatter            <- YOU edit this (model, mode, permissions). It is the
    ---                       only copy of these settings; the script never changes it.
    <!-- GENERATED ... -->
    body                   <- this script writes everything below the frontmatter

  Body sources, in order:
    OpenCode-only note  ->  .github/docs/prompts/agents/<name>.opencode-delta.md  (optional)
    Specialist rules    ->  .cursor/rules/<rule>.mdc, routed by the RULES table below
    Instructions        ->  .github/docs/prompts/agents/<name>.md  (shared with Claude)

This mirrors `build_claude_agents.py`: same shared prompts, same `-delta.md` idea,
same `--check`. The one difference is where settings live. Claude's frontmatter is a
few lines, so it sits in that script's table; OpenCode's permission arrays are long
YAML, so they stay in the agent file where OpenCode's own docs and examples apply.

Fails closed: a missing agent file, frontmatter, rule or prompt, or an empty source,
stops the build and nothing is written. (OpenCode would turn a missing `{file:...}`
into an empty string without a word.)

Usage:
    python3 scripts/build_opencode_agents.py            # rewrite the bodies
    python3 scripts/build_opencode_agents.py --check    # fail if any body is stale (CI, pre-commit)
    python3 scripts/build_opencode_agents.py --list     # show each agent and its sources
"""

# =============================================================================
# IMPORTS
# =============================================================================

from __future__ import annotations

import argparse
import re
import sys
from collections.abc import Mapping
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
AGENTS_DIR: Final[Path] = ROOT / ".opencode" / "agents"
PROMPTS_DIR: Final[Path] = ROOT / ".github" / "docs" / "prompts" / "agents"
RULES_DIR: Final[Path] = ROOT / ".cursor" / "rules"

# Which specialist rules each agent carries. This is the per-agent equivalent of
# Cursor's glob scoping: a rule loads only when its agent runs. To add an agent,
# create `.opencode/agents/<name>.md` with frontmatter, write its instructions in
# `.github/docs/prompts/agents/<name>.md`, add a line here, then `make opencode-agents`.
RULES: Final[Mapping[str, tuple[str, ...]]] = {
    "docs-fix": ("architecture-docs", "git-workflow"),
    "docs-sync": ("architecture-docs",),
    "eval-guardian": ("testing-and-eval",),
    "learn": ("learning-mode",),
    "pattern-scout": ("ai-sdk-patterns",),
    "security-auditor": ("observability", "ai-sdk-patterns"),
}

# One marker string, used both to stamp bodies and to recognise them later, so the
# "generated but unlisted" check can never drift from the banner text.
GENERATED_MARK: Final[str] = "GENERATED BODY — DO NOT EDIT BELOW THE FRONTMATTER"

BANNER: Final[str] = (
    "<!-- " + GENERATED_MARK + ".\n"
    "     Edit the frontmatter above freely; it is the source for this agent's settings.\n"
    "     Edit the body at its sources, then run `make opencode-agents`:\n"
    "{sources}"
    "     OpenCode 2.x does not expand {{file:...}} in agent files (ADR-001 §14).\n"
    "-->\n"
)

# `---` + YAML + `---` at the very top of a file. DOTALL lets `.` cross newlines;
# the lazy `.*?` stops at the FIRST closing fence, not at a `---` rule in the body.
FRONTMATTER: Final[re.Pattern[str]] = re.compile(r"\A---\n(?P<yaml>.*?)\n---\n", re.DOTALL)

# A line that is only `{file:...}`: the import syntax OpenCode ignores in agent files.
# Used by the tests and the verifier to prove no generated body still relies on it.
INCLUDE_LINE: Final[re.Pattern[str]] = re.compile(r"^\{file:[^{}\s]+\}$")


class AgentBuildError(Exception):
    """An agent file or one of its sources cannot be rendered."""


@dataclass(frozen=True, slots=True, kw_only=True)
class Rendered:
    """One finished agent file, ready to be written or compared."""

    name: str
    path: Path
    content: str
    sources: tuple[Path, ...]


# =============================================================================
# HELPER FUNCTIONS
# =============================================================================


def split_frontmatter(text: str, where: str) -> tuple[str, str]:
    """Split a file into its YAML frontmatter and everything after it.

    Raises
    ------
    AgentBuildError
        If the file does not start with a `---` fenced block.
    """
    match = FRONTMATTER.match(text)
    if not match:
        raise AgentBuildError(f"{where}: must start with --- frontmatter")
    return match.group("yaml"), text[match.end() :]


def read_source(path: Path, *, strip_header: bool = False) -> str:
    """Read one body source, optionally dropping a Cursor frontmatter header.

    Cursor's `description:` / `globs:` / `alwaysApply:` steer Cursor's own loader;
    inside an OpenCode prompt they are noise, so rules lose their header.

    Raises
    ------
    AgentBuildError
        If the file is missing or has no text left.
    """
    if not path.is_file():
        raise AgentBuildError(f"source not found: {path}")
    text = path.read_text(encoding="utf-8")
    if strip_header and (match := FRONTMATTER.match(text)):
        text = text[match.end() :]
    text = text.strip()
    if not text:
        raise AgentBuildError(f"source is empty: {path}")
    return text


# =============================================================================
# CORE FUNCTIONS
# =============================================================================


def render(
    name: str,
    rules: tuple[str, ...],
    root: Path,
    agents_dir: Path,
    prompts_dir: Path,
    rules_dir: Path,
) -> Rendered:
    """Build one agent file: its own frontmatter, then a freshly generated body.

    Parameters
    ----------
    name : str
        Agent ID; also the file stem of the agent and of its shared prompt.
    rules : tuple[str, ...]
        Rule stems to inline from `rules_dir`, in order.
    root : Path
        Repository root, used for display paths in the banner.
    agents_dir, prompts_dir, rules_dir : Path
        Where agent files, shared prompts and Cursor rules live.

    Returns
    -------
    Rendered
        Path, full new content and the sources that went into the body.

    Raises
    ------
    AgentBuildError
        If the agent file, its frontmatter or any required source is missing or empty.
    """
    path = agents_dir / f"{name}.md"
    if not path.is_file():
        raise AgentBuildError(
            f"{name}: {path} not found - create it with frontmatter first, then rebuild"
        )
    # Only the frontmatter survives; whatever was below it is replaced. That is what
    # makes a hand edit to the body show up as drift in --check.
    frontmatter, _old_body = split_frontmatter(path.read_text(encoding="utf-8"), path.name)

    sources: list[Path] = []
    parts: list[str] = []

    delta = prompts_dir / f"{name}.opencode-delta.md"
    if delta.exists():
        parts.append(read_source(delta))
        sources.append(delta)

    for rule in rules:
        rule_path = rules_dir / f"{rule}.mdc"
        parts.append(read_source(rule_path, strip_header=True))
        sources.append(rule_path)

    shared = prompts_dir / f"{name}.md"
    parts.append(read_source(shared))
    sources.append(shared)

    shown = "".join(
        f"       {p.resolve().relative_to(root.resolve()).as_posix()}\n" for p in sources
    )
    content = (
        f"---\n{frontmatter}\n---\n"
        + BANNER.format(sources=shown)
        + "\n"
        + "\n\n".join(parts)
        + "\n"
    )
    return Rendered(
        name=name,
        path=path,
        content=content,
        sources=tuple(sources),
    )


def unlisted(routes: Mapping[str, tuple[str, ...]], agents_dir: Path) -> list[Path]:
    """Return agent files with a generated body but no entry in the routing table.

    Such a body can never be refreshed, so it would silently go stale. Agent files
    without the banner are hand-written and left alone.
    """
    if not agents_dir.is_dir():
        return []
    return [
        path
        for path in sorted(agents_dir.glob("*.md"))
        if path.stem not in routes and GENERATED_MARK in path.read_text(encoding="utf-8")
    ]


def build(
    root: Path,
    *,
    agents_dir: Path,
    prompts_dir: Path,
    rules_dir: Path,
    routes: Mapping[str, tuple[str, ...]],
    check: bool = False,
    show: bool = False,
) -> int:
    """Render every routed agent, then write, verify or list them.

    Returns
    -------
    int
        Process exit code: 0 on success, 1 on any error, stale body or unlisted agent.
    """
    # Render everything before writing anything: one broken source must not leave
    # half the agents regenerated and half stale.
    try:
        rendered = [
            render(name, rules, root, agents_dir, prompts_dir, rules_dir)
            for name, rules in sorted(routes.items())
        ]
    except AgentBuildError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        print("nothing was written", file=sys.stderr)
        return 1

    def rel(path: Path) -> str:
        return path.resolve().relative_to(root.resolve()).as_posix()

    if show:
        for item in rendered:
            print(rel(item.path))
            for source in item.sources:
                print(f"    + {rel(source)}")
        return 0

    stray = unlisted(routes, agents_dir)

    if check:
        stale = [rel(r.path) for r in rendered if r.path.read_text(encoding="utf-8") != r.content]
        if stale:
            print("STALE - run `make opencode-agents`:", file=sys.stderr)
            for stale_path in stale:
                print(f"  {stale_path}", file=sys.stderr)
        if stray:
            print(
                "UNLISTED - generated body but no RULES entry in build_opencode_agents.py:",
                file=sys.stderr,
            )
            for stray_path in stray:
                print(f"  {rel(stray_path)}", file=sys.stderr)
        if stale or stray:
            return 1
        print("all generated OpenCode agent bodies are up to date")
        return 0

    for item in rendered:
        item.path.write_text(item.content, encoding="utf-8")
        print(f"wrote {rel(item.path)}")
    if stray:
        print("WARNING: generated bodies with no RULES entry (add one or delete):", file=sys.stderr)
        for stray_path in stray:
            print(f"  {rel(stray_path)}", file=sys.stderr)
    return 0


# =============================================================================
# MAIN FUNCTION
# =============================================================================


def main(argv: list[str] | None = None) -> int:
    """Parse arguments and run the build against the real repository."""
    parser = argparse.ArgumentParser(
        description="Generate .opencode/agents/ bodies from shared prompts and Cursor rules."
    )
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--check", action="store_true", help="exit 1 if any body is stale")
    mode.add_argument("--list", action="store_true", help="print each agent and its sources")
    args = parser.parse_args(argv)
    return build(
        ROOT,
        agents_dir=AGENTS_DIR,
        prompts_dir=PROMPTS_DIR,
        rules_dir=RULES_DIR,
        routes=RULES,
        check=args.check,
        show=args.list,
    )


# =============================================================================
# MAIN GUARD
# =============================================================================


if __name__ == "__main__":
    sys.exit(main())
