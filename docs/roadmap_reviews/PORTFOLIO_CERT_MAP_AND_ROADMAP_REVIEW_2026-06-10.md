# 🎓 Portfolio Certificate Map & Roadmap Cert Evaluation — Review-First Summary

**Prepared:** June 10, 2026
**Sources reviewed:** GitHub profile README (project order), `roadmap.html` v8.3, and 8 project scopes (DataVault, PolicyPulse, FormSense, ODI, StreamSmart ×2, AFC, Crucible). AFC's courses were already mapped in `AFC_EVAL_FIRST_CORE_SCOPE_v1.1` §15.
**Status:** 🟡 **REVIEW ONLY — no scope or roadmap file edited.** This is the full picture to approve before any edit.

---

## 1. Project Order (from README progression)

| # | Project | Role in arc | Course-mapping status |
|---|---|---|---|
| 1 | **1099 Reconciliation ETL** | Production anchor (live) | Foundation — no AI cert needed |
| 2 | **DataVault Analyst** | First AI project | Mapped below |
| 3 | **PolicyPulse** | RAG foundation (+ FastMCP) | Mapped below |
| 4 | **FormSense** | Document/multimodal AI | Mapped below |
| 5 | **Operations-Demand-Intelligence** | Enterprise analytics | Mapped below |
| 6 | **StreamSmart Optimizer** | Consumer AI (Stage 1 + full prod Stage 4–5) | Mapped below |
| 7 | **Attention-Flow Catalyst** | 🚩 Flagship #1 | ✅ Done (eval-first §15) |
| 8 | **Crucible** | 🚩 Flagship #2 (*built first*) | Mapped below |

---

## 2. Per-Project Certificate Map (newest + best, 1–2 picks each)

Legend: ⭐ single best pick · ✅ already in roadmap · 🆕 not in roadmap (candidate add)

### 1 · 1099 Reconciliation ETL — *Python, pandas, validation, pytest, CI*
- ⭐ ✅ **Python for Everybody** (foundation) + testing/CI learned in-project.
- **Verdict:** Fully covered. No AI cert needed — this is the production-Python anchor.

### 2 · DataVault Analyst — *LLM SDK, PandasAI, Pydantic, PII guardrails, DeepEval*
- ⭐ 🆕 **Building with the Claude API** (Anthropic Academy, free, official cert) — provider-agnostic SDK + structured outputs, the exact pattern DataVault uses.
- ✅ **IBM GenAI Engineering** (building GenAI apps with Python) — already covers the app layer.
- **Gap (honest):** PandasAI and governance-as-code guardrails have **no formal cert** — hands-on only.

### 3 · PolicyPulse — *RAG, ChromaDB, embeddings, Anthropic SDK, FastMCP, RAGAS*
- ⭐ ✅ **Building & Evaluating Advanced RAG** (RAG Triad / RAGAS) — the evaluation spine for cited, escalating answers.
- ✅ **MCP: Build Rich-Context AI Apps with Anthropic** — FastMCP server is core to PolicyPulse; **pull this forward** (currently sits Stage 4).
- ✅ Vector Databases: Embeddings to Applications (supporting).
- **Verdict:** Best-covered project. Action is *timing* (pull MCP + RAG-eval earlier), not new certs.

### 4 · FormSense — *Multimodal Gemini Vision, validation, structured extraction*
- ⭐ ✅ **Document AI: From OCR to Agentic Doc Extraction** (DLAI + LandingAI, Jan 2026) — **verified current**; near-exact match (PDF/scan → structured JSON, user-defined schemas).
- ✅ **Pre-processing Unstructured Data for LLM Applications** (supporting).
- **Verdict:** Covered and current. Action: pull Document AI forward to align with the FormSense build.

### 5 · Operations-Demand-Intelligence — *pandas, PandasAI, Plotly, Streamlit, AI insights*
- ⭐ ✅ **IBM Data Analyst** + **Statistics with Python** (analytics + demand patterns).
- ✅ **Generative AI Data Analyst (Vanderbilt)** — fits ODI's AI-analyst workflow, but ⚠️ OpenAI/ChatGPT-centric and needs ChatGPT Plus; keep as *optional* only.
- **Verdict:** Covered; AI-chat layer reuses DataVault's SDK skills. No new cert.

### 6 · StreamSmart Optimizer — *httpx async, external APIs, LangSmith, optimization, "Circle of Evaluation" (Stage 5)*
- ⭐ 🆕 **Evaluating AI Agents** (DLAI) — observability/traces + LLM-as-judge; maps to StreamSmart's LangSmith layer and the Stage-5 evaluation capstone.
- ✅ **Automated Testing for LLMOps** — for the full-production "Circle of Evaluation."
- **Gap:** LangSmith-specific training is vendor docs (LangChain Academy), not a major cert. Async/API skills are general Python (covered).

### 7 · Attention-Flow Catalyst — ✅ **already mapped** in `AFC_EVAL_FIRST_CORE_SCOPE_v1.1` §15 (Building with the Claude API, Automated Testing for LLMOps, Building & Evaluating Advanced RAG, +eval depth).

### 8 · Crucible — *NautilusTrader, Optuna, DuckDB, Ollama/Qwen3 local-first, LangGraph, agents, backtesting*
- ⭐ ✅ **AI Agents in LangGraph** — Crucible's agent crew is LangGraph; this is the direct match. (Plus ✅ Agentic AI / crewAI / Long-Term Agentic Memory for depth.)
- 🆕 **Fast & Efficient LLM Inference with vLLM** (DLAI) — closest formal course to the local layer (quantization, serving, `lm-eval`); complements ✅ Fine-Tuning LLMs with PEFT.
- **Gaps (honest, no strong cert exists):**
  - **Local-first Ollama/Qwen3** — taught via guides, **no recognized certificate**. Treat as hands-on; vLLM course is the nearest formal proxy.
  - **Trading/backtesting infrastructure** — no solid standalone cert short of Georgia Tech "ML for Trading" / OMSCS (your Stage 2–4 plan). Domain self-study + NautilusTrader docs.

---

## 3. Roadmap Certificate Evaluation (keep / dated / deprecated + replacement)

Legend: ✅ best right now · ⚠️ dated (works, better exists) · ⛔ deprecated · 🔁 duplicate

> **Headline:** I found **no ⛔ truly deprecated certificates.** The roadmap is current. The real signals are a few ⚠️ dated (2023 OpenAI-era) courses and 🔁 duplicates.

### Stage 1
| Certificate | Verdict | Action / Replacement |
|---|---|---|
| CS50 | ✅ | Keep |
| Python for Everybody | ✅ | Keep |
| Google Data Analytics | ✅ | Keep |
| IBM Data Analyst | ✅ | Keep |
| Statistics with Python | ✅ | Keep |
| IBM Generative AI Engineering | ✅ | Keep — best value-for-breadth GenAI cert |
| AI Python for Beginners | ✅ | Keep |
| Building & Evaluating Advanced RAG | ✅ | Keep — eval spine |
| Docker for Beginners (KodeKloud) | ✅ | Keep |
| Generative AI Data Analyst (Vanderbilt) | ⚠️ | OpenAI-centric, needs ChatGPT Plus → keep optional; SDK fluency better served by 🆕 Building with the Claude API |
| ChatGPT Prompt Engineering for Developers | ⚠️ | 2023/GPT-3.5 → optional refresh: **AI Prompting for Everyone** (2026). Low priority (prompt certs low-weight) |
| Building Systems with the ChatGPT API | ⚠️ | 2023 → superseded by IBM GenAI cert + agentic courses; demote to optional |
| LangChain for LLM Application Development | ⚠️ | LangChain churns → newer LangGraph courses supersede; demote |

### Stage 2
| Certificate | Verdict | Action |
|---|---|---|
| AWS Certified Data Engineer Associate | ✅ | Keep |
| Docker & Kubernetes Masterclass (Packt) | ✅ | Keep |
| BigQuery Basics (Google Cloud) | ✅ | Keep |
| dbt Fundamentals | ✅ | Keep |
| IBM RAG and Agentic AI Professional Certificate | ✅ | Keep (newer, strong) |

### Stage 3
| Certificate | Verdict | Action |
|---|---|---|
| Machine Learning Specialization (Andrew Ng) | ✅ | Keep |
| Deep Learning Specialization (Andrew Ng) | ✅ | Keep |
| Mathematics for Machine Learning | ✅ | Keep |
| MLOps Specialization (Duke) | ✅ | Keep |
| NVIDIA DLI: Fundamentals of Deep Learning | ✅ | Keep |
| Generative AI with LLMs (AWS + DLAI) | ✅ 🔁 | Keep one entry (listed twice) |
| Fine-Tuning LLMs with PEFT | ✅ 🔁 | Keep — consolidate two names → one |
| Ollama (local LLM) | ⚠️ | Skill, no cert → add 🆕 **Fast & Efficient LLM Inference with vLLM** as formal proxy |
| Fast.ai / Hugging Face NLP | ✅ | Keep |

### Stage 4
| Certificate | Verdict | Action |
|---|---|---|
| Agentic AI (Andrew Ng) | ✅ | Keep |
| MCP (Anthropic) / DLAI MCP course | ✅ | Keep — **pull forward** for PolicyPulse |
| AI Agents in LangGraph | ✅ | Keep |
| Multi-AI Agent Systems with crewAI | ✅ | Keep |
| Long-Term Agentic Memory with LangGraph | ✅ | Keep |

### Stage 5
| Certificate | Verdict | Action |
|---|---|---|
| Automated Testing for LLMOps | ✅ | Keep — **pull forward** for eval-heavy projects (AFC, StreamSmart) |
| Production AI Evaluation (concept) | ✅ | Add 🆕 **Evaluating AI Agents** + 🆕 **Improving Accuracy of LLM Applications** |

---

## 4. Net-New Courses to ADD (across the whole portfolio)

| 🆕 Add | Platform | Serves | Priority |
|---|---|---|---|
| ⭐ **Building with the Claude API** | Anthropic Academy (free, official cert) | DataVault, PolicyPulse, ODI, StreamSmart, AFC, Crucible — *everything Anthropic-SDK* | **HIGH** (Stage 1) |
| **Improving Accuracy of LLM Applications** | DeepLearning.AI | AFC, PolicyPulse, StreamSmart (hallucination/eval) | HIGH |
| **Evaluating AI Agents** | DeepLearning.AI | StreamSmart, Crucible, AFC (observability, LLM-as-judge) | MED |
| **Fast & Efficient LLM Inference with vLLM** | DeepLearning.AI | Crucible local layer (quantization/serving) | MED (Stage 3) |
| **AI Prompting for Everyone** (optional refresh) | DeepLearning.AI | replaces dated ChatGPT PE | LOW |

> Single highest-leverage add for the whole portfolio: **Building with the Claude API** — one free official cert that underwrites every Anthropic-SDK project.

---

## 5. Honest Gaps — No Strong Certificate Exists

These are skills your projects need where chasing a cert is the wrong move (build + document instead):

- **PandasAI** (DataVault, ODI) — hands-on only.
- **Governance-as-code guardrails / PII** (DataVault, PolicyPulse) — pattern, not a cert.
- **FastMCP specifically** — MCP courses teach the protocol; FastMCP itself is docs.
- **Local-first Ollama/Qwen3** (Crucible) — guides, not certs; vLLM course is the nearest proxy.
- **Trading/backtesting infrastructure** (Crucible, AFC) — no solid cert short of GT/OMSCS (already your Stage 2–4 plan).

---

## 6. Summary of Proposed Changes (for your approval — nothing edited yet)

| Category | Count | Detail |
|---|---|---|
| **Add (net-new)** | 4–5 | Building with the Claude API; Improving Accuracy of LLM Apps; Evaluating AI Agents; vLLM Inference; (AI Prompting for Everyone, optional) |
| **Pull forward (timing)** | 3 | MCP → PolicyPulse; Document AI → FormSense; Automated Testing for LLMOps → AFC/StreamSmart |
| **Dated → refresh/demote** | 3 | ChatGPT PE, Building Systems w/ ChatGPT API, LangChain for LLM App Dev |
| **Consolidate duplicates** | 2 | Generative AI with LLMs; Fine-Tuning/PEFT naming |
| **Deprecated** | 0 | None found |

### Recommended next steps (on your go, each gap-analyzed with before/after shown first)
1. **`roadmap.html`** — add the net-new courses, consolidate duplicates, demote dated ones, re-tag a few "pull-forward" courses to their project's stage.
2. **Optional per-scope** — add a small "Courses & Certifications" section to each non-AFC scope, mirroring AFC §15, so each project carries its own learn-while-building map.

> Per your additive-edit rule, I will not touch `roadmap.html` or any scope until you approve **which** of the above to apply.
