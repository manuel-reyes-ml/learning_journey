# v10.0 CORRECTION 22 — Gap Analysis + Paste-Ready Blocks

**Status:** OUTPUT COPY — awaiting your sign-off before anything is pasted into `roadmap.html`.
**Rule observed:** additive-only · archive untouched · version stays **v10.0** · no structural teardown · Claude touches no source files and no git.
**Date:** August 2026
**Cost:** $0

---

## PART 1 — GAP ANALYSIS

### Gap A — Stage 1 exit criterion is structurally dead (highest severity)

**Current state:** Stage 1 exits via internal AI-Builder elevation at Daybright, with an external DE/AE search documented only as a *fallback* triggered at Months 10–12.

**Fact that supersedes it:** Resignation tendered and accepted **in writing**, two-month handover, **last day of employment 9 October 2026**.

**Consequence:** internal elevation cannot occur. The fallback is no longer a fallback — it is the only path. The Stage 2 apply window compresses from Months 12–14 to approximately **Q1 2027**.

**Proposed ruling:** convert the documented fallback to the **primary path**; re-anchor Stage 1's exit to an *evidence* gate (DataVault S2 hardening shipped) rather than an *employer* gate.

---

### Gap B — Hours model is anchored to an employment state that ends 9 Oct 2026

**Current state:** the file's global banner and all budgets assume **25 hrs/week** (line 38, line 155 total row, line 1149, line 1631).

**Consequence:** every downstream time budget in the file is anchored to a constraint with a known expiry date. After 9 October the constraint materially loosens.

**Proposed ruling:** record a **two-phase hours model** — Phase A (now → 9 Oct 2026) holds 25 hrs/week unchanged; Phase B (post-9 Oct) expands, with the expansion **spent on DataVault S2 hardening first**, not on new courses. The 25 hrs/week banner stays as written (it is the standing planning baseline); Phase B is recorded as a dated amendment, not a global rewrite.

---

### Gap C — Target-role decision was never written down as a ruling

**Current state:** dual DE/AE targeting is implied throughout Stage 2 but has no single ruling line, and SWE / DevOps / AI-Engineer-direct were never formally evaluated and declined.

**Evidence gathered (Aug 2026, live sources):**

| Finding | Source quality |
|---|---|
| AI-engineer postings: only **2.5%** target 0–2 yrs experience; market centre is 3–7 yrs | Posting analysis (~1,000 postings) — ⚠️ industry publisher |
| SWE listings rose ~30% to 67,000+, but entry-level hiring at the 15 largest tech firms **fell 25%**; 22–25-year-old developer employment down ~20% | Market analysis — ⚠️ industry publisher |
| Entry-level DevOps is among the most competitive in tech, **hundreds of applicants per opening**; lateral-entry norm | Careers publisher — ⚠️ directional only |
| DE hiring **+23% YoY**; junior tier down ~40–67%; senior/specialised grew | Consistent with the finding already on record in this file |
| AE roles fill in **4–7 weeks**; deep SQL + SWE instincts + dbt-in-a-few-weeks is the bar | Practitioner/recruiter account — ⚠️ directional |
| **"Business context beat tool depth every time"** among DEs surviving layoff waves | Practitioner account |

**Proposed ruling:** **Analytics Engineer first door, Data Engineer parallel.** Rationale recorded as: it is the only target where the Daybright production-data work, the DataVault artifact, and the **ERISA moat** all read as *experience* rather than as a beginner portfolio. SWE and DevOps logged as **evaluated, not selected** — not for lack of demand (both are strong) but because the entry tier is the most contested in tech and the domain moat transfers at ~zero.

---

### Gap D — Language stack has no ruling line; four candidates evaluated this session

**Proposed rulings — all four declined, each with a falsifier:**

1. **Rust — evaluated, not selected.** Premium is real ($110K–$210K global; senior US $170K–$300K+; postings +35% YoY; TIOBE 13 → 7) but concentrates in **senior systems/infra and crypto**, with systems Rust paying 15–25% above application Rust at the same seniority. Practitioner consensus in DE is decisive: Rust is the language the *tools* are written in, consumed through **Python bindings** — Polars, DataFusion, delta-rs — and this roadmap already consumes it via **ruff and uv**. Even pro-Rust analysis concedes the general premium compresses as the talent pool doubles every ~18 months.
   **Falsifier:** re-evaluate at Stage 3 **only** if Crucible's live-execution path presents a genuine latency/memory-safety requirement — the one place in this portfolio where Rust's actual value proposition applies. Decided by ADR then, not by a course now.

2. **Go — evaluated, not selected.** Genuinely popular and well paid (median $145K–$165K, **15–20% above equivalent Python/JS backend roles**; ~12% of client API calls per Cloudflare Radar). But its role concentration is **cloud providers/infrastructure, fintech transaction systems, and the cloud-native ecosystem** — i.e. the DevOps/backend/platform lane declined in Gap C. Absent from DE/AE posting bars.
   **Falsifier:** revisit only if a Stage 3 target employer names Go in a posted JD.

3. **Java — evaluated, not selected.** Appears at **22.6%** of DE postings and 22% of AI-engineer postings, but concentrated in legacy Spark/Hadoop and enterprise JVM shops — the exact segment **PySpark is displacing** (Spark + Python co-occurs more often than Spark + Scala). Practitioner verdict: Java and Scala "are not required for most data engineering roles." Scala (17.5%) declined on the same grounds.
   **Falsifier:** a target employer posting a JVM-first data platform role.

4. **JavaScript as a separate sprint — declined as redundant.** JavaScript at **3.4%** of DE postings. More importantly, **TypeScript is a superset of JavaScript** — the existing Stage 2 row 18 TS sprint *already is* the JS sprint. No separate item can be justified.

**Confirmed and unchanged (recorded as a positive ruling, not merely an absence):**
- **SQL is the #1 language signal in DE postings at 79.4%** — ahead of Python. The highest-ROI "additional language" available is **depth in the one already held**: window functions, query optimisation, warehouse cost awareness, `Snowflake + SQL` and `dbt + Snowflake` posting pairs.
- **Python 71–73.7%** across DE, and **71% of AI-engineer postings** (#1 skill).
- **PySpark logged as the capturable differentiator** — Spark at 41.1% of DE postings with a real salary premium, reachable **through Python**, no Scala required. Already carried by the Stage 2 Big Data phase; this ruling names it explicitly.

⚠️ **Evidence-quality flag:** the posting-percentage figures are from data-education and interview-prep publishers analysing job-board corpora (1,000-posting and 4,000+-posting analyses), **not peer-reviewed research**. Adoption rests on **convergence across four independent 2026 analyses** producing consistent orderings, plus practitioner corroboration. Directional, and recorded as such — same standard as CORRECTIONS 18 and 19.

---

### Gap E — TypeScript + MCP sprint: build target and timing

**Current state (Stage 2 row 18):** HF MCP Course (primary) · Microsoft MCP for Beginners (secondary) · Total TypeScript Beginner + Zod (Week 1) · official MCP TS SDK quickstart → build one TS MCP server (Week 2). Timed at **~M14**.

**Two gaps found:**

1. **No AI-application-layer build target.** The sprint produces an MCP server but nothing demonstrating the **"last mile"** — the layer 2026 sources identify as TypeScript's actual job: *Python for the model, TypeScript for the things around the model*. Adoption datapoint: **62% of TypeScript projects started in 2026 use the Vercel AI SDK**, which is described as the industry standard for streaming AI UIs and is model-agnostic across 25+ providers with an Anthropic-fallback pattern in production use.
   **Proposed:** add **Vercel AI SDK as the Week-2(b) build target** — a streaming Claude-powered UI over PolicyPulse's existing retrieval. Not a course; a deliverable. This is FDE-round evidence no Python-only portfolio carries.
   **Guardrail recorded:** TS remains the last mile **only**. Sources are explicit that TS frameworks "lack the depth for complex multi-agent collaboration, long-horizon planning, and tool ecosystems — if building agents is your core product, choose Python." PolicyPulse, AFC and Crucible stay Python-primary.

2. **Timing is anchored to the pre-resignation calendar.** "~M14" was set when the apply window sat at Months 12–14. Under Gap A it must move so MCP/TS evidence is **fresh at interview**, not stale.
   **Proposed:** re-anchor to **immediately before the compressed Q1 2027 apply window**, and subordinate to DataVault S2 — the sprint never competes with the evidence gate.

---

### Gap F — Packt TypeScript course (per your instruction)

**Finding, stated plainly:** this course is **not currently in the roadmap.** All three `Packt` occurrences in the file are the *Docker & Kubernetes Masterclass* (Stage 2 row 9 + Archive mirror). It surfaced in this session's research only. Therefore "do not remove" resolves to **add, marked optional**.

**Governance note:** the **v8.9 ruling declined Coursera TypeScript material as frontend/framework-heavy**, and that ruling is currently cited inside row 18. Adding this course is a **partial amendment** to that ruling, logged here rather than left as a silent contradiction. Scope of the amendment: the v8.9 ruling declined *specializations*; this is a single 7-hour course that covers **Node.js as well as browser targets**, so the frontend-heavy objection applies only in part.

**Recorded honestly:** Coursera-Plus-included (**$0 marginal**), shareable certificate — which per the **CORRECTION 19 credential ladder is Tier 4/5, never a Certifications line**. Marked **⏸️ OPTIONAL — overflow only**, taken only if the Total TypeScript free tutorials leave a gap.

---

### Gap G — Snapshot counter is stale

**Current state:** line 43 reads *"Corrections 1–20 applied"*; the changelog already runs through **21 + addendum**.
**Proposed:** correct to **1–22**. (Same class of fix as CORRECTIONS 17, 18 and 19 each made.)

---

## PART 2 — PASTE-READY BLOCKS

### BLOCK 1 — Changelog entry
**Insert:** immediately after line 87 (the CORRECTION 21 addendum `</li>`), before the Archive-policy `<li>` at line 88.

```html
<li>🛠️ <strong>v10.0 CORRECTION 22</strong> (August 2026 — resignation re-anchoring; target-role and language-stack rulings; TS+MCP sprint upgraded and re-timed; same version): triggered by a change in external facts, not by a review. <strong>(1) 🔴 RESIGNATION RE-ANCHORING — the Stage 1 exit criterion is superseded.</strong> Resignation from Daybright tendered and <strong>accepted in writing</strong> with a two-month handover; <strong>last day of employment 9 October 2026</strong>. Internal AI-Builder elevation can no longer occur, so the <em>documented fallback</em> (external DE/AE search, previously triggered at Months 10–12) is <strong>converted to the primary path</strong>, and Stage 1 now exits on an <strong>evidence gate — DataVault S2 hardening shipped — not an employer gate</strong>. Apply window compresses from Months 12–14 to <strong>approximately Q1 2027</strong>. <strong>(2) ⏱️ Two-phase hours model recorded.</strong> Phase A (now → 9 Oct 2026): <strong>25 hrs/week unchanged</strong>, handover obligations honoured in full. Phase B (post-9 Oct): hours expand, and the expansion is <strong>spent on DataVault S2 hardening first — not on new courses</strong>; the 25 hrs/week banner stands as the standing planning baseline. <strong>(3) 🎯 Target-role ruling written down for the first time: Analytics Engineer first door, Data Engineer parallel.</strong> Rationale: it is the only target where the Daybright production-data work, the DataVault artifact and the <strong>ERISA moat</strong> read as <em>experience</em> rather than as a beginner portfolio — AE roles fill in 4–7 weeks on a deep-SQL + software-instincts bar with dbt learnable in weeks, DE hiring grew <strong>+23% YoY</strong> while the junior connect-A-to-B tier collapsed, and the trait practitioners name as decisive is that <em>business context beat tool depth every time</em>. <strong>❌ Software Engineer — evaluated, not selected:</strong> overall demand is strong (listings +~30% to 67,000+) but entry-level hiring at the 15 largest tech firms <strong>fell 25%</strong> with 22–25-year-old developer employment down ~20%, and a generic SWE loop values the finance/data moat at approximately zero. <strong>❌ DevOps / SRE — evaluated, not selected:</strong> demand is genuinely accelerating, but entry-level DevOps is among the most contested openings in tech (hundreds of applicants per posting) and the discipline is entered <em>laterally</em> from sysadmin/backend/SWE work because it is a trust role; the compensating fact is that this roadmap's production standard (Docker, GitHub Actions CI, pre-commit, structlog, monitoring) <strong>already embeds the DevOps layer inside a data role</strong>, capturing the skill without the competition. <strong>❌ AI Engineer as a first external title — evaluated, not selected:</strong> only <strong>2.5%</strong> of AI-engineer postings target 0–2 years, with the market centre at 3–7 years; it stays the Stage 3 destination reached <em>through</em> DE/AE, exactly as this file already sequences it. <strong>❌ ZTM career paths (AI Developer / AI Engineer / DevOps / Data Engineer / Software Engineer) — evaluated, not selected:</strong> course quality is well reviewed, but the paths are built for complete beginners and end below the level this roadmap already operates at (uv/ruff/mypy/structlog/CI with ADRs and C4); adopting one would duplicate active curriculum and trade build hours for video hours. The standing "ZTM = evidence, not credential" ruling (v9.1) and the Employer-Track ZTM study path are <strong>untouched</strong>. <strong>(4) 🔤 LANGUAGE-STACK RULINGS — Python + advanced SQL confirmed correct and sufficient; four candidates declined with falsifiers.</strong> Posting evidence: <strong>SQL 79.4%</strong> (the single highest-signal language in DE postings, <em>ahead of Python</em>), <strong>Python 71–73.7%</strong> in DE and <strong>71% in AI-engineer postings</strong>, <strong>Spark 41.1%</strong> with <code>Spark + Python</code> co-occurring more often than <code>Spark + Scala</code>. Consequence: the highest-return "additional language" is <strong>depth in the one already held</strong> — window functions, query optimisation, warehouse cost awareness, and the <code>Snowflake + SQL</code> / <code>dbt + Snowflake</code> posting pairs — and <strong>PySpark is named explicitly as the capturable posting-signal differentiator, reachable through Python with no Scala required</strong>. <strong>❌ Rust — evaluated, not selected:</strong> the premium is real ($110K–$210K global, senior US $170K–$300K+, postings +35% YoY, TIOBE 13 → 7) but concentrates in <strong>senior systems/infrastructure and crypto</strong> (systems Rust pays 15–25% above application Rust at equal seniority), and in data engineering the practitioner consensus is that Rust is the language the <em>tools</em> are written in and consumed through <strong>Python bindings</strong> — Polars, DataFusion, delta-rs — which this roadmap <em>already consumes via ruff and uv at zero language-learning cost</em>; even pro-Rust analysis concedes the general premium compresses as the talent pool doubles roughly every 18 months. <strong>Falsifier:</strong> re-evaluate at Stage 3 only if Crucible's live-execution path presents a genuine latency/memory-safety requirement — decided by ADR then, not by a course now. <strong>❌ Go — evaluated, not selected:</strong> popular and well paid (median $145K–$165K, <strong>15–20% above equivalent Python/JS backend roles</strong>; ~12% of client API calls per Cloudflare Radar) but its role concentration is cloud providers/infrastructure, fintech transaction systems and the cloud-native ecosystem — the DevOps/backend/platform lane declined above — and it is absent from DE/AE posting bars. <strong>Falsifier:</strong> a Stage 3 target employer naming Go in a posted JD. <strong>❌ Java — evaluated, not selected:</strong> present at <strong>22.6%</strong> of DE postings and 22% of AI-engineer postings, but concentrated in legacy Spark/Hadoop and enterprise JVM shops — the segment PySpark is displacing — with the practitioner verdict that Java and Scala are not required for most DE roles; <strong>Scala (17.5%) declined on the same grounds</strong>. <strong>Falsifier:</strong> a target employer posting a JVM-first data platform role. <strong>❌ JavaScript as a separate sprint — declined as redundant:</strong> JavaScript appears in <strong>3.4%</strong> of DE postings, and more decisively <strong>TypeScript is a superset of JavaScript</strong>, so the existing Stage 2 row 18 sprint already <em>is</em> the JavaScript sprint. Recorded for the avoidance of doubt: <strong>Java and JavaScript are unrelated languages</strong> sharing a 1995 naming decision and nothing else. ⚠️ <strong>Evidence-quality flagged in-file:</strong> the posting percentages come from data-education and interview-prep publishers analysing job-board corpora (a 1,000-posting and a 4,000+-posting analysis among them), <strong>not peer-reviewed research</strong>; adoption rests on <em>convergence across four independent 2026 analyses producing consistent orderings</em> plus practitioner corroboration, and is recorded as directional — the same standard applied in CORRECTIONS 18 and 19. <strong>(5) 🔨 TypeScript + MCP Server Sprint upgraded and re-timed (Stage 2 row 18).</strong> Gap found: the sprint shipped an MCP server but produced <strong>nothing at the AI-application layer</strong> — the layer 2026 sources identify as TypeScript's actual job (<em>Python for the model, TypeScript for the things around the model</em>). <strong>Vercel AI SDK added as the Week-2(b) build target</strong> — not a course, a deliverable: a streaming Claude-powered UI over PolicyPulse's existing retrieval. Selected on adoption evidence: <strong>62% of TypeScript projects started in 2026 use it</strong>, it is the named industry standard for streaming AI UIs, and it is model-agnostic across 25+ providers with the Anthropic-fallback pattern already in production use — matching this file's provider-agnostic architecture. <strong>Guardrail recorded:</strong> TypeScript stays the <em>last mile only</em>; the same sources are explicit that TS frameworks lack the depth for complex multi-agent collaboration and long-horizon planning, and that agent-core work belongs in Python — so <strong>PolicyPulse, AFC and Crucible remain Python-primary</strong>. <strong>Timing re-anchored:</strong> the "~M14" placement was set against the pre-resignation calendar; the sprint now sits <strong>immediately before the compressed Q1 2027 apply window</strong> so the MCP/TS evidence is fresh at interview, and it is <strong>subordinate to DataVault S2 — it never competes with the evidence gate</strong>. <strong>(6) ⏸️ Packt "Ultimate TypeScript Course" added as OPTIONAL overflow only (per approval).</strong> Recorded honestly: this course was <strong>not previously in this file</strong> (all prior Packt references are the Docker &amp; Kubernetes Masterclass), so this is an addition, not a restoration. Coursera-Plus-included (<strong>$0 marginal</strong>), ~7 hours, shareable certificate — which is <strong>Tier 4/5 on the CORRECTION 19 credential ladder and never a Certifications line</strong>. <strong>Partial amendment to the v8.9 ruling</strong> that declined Coursera TypeScript material as frontend/framework-heavy: that ruling addressed <em>specializations</em>, and this single course covers Node.js alongside browser targets, so the objection applies only in part — the amendment is logged rather than left as a silent contradiction, and <strong>the v8.9 ruling otherwise stands</strong>. Taken only if the free Total TypeScript tutorials leave a gap; <strong>Total TypeScript remains the primary Week-1 spine</strong>. <strong>(7) Snapshot corrected — the Current State Snapshot read "Corrections 1–20 applied" while the changelog already ran through 21 + addendum; now <strong>1–22</strong>.</strong> <strong>Cost: $0</strong> (Vercel AI SDK is free and open-source; the Packt course is Coursera-Plus-included; every ruling above is a decline or a confirmation). Additive-only apart from the snapshot count and the two in-row edits to Stage 2 row 18; <strong>no course removed, no ruling deleted</strong>; archive untouched; <strong>no structural teardown; version stays v10.0.</strong></li>
```

---

### BLOCK 2 — Snapshot counter fix (line 43)

**Find:**
```html
<li><strong>Version:</strong> v10.0, Corrections 1–20 applied · Evidence-first, replace-not-stack, production-grade from Stage 1.</li>
```
**Replace with:**
```html
<li><strong>Version:</strong> v10.0, Corrections 1–22 applied · Evidence-first, replace-not-stack, production-grade from Stage 1.</li>
```

---

### BLOCK 3 — Stage 2 row 18 in-row additions (line 297)

**3a — Insert immediately after the existing `🔨 <strong>Week 2:</strong> …` sentence, inside the same `<span>`:**

```html
<br>🚀 <strong>Week 2(b) — AI last-mile build target (🆕 v10.0 CORRECTION 22):</strong> <a href="https://ai-sdk.dev/" target="_blank">Vercel AI SDK</a> (FREE, open-source) — build a <strong>streaming Claude-powered UI over PolicyPulse's existing retrieval</strong>. Not a course; a deliverable. Chosen on adoption evidence: <strong>62% of TypeScript projects started in 2026 use it</strong>, it is the named industry standard for streaming AI UIs, and it is model-agnostic across 25+ providers — matching this file's provider-agnostic architecture and Anthropic-primary routing. ⚠️ <strong>Guardrail:</strong> TypeScript is the <em>last mile only</em> — TS frameworks lack the depth for multi-agent collaboration and long-horizon planning, so <strong>PolicyPulse, AFC and Crucible stay Python-primary</strong>.<br>⏸️ <strong>Optional overflow (🆕 v10.0 CORRECTION 22, per approval):</strong> <a href="https://www.coursera.org/learn/packt-ultimate-typescript-course-2024-learn-build-excel-ogzyf" target="_blank">Packt — Ultimate TypeScript Course</a> (Coursera Plus, $0 marginal, ~7 hrs, shareable certificate = <strong>Tier 4/5, never a Certifications line</strong>). Take <em>only</em> if the free Total TypeScript tutorials leave a gap; <strong>Total TypeScript remains the primary Week-1 spine</strong>. Partial amendment to the v8.9 ruling (which declined Coursera TS <em>specializations</em> as frontend-heavy — this is a single course covering Node.js alongside browser targets); the v8.9 ruling otherwise stands.
```

**3b — Duration cell.** Find `<td>2 weeks (~M14)</td>` in this row and replace with:

```html
<td>2 weeks — 🔄 <strong>re-timed v10.0 CORRECTION 22:</strong> immediately before the compressed <strong>Q1 2027</strong> apply window (was ~M14, set against the pre-resignation calendar) so MCP/TS evidence is fresh at interview; <strong>subordinate to DataVault S2 — never competes with the evidence gate</strong></td>
```

---

## PART 3 — WHAT I NEED FROM YOU

1. **Approve / amend Blocks 1–3** as drafted.
2. **Confirm Gap F handling** — you now know the Packt TS course was never in the file; confirm you still want it added as optional overflow (Block 3a includes it as drafted).
3. **Phase B hours figure** — I deliberately left post-9-Oct hours **unquantified** ("expands"). If you want a number in the file, tell me the figure and I'll draft the amendment.
4. **Downstream propagation is NOT included here.** Corrections 21-style all-scope propagation would touch the 14 project scope documents, the 5 public-facing docs, and the `1099_reconciliation_pipeline` README (still flagged as carrying retired career-path framing). Say the word and I'll scope that as a separate pass — it should not ride inside this correction.
