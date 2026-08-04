<!--
=====================================================================
 PULL REQUEST TEMPLATE  (modular: universal core + capability packs)
 Purpose: keep PRs reviewable, reproducible, and portfolio-grade.
 Synced to roadmap v10.0. Standards source: AGENTS.md + .cursor/rules/.
 HOW TO USE:
   1. Fill the CORE (always).
   2. Tick the packs this change touches in "Packs active".
   3. Expand ONLY those packs below and fill them. Delete untouched packs.
 DATA RULE: never commit real SSNs / DOBs / account numbers / client data.
   Use synthetic samples. Never paste secrets or API keys.
=====================================================================
-->

# ✅ PR Summary

**Packs active in this change** (tick what applies; fill matching pack below)
- [ ] 🟦 **DE** — Data Engineering (pipelines, schema, data quality)
- [ ] 🟩 **ML** — Classical / Deep ML (trained model, metrics, experiment)
- [ ] 🟪 **LLM / RAG** — Prompts, retrieval, LLM evals, cost/latency
- [ ] 🟧 **Agentic** — Autonomous loop, tools, autonomy tier, kill-switch
- [ ] ⬜ None — pure infra / docs / refactor (core only)

---

## 🎯 Objective
**Problem this PR solves**
<!-- One or two sentences. -->

**Deliverable**
<!-- The concrete artifact: corrected engine logic, new endpoint, eval harness, etc. -->
---
## 📌 Scope
### In scope
- [ ] <!-- change 1 -->

### Out of scope
- <!-- explicitly excluded, so reviewers don't expect it -->
---
## 🧩 What changed
### Files changed / added
- [ ] `src/...`
- [ ] `tests/...`
- [ ] `docs/adr/...`
- [ ] `notebooks/...`
- [ ] `docs/...`

### High-level approach
1. <!-- conceptual step 1 -->
2. <!-- conceptual step 2 -->
---
## 🏗️ Architecture & decisions
- [ ] **ADR added** for any decision in this PR with a real rejected alternative
      (or: no such decision — state why)
- [ ] Superseded ADRs **marked with a pointer**, not rewritten or deleted
- [ ] `architecture.dsl` updated if containers, boundaries or dependencies changed
- [ ] Mermaid diagrams **regenerated** via `make diagrams` — not hand-edited
- [ ] README **① Production · ② Cost · ③ Architecture** sections still accurate after this change
---
## ✅ Acceptance Criteria
<!-- Written as observable outcomes, mirrored from the Issue. -->
- [ ] AC1:
- [ ] AC2:
- [ ] AC3:
- [ ] No behavior change outside declared scope.
- [ ] Output remains compatible with downstream: `<module/function>`.
---
## 🧪 Validation (executed locally)
```bash
uv sync --frozen                       # fails if uv.lock is stale
uv run python -c "import <package>"    # import smoke test
uv run ruff check src/ tests/
uv run ruff format --check src/ tests/
uv run mypy src/
uv run pytest -q                       # unit + integration
uv run deepeval test run tests/test_eval.py   # if the project has eval gates
```
**Results** (paste short, masked output — no sensitive values):
```
<paste pytest summary line, e.g. "42 passed in 3.1s">
```
- [ ] `pyproject.toml` + committed **`uv.lock`** are the single source of deps (no `requirements.txt`)
- [ ] Typed source; `from __future__ import annotations`; `py.typed` present
- [ ] **structlog kwargs** for all logging — no `print()`, no f-strings or `%s` interpolation of payload
- [ ] Config through `settings` (pydantic-settings); no raw `os.environ`
- [ ] Retries via `stamina`, capped and transient-only; retried writes carry an idempotency key
- [ ] Conventional Commits used on the branch

## 🔁 Reproducibility & environment
- **Python / env:** <!-- 3.12, uv-managed, uv.lock committed and in sync -->
- **Seed(s) set:** <!-- global seed for any stochastic step, or "N/A" -->
- **Config pinned:** <!-- config file / env vars this run depends on -->
- **Rerun is deterministic / idempotent:** [ ] yes  [ ] no (explain)
- [ ] `run_id` bound via contextvars with `clear_contextvars()` called first (no cross-run bleed)

## 🔐 Security & data hygiene
- [ ] No real client data, SSNs, DOBs, account numbers committed
- [ ] No secrets / API keys / tokens in code, tests, or notebook output
- [ ] Credentials typed `SecretStr`; unwrapped only at the client constructor
- [ ] PII layers intact: `redact_pii` processor · `SecretStr` · display-boundary masking
- [ ] No prompt/completion **bodies** logged at INFO
- [ ] Dependencies reviewed (no unpinned or abandoned adds)
- [ ] Inputs validated (Pydantic / schema) at trust boundaries
- [ ] *(Regulated systems)* every public figure clears the **deposition test**
---
## 🧯 Risks / Edge Cases
- **Risk:** <!-- what could break -->
- **Edge cases covered:** <!-- nulls, dupes, missing keys, empty inputs, timeouts -->
- **Mitigation / rollback:** <!-- how to revert; feature flag; migration down-step -->
---
## 📎 Reviewer Notes
**Focus review on:** <!-- the 2–3 things most likely to be wrong -->
**Screenshots / sample outputs (masked, optional):**
<details><summary>run output</summary>

<!-- masked screenshot or small masked table -->

</details>
---
## 🔗 Linking
- Closes #<issue-number>



<!-- ================================================================
     CAPABILITY PACKS — expand + fill ONLY the ones ticked above.
     Delete the packs you did not tick.
================================================================= -->

<details>
<summary><b>🟦 DE PACK — Data Engineering</b></summary>

### Canonical schema impact
- **New columns:** <!-- name : dtype : meaning -->
- **Modified columns:** <!-- name : before → after -->
- [ ] No schema change

### Business rules implemented / updated
- **Rule(s):** <!-- concise description -->
- **Threshold(s):** <!-- e.g. 59.5 attained by 12/31; 55-rule; term-year logic -->
- **Exclusions / locks:** <!-- excluded-from-engine vs tax-code-locked -->

### Data quality
- **Join keys:** <!-- e.g. plan_id + participant_key -->
- **Null-handling:** <!-- missing DOB / term_date behavior -->
- **Type enforcement:** <!-- dates / Int64 / Float64 normalized -->
- [ ] No duplicate keys where uniqueness is required
- [ ] Idempotent: rerun produces stable output
- [ ] Data contract / freshness SLA stated if downstream consumers exist

### Lineage & versioning
- **Input source + version/hash:** <!-- dataset id, snapshot date, DVC/hash -->
- **Backfill / migration:** <!-- range affected + down-migration / rollback -->

### Export checks (if applicable)
- [ ] Template headers found (no misalignment)
- [ ] Output opens in Excel; columns populate correctly
</details>

<details>
<summary><b>🟩 ML PACK — Classical / Deep ML</b></summary>

### Model card (link or inline)
- **Model + version:** <!-- name, architecture, params -->
- **Intended use / out-of-scope:** <!-- what it's for; what it must NOT be used for -->
- **Limitations & known failure modes:**
- [ ] Model card file added/updated in repo and re-reviewed for this change

### Metrics vs. baseline  *(earned-overlay gate: ship only if it beats baseline)*
| Metric | Baseline | This PR | Δ | Threshold |
|--------|---------:|--------:|---:|-----------|
| <!-- e.g. F1 --> |  |  |  |  |
| <!-- e.g. RMSE --> |  |  |  |  |
- [ ] Candidate **beats** baseline on the primary metric (else: justify or close)

### Data & experiment provenance
- **Dataset version / split:** <!-- train/val/test sizes; split method; date -->
- [ ] Leakage check done (no target/temporal leakage across splits)
- **Experiment tracking:** <!-- MLflow run id / params logged -->
- **Seed + run count:** <!-- seed value; N runs; variance if stochastic -->

### Serving / monitoring impact
- **Latency / size change:** <!-- inference time, artifact size -->
- **Drift / monitoring hooks:** <!-- what to watch post-deploy -->
</details>

<details>
<summary><b>🟪 LLM / RAG PACK — Prompts, Retrieval, Evals</b></summary>

### Eval gates  *(BLOCKING — no evals, no merge)*
| Metric (DeepEval / RAGAS / GEval) | Threshold | Before | After |
|-----------------------------------|-----------|-------:|------:|
| Faithfulness / Groundedness | <!-- ≥0.85 baseline; ≥0.90 AFC & Crucible --> |  |  |
| Answer relevancy | ≥ 0.80 |  |  |
| Hallucination | <!-- <0.15 baseline; <0.10 AFC & Crucible --> |  |  |
| Context relevance / recall |  |  |  |
| Extraction accuracy (GEval) |  |  |  |
- [ ] Eval **set** ran (30+ labeled cases incl. adversarial and PII-probing), not a single example
- [ ] Regression checked before→after
- [ ] Meets project threshold (**raised bar: AFC and Crucible ≥0.90 faithfulness, <0.10 hallucination**)
- [ ] **Judge routing correct** — local Ollama for finance/proprietary eval data

### Prompt / retrieval changes
- **Prompt change:** <!-- summary; prompt is versioned in repo -->
- **Retrieval config:** <!-- chunking, top-k, embedding model, reranker -->
- **Vector / graph store:** <!-- ChromaDB / Neo4j GraphRAG; index rebuilt? -->

### Cost & latency budget
- **Tokens / call & est. $/run:** <!-- in/out tokens, unit cost -->
- **p95 latency:** <!-- ms -->
- [ ] Within budget; caching / batching noted if relevant
- [ ] README **② Cost** updated if unit economics changed — state the mechanism, not just the number

### Routing, guardrails & observability
- **Model routing:** <!-- from settings.ai_provider; finance/proprietary → local Ollama -->
- [ ] Provider fallback is **local, never cloud**
- [ ] No sensitive data sent to free/training-eligible cloud tiers
- [ ] Output validated (Pydantic / schema); response-side PII scan runs before display
- **Observability:** <!-- provider · model · tokens · latency · cost · guardrail status, structlog kwargs -->
- [ ] `query_id` bound to contextvars so SDK/httpx logs correlate
</details>

<details>
<summary><b>🟧 AGENTIC PACK — Autonomous Loop & Safety</b></summary>

### Taxonomy & autonomy
- **Type:** [ ] Workflow (fixed path)  [ ] Agent (model-directed loop)  *(Anthropic framing)*
- **Autonomy tier for this change:** <!-- read-only / draft-only / write / irreversible -->
- **Action space (tools):** <!-- exact tools + least-privilege scopes granted -->

### Loop spec
- **Trigger / schedule:**
- **Steps (plan → act → check → retry):**
- **State persistence:** <!-- where loop state lives; resumable? -->

### Exits & budgets
- **Layered exit conditions:** <!-- max iterations, success/failure heuristics -->
- **Cost / action caps:** <!-- $ cap, max tool calls, rate limit -->

### 🛑 Human oversight & kill-switch  *(mandatory for irreversible actions)*
- **Gate pattern:** [ ] pre-execution approval  [ ] post-execution review  [ ] escalation-on-risk
- [ ] **Human sign-off required before any irreversible action** (e.g. Crucible live trade) —
      no auto-approve, no timeout-approve, no confidence-threshold bypass
- [ ] **Kill-switch present and tested**, halting independently of the agent loop
- [ ] `human_signoff_required` and `killswitch_engaged` emitted as canonical events
- [ ] Backtest/paper and live paths separated **in the type system**, not by a runtime flag
- [ ] Full action audit log written
- [ ] Acknowledged: **eval scores never authorize execution** — a PASS is threshold met, not clearance
- **A2A:** <!-- N/A for solo tools; note if multi-agent (defer to Stage 3) -->

### Agent evaluation
- [ ] Trajectory / tool-use eval run — **Tool Correctness** (deterministic) and **Task Completion**
- [ ] *(Trading)* no P&L, returns, or account figures anywhere in this PR or its artifacts
</details>