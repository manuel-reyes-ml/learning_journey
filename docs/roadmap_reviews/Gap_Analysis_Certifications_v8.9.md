# Gap Analysis — Slotting New Credentials into Roadmap v8.9
### Presented BEFORE any edit · per your additive-only + gap-analysis-first workflow
*July 1, 2026 · roadmap.html is 4,624 lines · line anchors below are from the current v8.9 file*

---

## How your roadmap actually tracks certifications (the real "§18/§21")
Your v8.9 file has **no literal §18/§21 markers** (those are from your 21-section *scope-document* template). The functional equivalents are:

| Your scope-doc concept | Where it actually lives in roadmap.html |
|------------------------|------------------------------------------|
| §18 stage-by-stage evolution | Per-stage **Core Courses** tables (Stage 1 ~L310, Stage 2 ~L1323, Stage 3 ~L2083, Stage 4 courses + month-by-month ~L2958) + the **Multi-Stage Project Evolution** table (~L874) |
| §21 skills–roadmap alignment | The **before/after summary** table (Skills/Portfolio/**Certifications** rows, ~L4170–4184) + the **Total Investment** cost table (~L4213–4236) + the **progression-path** overview (~L91–124) |

So "slotting a cert in" means **(a)** a new row in that stage's Core Courses table, **(b)** an update to the Certifications summary row (~L4183), and **(c)** a line in the cost table (~L4221–4225).

---

## PART 1 — SECTION B: roadmap-integrated credentials (added directly to each stage)

### B1 · Anthropic Claude Certified Architect — Foundations (CCA-F)
- **Primary slot → Stage 4 (Agentic AI Engineer, `id="stage4"` L2675).** Add as a row in the Stage 4 courses table and a milestone in the Stage 4 month-by-month next to the existing **IBM RAG & Agentic AI Professional Certificate** (~L2958). Rationale: the CCA-F blueprint (agentic orchestration 27%, MCP integration 18%, Claude Code 20%) maps 1:1 to Stage 4's agentic capstone and your Anthropic-SDK-first, MCP-server work.
- **Secondary touch → Stage 1 (L436).** You already pulled the free **MCP course** forward into Stage 1. Add a one-line note there: *"CCA-F prep (free Anthropic Academy courses) begins now; exam deferred to Stage 4."* This is additive, no restructuring.
- **Cost:** $99 (free for first 5,000 Partner Network employees; prep free).
- **Flag:** exam access currently gated behind the (free) Claude Partner Network — mark as *"exam when access opens; prep now."*

### B2 · Databricks Certified Generative AI Engineer Associate
- **Recommended slot → Stage 3 (ML Engineer, `id="stage3"` L1993),** as a new Core Courses row. Alternative: late Stage 2. Rationale: production RAG + LLM chains + **MLflow** + Vector Search + evaluation/monitoring overlaps your eval-first discipline and sits at the Stage 2→3 production boundary. Python-based, which matches your stack.
- **Cost:** $200 · 45 Q / 90 min · valid 2 yrs.
- **Optional companion to note (not add):** the new **Databricks Context Engineer Associate** (agent-context/governance) — watch-list item for Stage 4.

### B3 · NVIDIA certification ladder (you have the DLI *courses*, not the *exams*)
- **NCA-GENL (Generative AI LLMs, Associate) → Stage 3.** Slots **directly after the existing NVIDIA DLI row (L2108–2116).** The note at **L2115** already claims *"NVIDIA certifications are the new gold standard… replaces discontinued TF cert"* — but only the DLI **course** is listed. NCA-GENL is the **missing exam** that makes that sentence true. **Cost:** $125 · 50–60 Q / 60 min · 2-yr validity.
- **NCP-AAI (Agentic AI LLMs, Professional) → Stage 4.** New row in Stage 4. Bullseye for the agentic capstone (agent architecture, multi-agent, RAG, AI safety). **Cost:** verify (professional tier).
- **NCP-GENL (Generative AI LLMs, Professional) → Stage 5 (Senior LLM, L3512).** **Stage 5 currently has zero certifications** — this becomes its natural capstone credential (design/train/fine-tune LLMs, distributed training). **Cost:** verify (professional tier).

**Section B stage map at a glance**

| Stage | Add | Anchor |
|-------|-----|--------|
| 1 (L280) | CCA-F prep note (free) | after L436 MCP row |
| 3 (L1993) | Databricks GenAI Associate; NVIDIA **NCA-GENL** | Stage 3 Core Courses; after L2116 |
| 4 (L2675) | Anthropic **CCA-F**; NVIDIA **NCP-AAI** | Stage 4 courses + month-by-month (~L2958) |
| 5 (L3512) | NVIDIA **NCP-GENL** (first Stage-5 cert) | new Stage 5 courses row |

---

## PART 2 — SECTION A: employer track (NEW standalone section)

You asked for these kept **separate** from the roadmap's skill progression (employer-focused, reimbursable, parallel). Proposal:

- **New `<h2 id="employer-track">` section: "🏢 EMPLOYER TRACK — Daybright Azure / Copilot Certifications (Parallel, Reimbursable)."**
- **Proposed placement (pick one in Part 5):**
  - **(A)** Immediately after **CORE TOOLCHAIN** (~L191), before Stage 1 — reads as a parallel track up front.
  - **(B)** After **Stage 5** ends (~L3800), before the Investment Summary — keeps the 5-stage narrative clean, employer track as an appendix. *(My recommendation: B.)*
- **One cross-link** from the progression-path overview (~L91) pointing to `#employer-track`, so it's discoverable without being woven in.
- **Internal structure:** short intro (why separate + reimbursement mechanics: case-by-case via `learning@daybright.com`, manager sign-off, professional-development framing, first-two-attempts reimbursed, no bonus) + this stage-aligned table:

| Roadmap timing | Azure/Copilot credential | Code | Cost | Purpose |
|----------------|--------------------------|------|------|---------|
| Stage 1 (now) | Azure AI Fundamentals | AI-901 | $99 | Foundation; easiest first approval; proves the benefit path |
| Stage 1 (parallel) | Applied Skills: declarative agents in VS Code | — | Free | Hands-on, code-first, MCP-capable |
| Stage 2 *(optional)* | Fabric Data Engineer Associate | DP-700 | $165 | Azure-native counterpart to your AWS DE cert |
| Stage 3 | AI Agent Builder Associate | AB-620 | $165 | Building agents on Copilot Studio (Daybright's AI tool) |
| Stage 4 | Azure AI Apps & Agents Developer | AI-103 | ~$165 | Portable Azure AI-developer capstone |

- **Cost handling:** because these are **employer-reimbursed**, keep them **out of your personal Investment/ROI total** (~L4229) — show them in the employer-track table as *"$0 net (reimbursed)"* so they don't distort your personal-spend figure.

---

## PART 3 — Reconciliation flags (pre-existing items these edits touch)

1. **Stale TensorFlow references.** The Stage 3 note (L2115) already replaced the TF cert with NVIDIA narratively, but two summary tables still cite it: **Certifications row (L4183)** lists *"TensorFlow"* and the **cost table (L4224)** lists *"Stage 3: TensorFlow Certificate $100."* Adding NVIDIA NCA-GENL is the natural moment to reconcile these. **Per your additive-only rule, I will not remove them without your say-so** — see Part 5 Q2.
2. **Cert count.** The summary "19+" (L4183) would rise. Additive update only.
3. **Cost table total.** Adding B-track rows (Databricks $200, NVIDIA $125 + pro tiers, CCA-F $99) changes the **$530 TOTAL (L4229)**. Section A stays out of this total (reimbursed).

---

## PART 4 — Proposed edit sequence (one file, discrete approval units)
1. Stage 4: add CCA-F + NCP-AAI rows/milestones.
2. Stage 3: add Databricks GenAI Associate + NVIDIA NCA-GENL rows.
3. Stage 5: add NVIDIA NCP-GENL (first Stage-5 cert).
4. Stage 1: add CCA-F prep one-liner (L436 area).
5. New employer-track `<h2>` section (Section A) at chosen location + overview cross-link.
6. Summary/cost reconciliation (Certifications row + cost table) — pending your Part 5 answers.

Each step outputs to `/mnt/user-data/outputs/` for your manual review and commit. No automatic commits.

---

## PART 5 — Decisions needed before I touch the file
1. **Section A placement:** (A) after Core Toolchain, or (B) after Stage 5 / before Investment Summary? *(I recommend B.)*
2. **TensorFlow reconciliation:** replace the stale TF refs with NVIDIA NCA-GENL, or leave TF and add NVIDIA additively alongside?
3. **Databricks GenAI:** Stage 3 (recommended) or late Stage 2?
4. **Employer-track costs:** keep fully separate (reimbursed/$0), or also list in the main investment table?
5. **NVIDIA professional tiers (NCP-AAI, NCP-GENL):** add now as *"planned / stretch"* rows, or defer until you're closer to Stages 4–5?
6. **Version bump:** on apply, tag as **v9.0** (new employer-track section + credential additions) with a changelog entry — confirm the bump target.

Reply with your calls on 1–6 and I'll execute one edit at a time, gap-checked, additive, for your review.
