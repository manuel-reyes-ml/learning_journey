#!/usr/bin/env bash
# labels_run.sh — the ONE side-effecting command script in the set.
#
# Named `_run`, not `_context`, so the exception is visible at the call site.
# It creates/updates GitHub labels and regenerates the reference doc. Per
# ADR-0003 the agent permission map does NOT gate this — review is the gate.
set -uo pipefail
TARGET="${1:-}"
echo "===== TARGET REPO ====="
if [[ -n "$TARGET" ]]; then echo "$TARGET (explicit argument)"
else gh repo view --json nameWithOwner -q .nameWithOwner 2>&1 || echo "CONTEXT_ERROR: could not resolve current repo. STOP and report."; fi
echo
echo "===== SETUP SCRIPT RUN (creates/updates labels) ====="
if [[ -x .github/scripts/setup-labels.sh || -r .github/scripts/setup-labels.sh ]]; then
  bash .github/scripts/setup-labels.sh "$TARGET" 2>&1 || echo "(setup-labels.sh exited non-zero — report the error above)"
else
  echo "CONTEXT_ERROR: .github/scripts/setup-labels.sh not found. STOP and report."
fi
echo
echo "===== LABELS NOW ON THE REPO ====="
gh label list --limit 100 2>&1 || echo "(gh label list unavailable)"
echo
echo "===== REGENERATED REFERENCE (first 25 lines) ====="
head -25 .github/docs/project_labels.md 2>/dev/null \
  || echo "CONTEXT_ERROR: .github/docs/project_labels.md was not regenerated. STOP and report."
echo
echo "===== END CONTEXT ====="
