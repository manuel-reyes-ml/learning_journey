# 🚩 Flagship Checklist — Definition of Done

> A project is **flagship / production-grade** only when every core box below is ticked, plus the
> capability packs it touches. Human commit is the final gate — nothing ships below this bar.
> Synced to roadmap **v10.0**. Canonical copy lives at `.github/docs/FLAGSHIP_CHECKLIST.md`;
> per-repo copies go to `docs/FLAGSHIP_CHECKLIST.md`. Check it before pinning the repo.
>
> **Standards source:** `AGENTS.md` (contract) + `.cursor/rules/` (detail). Where this checklist
> and a rule file disagree, the rule file wins and this file gets a correction.

**Project:** `<name>`  ·  **Roadmap stage:** `[ ] 1 Internal AI Builder  [ ] 2 AI-Focused DE/AE  [ ] 3 Applied AI Eng / FDE`
**Packs:** `[ ] DE  [ ] ML  [ ] LLM/RAG  [ ] Agentic`

---

## 0. The 40-second scan  *(a reviewer forms a judgement fast — win the top of the README first)*
- [ ] First line states **what it is + who it's for + why it's different**, finance-framed
- [ ] **Problem** (domain-specific, not generic) and **outcome** appear in the first ~200 words
- [ ] **Demo GIF (15–30s) and/or live demo link** above the fold
- [ ] One row of **functional badges** only (CI, coverage, version, license, eval-gate) — no vanity badges
- [ ] Reader can tell what it does **without reading code**

## 1. Repo hygiene & production standards
- [ ] `pyproject.toml` + committed **`uv.lock`** are the single dependency source — **zero** `requirements.txt`
- [ ] `src/` layout · `py.typed` present · fully typed source (PEP 604 unions)
- [ ] **`from __future__ import annotations`** as the first line of every module
- [ ] **`structlog`** via `ProcessorFormatter` — event name is a stable `snake_case` key, all data in
      kwargs. **No f-strings and no `%s`/`%d` interpolation of payload data.** No `print` outside `scripts/`
- [ ] `configure_logging()` called **once at the entrypoint**; no library-level `basicConfig()`
- [ ] All config through **`pydantic-settings`** (`settings`) — no raw `os.environ` reads
- [ ] Retries via **`stamina`** — capped attempts *and* total time, jittered, transient errors only
- [ ] Formatting/linting by **`ruff`** (`format` + `check`) — Black and standalone isort are retired
- [ ] Conventional Commits · semver · clean, readable commit history
- [ ] `Dockerfile` builds and runs using **`uv sync --frozen`** — never `pip install`
- [ ] `.env.example` present with **empty** values · `.env` gitignored
- [ ] `AGENTS.md` and `.cursor/rules/` committed
- [ ] "No vibe coding": every line understood and reviewed before merge (incl. AI-suggested code)

## 2. Testing & CI
- [ ] `pytest` suite passes locally and in CI
- [ ] Coverage at/above target `<e.g. 80%>` on core logic
- [ ] **GitHub Actions** green: lint (ruff) · format check · types (mypy) · tests · **eval gate**
- [ ] CI installs with **`uv sync --frozen`** (fails on a stale lock; never re-resolves)
- [ ] `conftest.py` carries the **`_reset_structlog`** fixture (`cache_logger_on_first_use=False`)
      and **`_no_retry_sleeps`** (`stamina.set_active(False)`)
- [ ] Load-bearing log events have **field-level assertions** via `structlog.testing.capture_logs`
- [ ] `pre-commit` hooks configured (format, lint, secrets scan) *(⚠️ not yet mirrored in
      `project-scaffold.mdc` — confirm whether this stays a standard or the Makefile + CI path replaces it)*

## 3. Documentation & architecture  *(your cross-project README standard)*
- [ ] README leads with the three headings, **in this order**: **① Production · ② Cost · ③ Architecture**
- [ ] **① Production** — where it runs, what depends on it, deploy path, monitoring, reliability posture,
      the blocking eval gates. *A stack list is not a production claim.*
- [ ] **② Cost** — the number **and the mechanism** behind it, with the reliability SLA it held to.
      *Explicitly optional for FormSense and AFC — never manufacture one.*
- [ ] **③ Architecture** — diagram + C4 + ADRs + contracts, with the decisions behind them
- [ ] **`docs/adr/`** present, starting with `0001-record-architecture-decisions.md`; one template only
      (MADR **or** Nygard); every decision with a **real rejected alternative** has a record
- [ ] Superseded ADRs **marked with a pointer** — never deleted or edited in place
- [ ] **`architecture.dsl`** (Structurizr) is the single C4 model source
- [ ] **C4 Context** on every project · **C4 Container** on the lead flagships (DataVault, PolicyPulse, Crucible)
- [ ] Mermaid diagrams are **exported** from the DSL via `make diagrams` — never hand-authored
- [ ] **Evaluation-metrics table** with thresholds/gates
- [ ] **15–30s demo GIF**
- [ ] **"What I Learned"** section (finance-to-tech narrative hook)
- [ ] Quick start is **3 steps, copy-paste**, and current (stale commands erode trust fast)
- [ ] README stays ~one screen + links; deep docs pushed to `/docs`
- [ ] **Résumé bullets: 4–6 max**, each answering Production, Cost or Architecture — anything answering
      none is cut. Numbers only where defensible in an interview; substitute scale/reliability outcomes
      otherwise. **Never invent a figure to fill the shape.**
- [ ] **No diagrams on the résumé** — parsers skip images. Architecture goes as *text* + repo link.

## 4. Evaluation gates  *(your #1 differentiator — gated, not asserted)*
- [ ] Eval runs on a **labeled set** of **30+ cases**, not a single happy-path example —
      incl. edge cases, out-of-scope questions, adversarial and PII-probing inputs
- [ ] Thresholds are **blocking** in CI (regression = no merge, enforced by branch protection)
- [ ] Baseline met: Answer Relevancy > 0.80 · Faithfulness > 0.85 · Hallucination < 0.15
- [ ] Raised bar met where it applies: **Faithfulness > 0.90 · Hallucination < 0.10 for AFC *and* Crucible**
- [ ] Agentic components also gated on **Tool Correctness** (deterministic) and **Task Completion**
- [ ] **GEval** criterion defined where no built-in metric fits (e.g. FormSense schema adherence)
- [ ] **Judge routing correct** — local Ollama judge for finance/proprietary eval data; cloud judge
      only on public data
- [ ] **Earned-overlay proven:** any ML / re-extraction / loop overlay **beats its baseline**, or it doesn't ship
- [ ] Results logged to `logs/evaluation/` and reflected in the README metrics table

## 5. Security & data hygiene
- [ ] **No real client data** (SSNs/DOBs/account numbers) anywhere — synthetic only; `data/synthetic/`
      is the only committed data directory
- [ ] Every credential typed **`SecretStr`**, unwrapped only at the client constructor
- [ ] Three PII layers intact and none doing another's job: the **`redact_pii` processor** in the
      structlog chain · `SecretStr` on credentials · **masking helpers at display boundaries**
- [ ] LLM output passes the **response-side PII scan** before display (a fourth, separate control)
- [ ] Secrets **never logged** (a `test_logging_no_secrets`-style test enforces it)
- [ ] No secrets/keys/tokens in code, tests, notebook output, or history
- [ ] No prompt or completion **bodies** logged at INFO — shape, counts and ids only
- [ ] Inputs validated (Pydantic/schema) at trust boundaries · dependencies reviewed
- [ ] **Privacy routing holds:** proprietary data never reaches a cloud provider; the provider fallback
      is **local, never cloud**; no free/training-eligible tiers on project data
- [ ] *(Regulated systems — DataVault)* every public figure clears the **"would I say this in a
      deposition"** test; regulatory constraints that shaped the design are documented as an ADR

## 6. Reproducibility & provenance
- [ ] Env + seeds pinned (**`uv.lock` committed and in sync**); rerun is deterministic/idempotent where applicable
- [ ] Only idempotent operations are retried; any retried write carries an **idempotency key**
- [ ] **Run manifests** persisted: `run_id` · git SHA · config/params hash · data-snapshot version · seeds
- [ ] `run_id` bound via **contextvars**, with `clear_contextvars()` called first so context never
      bleeds between runs
- [ ] Operational logs (`logs/`, gitignored) kept **separate** from durable audit/provenance artifacts (`runs/`)
- [ ] *(Research projects)* overfitting-budget ledger / OOS-peek log **version-controlled** as evidence

---

<!-- ===== CAPABILITY PACKS — complete the ones ticked at the top ===== -->

<details>
<summary><b>🟦 DE PACK</b></summary>

- [ ] Canonical schema documented; changes are intentional and noted
- [ ] Data-quality checks: join keys, null-handling, dtype enforcement, no dup keys where unique
- [ ] Idempotent reruns · scheduling/orchestration shown (Airflow/cron) if it's a pipeline
- [ ] Lineage: input source + version/hash; backfill/rollback path documented
- [ ] Data contracts and freshness SLAs stated where downstream consumers exist
- [ ] Export integrity (headers align, opens in Excel) if applicable
</details>

<details>
<summary><b>🟩 ML PACK</b></summary>

> Under v10.0, ML is a **compressed literacy module inside Stage 3**, not a career stage.
> Adaptation sequence: **Prompt → RAG → Fine-tune → Distill.** This pack applies when a project
> actually carries a model — it is not a target to reach for.

- [ ] **Model card** in repo (intended use · out-of-scope · limitations · failure modes), re-reviewed on model change
- [ ] Baseline-vs-candidate metrics table; candidate **beats baseline** on the primary metric
- [ ] Experiment tracking (MLflow run id · params); seed + run count reported
- [ ] Dataset version + train/val/test split disclosed; **leakage check** done
- [ ] Serving/monitoring impact noted (latency, drift signals)
</details>

<details>
<summary><b>🟪 LLM / RAG PACK</b></summary>

- [ ] Eval gates wired (DeepEval/RAGAS/GEval) with **before→after** regression
- [ ] Prompts **versioned**; prompt changes pass eval before promotion
- [ ] Retrieval config documented (chunking, top-k, embedding model, store: ChromaDB/Neo4j)
- [ ] **Cost & latency budget** reported (tokens/call, est. $/run, p95) — feeds README **② Cost**
- [ ] Per-query observability: provider · model · tokens · latency · cost · guardrail status,
      logged as structlog kwargs with `query_id` bound to contextvars
- [ ] **Privacy-first routing** enforced (finance/proprietary → local Ollama; never free/training-eligible tiers)
- [ ] Output validated (Pydantic) · PII + prompt-injection surface handled
- [ ] ADR records the retrieval strategy and its rejected alternative
</details>

<details>
<summary><b>🟧 AGENTIC PACK</b></summary>

- [ ] Type declared (**workflow vs agent**, per Anthropic's taxonomy) + **autonomy tier**
      (read-only / draft / write / irreversible), stated in both the ADR and the README
- [ ] **Action space = least privilege** (exact tools + scopes; nothing broader)
- [ ] Loop spec: trigger → plan → act → check → retry · exits: max iters + cost/action caps
- [ ] 🛑 **Human sign-off gate before any irreversible action** *(Crucible live trade)* — no
      auto-approve, no timeout-approve, no confidence-threshold bypass
- [ ] 🛑 **Kill-switch present and tested**, halting execution independently of the agent loop;
      kill-switch events logged (`killswitch_engaged`)
- [ ] `human_signoff_required` emitted whenever an irreversible action awaits approval
- [ ] **Eval scores never authorize execution** — a PASS means threshold met, not cleared to act
- [ ] Full action **audit log** written; provenance ties results to code+data
- [ ] Backtest/paper and live paths separated **in the type system**, not by a runtime flag
- [ ] *(Trading)* deterministic engine owns every entry/exit; the LLM never places or times a trade
- [ ] *(Trading)* **no P&L, returns, or account figures** in any public artifact — ever
- [ ] Trajectory / tool-use eval run; disclaimer present (not financial advice)
- [ ] A2A: N/A for solo tools; note if multi-agent (defer to Stage 3)
</details>

---

### ✅ Final gate
- [ ] Commit gate in `AGENTS.md` run clean (16 items)
- [ ] `make test` · `make format` · `make lint` · `make eval` · `make docker-build` all pass
- [ ] I (human) reviewed the full `git diff` and every box above before committing
- [ ] Repo is worthy of being a **pinned** flagship