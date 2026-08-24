"""
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

