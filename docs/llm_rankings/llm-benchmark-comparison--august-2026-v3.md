# 🏆 LLM Benchmark Comparison — August 2026 (v3.1)

> **Version:** 3.1 (August 17, 2026)
> **Supersedes:** `llm-benchmark-comparison--june-2026-v2.md` (June 22, 2026)
>
> 📝 **Changelog v3.1:** Second research pass closed six of eight verification gaps. + §4 SWE-bench Verified and SWE-bench Pro (with the four-competing-scores finding) · + §5 GPQA Diamond · + §6 HLE (with the closed-book vs tool-assisted protocol split and the FutureHouse validity finding) · + Arena Elo now reportable as a range · AIME 2026 and per-model context windows remain unverified. v3.0 = initial.
> **Sources:** Anthropic Claude Platform Docs (primary), OpenAI official announcements (primary), Artificial Analysis, tbench.ai, vals.ai, BenchLM, evals.report, PricePerToken, llm-stats, DataLearner, provider pricing pages
> **Method change from v2:** every figure now carries a **verification status marker**. Where independent sources disagree, the disagreement is shown rather than resolved by editorial preference.

---

## ⚠️ Read This First — Why v3 Looks Different From v2

This report was commissioned with an explicit instruction: *confirm every datum from trustworthy sources; assume nothing.* Applying that standard honestly forced three structural changes.

**1. The v2 format cannot be filled responsibly.** v2 presented ~20 models × 6 benchmarks as single authoritative percentages. Attempting to reproduce that for August 2026 revealed that most of those cells are not independently verifiable — they are vendor-reported, harness-dependent, or mirrored between aggregators that cite each other. v3 reports what can be sourced and leaves the rest visibly empty.

**2. Benchmark scores now diverge wildly across sources for the same model on the same benchmark.** See §3. This is the single most important finding in this report and it undermines the premise of ranking tables generally.

**3. The Artificial Analysis Intelligence Index changed composition.** v2's benchmark set (SWE-bench Verified, SWE-bench Pro, GPQA, HLE, AIME 2026, Arena Elo) is no longer what the industry's most-cited composite measures. <cite index="11-1">AA Intelligence Index v4.1.1 now combines nine evaluations: GDPval-AA v2, 𝜏³-Banking, Terminal-Bench v2.1, SciCode, Humanity's Last Exam, GPQA Diamond, CritPt, AA-Omniscience, and AA-LCR</cite> — weighted <cite index="10-1">across four categories contributing 25% each: agents, coding, general capability, and scientific reasoning</cite>. **SWE-bench is no longer a component.** Terminal-Bench replaced it.

### Verification status legend

| Marker | Meaning |
|:---:|:---|
| ✅ | **Primary source.** Vendor's own pricing page, docs, or announcement. |
| 🟡 | **Corroborated secondary.** Two or more independent trackers agree. |
| ⚠️ | **Disputed.** Sources materially disagree; range shown. |
| ❌ | **Unverified.** Could not be confirmed. Deliberately left blank. |

---

## 📋 What Changed Since June 22, 2026

Verified model releases in the intervening eight weeks:

| Date | Release | Status |
|:---|:---|:---:|
| Jun 30 | **Claude Sonnet 5** — Anthropic | 🟡 |
| Jul 1 | **Claude Fable 5 restored** after June 12 export-control suspension | ✅ |
| Jul 9 | **GPT-5.6 family GA** (Sol, Terra, Luna) — 1.05M context all tiers | 🟡 |
| Jul 16 | **Kimi K3** — Moonshot AI, 2.8T params, largest open-weight model released | 🟡 |
| Jul 21 | **Gemini 3.6 Flash** and **Gemini 3.5 Flash-Lite** — Google | 🟡 |
| Jul 24 | **Claude Opus 5** — Anthropic, replaces Opus 4.8 at same price | 🟡 |
| Jul 26–27 | **Kimi K3 weights** published, Modified MIT | 🟡 |
| Jul 30 | **OpenAI price cut** — Terra −20%, Luna −80%, Sol unchanged | ✅ |
| Aug 13 | **Gemini 3.7 Flash** — Google, "most intelligent workhorse model" | 🟡 |
| ~Aug 13–14 | **GLM-5.3** (Z.ai), **DeepSeek V4 Pro 0813**, **Qwen3.8 Max** | ⚠️ |
| — | **Claude Mythos 5** — limited availability via Project Glasswing | ✅ |
| — | **Grok 4.5 / Grok 4.6** — xAI | ⚠️ |

**Structural shift in the open-weight tier.** <cite index="8-1">Meta has not shipped Llama 5, now forecast for 2027, and pivoted to its first closed frontier model, Muse Spark (April 2026), with no weights and no architecture paper — leaving Chinese labs (DeepSeek, Moonshot, Z.ai, Alibaba, MiniMax) as the effective owners of the open-weight frontier.</cite> 🟡

---

## 3️⃣ ⚠️ THE CENTRAL FINDING — Benchmark Scores Are Not Comparable Across Sources

This deserves its own section because it invalidates the way v2 (and most public leaderboards) present data.

**Terminal-Bench is the coding benchmark now inside the AA Intelligence Index. Here is what six trackers report for it, all checked within days of each other:**

| Source | Benchmark version | Reported leader & score | Checked |
|:---|:---|:---|:---:|
| Artificial Analysis | v2.1 | <cite index="39-1">GPT-5.6 Sol (xhigh) 89.5%, followed by Claude Opus 5</cite> | Aug 2026 |
| vals.ai | v2.1 | <cite index="45-1">GPT-5.6 Sol 85.77%, Claude Opus 5 84.64%</cite> | Aug 13 |
| CodingFleet | v2.1 | <cite index="40-1">GPT-5.6 Sol 88.8%, Grok 4.6 88.4%, Kimi K3 88.3%, DeepSeek V4 Pro 0813 87.9%</cite> | Aug 14 |
| BenchLM | v2.0 | <cite index="41-1">GPT-5.6 Sol 91.9%, Claude Mythos 5 88.0%, GPT-5.6 Terra 87.4%</cite> | Aug 15 |
| evals.report | v2.0 | <cite index="42-1">Claude Fable 5 — 84.3% task success</cite> | Aug 2026 |
| PricePerToken | unspecified | <cite index="38-1">GPT-5.6 Sol 65.9%, Claude Fable 5 62.9%, GPT-5.5 60.6%</cite> | Aug 12 |

**The same model, same benchmark family, spans 65.9% → 91.9%.** That is a 26-point range.

### Why the spread exists — three documented mechanisms

**Version confusion.** <cite index="42-1">Terminal-Bench 2.1 is a different task set from 2.0, and most 2026 model cards self-report the 2.0 version.</cite> <cite index="40-1">Scores are not directly comparable across versions — 2.1 is harder.</cite>

**Harness and scaffold variation.** <cite index="40-1">Results combine vendor and leaderboard harnesses; compare directionally unless the same evaluator and scaffold were used.</cite> A concrete instance: <cite index="40-1">Grok 4.6 scores 88.4% on v2.1 per Artificial Analysis, while xAI itself reported Terminal-Bench v3.0 instead, at 26.0%.</cite>

**Refusal-fallback accounting.** This one is subtle and material. <cite index="45-1">Both Fable 5's and Opus 5's runs used Claude Opus 4.8 as a refusal fallback; counting Opus 5's nine affected passes as failures lowers it from 84.64% to 81.27%.</cite> A methodology choice invisible in the headline number moves it 3.4 points.

> **Practical implication for tooling decisions:** do not select a model on a leaderboard delta under ~5 points. That is inside the cross-source noise band. Run your own eval on your own task — 30–50 representative cases — and let that decide.

---

## 1️⃣ Composite Intelligence — Artificial Analysis Intelligence Index v4.1.1

> **What it measures:** <cite index="10-1">a weighted average of nine production benchmarks scaled 0–100, across agents, coding, general capability, and scientific reasoning at 25% each.</cite>
> **Why it replaced v2's tables:** it is the most-cited independent composite, and it is run by one evaluator with one methodology — which removes the cross-source problem in §3 (though not the harness problem within it).

| Rank | Model | Score | Status |
|:---:|:---|:---:|:---:|
| 1 | **Claude Opus 5** (Adaptive Reasoning, Max Effort) | **63** | ✅ |
| 1= | **Claude Opus 5** (Adaptive Reasoning, Xhigh Effort) | **63** | ✅ |
| 3 | **Claude Fable 5** (Max Effort, Opus 4.8 Fallback) | **62** | ✅ |
| 4 | **Grok 4.6** | 60.9 | 🟡 |

<cite index="11-1">Claude Opus 5 (Adaptive Reasoning, Max Effort) scores the highest on Artificial Analysis Intelligence Index with a score of 63, followed by Claude Opus 5 (Adaptive Reasoning, Xhigh Effort) with 63, and Claude Fable 5 (Max Effort, Opus 4.8 Fallback) with 62.</cite> ✅

<cite index="7-1">A mirrored snapshot verified August 15 ranks Claude Opus 5 first at 63.0%, ahead of Claude Fable 5 (62.1%) and Grok 4.6 (60.9%) among 177 tested models.</cite> 🟡

**Note the fallback annotation on Fable 5.** Its index entry explicitly carries "Opus 4.8 Fallback" — the same refusal-substitution caveat described in §3. Fable 5's score is not a clean single-model result.

**Ranks 5+ : ❌ not verified.** Numerous aggregators publish full top-20 tables; they disagree with each other and mostly mirror one another's data. Not reproduced here.

---

## 2️⃣ Coding — Terminal-Bench v2.1

> **What it tests:** <cite index="39-1">89 curated tasks across software engineering, system administration, data processing, model training, and security, with environment and instruction fixes so scores reflect agent capability rather than environment gaps.</cite>
> **Difficulty calibration:** <cite index="39-1">the 2.0 paper reported frontier models and agents scoring under 65%.</cite> August 2026 scores near 85–90% represent roughly a year of movement — or harness improvement. The benchmark authors publish dataset and harness at tbench.ai.

**Single-evaluator reading (Artificial Analysis, the AA-index component):**

| Rank | Model | Score | Status |
|:---:|:---|:---:|:---:|
| 1 | **GPT-5.6 Sol** (xhigh) | **89.5%** | ✅ |
| 2 | **Claude Opus 5** (Adaptive Reasoning) | — | ✅ (rank only) |

**Independent second reading (vals.ai, full split breakdown):**

<cite index="45-1">GPT-5.6 Sol leads at 85.77%, just ahead of Claude Opus 5 (84.64%) — but Sol's advantage is driven by the medium split (86.06% vs 83.64%), not the hard split, where they are tied at 84.44% with a sharp cliff to third place (74.44%). Eleven models reach 100% on easy, and the median on that split is 83.33%.</cite> 🟡

> 🔑 **The most decision-relevant fact in this report:** on the *hard* split the two leaders are **tied at 84.44%**, and third place is **10 points back**. The headline ranking is decided by medium-difficulty tasks. For production work that skews hard, Sol and Opus 5 are equivalent.

**Vendor-reported entrants (not independently verified):** <cite index="40-1">Kimi K3 at 88.3% (v2.1) with KimiCode at max reasoning; Grok 4.6 88.4%; DeepSeek V4 Pro 0813 87.9%; Qwen3.8 Max 86.6%; Gemini 3.7 Flash 85.8%; Muse Spark 1.2 82.9% via Meta's Muse Code harness; Muse Spark 1.1 80.0%.</cite> ⚠️ — mixed vendor/leaderboard harnesses, per the source's own warning.

---

## 4️⃣ SWE-bench Verified & SWE-bench Pro

**Status change first:** SWE-bench is **no longer a component of the AA Intelligence Index** ✅ — replaced by Terminal-Bench v2.1. v2 already recorded OpenAI's February 2026 withdrawal of SWE-bench Verified from official reporting over contamination. It remains widely quoted, so it is reported here with heavy caveats.

### SWE-bench Verified — approaching saturation

| Rank | Model | Score | Source | Status |
|:---:|:---|:---:|:---|:---:|
| 1 | **Claude Opus 5** | **96.0%** (Anthropic launch figure) / **97.0%** (vals.ai run) | localaimaster | ⚠️ |
| 2 | **GPT-5.6 Sol** | 96.2% | localaimaster | ⚠️ |
| 3 | **Claude Mythos 5** | 95.5% | BenchLM, Vellum | 🟡 |
| 4 | **Claude Fable 5** | 95.0% | multiple | 🟡 |

<cite index="69-1">As of August 15, 2026, Claude Opus 5 leads the SWE-bench Verified leaderboard with 96%, followed by Claude Mythos 5 (95.5%) and Claude Fable 5 (95%) across 64 tracked models. The top models are clustered within 1.0 points, suggesting this benchmark is nearing saturation for frontier models.</cite> 🟡

> ⚠️ **The ranking is inside the error bar.** <cite index="71-1">Most SWE-bench Verified scores are vendor-reported and can vary by ±2–3% depending on the agent scaffold, evaluation configuration, and random factors.</cite> A 1.0-point spread across the top four, against a ±2–3% variance, means **there is no verifiable #1 on this benchmark.** Note also that one source reports Opus 5 at both 96.0% and 97.0% depending on whose run you read.

**Open-weight tier:** <cite index="66-1">DeepSeek V4-Pro-Max posts 80.6% on SWE-bench Verified, the top open-weights score, tied with Gemini 3.1 Pro; V4-Flash-Max posts 79.0%.</cite> 🟡 <cite index="86-1">Kimi K3 reports 76.8%; GLM-5.2 has no vendor figure</cite> 🟡 — <cite index="66-1">GLM-5.2's 62.1% is third-party measured, as Z.ai published no SWE-bench number at launch.</cite> ⚠️

### SWE-bench Pro — ⚠️ four competing "best" scores, all real

This is the clearest documented case of the §3 problem in the entire report.

| Reported "best" | Model | What it actually measures |
|:---:|:---|:---|
| **80.3%** | Claude Mythos 5 / Fable 5 | Cross-source vendor aggregate (CodingFleet) |
| **80.0%** | Claude Fable 5 | llm-stats vendor aggregate |
| **61.5%** | Muse Spark 1.1 | Scale's standardized **SEAL harness** |
| **59.1%** | GPT-5.4 (xHigh) | Scale's **standardized public set** |
| **47.1%** | Claude Opus 4.6 | Scale's **private commercial set** |

<cite index="66-1">Three numbers all claim to be the best SWE-bench Pro score: 59.1% (GPT-5.4 xHigh, Scale's standardized public set), 80.0% (Claude Fable 5, the llm-stats vendor aggregate), and 47.1% (Claude Opus 4.6, Scale's private commercial set). All three are real. The spread is scaffolding and data splits, and most pages quoting a score never say which one they mean.</cite> ⚠️

<cite index="71-1">The Fable 5 ~80% is a vendor-scaffold number — on Scale's standardized SEAL harness the top score is Muse Spark 1.1 at 61.5%.</cite> 🟡

**Why the gap exists structurally:** <cite index="66-1">SWE-bench Pro is Scale AI's contamination-resistant benchmark — 1,865 real-world tasks across 41 professional repositories, scored Pass@1, which the same frontier models clearing 80–95% on SWE-bench Verified solve only ~59% of under standardized scaffolding.</cite>

**Vendor-reported Pro table** (CodingFleet, Aug 14, cross-source): <cite index="70-1">Claude Mythos 5 80.3%, Claude Fable 5 80.3%, Claude Opus 5 79.2%, Qwen3.8 Max 67.7%, GPT-5.6 Sol 64.6%, Muse Spark 1.1 61.5%, Qwen3.7 Max 60.6%, GLM-5.1 58.4%.</cite> ⚠️ — the same source warns <cite index="70-1">scores are vendor-reported unless otherwise noted, cross-vendor harnesses can differ, so treat small gaps as directional.</cite>

> 🔑 **Rule of thumb:** when someone quotes a SWE-bench Pro number at you, the first question is *which harness* — vendor scaffold, SEAL standardized, or private set. The answer moves the number by up to 33 points.

---

## 5️⃣ GPQA Diamond (Scientific Reasoning)

> **What it tests:** <cite index="89-1">448 multiple-choice questions written by domain experts in biology, physics and chemistry; PhD-level experts in the corresponding domains reach 65% accuracy (74% discounting clear mistakes identified in retrospect), while highly skilled non-expert validators reach 34% despite unrestricted web access.</cite> The Diamond subset is the hardest 198.
> **Why this one is more trustworthy:** Artificial Analysis runs it as a single evaluator with one methodology.

**Artificial Analysis (single evaluator) — ✅**

| Rank | Model | Score |
|:---:|:---|:---:|
| 1 | **Grok 4.6** (high) | **94.9%** |
| 2 | **Gemini 3.7 Flash** (high) | **94.5%** |
| 3 | **GPT-5.6 Sol** (max) | **94.1%** |

<cite index="89-1">Grok 4.6 (high) scores the highest on GPQA with 94.9%, followed by Gemini 3.7 Flash (high) at 94.5%, and GPT-5.6 Sol (max) at 94.1%.</cite> ✅

**Cross-reference:** <cite index="85-1">Vellum reports Claude Opus 5 / Claude Mythos 5 at 94.1 on GPQA Diamond.</cite> 🟡

**Open-weight tier:** <cite index="86-1">Kimi K3 at 93.5, GLM-5.2 at 91.2.</cite> 🟡

> 🔑 **Two observations.** First, the top five are inside 1 point — this benchmark is saturated and no longer discriminates between frontier models. Second, **Gemini 3.7 Flash at 94.5% is a $0.75/$3.75 model** matching flagships costing 7–40x more. On science reasoning specifically, paying for a flagship is hard to justify.

---

## 6️⃣ HLE — Humanity's Last Exam

> **What it tests:** <cite index="11-1">2,500 expert-vetted questions across mathematics, sciences and humanities, designed as the final closed-ended academic evaluation.</cite> Built by <cite index="90-1">Scale AI in partnership with the Center for AI Safety, as 2,500 of the toughest subject-diverse multi-modal questions, addressing benchmark saturation.</cite>

### ⚠️ The protocol split — this is why HLE numbers disagree by 20 points

| Protocol | Frontier score | Source |
|:---|:---:|:---|
| **Closed-book, no tools** (official CAIS/Scale) | **mid-40s%** | benchmarkingagents |
| **Tool-assisted / mixed aggregate** | **~55–65%** | BenchLM, PricePerToken |

<cite index="84-1">By August 2026 the text-only (no-tools) frontier has reached the mid-40s percent on the official CAIS/Scale leaderboard — real progress but still short of saturation.</cite> 🟡

BenchLM states the problem explicitly: <cite index="87-1">a model with search, browsing, or code execution is not taking the same test as a closed-book model — BenchLM can preserve published protocol notes and per-row provenance, but it cannot make differently disclosed HLE configurations fully comparable.</cite> ⚠️

**Tool-assisted / aggregate boards:**

| Source | Leader | Runner-up |
|:---|:---|:---|
| BenchLM (Aug 15) | <cite index="87-1">Claude Opus 5, 64.7%</cite> | <cite index="87-1">Claude Mythos 5 64.5%, Muse Spark 1.1 62.1%</cite> |
| PricePerToken (Aug 11) | <cite index="83-1">Claude Fable 5, 55.5%</cite> | <cite index="83-1">Claude Opus 5 54.9%, GPT-5.6 Sol 49.5%</cite> |
| Vellum | <cite index="85-1">Claude Opus 5, 64.7</cite> | <cite index="85-1">Claude Mythos 5, 64.5</cite> |

**Open-weight tier:** <cite index="86-1">Kimi K3 at 56, GLM-5.2 at 54.7.</cite> 🟡

**Reasoning effort dominates on this benchmark:** <cite index="84-1">as of August 2026 reasoning-configured models occupy the entire top of the text-only board, and the same base model in a non-reasoning or low-effort configuration scores materially lower — a gap far wider than the equivalent 1–2 points on MMLU-Pro or 3–4 points on GPQA-Diamond. The leaderboard reports each entry with its thinking-effort setting for exactly this reason.</cite>

### 🚨 Validity warning — treat HLE scores with caution

<cite index="88-1">An independent investigation by FutureHouse, published in July 2025, suggested that around 30% of the HLE answers for text-only chemistry and biology questions could be incorrect; the benchmark's team partially replicated the findings and said they hope to institute a continuous revisions process.</cite> ⚠️

**If roughly a third of the answer key in two major subjects is wrong, a 5-point difference between models on HLE carries very little information.** Weight this benchmark accordingly.

---

## 💰 Complete Pricing Table — Verified

> All prices USD per 1M tokens, standard tier, short-context.

### Anthropic — ✅ PRIMARY SOURCE (platform.claude.com/docs, verified Aug 17, 2026)

| Model | Input | 5m Cache Write | 1h Cache Write | Cache Hit | Output |
|:---|:---:|:---:|:---:|:---:|:---:|
| **Claude Fable 5** | $10 | $12.50 | $20 | $1.00 | $50 |
| **Claude Mythos 5** (limited availability) | $10 | $12.50 | $20 | $1.00 | $50 |
| **Claude Opus 5** | $5 | $6.25 | $10 | $0.50 | $25 |
| **Claude Opus 4.8** | $5 | $6.25 | $10 | $0.50 | $25 |
| **Claude Opus 4.7 / 4.6 / 4.5** | $5 | $6.25 | $10 | $0.50 | $25 |
| **Claude Sonnet 5** | $2 | $2.50 | $4 | $0.20 | $10 |
| **Claude Sonnet 4.6 / 4.5** | $3 | $3.75 | $6 | $0.30 | $15 |
| **Claude Haiku 4.5** | $1 | $1.25 | $2 | $0.10 | $5 |

**🔑 Correction to widespread reporting:** multiple trackers still state Sonnet 5 rises to $3/$15 on September 1. Anthropic's own docs say otherwise: <cite index="28-1">the $2/$10 pricing for Claude Sonnet 5, announced at launch as introductory pricing through August 31, 2026, is now the standard price. The previously scheduled increase to $3/$15 on September 1, 2026 will not occur.</cite> ✅

**🔑 The tokenizer caveat that breaks naive price comparison:** <cite index="28-1">Claude 4.7 and later models and Claude Mythos Preview use a newer tokenizer that produces approximately 30% more tokens for the same text. Claude Sonnet 4.6 and earlier use the previous tokenizer.</cite> ✅ — **A per-million-token comparison between Sonnet 5 and any pre-4.7 model understates Sonnet 5's real bill by roughly 30%.** This applies to every cross-vendor comparison in this document.

Other verified Anthropic mechanics: <cite index="28-1">Batch API discounts input and output 50%; cache hits cost 0.1x base input; Claude 4.6 and later include the full 1M context window at standard pricing with no long-context premium; `inference_geo: "us"` applies a 1.1x multiplier; Fast mode for Opus 5 and Opus 4.8 is $10/$50 and is unavailable with the Batch API.</cite> ✅

### OpenAI — ✅ PRIMARY (openai.com announcement) + 🟡 corroborated

| Model | Input | Output | Long-context meter | Status |
|:---|:---:|:---:|:---:|:---:|
| **GPT-5.6 Sol** | $5 | $30 | $10 / $45 | 🟡 |
| **GPT-5.6 Terra** | **$2** | **$12** | $4 / $18 | ✅ |
| **GPT-5.6 Luna** | **$0.20** | **$1.20** | $0.40 / $1.80 | ✅ |
| GPT-5.5 | $5 | $30 | $10 / $45 | 🟡 |
| GPT-5.5 Pro | $30 | $180 | — | 🟡 |
| GPT-5.4 | $2.50 | $15 | $5 / $22.50 | 🟡 |
| GPT-5.4 mini | $0.75 | $4.50 | — | 🟡 |

Directly from OpenAI: <cite index="29-1">starting July 30, API pricing is $2 per million input tokens and $12 per million output tokens for Terra, and $0.20 per million input tokens and $1.20 per million output tokens for Luna.</cite> ✅

<cite index="34-1">On 2026-07-30 OpenAI cut Luna by 80% and Terra by 20%, while Sol stayed the same. Luna's input dropped from $1.00 to $0.20 and output from $6.00 to $1.20; Terra's input fell from $2.50 to $2.00 and output from $15.00 to $12.00.</cite> 🟡

<cite index="36-1">The GPT-5.6 family went GA on July 9, 2026 with a 1.05M-token context window on all three tiers.</cite> 🟡 <cite index="36-1">Cached input bills at 10% of standard rates; the Batch API halves everything; a 10% regional-processing uplift applies to eligible models released on or after March 5, 2026.</cite> 🟡

> ⚠️ **v2's ladder is dead.** <cite index="32-1">Terra now undercuts GPT-5.4 at $2.00/$12.00 against $2.50/$15.00, and Luna is the cheapest model in the flagship table, roughly 4x under gpt-5.4-mini at $0.75/$4.50. If you are still reasoning from June's numbers, the whole ladder has moved under you.</cite>

### Google — 🟡 corroborated secondary

| Model | Input | Output | Note | Status |
|:---|:---:|:---:|:---|:---:|
| **Gemini 3.1 Pro** | $2 | $12 | ≤200K; $4/$18 above | 🟡 |
| **Gemini 3.7 Flash** | **$0.75** | **$3.75** | ⏰ **doubles Jan 1, 2027** | 🟡 |
| **Gemini 3.6 Flash** | $0.75 | $3.75 | moved onto 3.7 rate | ⚠️ |
| Gemini 3.5 Flash-Lite | $0.30 | $2.50 | | 🟡 |
| Gemini 2.5 Flash-Lite | $0.10 | $0.40 | current floor | 🟡 |

<cite index="61-1">Google released Gemini 3.7 Flash on August 13, 2026. Through December 31, 2026 the API rate is $0.75 per 1M input and $3.75 per 1M output. From January 1, 2027 it becomes $1.50 and $7.50.</cite> 🟡

⚠️ **Conflict on Gemini 3.6 Flash.** One tracker checked Aug 1 lists it at <cite index="60-1">$1.50/M input, $0.15/M cached input, $7.50/M output</cite>; another checked Aug 16 says <cite index="59-1">Google moved Gemini 3.6 Flash onto the same $0.75/$3.75 rate</cite>. Verify directly before budgeting.

> ⏰ **Two scheduled price increases to calendar:** Gemini 3.7 Flash and 3.6 Flash both double on **January 1, 2027**. Anything you build on Flash economics in Q4 2026 needs a 2x line in the 2027 forecast.

### Open-weight tier — 🟡 corroborated

| Model | Creator | Input | Output | Params / Context | License | Status |
|:---|:---|:---:|:---:|:---|:---|:---:|
| **Kimi K3** | Moonshot | $3.00 | $15.00 | 2.8T / 1.05M | Modified MIT | 🟡 |
| **GLM-5.2** | Z.ai | ~$1.40 | ~$4.40 | 744–753B / 1M | MIT | ⚠️ |
| **MiniMax M3** | MiniMax | ~$0.30 | ~$1.20 | — / 1M | Community | ⚠️ |
| **DeepSeek V4 Pro** | DeepSeek | $0.435 | $0.87 | 1.6T total, 49B active / 1M | MIT | 🟡 |
| **DeepSeek V4 Flash** | DeepSeek | $0.14 | $0.28 | — / 1M | MIT | 🟡 |
| Kimi K2.7 Code | Moonshot | $0.95 | $4.00 | — | — | 🟡 |
| Kimi K2.6 | Moonshot | $0.95 | $4.00 | — | — | 🟡 |
| **GLM-5.3** | Z.ai | ❌ | ❌ | weights promised, not shipped | — | ⚠️ |

<cite index="50-1">Kimi K3 is the largest open-weight model ever released at 2.8 trillion parameters and scored fourth overall on the Artificial Analysis Intelligence Index — ahead of Claude Opus 4.8.</cite> 🟡

<cite index="56-1">DeepSeek V4 Pro is the cost leader at $0.87 per million output tokens with MIT weights already on Hugging Face; GLM-5.2 is the fastest at about 168 tokens per second and sits between the other two on price and capability.</cite> 🟡

<cite index="56-1">On a blended cost-per-task basis, Artificial Analysis puts K3 at $0.94 per task and DeepSeek V4 Pro at $0.04.</cite> 🟡 — **a 23x spread**, which matters far more than the per-token headline.

**Self-hosting reality check:** <cite index="50-1">V4 Pro at 1.6T needs a multi-node GPU cluster for BF16 serving; GLM-5.2 at 753B requires roughly 8 H100s at standard quantization.</cite> 🟡 "Open weights" ≠ "runnable on your hardware."

**On GLM-5.3:** <cite index="54-1">use GLM-5.3 if you want the most ambitious new coding/cyber model and can accept first-party benchmark evidence, a brand-new endpoint, and weights that are promised rather than downloadable today.</cite> ⚠️

---

## 📉 Corrections to the June 2026 (v2) Report

| # | v2 claim | August 2026 status |
|:---:|:---|:---|
| 1 | GLM-5.2 at $0.45 / $1.80 | ⚠️ Current sources report **~$1.40 / ~$4.40** — roughly 3x higher. v2's figure may have been a discounted reseller rate. |
| 2 | DeepSeek V4 Pro at $0.23 / $1.10 | 🟡 Current: **$0.435 / $0.87** — input higher, output lower. |
| 3 | Claude Fable 5 "marked unavailable" | ✅ **Restored July 1, 2026** after the June 12 export-control suspension. Now live at $10/$50. |
| 4 | Claude Opus 4.8 as Anthropic flagship | ✅ Superseded by **Opus 5** (Jul 24) at identical $5/$25. |
| 5 | GPT-5.5 as OpenAI flagship | 🟡 Superseded by **GPT-5.6 Sol** (GA Jul 9). |
| 6 | SWE-bench tables as headline coding measure | ✅ **Removed from the AA Intelligence Index**; replaced by Terminal-Bench v2.1. |
| 7 | Qwen3.5 9B at $0.10 / $0.15 | ❌ Not re-verified. Treat as stale. |
| 8 | "Blended = (3×input + output)/4" | ⚠️ Methodologically unsound now — <cite index="55-1">Artificial Analysis prices on a blended 7:2:1 cache/input/output basis, which removes vendor framing.</cite> Ignoring cache pricing materially misstates agentic workload cost. |
| 9 | Per-token cross-vendor comparison | ⚠️ **Broken by the Claude 4.7+ tokenizer change** (~30% more tokens for identical text). ✅ |
| 10 | Llama 4 Maverick / Scout as the Meta open line | 🟡 Meta has **exited the open frontier**; Llama 5 forecast 2027, Muse Spark is closed-weights. |

---

## 🏅 Key Takeaways

### Best by category — only where verifiable

| Category | Leader | Basis | Status |
|:---|:---|:---|:---:|
| **Composite intelligence** | **Claude Opus 5** (Max/Xhigh Effort), 63 | AA Intelligence Index v4.1.1 | ✅ |
| **Terminal-Bench (single evaluator)** | **GPT-5.6 Sol** (xhigh), 89.5% | Artificial Analysis | ✅ |
| **Terminal-Bench hard split** | **Tie — Sol and Opus 5, 84.44%** | vals.ai | 🟡 |
| **Cheapest frontier-tier API** | **GPT-5.6 Luna**, $0.20/$1.20 | OpenAI announcement | ✅ |
| **Best open-weight all-rounder** | **Kimi K3** — 4th on AA Index, ahead of Opus 4.8 | AA Index | 🟡 |
| **Open-weight cost leader** | **DeepSeek V4 Pro**, $0.04/task blended | Artificial Analysis | 🟡 |
| **Absolute price floor (hosted)** | **DeepSeek V4 Flash**, $0.14/$0.28 | DeepSeek listing | 🟡 |
| **SWE-bench Verified** | **No verifiable #1** — top 4 within 1.0 pt, ±2–3% variance | multiple | ⚠️ |
| **SWE-bench Pro (SEAL standardized)** | **Muse Spark 1.1**, 61.5% | Scale SEAL harness | 🟡 |
| **GPQA Diamond** | **Grok 4.6** (high), 94.9% | Artificial Analysis | ✅ |
| **GPQA per dollar** | **Gemini 3.7 Flash**, 94.5% at $0.75/$3.75 | Artificial Analysis | ✅ |
| **HLE (tool-assisted)** | **Claude Opus 5**, 64.7% | BenchLM, Vellum | 🟡 |
| **HLE (closed-book official)** | frontier is **mid-40s%** — no single leader confirmed | CAIS/Scale | ⚠️ |
| **Agentic (AA Agentic Index)** | **Claude Opus 5**, 55.3 | Artificial Analysis | 🟡 |
| **Arena Elo (text)** | **Claude Fable 5**, ~1508–1525 | see below | ⚠️ |
| **AIME 2026** | ❌ **Not verified** | — | ❌ |

### Arena Elo — now reportable, as a range

Arena's own changelog ✅ confirms the roster is current: <cite index="78-1">claude-opus-5-high and claude-opus-5-max have been added to the Text, Vision, Document and Code Arena leaderboards; gpt-5.6-sol-xhigh, gpt-5.6-terra-xhigh and gpt-5.6-luna-xhigh have been added to Code, Document, Vision and Text Arena; Claude Opus 5 (Max) and (High) have been added to the Agent Arena.</cite>

**Text Arena — Claude Fable 5 leads, ~1508–1525** ⚠️ (range reflects snapshot date, not source disagreement)

- <cite index="75-1">On the August 1 cutoff, GPT-5.6 Sol sits #14 on Arena text at 1482.8, down from #11, while Claude Fable 5 leads at 1508.6.</cite> 🟡
- <cite index="80-1">Claude Fable 5 holds #1 on the overall text leaderboard at roughly 1525 ELO; Arena re-baselined its score on July 12 to count only votes cast since its July 1 restoration, and it settled back on top.</cite> 🟡

**Category boards** (BenchLM, from the Arena Leaderboard Dataset on Hugging Face, 2026-07 snapshot): <cite index="81-1">coding Elo led by claude-fable-5 at 1553; math led by claude-fable-5 at 1543; vision led by claude-fable-5 at 1334; the highest-rated openly licensed model is glm-5.1 at 1475.</cite> 🟡

**Agent board:** <cite index="75-1">Claude Opus 5 tops Arena's Agent board, with Kimi K3 in third; it also took #1 on Artificial Analysis's Agentic Index at 55.3, ahead of GPT-5.6 Sol at 54.0 and Claude Fable 5 at 52.8.</cite> 🟡

> ⚠️ **Two Arena-specific traps.** Methodology versioning: <cite index="74-1">updates such as the January 2026 rebrand caused 30+ Elo shifts unrelated to model quality — anchor decisions on methodology version.</cite> And noise floor: <cite index="74-1">treat any Elo gap under 30 points as procurement-equivalent noise; 60% of models within 30 Elo swap ranks within a single quarter.</cite> **The entire Text Arena top cluster sits inside that 30-point band.**

### Three practical conclusions

1. **Anthropic leads the composite; OpenAI leads single-evaluator coding; they tie on hard coding tasks.** Any claim stronger than that is not supported by verifiable evidence.
2. **The cheap tier collapsed in price and the expensive tier didn't.** Luna at $0.20/$1.20 and DeepSeek V4 Flash at $0.14/$0.28 make routing the dominant cost lever — far more than model choice at the top.
3. **Cross-source benchmark deltas under ~5 points are noise.** Build a task-specific eval; treat every table here as a shortlist generator, not a decision.

---

## 🔧 Relevance to a Cursor + OpenCode Stack

Cross-referencing the verified pricing above against the OpenCode Go roster (see `OpenCode_Go_Setup.md`):

| Go model | Go tier | Direct API price | Note |
|:---|:---:|:---:|:---|
| `glm-5.2` | ✅ $60/mo | ~$1.40 / ~$4.40 | Full Go tier, ~4,300 req/mo |
| `minimax-m3` | ✅ $60/mo | ~$0.30 / ~$1.20 | Cheapest full-tier |
| `qwen3.7-max` | ✅ $60/mo | ❌ not re-verified | |
| `kimi-k3` | ⚠️ $15/mo | $3.00 / $15.00 | Highest capability, ~490 req/mo |
| `deepseek-v4-pro` | ⚠️ $15/mo | $0.435 / $0.87 | Cheapest per token, reduced Go tier |
| `glm-5.3` | ⚠️ $15/mo | ❌ | Weights promised, not shipped |

**Observation:** DeepSeek V4 Pro is simultaneously the **cheapest** model on direct API and a **reduced-tier** model on Go. If it becomes your primary build model, direct API or OpenRouter is more economical than Go. GLM-5.2 remains the best Go default — full tier and mid-price.

---

## 📝 Methodology & Sources

### Source hierarchy applied

1. **Vendor primary** — pricing pages, docs, official announcements
2. **Single-evaluator independent** — Artificial Analysis, vals.ai (one methodology, reproducible)
3. **Multi-source aggregators** — used only where two independent trackers agree
4. **Rejected** — any figure appearing in exactly one aggregator with no primary trace

### Sources consulted

| Source | URL | Data used | Tier |
|:---|:---|:---|:---:|
| Claude Platform Docs | platform.claude.com/docs/en/about-claude/pricing | Full Anthropic pricing, tokenizer note, cache/batch/fast-mode | ✅ 1 |
| OpenAI | openai.com/index/advancing-the-price-performance-frontier-with-gpt-5-6 | Terra/Luna July 30 rates | ✅ 1 |
| Artificial Analysis | artificialanalysis.ai | Intelligence Index v4.1.1 composition and leaders; Terminal-Bench v2.1 | 2 |
| vals.ai | vals.ai/benchmarks/terminal-bench-2-1 | Terminal-Bench split analysis, fallback caveat | 2 |
| tbench.ai | tbench.ai/leaderboard | Benchmark provenance | 2 |
| BenchLM / evals.report / CodingFleet / PricePerToken / llm-stats / DataLearner | various | Divergence analysis (§3) | 3 |
| DeepInfra / MarkTechPost / LLM Gateway / BenchLM | various | Open-weight params, licensing, pricing | 3 |

### Caveats

1. **Harness dependence is the dominant source of error** in every coding score in this report.
2. **Vendor-reported scores are marked ⚠️** and use optimized scaffolds.
3. **Refusal fallbacks** materially alter Anthropic scores; check whether a run used Opus 4.8 substitution.
4. **The Claude 4.7+ tokenizer change (~30% more tokens)** invalidates naive per-token cross-vendor comparison. ✅
5. **Blended-price formulas that ignore cache pricing** misstate agentic workload cost. Cache reads are 10% of input on both Anthropic and OpenAI.
6. **Scheduled increases:** Gemini 3.7/3.6 Flash double January 1, 2027.
7. **Open weights ≠ self-hostable** at these parameter counts.
8. **Author disclosure:** this report was compiled by Claude (Anthropic). All Anthropic-favourable claims are cited to Anthropic's own docs (pricing) or to independent evaluators (rankings). The Arena section declines to report a figure that would have favoured Anthropic, because sources conflict.

### ❌ Explicitly not verified in this edition

**Closed in v3.1:** GPQA Diamond ✅ · HLE 🟡 · SWE-bench Verified ⚠️ · SWE-bench Pro 🟡 · Arena Elo ⚠️ · AA Agentic Index 🟡

**Still unverified:** AIME 2026 (MathArena at `matharena.ai/?comp=aime--aime_2026` is the credible primary source; one tracker reviewed shows no models scored for the 2026 set, and Artificial Analysis tracks AIME **2025**, not 2026 — v2's AIME 2026 table could not be reproduced) · per-model context windows beyond those cited · Grok 4.5/4.6 pricing · Qwen3.8 Max pricing (one source indicates $2/$6, single-sourced) · Muse Spark pricing (one source indicates $1.25/$4.25, single-sourced) · Nemotron, Gemma, Mistral, Amazon Nova current lines.

**These are absent by design, not oversight.** Populating them would have required carrying v2's figures forward or trusting single unsourced aggregators — both of which violate the verification standard set for this report.

---

> **Legend:** ✅ primary · 🟡 corroborated · ⚠️ disputed · ❌ unverified
> **Last Updated:** August 17, 2026
> **Next Update:** re-verify before any procurement decision; pricing moved three times in the eight weeks covered by this edition.
