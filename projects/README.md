# 🚀 Projects

The six portfolio projects in one line each, with the learning that feeds them. Full write-ups — Production · Cost · Architecture, stacks and scope documents — live in **[data-portfolio](https://github.com/manuel-reyes-ml/data-portfolio)**.

Every project puts AI to work — **powered** where the model does the core job, **assisted** where a deterministic core must make the decision. Status: ✅ live · 🏗️ in build · 📐 designed · 📅 planned

| Project | What it is | Status | Learning that feeds it |
|---|---|---|---|
| **[DataVault](https://github.com/manuel-reyes-ml/data-portfolio#-datavault--ai-assisted-1099-data-platform)**<br>*AI-assisted 1099 data platform* · flagship | The live 1099-R reconciliation pipeline, hardened into a dbt-tested data platform | ✅ S1 live · 🏗️ S2 | Mode SQL · dbt Fundamentals → Advanced · *The Data Warehouse Toolkit* · PostgreSQL for Everybody · Astronomer (Airflow) |
| **[PostCheck](https://github.com/manuel-reyes-ml/data-portfolio#-postcheck--ai-powered-qa-review-agent)**<br>*AI-powered QA review agent* · flagship | Reviews posted distributions against the request and the SOP; every verdict feeds a dbt quality mart | 📐 | Document AI · Improving Accuracy of LLM Applications · Building with the Claude API · dbt Fundamentals |
| **[PolicyPulse](https://github.com/manuel-reyes-ml/data-portfolio#-policypulse--ai-powered-policy-assistant)**<br>*AI-powered policy assistant* · flagship | Cited-answer RAG → GraphRAG over policy documents, with a FastMCP server | 🏗️ | Building & Evaluating Advanced RAG · Introduction to MCP · IBM GenAI Engineering · Vercel Academy (Stage 2) |
| **[Crucible](https://github.com/manuel-reyes-ml/data-portfolio#-crucible--ai-assisted-trading-research)**<br>*AI-assisted trading research* · flagship | Backtest → paper → live; a deterministic core owns every order, with human sign-off and a kill switch | 🏗️ | CS50P · MITx 6.00.1x · Databricks Academy (Stage 2) · LangChain Academy (Stage 3) |
| [AFC](https://github.com/manuel-reyes-ml/data-portfolio#-afc--ai-powered-predictive-trigger-analysis-supporting)<br>*AI-powered predictive trigger analysis* · supporting | Faithfulness-gated filing analysis + an ML event study, reported as calibrated lift — never returns | 🏗️ | Machine Learning Specialization (Ng) · *Machine Learning for Trading* (Jansen) · *AI Engineering* (Huyen) |
| [FormSense](https://github.com/manuel-reyes-ml/data-portfolio#-formsense--ai-powered-form-validator-supporting)<br>*AI-powered form validator* · supporting | Multimodal extraction of distribution forms against a frozen Pydantic contract | 📅 | Document AI · Pre-processing Unstructured Data for LLM Apps · Building with the Claude API |

Every project also draws on the shared foundations — uv, pre-commit, Git workflow, C4 + ADRs, Docker. Course links and status are in **[What I'm learning](../README.md#-what-im-learning)**.

**Backlog:** StreamSmart and Operations Demand Intelligence — [details](https://github.com/manuel-reyes-ml/data-portfolio#-backlog--shared-components).

---

## 🧭 How the projects fit the plan

- **One system per project.** Each evolves Stage 1 → Stage 3 and is never rebuilt — Stage 2 adds the data-engineering layer, Stage 3 the applied-AI layer.
- **DataVault comes first.** Its Stage 2 hardening is the evidence gate that ends Stage 1, and until it ships, analytics/data-engineering build hours stay ≥ applied-AI hours every fortnight.
- **Build order:** DataVault → PolicyPulse → Crucible. PostCheck is scoped to ship independently, so it never blocks the gate; AFC's evaluation core is small enough to publish early.
- **Same bar everywhere.** Flagship vs supporting is size, not quality — every repo meets the [production standard](https://github.com/manuel-reyes-ml/data-portfolio#️-production-standard).

---

[Portfolio write-ups](https://github.com/manuel-reyes-ml/data-portfolio) · [Learning journey](../README.md) · [Roadmap v10.0](https://manuel-reyes-ml.github.io/learning_journey/roadmap.html) · [GitHub profile](https://github.com/manuel-reyes-ml)
