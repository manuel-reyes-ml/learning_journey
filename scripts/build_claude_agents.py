"""
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


