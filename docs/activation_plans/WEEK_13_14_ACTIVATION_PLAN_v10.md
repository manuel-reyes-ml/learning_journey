# 🚀 WEEKS 13–14 MASTER ACTIVATION PLAN (v10.0)
## AI-901 Sprint + DataVault S2 Orchestration + 📈 AFC Build Begins | October 12–25, 2026

**Document Version:** 1.0 — 📈 created with the v3.3 **TRADING LANE EXPANSION** (13 Oct 2026, roadmap C64) · continues the 12-week template that started Mon 20 Jul 2026
**Covers:** Monday, October 12 – Sunday, October 25, 2026 (Stage 1 · Month 4 · Weeks 13–14 · Quarter 2 opens)
**Aligned To:** Career Roadmap v10.0, **Corrections 1–64** · Target: **Analytics Engineer first door · Data Engineer parallel** (C22 §3, C54)
**Prerequisite:** Weeks 11–12 metrics ≥80% and the Month-3 retro (Day 84) written. ⚠️ **This plan was generated before that retro, at your request (13 Oct 2026).** If the retro changes the hours model (item 8) or the Q2 shape (item 6), the retro wins and this plan is re-cut first — propose→approve, as always.
**Weekly Hours:** 25 · extra time outside the 25: the 📈 trading thread (~2 h, its last two weeks) + Google Git (~2 h) · pause rule unchanged: above ~29 h/week, extra time pauses before any flagship does.

> 🤖 **Agent Policy:** Phase 3, as Weeks 11–12 ended it, unless the retro's agent-policy review (item 4) changed it. The Q1 carve-outs carry into AFC: eval logic, perturbation labels and ADRs stay human-authored. The EDGAR adapter is ordinary plumbing — scaffold it with the agent under diff review.

> 🗓️ **Template dates.** Days 85–98 keep the template's calendar (Mon 12 Oct – Sun 25 Oct 2026), like Weeks 1–12. The block times are the template's too. Day 82 was your last day of employment, so if the retro moves your clock, keep the **block lengths** and move the times.

---

## 🧭 THIS FORTNIGHT — the lanes and the hours

| Lane | This fortnight | Hours |
|---|---|---|
| **L3 Applied AI** | 🎯 **AI-901 sprint + exam** (moved here by C58): one ~14 h sprint weighted to Microsoft Foundry, exam **Day 96** | **14.0 h** |
| **L2 AE/DE build** | **DataVault S2 — orchestration starts:** an Airflow DAG that runs the pipeline idempotently by logical date, with retries and a failure hook · **Track B #6–#7** on the public `1099_reconciliation_pipeline` | **15.0 h** |
| **L4 Trading** 📈 | **AFC build sheet Week 1, second slice:** the dependency spike (ADR-0005) and the EDGAR adapter with cache and provenance · **twin catch-up block** (3 h) | **9.0 h** |
| **L1 Foundations** | **Astronomer Academy — Airflow 101** (Stage 2 row 7️⃣, pulled forward like dbt was) · dbt Advanced → finish · **Kimball Ch. 6** · CS50P | 5.5 h |
| **L5 Job search** 🚦 | Narrow search continues: tailored applications incl. **Tier 3 (trading)** with the new market-data artifacts · warm messages · posts #13–#14 | 4.5 h |
| Review | Week 13 summary · **Day 98 fortnight review** | 2.0 h |
| *Extra time (outside the 25)* | 📈 **Trading thread, Weeks 13–14:** Crucible data spike part 2 + ADR draft, then the falsifier check and the `market_rehearsal` README · 🐙 Google Git → finish | ~4 h/week |
| | **Total inside the 25** | **50.0 h** |

⚖️ **Priority guardrail (C58 · C59):** AE/DE build **15.0 h** ≥ Applied AI **14.0 h** ✅. Tight on purpose: AI-901 was moved into this fortnight alone so that it would not share a fortnight with the Pro month (Weeks 1–2, v3.2 block). If the sprint runs over, the overflow comes out of Foundations, never out of DataVault.

**What is not here, on purpose:** the Sprint-1 Pro month and the PolicyPulse judge gate (a later Q2 fortnight, C59), the IBM GenAI PC (its window is set at the retro, C56), the Snowflake port (it starts a 30-day trial clock, so the retro schedules it), and the **CU Boulder bridge**, which opens in November (C44) — the retro names what pauses to make room, replace-not-stack.

---

## 🔄 WHAT THIS FORTNIGHT INHERITS

1. **AI-901 is self-funded, $99** (C22/32/37). Check for a voucher first — C38 notes Cloud Skills Challenge and virtual training day vouchers recur. The Day 54 exam-day protocol in Weeks 7–8 (kept as reference) applies unchanged.
2. **The guardrail keeps running** until DataVault S2 hardening ships (C59). Orchestration is one of the gate's six pieces: ingestion → dbt-tested models in CI ✅ → **orchestration** → contracts ✅ (Days 72–74) → Docker/ECS deploy → monitoring, with ADRs, a C4 view and a postmortem.
3. **AFC's Day-83 kickoff** left the repo bootstrapped (CI Tier 0 green, README replaced, ADRs 0001–0002) and a dependency-spike checklist written but not run. This fortnight runs it.
4. 📈 **The twin queue** (`notes/trading/twin-queue.md`) holds any twin from Weeks 1–12 that did not fit its day. Two catch-up blocks clear it.
5. 📈 **The trading thread** is in its last two weeks. Its exception **lapses on Day 98** (C64), and AB-620's extra-time study takes the slot back in Week 15.

---

## 🧠 STRATEGIC CONTEXT

### AI-901 — what the exam measures now (Microsoft Learn study guide, checked 13 Oct 2026)

The skills list is dated **15 April 2026** (page updated 13 July 2026). **Pass mark: 700.** The practice assessment now lives in Microsoft's **AI Skills Navigator**.

| Skill area | Weight | Sprint hours |
|---|---|---|
| Identify AI concepts | 40–45% | 1.5 h (one session) + whatever drills the practice scores point to |
| **Implement AI solutions with Microsoft Foundry** — generative AI apps and agents · text and speech · computer vision and image generation · information extraction | **55–60%** | **7.5 h** (five sessions) |
| Practice assessments (baseline, #2, #3) and gap drills | — | ~2.75 h |
| Skills-outline review, booking, the exam | — | ~2.25 h |
| | | **14.0 h** |

Your Weeks 3–6 study notes used AI-900-era concept labels, which map to the smaller half (the Weeks 7–8 realignment note). This sprint is weighted the other way: **five of the nine study sessions are Foundry.** The concepts half is the easier one, so it gets one session plus targeted drills. If an exercise needs an Azure subscription, use a free account, set a $5 budget alert first, and delete the resource group the same day.

### DataVault S2 — why orchestration comes first

It is the next gate piece that needs no trial clock. The Snowflake port starts a 30-day trial the day you open it, so the retro schedules it; orchestration can start today on what you already have. The design rule is the one DataVault was built on: **Airflow schedules, retries and records; DataVault's own commands do the work.** Airflow lives in its own environment and calls DataVault through `BashOperator`, so the two dependency sets never mix.

- **Airflow 3.3.2** (released 17 Sep 2026) lists Python **3.10–3.14** on PyPI, so the 3.14 floor holds. Install it the official way, with the constraints file for your Python version. The banked `constraints-3.13.txt` workaround from Weeks 5–6 is the fallback only if the 3.14 file fails to resolve — and then for the Airflow environment only (C28).
- Run it locally with `airflow standalone` for now. Docker comes with the Docker/ECS gate piece, not before.
- `dbt build` as one `BashOperator` task is enough for v0. `astronomer-cosmos` (one Airflow task per dbt model) is the hardening upgrade — name it in the ADR as *considered, deferred*.

### AFC — the build sheet's Week 1, second slice

AFC v9.1 §12 puts six things in Week 1. Day 83 did the bootstrap and two ADRs. This fortnight does the two that carry risk:

| Deliverable (sheet §6) | Acceptance | Why now |
|---|---|---|
| **#2 Dependency spike** | DeepEval, edgartools and selfcheckgpt (or not) installed on 3.14 **inside the Docker image**; result in **ADR-0005** | The sheet rates "eval dependencies don't install on 3.14" 🔴 High, and it is already confirmed for `factscore` |
| **#4 EDGAR adapter** | Fair-access compliant; cache + provenance manifest; **acceptance datetime captured**; tests use recorded fixtures (no network in CI) | Every later AFC deliverable reads through it — and it is where the two-clock lesson from Day 41 becomes real code |

Real SEC filings are allowed in the AFC repo because they are public records — **ADR-0004** says so explicitly, keeps the PII-redaction processor on and states the one boundary: no employer or non-public data, ever. Write it in the same session as the adapter.

### New concepts
```
Orchestration:  DAG · task · logical date ({{ ds }}) · idempotent re-runs ·
                retries + retry_delay · on_failure_callback · catchup=False ·
                DAG-integrity test (zero import errors)
AI-901:         Foundry projects, model deployment, agents · speech + language ·
                vision + image generation · content/information extraction
AFC:            fair-access client (User-Agent, ≤10 req/s) · content-addressed
                cache · provenance manifest · acceptanceDateTime · recorded fixtures
Model:          Kimball Ch. 6 — accumulating snapshot · header/line facts ·
                role-playing dates (one lifecycle, many milestones)
```

---

## 🗓 WEEK 13 (Oct 12–18)

### Week 13 goals

- [ ] AI-901 booked (voucher checked) · baseline practice assessment logged · five Foundry sessions
- [ ] Airflow 101 done · orchestration ADR written · DAG v0 runs end-to-end · idempotent re-run proven
- [ ] Track B #6: structlog + PII redaction + a `capture_logs` test on the public 1099 repo
- [ ] 📈 AFC dependency spike run → ADR-0005 · twin catch-up block 1
- [ ] 📈 Extra time: Crucible spike part 2 → ADR draft
- [ ] 🚦 1 tailored application · 1 warm message · post #13

### 📌 DAY 85 — Monday, October 12
**Morning:** 90 min 🎯 **AI-901 — open the sprint.** Read the skills outline line by line and mark each line ☐/🚧/✅ against what you know. Take the **baseline practice assessment** in AI Skills Navigator and log the score per skill area in `notes/certs/ai-901.md` — that table decides where the drills go. Check for a voucher, then **book the exam for Friday 23 October (Day 96)**.
**Evening:** 90 min **Astronomer Academy — Airflow 101, part 1** (free; DAGs, tasks, scheduling, the UI) · 30 min 🚦 **Job lane** — tracker + one Tier-1 warm message · journal + commit

### 📌 DAY 86 — Tuesday, October 13
**Morning:** 90 min 🎯 AI-901 — **Foundry 1/5: generative AI apps** (create a project, deploy a model, test it in the playground, call it from Python). Notes in your own words.
**Evening:** 120 min 🛠️ **Track B #6** on the public `1099_reconciliation_pipeline` — `structlog` with `ProcessorFormatter` + the `redact_pii` processor, and a test with `structlog.testing.capture_logs` asserting that a fake SSN never appears in output (`cache_logger_on_first_use=False` in tests) · journal + commit (`feat(logging): structlog with PII redaction`)

### 📌 DAY 87 — Wednesday, October 14
**Morning:** 90 min 🎯 AI-901 — **Foundry 2/5: agents** (an agent with a tool and instructions; what the service runs for you versus what you write).
**Evening:** 60 min **Airflow 101, part 2** (operators, retries, the logical date) · 60 min 🛠️ **DataVault — orchestration ADR** (`docs/adr/`, Nygard): Airflow per the roadmap; local `airflow standalone` in its own uv environment now, Docker at the deploy step; `BashOperator` → DataVault's `make` targets; `astronomer-cosmos` considered, deferred; the 3.14 constraints check and its fallback · journal + commit

### 📌 DAY 88 — Thursday, October 15
**Morning:** 90 min 🎯 AI-901 — **Foundry 3/5: text and speech** (language analysis, speech-to-text, text-to-speech).
**Evening:** 120 min 🛠️ **DataVault DAG v0.** First split `make run` into four targets (`generate`, `normalize`, `dbt-build`, `export`), each taking `DS=<date>`. Then the DAG, in a new `orchestration/` folder with its own `pyproject.toml`:
```python
"""DataVault daily run: Airflow schedules and retries; DataVault's own commands do the work."""

from datetime import timedelta

import pendulum
from airflow.providers.standard.operators.bash import BashOperator
from airflow.sdk import DAG

REPO = "cd ~/dev/datavault && "            # DataVault's own uv environment runs every step

with DAG(
    dag_id="datavault_daily",
    schedule="@daily",
    start_date=pendulum.datetime(2026, 10, 1, tz="America/New_York"),
    catchup=False,
    default_args={"retries": 2, "retry_delay": timedelta(minutes=5)},
    tags=["datavault", "s2"],
) as dag:
    steps = [
        BashOperator(task_id=target, bash_command=REPO + f"make {target} DS={{{{ ds }}}}")
        for target in ("generate", "normalize", "dbt-build", "export")
    ]
    steps[0] >> steps[1] >> steps[2] >> steps[3]
```
> The quadruple braces are an f-string escape: Python writes `{{ ds }}`, and Airflow's Jinja fills in the run's logical date. Trigger it once from the UI; all four tasks green = DAG v0. Journal + commit.

### 📌 DAY 89 — Friday, October 16
**Morning:** 90 min 🎯 AI-901 — **Foundry 4/5: computer vision and image generation.**
**Evening:** 90 min 🛠️ **Idempotency, proven at the orchestrator** — trigger the DAG twice for the **same** logical date (`airflow dags test datavault_daily 2026-10-15`, twice) and assert identical row counts in every mart: Day 66 proved it for `dbt build`; this proves it for the whole run. Write the check as a script the next steps can reuse, and record the result in the ADR · 30 min 🚦 one tailored application (log it against n/25) · journal + commit

### 📌 DAY 90 — Saturday, October 17 (5.5h)
**Morning (5:00–8:30):**
- [ ] 150 min — 📈 **AFC deliverable #2: the dependency spike** — run Day 83's checklist. In the AFC Docker image on `python:3.14-slim`: `uv add` DeepEval and edgartools, then try `selfcheckgpt` (0.1.7: sdist only, unpinned torch/transformers/spaCy). Record for each package: resolves? installs? imports? image size? Then write **ADR-0005** — what installed, what did not, and the fallback the sheet names (D-4: re-implement the SelfCheck prompt variant if the library fails). A failed install is a result, not a blocker.
- [ ] 60 min — **dbt Advanced → finish** (the last paths) · badges into `evidence.md`

**Evening (8:00–10:00):** 120 min 📈 **Twin catch-up block 1** — work `notes/trading/twin-queue.md` from the top: oldest first, because later twins build on earlier ones (#7 needs #6's generator). Tick each one in the queue as it ships. Queue empty? The time goes to the AFC adapter (Day 97). · journal + commit

### 📌 DAY 91 — Sunday, October 18 (2h)
60 min week summary + ⚖️ **priority check** (fortnight-to-date AE/DE vs Applied AI from the journal) + AI-901 practice-score table updated + plan Week 14 · 60 min 🚦 draft + publish **post #13** — artifact: the DAG graph and the idempotency check (*"I ran the same day twice and nothing changed — on purpose"*) · journal 🎉

> 📈 **Extra-time trading thread — Week 13 (~2 h · v3.3, C64): Crucible's data spike, part 2.**
> - **Delisted coverage** (§5.4 column 3): pick five names that delisted or merged between 2018 and 2025 — EDGAR Form 25 filings are the survivorship-free place to find them — and ask each candidate source for their history. Served or not, per source.
> - **Earnings endpoints:** Finnhub `/calendar/earnings` and Alpha Vantage `EARNINGS` on their free keys. Served, gated, or partial — one line each. If either is gated, Crucible's fallback is EDGAR 8-K Item 2.02 (§5.4).
> - **Close-price agreement** (column 6): 20 random dates × SPY + 11 sector funds, between each pair of sources. State the tolerance before you look (e.g. 0.5% on raw closes) and record the pass rate.
> - **ADR draft** — `notes/trading/adr-drafts/crucible-0001-price-source.md`: the primary and fallback price source, the spike table attached (counts, dates and yes/no only — never prices), and the falsifier from §5.4. It moves into the Crucible repo when Crucible bootstraps.

---

## 🗓 WEEK 14 (Oct 19–25)

### Week 14 goals

- [ ] 🎯 **AI-901 TAKEN (Day 96)** — Foundry 5/5 · concepts · practice #2 and #3 (target ≥ 80%) done first
- [ ] DAG hardened: retries, failure callback, DAG-integrity test in CI · ADR final
- [ ] Track B #7: `pydantic-settings` + `SecretStr` + `stamina` retries
- [ ] Kimball Ch. 6 read against DataVault and the order lifecycle
- [ ] 📈 AFC EDGAR adapter: acceptance datetime captured, fixtures green, ADR-0004 · twin queue empty
- [ ] 📈 Extra time: thread falsifier checked · `market_rehearsal` README public · the exception closed on Day 98
- [ ] 🚦 2 tailored applications, one Tier 3 with the market-data artifacts · post #14

### 📌 DAY 92 — Monday, October 19
**Morning:** 90 min 🎯 AI-901 — **Foundry 5/5: information extraction** (pull fields out of documents and forms into structured output — your day job's problem, in Microsoft's service).
**Evening:** 120 min 🛠️ **DAG hardening** — an `on_failure_callback` that writes one structured log line naming the task and logical date (email later, with monitoring); a pytest that loads the DAG folder and asserts **zero import errors** (the DAG-integrity pattern from Airflow 101), wired into DataVault's CI; README ①Production gains one honest line: *"runs daily under Airflow locally; not yet deployed"* · journal + commit

### 📌 DAY 93 — Tuesday, October 20
**Morning:** 90 min 🎯 AI-901 — **Identify AI concepts** (the 40–45%): AI workloads, machine-learning basics, responsible-AI principles. One page of your own definitions, each with an example from your work or projects.
**Evening:** 90 min 🛠️ **Track B #7** — `pydantic-settings` with `SecretStr` for every credential, and `stamina` retries on anything that touches a network or a file share; tests for both · 30 min **Kimball Ch. 6, part 1** — order management: header and line facts, role-playing date dimensions · journal + commit

### 📌 DAY 94 — Wednesday, October 21
**Morning:** 90 min 🎯 AI-901 — **practice assessment #2** → drill the two weakest skill areas from your table, nothing else.
**Evening:** 90 min 🛠️ DataVault — finalize the orchestration ADR with what the week taught (the idempotency result, what the failure hook does and does not do yet) + a C4 **container** view update showing Airflow beside the pipeline · 30 min **Kimball Ch. 6, part 2** — the **accumulating snapshot**. In `docs/modeling-notes.md`, sketch two: a trading order (submitted → partially filled → filled → settled) and a distribution (received → IGO/NIGO → processed → 1099 issued — PostCheck's core). Same shape, one row per lifecycle, a date column per milestone · journal + commit

### 📌 DAY 95 — Thursday, October 22
**Morning:** 30 min 🎯 AI-901 — **practice assessment #3**, light review only; no new material the day before · 60 min 🛠️ DataVault — run the idempotency script against the hardened DAG; commit the evidence
**Evening:** 90 min 🛠️ DataVault — merge the orchestration branch, `CHANGELOG.md`, tag **v0.3.0** with release notes (*"scheduled, retried, idempotent by logical date"*) · 30 min 🚦 Job lane — tracker; pick the Tier-3 posting for Friday · early night

### 📌 DAY 96 — Friday, October 23 · 🎯 AI-901 EXAM
**Morning:** 90 min — 🎯 **the exam** (book any slot that day; post-employment, a daytime slot is fine and the 4:30 block becomes rest). Protocol: the Day 54 reference in Weeks 7–8. Pass → score report and Credly link into `evidence.md`; draft the résumé line and a post the same day. Miss → log the gap areas, rebook within 48 hours (another $99), no spiral.
**Evening:** 60 min 🚦 **two tailored applications** — one Tier 1, and one **Tier 3 (trading)** that links the work a trading-data team can open: `market_rehearsal` (two clocks, the `ASOF LEFT JOIN`, a restatement handled two ways, SCD2 from vendor updates) and the AFC repo. If the `market_rehearsal` README is not up yet, send the Tier-3 one next week · 60 min **CS50P** (next week's lecture) · journal 🎉

### 📌 DAY 97 — Saturday, October 24 (5.5h)
**Morning (5:00–8:30):**
- [ ] 150 min — 📈 **AFC deliverable #4: the EDGAR adapter** (`src/afc/edgar/`). Requirements — build them; the plan no longer hands you the file:
  - **Fair access:** a declared `User-Agent` with your contact email; at most 10 requests/second, enforced in code, not by hope.
  - **Cache:** raw bytes on disk keyed by accession number; a cached file is never re-pulled.
  - **Provenance manifest:** one row per fetch — URL, `fetched_at` (UTC), SHA-256, bytes, and the filing's **`acceptanceDateTime`** from the submissions JSON. That field is AFC's knowledge time (§4.2) — the real version of the clock Day 41 synthesised.
  - **ADR-0004** (public-record rule) in the same commit.
- [ ] 60 min — 🛠️ DataVault: the README's *Orchestration* section + the DAG screenshot · journal

**Evening (8:00–10:00):** 60 min 📈 **twin catch-up block 2** (the queue should end empty; if it is already empty, add this hour to the adapter) · 60 min 📈 **AFC adapter tests** — recorded fixtures (two real Form 4 filings and their submissions JSON, saved once), no network in CI; one test asserts that `acceptanceDateTime` survives into the manifest unchanged · journal + commit (`feat(edgar): fair-access adapter with cache and provenance`)

### 📌 DAY 98 — Sunday, October 25 (2h) — 🏁 **FORTNIGHT REVIEW**
- [ ] 60 min — the review, in `weekly-summaries/week-13-14.md`:
```
1. AI-901: result · score by skill area · what the Foundry half taught
2. ⚖️ GUARDRAIL: AE/DE vs Applied AI hours for the fortnight (plan: 15.0 vs 14.0)
3. DATAVAULT S2: orchestration state vs the gate · next piece (Snowflake
   port? Docker/ECS?) — matches what the retro scheduled?
4. 📈 AFC: ADR-0005 result · adapter fixtures green? · Week-2 start date
5. 📈 TRADING THREAD — CLOSE THE EXCEPTION (C64): gap_report → sessions
   missed in Weeks 10–13 (falsifier: > 5 → it already stopped) · weekly
   totals ≤ ~29 h? · spike ADR drafted? → the exception LAPSES today;
   the snapshot job keeps running unattended; AB-620's extra-time study
   opens Week 15
6. 📈 TWIN QUEUE: empty? Anything still queued is dropped or re-planned,
   never carried silently
7. JOB LANE: applications n/25 · screens · which tier answered · did the
   Tier-3 application use the market-data artifacts?
8. WEEK 15+: what the retro already decided + what this review adds →
   input for the next plan (propose→approve)
```
- [ ] 60 min — 🚦 publish **post #14** — artifact: the `market_rehearsal` lineage graph and its test list (*"two clocks for one filing, and the test that catches the wrong one"*) · journal 🎉

> 📈 **Extra-time trading thread — Week 14 (~2 h · v3.3, C64): close it well.**
> - Run `gap_report.py` and write the count into Day 98's review.
> - **`market_rehearsal` README** in `learning_journey`: what it proves (knowledge time with two clocks, the inner-join trap, restatements replaced in a mart and appended in `signalcore.data`, SCD2 from vendor updates, OHLC integrity, AFC's label with an unfinished horizon left NULL), how to run it in three commands, and the line *"synthetic data only — no vendor rows"*.
> - Draft post #14 from it.

---

## 📊 2-WEEK SUCCESS METRICS

- [ ] 🎯 AI-901 taken (pass ≥ 700) · evidence file updated
- [ ] 3 practice assessments logged by skill area
- [ ] Airflow 101 done · orchestration ADR
- [ ] DAG v0 → hardened: idempotent re-run proven, retries, failure hook, integrity test in CI
- [ ] DataVault **v0.3.0** tagged
- [ ] Track B #6–#7 merged on the public 1099 repo
- [ ] Kimball Ch. 6 · dbt Advanced finished · CS50P +1 week

- [ ] 📈 AFC: ADR-0005 (spike) · EDGAR adapter + ADR-0004 · fixtures green, no network in CI
- [ ] 📈 Twin queue empty (or each leftover re-planned)
- [ ] 📈 Extra time: Crucible spike ADR draft · `market_rehearsal` README · exception closed Day 98
- [ ] 🚦 3 tailored applications (one Tier 3) · warm message · tracker n/25
- [ ] Posts #13–#14 · ⚖️ guardrail held (15.0 ≥ 14.0)

**Passing bar: 80%.** Non-negotiables: **the AI-901 attempt**, **the idempotent DAG** (the first S2 gate piece built after the soft trigger) and **the guardrail**.

---

## 🔭 WHAT COMES NEXT

**Week 15 onward is generated from the Month-3 retro plus Day 98's review**, propose→approve. What is already known:
- **AB-620's extra-time study opens in Week 15** (C42 committed it; C64 moved it here), self-funded ~$165. The exam date is set at Day 98, after the AI-901 result.
- **The CU Boulder bridge opens in November** (C44), inside the 25: the next plan names what pauses to make room.
- **DataVault S2** continues toward the gate: the Snowflake port when the retro schedules its trial, then Docker/ECS and monitoring.
- **AFC** continues at the build sheet's Week 2 (sampling frame, Form 4 parsers, the analyst schema) in the trading lane's Saturday blocks.
- The **Pro month + PolicyPulse judge gate** go in a later Q2 fortnight, inside Applied AI's share (C59).

---
*Aligned to Career Roadmap v10.0 (Corrections 1–64) · continues the v3.0–v3.3 twelve-week template (v3.3 trading lane expansion, C63–C64, 13 Oct 2026). Generated before the Month-3 retro at your request; the retro recalibrates it. This plan does not edit `roadmap.html`; propose→approve governance applies.*
