#!/usr/bin/env bash
# draft_issue_context.sh — context loader for /draft-issue. Read-only. See ADR-0001.
set -uo pipefail
emit() { # emit <label> <path> <blocking:yes|no>
  echo "===== $1 ====="
  if [[ -r "$2" ]]; then cat "$2"
  elif [[ "$3" == "yes" ]]; then echo "CONTEXT_ERROR: $2 not readable. STOP and report."
  else echo "(not present: $2)"; fi
  echo
}
emit "ISSUE TEMPLATE (authoritative structure)" ".github/ISSUE_TEMPLATE/task.md" yes
emit "APPROVED LABELS (the ONLY permitted label source)" ".github/docs/project_labels.md" yes

echo "===== REPOSITORY MODULES ====="
find src -name '*.py' 2>/dev/null | head -100 || echo "(no src/ yet)"
echo
echo "===== EXISTING DECISION RECORDS ====="
ls docs/adr 2>/dev/null || echo "no docs/adr yet"
echo
echo "===== OPEN ISSUES (avoid duplicates) ====="
gh issue list --state open --limit 30 2>&1 || echo "(gh issue list unavailable)"
echo
echo "===== END CONTEXT ====="
