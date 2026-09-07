#!/usr/bin/env bash
# ---------------------------------------------------------------------------
# task_brief_context.sh — context loader for /task-brief. Read-only. ADR-0001.
#
# Emits ISSUE_NUMBER as its first line. The shared body reads the Issue number
# from that line rather than from `$1`, because argument substitution differs
# per harness: `$1` interpolates on OpenCode and is literal in a Claude Code
# skill body (ADR-0006). The number enters here, through the invocation.
# ---------------------------------------------------------------------------
set -uo pipefail

ISSUE="${1:-}"
TEMPLATE=".github/docs/templates/task_brief.md"
PLAN=".github/plans/issue-${ISSUE}-task-brief.md"

echo "===== ISSUE NUMBER ====="
if [[ -z "$ISSUE" ]]; then
  echo "CONTEXT_ERROR: no Issue number was passed. STOP and report."
  echo "===== END CONTEXT ====="
  exit 0
fi
echo "ISSUE_NUMBER=${ISSUE}"
echo

echo "===== BRIEF TEMPLATE (authoritative structure) ====="
if [[ -r "$TEMPLATE" ]]; then cat "$TEMPLATE"
else echo "CONTEXT_ERROR: template not readable at ${TEMPLATE}. STOP and report."; fi

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