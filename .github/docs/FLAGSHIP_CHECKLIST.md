# 🚩 Flagship Checklist — Definition of Done

> A project is **flagship / production-grade** only when every core box below is ticked, plus the
> capability packs it touches. Human commit is the final gate — nothing ships below this bar.
> Copy this into each repo as `docs/FLAGSHIP_CHECKLIST.md` and check it before pinning the repo.

**Project:** `<name>`  ·  **Roadmap stage:** `<N>`  ·  **Packs:** `[ ] DE  [ ] ML  [ ] LLM/RAG  [ ] Agentic`

---

## 0. The 40-second scan  *(a reviewer decides in ~40s — win the top of the README first)*
- [ ] First line states **what it is + who it's for + why it's different**, finance-framed
- [ ] **Problem** (domain-specific, not generic) and **quantified result** appear in the first ~200 words
- [ ] **Demo GIF (15–30s) and/or live demo link** above the fold *(84% of managers look for a working demo)*
- [ ] One row of **functional badges** only (CI, coverage, version, license, eval-gate) — no vanity badges
- [ ] Reader can tell what it does **without reading code**

## 1. Repo hygiene & production standards
- [ ] `pyproject.toml` is the **single** dependency source — **zero** `requirements.txt`
- [ ] `src/` layout · `py.typed` present · fully typed source
- [ ] `logging` (structured/JSON where apt) — **no `print`** in library code
- [ ] Conventional Commits · semver · clean, readable commit history
- [ ] `Dockerfile` builds and runs · `.env.example` present
- [ ] "No vibe coding": every line understood and reviewed before merge (incl. AI-suggested code)

## 2. Testing & CI
- [ ] `pytest` suite passes locally and in CI
- [ ] Coverage at/above target `<e.g. 80%>` on core logic
- [ ] **GitHub Actions** green: lint (ruff) · types (mypy) · tests · eval gate
- [ ] `pre-commit` hooks configured (format, lint, secrets scan)

## 3. Documentation (your cross-project README standard)
- [ ] Mermaid **architecture diagram**
- [ ] **Evaluation-metrics table** with thresholds/gates
- [ ] **15–30s demo GIF**
- [ ] **"What I Learned"** section (finance-to-tech narrative hook)
- [ ] Quick start is **3 steps, copy-paste**, and current (stale commands erode trust fast)
- [ ] README stays ~one screen + links; deep docs pushed to `/docs`

## 4. Evaluation gates  *(your #1 differentiator — gated, not asserted)*
- [ ] Eval runs on a **labeled set**, not a single happy-path example
- [ ] Thresholds are **blocking** in CI (regression = no release)
- [ ] Project threshold met *(e.g. AFC faithfulness ≥ 0.90 for finance data)*
- [ ] **Earned-overlay proven:** any ML / re-extraction / loop overlay **beats its baseline**, or it doesn't ship

## 5. Security & data hygiene
- [ ] **No real client data** (SSNs/DOBs/account numbers) anywhere — synthetic/masked only
- [ ] Secrets via `SecretStr`/env; **never logged** (a `test_logging_no_secrets`-style test enforces it)
- [ ] No secrets/keys/tokens in code, tests, notebook output, or history
- [ ] Inputs validated (Pydantic/schema) at trust boundaries · dependencies reviewed

## 6. Reproducibility & provenance
- [ ] Env + seeds pinned; rerun is deterministic/idempotent where applicable
- [ ] **Run manifests** persisted: `run_id` · git SHA · config/params hash · data-snapshot version · seeds
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
- [ ] Export integrity (headers align, opens in Excel) if applicable
</details>

<details>
<summary><b>🟩 ML PACK</b></summary>

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
- [ ] **Cost & latency budget** reported (tokens/call, est. $/run, p95)
- [ ] **Privacy-first routing** enforced (finance/proprietary → local Ollama; never free/training-eligible tiers)
- [ ] Output validated (Pydantic) · PII + prompt-injection surface handled
</details>

<details>
<summary><b>🟧 AGENTIC PACK</b></summary>

- [ ] Type declared (workflow vs agent) + **autonomy tier** (read-only / draft / write / irreversible)
- [ ] **Action space = least privilege** (exact tools + scopes; nothing broader)
- [ ] Loop spec: trigger → plan → act → check → retry · exits: max iters + cost/action caps
- [ ] 🛑 **Human sign-off gate before any irreversible action** *(Crucible live trade)*
- [ ] 🛑 **Kill-switch present and tested**; kill-switch events logged
- [ ] Full action **audit log** written; provenance ties results to code+data
- [ ] *(Trading)* deterministic engine owns every entry/exit; the LLM never places or times a trade
- [ ] Trajectory / tool-use eval run; disclaimer present (not financial advice)
- [ ] A2A: N/A for solo tools; note if multi-agent (Stage 4–5)
</details>

---

### ✅ Final gate
- [ ] I (human) reviewed the full `git diff` and every box above before committing
- [ ] Repo is worthy of being a **pinned** flagship
