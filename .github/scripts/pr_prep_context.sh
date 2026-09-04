#!/usr/bin/env bash
# pr_prep_context.sh — context loader for /pr-prep. Read-only. See ADR-0001.
set -uo pipefail
BASE="${1:-main}"
emit() {
  echo "===== $1 ====="
  if [[ -r "$2" ]]; then cat "$2"
  elif [[ "$3" == "yes" ]]; then echo "CONTEXT_ERROR: $2 not readable. STOP and report."
  else echo "(not present: $2)"; fi
  echo
}
emit "PR TEMPLATE (authoritative structure)" ".github/pull_request_template.md" yes
emit "APPROVED LABELS (the ONLY permitted label source)" ".github/docs/project_labels.md" yes

echo "===== BRANCH ====="
git rev-parse --abbrev-ref HEAD 2>&1
echo
echo "===== CHANGE SUMMARY vs ${BASE} ====="
git diff "${BASE}...HEAD" --stat 2>&1 || echo "CONTEXT_ERROR: git diff vs ${BASE} failed. STOP and report."
echo
echo "===== COMMITS ON THIS BRANCH ====="
git log "${BASE}..HEAD" --oneline 2>&1
echo
echo "===== COMMIT FOOTERS (for Closes #NN) ====="
git log "${BASE}..HEAD" --format='%b' 2>/dev/null | grep -iE '^(refs|closes|fixes)' || echo "(no Refs/Closes footer found — flag the missing Issue link)"
echo
echo "===== ADR / ARCHITECTURE CHANGES ON THIS BRANCH ====="
git diff "${BASE}...HEAD" --name-only -- docs/adr architecture.dsl docs/diagrams README.md 2>&1 \
  || echo "(none)"
echo
echo "===== TASK BRIEF FOR THIS BRANCH (pack cross-check) ====="
cat .github/plans/*task-brief.md 2>/dev/null | head -60 || echo "(no brief found in .github/plans/)"
echo
echo "===== END CONTEXT ====="
