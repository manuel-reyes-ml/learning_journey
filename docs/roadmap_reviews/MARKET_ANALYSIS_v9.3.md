# Market Analysis — Roadmap v9.3 Restructure

**Companion to:** `roadmap.html` v9.3 (2026 Market Realignment)
**Prepared:** July 9, 2026
**Subject:** Manuel Reyes — Plan Administrator (Daybright) → Applied AI Engineer
**Purpose:** Evidence base for every structural change in the v9.3 changelog, with salary bands for each target role and an honest bias rating on every source.

---

## 1. The Question

> *Is AI Engineering still suitable for 2026, or is it too crowded? Should I specialize in Data Science, ML Engineering, or AI/DE Systems Architecture instead?*

## 2. The Answer

**AI Engineering is the least saturated of the four options — but it is saturated at the *keyword* layer and starved at the *evidence* layer.** These are different markets. The v9.2 roadmap was optimized for the wrong one.

Two findings, held together, explain the whole restructure:

1. For people in AI Engineering, ML, or Forward Deployed Engineering, the 2026 market is described by hiring managers as *incredible*. For everyone else it is much less so.
2. Simultaneously, hiring managers report that candidates are rebranding as senior AI Engineers with resumes dense in RAG, evals, and inference keywords — *"but when digging deeper there is little substance."* Referrals have become the dominant channel because inbound is drowning in AI-generated applications.

The bottleneck is not access to the field. **It is proof.** That is good news for a candidate whose existing discipline is eval-first (DeepEval/RAGAS blocking gates, faithfulness ≥ 0.9) and whose domain is ERISA-regulated retirement plans.

---

## 3. The Structural Insight: There Are Only Three Real Jobs

A practicing CTO published an April-2026 audit after seeing this list of open titles in a single week: *AI Engineer, Applied AI Engineer, AI Software Engineer, Generative AI Engineer, GenAI Engineer, LLM Engineer, Prompt Engineer, Context Engineer, Agent Engineer, Agentic AI Engineer, RAG Engineer, AI Systems Engineer, AI Platform Engineer, AI Infrastructure Engineer, AI Reliability Engineer, Model Deployment Engineer, LLMOps Engineer, AI Ops Engineer, AI Evaluator, Evals Engineer, AI Red Teamer, Forward-Deployed Engineer, AI Solutions Architect… and "Builder."*

His conclusion: these collapse into roughly **three real jobs**, and everything else is branding.

| # | The actual job | Titles used | Median | Who wins this job |
|---|---|---|---|---|
| **1** | Builds products on top of foundation models | AI Engineer, Applied AI Engineer, LLM Engineer, GenAI Engineer, **FDE** | **~$185K** | Domain depth + systems sense + shipped evidence |
| **2** | Trains / fine-tunes models | ML Engineer, ML Research Engineer, Research Scientist | **~$265K** | **PhD common.** Older discipline. |
| **3** | Keeps AI infrastructure from catching fire | MLOps, LLMOps, AI Platform, AI Infrastructure, AI Reliability | **~$161K** | Senior infra engineers (5–10 yrs) |

### Applying this to the v9.2 roadmap

- **v9.2 Stage 3** (14 months, $400) trained for **Job #2** — the family where PhDs are common and 15 years of finance-domain expertise is worth nothing.
- **v9.2 Stage 5** (the destination) is **Job #1** — the family where that domain expertise *is* the moat.

> **The v9.2 roadmap spent 14 months qualifying for the job Manuel shouldn't want, in order to reach the job he already has an edge in.**

That single sentence is the entire case for the restructure. It does not depend on FDE, "AI Platform Engineer," or any other title.

**Corroborating evidence (technical, not market):** the correct 2026 adaptation sequence is **Prompt → RAG → Fine-tune → Distill**. Base models have closed most of the gaps that motivated fine-tuning two years ago. Fine-tuning is the *wrong tool* when the problem is a knowledge gap — that is RAG's job. The real cost of fine-tuning is not compute but data curation, evaluation, and 12-month lifecycle ownership. v9.2's Stage 3 capstone ("Fine-Tuned Financial LLM" via QLoRA) taught step 3 of 4 as if it were step 1.

**A regulated-finance-specific reason RAG beats fine-tuning:** retrieval can enforce per-document access clearance at query time. A fine-tuned model cannot — the knowledge is baked into the weights. For HIPAA/PCI-DSS/ERISA-adjacent workloads this is often decisive.

---

## 4. The Four Options, Scored

| Path | 2026 demand signal | Median comp | Entry barrier from current position | Verdict |
|---|---|---|---|---|
| **AI Engineer (applied)** | Fastest-growing title; demand **+74% YoY**; #1 fastest-growing US job (LinkedIn, 2026) | **~$185K** | Reachable in ~30 months via DE | ★★★★★ **Target** |
| **Data Engineer** | **Most undersupplied role in enterprise hiring** | $95–130K entry | Reachable in ~20 months | ★★★★☆ **Stepping stone** |
| **ML Engineer** | +38% YoY; growth has *cooled* relative to AI Engineer | ~$165–265K | PhD common; 14-month detour | ★★☆☆☆ Avoid as a career stop |
| **Data Scientist** | Demand growth **flattened to 12%**; role narrowed to causal inference & experimentation | ~$140K | Requires stats-research base built from zero | ★☆☆☆☆ **Drop** |
| **AI/DE Systems Architecture** | Real and well-paid | $140–332K | **Requires 5–8 yrs prior SWE/DS experience** | Destination, not entry |
| **AI Platform Engineer** | Real and well-paid | Glassdoor avg **$211K** | **Live postings require 5–10+ yrs software / 6–7 yrs cloud AI** | Destination, not entry |

**Note on Data Science:** it is *not* dying — BLS projects 33.5% growth through 2034, and data scientists were only ~3% of tech layoffs 2022–24 versus 22%+ for software engineers. It is simply the wrong fit here: it rewards statistical and experimental rigor over production engineering, and 73.9% of DS postings emphasize communication above any technical tool. Manuel's advantage is domain + systems, not causal inference.

---

## 5. Why Stage 1's Old Exit Criterion Had To Go

**v9.2 said:** Month 0 ~$90K (bookkeeper) → **Month 5: $65K (Analyst)**.

That is a **~$25K pay cut** into the single most AI-compressed entry role in data.

| Evidence | Detail |
|---|---|
| Entry-level contraction | In 2026 posting analysis, **every** data-analyst experience band grew **except 0–2 years**, which declined. The most sought band is 2–4 years. |
| Role hollowing | The 2026 analyst spends less time on query syntax and more on scoping, framing, and stakeholder translation. *"If the work is 'summarize this CSV and make a chart,' AI is good enough."* |
| Toolkit commoditized | Five years ago SQL + Python opened the door. Today those are **table stakes**. |
| Salary bands | US data analyst base 2026: **$72K–$98K entry**, $92K–$135K senior. Even the optimistic end of entry is a lateral move at best. |

**Replacement:** internal AI-builder elevation at Daybright. No pay cut, employer-funded certs (AI-901 → AB-620 via the Financial Industry Professional Education Program), two production references, and the domain moat compounds instead of resetting.

---

## 6. Why Stage 2's Goal Role Is "Data Engineer" — Not Something Fancier

Three titles were considered and rejected:

| Rejected title | Disqualifying evidence |
|---|---|
| **AI Systems Architect** | Solutions-architect roles require **5–8 years** of prior software engineering or data science experience. |
| **AI Platform Engineer** | Live Indeed/ZipRecruiter postings: **"5–10+ years software"**, *"6 years experience deploying scalable and responsible AI solutions on cloud platforms."* Glassdoor average **$211,468**. This is a senior title. |
| **Forward Deployed Engineer** | A destination, not a feeder label. Applying from here produces the exact resume hiring managers screen against. The CTO's worst 2026 rejection: *"Principal Agentic GenAI Forward-Deployed Context Architect"* — GitHub contained three forks of a LangChain tutorial. His best hire that year had **"Software Engineer"** on LinkedIn and three shipped production LLM systems. |

**Data Engineer is the correct goal role.** It is real, abundant, hireable, and currently **the most undersupplied role in enterprise hiring**. Every enterprise AI program needs reliable data infrastructure before it needs a model.

### Why DE is also the best on-ramp to FDE later

- Backend engineering, DevOps, **data engineering**, and ML engineering are the **most common documented backgrounds for FDE transitions**.
- **60%+ of Databricks resident solutions architects came from internal engineering roles with zero prior customer-facing work.** Companies hire for technical depth plus communication *potential*, then train the customer interaction.
- FDE hiring **values production experience over years-in-industry**: two years on-call for data pipelines counts for more than six years of analytics engineering with no production incident ever debugged.
- FDE demand **concentrates in fintech and highly regulated industries**, where engineers navigate compliance requirements alongside technical integration. This is Manuel's home field.

**This is why Stage 2 gained a production-operations layer.** It was the missing half of the stack.

---

## 7. Salary Bands for Every Target Role

All figures are US, 2026, base unless noted. Ranges vary by source; the spread is shown deliberately rather than averaged away.

| Role | Entry / Junior | Mid | Senior | Source & bias |
|---|---|---|---|---|
| **Data Analyst** (rejected) | $72K–$98K | — | $92K–$135K | KORE1 recruiter data blending Glassdoor, Levels.fyi, BuiltIn, Salary.com. *Medium-high — staffing firm, but discloses methodology and source spread.* |
| **Data Engineer** *(Stage 2 goal)* | $95K–$130K | $130K–$165K | $165K+ | Cross-source consensus; "most undersupplied enterprise role." *Medium — consultancy blog.* |
| **Data Scientist** (dropped) | — | **~$140K median** | $170K+ | BLS OEWS 2026 + Glassdoor. Demand growth flattened to 12%. *Medium.* |
| **ML Engineer** (detour cut) | — | **~$165K median** | $240K+ | Same. Demand +38% YoY. Job-family median for train/fine-tune work runs **~$265K** but *PhD common*. *Medium.* |
| **AI Engineer / Applied AI** *(Stage 4 goal)* | $130K–$200K TC | **~$185K median** | $200K–$350K | BLS OEWS 2026 via Second Talent; Axial Search analysis of 10,133 AI/ML postings gives median base **$187,500** (junior $150K / mid $193K / senior $240K). *Medium.* |
| **AI Platform / MLOps** (not targeted) | — | **~$161K median** | $180K–$250K TC | Glassdoor avg $211K; postings require 5–10 yrs. *Medium.* |
| **Forward Deployed Engineer** *(Stage 5)* | — | **Median $173,816–$190,000** | Base $215K–$310K | Live Data Technologies; Paraform (135–200K postings); KORE1. Posted bands cluster **$150K–$217K base**, midpoint $183K. *Medium — recruiting marketplaces.* |
| **FDE @ frontier labs** | — | — | **$350K–$550K TC** | Anthropic/OpenAI mid-to-senior bands; Palantir avg TC ~$238K, staff clearing $630K+. *Low-medium — heavily equity-weighted. **Treat as a ceiling, not a floor.*** |

### Premiums worth knowing
- LLM-focused engineers command **25–40% salary premiums** over generalist ML practitioners.
- Postings specifically requiring **RAG, agent orchestration, and LLM eval** experience carry a **25–40% premium** over comparable backend engineering roles.
- AI Engineers earn **15–25% above ML Engineers** at equivalent seniority (Dice / Levels.fyi 2026).
- Broader AI-skill wage premium: **~56%** vs non-AI peers (Addison Group 2026, refreshing PwC's AI Jobs Barometer).

### Realistic v9.3 salary path

| Milestone | Month | Comp |
|---|---|---|
| Plan Administrator (today) | 0 | ~$90K |
| Internal AI Builder, Daybright | 8 | ~$90–100K *(no cut)* |
| Data Engineer (first external move) | 20 | $95–130K |
| Applied AI Engineer | 31 | $130–170K |
| Senior Applied AI Eng / FDE track | 34+ | $175–250K |

**Honest framing:** v9.3 saves 3 months (37 → 34). **Speed is not the win.** The win is (a) never taking a $25K pay cut, and (b) not spending 14 months competing against PhDs in a job family where the finance moat is worth zero.

---

## 8. Remote-Work Reality Check

The v9.2 title said "Remote Global Track." That framing treated remote as free.

- AI Engineers: **~26% remote / ~27% hybrid.**
- One posting analysis puts **fully-remote AI roles at 5–8%** across DS/MLE/AI Eng.
- **Better odds by route:** Databricks RSAs are *mostly remote* (10–20% travel); Snowflake PSEs are often remote-first. Palantir-style FDE is travel-heavy.
- FDE geographic concentration has shifted: **New York (35% of postings) has surpassed San Francisco (11%)**, driven by fintech and regulated industries.

**Action:** plan hybrid, negotiate remote, bias the apply-list toward routes where remote is structurally normal.

---

## 9. Why Certifications Were Cut 24+ → 7

The v9.2 target of "24+ certifications" directly contradicts the document's own **"replace, not stack"** principle — and contradicts the market.

Hiring managers in 2026 report: *"Lots of people are rebranding themselves as senior AI Engineers… Their resumes now have lots of AI-related keywords mentioned, like RAG, evals, inference… but when digging deeper there is little substance."* Larger companies now run AI screening because inbound is saturated. **Keyword density is now a negative signal, not a positive one.**

### The surviving seven

| Cert | Cost | Track | Why it survives |
|---|---|---|---|
| Azure AI Fundamentals (AI-901) | $99 | Employer (reimbursed) | Cheapest first approval; proves the reimbursement path works |
| AI Agent Builder Associate (AB-620) | $165 | Employer (reimbursed) | Strongest Daybright alignment — RAG, MCP, multi-agent on Copilot Studio |
| Fabric Data Engineer (DP-700) *(optional)* | $165 | Employer (reimbursed) | Matches Daybright's Azure stack |
| AWS Certified Data Engineer – Associate | $150 | Personal | AWS leads AI job postings at **~40%** share (Azure ~30%, GCP ~25%) |
| Databricks Certified GenAI Engineer Associate | $200 | Personal | Industry's first production-GenAI cert; maps to the RSA path |
| Neo4j Certified Professional | Free | Personal | GraphRAG credential; free |
| Anthropic Claude Certified Architect (CCA-F) | $99* | Personal | Provider source-of-truth for the primary SDK |

**Cut:** NVIDIA NCA-GENL, NCP-AAI, NCP-GENL, TensorFlow Developer Certificate (discontinued May 2024), Google Data Analytics Professional Certificate. Coursera Professional Certificates are retained as *learning*, not listed as *credentials*.

**Note:** cloud-specific AI certifications do carry a documented **20–25% salary premium** — but for **professionals already working in the space**, not as a substitute for shipped systems.

---

## 10. The Local-LLM Thesis Was Wrong

**v9.2 claim:** *"Finance companies MUST run AI locally — regulatory constraints prohibit sending data to OpenAI."*

**Contradiction inside the same document:** Daybright runs **Microsoft 365 Copilot on Azure OpenAI** — a private endpoint inside a VPC, not on-premise. Regulated finance overwhelmingly uses private-endpoint cloud.

**Corrected thesis — "Privacy-Routed":**

| Data class | Destination |
|---|---|
| Participant PII, ERISA-regulated records | Local inference (Ollama, Qwen3.5) |
| Internal proprietary, non-PII | Private-endpoint cloud (Azure OpenAI, Bedrock, Anthropic SDK) |
| Public build scaffolding | Free tiers (Gemini free project) |

The scarce skill is **knowing which data goes where and being able to prove it in an audit** — not running a 9B model on a Mac Mini. That claim survives scrutiny. The old one did not.

---

## 11. Source Register — With Bias Ratings

Trust ratings reflect whether the source has a commercial incentive to reach the conclusion it reached.

| # | Claim | Source | Trust | Bias note |
|---|---|---|---|---|
| 1 | AI/ML/FDE market "incredible"; everyone else struggling; AI keyword-stuffing with "little substance"; referrals dominate | **The Pragmatic Engineer**, *Tech jobs market in 2026, Part 3* (July 2026) — 50+ hiring managers, engineers, and leaders interviewed | **HIGH** | Subscription newsletter; no product in this market. Best single source in the register. |
| 2 | Three real AI jobs; ~$185K / ~$265K (PhD common) / ~$161K; title chaos; the "Forward-Deployed Context Architect" rejection anecdote | **Ivan Turković**, practicing CTO, *AI Job Titles in 2026* (April 2026) | **HIGH** | Argues against his own industry's incentives. Anecdotes are single-source; the medians are cross-checkable. |
| 3 | AI Platform Engineer requires 5–10+ yrs software / 6–7 yrs cloud AI; avg $211,468 | **Live Indeed + ZipRecruiter postings**; Glassdoor salary page | **HIGH** | Primary source. |
| 4 | Only the 0–2 yr DA experience band declined in 2026; role has shifted to scoping/stakeholder work | **365 Data Science**, 1,000-posting analysis (April 2026); **KORE1** hiring guide | **MEDIUM-HIGH** | 365DS sells DA courses (incentive is to say the market is *good*, yet reports the decline anyway — which strengthens it). |
| 5 | Prompt → RAG → Fine-tune → Distill; base models closed the fine-tuning gap; real cost is curation + 12-mo lifecycle | **BigData Boutique** (May 2026) | **HIGH** | *Sells fine-tuning consulting and argues against fine-tuning.* Against-interest. |
| 6 | RAG enforces per-document clearance; fine-tuning cannot — decisive for HIPAA/PCI-DSS | RannLab enterprise RAG analysis (July 2026) | MEDIUM | Sells RAG. Mechanism is verifiable independently. |
| 7 | AI Eng +74% YoY / ML Eng +38% / DS +12%; medians $185K / $165K / $140K | **Second Talent**, citing BLS OEWS 2026 + LinkedIn Future of Work | MEDIUM | Staffing firm. Underlying BLS/LinkedIn sources are checkable. |
| 8 | Median AI/ML base $187,500 across 10,133 postings (junior $150K / mid $193K / senior $240K) | **Axial Search** posting analysis, via FoundRole | MEDIUM | Job board. Large N. |
| 9 | LLM-focused engineers earn 25–40% over generalist ML; RAG/agents/evals postings carry 25–40% premium | ODSC research, via Neil Dave | MEDIUM | Secondary citation; could not verify ODSC primary. |
| 10 | DE is the most undersupplied enterprise role | **Tredence** (April 2026) | MEDIUM | Consultancy. |
| 11 | Data Science is *not* dying: BLS 33.5% growth to 2034; DS was ~3% of tech layoffs vs 22%+ for SWE | BLS Employment Projections 2025; Indeed Hiring Lab, via Pin | **MEDIUM-HIGH** | Government primary + Indeed. Included specifically because it cuts *against* the recommendation to drop DS. |
| 12 | DE/DevOps/backend/MLE are the most common FDE feeder backgrounds; 60%+ of Databricks RSAs came from internal eng with no customer-facing experience; production experience > years-in-industry | **thedatascientist.com** / **fde.academy** | **LOW-MEDIUM** | ⚠️ **Both promote paid FDE training programs.** The "production experience > tenure" claim is independently corroborated by KORE1's recruiter writeup, which has opposite incentives. The 60% Databricks figure is **uncorroborated** — treat as directional. |
| 13 | FDE median $173,816–$190,000; bands $150K–$217K base; frontier-lab TC $350K–$550K; NY 35% of postings vs SF 11%; fintech/regulated concentration | Paraform; Recruiting From Scratch (135–200K postings); KORE1; MarkTechPost | MEDIUM | Recruiting marketplaces — incentive to inflate. Frontier-lab numbers are equity-weighted; **ceiling, not floor.** |
| 14 | Anthropic FDE spec: "production experience with LLMs including advanced prompt engineering, agent development, evaluation frameworks, and deployment at scale" | Anthropic FDE job specification, via MarkTechPost | **HIGH** | Primary job spec, secondhand. |
| 15 | AI Engineers ~26% remote / ~27% hybrid; fully-remote AI roles 5–8% of postings | HeroHunt (LinkedIn Jobs on the Rise data); Let's Data Science | MEDIUM | Two independent estimates, same direction. |
| 16 | Cloud AI certs → 20–25% salary premium *for those already in the space*; AWS ~40% / Azure ~30% / GCP ~25% of AI postings | Nucamp, via HeroHunt | MEDIUM | Bootcamp-adjacent. |
| 17 | RAGAS four-metric decomposition (faithfulness / answer relevancy / context precision / context recall) is the dominant 2026 RAG eval framework | Sthambh (April 2026) | MEDIUM | Consultancy. Technically verifiable. |
| 18 | ~~1.6M open AI roles vs 518K candidates; 3.2:1 gap; 143% YoY growth~~ | ~~FutureProofing.dev~~ | **DISCARDED** | ❌ Staffing agency selling engineers at $13.5K/month. Numbers unverifiable and directly serve the sales pitch. **Excluded from all reasoning above.** |

---

## 12. What Could Make This Analysis Wrong

Stated up front, because a three-year plan deserves a falsification list:

1. **Title medians conflate seniority.** "AI Engineer ~$185K" mixes a 3-year startup engineer with a staff engineer at a lab. Entry bands are materially lower.
2. **"Demand +74% YoY" is measured off a tiny 2023 base.** Percentage growth on a new category is not the same as absolute opportunity.
3. **The DE→FDE conversion evidence leans on sources selling FDE training.** The mechanism is plausible and partly corroborated; the specific 60% figure is not independently verified.
4. **Agentic AI could compress the Applied AI Engineer role** the way it compressed the data analyst role. The hedge is the same one that protects Manuel today: domain depth plus the eval/verification layer, which is the part that does not automate.
5. **Daybright may not grant the internal elevation.** If Months 1–8 produce no scope change, Stage 1's exit criterion fails and the plan should fall back to an external Data Engineer search at Month 12 — *not* to a Data Analyst search.
6. **Salary data lags.** Every figure here is Q1–Q2 2026. Re-check bands before any negotiation.

---

## 13. Open Items Requiring Decision

| # | Item | Options |
|---|---|---|
| 1 | AWS DE Associate ($150, personal) vs DP-700 ($165, reimbursed) | AWS has ~40% posting share; DP-700 is free and matches Daybright's Azure stack. Could do both. |
| 2 | Georgia Tech OMSCS (previously mapped to Stages 2–4) | Not addressed in v9.3. A master's substitutes for the ML-literacy stage and hardens the Job #2 door — but adds 2–3 years. Needs a separate decision. |
| 3 | Which flagship survives — AFC or Crucible? | v9.3 cuts the portfolio to 2 flagships + 3 supporting. Crucible is the chosen first build; AFC is read-only research. Both cannot stay flagship. |
| 4 | Month numbering inside stage bodies | Stage headers, summary boxes, and the transformation table are updated to v9.3 offsets. Some month-by-month sections inside Stages 2–5 still carry v9.2 offsets. Flagged, not silently rewritten. |

---

*Prepared as a companion to roadmap v9.3. Every claim above is traceable to the source register in §11. Where a source had an incentive to reach its conclusion, that incentive is disclosed. Where a source contradicted the recommendation, it is included anyway (see §11 row 11).*
