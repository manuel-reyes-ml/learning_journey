# 🏆 LLM Benchmark Comparison — November 2026 (v4.0)

> **Version:** 4.0 (November 18, 2026)
> **Supersedes:** `llm-benchmark-comparison--august-2026-v3_2.md` (August 17, 2026)
>
> 📝 **Changelog v4.0:** **The yardstick changed, not just the models.** Artificial Analysis replaced its composite with **Intelligence Index v5** on October 27 (60% private test sets), and three of v3.2's headline benchmarks are now saturated or archived (SWE-bench Verified, GPQA Diamond, AIME 2026). This version keeps v3.2's structure and its "every model keeps its row, missing scores show —" convention, but re-bases every ranking on the current benchmark set. + Claude Fable 5.2 / Opus 5.5 / Sonnet 5.5 / Haiku 5.5 · + GPT-6 family (Astra, Sol, Terra, Luna; 6.1 and 6.2) · + Gemini 4 (Argon, Carbon, Hydrogen) · + Kimi K3.1 Pro, Qwen4 Max, GLM-5.3, DeepSeek V4.1 Flash, MiniMax M3.1 Flash, MiMo-V2.6, Mistral Large 4, Muse Wonder / Ember · + FrontierCode 2.0 and HLE-Diamond sections · OpenCode Go table rebuilt from the live Console.
>
> 📝 **v3.2:** full open-weight rosters restored + local tier. **v3.1:** SWE-bench, GPQA, HLE, Arena added. **v3.0:** verification-status method.

---

## ⚠️ Read This First

Same commission as v3.2: *confirm every datum from trustworthy sources; assume nothing.*

**1. Every figure carries a verification marker.** Where sources disagree, the disagreement is shown rather than resolved by preference.

**2. Missing data shows as "—", not as a deleted row.** Many newly released models have not been run on older benchmarks, and several older benchmarks have stopped accepting new models. A "—" now often means *the benchmark retired*, not *the model is weak*.

**3. The AA Intelligence Index changed composition again — and this time the change is large.** v5.0.1 (launched October 27, 2026) combines nine evaluations in four equally weighted categories:

| Category (25% each) | Evaluations (weight) |
|:---|:---|
| Knowledge work | AA-Briefcase v1.1 (15%) · AutomationBench-AA (5%) · GDP.pdf (5%) |
| Coding | FrontierCode-AA 2.0 (15%) · Terminal-Bench 4.0 (10%) |
| Science | Terminal-Bench-Science 0.1 (15%) · CritPt v2 hard subset (10%) |
| General | AA-Omniscience v1.1 (15%) · HLE-Diamond (10%) |

**Removed since v3.2:** GDPval-AA, SciCode, AA-LCR, 𝜏³-Banking, GPQA Diamond, the original HLE, and Terminal-Bench v2.1. **60% of the index now uses private test sets or held-out answers.** Agentic evaluations are 55% of the weight but roughly 90% of output tokens. ✅ (AA methodology page + v5 launch article)

> 🔑 **No v5 score is comparable with any v4.x score in v3.2.** Opus 5 was 63 on v4.1.1; on v5 the leader of the whole field is 65. Do not chart v3.2 → v4.0 as a trend line.

| Marker | Meaning |
|:---:|:---|
| ✅ | **Primary source** — vendor pricing page / docs / announcement, or the evaluator's own leaderboard page |
| 🟡 | **Corroborated** — two or more independent trackers agree |
| ⚠️ | **Disputed, single-sourced, or vendor-reported** — range shown where known |
| — | **No published score** (or benchmark retired before the model shipped) |

> ⚠️ **Author disclosure:** compiled by Claude (Anthropic). An Anthropic model (Fable 5.2) leads several tables in this edition. Those rankings are cited to independent evaluators (Artificial Analysis, Cognition, Arena), and the places where Anthropic does **not** lead — Arena Text, cost per task, Terminal-Bench 4.0 on AA's harness — are shown with equal prominence.

---

## 📋 What Changed Since August 17, 2026

| Date | Release | Status |
|:---|:---|:---:|
| Aug 24 | **OpenCode Go drops the $5 first month** (changelog v1.18.22) | 🟡 |
| Aug 25–26 | **GLM-5.3 weights** (custom licence) · **GLM-5.3-Flash** (MIT, 320B / 18B active) | 🟡 |
| Aug 28 | **Terminal-Bench 4.0** — 66 tasks, 8-hour timeout, 5 trials per task | ✅ |
| Sep 1 | **Claude Fable 5.1 / Mythos 5.1** — $10/$50 | ✅ |
| Sep 1 | vals.ai **archives SWE-bench Verified and GPQA Diamond** as saturated | ✅ |
| Sep 3 | **GPT-6 Astra** — $10/$50, 1.05M context | 🟡 |
| Sep 10 | **DeepSeek V4.1 Flash** (MIT) replaces V4 Flash; peak/off-peak pricing | 🟡 |
| Sep 21 | **Grok 4.7** — xAI, $2/$6, 500K context | 🟡 |
| Sep 22 | **Claude Opus 5.5** — $4/$20 (first Opus price cut) · **Sonnet 5.5** $2/$10 | ✅ |
| Sep 22 | **GPT-6 Sol** ($2/$10) + **GPT-6 Luna** ($0.10/$0.50) · **HLE-Diamond** released | 🟡 |
| Sep 28 | **OpenCode Go Plus** — $40/mo | 🟡 |
| ~Sep 29 | **GPT-6.1 Sol** — $2/$10 | 🟡 |
| Oct 13 | **Gemini 4 Argon GA** — $2/$10 intro → $4/$20 from Dec 1 | 🟡 |
| Oct 19 | **MiniMax M3.1 Flash** | 🟡 |
| Oct 23 | **Kimi K3.1 Pro** — $2/$10; weights promised by Nov 4, custom licence | 🟡 |
| Oct 26 | **GPT-6.1 Terra** — $1/$5 | 🟡 |
| Oct 27 | **AA Intelligence Index v5** — 60% private | ✅ |
| Oct | **Mistral Large 4** — open weights, Mistral Ecosystem licence *(sources give Oct 6, Oct 29 and Nov 5)* | ⚠️ |
| Oct–Nov | **Meta Muse Wonder / Muse Ember / Muse Spark Open** | ⚠️ |
| Nov 9 | **Claude Fable 5.2 / Mythos 5.2** — $8/$40 (−20%) | ✅ |
| Nov 10–12 | **Gemini 4 Carbon** ($2/$10 intro) · **Gemini 4 Hydrogen** ($1.50/$7.50) | 🟡 |
| Nov 14 | **AA Coding Agent Index v2.1** — FrontierCode 2.0 + Terminal-Bench 4.1 | 🟡 |
| Nov 16 | **Qwen4 Max** — $1.50/$4.50, **closed weights** | ✅ |
| Nov 17 | **GPT-6.2 Astra** ($8/$40) + **GPT-6.2 Sol** ($2/$10) | ✅ |

**Structural shift #1 — the open-weight gap widened, by measurement.** On v4.3 the best open model trailed the leader by ~3 points. On v5's launch day the best announced-open model (Kimi K3.1 Pro, weights then unreleased) trailed by 12, and the best *released*-weights models (DeepSeek V4.1 Flash, GLM-5.3, both 32) trailed by 26. ✅ (AA v5 article). With Fable 5.2 now at 65, Kimi K3.1 Pro sits 19 points back. A rank change after a methodology change is **not** evidence that any model got worse — it is evidence that public-benchmark scores were flattering some models.

**Structural shift #2 — the classic benchmarks retired.** SWE-bench Verified and GPQA Diamond were archived by vals.ai as saturated; AIME 2026 sits at 100% on MathArena; SWE-bench Pro's public split was audited as ~30% broken. The live frontier is now FrontierCode 2.0, Terminal-Bench 4.0, HLE-Diamond and Terminal-Bench-Science.

**Structural shift #3 — price compression at the top.** Fable 5.2 ($8/$40), GPT-6.2 Astra ($8/$40) and Opus 5.5 ($4/$20) are all cheaper than their predecessors. But **effort setting now moves the bill more than list price**: Fable 5.2 costs $26.54 per AA index task at max and $9.08 at high, for 3 points. 🟡

---

## 🚨 THE CENTRAL FINDING — Still Not Comparable Across Sources

Terminal-Bench 4.0, the same benchmark version, checked within weeks:

| Source | Harness | Reported leader & score |
|:---|:---|:---|
| Artificial Analysis | AA's own run | Kimi K3.1 Pro **67.2%**, Gemini 4 Carbon 65.2%, Claude Sonnet 5.5 63.6% |
| tbench.ai official board (Oct 17) | Each lab's agent | Claude Opus 5.5 **64.8% ± 3.1** |
| Anthropic (vendor) | Claude Code | Claude Opus 5.5 66.4% |
| Moonshot (vendor table) | Kimi harness | Kimi K3.1 Pro 65.7% · GPT-6 Astra 58.2% · DeepSeek V4.1 Flash 42.3% |
| Pricing aggregator (Nov 3) | mixed | Claude Sonnet 5.5 70.6% |

**One version, one month, 63.6% → 70.6% for the same Sonnet 5.5 depending on who ran it.** Four documented mechanisms, three of them new since v3.2:

**Version churn.** Terminal-Bench shipped 2.1 (May, 89 tasks) → 3.0 (July 30, 74 tasks) → 4.0 (Aug 28, 66 tasks) → 4.1 (inside AA's Coding Agent Index, Nov 14). Top scores by version were 83.4% → 34.4% → 51.8% at each launch. None of those numbers describe the same test. 🟡

**Methodology churn.** The same models scored materially differently on AA v4.x and v5: GLM-5.3 shows 45 on a v4 snapshot and 32 on v5; DeepSeek V4.1 Flash 39 vs 32. 🟡

**Effort non-monotonicity.** On AA's Coding Agent Index v2.1, Fable 5.2 at **high** scores 58 ($7.51/task) and at **max** scores 56 ($44.22/task) — max effort blew scope and time limits. "Max" is not "best." 🟡

**Fallback accounting (carried over).** AA lists Fable 5.2 as "Max, **Default Fallback**" — some refusal-flagged requests route to a fallback model. Treat Fable 5.2 entries as configuration results, not clean single-model results. ⚠️

> 🔑 **Do not select a model on a leaderboard delta under ~5 points**, or on any delta between two different effort settings without cost per task beside it. Run 30–50 representative cases from your own work.

---

# 1️⃣ Composite Intelligence — AA Intelligence Index v5.0.1

| Rank | Model (effort) | Creator | Score | Type | Status |
|:---:|:---|:---|:---:|:---:|:---:|
| 1 | **Claude Fable 5.2** (max) ⚡ † | Anthropic | **65** | Paid | ✅ |
| 2 | **GPT-6.2 Astra** (max) ⚡ | OpenAI | **62** | Paid | 🟡 |
| 2= | Claude Fable 5.2 (xhigh / high) ⚡ | Anthropic | 62 | Paid | 🟡 |
| 4 | **Gemini 4 Carbon** (high) ⚡ | Google | **60** | Paid | ✅ |
| 5 | **Claude Opus 5.5** (max) ⚡ | Anthropic | 59 | Paid | 🟡 *(58 at v5 launch)* |
| 6 | **GPT-6.2 Sol** (max) ⚡ | OpenAI | 57 | Paid | ✅ |
| 6= | GPT-6 Astra (max) ⚡ | OpenAI | 57 | Paid | ✅ |
| 8 | GPT-6.1 Sol (max) ⚡ | OpenAI | 55 | Paid | ✅ |
| 8= | Claude Sonnet 5.5 (max) ⚡ | Anthropic | 55 | Paid | 🟡 *(54.5)* |
| — | Gemini 4 Hydrogen (xhigh) ⚡ | Google | 54 | Paid | ⚠️ *(single tracker)* |
| — | GPT-6.1 Terra (max) ⚡ | OpenAI | 51 | Paid | 🟡 |
| — | Gemini 4 Argon (high) ⚡ | Google | 50 | Paid | ✅ |
| — | Muse Wonder (max) ⚡ | Meta | 50 / 43.6 | Paid | ⚠️ *(trackers conflict; "Full" vs base config)* |
| — | Claude Fable 5.1 (max) ⚡ | Anthropic | 49 | Paid | 🟡 |
| — | **Kimi K3.1 Pro** ⚡ ★ | Moonshot | **46** | **Open (custom)** | ✅ |
| — | Qwen4 Max ⚡ | Alibaba | 43 | Paid *(closed weights)* | 🟡 |
| — | Claude Haiku 5.5 (max) ⚡ | Anthropic | 36 | Paid | ✅ |
| — | Muse Ember (max) ⚡ | Meta | 36 | Paid | ✅ |
| — | Grok 4.7 (xhigh) ⚡ | xAI | 35.5 | Paid | ⚠️ |
| — | **DeepSeek V4.1 Flash 1017** (max) ⚡ ★ | DeepSeek | **32** | **Open (MIT)** | ✅ |
| — | **GLM-5.3** (max) ⚡ ★ | Z.ai | **32** | **Open (custom)** | ✅ |
| — | MiMo-V2.6-Pro ⚡ ★ | Xiaomi | 30 | Open | ⚠️ |
| — | MiniMax M3.1 Flash ⚡ | MiniMax | 29 | Restricted | ⚠️ |
| — | GLM-5.3-Flash ⚡ ★ | Z.ai | 28 | Open (MIT) | ⚠️ |
| — | GPT-6 Luna (max) ⚡ | OpenAI | 28 | Paid | ⚠️ |
| — | DeepSeek V4 Pro 0813 (max) ⚡ ★ | DeepSeek | 23 | Open (MIT) | ⚠️ |
| — | Qwen3.8-27B (xhigh) ⚡ ★ | Alibaba | 20 | Open / local | ⚠️ |
| — | MiniMax M3 ⚡ ★ | MiniMax | 19 | Open (community) | ⚠️ |
| — | GLM-5.2 ⚡ ★ | Z.ai | — *(no v5 row found)* | Open (MIT) | — |
| — | Kimi K3 ⚡ ★ | Moonshot | — *(no v5 row found)* | Open (custom) | — |
| — | Claude Mythos 5.2 ⚡ | Anthropic | — *(same model as Fable 5.2, vetted access)* | Paid | — |

> † Fable 5.2 leads five of the nine evaluations: HLE-Diamond 80% (prev. best 69%), AA-Omniscience 67 (54), Terminal-Bench-Science 73% (65%), CritPt v2 77% (72%), FrontierCode 2.0 49% (46%). It does **not** lead AA-Briefcase (1785 Elo, inside the interval of Opus 5.5 at 1800 and behind Sonnet 5.5 at 1813). 🟡
>
> ⚠️ Rows marked ⚠️ come from secondary trackers mirroring AA snapshots taken on different days (Nov 3–17). Treat ordering below rank 10 as indicative.

### Cost per AA index task — the column that changes the decision

| Model (effort) | Score | Cost / task | Status |
|:---|:---:|:---:|:---:|
| Claude Fable 5.2 (max) | 65 | **$26.54** | 🟡 |
| Claude Fable 5.2 (high) | 62 | $9.08 | 🟡 |
| Claude Opus 5.5 (max) | 58–59 | $10.04 | ✅ |
| Gemini 4 Carbon (high) | 60 | $7.76 | 🟡 |
| GPT-6.2 Astra (max) | 62 | **$4.00** | 🟡 |
| Qwen4 Max | 43 | $3.27 | 🟡 |
| GPT-6.1 Sol (max) | 55 | $1.27 | ✅ |
| **GPT-6.2 Sol (max)** | **57** | **$1.01** | 🟡 |
| GPT-6.1 Terra (max) | 51 | $0.96 | ✅ |

> 🔑 **GPT-6.2 Sol reaches GPT-6 Astra's score at ~15% of its cost per task.** Fable 5.2 also used ~275M output tokens across the index vs ~54M for GPT-6 Astra. The leader and the value leader are different models. 🟡

**AA Coding Agent Index v2.1** (Nov 14, model + agent harness): Fable 5.2 (high/xhigh) and Opus 5.5 (max) tie at **58**; Fable 5.2 max 56; GPT-6.1 Sol max in Codex 52 at $1.51/task. Average scores fell ~5 points from v2.0 because of FrontierCode 2.0's harder grading. 🟡

---

# 2️⃣ Coding — Terminal-Bench 4.0 + FrontierCode 2.0

> Terminal-Bench 4.0: 66 containerized professional tasks; 8 removed and ~19 fixed vs 3.0; flat 8-hour agent timeout; 5 trials per task with 95% CI. **Not comparable with 2.x or 3.0.** ✅ (tbench.ai)

### Terminal-Bench 4.0

| Model | Creator | Score | Type | Status |
|:---|:---|:---:|:---:|:---:|
| **Kimi K3.1 Pro** ⚡ ★ | Moonshot | **67.2%** (AA) / 65.7% (vendor) | **Open** | ⚠️ |
| **Claude Opus 5.5** ⚡ | Anthropic | 66.4% (vendor) / **64.8% ± 3.1** (tbench official) | Paid | 🟡 |
| **Gemini 4 Carbon** (high) ⚡ | Google | 65.2% (AA) | Paid | ✅ |
| **Claude Sonnet 5.5** (max) ⚡ | Anthropic | 63.6% (AA) / 70.6% (aggregator) | Paid | ⚠️ |
| GPT-6 Astra ⚡ | OpenAI | 57.9% (vendor) / 58.2% (Moonshot table) | Paid | ⚠️ |
| Claude Opus 5 (max) ⚡ | Anthropic | 51.8% (tbench, Aug 29 launch board) | Paid | ✅ |
| DeepSeek V4.1 Flash ⚡ ★ | DeepSeek | 42.3% (Moonshot table) / ~31% (tracker) | Open | ⚠️ |
| Grok 4.7 (xhigh, Grok Build) ⚡ | xAI | 38.0% | Paid | ⚠️ |
| GLM-5.3 ⚡ ★ | Z.ai | ~38% | Open | ⚠️ |
| Kimi K3 ⚡ ★ | Moonshot | ~13% (AA) | Open | ⚠️ |
| Claude Fable 5.2 ⚡ | Anthropic | — | Paid | — |
| GPT-6.2 Astra / Sol ⚡ | OpenAI | — | Paid | — |
| Qwen4 Max ⚡ | Alibaba | — | Paid | — |
| GLM-5.2 ⚡ ★ | Z.ai | — | Open | — |
| MiniMax M3 / M3.1 Flash ⚡ | MiniMax | — | Open / restricted | — |

> 🔑 **An open-weight model tops Terminal-Bench 4.0 on AA's harness** (Kimi K3.1 Pro, up from ~13% for Kimi K3) while the same model sits 19 points behind on the composite. Terminal tasks and mergeable-code tasks are now measuring different things.

### FrontierCode 2.0 (Cognition) — the new "real code" benchmark

> 132 private tasks built by open-source maintainers from their own repositories; graded on whether a maintainer would **merge** the change, with blocking criteria that zero a task. ✅ (Cognition)

| Model | Creator | Score (Cognition board) | Status |
|:---|:---|:---:|:---:|
| **Claude Fable 5.2** (xhigh) ⚡ | Anthropic | **49.1%** | ✅ |
| Claude Opus 5.5 ⚡ | Anthropic | 45.5% | ✅ |
| GPT-6.2 Astra ⚡ | OpenAI | ~44% (vendor) | ⚠️ |
| GPT-6.2 Sol ⚡ | OpenAI | 43.8% (vendor, $1.29/task) | ⚠️ |
| GPT-6 Astra ⚡ | OpenAI | 42.8% | ✅ |
| Open-weight models ★ | — | — *(not on the published top 10)* | — |

> ⚠️ AA runs FrontierCode under its own harness for the Intelligence Index, so AA's FrontierCode-AA figures differ from Cognition's board. Quote which one.

---

# 3️⃣ SWE-bench Verified — 🪦 Saturated and archived

> vals.ai archived SWE-bench Verified on **September 1, 2026**. Most models released since have no Verified score, and the labs have stopped reporting it. The table below is the **final** independent state, kept for continuity. The top cluster is narrower than the ±2–3 point scaffold noise.

## 💼 Paid / Closed

| Model | Creator | Score | Input $/1M | Output $/1M | Status |
|:---|:---|:---:|:---:|:---:|:---:|
| Claude Opus 5 ⚡ | Anthropic | **97.0%** (vals, final board) | $5.00 | $25.00 | ✅ |
| GPT-5.6 Sol ⚡ | OpenAI | 96.2% (vals) | $4.00 *(promo)* | $20.00 | ✅ |
| Claude Fable 5 ⚡ | Anthropic | 95.0% | $10.00 | $50.00 | 🟡 |
| Claude Fable 5.2 ⚡ | Anthropic | — | $8.00 | $40.00 | — |
| Claude Opus 5.5 ⚡ | Anthropic | — | $4.00 | $20.00 | — |
| Claude Sonnet 5.5 ⚡ | Anthropic | — | $2.00 | $10.00 | — |
| Claude Haiku 5.5 ⚡ | Anthropic | — | $0.10 | $0.50 | — |
| GPT-6.2 Astra ⚡ | OpenAI | — | $8.00 | $40.00 | — |
| GPT-6.2 Sol ⚡ | OpenAI | — | $2.00 | $10.00 | — |
| GPT-6.1 Terra ⚡ | OpenAI | — | $1.00 | $5.00 | — |
| GPT-6 Luna ⚡ | OpenAI | — | $0.10 | $0.50 | — |
| Gemini 4 Carbon / Argon ⚡ | Google | — | $2.00 → $4.00 | $10.00 → $20.00 | — |
| Gemini 4 Hydrogen ⚡ | Google | — | $1.50 | $7.50 | — |
| Grok 4.7 ⚡ | xAI | — | $2.00 | $6.00 | — |
| Qwen4 Max ⚡ | Alibaba | — | $1.50 | $4.50 | — |

## 🆓 Free / Open Weights

| Model | Creator | Score | Input $/1M | Output $/1M | Licence | Status |
|:---|:---|:---:|:---:|:---:|:---|:---:|
| **DeepSeek V4 Pro 0813** ⚡ ★ | DeepSeek | **96.4%** (vals, $0.10/test) | $0.66–1.32 | $1.98–3.96 | MIT | ✅ |
| **Kimi K3** ⚡ ★ | Moonshot | 93.4% (vals) | ~$2.50 | ~$14.00 | Custom | ⚠️ |
| Qwen3.8 Max ⚡ ★ | Alibaba | 85.6% (vals) | $2.00 | $6.00 | Custom | ✅ |
| GLM-5.2 ⚡ ★ | Z.ai | 82.8% (vals) | $1.40 | $4.40 | MIT | ✅ |
| MiniMax M3 ⚡ ★ | MiniMax | 80.5% | $0.30 | $1.20 | Community | 🟡 |
| Kimi K3.1 Pro ⚡ ★ | Moonshot | — | $2.00 | $10.00 | Custom | — |
| DeepSeek V4.1 Flash ⚡ ★ | DeepSeek | — | $0.15–0.30 | $0.60–1.20 | MIT | — |
| GLM-5.3 / GLM-5.3-Flash ⚡ ★ | Z.ai | — | $1.40 / $0.15 | $4.40 / $0.50 | Custom / MIT | — |
| MiniMax M3.1 Flash ⚡ | MiniMax | — | $0.15 | $0.60 | Restricted | — |
| MiMo-V2.6-Pro / Flash ⚡ ★ | Xiaomi | — | — | $0.87 / $0.28 | Open | ⚠️ |
| Mistral Large 4 ★ | Mistral | — | $1.36 *(50% promo $0.68)* | $4.18 *($2.09)* | Mistral Ecosystem | 🟡 |
| Qwen3.8-27B ⚡ ★ | Alibaba | — | local | local | Apache 2.0 | — |
| Gemma 4 ⚡ ★ | Google | — | local | local | Apache 2.0 | — |
| gpt-oss-20b / 120b ★ | OpenAI | — | local / ~$0.60 out | — | Apache 2.0 | — |

> 🔑 **The last independent Verified board has an open MIT model in second place at $0.10 per test** (DeepSeek V4 Pro 0813, 96.4%) — a result the benchmark could no longer separate from the 97% leader.

---

# 4️⃣ SWE-bench Pro — ⚠️ Now carries an audit warning

**The new fact:** on July 8, 2026, OpenAI published a task-level audit of the 731-task public split concluding that **roughly 30% of tasks are broken**, and withdrew its earlier recommendation to treat Pro as the leading coding eval. Scale also changed the harness (older runs: capped cost, 50 turns; current: uncapped, 250 turns). ⚠️

| Harness | Leader | Score |
|:---|:---|:---:|
| Vendor aggregate (llm-stats, 59 models) | **Claude Opus 5.5** | **89.9%** |
| **Scale SEAL standardized public set** (Sep 14) | **Muse Spark 1.1** | **61.5%** (± 3.1) |
| Scale standardized public set | GPT-5.4 (xHigh) | 59.1% (± 3.6, shares rank 1) |
| Scale private commercial set | Muse Spark 1.1 | 51.5% |

**Open weights (vendor aggregate):** Hy4 preview 65.7% · Qwen3.8-Flash-Next 62.5% · GLM-5.2 62.1% · Qwen3.8-27B 61.7%. ⚠️

**Not on either Scale board:** Claude Opus 5, Fable 5.1, GPT-6 Astra, GLM-5.3, Kimi K3 — the newest frontier models mostly don't submit. 🟡

> 🔑 When someone quotes a Pro number, ask **which harness and which date**. Before July and after July are different measurements.

---

# 5️⃣ GPQA Diamond — 🪦 Saturated

> 198 expert-written graduate science questions. vals.ai archived it on September 1, 2026 (24 of 136 models above 90%); AA dropped it from the v5 index.

| Model | Creator | Score | Type | Status |
|:---|:---|:---:|:---:|:---:|
| **Gemini 4 Argon** ⚡ | Google | **96.5%** (provider-endpoint tracker, Nov 5) | Paid | ⚠️ |
| **GPT-6 Astra** ⚡ | OpenAI | 95.8% | Paid | ⚠️ |
| Gemini 3.1 Pro Preview ⚡ | Google | 95.45% (vals final) | Paid | ✅ |
| GPT-5.6 Sol ⚡ | OpenAI | 95.20% (vals final) | Paid | ✅ |
| Grok 4.6 ⚡ | xAI | 94.70% (vals final) | Paid | ✅ |
| Claude Mythos 5 ⚡ | Anthropic | 94.6% | Paid | 🟡 |
| GPT-6 Sol ⚡ | OpenAI | 94.3% | Paid | ⚠️ |
| **Kimi K3** ⚡ ★ | Moonshot | **93.5** | **Open** | 🟡 |
| GLM-5.2 ⚡ ★ | Z.ai | 91.2 | Open | 🟡 |
| Qwen3.6-27B ⚡ ★ | Alibaba | 87.8 | Open / local | ⚠️ |
| Claude Fable 5.2 / Opus 5.5 ⚡ | Anthropic | — | Paid | — |
| Gemini 4 Carbon ⚡ | Google | — | Paid | — |
| Kimi K3.1 Pro / Qwen4 Max / GLM-5.3 ⚡ | — | — | — | — |

> ⚠️ vals.ai noted that a published Claude Fable 5 GPQA figure counted refusal-triggered fallbacks as successes; scored as failures, it falls sharply. Fallback accounting matters here too.
>
> 🔑 **The top seven sit inside ~2 points. Use GPQA only as a floor check, not a ranking.**

---

# 6️⃣ HLE → HLE-Diamond

> **HLE-Diamond** (released Sep 22, 2026) is a cleaned, 1,000-question subset of Humanity's Last Exam — 500 reasoning + 500 knowledge — built by CAIS and Scale AI after a year of fixing the answer key. It is the direct response to v3.2's validity warning (FutureHouse's finding that ~30% of chemistry/biology answers could be wrong). AA replaced the original HLE with it in v5. ✅

### HLE-Diamond (AA, no tools)

| Model (effort) | Creator | Score | Type | Status |
|:---|:---|:---:|:---:|:---:|
| **Claude Fable 5.2** (max) ⚡ | Anthropic | **80%** | Paid | 🟡 |
| Gemini 4 Carbon ⚡ | Google | 69.1% | Paid | 🟡 |
| Claude Opus 5.5 (max) ⚡ | Anthropic | 67.9% | Paid | 🟡 |
| GPT-6 Astra (max) ⚡ | OpenAI | ~64% | Paid | ⚠️ |
| GPT-6.2 Astra ⚡ | OpenAI | — *(AA: second only to Fable 5.2)* | Paid | ⚠️ |
| Released open-weight models ★ | — | well behind *(AA)* | Open | ⚠️ |

The largest gain is on the **knowledge** half: Fable 5.2 75% vs Gemini 4 Carbon 59%. 🟡

### Original HLE — other boards (protocols differ)

| Board | Leader | Score | Status |
|:---|:---|:---:|:---:|
| Scale's HLE board (Sep 29) | GPT-6 Astra | 60.6% | ⚠️ |
| Vendor-reported (BenchLM, Nov 12) | Claude Fable 5.2 | 74.2% · Kimi K3.1 Pro 70% · Fable 5.1 65% | ⚠️ |
| AA (Sep 1, v4.1.1) | Claude Fable 5.1 (max) | 59.1% | ✅ |

> 🔑 **Tool use, effort and the question set each move HLE by 10–20 points.** Quote HLE-Diamond, no tools, with effort level — or don't quote it.

---

# 7️⃣ AIME 2026 (Math) — ✅ Verified, and saturated

v3.2 could not reproduce any AIME 2026 table. It can now be verified — and it no longer discriminates:

| Source | Leader | Score | Status |
|:---|:---|:---:|:---:|
| **MathArena** (4 runs × 30 problems, Oct 17) | **GPT-5.5 (xhigh)** and **Claude Opus 4.8 (max)**, tied | **100.00%** | ✅ |
| llm-stats (self-reported, 12 models) | Kimi K2.6 | 96.4% | ⚠️ |
| BenchLM (July) | GLM-5.2 | 99.2% | ⚠️ |

MathArena now lists final-answer competitions as **deprecated**. 🟡 v2's AIME 2026 table remains suspect; the open question from v3.2 is closed as "saturated." Harder successors (FrontierMath v2, HMMT Feb 2026, USAMO 2026) are where math separation now lives. ⚠️

---

# 8️⃣ Arena (Human Preference)

| Board (snapshot) | Leader | Score | Status |
|:---|:---|:---:|:---:|
| **Text** (Nov 11) | **Gemini 4 Carbon (High)** | **1526 ± 10** *(preliminary, ~4.3k votes)* | ✅ |
| Text #2 | Gemini 4 Argon (High) | 1522 ± 5 | ✅ |
| Text #3 | Muse Wonder (Max) | 1511 ± 6 | ✅ |
| Text #4 | Claude Opus 5.5 (High) | 1507 ± 6 | ✅ |
| Text #5–7 | Fable 5 (High) 1504 · Opus 4.6 (High) 1503 · Fable 5.1 (Max) 1502 | — | ✅ |
| **Coding (text sub-board)** (Nov 11) | Gemini 4 Carbon (High) | 1568 ± 19 | ✅ |
| **Agent Arena** (Nov 11) | **Claude Fable 5.2 (Max)** | 30.5% net improvement · Opus 5.5 19.5% · Gemini 4 Carbon 16.9% · GPT-6.1 Sol 12.4% | ✅ |
| **WebDev** | Claude Fable 5.2 (xHigh) | #1 | ✅ |
| **Best open-weight (Text)** | Kimi K3.1 Pro | ~1488 | ⚠️ |

> ⚠️ Fable 5.2 has no settled Text Arena rating yet. The Text top seven sit inside **24 points** — inside the 30-Elo band where rank swaps within a quarter are common. **Agent Arena is the board that separates models today**, and it also shows cost: ~$8.69/task for Fable 5.2 vs ~$1.36 for Gemini 4 Carbon and ~$1.02 for GPT-6.1 Sol.

---

# 9️⃣ Local / Self-Hostable Tier

### ⚠️ "Open weights" ≠ runnable — even more so now

The open frontier got bigger: Kimi K3.1 Pro is 3T-class, Qwen3.8-Flash-Next needs ~120 GB at Q4, Mistral Large 4 is ~1.06 TB at bf16. Below them the practical local tier is still ~8B–30B. 🟡

### Actually runnable, by hardware (Nov 2026)

| Model | Footprint (Ollama tag) | Context | Evidence | Status |
|:---|:---:|:---:|:---|:---:|
| **Qwen3.8-27B** ★ | ~18 GB | 256K | Best local coder for 24 GB / 32 GB Mac; AA v5 20; vendor: beats Opus 4.6 Max on SWE-bench Pro | 🟡 |
| **Muse Glimmer-30B** ★ (Meta, dense) | ~18 GB | — | Runner-up at 24–32 GB; tools + image input | ⚠️ |
| Qwen3-Coder-30B-A3B ★ | ~18 GB | 256K | Coding specialist; MoE speed | 🟡 |
| **Gemma 4 26B-A4B** ★ | ~16 GB | 256K | Workstation MoE | 🟡 |
| **gpt-oss-20b** ★ | ~16 GB | — | 16 GB default pick | 🟡 |
| **Gemma 4 12B** ★ | ~7.7 GB | 256K | Best 16 GB pick when tool calling matters | 🟡 |
| Granite 4.2 8B ★ | ~5 GB | 131K | 8 GB tier | ⚠️ |
| Qwen 3.5 9B ★ | <10 GB | — | **Still no published benchmarks** | — |
| Qwen3.6-27B ★ | ~17 GB | 262K | v3.2's pick; superseded by Qwen3.8-27B | 🟡 |

> ⚠️ **Ollama's default context window is 4K tokens** on machines under its 24 GB line. Raise it before judging any local model in an agent — a 4K agent session is a crippled test. 🟡
>
> ⚠️ **Ollama `:cloud` tags** still exist alongside local tags for several models — pulling one does not give local inference.

**Licences (Nov 2026):** MIT — DeepSeek V4.1 Flash, GLM-5.3-Flash, GLM-5.2 · Apache 2.0 — Gemma 4, Qwen3.8-27B, gpt-oss · Custom / revenue-gated — Kimi K3 / K3.1 Pro, GLM-5.3, Qwen3.8-2.4T · Mistral Ecosystem licence (not Apache, not MIT) — Mistral Large 4 · Closed — Qwen4 Max, all Muse models except gated Muse Spark Open. 🟡

---

# 💰 Complete Pricing Table

### Anthropic — ✅ PRIMARY (platform.claude.com/docs pricing, read Nov 18, 2026)

| Model | Input | 5m Cache Write | 1h Cache Write | Cache Hit | Output |
|:---|:---:|:---:|:---:|:---:|:---:|
| **Claude Fable 5.2** | **$8** | $10 | $16 | $0.20 | **$40** |
| Claude Mythos 5.2 *(vetted access)* | $8 | $10 | $16 | $0.20 | $40 |
| Claude Fable 5.1 / Mythos 5.1 | $10 | $12.50 | $20 | $0.25 | $50 |
| Claude Fable 5 / Mythos 5 | $10 | $12.50 | $20 | $1.00 | $50 |
| **Claude Opus 5.5** | **$4** | $5 | $8 | $0.20 | **$20** |
| Claude Opus 5 / 4.8 / 4.7 / 4.6 / 4.5 | $5 | $6.25 | $10 | $0.50 | $25 |
| **Claude Sonnet 5.5** | **$2** | $2.50 | $4 | **$0.10** | **$10** |
| Claude Sonnet 5 | $2 | $2.50 | $4 | $0.20 | $10 |
| Claude Sonnet 4.6 / 4.5 | $3 | $3.75 | $6 | $0.30 | $15 |
| **Claude Haiku 5.5** (prompt ≤100K) | **$0.10** | $0.125 | $0.20 | $0.01 | **$0.50** |
| Claude Haiku 5.5 (prompt >100K) | $0.50 | $0.625 | $1 | $0.05 | $2.50 |
| Claude Haiku 4.5 | $1 | $1.25 | $2 | $0.10 | $5 |

**Mechanics:** Batch −50% (Fable 5.2 $4/$20, Opus 5.5 $2/$10). Cache hits 0.1× input for most models, **0.05×** for Opus 5.5 / Sonnet 5.5, **0.025×** for Fable / Mythos 5.x. Fast mode (up to 2.5× output speed) Fable 5.2 $16/$80, Opus 5.5 $8/$40 — not with Batch. `inference_geo: "us"` 1.1×. Full 1M context at standard price for Claude 4.6+ **except Haiku 5.5**, which bills the whole request at the higher tier once the prompt passes 100K. ✅

**🔑 Tokenizer caveat (unchanged):** Claude 4.7 and later use a tokenizer that produces ~30% more tokens for the same text. ✅ Every cross-vendor per-token comparison below understates the Claude bill by roughly that much.

### OpenAI

| Model | Input | Cached | Output | Note | Status |
|:---|:---:|:---:|:---:|:---|:---:|
| **GPT-6.2 Astra** | **$8** | $0.40 | **$40** | Nov 17; −20% vs GPT-6 Astra | ✅ |
| GPT-6 Astra | $10 | $1.00 | $50 | Sep 3 | 🟡 |
| **GPT-6.2 Sol** | **$2** | $0.10 | **$10** | Nov 17; same as 6.1 Sol | ✅ |
| GPT-6.1 Sol / GPT-6 Sol | $2 | $0.10 / $0.20 | $10 | | 🟡 |
| **GPT-6.1 Terra** | **$1** | $0.05 | **$5** | Oct 26 | 🟡 |
| **GPT-6 Luna** | **$0.10** | — | **$0.50** | Sep 22 | 🟡 |
| GPT-5.6 Sol | $4 | $0.40 | $20 | promo "at least through Nov 21, 2026" | 🟡 |

Batch / Flex −50%; Fast 2×; prompts over 272K input tokens bill at a higher long-context rate. 🟡

### Google

| Model | Input | Output | Note | Status |
|:---|:---:|:---:|:---|:---:|
| **Gemini 4 Carbon** | **$2 → $4** | **$10 → $20** | Intro price ends **Nov 30**; $4/$20 from **Dec 1**; thinking tokens bill as output | 🟡 |
| **Gemini 4 Argon** | $2 → $4 | $10 → $20 | Same schedule | 🟡 |
| **Gemini 4 Hydrogen** | **$1.50** | **$7.50** | Flat across 1M context; free tier | 🟡 |
| Gemini 3.7 Flash | $0.75 | $3.75 | v3.2 figure; scheduled to double Jan 1, 2027 — not re-verified | ⚠️ |
| Gemini 3.5 Flash-Lite | $0.30 | $2.50 | v3.2 figure | ⚠️ |

### xAI · Meta · Alibaba (closed)

| Model | Input | Output | Status |
|:---|:---:|:---:|:---:|
| Grok 4.7 | $2.00 | $6.00 (500K ctx) | 🟡 |
| Muse Wonder (Meta) | $4.00 | $20.00 | ⚠️ |
| Muse Ember (Meta) | — | $0.50 | ⚠️ |
| **Qwen4 Max** (Alibaba, closed weights) | **$1.50** | **$4.50** | ✅ |

### Open weights (hosted API rates)

| Model | Creator | Input | Output | Params / Context | Licence | Status |
|:---|:---|:---:|:---:|:---|:---|:---:|
| **Kimi K3.1 Pro** ★ | Moonshot | $2.00 | $10.00 | 3T-class / 1M | Custom | 🟡 |
| GLM-5.3 ★ | Z.ai | $1.40 | $4.40 | — / 1M | Custom | 🟡 |
| Mistral Large 4 ★ | Mistral | $1.36 *(promo $0.68)* | $4.18 *(promo $2.09)* | 1.05T / 52B active | Mistral Ecosystem | 🟡 |
| DeepSeek V4 Pro 0813 ★ | DeepSeek | $0.66 off-peak / $1.32 peak | $1.98 / $3.96 | 1.6T / 49B active / 1M | MIT | 🟡 |
| MiMo-V2.6-Pro ★ | Xiaomi | — | $0.87 | — / 1M | Open | ⚠️ |
| MiniMax M3 ★ | MiniMax | $0.30 | $1.20 | — / 1M | Community | 🟡 |
| **DeepSeek V4.1 Flash** ★ | DeepSeek | **$0.15 off-peak / $0.30 peak** | **$0.60 / $1.20** | — / 1M | **MIT** | 🟡 |
| MiniMax M3.1 Flash | MiniMax | $0.15 | $0.60 | — / 1M | Restricted | 🟡 |
| **GLM-5.3-Flash** ★ | Z.ai | **$0.15** | **$0.50** | 320B / 18B active / 1M | **MIT** | 🟡 |
| Gemma 4 · Qwen3.8-27B · gpt-oss-20b ★ | various | free (local) | free | 12–30B | Apache 2.0 | 🟡 |

DeepSeek peak hours: 01:00–04:00 and 06:00–10:00 UTC, Monday–Friday; peak = 2× off-peak. V4 Flash ($0.14/$0.28) is **retired** — its names now route to V4.1 Flash. 🟡

---

# 📉 Corrections to the August 2026 (v3.2) Report

| # | v3.2 claim | November 2026 status |
|:---:|:---|:---|
| 1 | AA Intelligence Index v4.1.1 as composite | ✅ **Replaced by v5.0.1** (Oct 27); no v4 → v5 comparison is valid |
| 2 | "The open tier reached the frontier" (Kimi K3 #3) | ✅ **Reversed under v5** — best released-weights model 26 pts behind at launch; Kimi K3.1 Pro 19 behind today |
| 3 | Terminal-Bench v2.1 as headline coding measure | 🟡 Superseded by **3.0 (Jul 30) → 4.0 (Aug 28) → 4.1** |
| 4 | SWE-bench Verified table | ✅ **Archived as saturated** (vals.ai, Sep 1) |
| 5 | SWE-bench Pro "four competing scores" | ⚠️ Still true, plus **OpenAI's audit: ~30% of public tasks broken** |
| 6 | GPQA Diamond as reasoning signal | ✅ **Saturated**; archived by vals.ai; dropped from AA v5 |
| 7 | HLE with a validity warning | ✅ **Replaced by HLE-Diamond** — the cleaned answer key |
| 8 | AIME 2026 "could not be reproduced" | ✅ **Verified on MathArena — and saturated at 100%** |
| 9 | Claude Opus 5 at $5/$25 as Opus tier | ✅ **Opus 5.5 at $4/$20** (Sep 22) |
| 10 | Claude Fable 5 at $10/$50 as top tier | ✅ **Fable 5.2 at $8/$40** (Nov 9) |
| 11 | GPT-5.6 Sol as OpenAI flagship | ✅ **GPT-6.2 Astra** (Nov 17); Sol is now the mid tier |
| 12 | Gemini 3.7 Flash as intelligence-per-dollar winner | 🟡 Gemini 4 family; Carbon/Argon price **doubles Dec 1** |
| 13 | DeepSeek V4 Flash $0.14/$0.28 price floor | 🟡 **Retired**; V4.1 Flash $0.15/$0.60 off-peak, 2× at peak |
| 14 | DeepSeek V4 Pro $0.435/$0.87 | 🟡 **Promo over** — $0.66/$1.98 off-peak, $1.32/$3.96 peak |
| 15 | Kimi K3 as best open all-rounder | 🟡 **Kimi K3.1 Pro** (TB4 67.2%, AA v5 46) |
| 16 | Arena Text leader Claude Fable 5 | ✅ **Gemini 4 Carbon** (preliminary); Fable 5.2 leads Agent Arena and WebDev |
| 17 | Qwen3.6-27B as best 24 GB local model | 🟡 **Qwen3.8-27B** |
| 18 | "Meta exited the open frontier" | ⚠️ Partly reversed — Muse Glimmer-30B (open, local-class) and gated Muse Spark Open |
| 19 | OpenCode Go "$5 first month, then $10" | 🟡 **Discontinued Aug 24, 2026** — $10 from the first charge |

---

# 🏅 Key Takeaways

| Category | 🥇 Best Paid | 🥈 Best Open/Free | Status |
|:---|:---|:---|:---:|
| **Composite (AA v5)** | Claude Fable 5.2 (max), 65 | **Kimi K3.1 Pro, 46** (custom licence) / DeepSeek V4.1 Flash & GLM-5.3, 32 | ✅ |
| **Composite per dollar** | **GPT-6.2 Sol**, 57 at $1.01/task | DeepSeek V4.1 Flash (MIT) | 🟡 |
| **Terminal-Bench 4.0** | Opus 5.5 64.8% (official) / Gemini 4 Carbon 65.2% (AA) | **Kimi K3.1 Pro, 67.2% (AA)** | ⚠️ |
| **FrontierCode 2.0** | Claude Fable 5.2, 49.1% | — | ✅ |
| **Coding Agent Index v2.1** | **Tie — Fable 5.2 (high) & Opus 5.5 (max), 58** | — | 🟡 |
| **SWE-bench Verified** | *Archived* — Opus 5 97.0% final | DeepSeek V4 Pro 0813, 96.4% | ✅ |
| **SWE-bench Pro (SEAL)** | Muse Spark 1.1, 61.5% | Hy4 preview 65.7% *(vendor aggr.)* | ⚠️ |
| **GPQA Diamond** | *Saturated* — Gemini 4 Argon ~96.5% | Kimi K3, 93.5 | ⚠️ |
| **HLE-Diamond** | Claude Fable 5.2, 80% | — | 🟡 |
| **AIME 2026** | *Saturated* — GPT-5.5 / Opus 4.8, 100% | GLM-5.2 99.2% *(self-reported)* | ✅ |
| **Arena Text** | Gemini 4 Carbon, 1526 *(prelim.)* | Kimi K3.1 Pro ~1488 | ✅ / ⚠️ |
| **Agent Arena** | Claude Fable 5.2, 30.5% | — | ✅ |

### Best value

| Category | Winner | Basis |
|:---|:---|:---|
| 🏆 **Intelligence per dollar** | **GPT-6.2 Sol** | 57 on AA v5 at ~$1.01/task |
| 🏆 **Cheapest frontier-family tier** | **GPT-6 Luna / Claude Haiku 5.5** | $0.10/$0.50 |
| 🏆 **Best open all-rounder** | **Kimi K3.1 Pro** | Top open on AA v5 and TB4; custom licence |
| 🏆 **Best MIT-licensed** | **DeepSeek V4.1 Flash** | 32 on AA v5 at $0.15/$0.60 off-peak |
| 🏆 **Cheapest MIT hosted** | **GLM-5.3-Flash** | $0.15/$0.50 |
| 🏆 **Best local (24 GB GPU / 32 GB Mac)** | **Qwen3.8-27B** | Apache 2.0, ~18 GB |
| 🏆 **Best local (16 GB unified)** | **gpt-oss-20b / Gemma 4 12B** | fits; Gemma 4 12B for tool calling |
| 🏆 **Most permissive licence** | **Gemma 4 / Qwen3.8-27B / gpt-oss** | plain Apache 2.0 |

### Three conclusions

1. **Private test sets changed the open-weight story.** v3.2's headline ("the open tier reached the frontier") was true on public benchmarks and stopped being true on v5. The open tier still wins specific boards — Terminal-Bench 4.0, cost per task — but not the composite.
2. **The benchmark set turned over in one quarter.** Four of v3.2's eight headline benchmarks are saturated, archived or audited. The ones replacing them (FrontierCode 2.0, Terminal-Bench 4.0, HLE-Diamond) are newer, harder — and already spread 7+ points across harnesses.
3. **Effort routing now beats model choice on cost.** Fable 5.2 at high effort matches or beats its own max on the Coding Agent Index at about one-sixth the price. The same model spans $2.48–$44.70 per task by effort. Pick an effort default before you pick a model.

---

# 🔧 Relevance to a Cursor + OpenCode Stack

**OpenCode Go — live Console figures, Nov 18, 2026** (Go $10/mo · Go Plus $40/mo · Go Teams $20/member/mo, 2-member minimum)

| Go model | Go monthly limit | Est. requests / 5 hr (Go) | Direct API (in/out) | Evidence | Retention |
|:---|:---:|:---:|:---:|:---|:---:|
| `glm-5.2` | **$60** | 792 | $1.40 / $4.40 | v4.x: 51; TB 2.1 81%; no v5 row | 0 days |
| `minimax-m3` | **$60** | 3,210 | $0.30 / $1.20 | AA v5 19; SWE-V 80.5% | 0 days |
| `deepseek-v4-pro` | **$15** | 1,040 | $0.66 / $1.98 | AA v5 23; SWE-V 96.4% (final) | 0 days\* |
| `kimi-k3` | **$15** | 98 | ~$2.50 / ~$14 | superseded by K3.1 Pro | 0 days |
| `kimi-k3.1-pro` | $15 | 147 | $2.00 / $10.00 | **AA v5 46 (top open); TB4 67.2%** | 0 days |
| `glm-5.3` | $15 *(temporarily higher through Nov 22)* | 198 | $1.40 / $4.40 | AA v5 32 | 0 days |
| `glm-5.3-flash` | $60 | 6,320 | $0.15 / $0.50 | AA v5 28; MIT | 0 days |
| `deepseek-v4.1-flash` | **$100** | **43,300** | $0.15 / $0.60 | AA v5 32; MIT | 0 days\* |
| `minimax-m3.1-flash` | $20 | ~3,880 | $0.15 / $0.60 | AA v5 29 | 0 days |
| `claude-haiku-5.5` | $15 | 3,850 | $0.10 / $0.50 | AA v5 36 | ⚠️ 30 days |
| `gpt-6-luna` | $15 | 4,230 | $0.10 / $0.50 | AA v5 28 | ⚠️ 30 days |
| Gemini 4 Argon | $30 | 566 | $2 → $4 / $10 → $20 | AA v5 50 | ⚠️ 55 days |

\* DeepSeek's zero-retention agreement is renewed monthly; currently valid through **Nov 30, 2026**. DeepSeek models also require Global region access. ⚠️

**How the allowance actually works (resolves v3.2's open question):** paid Go models draw on **one shared allowance**. A model's monthly limit is how much of that allowance it would use if it were the only model you used — so $1.50 on a $15-limit model uses 10% of the month, while $1.50 on a $60-limit model uses 2.5%. Windows: 20% of the allowance per 5 hours, 50% per week (resets Monday 00:00 UTC). At the limit, requests block unless **Extra Usage** (the setting formerly called "Use balance") is on — then they bill your Console credit. ✅ (OpenCode Go docs)

**Three observations:**

1. **GLM-5.2 is still a defensible default on allowance, but it is now unbenchmarked on v5** and has ~4× fewer requests per window than MiniMax M3 and ~55× fewer than DeepSeek V4.1 Flash. Its case rests on v4-era evidence.
2. **Kimi K3.1 Pro strictly dominates Kimi K3 on Go** — same $15 limit, ~50% more requests per window, and the strongest open result on both AA v5 and TB4. Anywhere a config names `kimi-k3`, `kimi-k3.1-pro` is the like-for-like swap (confirm the slug with `/models`).
3. **Retention now varies by Go model.** Every model in a privacy-sensitive path should be a 0-day row; Haiku 5.5, GPT-6 Luna, Grok 4.7 (30 days) and Gemini 4 Argon (55 days) should not be.

---

# 📝 Methodology & Sources

### Source hierarchy (unchanged)

1. **Vendor primary** — pricing pages, docs, announcements
2. **Single-evaluator independent** — Artificial Analysis, Cognition (FrontierCode), tbench.ai, vals.ai, Scale SEAL, MathArena, Arena
3. **Multi-source aggregators** — used where two independent trackers agree
4. **Rejected** — figures appearing in one aggregator with no primary trace

### Sources

| Source | Data used | Tier |
|:---|:---|:---:|
| platform.claude.com/docs (pricing) | Full Anthropic rate card, cache/batch/fast, residency, tokenizer | ✅ 1 |
| Anthropic, OpenAI, Alibaba, Google launch posts (via coverage) | Release dates, list prices | ✅ 1 |
| opencode.ai/docs/go · opencode.ai/console/go · opencode.ai/go | Plans, shared allowance, per-model limits, retention | ✅ 1 |
| artificialanalysis.ai (methodology, v5 article, GPT-6.2 article, Fable 5.2 page, TB4 page) | Index v5.0.1, scores, cost per task | 2 |
| tbench.ai (via mirrors) | Terminal-Bench 4.0 official board and version history | 2 |
| Cognition FrontierCode board (via mirrors) | FrontierCode 2.0 | 2 |
| vals.ai | Final SWE-bench Verified and GPQA boards; archive notices | 2 |
| labs.scale.com | SWE-bench Pro, HLE | 2 |
| matharena.ai (via mirror) | AIME 2026 | 2 |
| arena.ai | Text, Coding, Agent, WebDev boards | 2 |
| modelcap, developersdigest, benchleader, BenchLM, llm-stats, requesty, officechai, implicator, The New Stack, datacamp, eweek, techjacksolutions, buildful, openchamber, threatfrontier, hashnode, kilo | Cross-checks, open-weight rows, local tier, pricing | 3 |

### Caveats

1. **Harness and version dependence is the dominant error source** in every coding score here — now including version churn inside a single benchmark family.
2. **AA v5 ≠ AA v4.** Never mix them in one chart.
3. **Effort settings are separate configurations.** A model's "score" without its effort level and cost per task is incomplete.
4. **Fallback routing** ("Default Fallback") still affects Anthropic top-tier entries.
5. **The Claude 4.7+ tokenizer (~30% more tokens)** still breaks naive per-token comparison. ✅
6. **Scheduled price changes:** Gemini 4 Carbon/Argon double Dec 1, 2026; GPT-5.6 Sol promo guaranteed only through Nov 21, 2026; DeepSeek ZDR on Go renews monthly.
7. **Open weights ≠ self-hostable** at trillion-parameter scale.
8. **Licences differ per checkpoint** — GLM-5.3 is custom while GLM-5.3-Flash is MIT; Kimi K3.1 Pro is custom.

### ❌ Still unverified

Claude Fable 5.2 on Terminal-Bench 4.0 (no independent figure found) · GPT-6.2 Astra/Sol independent TB4 · GLM-5.2 and Kimi K3 on AA v5 · Grok 4.7 on AA v5 (single-sourced 35.5) · Muse Wonder (43.6 vs 50 conflict) · Fable 5.2 Text Arena rating · Kimi K3.1 Pro final weight licence terms · Gemini 3.7 Flash current price · Qwen 3.5 9B benchmarks (**none published**).

---

> **Legend:** ⚡ reasoning · ★ open weights · ✅ primary · 🟡 corroborated · ⚠️ disputed/vendor-reported/single-sourced · — no published score or benchmark retired
> **Last Updated:** November 18, 2026
> **Next Update:** re-verify after **Dec 1** (Gemini 4 price step) and before any procurement decision — four frontier launches landed in the nine days before this edition.
