# 🚀 Project Portfolio Directory

**3 Flagships + 2 Supporting** | One system per project, evolved S1 → S3 | Evidence-first, evaluation-gated

> **Portfolio Hub:** **[data-portfolio →](https://github.com/manuel-reyes-ml/data-portfolio)** for full project summaries, tech stacks, scope documents, and skills badges. This page is the index that lives alongside the roadmap.

Aligned to the **[v10.0 career roadmap](https://manuel-reyes-ml.github.io/learning_journey/roadmap.html)** — 3 stages, ~32 months.

---

## 📌 Project Pipeline (S1 → S3)

Each project is **one system that evolves across stages**, not a set of scattered tutorials. *Flagship vs supporting denotes size and emphasis — not a quality tier; every project carries the full production standard.*

| # | Project | Role | What it does | Status |
|---|---------|------|-------------|--------|
| 1 | 🧾 **1099 / DataVault Data Platform** | 🚩 Flagship — Data Engineering | 1099 reconciliation core → dbt-tested platform (CI) → Applied-AI natural-language analyst layer (HITL on every write) | ✅ **S1 core live** |
| 2 | 📋 **PolicyPulse** | 🚩 Flagship — Applied AI (RAG) | Cited-source RAG over plan documents → GraphRAG hybrid (Neo4j + ChromaDB) → agentic + eval/observability; exposes a **FastMCP server** | 🏗️ **S1 shipping** |
| 3 | 🔥 **Crucible** | 🚩 Flagship — Autonomous trading research | Multi-timeframe (swing → intraday) backtest → paper → live through validation gates; **HITL sign-off + kill-switch** on the live path | 🏗️ **S1 in progress** |
| 4 | 📈 **Attention-Flow Catalyst (AFC)** | Supporting — Research | Eval-first core: SEC-grounded faithfulness benchmark + controlled-perturbation catalog; GraphRAG financial-KG | 🏗️ **S1 core** |
| 5 | 📄 **FormSense** | Supporting — Document ops | Multimodal structured extraction from distribution forms; Pydantic frozen-schema contract; agentic workflow | 📅 Planned |
| 6 | 📺 **StreamSmart** · 📊 **ODI** | Backlog | Consumer subscription optimizer · enterprise demand analytics (ODI = consolidation candidate) | 🗒️ Backlog |

> Shared library: **`signalcore`** — point-in-time-safe primitives beneath AFC + Crucible (siblings, no merge). Content tooling: **Cadence** (build-in-public pipeline — a tool, not a portfolio flagship).

---

## 🏆 Production Highlight

### 🧾 1099 / DataVault Data Platform (S1 core) — ✅ Live at Daybright Financial

| ⚡ ~95% time reduction | 💰 ~$15,000/year savings | 📊 10× scalability | ✅ Caught a tax-code error a manual pass missed |
|---|---|---|---|

Ingests Matrix + Relius into a canonical model, reconciles them, derives Box-7 codes, and surfaces corrections analytics. The public build uses synthetic data only; the production deployment runs internally on regulated data.

---

## 🚩 Flagship Highlights

### 📋 PolicyPulse — Applied-AI flagship (RAG)
Retrieval-augmented answering over retirement-plan documents with cited sources and confidence-gated escalation; exposes a **FastMCP server**. Evolves from vector RAG (S1) → **GraphRAG hybrid (Neo4j + ChromaDB)** for multi-hop questions (S2/S3) → agentic workflows with a three-layer eval spine (per-query metrics + trajectory tracing + drift vs. a frozen golden set).

### 🧾 1099 / DataVault Data Platform — Data-Engineering flagship
One system across the arc. **S1:** the live 1099 reconciliation core. **S2:** hardened into a platform — dbt-tested models (CI-gated), orchestration (Airflow), data contracts, containerized deploy, monitoring, one written incident/postmortem. **S3:** the Applied-AI analyst layer (natural-language querying) with **human-in-the-loop on every write**.

### 🔥 Crucible — Autonomous trading-research flagship (started first)

> **The question it answers, for any strategy:** *Does this have a real edge that survives out-of-sample validation — and can an autonomous agent trade it without babysitting?*

**Multi-timeframe (swing → intraday):** swing-first is the lower-risk on-ramp; intraday plugins follow once swing clears all three integrity gates. **AI behind the Wall:** an LLM proposes strategy improvements, but they're *proved* by deterministic backtests it never optimizes against — the out-of-sample set is a sealed vault, every peek logged in an overfitting-budget ledger. Strategies are plugins (Protocol + ABC + registry).

| Stage | Evolution | Live money? |
|-------|-----------|-------------|
| **S1** | Own event-driven backtest harness + AI research loop + integrity spine (sealed OOS vault · overfitting ledger · engine-parity gate) | No |
| **S2** | Migrate to NautilusTrader (engine-parity gate); autonomous paper crew (LangGraph); local Qwen/Ollama analyst | No |
| **S3** | Autonomous micro-sizing (Alpaca); deterministic core + multi-agent oversight; **mandatory HITL sign-off + kill-switch** | Yes (small) |

**Distinct from AFC (why both, not redundancy):** AFC is *read-only research* on illiquid sub-$5 small-caps over a multi-day *swing* horizon; Crucible is *autonomous execution* on liquid names *intraday*. ~70% shared engineering spine (`signalcore`), two genuinely different hard problems.

> ⚖️ *Educational/research project. Not investment advice; makes no claim of positive expectancy — validation is the entire point.*

**Supporting projects:** AFC (eval-first research core → GraphRAG financial-KG) and FormSense (multimodal document ops) carry the same production standard at smaller scope.

---

## 🏗️ Production Standard (v10.0 — all projects)

Every project ships with a **Mermaid diagram + C4 Context diagram** (+ Container view on lead flagships) · **`docs/adr/`** numbered Architecture Decision Records (context → decision → consequences) · Dockerfile · evaluation-metrics table · demo GIF · "What I Learned" · **eval-first blocking gates** · **synthetic data only** in public repos · `pyproject.toml` + `src/` + `py.typed` + ruff + mypy · Conventional Commits. *Stage 3 adds an ADR set + an architecture-defense rehearsal — present and defend the design against a reviewer, mirroring the FDE panel format.*

**Evaluation:** DeepEval + pytest across all projects · RAGAS (PolicyPulse) · SelfCheckGPT (PolicyPulse + AFC) · FActScore (AFC) · Arize Phoenix observability.

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