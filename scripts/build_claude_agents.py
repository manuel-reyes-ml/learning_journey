#!/usr/bin/env python3
"""Build `.claude/agents/*.md` and `.claude/output-styles/learn.md` from shared prompts.

WHY THIS SCRIPT EXISTS
----------------------
Claude Code subagent files have no import mechanism. The markdown body *is* the
system prompt, parsed once, and `@path` does not expand there (open requests
anthropics/claude-code#5914 and #6899). OpenCode agents *do* support `{file:...}`.

So agents cannot share a body by reference the way commands can. They share it by
**generation** instead — the same shape as `architecture.dsl` → Mermaid via
`make diagrams`: one model source, rendered out to a committed artifact that is
never hand-edited.

  Instructions  →  .github/docs/prompts/agents/<name>.md          (edit this)
  Claude-only   →  .github/docs/prompts/agents/<name>.claude-delta.md  (optional)
  Settings      →  the AGENTS table below                          (edit this)
  Output        →  .claude/agents/<name>.md                        (never edit)

Usage:
    python3 scripts/build_claude_agents.py            # write the files
    python3 scripts/build_claude_agents.py --check    # fail if out of date (CI)
"""

# =============================================================================
# IMPORTS
# =============================================================================

from __future__ import annotations

import argparse
import sys

from pathlib import Path
from typing import Final

# =============================================================================
# MODULE CONFIGURATION
# =============================================================================
# =====================================================
# Constants
# =====================================================

ROOT: Final[Path] = Path(__file__).resolve().parent.parent
PROMPTS: Final[Path] = ROOT / ".github" / "docs" / "prompts" / "agents"
AGENTS_OUT: Final[Path] = ROOT / ".claude" / "agents"
STYLES_OUT: Final[Path] = ROOT / ".claude" / "output-styles"

BANNER: Final[str] = (
    "<!-- GENERATED FILE — DO NOT EDIT.\n"
    "     Body:     .github/docs/prompts/agents/{name}.md\n"
    "     Settings: scripts/build_claude_agents.py\n"
    "     Rebuild:  make claude-agents\n"
    "-->\n"
)

AGENTS: Final[dict[str, tuple[str, str]]] = {
    "security-auditor": (
        "agent",
        """name: security-auditor
description: Audits for hardcoded secrets, exposed PII, unsafe logging and config, and data-boundary violations. Read-only. Use before staging any change on finance-adjacent work.
tools: Read, Grep, Glob, Bash
disallowedTools: Edit, Write, NotebookEdit, WebFetch, WebSearch
model: sonnet
permissionMode: plan""",
    ),
    "eval-guardian": (
        "agent",
        """name: eval-guardian
description: Runs the AI evaluation suite and reports scores against thresholds — RAG, agentic and GEval, with the raised bar for AFC and Crucible. Read and eval commands only, no edits.
tools: Read, Grep, Glob, Bash
disallowedTools: Edit, Write, NotebookEdit, WebFetch, WebSearch
model: sonnet
permissionMode: plan""",
    ),
    "pattern-scout": (
        "agent",
        """name: pattern-scout
description: Scouts current production-grade patterns and compares them to this codebase. Read-only, can fetch docs and the web. Use to find better or newer approaches.
tools: Read, Grep, Glob, Bash, WebFetch, WebSearch
disallowedTools: Edit, Write, NotebookEdit
model: opus
permissionMode: plan""",
    ),
    "docs-sync": (
        "agent",
        """name: docs-sync
description: Reviews documentation against the actual codebase to find drift, including ADRs, C4 diagrams and README structure. Read-only, reports but never edits.
tools: Read, Grep, Glob, Bash
disallowedTools: Edit, Write, NotebookEdit, WebFetch, WebSearch
model: sonnet
permissionMode: plan""",
    ),
    "docs-fix": (
        "agent",
        """name: docs-fix
description: Updates documentation files directly — markdown, README, CHANGELOG, docs/. Edits docs only, never code, never ADRs, never generated diagrams. The writable counterpart to docs-sync.
tools: Read, Grep, Glob, Bash, Edit, Write
disallowedTools: WebFetch, WebSearch
model: sonnet
hooks:
  PreToolUse:
    - matcher: "*"
      hooks:
        - type: command
          command: python3 "${CLAUDE_PROJECT_DIR}/.claude/hooks/guard.py" docs-only
          timeout: 15""",
    ),
    "learn": (
        "style",
        """name: Learn
description: Teaching pair-programmer for Stage 1 — explains concepts, patterns and tradeoffs; never writes production code for me.
keep-coding-instructions: true""",
    ),
}


# =============================================================================
# CORE FUNCTION
# =============================================================================

def render(name: str) -> tuple[Path, str]:
    """Assemble one output file from its frontmatter, shared body and optional delta."""
    kind, frontmatter = AGENTS[name]
    body = (PROMPTS / f"{name}.md").read_text(encoding="utf-8").rstrip()

    delta_path = PROMPTS / f"{name}.claude-delta.md"
    delta = delta_path.read_text(encoding="utf-8").strip() if delta_path.exists() else ""

    parts = [f"---\n{frontmatter}\n---\n", BANNER.format(name=name)]
    if delta:
        parts.append("\n" + delta + "\n")
    parts.append("\n" + body + "\n")

    out_dir = AGENTS_OUT if kind == "agent" else STYLES_OUT
    return out_dir / f"{name}.md", "".join(parts)


# =============================================================================
# MAIN FUNCTION
# =============================================================================

def main(argv: list[str] | None = None) -> int:
    """Write or verify every generated agent file."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", help="exit 1 if any file is stale")
    args = parser.parse_args(argv)

    AGENTS_OUT.mkdir(parents=True, exist_ok=True)
    STYLES_OUT.mkdir(parents=True, exist_ok=True)

    stale: list[str] = []
    for name in AGENTS:
        path, content = render(name)
        if args.check:
            current = path.read_text(encoding="utf-8") if path.exists() else ""
            if current != content:
                stale.append(str(path.relative_to(ROOT)))
        else:
            path.write_text(content, encoding="utf-8")
            print(f"wrote {path.relative_to(ROOT)}")
    
    if args.check:
        if stale:
            print("STALE - run 'make claude-agents' :", file=sys.stderr)
            for s in stale:
                print(f"  {s}", file=sys.stderr)
            return 1
        print("all generated agent files are up to date")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())


# .relative.to(other=)
# p = Path("/Users/manuel/repo/.claude/agents/docs-fix.md")
# p.relative_to("/Users/manuel/repo")
# PosixPath('.claude/agents/docs-fix.md')
# It strips a prefix off a path and gives you what's left. Returns a Path object, not a string.
# It raises ValueError if the prefix doesn't match:
#   Path("/etc/hosts").relative_to("/Users/manuel")
#   ValueError: '/etc/hosts' is not in the subpath of '/Users/manuel'
#
# That's actually useful — it's a cheap way to assert a path is inside a directory you expect.
# Since Python 3.12 you can pass walk_up=True to get ../.. style results instead of an error.