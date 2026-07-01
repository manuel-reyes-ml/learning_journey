# Certification & Course Roadmap Review
### Daybright Education Benefit × Roadmap v8.9 Alignment
*Prepared July 1, 2026 · All prices USD, verify at source before purchase · No roadmap edits applied — recommendations only*

---

## 0. Context recap

- **Daybright is confirmed a Microsoft/Azure + Entra shop** (device is `AzureAdJoined: YES` under Intune; AI tooling is Microsoft 365 Copilot, which runs on Azure OpenAI). Line-of-business apps (OnBase, Relius) sit in the same Microsoft/Windows ecosystem.
- **The benefit reimburses exam fees + required study materials for the first two attempts.** Bonuses apply **only** to the finance/actuarial/securities certs on the pre-approved schedule — none of the tech certs below carry a bonus.
- **Every credential here is off the pre-approved list**, so all go through the **case-by-case path** (`learning@daybright.com`, manager sign-off, framed as *professional development*). Approval odds are highest for the **Microsoft/Azure** items because they match Daybright's actual stack; the non-Microsoft items (Databricks/NVIDIA/Anthropic) are submittable but carry a weaker "relevance to Daybright" argument.
- **Pitch framing that wins:** *"I want to grow into an internal AI-builder role using our existing Microsoft/Azure/Copilot stack."* Anchor on professional development, not current-role duties.

---

## SECTION A — Daybright Ecosystem (Microsoft / Azure / Copilot)
### Highest reimbursement-approval odds. This is the sequence to spend the benefit on.

| # | Credential | Code | Cost | Level | Why it fits Daybright + your roadmap |
|---|-----------|------|------|-------|--------------------------------------|
| 1 | Azure AI Fundamentals | **AI-901** | **$99** | Fundamentals | Cheapest, easiest first approval; proves the reimbursement path works. Foundation for everything below. Note: the refreshed exam now expects some hands-on Foundry/Python, not pure theory. |
| 2 | Applied Skills: Extend M365 Copilot with declarative agents (VS Code) | *(lab)* | **Free** | Hands-on | Zero-cost, VS Code + M365 Agents Toolkit + TypeSpec. Closest to your "no vibe coding" ethos; supports MCP. Do this in parallel — nothing to reimburse. |
| 3 | AI Agent Builder Associate | **AB-620** | **$165** | Associate | Building agents on **Copilot Studio** — the exact AI tool Daybright uses. Covers RAG, **MCP servers**, A2A, multi-agent, Foundry, REST APIs. Ties to your Month-14 MCP sprint + PolicyPulse FastMCP server. Caveat: Copilot Studio is the most low-code tool here. |
| 4 | Azure AI Apps & Agents Developer Associate | **AI-103** | **~$165** | Associate | The portable "AI developer" capstone (successor to retired AI-102). Foundry + Python + generative-AI apps + agents. Most transferable to your external Senior LLM Engineer goal. Currently in beta — verify code/price. |
| + | *(Optional, Stage 2)* Fabric Data Engineer Associate | **DP-700** | **$165** | Associate | Azure-native equivalent of your AWS DE cert; SQL/PySpark/KQL on Microsoft Fabric — runs on Daybright's stack. Fabric-era successor to the retired DP-203. English exam updates July 21, 2026. |

**Core sequence cost (items 1–4): ~$429.** Adding DP-700: ~$594.

**Timing landmines (all real as of today):** AI-102 and AI-900 **retired June 30, 2026** — do not buy prep for those; use AI-901 / AI-103 successors. AB-620 went GA ~June 2026; AI-103 is still in beta (delayed scoring, ~2–3 months to results).

**Links**
- AI-901 — https://learn.microsoft.com/en-us/credentials/certifications/azure-ai-fundamentals/
- Applied Skills (declarative agents, VS Code) — https://learn.microsoft.com/en-us/credentials/applied-skills/extend-microsoft-365-copilot-with-declarative-agents-by-using-visual-studio-code/
- AB-620 (AI Agent Builder Associate) — https://learn.microsoft.com/en-us/credentials/certifications/ai-agent-builder-associate/ · study guide: https://learn.microsoft.com/en-us/credentials/certifications/resources/study-guides/ab-620
- AI-103 (Azure AI Apps & Agents Developer) — search "AI-103" on https://learn.microsoft.com/credentials/
- DP-700 (Fabric Data Engineer) — https://learn.microsoft.com/en-us/credentials/certifications/fabric-data-engineer-associate/

---

## SECTION B — Best-in-Class Credentials NOT Yet in Your Roadmap
### Recruiter-recognized, roadmap-advancing. Fund yourself or attempt case-by-case (weaker Daybright relevance).

### B1. Anthropic — Claude Certified Architect, Foundations (CCA-F) ⭐ top pick
The single tightest fit for your stack: you're **Anthropic-SDK-first**, you build **MCP servers** (PolicyPulse FastMCP), and you run agentic loops (Crucible, AFC). The exam blueprint maps almost 1:1 to what you already do.

- **Cost:** $99 per attempt (free for the first 5,000 Claude Partner Network employees; partner membership is free for any org bringing Claude to market). **Prep courses are free for everyone** on Anthropic Academy (Skilljar) — 13 courses.
- **Format:** 60 questions, 120 min, proctored (Pearson VUE), scaled 100–1000, **pass = 720**. Launched March 12, 2026. A "301-level" exam for people who already build.
- **Domains:** Agentic Architecture & Orchestration (27%), Claude Code Config & Workflows (20%), Prompt Engineering & Structured Output (20%), Tool Design & **MCP Integration** (18%), Context Management & Reliability (15%).
- **Roadmap fit:** Stage 4 (Agentic) → Stage 5 (Senior LLM). Philosophically aligned with "no vibe coding" — it rewards people who've shipped, not memorized.
- **Access caveat:** currently gated behind Partner Network; public registration signaled but undated. Free prep courses are open now regardless.
- **Links:** https://www.pearsonvue.com/us/en/anthropic.html · prep: https://anthropic.skilljar.com

### B2. Databricks — Certified Generative AI Engineer Associate
The industry's first comprehensive production-GenAI engineering cert; strong recruiter signal for RAG/LLM roles. Not on your roadmap and worth adding.

- **Cost:** $200 · 45 questions · 90 min · online proctored · valid 2 years · **Python-based**.
- **Covers:** designing LLM apps, RAG pipelines, LLM chains, Vector Search, Model Serving, **MLflow**, Unity Catalog governance, evaluation & monitoring — directly overlaps your DeepEval/eval-first discipline.
- **Roadmap fit:** Stage 2→3 (production RAG/LLMOps). Also note the newer **Databricks Certified Context Engineer Associate** (context/governance for agent systems) — cutting-edge, agentic, worth watching.
- **Link:** https://www.databricks.com/learn/certification/genai-engineer-associate

### B3. NVIDIA — Generative AI / Agentic ladder
You have NVIDIA **DLI courses** in your roadmap but not the **certification exams**. The exams are the recruiter-recognized artifact. Clean three-rung ladder mapped to your stages:

| Rung | Exam | Cost | Level | Maps to |
|------|------|------|-------|---------|
| Associate | **NCA-GENL** (Generative AI LLMs) | $125 | Entry | Stage 2–3 — transformers, prompt eng, RAG, PEFT, deployment (50–60 Q, 60 min, 2-yr validity) |
| Professional | **NCP-AAI** (Agentic AI LLMs) | *verify* | Pro | **Stage 4 bullseye** — agent architecture, multi-agent design, RAG, AI safety. Now GA on Certiverse. |
| Professional | **NCP-GENL** (Generative AI LLMs) | *verify* | Pro | Stage 5 — design/train/fine-tune LLMs, distributed training (2–3 yrs exp recommended) |

- Multimodal option (**NCA-GENM**) is relevant to **FormSense** (multimodal IDP) if you want a targeted add.
- **Link:** https://www.nvidia.com/en-us/learn/certification/

---

## SECTION C — Already in Your Roadmap (no action; listed to avoid double-counting)
Your v8.9 already includes a strong course/cert spine, so these are **not** re-recommended:
- **Certs:** AWS Certified Data Engineer – Associate (flagship); Neo4j Certified Professional.
- **Coursera / IBM:** IBM Generative AI Engineering Professional Certificate; IBM Intro to Data Engineering; AWS Data Engineering Professional Certificate; Agentic AI with LangChain (IBM); Docker & Kubernetes Masterclass (Packt); Google BigQuery Basics; MLOps Specialization (Duke); AI Agents & Agentic AI in Python (Vanderbilt); Generative AI with LLMs (AWS + DeepLearning.AI).
- **DeepLearning.AI:** Vector Databases; Pre-processing Unstructured Data; RAG (Production-Ready); Knowledge Graphs for RAG; Fine-Tuning LLMs with PEFT; vLLM Inference; Agentic AI (Andrew Ng); Evaluating AI Agents; Agentic Knowledge Graph Construction.
- **Andrew Ng:** Math for ML; ML Specialization; Deep Learning Specialization.
- **NVIDIA DLI:** Fundamentals of Deep Learning (course only — see B3 for the exams).
- **Degree:** Georgia Tech OMSCS (ML spec), planned Stages 2–4 post-Spain.

---

## SECTION D — Also Considered (lower priority for your goals; included for completeness)
So nothing is left out — but these rank below A/B for you:
- **GitHub Copilot (GH-300)** — $99, 100 min. Tests *using* Copilot as a coding assistant, **not** building systems; off-roadmap and mildly at odds with "no vibe coding." Skip unless you specifically want it. https://learn.microsoft.com/en-us/credentials/certifications/github-copilot/
- **Google Cloud Professional ML Engineer / Professional Data Engineer** — recruiter-recognized, but you're consolidating on Azure (employer) + AWS (roadmap); a third cloud dilutes focus. Verify current pricing at cloud.google.com/learn/certification.
- **dbt Analytics Engineering Certification** — you already use dbt; a credential is a modest signal-booster for Stage 2. Verify at getdbt.com.
- **SnowPro (Snowflake)** — you flagged Snowflake as a coverage gap; only pursue if a target job requires it.
- **Hugging Face / LangChain** — high-value *free courses*, but no widely-recognized proctored exam; treat as learning, not credentials.
- **IAPP AIGP (AI Governance)** — governance-focused; relevant later if you move toward responsible-AI/architecture roles, not now.

---

## SECTION E — Recommended Integrated Sequence (Daybright $ + roadmap credentials by stage)

| Stage | Daybright-reimbursable (Microsoft/Azure) | Self-fund / case-by-case (roadmap best-in-class) |
|-------|------------------------------------------|--------------------------------------------------|
| **1 — GenAI-First Analyst/AI Eng (now)** | ① AI-901 ($99) → ② Applied Skills declarative agents (free) | Start free Anthropic Academy courses; earn **Anthropic CCA-F** when access opens ($99/free) |
| **2 — Data Engineer** | *(optional)* DP-700 Fabric DE ($165) | Keep AWS DE (in roadmap); **NVIDIA NCA-GENL** ($125) |
| **3 — ML Engineer** | ③ AB-620 ($165) | **Databricks GenAI Engineer Associate** ($200); Neo4j (in roadmap) |
| **4 — Agentic AI Engineer** | ④ AI-103 (~$165) | **NVIDIA NCP-AAI** (agentic pro); reinforce CCA-F |
| **5 — Senior LLM Engineer** | *(renewals)* | **NVIDIA NCP-GENL** (LLM pro); OMSCS (in roadmap) |

**Fastest high-signal moves right now (next 30–60 days):**
1. Submit the AI-901 pre-approval email to your manager (cheapest, proves the benefit path).
2. Start the **free** Applied Skills declarative-agents lab and **free** Anthropic Academy courses in parallel — zero cost, immediate portfolio + LinkedIn signal.
3. Queue **AB-620** as the flagship Daybright-reimbursed exam once AI-901 is approved.

---

## Next steps (your call — nothing edited yet)
- **(a)** Draft the `learning@daybright.com` pre-approval email (starting with AI-901, then AB-620), built on the professional-development + Azure/Copilot-stack angle.
- **(b)** Run a gap analysis showing exactly where these credentials slot into your v8.9 stage tables (§18/§21) before any roadmap edit.
- **(c)** Both.

*Sources: Microsoft Learn, Databricks, NVIDIA, Anthropic/Pearson VUE official pages plus 2026 exam-guide aggregators, retrieved July 1, 2026. Prices marked "verify" were not confirmed to a single figure this session.*
