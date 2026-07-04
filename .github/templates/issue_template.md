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
- [ ] `notebooks/...`
- [ ] `docs/...`

**High-level steps**
1. …
2. …
3. …
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
- [ ] `python -c "import <package>"` passes
- [ ] Notebook cell(s) run clean
- [ ] `python -m pytest -q` green

**Data quality (if data touched)**
- [ ] No duplicate keys where uniqueness required
- [ ] Expected columns present in canonical schema
- [ ] Dtypes correct (dates / Int64 / Float64)
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
- [ ] Plan uses masked/synthetic data only — no real client data
- [ ] No secrets committed
---
## 📎 Definition of Done (PR checklist)
- [ ] Summary + rationale in PR
- [ ] Verification commands/cells included
- [ ] Reproducibility noted (env, seed, config)
- [ ] Matching packs filled in PR
- [ ] `Closes #<issue-number>`



<!-- ============ CAPABILITY PACKS — expand + fill the ticked ones ============ -->

<details>
<summary><b>🟦 DE PACK</b></summary>

- **Canonical schema impact:** new/modified columns, or "no change"
- **Business rule(s) + threshold(s):** <!-- e.g. 59½ by 12/31; 55-rule; exclusions/locks -->
- **Join keys / null-handling / type enforcement:**
- **Lineage:** input source + version/hash; backfill range + rollback
- **Export checks:** template header alignment; opens in Excel
</details>

<details>
<summary><b>🟩 ML PACK</b></summary>

- **Model + intended use / out-of-scope:** (model card to be added/updated)
- **Baseline to beat:** metric + current baseline value + target threshold
- **Dataset version + split plan:** train/val/test; leakage guard
- **Experiment tracking:** MLflow run planned; seed + run count
- **Serving/monitoring impact:** latency, drift signals to watch
</details>

<details>
<summary><b>🟪 LLM / RAG PACK</b></summary>

- **Eval gates (blocking):** metrics + thresholds (DeepEval / RAGAS / GEval; AFC ≥0.90 faithfulness)
- **Prompt / retrieval changes:** prompt version; chunking / top-k / embedding model
- **Store:** ChromaDB / Neo4j; index rebuild needed?
- **Cost & latency budget:** tokens/call, est. $/run, p95 target
- **Routing & guardrails:** privacy-first (finance→local Ollama); PII + injection surface
</details>

<details>
<summary><b>🟧 AGENTIC PACK</b></summary>

- **Type:** workflow vs agent (Anthropic taxonomy)
- **Autonomy tier + action space:** read-only / draft / write / irreversible; tools + least-privilege scopes
- **Loop spec:** trigger, steps, state persistence
- **Exits & budgets:** max iterations, cost/action caps
- **🛑 Human gate + kill-switch:** required before irreversible actions (e.g. Crucible live trade); audit log
- **Agent eval:** trajectory / tool-use eval planned
- **A2A:** N/A for solo tools; note if multi-agent (Stage 4–5)
</details>