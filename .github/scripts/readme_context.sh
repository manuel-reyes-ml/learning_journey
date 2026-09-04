#!/usr/bin/env bash
# readme_context.sh — context loader for /readme. Read-only. See ADR-0001.
#
# NOTE: architecture-docs.mdc is deliberately NOT loaded here. It is a Cursor
# rule; on OpenCode the specialist route lives in the docs-sync agent, and on
# neither harness does this command need a second copy. See ADR-0001.
set -uo pipefail
emit() {
  echo "===== $1 ====="
  if [[ -r "$2" ]]; then cat "$2"
  elif [[ "$3" == "yes" ]]; then echo "CONTEXT_ERROR: $2 not readable. STOP and report."
  else echo "(not present: $2)"; fi
  echo
}
emit "README TEMPLATE (authoritative structure)" ".github/docs/templates/README_template.md" yes
emit "FLAGSHIP CHECKLIST (the bar)"              ".github/docs/FLAGSHIP_CHECKLIST.md"        yes
emit "MODEL CARD TEMPLATE (only if repo trains a model)" ".github/docs/templates/MODEL_CARD.md" no

echo "===== PYPROJECT ====="
head -60 pyproject.toml 2>/dev/null || echo "CONTEXT_ERROR: no pyproject.toml. STOP and report."
echo
echo "===== SOURCE MODULES ====="
find src -name '*.py' 2>/dev/null | head -60 || echo "(no src/ yet)"
echo
echo "===== DECISION RECORDS ====="
ls docs/adr 2>/dev/null || echo "no docs/adr yet"
echo
echo "===== ARCHITECTURE DSL / DIAGRAMS ====="
ls architecture.dsl docs/diagrams 2>/dev/null || echo "(no architecture.dsl or docs/diagrams — flag against the standard)"
echo
echo "===== CI WORKFLOWS (for badge and gate claims) ====="
ls .github/workflows/ 2>/dev/null || echo "(no workflows — a badge would be a vanity badge)"
echo
echo "===== EVAL SUITE PRESENT? ====="
ls tests/test_eval.py 2>/dev/null || echo "(no eval suite — omit the evaluation table)"
echo
echo "===== RECENT HISTORY ====="
git log --oneline -15 2>&1 || echo "(no history)"
echo
echo "===== REPO ROOT ====="
ls -1 2>&1
echo
echo "===== END CONTEXT ====="
