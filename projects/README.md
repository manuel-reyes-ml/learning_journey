# 🚀 Project Portfolio Directory

**3 Flagships + 2 Supporting** | One system per project, evolved S1 → S3 | Evidence-first, evaluation-gated

> **Portfolio Hub:** **[data-portfolio →](https://github.com/manuel-reyes-ml/data-portfolio)** for full project summaries, tech stacks, scope documents, and skills badges. This page is the index that lives alongside the roadmap.

Aligned to the **[v10.0 career roadmap](https://manuel-reyes-ml.github.io/learning_journey/roadmap.html)** — 3 stages, ~32 months.

---

## 📌 Project Pipeline (S1 → S3)

Each project is **one system that evolves across stages**, not a set of scattered tutorials. *Flagship vs supporting denotes size and emphasis — not a quality tier; every project carries the full production standard.*

| # | Project | Role | What it does | Status |
|---|---------|------|-------------|--------|
| 1 | 🧾 **DataVault / 1099 Data Platform** | 🚩 Flagship — Data Engineering | 1099 reconciliation core → dbt-tested platform (CI) → Applied-AI natural-language analyst layer (HITL on every write) | ✅ **S1 core live** |
| 2 | 📋 **PolicyPulse** | 🚩 Flagship — Applied AI (RAG) | Cited-source RAG over plan documents → GraphRAG hybrid (Neo4j + ChromaDB) → agentic + eval/observability; exposes a **FastMCP server** | 🏗️ **S1 shipping** |
| 3 | 🔥 **Crucible** | 🚩 Flagship — Autonomous trading research | Multi-timeframe (swing → intraday) backtest → paper → live through validation gates; **HITL sign-off + kill-switch** on the live path | 🏗️ **S1 in progress** |
| 4 | 📈 **Attention-Flow Catalyst (AFC)** | Supporting — Research | Eval-first core: SEC-grounded faithfulness benchmark + controlled-perturbation catalog; GraphRAG financial-KG | 🏗️ **S1 core** |
| 5 | 📄 **FormSense** | Supporting — Document ops | Multimodal structured extraction from distribution forms; Pydantic frozen-schema contract; agentic workflow | 📅 Planned |
| 6 | 📺 **StreamSmart** · 📊 **ODI** | Backlog | Consumer subscription optimizer · enterprise demand analytics (ODI = consolidation candidate) | 🗒️ Backlog |

> Shared library: **`signalcore`** — point-in-time-safe primitives beneath AFC + Crucible (siblings, no merge). Content tooling: **Cadence** (build-in-public pipeline — a tool, not a portfolio flagship).
>
> Toolchain: **uv (Astral)** manages packages and environments across every project above; **`structlog` + `pydantic-settings` + `stamina`** are the shared observability, configuration and retry layer beneath all of them; a pinned **`.pre-commit-config.yaml`** is the shared enforcement layer at the commit boundary. **Conda** is a deliberate exception, not a default — reserved for **Crucible only**, and only if it grows compiled numerical / CUDA / BLAS backends where binary channels beat wheels.

---

## 🏆 Production Highlight

### 🧾 DataVault / 1099 Data Platform (S1 core) — ✅ Live in an ERISA-regulated environment

| ⚡ ~95% time reduction | 📈 Full distribution book, no added headcount | 🛡️ Derived-vs-reported Box-7 validation gate | ✅ Reconciliation success rate held to a freshness SLA |
|---|---|---|---|

Ingests Matrix + Relius into a canonical model, reconciles them, derives Box-7 codes, and surfaces corrections analytics.

> 🔒 **Regulated-environment disclosure.** The public build uses synthetic data only; the production deployment runs internally on regulated data. Published claims are limited to **mechanism and non-identifying relative deltas** — no absolute cost figures, participant or plan data, client identifiers, or employer-identifying volumes. The Cost line for this project is therefore thinner than a typical portfolio project's: a disclosure constraint, not a gap.

---

## 🚩 Flagship Highlights

### 📋 PolicyPulse — Applied-AI flagship (RAG)

- **① Production** — Containerised RAG + **FastMCP** service; **RAGAS/DeepEval blocking gates are merge conditions**, not reports; confidence-gated escalation path.
- **② Cost** — Cost-per-query and p95 latency measured across inference substrates; local-vs-cloud routing policy; embedding/re-index cost.
- **③ Architecture** — GraphRAG (Neo4j + ChromaDB) · retrieval-strategy **ADRs with rejected alternatives** · C4 Context + Container · MCP read → approval-gated write boundary.

Retrieval-augmented answering over retirement-plan documents with cited sources and confidence-gated escalation; exposes a **FastMCP server**. Evolves from vector RAG (S1) → **GraphRAG hybrid (Neo4j + ChromaDB)** for multi-hop questions (S2/S3) → agentic workflows with a three-layer eval spine (per-query metrics + trajectory tracing + drift vs. a frozen golden set).

**Last-mile layer:** a streaming Claude-powered UI on **Vercel AI SDK 7 + TypeScript + Zod + React**. Model-call ownership is ruled rather than left ambiguous — the Next.js route handler owns the call for the single-turn chat and invokes retrieval as a tool. ⚠️ **Language boundary:** TypeScript is the **last mile only**. The agentic loop, GraphRAG fusion, access-control retrieval and the full eval suite stay in **Python**; no agent core crosses the boundary.

### 🧾 DataVault / 1099 Data Platform — Data-Engineering flagship

- **① Production** — Live, depended-upon pipeline in a regulated environment — reconciliation success rate, freshness SLA, quarantine/retry behaviour, schema contracts, on-call reality.
- **② Cost** — 🔒 *Deliberately constrained.* Mechanism + non-identifying relative deltas + manual hours removed. No absolute figures — see the disclosure above.
- **③ Architecture** — **ERISA-driven ADRs** (retention, auditability, reconciliation guarantees, PII boundary) · C4 Context + Container · dbt tests and data contracts.

One system across the arc. **S1:** the live 1099 reconciliation core. **S2:** hardened into a platform — dbt-tested models (CI-gated), orchestration (Airflow), data contracts, containerized deploy, monitoring, one written incident/postmortem. **This is the Stage 1 exit gate** — the roadmap now exits Stage 1 on shipped evidence rather than on an employment milestone, and this is the evidence. **S3:** the Applied-AI analyst layer (natural-language querying) with **human-in-the-loop on every write**.

### 🔥 Crucible — Autonomous trading-research flagship (started first)

- **① Production** — Backtest → paper → live path with **mandatory HITL sign-off + kill-switch**; deterministic core owns every trade; intended-vs-filled reconciliation.
- **② Cost** — Compute cost per backtest sweep, data-feed cost, sweep efficiency (results per compute-hour).
- **③ Architecture** — Multi-timeframe design · execution and risk-control ADRs · C4 Context + Container · `signalcore` boundary (primitives in, strategy logic out).

> **The question it answers, for any strategy:** *Does this have a real edge that survives out-of-sample validation — and can an autonomous agent trade it without babysitting?*

**Multi-timeframe (swing → intraday):** swing-first is the lower-risk on-ramp; intraday plugins follow once swing clears all three integrity gates. **AI behind the Wall:** an LLM proposes strategy improvements, but they're *proved* by deterministic backtests it never optimizes against — the out-of-sample set is a sealed vault, every peek logged in an overfitting-budget ledger. Strategies are plugins (Protocol + ABC + registry).

| Stage | Evolution | Live money? |
|-------|-----------|-------------|
| **S1** | Own event-driven backtest harness + AI research loop + integrity spine (sealed OOS vault · overfitting ledger · engine-parity gate); uv-managed env *(Conda only if compiled/GPU backends land)* | No |
| **S2** | Migrate to NautilusTrader (engine-parity gate); autonomous paper crew (LangGraph); local Qwen/Ollama analyst | No |
| **S3** | Autonomous micro-sizing (Alpaca); deterministic core + multi-agent oversight; **mandatory HITL sign-off + kill-switch** | Yes (small) |

**Distinct from AFC (why both, not redundancy):** AFC is *read-only research* on illiquid sub-$5 small-caps over a multi-day *swing* horizon; Crucible is *autonomous execution* on liquid names *intraday*. ~70% shared engineering spine (`signalcore`), two genuinely different hard problems.

> ⚖️ *Educational/research project. Not investment advice; makes no claim of positive expectancy — validation is the entire point.*

**Supporting projects:** AFC (eval-first research core → GraphRAG financial-KG) and FormSense (multimodal document ops) carry the same production standard at smaller scope.

---

## 🏗️ Production Standard (v10.0 — all projects)

Every project ships with a **Mermaid diagram + C4 Context diagram** (+ Container view on lead flagships) · **`docs/adr/`** numbered Architecture Decision Records (context → decision → consequences) · Dockerfile · evaluation-metrics table · demo GIF · "What I Learned" · **eval-first blocking gates** · **synthetic data only** in public repos · **Python 3.14** · `pyproject.toml` + **`uv.lock`** + `src/` + `py.typed` + ruff + mypy · **structured logging** (`structlog` over stdlib via `ProcessorFormatter`, so third-party library logs render through the same chain) with a **PII-redaction processor** in that chain · **typed configuration** (`pydantic-settings`, every credential `SecretStr`) · **capped jittered retries** (`stamina`) · Conventional Commits · **branch → PR → self-review → merge** (never direct commits to `main`) · a pinned **`.pre-commit-config.yaml`**. **Environments are uv-managed** (Astral) — a committed lockfile plus `uv sync --frozen` in CI/Docker makes every build byte-reproducible; no `requirements.txt` anywhere. **The Python version is a single-source pin:** declared once as `requires-python = ">=3.14"` in `pyproject.toml`, with `[tool.ruff] target-version`, `[tool.mypy] python_version`, the Dockerfile base image and the CI matrix all reading from it — a mismatch is a **CI failure, not a lint warning**. The **standard GIL build** is used deliberately; the free-threaded `python3.14t` build is *not*, because no workload here is CPU-bound across cores and that build is where the C-extension wheel problems still live. **Logs go to stdout** (12-Factor) — rotation and shipping belong to the runtime, and run context (`run_id`) is bound via `contextvars` so one query reconstructs a full pipeline run rather than one file per stage. *Stage 3 adds an ADR set + an architecture-defense rehearsal — present and defend the design against a reviewer, mirroring the FDE panel format.*

**Evaluation:** DeepEval + pytest across all projects · RAGAS (PolicyPulse) · SelfCheckGPT (PolicyPulse + AFC) · FActScore (AFC) · Arize Phoenix observability (S3).

**Enforcement:** the hook set is a **strict subset of the CI gate** — CI stays authoritative and nothing runs locally that doesn't also run in CI, so the two can't quietly disagree. `ruff-check --fix` before `ruff-format` · `uv-lock` (keeps the lockfile claim above honest) · `gitleaks` + `detect-private-key` · `nbstripout` wherever notebooks exist, which is what makes **synthetic data only** a mechanical guarantee rather than a thing to remember · `conventional-pre-commit` on the `commit-msg` stage. **`mypy` is deliberately CI-only** — the `mirrors-mypy` hook's default `--ignore-missing-imports` silently degrades third-party types to `Any`, so the exclusion is an ADR, not an omission.

**Observability:** structured events are testable assertions, not just output — `structlog.testing.capture_logs` lets tests assert on *fields* rather than regex-matching log strings, so audit trails, guardrail activations and reconciliation outcomes carry real coverage. A trace-correlation processor (`trace_id` / `span_id`) is stubbed from S1 so the S3 Phoenix layer attaches without touching call sites.

---

## 🗂️ Repository Strategy

| Repo | What's there | Where |
|------|-------------|-------|
| **[data-portfolio](https://github.com/manuel-reyes-ml/data-portfolio)** | Portfolio hub — summaries, tech stacks, scope documents, skills badges | Separate repo |
| **[learning_journey](https://github.com/manuel-reyes-ml/learning_journey)** | Roadmap, learning log, and this project directory | This repo |
| Project repos | Source, tests, architecture, deployment (linked from the hub as each goes public) | Individual repos |

---

## 🔗 Quick Links

| Resource | Link |
|----------|------|
| 📊 Portfolio Hub | [data-portfolio](https://github.com/manuel-reyes-ml/data-portfolio) |
| 📋 Interactive Roadmap | [v10.0 roadmap (3 stages, ~32 months)](https://manuel-reyes-ml.github.io/learning_journey/roadmap.html) |
| 👤 GitHub Profile | [@manuel-reyes-ml](https://github.com/manuel-reyes-ml) |
| 🔗 LinkedIn | [Manuel Reyes](https://linkedin.com/in/mr410) |

---

### 💡 *Three flagships. One system per project, evolved S1 → S3. Production code, evaluation-gated, in a regulated domain.*

**[→ Full Portfolio Hub](https://github.com/manuel-reyes-ml/data-portfolio)** | **[→ Interactive Roadmap](https://manuel-reyes-ml.github.io/learning_journey/roadmap.html)**