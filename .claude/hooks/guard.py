#!/usr/bin/env python3
"""PreToolUse gate for Claude Code.

Why this file exists
--------------------
Instruction files (CLAUDE.md, AGENTS.md, agent bodies) are *context*: Claude reads
them and tries to comply. `permissions.deny` is *configuration*, and has a documented
history of non-enforcement for Read/Edit in some releases. A PreToolUse hook is the
only layer that fires before the permission-mode check and holds even under
`bypassPermissions` / `--dangerously-skip-permissions`.

This is CORRECTION 39 §11 restated one layer down: a prohibition in a prompt is
persuasion, a permission is configuration, a hook is architecture.

Contract: read the event JSON on stdin, exit 0 to allow, exit 2 to block with the
reason on stderr. Exit 2 is used rather than `permissionDecision: "deny"` JSON
because the combined form has an open non-enforcement report; exit 2 blocks
unconditionally.

Usage:
    python3 .claude/hooks/guard.py            # global profile
    python3 .claude/hooks/guard.py docs-only  # scoped: docs-fix subagent
"""

# =============================================================================
# IMPORTS
# =============================================================================

from __future__ import annotations

import json
import re
import sys

from fnmatch import fnmatch
from typing import Final

# =============================================================================
# MODULE CONFIGURATION
# =============================================================================
# =====================================================
# Constants
# =====================================================

# Set by the caller: `guard.py` (global) or `guard.py docs-only` (the docs-fix
# subagent). Claude Code has no per-subagent path permissions — `permissions` in
# settings.json is project-global — so a scoped hook is the only way to give one
# agent a narrower write surface than the rest.
PROFILE: Final[str] = sys.argv[1] if len(sys.argv) > 1 else "global"

# --- git verbs the human owns, never the agent (AGENTS.md commit gate) -----------
FORBIDDEN_GIT: Final[tuple[str, ...]] = (
    "commit", "push", "reset --hard", "rebase", "cherry-pick",
    "tag", "clean -fd", "filter-branch",
)
FORBIDDEN_CMDS: Final[tuple[str, ...]] = (
    r"\bgh\s+pr\s+(create|merge)\b",
    r"\bgh\s+issue\s+create\b",
    r"\bgh\s+release\s+create\b",
    r"\bsudo\b",
    r"\brm\s+-rf\b",
    r"\bpip\s+install\b",   # the standard is uv; pip is retired
    r"\bblack\b",           # retired in favour of ruff format
)

# --- paths that must never be read (proprietary / secrets / source-of-truth) -----
DENY_READ: Final[tuple[str, ...]] = (
    "*.env", "*.env.*", "**/.env", "**/.env.*",
    "**/data/raw/**", "**/data/processed/**", "**/data/outputs/**",
    "**/credentials*", "**/*.pem", "**/*.key",
    "**/roadmap.html",
)

# --- paths that must never be written --------------------------------------------
DENY_WRITE: Final[tuple[str, ...]] = DENY_READ + (
    "**/docs/adr/**",        # immutable once accepted: supersede, never rewrite
    "**/architecture.dsl",   # single Structurizr model source
    "**/docs/diagrams/**",   # generated exports: `make diagrams`
    "**/uv.lock",            # regenerate with `uv lock`, never hand-edit
)

# --- docs-only profile: the writable surface for the docs-fix subagent ------------
DOCS_ALLOW: Final[tuple[str, ...]] = ("*.md", "**/*.md", "*.mdx", "**/*.mdx", "**/docs/**")
DOCS_EXTRA_DENY: Final[tuple[str, ...]] = ("**/.github/**", "**/.opencode/**", "**/.cursor/**", "**/.claude/**")

WRITE_TOOLS: Final[set[str]] = {"Edit", "Write", "NotebookEdit", "MultiEdit"}
READ_TOOLS: Final[set[str]]= {"Read", "NotebookRead"}


# =============================================================================
# CORE FUNCTIONS
# =============================================================================

def block(reason: str) -> None:
    """Block the tool call and hand the reason back to Claude as the error."""
    # stderr, NOT print(). `print()` writes to stdout, which Claude Code parses
    # as structured JSON — a prose message there is at best ignored, at worst
    # confuses the parser. The block itself still lands (exit 2 does that), but
    # Claude would be refused with no idea why and would likely just retry.
    print(f"BlOCKED by .claude/hooks/guard.py - {reason}", file=sys.stderr)
    sys.exit(2)


def normalise(cmd: str) -> str:
    """Collapse the documented bypasses before pattern-matching.

    `git -C /path commit` and `git -c user.name=x commit` are functionally
    `git commit` but slip past naive substring matching — a real reported escape.
    Strip those, and flatten `cd /path && git commit` chains, before testing.
    """
    cmd = " ".join(cmd.split())

    # re.sub(pattern, replacement, string)
    # "Find every place pattern matches, swap in replacement, hand me back a new string."
    # 1. It returns a new string. Python strings are immutable, so nothing is modified in place.
    #    You must assign the result — re.sub(...) on its own line does nothing.
    # 2. It replaces all matches by default, not just the first. Pass count=1 to limit it.
    # 3. If nothing matches, you get the original string back. No error, no None. Silent no-op.
    #
    # \b        word boundary — matches `git`, not `legit` or `gitlab`
    # \s+       one or more whitespace
    # (?: ... ) group the alternatives WITHOUT capturing them
    # \S+       the path or key=value that follows the flag
    # +         the whole group, repeated — catches stacked flags
    cmd = re.sub(r"\bgit\s+(?:-C\s+\S+\s+|-c\s+\S+\s+)+", "git ", cmd)

    # Empty replacement string = delete. `cd /tmp && git push` -> `git push`.
    cmd = re.sub(r"\bcd\s+\S+\s*&&\s*", "", cmd)
    return cmd


def matches(path: str, patterns: tuple[str, ...]) -> bool:
    """True if `path` matches any glob in `patterns`."""
    return any(fnmatch(path, p) for p in patterns)


# =============================================================================
# MAIN FUNCTION
# =============================================================================

def main() -> None:
    """Inspect one PreToolUse event and allow or block it."""
    try:
    # Claude Code pipes the event in as JSON on stdin — no arguments. Because
    # stdin is a slot the caller wires up, `make claude-verify` can feed the same
    # bytes with `echo` and exercise the exact production path, not a mock.
    #
    # `sys.stdin` is a file object, so `json.load()` reads it directly
    # (`json.loads()` is the string form). A JSON object becomes a dict, so
    # `event["tool_name"]` is an ordinary dict lookup.
    #
    # DECISION: fail OPEN on malformed input. Exit 0 means "allow, no opinion".
    # Failing closed would block every tool call over one bad byte, and a hook
    # that crashes protects nothing. The alternative — fail closed — is stricter
    # but can lock you out of your own session. Revisit if this ever fires.
        event = json.load(sys.stdin)
    except (json.JSONDecodeError, ValueError):
        sys.exit(0)

    tool = event.get("tool_name", "")
    data = event.get("tool_input") or {}

    if tool == "Bash":
        cmd = normalise(str(data.get("command", "")))
        for verb in FORBIDDEN_GIT:
            if re.search(rf"\bgit\s+{re.escape(verb)}\b", cmd):
                block(
                    f"`git {verb}` is human-controlled. Stage with `git add` if asked, "
                    "then report the diff and stop. I commit manually after review."
                )
        for pattern in FORBIDDEN_CMDS:
            if re.search(pattern, cmd):
                block(
                   f"command matches a prohibited pattern ({pattern}). "
                    "Report what you would run and why; I execute it." 
                )
        sys.exit(0)

    path = str(data.get("file_path") or data.get("notebook_path") or "")
    if not path:
        sys.exit(0)

    if tool in READ_TOOLS and matches(path, DENY_READ):
        block(
            f"{path} is immutable or generated. Propose the change and hand it "
            "to me — ADRs are superseded not rewritten, diagrams are regenerated."
        )
    if PROFILE == "docs-only":
        if matches(path, DOCS_EXTRA_DENY):
            block(f"{path} is config/tooling, not a doc describing code.")
        if not matches(path, DOCS_ALLOW):
            block(
                f"{path} is not a documentation file. This agent edits docs only; "
                "report the exact change and hand it to Build mode."  
            )

    sys.exit(0)


if __name__ == "__main__":
    main()