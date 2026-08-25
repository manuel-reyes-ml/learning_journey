# 🚀 Learning Journey: Business Ops Professional → Applied AI Engineer (FDE Track)

**Evidence-First Career Transformation** | Production code with measurable impact | Systematic ~32-Month Journey

> **🟢 Open to AI-Focused Analytics Engineer** (first door) **and Data Engineer** (parallel) **roles.**
> **Current Stage:** Internal AI Builder (Stage 1 of 3) — *the build work, not a job title*
> **Next Milestone:** Flagship #1 (PolicyPulse) shipping with eval gates + DataVault S2 hardening (the stage-exit evidence gate)
> **Ultimate Goal:** Applied AI Engineer → Forward-Deployed Engineer (FDE) track
> **Study Commitment:** 25 hours/week systematic learning

[![Open to work](https://img.shields.io/badge/🟢_Open_to-Analytics_Engineer_·_Data_Engineer-success?style=flat-square)]()
[![Targeting](https://img.shields.io/badge/Targeting-Analytics_Engineer_·_Data_Engineer-4479A1?style=flat-square)]()
[![Current Stage](https://img.shields.io/badge/Stage-1%3A%20Internal%20AI%20Builder-green)]()
[![Study Hours](https://img.shields.io/badge/Weekly%20Hours-25-orange)]()
[![Timeline](https://img.shields.io/badge/Timeline-~32%20Months%20(3%20Stages)-blue)]()
[![Evidence-First](https://img.shields.io/badge/🤖_Evidence--First-Proof_over_Keywords-blueviolet)]()

📋 **[View Complete Interactive Roadmap (v10.0) →](https://manuel-reyes-ml.github.io/learning_journey/roadmap.html)**

> **🆕 v10.0 (2026 Market Realignment):** 5 stages → **3 stages** (~32 months). Path retitled **Internal AI Builder → AI-Focused Data Engineer / Analytics Engineer → Applied AI Engineer → FDE track**. Portfolio focused to **4 flagships + 2 supporting**. No external Data Analyst search (the 0–2 yr analyst band is contracting) — that ruling stands. Certifications trimmed to a purposeful **9 + 1 conditional**; **OMSCS (Computing Systems)** added as a parallel degree track.
>
> **🆕 v10.0 Corrections 22 + 32 (August 2026) — what changed:** the internal-elevation premise is retired. The former *fallback* (external DE/AE search) is now the **primary path**, targeted **Analytics Engineer first, Data Engineer in parallel**, apply window **~Q1 2027**. Stage 1 keeps its name because **the build work is unchanged and continues through the handover** — what retired is the employment premise. Its exit is now an **evidence gate: DataVault S2 hardening shipped**. **All certifications are self-funded** — no employer reimbursement applies to any of them; per-exam costs are now documented in each stage. Framing is **evidence over keywords**.

---

## 🗺️ Quick Navigation

**👔 For Recruiters / Hiring Managers:**
1. **[💼 Portfolio →](https://github.com/manuel-reyes-ml/data-portfolio)** — Live ETL system + 4 flagships ⭐ **START HERE**
2. **[🎯 Evidence-First Approach →](#-evidence-first-approach)** — How this is built
3. **[📊 Complete Roadmap →](https://manuel-reyes-ml.github.io/learning_journey/roadmap.html)** — 3-stage visualization
4. **[🔗 LinkedIn →](https://www.linkedin.com/in/mr410/)** — Professional background

**🎓 For Fellow Learners:**
1. **[🤖 AI Tools & Workflows →](#-ai-tools--workflows-integration)** — Stack and approach
2. **[📚 Repository Structure →](#-repository-structure)** — How this is organized
3. **[💡 Learning Philosophy →](#-learning-philosophy)** — Core principles
4. **[🛠️ Setup Guides →](./getting_started/)** — Environment configuration

---

## 💪 What Makes This Different

**Most learning repositories:** tutorial completions and course exercises with no real-world application.

**This repository demonstrates:**
- ✅ **Production system deployed** — a live ETL pipeline running in an ERISA-regulated retirement-plan operations environment, with public code and evaluation discipline
- ✅ **Focused portfolio: 4 flagships + 2 supporting** — real systems (Applied-AI, Data Engineering, autonomous-execution safety, and one dual-target system that evidences both doors at once), not a repo pile
- ✅ **Domain depth** — 15+ yrs business operations (manufacturing, digital marketing) + 2 yrs ERISA-regulated financial operations + 5+ yrs independent trading
- ✅ **Eval-first engineering** — DeepEval / RAGAS / GEval as **blocking gates** (faithfulness ≥ 0.9 for financial data)
- ✅ **Production standards** — typed Python, **`uv` + committed `uv.lock`**, `pyproject.toml` + `src/`, ruff/mypy, Docker, GitHub Actions CI, Conventional Commits **enforced by a `commit-msg` hook**, **a pinned `.pre-commit-config.yaml` in every repo**; **structured logging (`structlog`) with a PII-redaction processor**, typed config (`pydantic-settings`), capped retries (`stamina`); **no vibe coding** (every line understood before merge)
- ✅ **Measurable business impact** — **95% time reduction** and a derived-vs-reported validation gate that quarantines mismatches before distribution

**The key differentiator:** already delivering production value while building toward Data Engineering and Applied AI — with evaluation evidence that stands up to scrutiny.

---

## 🤖 Evidence-First Approach

The 2026 market is **saturated at the keyword layer and starved at the evidence layer.** Resumes are dense in RAG/evals/inference keywords with little substance; referrals and shipped production systems dominate. My position isn't more certificates or broader titles — it's **proof**: production systems with evaluation gates, deployed and measured.

### The 3-Stage Framework

Each stage compounds the same moat (finance/ERISA + trading depth + eval-first discipline) instead of resetting it.

**Stage 1: Internal AI Builder** (Months 1–8) 🟢 ACTIVE
```
Foundation:  Production Python (typed, uv + uv.lock, pyproject, ruff/mypy, pre-commit) + SQL + Docker/CI
+ AI Layer:  Anthropic SDK (structured outputs, tool use, prompt caching) + RAG + MCP literacy
+ Eval Layer: RAGAS/DeepEval as blocking gates, golden datasets, hallucination detection
+ Certs:     Azure AI Fundamentals (AI-901, $99) — committed
+             AI Agent Builder Associate (AB-620, ~$165) — CONDITIONAL (Microsoft-ecosystem trigger only)
             all self-funded — no employer reimbursement on any credential
= Result: PolicyPulse v1 shipping with eval gates + DataVault S2 hardening (the exit gate)
          → available 9 Oct 2026; external AE/DE search is the primary path
```

**Stage 2: AI-Focused Data Engineer / Analytics Engineer** (Months 9–20) 📅 PLANNED — *dual-target*
```
Foundation:  SQL at scale + dbt (tested project, CI-gated) + warehouse (Snowflake primary — "one deep"; BigQuery/Fabric awareness)
+ Pipelines: Airflow orchestration + Kafka streaming basics + PySpark
+ Governance: data contracts, dbt tests / Great Expectations, lineage, access-control awareness
+ Deploy:    Docker → ECS/Fargate + Terraform basics + monitoring + incident writeups
+ AI-adjacent: embedding pipelines + vector stores + unstructured-data ETL feeding RAG
= Result: DE flagship production-hardened; first external move (~M18–20); DP-700 + AWS DE Associate
```

**Stage 3: Applied AI Engineer → FDE Track** (Months 21–32) 📅 PLANNED
```
Foundation:  Production agentic systems (Building Effective Agents taxonomy) + MCP servers + HITL gates
+ Eval-as-eng: RAGAS/DeepEval/GEval as CI-blocking gates; SelfCheckGPT/FActScore for finance-grade rigor
+ ML-literacy: embeddings, inference economics, one small fine-tune AS LITERACY (Prompt→RAG→Fine-tune→Distill)
+ Privacy edge: privacy-routed architecture (PII local, proprietary via private endpoints)
+ FDE edge:   discovery & decomposition (the case-study round that filters most candidates) — ERISA client-facing background as the structural advantage
= Result: Applied AI Engineer (~M30); FDE apply list live at M32+; CCA-F + AI-103 + Databricks GenAI + Neo4j
```

### Why This Approach

| Keyword-Layer Path | Evidence-First Path (This Journey) |
|--------------------|------------------------------------|
| Certificate/keyword density | Shipped production systems with eval gates |
| Broad titles, title inflation | Sharp identity: AE/DE → Applied AI → FDE |
| Generic tutorial projects | Real production systems on owned data |
| "Prompts an LLM" | Builds, evaluates, deploys, and monitors LLM systems |

**Market context (2026):** model evaluation now appears in ~12% of AI/ML engineering postings and is repeatedly named the year's differentiator — while only ~6% of postings request any certification, and deployed systems outrank credentials. The real screen is the gap between *using* AI and being able to *verify, constrain, and evaluate* it — a gap that commands a documented wage premium (the majority of developers use AI tools; a minority trust the output). Applied-AI and FDE demand spans many industries — regulated-finance depth is one edge I bring, not the boundary.

---

## 🏆 Production & Portfolio Highlights

> **Focused portfolio: 4 flagships + 2 supporting**, built on a live production system.
>
> **🏗️ Production standard (every repo):** architecture diagram (Mermaid), **ADR set (`docs/adr/`) + C4 context diagram** (lead flagships add a C4 container view), Dockerfile, evaluation-metrics table (DeepEval), 15–30s demo GIF, and "What I Learned." **Non-negotiable standards:** no vibe coding, eval-first blocking gates, **synthetic data only** in public repos, `pyproject.toml` + **`uv.lock`** + `src/` + `py.typed` + ruff + mypy · **a pinned `.pre-commit-config.yaml` — hooks are a *strict subset* of the CI gate, so CI stays authoritative and nothing is checked locally that isn't also checked in CI** · **structured logging (`structlog` over stdlib via `ProcessorFormatter`) + PII redaction processor · typed config (`pydantic-settings`, `SecretStr` credentials) · capped jittered retries (`stamina`)**, Conventional Commits, earned-overlay policy (ML ships only if it beats the baseline). *Every image builds with `uv sync --frozen` — reproducible by construction.*

### 🏁 Flagship 1 — [PolicyPulse](https://github.com/manuel-reyes-ml/policypulse) · *Applied-AI* | 🔌 Exposes FastMCP server

**RAG → GraphRAG document intelligence** | "Ask Your Policies"

- **① Production** — Containerised RAG + **FastMCP** service; **RAGAS/DeepEval blocking gates are merge conditions**, not reports; confidence-gated escalation path.
- **② Cost** — Cost-per-query and p95 latency measured across inference substrates; local-vs-cloud routing policy; embedding/re-index cost.
- **③ Architecture** — GraphRAG (Neo4j + ChromaDB) · retrieval-strategy **ADRs with rejected alternatives** · C4 Context + Container · MCP read → approval-gated write boundary.

Answers retirement-plan policy questions with cited sources, auto-escalates when uncertain, and enforces **per-document access control at retrieval time** — a differentiator for sensitive-document use cases.

| Feature | Implementation |
|---------|----------------|
| **Retrieval** | Embeddings + ChromaDB; **GraphRAG hybrid (Neo4j + ChromaDB)** for multi-hop questions |
| **Grounding** | Every answer cites specific policy section & document |
| **Escalation** | Confidence gate → auto-generated ticket with context |
| **MCP Server** | FastMCP exposes retrieval as MCP tools (Cursor / Claude Desktop) |
| **Evaluation** | **RAGAS + DeepEval as blocking gates**; evaluator-optimizer retrieval loop |

**Tech:** Python • **Anthropic SDK (primary, Gemini fallback)** • ChromaDB • **Neo4j (GraphRAG)** • Gemini Embeddings • Streamlit • Pydantic • DeepEval • RAGAS • **FastMCP** • Docker • GitHub Actions CI

**Stages:** S1 (RAG + eval gates + FastMCP) → S3 (GraphRAG + access-control-aware retrieval + full eval suite)

---

### 🏁 Flagship 2 — [DataVault / 1099 Data Platform](https://github.com/manuel-reyes-ml/1099_reconciliation_pipeline) · *Data Engineering*

**Production financial data platform** — the live 1099 reconciliation pipeline, hardened end-to-end

- **① Production** — Live, depended-upon pipeline in a regulated environment — reconciliation success rate, freshness SLA, quarantine and retry behaviour, schema contracts, on-call reality.
- **② Cost** — 🔒 *Deliberately constrained.* Mechanism + non-identifying relative deltas + manual hours removed. No absolute figures — see the disclosure note above.
- **③ Architecture** — **ERISA-driven ADRs** (retention, auditability, reconciliation guarantees, PII boundary) · C4 Context + Container · dbt tests and data contracts.

An end-to-end production system: ingestion → **dbt-tested models (CI-gated)** → **orchestrated (Airflow)** → **data-quality contracts** → **deployed (Docker/ECS)** → **monitored**, with written incident/postmortems. Adds a **semantic / metrics layer** for the Analytics-Engineer story.

**Live impact (current state):** **95% time reduction** • scales to the full distribution book without added headcount • a **derived-vs-reported Box-7 validation gate** that quarantines mismatches before distribution • reconciliation success rate held against a stated freshness SLA.

> 🔒 *Regulated-environment disclosure: mechanism and non-identifying relative deltas only. No absolute cost figures, participant or plan data, client identifiers, or employer-identifying volumes — per the roadmap's v10.0 Correction 18 ERISA rule.*

| Layer | Implementation |
|-------|----------------|
| **Transformation** | **dbt** — tested models at real scale, docs alongside code, CI that gates merges |
| **Orchestration** | **Airflow** DAGs with retries, alerting, monitoring |
| **Quality & governance** | Data contracts, **dbt tests / Great Expectations**, lineage, access-control awareness |
| **Deploy & ops** | **Docker → ECS/Fargate**, Terraform basics, incident writeups |
| **Semantic layer** | Metric definitions + dashboard handoff (Power BI) — the AE differentiator |

**Tech:** Python • SQL • **dbt** • **Airflow** • **Snowflake** (primary) • BigQuery/Fabric awareness • DuckDB • Parquet • **Great Expectations** • Docker • **AWS (S3, ECS)** • **Terraform** • GitHub Actions CI

**Stages:** S1 (live, retro-migrated to production standards) → S2 (dbt/orchestration/contracts/deploy — *retains scheduling priority*; feeds the first external move) → S3 (adds the **DataVault Applied-AI layer** — NL-to-SQL over the semantic layer, HITL on every write)

---

### 🏁 Flagship 3 — [Crucible](https://github.com/manuel-reyes-ml/crucible) · *Autonomous Execution Research* | 🦙 Local-First AI

- **① Production** — Paper→live execution path with **mandatory human sign-off + kill-switch**, monitoring, and intended-vs-filled reconciliation.
- **② Cost** — Compute cost per backtest sweep, data-feed cost, sweep efficiency (results per compute-hour).
- **③ Architecture** — Multi-timeframe design · execution and risk-control ADRs · C4 Context + Container · `signalcore` boundary (primitives in, strategy logic out).

**Backtest → paper → live** autonomous **multi-timeframe (swing → intraday)** research platform. *"Does this strategy have a real edge that survives out-of-sample validation — and can an autonomous agent trade it without me babysitting it?"* *(Swing-first is the lower-risk on-ramp; intraday plugins follow once swing clears all three gates.)*

Production-safety engineering for an autonomous system handling irreversible actions: a **mandatory human-in-the-loop sign-off + kill-switch** on the live path, and an **"LLM behind the Wall"** information barrier — the model sees only in-sample aggregated stats, never raw ticker-date outcomes. A **verifier agent** sits before the human gate. Grounded in 5+ years of hands-on independent trading.

| Phase | What it produces | Stage | Real money? |
|-------|------------------|-------|-------------|
| **1 — Backtest Engine** | Own event-driven harness + AI research loop + sealed OOS vault; IT-1 ORB + VWAP Reclaim plugins | S1 | No |
| **2 — Paper Agent** | Migrate to NautilusTrader (engine-parity gate); autonomous paper agent crew (LangGraph); local Qwen3/Ollama analyst | S2–S3 | No |
| **3 — Live Agent** | Autonomous live micro-sizing on Alpaca + Schwab/TOS; deterministic core + multi-agent oversight | S3 | Yes (small) |

**Defensibility:** sealed OOS vault + logged overfitting budget + walk-forward CV • LLM behind the Wall • deterministic core owns every trade • published agentic evals (**Tool Correctness = 1.0**, **Task Completion > 0.8**) • verifier agent before the HITL gate.

**Tech:** Python • own harness → **NautilusTrader** • Optuna • DuckDB • Parquet • **Ollama/Qwen3 (local-first)** → Anthropic/Gemini • Pydantic • **LangGraph** • **Alpaca** + **Schwab/TOS** • DeepEval • Docker • GitHub Actions CI

> ⚖️ *Educational/research project. Not investment advice; makes no claim of positive expectancy — validation is the entire point.*

---

### 🏁 Flagship 4 — [PostCheck](https://github.com/manuel-reyes-ml/postcheck) · *Dual-target: Applied AI **and** Analytics/Data Engineering*

**The only project whose single deliverable produces first-class evidence for both target doors.**

- **① Production** — **Read-only and advisory — a binding, tested safety invariant.** Never keys, posts, reverses or corrects; never contacts a participant, advisor, TPA or sponsor; never edits SSN, name or DOB. An IGO verdict is a **recommendation to a human, never an authorization**.
- **② Cost** — Provider-agnostic across three named substrates (**Anthropic · Azure OpenAI via Microsoft Foundry · local Ollama**); one eval suite, gates run per substrate.
- **③ Architecture** — The spreadsheet is a **rendered export, never the source of truth** · declared grain (`fct_document_reviews` = one row per packet × review run) · ADRs + C4 Context + Container.

An autonomous **post-posting QA review agent** for regulated distribution operations. It watches an intake folder and claims each packet **exactly once** (event-as-hint + poll floor + content-hash idempotency + lease TTL), parses the posted-transaction export **deterministically** (row-type discriminator dispatch — *the LLM never sees the workbook*), segments and extracts a scanned multi-document packet with a multimodal model, routes on form family, resolves live-vs-dead payee legs, then adjudicates against a **versioned SOP** across a fixed 15-item verification surface (PASS / EXCEPTION / CRITICAL / N/A) → **IGO** / **NIGO (needs clarification)** / **NIGO (do not process)**.

Findings escalate to the human processor with field, form value, export value, **SOP citation** and fix. Every adjudication appends to an **event log feeding a dbt-modelled NIGO quality mart** — first-pass IGO rate, reason Pareto, reason-mix drift, agent-vs-human agreement.

| Door | What this system evidences |
|------|----------------------------|
| 🤖 **Applied AI** | Agentic adjudication with a **hard escalation boundary** · multimodal reasoning over scanned packets · three-layer eval with a blocking gate · MCP + HITL |
| 📊 **Analytics / Data Engineering** | **Exactly-once event ingestion** · deterministic parsing of a ragged block-structured source · **append-only event log with a declared grain** · dbt models + contracts · a metrics layer answering a real operational question |

**📏 Measured against a real incumbent** — a prompt-only reviewer already in use — so the headline is a genuine before/after rather than an unfalsifiable claim. Headline metric: **false-CRITICAL rate** versus a flattened-text baseline running the identical rule pack on the identical golden set. **The blocking gate is false-NIGO rate, not accuracy** (precision blocks, recall is reported). **Synthetic corpus only** — the controlled-NIGO-injection generator is itself a portfolio artifact and the only route to ground-truth labels.

> 🔀 **PostCheck is not FormSense.** FormSense sits **pre-index** — is this form complete, legible and internally consistent enough to file? It judges the form *against itself*. PostCheck sits **post-posting** — does the posted transaction match the request and comply with the SOP? It judges the form *against the posted export*. Different position in the workflow, different source of truth, different escalation target. **Never merged.**

**Tech:** Python • Anthropic SDK • Azure OpenAI / Microsoft Foundry • Ollama (local) • multimodal extraction • Pydantic • **dbt** • DeepEval • FastMCP • Docker • GitHub Actions CI

> 🗓️ **Scheduling:** the standard budget stays 25 hrs/week and the priority order when hours are scarce is **DataVault → PolicyPulse → Crucible**. PostCheck S1 is scoped to be **independently shippable and independently evidence-bearing**, so it never blocks the evidence gate.

---

### 🧩 Supporting — [FormSense](https://github.com/manuel-reyes-ml/formsense) · *Document AI*

- **① Production** — Deploy path (Docker + CI) with **GEval schema-adherence gates** as merge conditions; escalation routing on low confidence.
- **② Cost** — ⚪ Optional at supporting tier — not manufactured where there is nothing to report.
- **③ Architecture** — Frozen Pydantic schema contract · full ADR set + C4 Context · document → parse → validate → route boundary.

Multimodal **agentic workflow** (Anthropic *Building Effective Agents* taxonomy — precise vocabulary, *not* multi-agent) that extracts and validates synthetic ERISA distribution forms against a **frozen Pydantic schema contract**, with **GEval schema-adherence** gates and smart routing (complete → ticket | incomplete → advisor email).

**Tech:** Python • Vision LLM • Streamlit • Pydantic • DeepEval (GEval) • Docker • GitHub Actions CI · **Stages:** S1 → S3

---

### 🧩 Supporting — [Attention-Flow Catalyst (AFC)](https://github.com/manuel-reyes-ml/attention-flow-catalyst) · *Research*

- **① Production** — Read-only research loop; **faithfulness ≥ 0.9 as a blocking gate** — the eval-first premise is the deliverable.
- **② Cost** — ⚪ Optional at supporting tier. Where it applies: cost-per-screen-run and embedding/re-index cost.
- **③ Architecture** — GraphRAG (Neo4j + ChromaDB) · full ADR set + C4 Context · `signalcore` boundary (primitives in, thresholds out).

Read-only **GraphRAG** financial-research loop over small-cap trigger signals (insider buys, attention spikes, volume, dilution, squeeze-context), with a **faithfulness ≥ 0.9** evaluation showcase for financial-data sensitivity. Demonstrates bounded, unattended-safe agent design (read-only/verifiable).

**Tech:** Python • DuckDB • Parquet • httpx async • edgartools • **Neo4j + ChromaDB (GraphRAG)** • **Anthropic SDK** • DeepEval • SelfCheckGPT + FActScore • Docker • CI · **Stages:** S1 → S3 *(the SEC-grounded faithfulness benchmark is an S1 deliverable — the smallest publishable high-signal artifact; the GraphRAG research loop is S3)*

---

### 📅 Backlog (production-grade when built, positioned last)

- 📊 **[Operations-Demand-Intelligence](https://github.com/manuel-reyes-ml/operations-demand-intelligence)** — AI-powered workflow-demand analytics on enterprise OnBase data (consolidation candidate against the 1099 platform's mart/AI layer)
- 📺 **[StreamSmart Optimizer](https://github.com/manuel-reyes-ml/streamsmart-optimizer)** — consumer AI app (external APIs, async HTTP, optimization)

> **Note:** the former standalone *DataVault Analyst* (PandasAI / NL querying) is now the **S3 Applied-AI layer of Flagship 2** — text-to-SQL over the semantic layer with HITL on every write. No separate repo.

---

## 📂 Repository Structure

```
learning_journey/
│
├── 📄 README.md                          # This file — evidence-first overview
│
├── 📂 projects/                          # ⭐ Project directory (links to separate repos)
│   └── README.md                         # Portfolio index
│       ├── PolicyPulse (Flagship 1 — Applied AI: RAG→GraphRAG, FastMCP)
│       ├── DataVault / 1099 Data Platform (Flagship 2 — Data Engineering; live production)
│       ├── Crucible (Flagship 3 — autonomous execution: backtest→paper→live)
│       ├── PostCheck (Flagship 4 — dual-target: agentic QA review + dbt NIGO quality mart)
│       ├── FormSense (Supporting — multimodal agentic workflow)
│       ├── Attention-Flow Catalyst (Supporting — read-only GraphRAG research)
│       └── Backlog: Operations-Demand-Intelligence · StreamSmart  (DataVault = Flagship 2 S3 layer)
│
├── 📂 getting_started/                   # For new visitors (setup + AI tools)
│
├── 📂 courses/                           # Course-specific materials
│   ├── cs50_harvard/                     # CS fundamentals + OMSCS evidence
│   ├── python_for_everybody/             # Python foundation
│   ├── ibm_genai_engineering/            # 🤖 IBM GenAI Engineering (Stage 1 spine)
│   ├── anthropic_claude_api/             # Building with the Claude API (SDK source-of-truth)
│   ├── deeplearning_ai/                  # Evals, RAG, MCP, Agentic AI short courses
│   ├── aws_data_engineering/             # 📅 Stage 2 DE spine
│   ├── dbt_airflow_kafka/                # 📅 Stage 2 DE/AE tooling
│   └── ai_native_data_engineering/       # 📅 Stage 2 — vector schemas, PII-safe corpora, reproducible datasets
│
├── 📂 certifications/                    # Certificate tracking (9 + 1 conditional)
│   └── in-progress/
│       ├── ai-901-progress.md            # Azure AI Fundamentals (committed, self-funded)
│       ├── ab-620-progress.md            # AI Agent Builder Associate (⏸️ conditional)
│       ├── ibm-genai-engineering-progress.md
│       └── ...                            # DP-700, AWS DE, NCA-GENL, Databricks, Neo4j, AI-103, CCA-F
│
├── 📂 docs/                              # Documentation & GitHub Pages
│   ├── index.html                        # Landing page
│   └── roadmap.html                      # Interactive roadmap (v10.0)
│
├── 📂 notes/                             # Learning journal (learning-log.md, strict template)
│
├── .gitignore
├── .vscode/                              # VS Code settings
├── .pre-commit-config.yaml               # pinned hook set; strict subset of the CI gate
├── pyproject.toml                        # Python dependencies (PEP 621, uv-managed)
└── uv.lock                               # committed lockfile — reproducible installs
```

---

## 🎯 The ~32-Month Roadmap (3 Stages)

Systematic progression that compounds the finance/ERISA + trading + eval-first moat at every stage — the moat is never reset, whoever the employer is.

### Stage 1: Internal AI Builder (Months 1–8) 🟢 ACTIVE

> **Note on the name:** "Internal AI Builder" labels **the work**, not an employment status — the flagships keep shipping regardless of employer.

**Core:** Production Python (typed, **uv + `uv.lock`**, pyproject, ruff/mypy, **pre-commit**) • SQL • Docker/CI
**AI:** Anthropic SDK (structured outputs, tool use, prompt caching) • RAG • MCP literacy • Pydantic • Streamlit
**Eval:** RAGAS/DeepEval blocking gates • golden datasets • hallucination detection
**Certs (self-funded):** **AI-901 ($99)** — committed. **AB-620 (~$165) is conditional, not committed:** it is the low-code Copilot Studio maker path, and this portfolio's evidence standard is production Python — typed, tested, eval-gated, ADR-documented. Single activation trigger: a deliberate decision to specialize in the Microsoft ecosystem. The committed Azure-native credential is **AI-103** (code-first Foundry, Stage 3).
**Collaboration:** Git team workflow — **branch → PR → review → merge**, rebase and conflict resolution *(build target: the falsifiable proof is feature branches and self-reviewed PRs on the flagships, not a certificate)*
**Last mile:** TypeScript + Zod + **Vercel AI SDK 7** + React — a streaming Claude-powered UI over PolicyPulse retrieval. ⚠️ **Guardrail:** TypeScript is the **last mile only**; PolicyPulse, AFC and Crucible stay Python-primary and no agent core crosses the language boundary

**Learning path:** CS50x (Harvard) • **CS50P** (Harvard — Python, testing/debugging rigor) • **MITx 6.00.1x** (MIT — Python CS foundations) • Python for Everybody • AI Python for Beginners • Building with the Claude API (Anthropic Academy) • Improving Accuracy of LLM Apps • Building & Evaluating Advanced RAG • MCP primer • AI Prompting for Everyone • 30 Days of Streamlit • Docker for Beginners • **uv — Python packaging** (Astral official docs + Al Sweigart quickstart) • **pre-commit hooks** (Stefanie Molin's four-article series + `pre-commit.com` — *no certification exists for this and no substantive course does either; the shipped config is the evidence*) • *conditional:* **Conda Basics** (Anaconda — only if Crucible needs compiled/GPU backends) • **IBM Generative AI Engineering Professional Certificate** (Stage 1 spine)

**Deliverables:** PolicyPulse v1 (eval gates + FastMCP) • 1099 pipeline retro-migrated to production standards (incl. `pip → uv` migration) • AI-901 passed • two documented production automation wins

> **Exit criterion (evidence gate):** **DataVault S2 hardening shipped.** The prior internal-scope-change criterion is superseded — internal elevation can no longer occur. **Primary path:** external **Analytics Engineer** (first door) / **Data Engineer** (parallel) search, apply window **~Q1 2027**. *Not* a Data Analyst search, under any circumstance.

### Stage 2: Analytics Engineer (first door) / AI-Focused Data Engineer (Months 9–20) 🎯 PRIMARY PATH

> *"AI-focused" ≠ vanilla DE:* the target is data platforms built for AI workloads — AI-managed / AI-ready pipelines, embedding pipelines, vector stores, and unstructured-data ETL feeding RAG — not BI-only engineering.

**Core:** SQL at scale • **Polars** (default dataframe engine for ingestion and bulk transforms; pandas retained deliberately at the `openpyxl` template write and the plotting hand-off — the reviewable artifact is the ADR recording which engine owns which layer, plus a `.explain()` query plan, never a speed number on a small dataset) • **dbt** (tested project, CI-gated) • warehouse (**Snowflake** primary — the "one deep", canonical dbt pairing; BigQuery + Microsoft Fabric awareness) • **Airflow** • **Kafka** basics • **PySpark**
**Governance:** data contracts • dbt tests / Great Expectations • lineage • access-control awareness
**Deploy:** Docker → ECS/Fargate • **Terraform** basics • monitoring • incident writeups
**AI-adjacent:** embedding pipelines • vector stores • unstructured-data ETL feeding RAG

**Certs (self-funded):** **DP-700** ($165) + **AWS Certified Data Engineer – Associate** (DEA-C01, $150) + *conditional menu: dbt Analytics Engineering (**~$200** — the tested dbt project with CI is the primary signal; the cert is a tiebreaker, not the unlock)* + **ONE optional lakehouse cert**

> **Lakehouse slot — three co-equal options, take exactly ONE**, matched to a target employer's stack, never stacked: **DP-750** ($165) · **SnowPro Core** (COF-C03, $175) · **Databricks DE Associate** ($200). *No default is set on purpose — with the funding advantage gone they sit within $35 of each other, and the deciding input is the target employer's stack, which isn't knowable until the apply window.*

**AI-native depth (Correction 43):** the **IBM AI-Native Data Engineering Professional Certificate** (7 courses, Coursera Plus) sits in Stage 2 for the three layers with no prior coverage — **vector schemas + retrieval governance**, **PII-safe corpus preparation and citation-grade chunking**, and **reproducible ML-ready datasets** (leakage, contamination, point-in-time correctness, CI gates for schema/slice/drift/bias). Scope chosen at enrolment; subordinate to the DataVault S2 ship, which it never competes with.

**Key deliverable:** DataVault production-hardened (**the Stage 1 exit gate**); first external offer — apply window **~Q1 2027**

### Stage 3: Applied AI Engineer → FDE Track (Months 21–32) 📅 PLANNED

**Core:** production agentic systems (Building Effective Agents taxonomy) • MCP servers in anger • HITL gates for irreversible actions • unattended-safe design for read-only/verifiable agents
**Eval-as-engineering:** RAGAS/DeepEval/GEval as CI-blocking gates • SelfCheckGPT/FActScore for finance-grade rigor • eval dashboards as portfolio artifacts
**ML-literacy module (2–3 months, embedded):** embeddings in depth • inference economics • one small fine-tune AS LITERACY (Prompt→RAG→Fine-tune→Distill) — *substituted by OMSCS coursework if the degree track is active*
**Privacy/compliance edge:** privacy-routed architecture • per-document access clearance at retrieval time

**🎯 FDE differentiator — Discovery & Decomposition (first-class skill):** FDE loops run a system-design round, a decomposition/open-ended case study (the round where most technically-strong candidates wash out), and a client-simulation role-play — with customer discovery and communication weighted at roughly half the evaluation, and graders scoring the *process* (clarifying questions before solutioning, clean decomposition, prioritization, transparent trade-offs) over the final answer. My **ERISA client-facing operations background is the structural edge on exactly the round that eliminates most candidates.** Portfolio proof: every flagship carries an **ADR set + C4 diagram** for architecture-defense rehearsal.

**Certs (self-funded):** **Anthropic CCA-F** (~$125 — ⚠️ *confirm price and the Claude Partner Network access route at booking; both post-date the Pearson VUE migration*) + **Azure AI-103** ($165 — code-first Foundry counterpart to CCA-F) + **Databricks Certified GenAI Engineer Associate** ($200) + **NVIDIA NCA-GENL** ($125) + **Neo4j Certified Professional** (**free**)

**Key deliverable:** Applied AI Engineer role (~M30); one public talk on a deployed system; FDE apply list live at M32+ (across industries; remote-normal routes weighted)

### 🎓 Parallel Degree Track — Georgia Tech OMSCS (Computing Systems)

Accredited M.S. Computer Science (~$8–9K total), Computing Systems specialization (distributed systems, databases, OS, architecture). Mapped to Stages 2–3 as a substitute for redundant self-study; AI/ML electives substitute for the Stage 3 ML-literacy module. Academic projects kept **architecturally separate** from public repos.

**📋 [View Interactive Roadmap →](https://manuel-reyes-ml.github.io/learning_journey/roadmap.html)**

---

## 🤖 AI Tools & Workflows Integration

### Current Stack (Stage 1)

**Development:**
- **VS Code** (first-class editor) — Python, SQL, Jupyter notebooks
- **Cursor AI IDE** — AI pair programming (with `.cursor/rules` scoped rules)
- **OpenCode** — agentic harness (custom agents, slash commands); local `qwen3.5-16k` Modelfile
- **uv (Astral)** — package/environment manager for every repo (`uv init` / `uv add` / `uv run`); committed `uv.lock` = reproducible installs. Replaces pip + virtualenv + pip-tools + pyenv
- **Conda (Anaconda)** — ⏸️ *conditional, Crucible only* — reserved for compiled numerical / CUDA / BLAS backends where binary channels beat wheels; never mixed with uv in one environment

**GenAI Engineering:**
- **Anthropic SDK** — *primary* provider (structured outputs, tool use, prompt caching); PolicyPulse + AFC
- **Gemini SDK** — fallback (embeddings, multimodal Vision, cheap safety-judge)
- **Ollama + LM Studio (local-first)** — privacy-routed models; finance/proprietary data stays on-machine
- **Pydantic** — structured-output validation • **ChromaDB** — vector store • **Neo4j** — GraphRAG hybrid retrieval
- **FastMCP** — MCP servers exposing retrieval as tools • **LangChain / LangGraph** — agentic workflows
- **OpenRouter** — PAYG routing for bulk agentic work
- **Vercel AI SDK 7 + TypeScript/Zod + React** — the **last-mile layer**: a streaming Claude-powered UI over PolicyPulse retrieval. **Model-call ownership is ruled, not left ambiguous:** the Next.js route handler owns the call for the single-turn chat and invokes retrieval as a tool; **Python owns the agentic loop**, GraphRAG fusion, access-control retrieval and the full eval suite. ⚠️ **No agent core crosses the language boundary**

**AI Evaluation (cross-project standard):**
- **DeepEval + pytest** — eval-driven development in CI • **RAGAS** — RAG Triad metrics (PolicyPulse)
- **GEval** — schema-adherence (FormSense) • **SelfCheckGPT + FActScore** — hallucination rigor (AFC)
- **Thresholds:** faithfulness ≥ 0.9 (AFC) • GEval ≥ 0.85 (FormSense) • Tool Correctness = 1.0 / Task Completion > 0.8 (agentic)

**Containerization:** Docker (Dockerfile for every repo; Stage 1 fundamentals via KodeKloud) — images build via `uv sync --frozen` for byte-reproducible dependency installs

### Integration Principles
**Transparency:** document AI assistance in commits • **Team-workflow discipline:** branch → PR → self-review → merge on the flagships, rather than direct commits to `main` — *the checkable artifact, since a solo portfolio has no second reviewer to prove it any other way* • **Validation:** always test AI-generated code • **No vibe coding:** every line understood before merge, diff-review-before-merge, manual commit as the final control gate — with **pre-commit as the automated gate in front of it** (secrets, notebook output, lockfile drift and commit format are caught mechanically, so human review is spent on logic rather than lint) • **Privacy-first routing:** PII/proprietary local, proprietary via private endpoints, public scaffolding only on free tiers

### Evolution Path

| Stage | AI Tools & Frameworks |
|-------|----------------------|
| **2** | **Polars** + dbt + Airflow + Kafka + PySpark + Snowflake (primary)/BigQuery/Fabric + vector DBs + embedding pipelines + **PII-safe unstructured-data ETL** + **reproducible ML-ready datasets (point-in-time correctness)** + Docker→ECS + Terraform |
| **3** | Agentic AI (Andrew Ng) + MCP servers (full) + LangGraph + long-term agentic memory + HuggingFace NLP (local embeddings) + Neo4j GraphAcademy + PEFT (literacy) + vLLM inference economics |

---

## 💻 Development Environment

**Editors & workflow:**
- **VS Code** (primary) — Python, SQL, Jupyter notebooks
- **Cursor AI** (AI pair programming) + a **dual agentic harness — OpenCode + Claude Code** — governed by one portable `AGENTS.md` contract and a shared prompt-extraction layer, so the same standards drive both and nothing is duplicated
- **Make** (task automation via `Makefile`) • **Git** + Conventional Commits
- **uv** (packages, virtual envs, Python versions) — `uv run` replaces manual venv activation

**Languages & data:**
- **Python 3.14** (standard GIL build — the free-threaded `python3.14t` build is deliberately **not** used; no CPU-bound multicore workload here, and it is where the C-extension wheel problems live), SQL
- **Polars** (default engine), pandas (boundary-scoped), NumPy, DuckDB, Parquet, Matplotlib, Seaborn, Plotly
- Databases: SQLite, DuckDB, ChromaDB, Neo4j, PostgreSQL (Stage 2)

**AI / GenAI:**
- Anthropic SDK (primary), Gemini, OpenAI, Ollama/LM Studio (local)
- Pydantic, LangChain/LangGraph, FastMCP, Streamlit

**Evaluation:**
- DeepEval + pytest, RAGAS, GEval, SelfCheckGPT, FActScore, LangSmith

**Containerization & CI:**
- Docker → Kubernetes (Stage 2), GitHub Actions CI

**Production standards:**
- **Commit-boundary enforcement: pinned `.pre-commit-config.yaml`** — `ruff-check --fix` ordered *before* `ruff-format`, `uv-lock` (keeps the lockfile honest), `gitleaks` + `detect-private-key`, `nbstripout` wherever notebooks exist, and `conventional-pre-commit` on the `commit-msg` stage. **`mypy` is deliberately CI-only** — the `mirrors-mypy` hook's default `--ignore-missing-imports` silently degrades third-party types to `Any`; the exclusion is recorded as an ADR rather than left as an omission
- `pyproject.toml` + **`uv.lock`** + `src/` + `py.typed`, ruff format, mypy (3.14) · **structured logging (`structlog` + `ProcessorFormatter`) + PII redaction processor · typed config (`pydantic-settings`) · capped retries (`stamina`)**, Conventional Commits
- Dependency management: **uv** (`uv add`, `uv sync --frozen` in CI/Docker) — **no `requirements.txt` anywhere**
- **Single-source Python pin:** the version is declared **once** as `requires-python = ">=3.14"` in `pyproject.toml`; `[tool.ruff] target-version`, `[tool.mypy] python_version`, the Dockerfile base image and the CI matrix all read from it. **A mismatch is a CI failure, not a lint warning**

```bash
git clone https://github.com/manuel-reyes-ml/learning_journey.git
cd learning_journey
open getting_started/SETUP_GUIDE.md          # setup incl. AI tools
uv sync                                      # creates .venv + installs from uv.lock
uv run pre-commit install --hook-type commit-msg   # installs the pinned hook set
uv run python getting_started/environment-verification.py
```

---

## 💡 Learning Philosophy

### Core Principles
- **Evidence over keywords:** ship production systems with eval gates, not certificate density
- **Eval-first discipline:** DeepEval/RAGAS/GEval as blocking gates, not afterthoughts
- **No vibe coding:** every line intentionally written and understood before merge
- **Production-first:** proper error handling, testing, typed code, documentation
- **Replace, not stack:** every new cert/course must displace something of lesser signal
- **Domain application:** apply every skill to real problems (finance/ERISA depth is one edge, not the only lane)
- **Systematic progression:** clear 3-stage path with measurable milestones

### Beyond Basic Completion
- Every exercise is enhanced with real-world application, error handling, tests, and eval gates
- AI assistance is documented transparently in commits
- Learning is logged in `notes/learning-log.md` under a strict entry template — source, format, stage tag, project tags, a takeaway in my own words, and an "Apply" line tied to a specific project

---

## 📊 Current Progress

**Availability:** 🟢 **Open to roles** — AI-Focused Analytics Engineer (first door) · Data Engineer (parallel)
**Active Stage:** 1 of 3 (Internal AI Builder — *the work*, exiting on an evidence gate)
**Portfolio:** 4 flagships (PolicyPulse, DataVault / 1099 Platform [live], Crucible, PostCheck) • 2 supporting (FormSense, AFC) • backlog (ODI, StreamSmart)
**Certifications:** 9 + 1 conditional — **all self-funded**. **Eight committed ≈ $1,029** across S1–S3; ≈ **$1,594** full-canon ceiling if every conditional is taken (optional lakehouse slot ~$165–200, dbt AE ~$200, AB-620 ~$165)
**Study Hours:** 25/week consistent

**Next milestones:**
- PolicyPulse v1 shipped (RAG + eval gates + FastMCP)
- **DataVault S2 hardening — the Stage 1 exit gate**
- AI-901 passed (AB-620 held as conditional)
- Vercel AI SDK 7 last-mile UI over PolicyPulse retrieval (fresh for the Q1 2027 window)
- Feature-branch + PR workflow visible across the flagship repos
- IBM GenAI Engineering Professional Certificate completed; CS50 on track for OMSCS window

---

## 🔗 Connect & Collaborate

**Professional:**
- **LinkedIn:** [Manuel Reyes](https://www.linkedin.com/in/mr410/)
- **GitHub:** [@manuel-reyes-ml](https://github.com/manuel-reyes-ml)
- **Email:** manuelreyesv410@gmail.com

**Portfolio:**
- [1099 Data Platform](https://github.com/manuel-reyes-ml/1099_reconciliation_pipeline) 🏁 Flagship 2 — Data Engineering (live)
- [PolicyPulse](https://github.com/manuel-reyes-ml/policypulse) 🏁 Flagship 1 — Applied AI
- [Crucible](https://github.com/manuel-reyes-ml/crucible) 🏁 Flagship 3 — Autonomous execution
- [FormSense](https://github.com/manuel-reyes-ml/formsense) 🧩 Supporting — Document AI
- [Attention-Flow Catalyst](https://github.com/manuel-reyes-ml/attention-flow-catalyst) 🧩 Supporting — Research
- Backlog: [Operations-Demand-Intelligence](https://github.com/manuel-reyes-ml/operations-demand-intelligence) · [StreamSmart Optimizer](https://github.com/manuel-reyes-ml/streamsmart-optimizer) — *DataVault NL-analytics is folded into Flagship 2 as its S3 Applied-AI layer*

**Open to:**
- 💼 Data Engineer / Analytics Engineer roles (dual-target; AE more remote-accessible)
- 🤖 Applied AI / Forward-Deployed Engineer roles across industries
- 🤝 Code reviews, technical discussions, knowledge exchange on data + AI + finance

---

## 💭 The Vision

This repository documents a complete career transformation: from business-ops professional to **Applied AI Engineer on the FDE track**, with production evidence and evaluation discipline from Day 1.

**What this represents:**
- ~32-month systematic journey with measurable milestones
- A focused portfolio (4 flagships + 2 supporting) spanning Applied AI, Data Engineering, autonomous-systems safety, and regulated-operations QA
- Production systems with real business impact
- An evidence-first approach: proof that stands up to scrutiny, not keyword density

**Ultimate goal:** Applied AI Engineer → Forward-Deployed Engineer, combining deep finance/ERISA and trading expertise with production agentic AI behind evaluation gates and safety barriers.

---

## ⭐ Follow the Journey

Real-time documentation of an evidence-first career transformation.

- ⭐ **Star this repository** to follow the journey
- 🔔 **Watch** for updates on project progress and eval results
- 🔗 **Connect** for professional discussions and collaboration

---

### 💡 *"~32 months. 4 flagships. Evidence over keywords. Production code with measurable impact. Clear trajectory."*

**Current Stage:** Internal AI Builder (1 of 3) | 🟢 Active • Building in Public • Deploying Production Systems

**[→ View Live Progress & Interactive Roadmap](https://manuel-reyes-ml.github.io/learning_journey/)**