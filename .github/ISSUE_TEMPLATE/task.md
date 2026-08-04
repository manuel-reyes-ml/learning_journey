---
name: "🧭 Execution Plan (task / feature / fix)"
about: "Production-grade work item: core plan + capability packs (DE/ML/LLM/Agentic)"
title: "[<area>] <concise outcome>"
labels: []
assignees: ""
---

<!--
 Fill the CORE (always). Tick the packs this work touches under "Packs in scope",
 then expand + fill ONLY those packs at the bottom and delete the rest.
 The packs you tick here should match the ones in the Cursor task brief and the PR.
 Standards source: AGENTS.md + .cursor/rules/. Roadmap v10.0.
-->

## 🎯 Objective
- **Problem this solves:**
- **Expected deliverable / output:**

**Packs in scope**
- [ ] 🟦 DE — Data Engineering
- [ ] 🟩 ML — Classical / Deep ML
- [ ] 🟪 LLM / RAG
- [ ] 🟧 Agentic
- [ ] ⬜ None (core only)
---
## 📌 Scope
**In scope**
- [ ] …

**Out of scope**
- …
---
## 🧩 Implementation Plan
**Files to change / add**
- [ ] `src/...`
- [ ] `tests/...`
- [ ] `docs/adr/...`   <!-- required if a decision here has a real rejected alternative -->
- [ ] `architecture.dsl`  <!-- if containers / boundaries / dependencies change -->
- [ ] `notebooks/...`
- [ ] `docs/...`

**High-level steps**
1. …
2. …
3. …

**Decisions expected**
- **Decision:** <!-- what has to be chosen --> · **Alternatives:** <!-- what else was on the table -->
- [ ] If a real alternative gets rejected, an **ADR** is written as part of this work
---
## 🔧 Branch + Commit Plan
**Branch:** `feature/<issue-number>-<slug>`

**Commits (planned, Conventional Commits):**
1. `feat: …`
2. `test: …`
3. `docs: …`
---
## 🧪 Validation Plan (local)
**Smoke**
- [ ] `uv sync --frozen` succeeds (lock in sync)
- [ ] `uv run python -c "import <package>"` passes
- [ ] Notebook cell(s) run clean
- [ ] `uv run ruff check src/ tests/` · `uv run mypy src/` clean
- [ ] `uv run pytest -q` green
- [ ] `uv run deepeval test run tests/test_eval.py` passes *(if the project has eval gates)*

**Data quality (if data touched)**
- [ ] No duplicate keys where uniqueness required
- [ ] Expected columns present in canonical schema
- [ ] Dtypes correct (dates / Int64 / Float64)
- [ ] Rerun is idempotent; any retried write carries an idempotency key
---
## ✅ Acceptance Criteria
- [ ] AC1: <!-- observable outcome -->
- [ ] AC2:
- [ ] AC3:
---
## 🧯 Risks / Edge Cases
- **Risk:** …
- **Edge cases:** missing DOB / missing year / duplicates / NaNs / empty input / timeout
- **Mitigation:** …
---
## 🔐 Data & Security
- [ ] Plan uses synthetic data only — no real client data
- [ ] No secrets committed; credentials typed `SecretStr`
- [ ] Config through `settings` (pydantic-settings), not raw `os.environ`
- [ ] Proprietary data stays on local Ollama; provider fallback is local, never cloud
---
## 📎 Definition of Done (PR checklist)
- [ ] Summary + rationale in PR
- [ ] Verification commands/cells included
- [ ] Reproducibility noted (env, seed, config, `uv.lock` in sync)
- [ ] ADR added if a decision had a rejected alternative
- [ ] Diagrams regenerated via `make diagrams` if the model changed
- [ ] Eval gate passes (blocking — no evals, no merge)
- [ ] Matching packs filled in PR
- [ ] `Closes #<issue-number>`



<!-- ============ CAPABILITY PACKS — expand + fill the ticked ones ============ -->

<details>
<summary><b>🟦 DE PACK</b></summary>

- **Canonical schema impact:** new/modified columns, or "no change"
- **Business rule(s) + threshold(s):** <!-- e.g. 59½ by 12/31; 55-rule; exclusions/locks -->
- **Join keys / null-handling / type enforcement:**
- **Idempotency:** rerun-safe? retried writes keyed?
- **Lineage:** input source + version/hash; backfill range + rollback
- **Data contract / freshness SLA:** if downstream consumers exist
- **Export checks:** template header alignment; opens in Excel
</details>

<details>
<summary><b>🟩 ML PACK</b></summary>

<!-- Under v10.0, ML is a compressed literacy module inside Stage 3, not a career stage.
     Sequence: Prompt → RAG → Fine-tune → Distill. -->

- **Model + intended use / out-of-scope:** (model card to be added/updated)
- **Baseline to beat:** metric + current baseline value + target threshold
- **Dataset version + split plan:** train/val/test; leakage guard
- **Experiment tracking:** MLflow run planned; seed + run count
- **Serving/monitoring impact:** latency, drift signals to watch
</details>

<details>
<summary><b>🟪 LLM / RAG PACK</b></summary>

- **Eval gates (blocking):** answer relevancy > 0.80 · faithfulness > 0.85 · hallucination < 0.15.
  **Raised bar for AFC and Crucible: faithfulness ≥ 0.90, hallucination < 0.10.**
- **Labeled set:** 30+ cases incl. edge, out-of-scope, adversarial, PII-probing
- **Judge routing:** local Ollama for finance/proprietary eval data; cloud only on public data
- **Prompt / retrieval changes:** prompt version; chunking / top-k / embedding model
- **Store:** ChromaDB / Neo4j; index rebuild needed?
- **Cost & latency budget:** tokens/call, est. $/run, p95 target — feeds README **② Cost**
- **Routing & guardrails:** privacy-first (finance → local Ollama; Anthropic SDK as primary cloud);
  fallback is local; PII + injection surface; response-side scan before display
</details>

<details>
<summary><b>🟧 AGENTIC PACK</b></summary>

- **Type:** workflow vs agent (Anthropic taxonomy)
- **Autonomy tier + action space:** read-only / draft / write / irreversible; tools + least-privilege scopes
- **Loop spec:** trigger, steps, state persistence
- **Exits & budgets:** max iterations, cost/action caps
- **🛑 Human gate + kill-switch:** required before irreversible actions (e.g. Crucible live trade) —
  no auto-approve, no timeout-approve, no confidence bypass; audit log; `human_signoff_required`
  and `killswitch_engaged` events
- **Path separation:** backtest/paper vs live enforced in the type system, not a runtime flag
- **Agent eval:** Tool Correctness (deterministic) + Task Completion planned.
  Note: eval scores never authorize execution.
- **A2A:** N/A for solo tools; note if multi-agent (defer to Stage 3)
</details>