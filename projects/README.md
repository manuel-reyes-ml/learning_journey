# 🚀 Project Portfolio Directory

**8 Production-Grade Projects** | Skills Progression | GenAI-First from Day 1 | Two Flagships

> **Portfolio Hub:** **[data-portfolio →](https://github.com/manuel-reyes-ml/data-portfolio)** for full project summaries, tech stacks, and skills badges.

---

## 📌 Project Pipeline (Easy → Flagship)

Each project introduces new capabilities that build on the previous — demonstrating systematic skill growth, not scattered tutorials.

> 🏗️ **Production Standard (v8.9):** Every project ships with architecture diagram (Mermaid), Dockerfile, evaluation metrics table (DeepEval + pytest), demo GIF, and "What I Learned" section. Flagship projects (PolicyPulse, AFC, Crucible) add advanced rigor — FastMCP server + hallucination detection (SelfCheckGPT/FActScore) for the research systems; sealed out-of-sample vault + overfitting-budget ledger + engine-parity gate for Crucible.

| # | Project | What It Does | New Skills Added | Status |
|---|---------|-------------|-----------------|--------|
| 1 | 🧾 **[1099 Reconciliation Pipeline](https://github.com/manuel-reyes-ml/1099_reconciliation_pipeline)** | ETL reconciling retirement plan data between financial systems | ETL, pandas, pytest, CI/CD | ✅ **Production** |
| 2 | 🔐 **[DataVault Analyst](https://github.com/manuel-reyes-ml/datavault-analyst)** | PII-safe "Chat With Your Data" for retirement plan operations | + LLM SDK, PandasAI, Pydantic, PII governance | 📅 Next |
| 3 | 📋 **[PolicyPulse](https://github.com/manuel-reyes-ml/policypulse)** | RAG chatbot answering HR policy questions with cited sources + **exposes FastMCP server** | + Embeddings, ChromaDB, RAG, semantic search, RAG Triad evaluation, **FastMCP server, Anthropic SDK primary** · *upgrade path:* **GraphRAG hybrid (Neo4j + ChromaDB)** | 📅 Planned |
| 4 | 📄 **[FormSense](https://github.com/manuel-reyes-ml/formsense)** | Vision AI reads handwritten distribution forms and routes them | + Multimodal AI (Gemini Vision), business rule validation | 📅 Planned |
| 5 | 📊 **[Operations-Demand-Intelligence](https://github.com/manuel-reyes-ml/operations-demand-intelligence)** | AI-powered workflow demand analysis for staffing decisions | + Enterprise real data, advanced analytics, Plotly | 🚧 In Dev |
| 6 | 📺 **[StreamSmart Optimizer](https://github.com/manuel-reyes-ml/streamsmart-optimizer)** | AI streaming subscription rotation advisor with live APIs | + External APIs, consumer UX, async HTTP, optimization | 📅 Planned |
| 7 | 📈 **[Attention-Flow Catalyst](https://github.com/manuel-reyes-ml/attention-flow-catalyst)** 🚀 | Predictive trigger analysis for small-cap stocks (5-stage flagship) | + Statistical methodology, DuckDB, async, multi-source data (6 triggers incl. **T6 Squeeze-Context**), **Financial Knowledge Graph (Neo4j)**, **financial-grade eval (SelfCheckGPT + FActScore, 0.9 faithfulness)** | 🚧 Phase 1A |
| 8 | 🔥 **[Crucible](https://github.com/manuel-reyes-ml/crucible)** 🚀 | Autonomous intraday trading research platform: backtest → paper → live, AI behind a sealed out-of-sample vault (flagship #2, started first) | + Own backtest harness → NautilusTrader, deterministic strategy plugins, sealed OOS vault + overfitting budget, **local-first LLM (Qwen3/Ollama)**, LangGraph multi-agent execution, Alpaca + Schwab/TOS, **human-in-the-loop sign-off + kill-switch on live** | 🚧 Phase 1 |

---

## 🏆 Production Highlight

### 🧾 [1099 Reconciliation ETL Pipeline](https://github.com/manuel-reyes-ml/1099_reconciliation_pipeline) — ✅ Live at Daybright Financial

| ⚡ 95% time reduction | 💰 $15,000+/year savings | 📊 10x scalability | ✅ Zero errors |
|---|---|---|---|

---

## 🚀 Flagship Highlight

### 📈 [Attention-Flow Catalyst](https://github.com/manuel-reyes-ml/attention-flow-catalyst) — 🚀 Evolves Through All 5 Career Stages

> **Research Question:** Which trigger or combination best predicts +10% price moves within 3 trading days?

| Stage | Evolution | AI Integration |
|-------|-----------|----------------|
| **1** (Active) | Statistical backtesting + signal leaderboard | LLM SDK chat, PandasAI, AI insights |
| **2** | AWS pipelines, 500+ tickers, vector + graph storage | RAG infrastructure, embedding pipelines, GraphRAG (Neo4j) |
| **3** | ML predictions, ensemble models | Local LLMs (Ollama), fine-tuned financial models |
| **4** | Agentic AI trading system | Loop Engineering (autonomous agents, human-in-the-loop gates) + Multi-agent orchestration with named patterns (orchestrator-workers, sequential, evaluator-optimizer per Anthropic's "Building Effective Agents") + MCP servers per worker + LangGraph |
| **5** | Production deployment + monetization | A2A protocol for multi-tenant SaaS (Researcher-Agent ↔ Risk-Agent ↔ Compliance-Agent), LLMOps testing, CI/CD for AI, monitoring |

**What makes it defensible:** Walk-forward validation • survivorship bias controls • real SEC data • 6-trigger framework (incl. T6 squeeze-context) • Financial Knowledge Graph (Neo4j) capstone • 6 years trading domain expertise codified into algorithms

---

## 🔥 Flagship Highlight #2

### 🔥 [Crucible](https://github.com/manuel-reyes-ml/crucible) — Autonomous Intraday Trading Research Platform (started first)

> **The question it answers, for any strategy:** *Does this have a real edge that survives out-of-sample validation — and can an autonomous agent trade it without me babysitting it?*

**Distinct from AFC (why two flagships, not redundancy):** AFC is *read-only research* on illiquid sub-$5 small-caps over a multi-day *swing* horizon. Crucible is *autonomous execution* on liquid names over an *intraday* horizon. ~70% shared engineering spine, two genuinely different hard problems.

**The core idea — AI behind a wall:** an LLM research analyst proposes strategy improvements, but its ideas are *proved* by deterministic backtests it never optimizes against. The out-of-sample set is a sealed vault opened once per finalized hypothesis, every peek logged in an overfitting-budget ledger. Strategies are plugins (Protocol + ABC + registry) — IT-1 ORB + VWAP Reclaim ship together in Phase 1 to prove adding one needs zero engine changes.

| Phase | Evolution | Stage | Real money? |
|-------|-----------|-------|-------------|
| **1 — Backtest Engine** | Own event-driven harness + AI research loop + sealed OOS vault (IT-1 ORB + VWAP Reclaim) | Stage 1 | No |
| **2 — Paper Agent** | Migrate to NautilusTrader (engine-parity gate); autonomous paper-trading crew (LangGraph); local Qwen3/Ollama analyst | Stages 2–3 | No |
| **3 — Live Agent** | Autonomous micro-sizing on Alpaca + Schwab/TOS; deterministic core + multi-agent oversight | Stages 3–4 | Yes (small) |

**What makes it defensible:** Sealed out-of-sample vault • logged overfitting budget • walk-forward CV • engine-parity gate (own harness vs. Nautilus) • deterministic execution core (LLM never in the trade loop) • mandatory human-in-the-loop sign-off + kill-switch on live execution • local-first AI (no API fee, data stays local)

> ⚖️ *Educational/research project. Not investment advice; makes no claim of positive expectancy — validation is the entire point.*

---

## 🗂️ Repository Strategy

Each project lives in its own repo for clean version control, focused documentation, and recruiter-friendly links.

| Repo Type | What's There | Where |
|-----------|-------------|-------|
| **Project repos** (×8) | Source code, tests, architecture, deployment | Individual repos linked above |
| **[data-portfolio](https://github.com/manuel-reyes-ml/data-portfolio)** | Portfolio hub with summaries + full skills badges | Separate repo |
| **[learning_journey](https://github.com/manuel-reyes-ml/learning_journey)** | Courses, certifications, roadmap, this directory | This repo |

---

## 🛠️ Quality Standards (All Projects)

**Code:** Type hints • NumPy-style docstrings • error handling • modular design • clean commit history

**Testing & CI:** pytest • DeepEval evaluation framework • GitHub Actions CI • synthetic test data (no client PII)

**AI Integration:** Production guardrails (read-only, cost controls, disclaimers) • transparent AI assistance • Pydantic-validated outputs

**AI Evaluation:** DeepEval + pytest across all projects • RAGAS RAG Triad metrics (PolicyPulse) • SelfCheckGPT (PolicyPulse + AFC) • FActScore (AFC, financial-grade rigor) • LangSmith observability (StreamSmart)

**Containerization:** Dockerfile in every project • Docker for Beginners (KodeKloud) foundation

**Documentation:** Problem → solution → impact • Mermaid architecture diagrams • setup instructions • demo GIF • "What I Learned" section

---

## 🔗 Quick Links

| Resource | Link |
|----------|------|
| 📊 **Portfolio Hub** | [data-portfolio](https://github.com/manuel-reyes-ml/data-portfolio) |
| 📋 **Interactive Roadmap** | [37-Month Roadmap (v8.9)](https://manuel-reyes-ml.github.io/learning_journey/roadmap.html) |
| 👤 **GitHub Profile** | [@manuel-reyes-ml](https://github.com/manuel-reyes-ml) |
| 🔗 **LinkedIn** | [Manuel Reyes](https://linkedin.com/in/mr410) |

---

### 💡 *"8 projects. Two flagships. Skills progression. Production code from Day 1."*

**[→ Full Portfolio Hub](https://github.com/manuel-reyes-ml/data-portfolio)** | **[→ Interactive Roadmap](https://manuel-reyes-ml.github.io/learning_journey/roadmap.html)**