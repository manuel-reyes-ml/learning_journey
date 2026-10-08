# 🧭 Activation Plans v3.0 — Job-First Re-Cut · Changelog

**Approved:** 6 Oct 2026 (Manuel) · **Scope:** the six bi-weekly plans `WEEK_01_02` … `WEEK_11_12` · **Template:** fresh 12 weeks from Mon 20 Jul 2026 · **Hours:** 25/week, unchanged · **Aligned to:** roadmap v10.0, Corrections 1–56
**Roadmap:** the two corrections this re-cut created — **C55 and C56** — were approved and **applied to `roadmap.html` on 7 Oct 2026** (changelog entries + inline propagation; snapshot now 1–56; archive untouched). Their text is reproduced at the bottom.

---

## 1. Why the re-cut

**Target-role ruling (unchanged, C22 §3 + C54):** Analytics Engineer first door · Data Engineer parallel · Applied AI → FDE at Stage 3. A soft trigger (public DataVault dbt slice) opens a narrow, referral-led, domain-matched search; the full DataVault S2 ship opens the broad ~Q1 2027 search. Not a Data Analyst search.

**What the 6 Oct review found in the v2.x plans and repos:**

| # | Finding | v3.0 response |
|---|---|---|
| 1 | dbt mentioned 3× in 12 weeks with no build session; Snowflake and DuckDB 0× | dbt Fundamentals W5–6 · rehearsal Day 41 · DataVault dbt-first W7–8 · soft trigger Day 70 · dbt Advanced W11–12 |
| 2 | No job-search pipeline (no target list, résumé session or conversations; "referral" 2×) | Job lane from Day 1, three tiers, falsifier tracking |
| 3 | Plans aligned to C1–43 (footers 1–20); C44–C54 missing | Realigned; CU Boulder bridge in the Q2 shape and retro |
| 4 | Profile links to non-public flagship repos (404 for visitors); 1099 README still uses `pip install -r requirements.txt` and a non-matching clone slug | "No dead links" rule · PolicyPulse public Day 77 · 1099 quick fix Day 83 · README honesty pass Day 69 |
| 5 | 🆕 Your ruling: start the trading projects this quarter | Trading lane: market-data dbt rehearsal (Day 41) + AFC Phase-1 kickoff (Day 83) |

## 2. Changes by fortnight

| Fortnight | Main changes |
|---|---|
| **W1–2** | Master v3.0 block (lanes, milestone calendar, "what moved", trading-lane and job-lane rules, tooling note) · Step 7b pre-commit from commit one · Step 10 evidence file + private job workspace · LinkedIn headline (Day 7) · targets start (Day 14) |
| **W3–4** | Target list v0 — 15 companies, three tiers (Day 21) · first informational-conversation request (Day 28) · SQL framed as the dbt on-ramp |
| **W5–6** | dbt Fundamentals in AI Prompting's slots (→ flex) · Claude API target ~40% · 3.14 retrofit collapsed to reference · **Day 41: trading lane opens** — market-data dbt rehearsal with a lookahead singular test (DuckDB `ASOF JOIN`) · résumé v0 skeleton |
| **W7–8** | DataVault scaffolds with dbt · ADR 0002 "Python ingests, dbt decides" · recon buckets + Box-7 checks as dbt models, a unit test per rule (Python engine collapsed to reference) · `make run` end-to-end · corrections mart · targets → 30 |
| **W9–10** | `dbt build` blocking in CI (Day 61) · docs on GitHub Pages (Day 66) · Track A before-metrics on a work day (Day 68) · **v0.1.0 release + soft-trigger gate (Days 69–70)** · résumé v1, Featured, README honesty pass · S2 short labs → flex · AB-620 blocks moved fully to extra time |
| **W11–12** | Narrow search runs (applications + warm messages, falsifier tracker) · IBM GenAI PC → Q2; mornings to dbt Advanced, AE interview reps, AFC prep · PolicyPulse public (Day 77) · automation win drafted Day 77 · PostCheck knowledge capture (Day 81) · **Day 83: AFC Phase-1 kickoff** · retro items 9–12 (job lane, trading lane, C55/C56, CU Boulder) · Q2 shape (Snowflake port, AFC v1.0.0, ML Specialization at AFC Phase 2) |

## 3. What did not change

Dates (20 Jul – 11 Oct 2026) · 25 hrs/week and the block schedule · Day 82 as the last day of employment and its exit checklist · synthetic-data-only in public repos · propose→approve governance and preserve-and-append (superseded items are struck through or collapsed, never deleted) · certification canon · the extra-time rulings (AB-620, Google Git — outside the 25) · Crucible's position (third; no build this quarter) · the Build Progression order DataVault → PolicyPulse → Crucible.

## 4. Verify before executing

1. **dbt on Python 3.14:** dbt Core 1.12 is the first line supporting 3.14. Confirm `dbt-duckdb` resolves under uv on the day (Day 34 setup). If not, pin the newest version that resolves and write an ADR — do not lower the repo floor.
2. **Snowflake trial (Q2):** 30 days / $400, no card. Start it only once the port is scheduled.
3. ✅ **C55 and C56** — applied 7 Oct 2026. Bridge-tier applications are tracked separately so C55's falsifier can be read.
4. Still owed from earlier sessions: harness reversal (C39), AB-620 status change, hours-model exception.

## 5. Research basis (checked 6 Oct 2026)

- AE screening on dbt + a warehouse: KORE1, *How to Hire an Analytics Engineer: 2026 Guide* — kore1.com/how-to-hire-analytics-engineer-2026/
- What moves AE offers (one end-to-end public dbt project): analyticsengineering.com/resources/analytics-engineer-salary-guide
- How reviewers read a dbt portfolio (transformations, tests, macros, vars): r/dataengineering portfolio-review thread (May 2026 snapshot)
- GitHub as hiring due diligence: Pipeline To Insights, *The Data Engineer's GitHub Portfolio (2026 Edition)*
- Domain-matched postings: Vestwell Data Engineer (Jan 2026; Snowflake + dbt/Fivetran, 3–5 yrs) and Vestwell Analyst, Client Data Migration (Jan 2026; 2+ yrs financial/data operations, advanced SQL incl. reconciliations, recordkeeper feeds, Snowflake) — Duke Capital Partners job board · Ascensus process-excellence / transformation roles (Power Platform, Azure, RPA, agentic AI in 401(k) operations) — careers.ascensus.com, builtin.com
- Targeted vs mass applying: Huntr Q1 2026 Job Search Trends (via f1jobs.io) · referral share of hires: SHRM/Jobvite/LinkedIn aggregations (2026)
- dbt × Python: docs.getdbt.com Python compatibility matrix (3.14 from v1.12) · dbt-core v1.12.0 release notes (16 Jul 2026) · dbt-labs/jaffle_shop_duckdb PR #98
- dbt v2 / Fusion: duckdb.org/2026/09/22/dbt-fusion · docs.getdbt.com Fusion availability (DuckDB beta) · Fusion quickstart (VS Code extension requires Fusion)
- dbt for trading data: github.com/rajib-k-das/point-in-time-fundamentals (dbt + DuckDB, point-in-time SEC data) · github.com/pratri/market-data-pipeline (as-of filing-date joins in dbt) · DuckDB `ASOF JOIN` (motherduck.com glossary)
- Roadmap internals: AFC Stage-1 build sheet v9.1 (dbt listed "Not in S1"; 16-week timeline; early-artifact clause) · Build Progression (AFC/Crucible lakehouses at S2) · C22, C35, C44, C46–C48, C54

---

## 6. v10.0 CORRECTION 55 — ✅ applied to roadmap.html, 7 Oct 2026

**v10.0 CORRECTION 55 (October 2026 — domain-bridge tier admitted inside the C54 narrow search; same version):** triggered by the 6 Oct 2026 activation-plan review, which found live 2026 postings at retirement recordkeepers that read Manuel's operations experience as the requirement rather than a gap.
**(1) Ruling proposed:** inside the soft-trigger search, a **bridge tier** joins the target list — technical data roles at Tier-1 recordkeepers / TPAs whose titles may not contain "engineer" (data conversion / migration, data operations, implementation data, operations automation / agentic operations) — **only** where the posting requires SQL plus a warehouse or automation platform plus retirement-plan domain.
**(2) Why this does not reopen the analyst search:** the "not a Data Analyst search, under any circumstance" clause guards against the contracting generic 0–2-year analyst band. Bridge-tier postings ask for 2+ years of domain operations — the requirement Manuel meets — e.g. Vestwell's January 2026 *Analyst, Client Data Migration* (advanced SQL including reconciliations, recordkeeper feeds, Snowflake) and Ascensus's 2026 operations-automation roles (Power Platform / Azure / agentic AI in 401(k) operations).
**(3) Guardrails:** the dbt slice and DataVault S2 continue unchanged; a bridge offer is accepted only if the role works in SQL / a warehouse or an automation platform daily; AE / DE stays the destination title; AB-620's Copilot-ecosystem value is assessed against bridge-tier postings at renewal.
**(4) Falsifier:** if bridge-tier applications do not produce screens at a higher rate than AE / DE applications within the same 25-application window, the tier is dropped.
Propagation: Stage 1 exit criterion (soft-trigger note), Stage 2 referral-geography block. Cost: $0. No course, certification, book or hours figure changed; archive untouched; version stays v10.0.

## 7. v10.0 CORRECTION 56 — ✅ applied to roadmap.html, 7 Oct 2026

**v10.0 CORRECTION 56 (October 2026 — Stage-1 schedule pull-forwards recorded from the v3.0 activation-plan re-cut; same version):** the six activation plans were re-cut as a job-first 12-week template (25 hrs/week, from 20 Jul 2026). Recorded here so the roadmap stays authoritative over the plans.
**(1)** *dbt Fundamentals* (Stage 2 core row 5️⃣) is taken in Stage 1, Weeks 5–6, and *dbt Advanced Learning Paths* (row 6️⃣) starts Week 11 — Stage 2 learning done first, under C54 §5's "S2 work done first, not new scope".
**(2)** DataVault's Stage-1 reconciliation and Box-7 logic is built **as dbt models with tests** (C35 §2 made literal); Python owns generation, ingestion and the row-level contract.
**(3)** The IBM GenAI Engineering PC start moves from Week 11 to Q2 (after the soft trigger) — still inside its Months 3–6 window.
**(4)** AFC's Phase-1 kickoff lands on Day 83 under the AFC build sheet's early-artifact clause; a market-data dbt rehearsal runs in `learning_journey` (practice, not portfolio) on Day 41. AFC's own dbt work stays in S2, as the build sheet states.
**(5)** *AI Prompting for Everyone* moves to flex; the four S2 short DL.AI labs become flex inside the Pro month.
**Falsifier:** if the soft trigger slips past Week 12, the pull-forwards are reviewed before Q2 adds any new thread. Cost: $0. No course, certification or book added or removed; hours unchanged at 25/week; Crucible's position unchanged; archive untouched; version stays v10.0.
