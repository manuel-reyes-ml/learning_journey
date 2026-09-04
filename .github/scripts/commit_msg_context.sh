#!/usr/bin/env bash
# commit_msg_context.sh — context loader for /commit-msg. Read-only. See ADR-0001.
set -uo pipefail
echo "===== STAGED DIFF (full) ====="
staged=$(git diff --staged 2>&1)
if [[ -z "${staged// }" ]]; then
  echo "CONTEXT_ERROR: nothing is staged. STOP and report — do not write a message."
else
  echo "$staged"
fi
echo
echo "===== STAGED FILE SUMMARY ====="
git diff --staged --stat 2>&1
echo
echo "===== ADRs STAGED IN THIS COMMIT ====="
git diff --staged --name-only -- docs/adr 2>/dev/null || true
echo
echo "===== RECENT COMMIT SUBJECTS (style reference) ====="
git log --oneline -10 2>&1 || echo "(no history)"
echo
echo "===== END CONTEXT ====="
