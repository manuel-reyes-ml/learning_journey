# 📚 Learning Journey — Business Operations → AI-Ready Analytics & Data Engineering → Applied AI

The learning record behind my portfolio: what I'm studying, why, and in what order.
**3 stages · ~32 months · 25 hrs/week · evidence over keywords.**

> **Now:** Stage 1 of 3 — *Internal AI Builder* (the build work, not a job title)
> **Targeting:** Analytics Engineer (first door) · Data Engineer (parallel) — on AI-ready data platforms · 🟢 open to roles
> **Next gate:** DataVault S2 hardening shipped — the evidence that exits Stage 1
> **Long term:** Applied AI Engineer → Forward-Deployed Engineer

[![Roadmap](https://img.shields.io/badge/Roadmap-v10.0-28a745)](https://manuel-reyes-ml.github.io/learning_journey/roadmap.html)
[![Portfolio](https://img.shields.io/badge/Portfolio-data--portfolio-667eea)](https://github.com/manuel-reyes-ml/data-portfolio)
[![Profile](https://img.shields.io/badge/GitHub-manuel--reyes--ml-181717?logo=github)](https://github.com/manuel-reyes-ml)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-mr410-0077B5?logo=linkedin)](https://www.linkedin.com/in/mr410/)

### Where things live

| If you want… | Go to |
|---|---|
| The 60-second summary | **[Profile](https://github.com/manuel-reyes-ml)** |
| Projects, architecture, the production standard | **[data-portfolio](https://github.com/manuel-reyes-ml/data-portfolio)** |
| What I'm learning, why, and how I work | **This repo** |
| Every decision with its evidence and rejected alternatives | **[Interactive roadmap (v10.0)](https://manuel-reyes-ml.github.io/learning_journey/roadmap.html)** |

---

## 🗺️ The path

| Stage | Months | Goal | Exit evidence | Exams |
|---|---|---|---|---|
| **1 · Internal AI Builder** 🟢 | 1–8 | Production Python, SQL + dbt, eval-first applied AI | **DataVault S2 hardening shipped** | AI-901 |
| **2 · Analytics / Data Engineer (AI-ready data)** 🎯 | 9–20 | dbt + one warehouse deep, orchestration, contracts, deploy, AI-ready data | First AE/DE role; DataVault production-hardened | DP-700 · AWS DEA-C01 |
| **3 · Applied AI → FDE** | 21–32 | Production agentic systems, eval-as-engineering, discovery & decomposition | Applied AI Engineer role; FDE apply list | AI-103 · NCA-GENL · Databricks GenAI · Neo4j |

**The rules that govern it**

- **Evidence gates, not dates.** Stage 1 exits when DataVault S2 ships: ingestion → dbt-tested models in CI → Airflow → data contracts → Docker/ECS → monitoring, with ADRs, a C4 view and a written postmortem.
- **Priority guardrail.** Until that gate, Analytics/Data Engineering build hours ≥ Applied-AI hours, every fortnight. After it, Applied AI becomes the majority lane.
- **Replace, not stack.** A new course or credential must displace something of lesser signal, and must feed a named project.
- **One system per project.** Each project evolves S1 → S3; nothing is rebuilt per stage.
- **Not a generic Data Analyst search.** The target is AE/DE. Domain-bridge data roles at retirement recordkeepers count only when they require SQL plus a warehouse or automation platform.

---

## 📖 What I'm learning

Status: ✅ done · 🚧 in progress · 📅 next · ⏸️ conditional (taken only on a named trigger)

### Stage 1 — now

**Analytics & data engineering first**
- 🚧 [Mode SQL Tutorial](https://mode.com/sql-tutorial/) — SQL is the single most load-bearing AE/DE skill
- 🚧 [dbt Fundamentals](https://learn.getdbt.com/courses/dbt-fundamentals) → [dbt Advanced Learning Paths](https://learn.getdbt.com/) — pulled forward from Stage 2; DataVault's reconciliation rules become tested dbt models (dbt Core + DuckDB)
- 📖 *The Data Warehouse Toolkit* (Kimball & Ross) — dimensional modeling and declaring the grain

**CS & Python foundations**
- 🚧 [CS50x](https://www.edx.org/course/introduction-computer-science-harvardx-cs50x) · 🚧 [Python for Everybody](https://www.coursera.org/specializations/python) · 📅 [CS50P](https://www.edx.org/learn/python/harvard-university-cs50-s-introduction-to-programming-with-python) · 📅 MITx 6.00.1x
- 📅 **[CU Boulder](https://www.coursera.org/degrees/ms-computer-science-boulder) — Foundations of Data Structures & Algorithms** (CSCA 5414 · 5424 · 5454, 3 graduate credits, Nov 2026 – Feb 2027) — the bridge into OMSCS
- 📖 *Fluent Python* (Ramalho, owned) · *Robust Python* (Viafore) · *Python Testing with pytest* (Okken)

**Production engineering** — docs-first; the shipped config is the evidence
- 🚧 [uv](https://docs.astral.sh/uv/getting-started/) + [Al Sweigart's quickstart](https://inventwithpython.com/blog/uv-quickstart-tutorial.html) · [pre-commit](https://pre-commit.com/) + [Stefanie Molin's series](https://stefaniemolin.com/articles/devx/pre-commit/setup-guide/)
- 🚧 Architecture documentation: [C4 model](https://c4model.com/) + [ADRs (AWS Prescriptive Guidance)](https://docs.aws.amazon.com/prescriptive-guidance/latest/architectural-decision-records/welcome.html)
- 🚧 [Introduction to Git and GitHub](https://www.coursera.org/learn/introduction-git-github) (Google) — scoped to branching, rebase, conflicts and pull requests (~8 hrs)
- 🚧 [Docker for Beginners](https://www.coursera.org/learn/docker-for-the-absolute-beginner) (KodeKloud) · `structlog` / `stamina` / `pydantic-settings` docs

**Applied AI & evaluation**
- 🚧 [Building with the Claude API](https://anthropic.skilljar.com/claude-with-the-anthropic-api) · 🚧 [Introduction to MCP](https://anthropic.skilljar.com/introduction-to-model-context-protocol) (Anthropic Academy)
- 📅 [Improving Accuracy of LLM Applications](https://www.deeplearning.ai/short-courses/improving-accuracy-of-llm-applications/) · [Building & Evaluating Advanced RAG](https://www.deeplearning.ai/short-courses/building-evaluating-advanced-rag/) — labs batched into one paid month, notebooks downloaded
- 📅 [IBM Generative AI Engineering Professional Certificate](https://www.coursera.org/professional-certificates/ibm-generative-ai-engineering) — from Month 4
- 📖 *AI Engineering* (Huyen)

**Machine learning for AFC** *(the one project that ships ML in Stage 1)*
- 📅 [Machine Learning Specialization](https://www.coursera.org/specializations/machine-learning-introduction) (Andrew Ng) — courses 1–2 before AFC's ML weeks
- 📖 *Machine Learning for Trading* (Jansen, 3rd ed.) — purged cross-validation, gradient boosting, calibration

### Stage 2 — next

- [DeepLearning.AI Data Engineering Professional Certificate (with AWS)](https://www.coursera.org/professional-certificates/data-engineering) — the DE spine and the DEA-C01 on-ramp
- [Snowflake Data Engineering Professional Certificate](https://www.coursera.org/professional-certificates/snowflake-data-engineering) — one warehouse, deep
- [PostgreSQL for Everybody](https://www.coursera.org/specializations/postgresql-for-everybody) · [Astronomer Academy — Airflow](https://academy.astronomer.io/) · [Databricks Academy](https://customer-academy.databricks.com/learn) · [Kafka 101](https://developer.confluent.io/courses/apache-kafka/events/) · [Terraform](https://developer.hashicorp.com/terraform/tutorials)
- [IBM AI-Native Data Engineering Professional Certificate](https://www.coursera.org/professional-certificates/ibm-ai-native-data-engineering) — selected courses: vector retrieval governance, PII-safe corpus preparation, point-in-time-correct datasets
- TypeScript last mile: [Vercel Academy — Builders Guide to the AI SDK](https://vercel.com/academy/ai-sdk) — a streaming UI over PolicyPulse retrieval; Python keeps the agent core
- 📖 *Data Engineering Design Patterns* (Konieczny)

### Stage 3 — later

- [Agentic AI](https://www.deeplearning.ai/courses/agentic-ai/) (Andrew Ng) · [LangChain Academy](https://academy.langchain.com/) · [Hugging Face LLM Course](https://huggingface.co/learn/llm-course)
- Anthropic Academy: [MCP Advanced Topics](https://anthropic.skilljar.com/model-context-protocol-advanced-topics) · [Agent Skills](https://anthropic.skilljar.com/introduction-to-agent-skills) · [Claude Code in Action](https://anthropic.skilljar.com/claude-code-in-action)
- [AI-103 learning path](https://learn.microsoft.com/en-us/credentials/certifications/resources/study-guides/ai-103) (Microsoft Foundry) · [Neo4j GraphAcademy](https://graphacademy.neo4j.com/)
- Architecture-defense rehearsal: one architectural kata a month → C4 + ADRs → present and defend
- 📖 *Fundamentals of Software Architecture* (Richards & Ford, 2nd ed.) · *Hands-On Large Language Models* (Alammar & Grootendorst)

---

## 🎓 Credentials

**Ladder:** shipped systems → accredited degree → proctored exams → coursework certificates → completion certificates. Exams clear filters; shipped systems win offers. **All self-funded.**

**Committed — 7 exams, ≈ $904**

| Exam | Stage | Cost (USD) |
|---|---|---|
| [Azure AI Fundamentals (AI-901)](https://learn.microsoft.com/en-us/credentials/certifications/azure-ai-fundamentals/) | S1 | $99 |
| [Fabric Data Engineer Associate (DP-700)](https://learn.microsoft.com/en-us/credentials/certifications/fabric-data-engineer-associate/) | S2 | $165 |
| [AWS Certified Data Engineer – Associate (DEA-C01)](https://aws.amazon.com/certification/certified-data-engineer-associate/) | S2 | $150 |
| [Azure AI Apps & Agents Developer Associate (AI-103)](https://learn.microsoft.com/en-us/credentials/certifications/azure-ai-apps-and-agents-developer-associate/) | S3 | $165 |
| [NVIDIA-Certified Associate: Generative AI LLMs (NCA-GENL)](https://www.nvidia.com/en-us/learn/certification/generative-ai-llm-associate/) | S3 | $125 |
| [Databricks Generative AI Engineer Associate](https://www.databricks.com/learn/certification/genai-engineer-associate) | S3 | $200 |
| [Neo4j Certified Professional](https://graphacademy.neo4j.com/) | S3 | Free |

**⏸️ Conditional — taken only on a named trigger, never stacked**

| Exam | Cost | Trigger |
|---|---|---|
| [AI Agent Builder Associate (AB-620)](https://learn.microsoft.com/en-us/credentials/certifications/ai-agent-builder-associate/) | ~$165 | A deliberate Microsoft-ecosystem specialization — e.g. target employers running M365 Copilot / Power Platform as their agent surface |
| [dbt Analytics Engineering](https://www.getdbt.com/certifications/analytics-engineer-certification-exam) | ~$200 | ≥ 3 target postings name it, or the DataVault dbt models ship with budget to spare — the tested dbt project is the real signal |
| Claude Certified Developer → Architect (CCDV-F → CCA-F) | ~$125 each | Claude Partner Network access — individuals can't register yet |
| Lakehouse slot — take exactly one | $165–$200 | DP-750 · SnowPro Core · Databricks DE Associate, matched to the target employer's stack |

Ceiling if every conditional fires: ≈ $1,594 (≈ $1,719 with both Claude exams), spread across three stages.

**Coursework certificates** — IBM Generative AI Engineering · DeepLearning.AI Data Engineering (with AWS) · Snowflake Data Engineering · IBM AI-Native Data Engineering (selected courses). Learning evidence; the capstone is the deliverable, not the PDF.

### Degree track

- **Now:** B.S., Industrial & Systems Engineering
- **Bridge (Nov 2026 – Feb 2027):** CU Boulder graduate Data Structures & Algorithms pathway — a graded US graduate transcript, preparation for Graduate Algorithms, and automatic admission to the [CU Boulder MS-CS](https://www.coursera.org/degrees/ms-computer-science-boulder) as the documented fallback
- **Target:** [Georgia Tech OMSCS](https://omscs.gatech.edu/), Computing Systems — applying Aug 2027 for Spring 2028 (≈ $10–11K). Data-engineering courses first (Databases, Distributed Computing, Cloud Systems), then AI electives (Deep Learning, NLP, [ML for Trading](https://omscs.gatech.edu/cs-7646-machine-learning-trading)). Coursework substitutes for overlapping self-study; academic work stays out of public repos.

---

## 🧠 How I learn

- **Theory first, then build.** The failure mode isn't starting with theory — it's stopping there. Every course must feed a named project.
- **No vibe coding.** AI assists; I read and understand every line before it merges.
- **Log it in my own words.** [`notes/learning-log.md`](notes/learning-log.md) uses a strict template: source · format · stage · project tags · takeaway · an *Apply* line tied to a specific project.
- **Badges aren't credentials.** Completion certificates and books are learning evidence — never a Certifications line.
- **Re-verify before buying.** Books are bought at stage entry, editions and prices checked at purchase.

---

## 🤖 How I work — environment & AI workflow

- **Editors:** VS Code (Python, SQL, Jupyter) · Cursor (hosts the agent harness)
- **Agent harness:** OpenCode is the writer; Claude Code is a read-only reviewer — one portable `AGENTS.md` contract drives both. A guard hook blocks agent `git commit` / `push`, so every commit is made by a human. Planning runs on a local model; regulated or proprietary code is never opened in a cloud harness. Decisions are recorded in [`docs/adr/`](docs/adr/).
- **Models:** Anthropic SDK (primary) · Gemini (fallback) · Ollama + LM Studio (local, privacy-routed) · OpenRouter (overflow)
- **Python:** 3.14, standard GIL build · `uv` with a committed `uv.lock` · ruff · mypy (CI-only, by ADR) · pytest
- **Commit boundary:** pinned pre-commit hooks — a strict subset of CI — `ruff-check` → `ruff-format`, `uv-lock`, `gitleaks`, `detect-private-key`, `nbstripout` where notebooks exist, and Conventional Commits on the `commit-msg` stage

```bash
git clone https://github.com/manuel-reyes-ml/learning_journey.git && cd learning_journey
uv tool install pre-commit --with pre-commit-uv   # one-time
make sync      # uv sync --all-packages --all-groups, from uv.lock
make hooks     # installs the pre-commit and commit-msg stages
uv run python getting_started/environment_verification.py
```

---

## 📂 Repository structure

```
learning_journey/
├── courses/           # course work, one folder per course (CS50, Python for Everybody, SQL, …)
├── books/             # reading notes and exercises (Fluent Python, …)
├── certifications/    # exam and certificate progress
├── notes/             # learning log + trading research notes
├── projects/          # index of portfolio projects (full write-ups live in data-portfolio)
├── getting_started/   # setup guides: local and cloud LLMs, agentic workflow, environment check
├── docs/
│   ├── roadmap.html   # the interactive roadmap (GitHub Pages)
│   ├── adr/           # architecture decision records for this repo and the agent harness
│   └── activation_plans/
├── llm-api-smoke-test/  # uv workspace member — provider smoke tests
├── scripts/           # harness generators and checks
├── AGENTS.md          # the portable agent contract
└── pyproject.toml · uv.lock · .pre-commit-config.yaml · Makefile
```

---

📫 [manuelreyesv410@gmail.com](mailto:manuelreyesv410@gmail.com) · [LinkedIn](https://www.linkedin.com/in/mr410/) · ⭐ Star the repo to follow the journey
