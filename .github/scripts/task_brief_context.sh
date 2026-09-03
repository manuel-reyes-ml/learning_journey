#!/usr/bin/env bash
# ---------------------------------------------------------------------------
# task_brief_context.sh — context loader for the /task-brief command.
#
# WHY THIS FILE EXISTS
#   Command-template `!` injection is SINGLE-PASS on both harnesses. A `!` block
#   inside an imported prompt body arrives as literal text and never executes
#   (verified: OpenCode 1.17.9, probe v4 — level-2 marker file was never created).
#   So all shell for this command must run at level 1, in the wrapper.
#
#   Duplicating six `!` lines across the OpenCode and Claude Code wrappers would
#   be drift. This script is the single source instead: each wrapper calls it
#   once, and the shared prompt body stays instructions-only.
#
# CONTRACT
#   $1 = GitHub Issue number. Emits context to stdout. Never writes, never fails
#   the command — a missing input is reported inline so the agent can STOP.
# ---------------------------------------------------------------------------
set -uo pipefail

ISSUE="${1:-}"
TEMPLATE=".github/docs/templates/task_brief.md"
PLAN=".github/plans/issue-${ISSUE}-task-brief.md"

if [[ -z "$ISSUE" ]]; then
  echo "CONTEXT_ERROR: no Issue number was passed. STOP and report."
  exit 0
fi

echo "===== BRIEF TEMPLATE (authoritative structure) ====="
if [[ -r "$TEMPLATE" ]]; then
  cat "$TEMPLATE"
else
  echo "CONTEXT_ERROR: template not readable at ${TEMPLATE}. STOP and report."
fi

echo
echo "===== ISSUE #${ISSUE} ====="
gh issue view "$ISSUE" 2>&1 || echo "CONTEXT_ERROR: gh issue view failed. STOP and report."

echo
echo "===== ISSUE REVISION STAMP ====="
gh issue view "$ISSUE" --json updatedAt --jq .updatedAt 2>&1 \
  || echo "CONTEXT_ERROR: revision stamp unavailable."

echo
echo "===== MODULES IN SCOPE ====="
find src tests -name '*.py' 2>/dev/null | head -100 || echo "(no src/ or tests/ yet)"

echo
echo "===== EXISTING DECISION RECORDS ====="
ls docs/adr 2>/dev/null || echo "no docs/adr yet"

echo
echo "===== PRIOR BRIEF FOR THIS ISSUE ====="
cat "$PLAN" 2>/dev/null || echo "no prior brief"

echo
echo "===== END CONTEXT ====="
