# Roadmap v10.0 Review — Agent 1 (Claude)

> **Archived review** — Claude's independent analysis of Career Roadmap v10.0.
> **Source:** Pasted directly in chat.
> **Subject:** Full audit of `roadmap.html` v10.0 against 2026 hiring-manager & recruiter data.
> **Archived:** July 13, 2026

---

## Research process (as reported by the agent)

I'll start by reading your roadmap v10.0 in full so my research is anchored to your actual stages, targets, and the certifications you already have slotted in. Then I'll pull recruiter/hiring-manager data from the web to pressure-test each stage.

The file is large (5,157 lines, with a v9.2 archive at the bottom). I extracted the key v10.0 sections — the certifications list and each stage's course tables — so I reviewed the actual current state, not memory. I read the three v10.0 stage sections in full detail so I captured every course and cert exactly before researching.

With a complete inventory of every course and cert across the three stages in hand, I researched what recruiters and hiring managers actually value in 2026 — starting with the most cert-sensitive stage (Stage 2, DE/AE), then Stage 3 (Applied AI/FDE), then Stage 1 (Azure/Copilot).

Key mid-research findings that shaped the audit:

- Microsoft is renaming its AI certs (AI-102 retiring June 30, 2026; AI-103 replacing it), so I verified the exact codes in your Stage 1 employer track (AI-901, AB-620) against Microsoft's current 2026 catalog.
- Microsoft launched several new AI-era certs in 2026 (AI-103 Azure AI Apps & Agents Developer, DP-750 Azure Databricks Data Engineer) that didn't exist when v10.0 was written — and both sit squarely on your employer's Azure stack.
- AB-620 is fully verified and perfectly placed. Key distinction confirmed: AB-620 is low-code Copilot Studio (maker path) while the new **AI-103** is code-first Azure AI Foundry (Python SDK, custom agents, multi-agent orchestration) — directly relevant to your Applied AI identity.
- The FDE research strongly validates your Stage 3 thesis — it's explicitly portfolio/performance-driven ("the credential market has not caught up"), NYC-fintech-concentrated, and eval-engineering is "the 2026 non-negotiable." Your regulated-finance domain edge is directly confirmed.
- I verified two specifics: the Anthropic CCA-F credential (very new) and the analytics-engineer/dbt cert reality.

I anchored to `roadmap.html` as the governing source for your stages, courses, and certs (it's your protected source-of-truth, so it's the right document for a cert-gap review).

---

## Headline verdict

Your roadmap is remarkably well-aligned to what the 2026 market actually rewards — more so than most plans I'd review. The single strongest cross-cutting signal in the data validates your entire philosophy: recruiters and ATS/VMS screeners now treat a coherent skills story of two to three targeted certifications paired with real projects as far stronger than a wall of unrelated badges — one cloud cert plus one platform cert plus two or three solid projects beats five disconnected credentials every time. Multiple independent 2026 analyses land on the same rule: one relevant cert, one real project, and strong fundamentals. Your "replace, not stack" and evidence-first stance isn't just defensible — it's exactly the meta the market is screening for.

So this isn't a "you're missing a bunch of certs" review. It's a "three factual updates and two or three genuinely new, employer-funded options that appeared *after* you wrote v10.0" review — driven mostly by Microsoft's mid-2026 certification overhaul, which reorganized the entire Azure catalog around AI and agents.

---

### Stage 1 — Internal AI Builder (AI-901, AB-620)

**Verdict: complete and current. No changes needed.** Both employer-track certs check out against the live 2026 catalog.

- **AI-901 is correct** — you're already ahead of a trap here. AI-900 was replaced by AI-901 (Azure AI Fundamentals, same certification name), and AI-900 retires June 30, 2026. A stale roadmap would still say "AI-900"; yours doesn't. One nuance worth noting: AI-901 now includes basics of Python and implementation using Microsoft Foundry, so it's slightly more hands-on than the old fundamentals exam.
- **AB-620 is verified and an ideal fit.** It's the AI Agent Builder Associate exam, generally available June 2026, an intermediate developer-focused certification for building, integrating and managing enterprise agents in Microsoft Copilot Studio, at a USD 165 fee. Its syllabus maps directly to your internal-elevation story with Jen: it covers MCP tools, A2A multi-agent collaboration, Foundry integration, enterprise knowledge sources, Azure AI Search, and agent evaluation with test sets.

One forward-looking flag (not a Stage 1 change): the data surfaced a clean distinction you'll want to exploit later — AB-620 is the low-code Copilot Studio maker cert, while AI-103 is the code-first Azure AI Foundry cert for custom agentic apps with Python/.NET SDK, tool calling, and multi-agent orchestration; many enterprises run both side by side. Hold that thought for Stage 3.

---

### Stage 2 — Data Engineer / Analytics Engineer (DP-700, AWS DEA-C01 + conditionals)

**Verdict: your two committed certs are the two S-tier certs. One high-value swap to consider.**

Your committed pair is exactly right. The 2026 S-tier that consistently appears in US job requisitions and VMS filters names AWS Certified Data Engineer – Associate (DEA-C01) as the gold standard for cloud-native pipeline roles, and Microsoft Fabric Data Engineer Associate (DP-700) as essential for enterprise environments migrating to Microsoft Fabric. DEA-C01 is also the volume play: it has the most job openings, because the sheer number of AWS-powered enterprises creates the largest pool of actively hiring data engineering roles. Your conditional trio (dbt AE, SnowPro Core, Databricks DE — take one, never stack) matches the market precisely, and your decision to decline GCP PDE is well-supported: it's the top credential specifically for BigQuery-heavy and ML-adjacent analytics roles, which isn't your Azure-internal / AWS-external trajectory.

**My single best recommendation for this stage:** Microsoft launched a brand-new cert that didn't exist when you wrote v10.0 — **DP-750, Azure Databricks Data Engineer Associate.** It covers designing and implementing scalable, secure data pipelines using Azure Databricks, intended for data professionals building real-time analytics and AI-ready data foundations in the cloud, with the exam expected to go live in May 2026. This is strictly better than your conditional "Databricks DE Associate ($200 personal)" for your situation: it delivers the same lakehouse/Spark signal, but it's a **Microsoft cert on your employer's exact Azure stack — so it's employer-reimbursable**, not a $200 personal spend. If your Month 12–14 apply-list skews Databricks/lakehouse, take DP-750 through the reimbursement path instead of the vendor-neutral Databricks exam.

**Secondary option:** the **Databricks Certified GenAI Engineer Associate** currently sits in your Stage 3, but the DE-side data now treats it as a Stage-2-caliber credential — the certification that defines 2026 for data engineering, because every data engineering job at top companies now mentions AI integration, RAG pipelines, vector databases, or LLM-powered features. Given your explicit "AI-focused Data Engineer" framing and the AI-adjacent DE evidence you're already building in Stage 2 (embedding pipelines, vector stores), it's worth *noting* it as a bridge credential that doubles as a Stage 2 asset. I wouldn't move it — the Databricks hands-on requirement fits better in Stage 3 — but flag it in the Stage 2 skill plan as "also reads as a DE cert."

---

### Stage 3 — Applied AI Engineer → FDE (CCA-F, Databricks GenAI, NCA-GENL, Neo4j)

**Verdict: strategy is sound and the FDE thesis is strongly validated. One factual price correction, and one genuinely new employer-funded cert to add.**

The FDE research confirms your whole endgame framing. It's portfolio-driven, not credential-driven: the credential market has not caught up, Anthropic has said publicly that roughly half its technical staff had no prior ML experience, and OpenAI runs a six-month residency for engineers who don't currently focus on AI. The skill stack the postings demand — traditional software engineering combined with LLM evals, RAG production, system design for LLM products, and deep customer empathy — is exactly what your Stage 3 builds, and eval engineering is the 2026 non-negotiable, which is your blocking-gate discipline. Two details that specifically reward *your* positioning: New York now accounts for 35% of all FDE postings, tracking with fintech and compliance-heavy industries that need hands-on deployment support, and the "decomposition" case-study interview validates your CS50 restoration.

Your cert choices hold up. NCA-GENL is correctly positioned as the LLM infrastructure credibility credential, and CCA-F is aligned to your Anthropic-first identity — one working-engineer analysis calls it the one quietly becoming the AWS Solutions Architect of the LLM era, the credential that signals you're hireable into senior AI engineering roles in a way nothing else on the market currently does.

**Factual correction:** CCA-F is no longer $99. Anthropic moved the Claude Certified Architect – Foundations exam onto Pearson VUE, live from June 30, 2026, with a new $125 fee, up to 4 retakes per 12 months, and a 12-month term with free renewal — while the exam content stays identical. Also, Anthropic has since expanded to a four-track program covering three roles (Associate, Developer, Architect) and two levels (Foundations, Professional) — so there's now a code-first **Developer** track alongside the customer-facing Architect track. Your Architect (CCA-F) choice is still right because it maps to the FDE/solution-scoping endgame, but the Developer cert is worth knowing about for your code-first identity.

**My single best recommendation for this stage (and arguably the whole roadmap):** add **AI-103 — Azure AI Apps and Agents Developer Associate.** This is the successor to the retiring AI-102, and it's a different animal: it validates building modern AI-powered applications, agent workflows, RAG solutions, and production-ready generative AI systems on Azure, marking a shift toward agentic development on Microsoft Foundry. It's the highest-leverage single addition available to you because it stacks four things at once — it's brand new, it's **employer-reimbursable** (Azure stack), it maps 1:1 to your Applied AI Engineer target, and it's the code-first Azure-native counterpart to CCA-F and the Databricks GenAI cert. It turns your employer track into a genuine on-ramp to the Applied-AI destination rather than stopping at DP-700.

**Evaluated but I'd decline** (consistent with your own logic): the **AWS ML Engineer Associate (MLA-C01)**, cited as one of the most relevant AI certifications in 2026 for data engineers and MLOps engineers working in AWS environments, validating the ability to implement and operationalize ML workloads in production, with an intended candidate having at least a year of SageMaker experience. It's real and valued — but it sits on the ML-engineer/SageMaker path you deliberately cut, so it's off-trajectory. Log it as evaluated-not-selected; revisit only if a target employer is SageMaker-heavy.

---

### What I'd change (pending your approval — no edits made)

1. **Stage 3 factual fix:** CCA-F cost `$99` → `$125` (Pearson VUE migration, June 30 2026), with a note on the new 12-month term + free renewal.
2. **Stage 3 add:** **AI-103 (Azure AI Apps & Agents Developer Associate)** to the employer-reimbursable track as the code-first Azure counterpart to CCA-F — the roadmap's clearest new bridge from employer stack to Applied-AI destination.
3. **Stage 2 swap-in option:** replace the conditional "Databricks DE Associate ($200 personal)" with **DP-750 (Azure Databricks Data Engineer, employer-reimbursed)** as the lakehouse-coverage path, keeping vendor-neutral Databricks as a fallback only for non-Azure Databricks shops.
4. **Two annotations (no structural change):** note AI-901's expanded Python/Foundry scope in Stage 1; note that Databricks GenAI "also reads as a DE cert" in the Stage 2 skill plan.

Everything else — your committed pair (DP-700 + DEA-C01), the conditional platform-cert menu, NCA-GENL, Neo4j, the GCP decline, and the whole course spine — I'd leave exactly as is. The data backs it.

---

*Closing offer:* Want me to draft these as additive edits with Conventional Commit messages (strikethrough convention preserved, version bump to note the cert audit), and deliver to an outputs copy for your manual review? I can also cross-check the findings against your Learning Journey and `data-portfolio` GitHub docs in the same pass if you'd like the cert taxonomy synced there too.
