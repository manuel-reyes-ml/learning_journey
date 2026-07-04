#!/usr/bin/env bash
# =====================================================================
# setup-labels.sh — idempotent GitHub label setup (universal core + packs)
#
# WHAT IT DOES
#   Creates a consistent label taxonomy on a repo via the gh CLI. Re-runnable:
#   `--force` updates an existing label in place instead of failing, so this is
#   safe to run as many times as you like. Additive by default — the only
#   destructive part (prune) is commented out and must be opted into deliberately.
#
# USAGE
#   chmod +x setup-labels.sh
#   ./setup-labels.sh                 # applies to the current repo
#   ./setup-labels.sh owner/repo      # applies to a specific repo
#
# REQUIRES
#   gh (authenticated — check with `gh auth status`)
#
# HOW AN AGENT SHOULD USE THIS
#   1) Run the audit (read-only) to see existing labels.
#   2) Keep the UNIVERSAL CORE as-is.
#   3) Uncomment ONLY the packs this repo needs (DE / ML / LLM-RAG / Agentic /
#      domain). Packs mirror the issue/PR/task-brief/checklist vocabulary.
#   4) Run the script. Then run the VERIFY step and report the label list.
#   Do NOT enable the PRUNE section without explicit human approval.
# =====================================================================

set -euo pipefail

REPO="${1:-$(gh repo view --json nameWithOwner -q .nameWithOwner)}"
echo "▶ Target repo: $REPO"

mklabel() {  # $1=name  $2=color(hex, no #)  $3=description
  gh label create "$1" --color "$2" --description "$3" --force --repo "$REPO"
}

# ── AUDIT (read-only) — see what's there before changing anything ─────
echo "▶ Existing labels:"
gh label list --repo "$REPO" || true

# =====================================================================
# UNIVERSAL CORE  (every repo gets these — keep consistent everywhere)
# =====================================================================

# type: — blue family
mklabel "type: feature"  "0075CA" "New functionality"
mklabel "type: bug"      "D73A4A" "Defect or incorrect behavior"
mklabel "type: docs"     "0052CC" "Documentation updates"
mklabel "type: test"     "5319E7" "Tests / coverage"
mklabel "type: refactor" "006B75" "Refactor without behavior change"
mklabel "type: chore"    "BFD4F2" "Tooling / deps / maintenance"

# priority: — red→amber gradient
mklabel "priority: P0" "B60205" "Urgent / blocking"
mklabel "priority: P1" "D93F0B" "High priority"
mklabel "priority: P2" "FBCA04" "Normal priority"

# status: — green family (apply one at a time)
mklabel "status: in progress"  "0E8A16" "Actively being worked"
mklabel "status: needs review" "C2E0C6" "Ready for review"
mklabel "status: blocked"      "006B29" "Waiting on a dependency"

# area: — neutral family (generic areas useful in any repo)
mklabel "area: config"    "C5DEF5" "Config / schema mappings"
mklabel "area: notebooks" "FEF2C0" "Notebooks / walkthroughs"
mklabel "area: data-viz"  "D2DAE1" "Plots / KPIs / dashboards"
mklabel "area: ci"        "D4C5F9" "CI/CD / GitHub Actions"

# =====================================================================
# PROJECT PACKS  — uncomment the ones a given repo needs
# (Same vocabulary as your issue/PR/task-brief/checklist packs.)
# =====================================================================

# ── DE pack ──────────────────────────────────────────────────────────
# mklabel "area: pipeline"     "1D76DB" "Ingestion / ETL / orchestration"
# mklabel "area: schema"       "0052CC" "Canonical schema / contracts"
# mklabel "area: data-quality" "0E8A16" "Validation / nulls / dedupe / idempotence"
# mklabel "area: export"       "C5DEF5" "Output / correction-template export"

# ── ML pack ──────────────────────────────────────────────────────────
# mklabel "area: model"      "5319E7" "Model code / training"
# mklabel "area: eval"       "8256D0" "Metrics / thresholds / regression gates"
# mklabel "area: experiment" "A371F7" "Experiment tracking / runs"
# mklabel "area: dataset"    "D4C5F9" "Datasets / splits / versioning"

# ── LLM / RAG pack ───────────────────────────────────────────────────
# mklabel "area: retrieval"  "006B75" "Chunking / embeddings / vector-graph store"
# mklabel "area: prompts"    "0075CA" "Prompt versioning / templates"
# mklabel "area: eval"       "8256D0" "DeepEval / RAGAS / GEval gates"
# mklabel "area: cost"       "FBCA04" "Token / latency / spend budget"
# mklabel "area: guardrails" "D73A4A" "PII / injection / output validation"

# ── Agentic pack (+ safety) ──────────────────────────────────────────
# mklabel "area: agent-loop"    "006B75" "Loop / planning / tool orchestration"
# mklabel "area: tools"         "C5DEF5" "Tool integrations / MCP"
# mklabel "area: observability" "D4C5F9" "Tracing / audit logs"
# mklabel "safety: human-gate"  "B60205" "Requires human sign-off before action"
# mklabel "safety: kill-switch" "B60205" "Touches the kill-switch / live path"

# ── Domain pack — EXAMPLE: 1099 reconciliation pipeline (your original) ─
# mklabel "engine: A-reconcile"    "0366D6" "Relius <-> Matrix reconciliation engine"
# mklabel "engine: B-age"          "0366D6" "Age-based tax code engine"
# mklabel "engine: C-roth-taxable" "0366D6" "Roth taxable + basis engine"
# mklabel "engine: D-ira-rollover" "0366D6" "IRA rollover engine"

# =====================================================================
# OPTIONAL PRUNE  (DESTRUCTIVE — leave commented unless approved)
# Removes GitHub's noisy default labels that don't fit this workflow.
# Deleting a label removes it from any issues/PRs it was on.
# =====================================================================
# for l in "duplicate" "invalid" "question" "wontfix" \
#          "good first issue" "help wanted" "enhancement" "documentation" "bug"; do
#   gh label delete "$l" --repo "$REPO" --yes 2>/dev/null || true
# done

# ── VERIFY ───────────────────────────────────────────────────────────
echo "✓ Done. Current labels:"
gh label list --repo "$REPO"
