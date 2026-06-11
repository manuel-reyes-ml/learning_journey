# 📋 AFC Roadmap — Course Inventory Review & Remove/Add Summary

**Prepared:** June 10, 2026
**Scope reviewed:** `roadmap.html` (v8.3) — all course/certification entries, Stages 1–5
**Trigger:** Alignment check against `AFC_EVAL_FIRST_CORE_SCOPE_v1.1` (Python-for-AI + evaluation focus)
**Status:** 🟡 Independent summary — `roadmap.html` is **not modified**. This is a recommendation for your review.

---

## 1. Method & Honesty Note

- I extracted every course link/name from `roadmap.html` (≈45 entries, with some duplicates).
- I **directly verified (this session, web)** the highest-deprecation-risk items: the 2023 ChatGPT-era DeepLearning.AI courses, the IBM GenAI Engineering certificate, and the current DeepLearning.AI catalog.
- The remaining stable credentials (Coursera professional certs, Kaggle, Fast.ai, Hugging Face, university specializations) are assessed as **standard and still-live** based on platform durability, but I did **not** open all ~45 individually. Items I could not confirm with certainty are marked **❓ confirm**.
- **Bottom line:** I found **no evidence of broad course retirements.** The hygiene work is *deduplication* and a couple of *dated-but-valid* refreshes — not mass removal.

---

## 2. Verification Status — Full Inventory

Legend: ✅ live & valid · ⚠️ dated-but-live (optional refresh) · 🔁 duplicate (consolidate) · ❓ confirm · ⭐ relevant to AFC eval-first slice

### Foundation / Stage 1
| Course | Platform | Status |
|---|---|---|
| CS50: Introduction to Computer Science | edX | ✅ (verified live) |
| Python for Everybody Specialization | Coursera (Michigan) | ✅ |
| ⭐ AI Python for Beginners (Andrew Ng) | DeepLearning.AI | ✅ (current) |
| Google Data Analytics Professional Certificate | Coursera | ✅ |
| IBM Data Analyst Professional Certificate | Coursera | ✅ |
| Statistics with Python Specialization | Coursera (Michigan) | ✅ |
| ⭐ IBM Generative AI Engineering Professional Certificate | Coursera | ✅ (verified: 16 courses, current) |
| Generative AI Data Analyst Specialization (Vanderbilt) | Coursera | ✅ (already flagged optional) |
| Docker for Beginners (KodeKloud) | Coursera | ✅ |
| ⭐ ChatGPT Prompt Engineering for Developers | DeepLearning.AI | ⚠️ (verified live; 2023/GPT-3.5, dated) |
| Building Systems with the ChatGPT API | DeepLearning.AI | ⚠️ (2023, dated) |
| LangChain for LLM Application Development | DeepLearning.AI | ⚠️ (dated; LangChain churns fast) |
| ⭐ Building & Evaluating Advanced RAG | DeepLearning.AI | ✅ (current; **already in roadmap**) |
| ⭐ Automated Testing for LLMOps | DeepLearning.AI | ✅ (current; **already in roadmap**) |
| LLM Series by DeepLearning.AI | DeepLearning.AI | ❓ (generic link, not a specific course — vague) |

### RAG / Agents / Eval (Stages 2–4)
| Course | Platform | Status |
|---|---|---|
| Generative AI with LLMs (AWS + DLAI) | Coursera | ✅ 🔁 (listed twice) |
| Finetuning Large Language Models / "Fine-Tuning LLMs with PEFT" | DeepLearning.AI | ✅ 🔁 (same URL, two names) |
| Vector Databases: Embeddings to Applications | DeepLearning.AI | ✅ 🔁 (listed twice) |
| Retrieval Augmented Generation — "Production Ready" / "Full Course" | DLAI / Coursera | ✅ 🔁 (two variants of RAG) |
| AI Agents in LangGraph | DeepLearning.AI | ✅ |
| Agentic AI (Andrew Ng) | DeepLearning.AI | ✅ |
| Agentic AI with LangChain (IBM) | Coursera | ✅ |
| Multi-AI Agent Systems with crewAI | DeepLearning.AI | ✅ |
| Long-Term Agentic Memory with LangGraph | DeepLearning.AI | ✅ |
| MCP: Build Rich-Context AI Apps with Anthropic | DeepLearning.AI | ✅ |
| Agent Skills with Anthropic | DeepLearning.AI | ✅ |
| Claude Code: A Highly Agentic Coding Assistant | DeepLearning.AI | ✅ |
| AI Engineer Agentic Track: Complete Agent & MCP Course | Udemy | ❓ confirm (Udemy listings change) |
| Document AI: From OCR to Agentic Doc Extraction | DeepLearning.AI | ✅ (FormSense-relevant) |
| Pre-processing Unstructured Data for LLM Applications | DeepLearning.AI | ✅ |
| IBM RAG and Agentic AI Professional Certificate | Coursera | ✅ |
| LangChain & Vector Databases | Udemy | ❓ confirm (Udemy, dated) |

### ML / Math / Data Engineering / Infra (Stages 2–3)
| Course | Platform | Status |
|---|---|---|
| Machine Learning Specialization (Andrew Ng) | Coursera | ✅ |
| Deep Learning Specialization (Andrew Ng) | Coursera | ✅ |
| Mathematics for Machine Learning Specialization | Coursera | ✅ |
| MLOps Specialization (Duke) | Coursera | ✅ |
| AWS Data Engineering Professional Certificate | Coursera | ✅ |
| Introduction to Data Engineering | Coursera | ✅ |
| SQL for Data Science | Coursera | ✅ |
| BigQuery Basics for Data Analysts (Google Cloud) | Coursera | ✅ |
| dbt Fundamentals | getdbt.com | ✅ |
| Docker & Kubernetes Masterclass (Packt) | Coursera | ✅ |
| Apache Airflow: The Hands-On Guide | Udemy | ❓ confirm |
| PostgreSQL Bootcamp | Udemy | ❓ confirm |
| PySpark for Big Data | Udemy | ❓ confirm |
| NVIDIA DLI: Fundamentals of Deep Learning | NVIDIA | ✅ |
| Fast.ai Practical Deep Learning | fast.ai | ✅ (free, current) |
| Hugging Face NLP Course | huggingface.co | ✅ (current) |
| Kaggle Learn / Competitions | Kaggle | ✅ |

---

## 3. REMOVE / CONSOLIDATE (hygiene — duplicates, not deprecations)

These are the same course appearing more than once; collapse each to a single canonical entry.

| Action | Detail |
|---|---|
| Consolidate | **Vector Databases: Embeddings to Applications** — appears twice → one entry |
| Consolidate | **Generative AI with LLMs** = **Generative AI with Large Language Models (AWS + DLAI)** — same Coursera URL → one entry |
| Consolidate | **Finetuning Large Language Models** = **Fine-Tuning LLMs with PEFT** — same DLAI URL, two display names → one entry (use the PEFT name; it's clearer) |
| Consolidate | **ChatGPT Prompt Engineering for Developers** & **Building Systems with the ChatGPT API** — each appears twice (Stage 1 + Stage 4) → keep one canonical reference, cross-link if needed |
| Consolidate | **RAG "Production Ready"** vs **RAG "Full Course"** — two RAG variants; pick one as canonical (the Coursera Full Course if you want a certificate; the short course if you want speed) |
| Replace | **"LLM Series by DeepLearning.AI"** (generic catalog link) → replace with the *specific* named DLAI courses you actually intend to take, so the roadmap is auditable |

---

## 4. SUPERSEDE / REFRESH (dated-but-valid — optional)

Still live, but built on 2023 models/tooling. Keep if you want the certificate; refresh if you want current material.

| Dated course | Why dated | Optional replacement (2026) |
|---|---|---|
| ChatGPT Prompt Engineering for Developers | 2023, GPT-3.5, OpenAI-only | **AI Prompting for Everyone** (Andrew Ng, 2026) — positioned as the next-gen prompting course. *Note: your Anthropic-SDK work makes prompt-engineering certs low-priority anyway.* |
| Building Systems with the ChatGPT API | 2023, OpenAI-only | Already superseded in practice by your **IBM GenAI Engineering** cert + the newer agentic courses — safe to demote to optional |
| LangChain for LLM Application Development | LangChain API churns | Your roadmap already carries newer LangGraph/agent courses — demote to optional |

> Reality check on certs (2026 hiring): prompt-engineering certificates carry little weight; a documented project portfolio signals ability far better. Don't spend scarce hours chasing dated prompt certs — your AFC eval-first repo is the stronger signal.

---

## 5. ADD (per AFC Eval-First Scope v1.1)

Genuinely missing from `roadmap.html`. All free; all issue certificates.

| Add | Platform | Cert/Cost | Why (maps to scope) | Priority |
|---|---|---|---|---|
| ⭐ **Building with the Claude API** | **Anthropic Academy** | Free, official LinkedIn cert | Provider-source-of-truth for your Anthropic-SDK-primary analyst (deliverable #4); 84 lessons, 8+ hrs; fellowship-aligned signal | **HIGH** |
| ⭐ **Improving Accuracy of LLM Applications** | DeepLearning.AI | Free, cert | Build an eval framework from scratch + **deliberately simulate hallucinations** — mirrors your §4 perturbation methodology | **HIGH** |
| **Evaluating AI Agents** | DeepLearning.AI | Free (beta), cert | Code-based vs LLM-as-a-Judge evaluators, metric selection, traces — depth beyond the RAG Triad | MED |

### ⚠️ Already present — do NOT re-add (the review's key catch)
- **Automated Testing for LLMOps** (DLAI) — *already in your roadmap.* This is your CI hallucination-eval gate; **pull it forward into Stage 1** for this slice rather than adding it.
- **Building & Evaluating Advanced RAG** (DLAI) — *already in your roadmap.* The RAG Triad is your eval's conceptual spine; pull forward.

> Optional (broader Anthropic track, not slice-critical): Anthropic Academy also offers **MCP** and **Claude Code** courses — but your roadmap already has the DeepLearning.AI versions of both, so these are redundant unless you specifically want the model-maker's certificate.

---

## 6. KEEP AS-IS (the stable backbone)

No action needed — these are durable, current, and correctly placed: CS50, Python for Everybody, Statistics with Python, IBM GenAI Engineering, IBM/Google Data certs, Machine Learning + Deep Learning + Math-for-ML specializations, MLOps (Duke), AWS Data Engineering, dbt Fundamentals, Hugging Face NLP, Fast.ai, NVIDIA DLI, Kaggle, and the agentic suite (LangGraph, crewAI, MCP, Agent Skills, Claude Code, Document AI).

---

## 7. Net Change Summary

| Category | Count | Items |
|---|---|---|
| **Remove/Consolidate (duplicates)** | ~6 | Vector DBs ×2, GenAI w/ LLMs ×2, Finetuning/PEFT names, ChatGPT PE ×2, Building Systems ×2, RAG variants; + replace generic "LLM Series" link |
| **Supersede/Refresh (optional)** | 3 | ChatGPT PE → AI Prompting for Everyone; demote 2 dated OpenAI-era courses |
| **Add (new)** | 3 | Building with the Claude API (Anthropic Academy); Improving Accuracy of LLM Applications; Evaluating AI Agents |
| **Already present — pull forward** | 2 | Automated Testing for LLMOps; Building & Evaluating Advanced RAG |
| **Confirm (couldn't fully verify)** | ~6 | Udemy items + generic DLAI link |

---

## 8. Caveats

- This is a **point-in-time** check (June 10, 2026). Course catalogs move; re-verify links before enrolling.
- I did not individually open every Coursera/Udemy listing; **❓ confirm** items are the ones to spot-check yourself.
- Nothing here changes `roadmap.html`. If you approve any of these, the next step is a separate, gap-analyzed edit to the roadmap — your call, per your additive-edit rule.
