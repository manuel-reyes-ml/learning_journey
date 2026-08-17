# 🏆 LLM Benchmark Comparison — August 2026 (v3.2)

> **Version:** 3.2 (August 17, 2026)
> **Supersedes:** `llm-benchmark-comparison--june-2026-v2.md` (June 22, 2026)
>
> 📝 **Changelog v3.2:** **Full model rosters restored.** v3.0/v3.1 deleted rows where scores couldn't be verified, which silently stripped most open-weight models and produced a Claude/GPT-heavy document. This version restores v2's convention — every model keeps its row, missing scores show "—" — and adds a dedicated open-weight section and a new **local/self-hostable tier**. + Qwen, Gemma, Nemotron, MiMo, Hy3, gpt-oss, Llama lines restored · + §9 local models by hardware.
>
> 📝 **v3.1:** Added SWE-bench Verified & Pro, GPQA Diamond, HLE, Arena Elo ranges. **v3.0:** Initial rebuild on verification-status method.

---

## ⚠️ Read This First

This report was commissioned with an explicit instruction: *confirm every datum from trustworthy sources; assume nothing.* Three things follow.

**1. Every figure carries a verification marker.** Where sources disagree, the disagreement is shown rather than resolved by editorial preference.

**2. Missing data shows as "—", not as a deleted row.** This matters more than it sounds. Aggregators cover frontier closed models far more densely than open-weight ones, so a naive "only publish what's verified" rule systematically deletes the open tier and manufactures a false picture of a two-horse race. v2 got this right with "—"; this version restores it.

**3. The AA Intelligence Index changed composition since June.** <cite index="11-1">v4.1.1 now combines nine evaluations: GDPval-AA v2, 𝜏³-Banking, Terminal-Bench v2.1, SciCode, Humanity's Last Exam, GPQA Diamond, CritPt, AA-Omniscience, and AA-LCR</cite>, weighted <cite index="10-1">across four categories at 25% each: agents, coding, general capability, and scientific reasoning</cite>. **SWE-bench is no longer a component** — Terminal-Bench replaced it.

| Marker | Meaning |
|:---:|:---|
| ✅ | **Primary source** — vendor pricing page, docs, or announcement |
| 🟡 | **Corroborated** — two or more independent trackers agree |
| ⚠️ | **Disputed or vendor-reported** — range shown where known |
| — | **No published score** |

> ⚠️ **Author disclosure:** compiled by Claude (Anthropic). Anthropic-favourable claims are cited to Anthropic's own docs (pricing) or independent evaluators (rankings). Where a metric would favour Anthropic but sources conflict, the conflict is shown.

---

## 📋 What Changed Since June 22, 2026

| Date | Release | Status |
|:---|:---|:---:|
| Jun 30 | **Claude Sonnet 5** — Anthropic | 🟡 |
| Jul 1 | **Claude Fable 5 restored** after June 12 export-control suspension | ✅ |
| Jul 9 | **GPT-5.6 GA** (Sol, Terra, Luna) — 1.05M context all tiers | 🟡 |
| Jul 16 | **Kimi K3** — 2.8T params, largest open-weight model ever released | 🟡 |
| Jul 21 | **Gemini 3.6 Flash** + **Gemini 3.5 Flash-Lite** | 🟡 |
| Jul 24 | **Claude Opus 5** — replaces Opus 4.8 at identical $5/$25 | 🟡 |
| Jul 26–27 | **Kimi K3 weights** published — custom licence, *not* MIT | 🟡 |
| Jul 30 | **OpenAI price cut** — Terra −20%, Luna −80%, Sol unchanged | ✅ |
| Aug 5 | **Muse Spark 1.2** + **Muse Code** — Meta | ⚠️ |
| Aug 13 | **Gemini 3.7 Flash** — Google | 🟡 |
| ~Aug 13–14 | **GLM-5.3**, **DeepSeek V4 Pro 0813**, **Qwen3.8 Max** | ⚠️ |
| — | **Claude Mythos 5** — limited availability (Project Glasswing) | ✅ |
| — | **Grok 4.5 / Grok 4.6** — xAI | ⚠️ |

**Structural shift.** <cite index="8-1">Meta has not shipped Llama 5, now forecast for 2027, and pivoted to its first closed frontier model, Muse Spark (April 2026), with no weights and no architecture paper — leaving Chinese labs (DeepSeek, Moonshot, Z.ai, Alibaba, MiniMax) as the effective owners of the open-weight frontier.</cite> 🟡

**And the open tier is no longer trailing.** <cite index="105-1">Kimi K3 (2.8T MoE) ranks #3 overall on the Artificial Analysis Intelligence Index — ahead of every proprietary model except Claude Fable 5 and GPT-5.6 Sol — and took #1 on the Frontend Code Arena. It is not a lone outlier: DeepSeek V4 Pro posts 80.6% on SWE-bench Verified (matching Gemini 3.1 Pro) and MiniMax M3 80.5%, while GLM-5.2 scores 62.1% on SWE-bench Pro against GPT-5.5's 58.6% — an MIT-licensed model you can self-host outscoring a $5/$30 US flagship on agentic coding.</cite> 🟡

---

## 🚨 THE CENTRAL FINDING — Scores Are Not Comparable Across Sources

Six trackers, same benchmark family, checked within days:

| Source | Version | Reported leader & score |
|:---|:---|:---|
| Artificial Analysis | v2.1 | <cite index="39-1">GPT-5.6 Sol (xhigh) 89.5%, then Claude Opus 5</cite> |
| vals.ai | v2.1 | <cite index="45-1">GPT-5.6 Sol 85.77%, Claude Opus 5 84.64%</cite> |
| CodingFleet | v2.1 | <cite index="40-1">GPT-5.6 Sol 88.8%, Grok 4.6 88.4%, Kimi K3 88.3%</cite> |
| BenchLM | v2.0 | <cite index="41-1">GPT-5.6 Sol 91.9%, Claude Mythos 5 88.0%</cite> |
| evals.report | v2.0 | <cite index="42-1">Claude Fable 5 84.3%</cite> |
| PricePerToken | unspecified | <cite index="38-1">GPT-5.6 Sol 65.9%, Claude Fable 5 62.9%</cite> |

**Same benchmark family spans 65.9% → 91.9%.** Three documented mechanisms:

**Version confusion.** <cite index="42-1">Terminal-Bench 2.1 is a different task set from 2.0, and most 2026 model cards self-report 2.0.</cite> <cite index="40-1">2.1 is harder; scores are not directly comparable across versions.</cite>

**Harness variation.** <cite index="40-1">Grok 4.6 scores 88.4% on v2.1 per Artificial Analysis, while xAI itself reported Terminal-Bench v3.0 instead, at 26.0%.</cite>

**Refusal-fallback accounting.** <cite index="45-1">Both Fable 5's and Opus 5's runs used Claude Opus 4.8 as a refusal fallback; counting Opus 5's nine affected passes as failures lowers it from 84.64% to 81.27%.</cite>

**And on SWE-bench, essentially nothing is independently verified:** <cite index="102-1">most SWE-bench Verified numbers are vendor self-reported; the llm-stats tracker lists 0 of 104 entries as independently verified.</cite> ⚠️

> 🔑 **Do not select a model on a leaderboard delta under ~5 points.** That is inside the cross-source noise band. Run 30–50 representative cases from your own work.

---

# 1️⃣ Composite Intelligence — AA Intelligence Index v4.1.1

| Rank | Model | Creator | Score | Type | Status |
|:---:|:---|:---|:---:|:---:|:---:|
| 1 | **Claude Opus 5** (Max Effort) ⚡ | Anthropic | **63** | Paid | ✅ |
| 1= | **Claude Opus 5** (Xhigh Effort) ⚡ | Anthropic | **63** | Paid | ✅ |
| 3 | **Claude Fable 5** (Max, Opus 4.8 fallback) ⚡ † | Anthropic | **62** | Paid | ✅ |
| 4 | **Grok 4.6** ⚡ | xAI | 60.9 | Paid | 🟡 |
| 5 | **GPT-5.6 Sol** ⚡ | OpenAI | 61 | Paid | ⚠️ |
| ~3–6 | **Kimi K3** ⚡ ★ | Moonshot | **57** | **Open** | 🟡 |
| — | **GLM-5.2** ⚡ ★ | Z.ai | **51** | **Open** | 🟡 |
| — | MiniMax M3 ⚡ ★ | MiniMax | 44 | Open | 🟡 |
| — | DeepSeek V4 Pro ⚡ ★ | DeepSeek | 44 | Open | 🟡 |

<cite index="11-1">Claude Opus 5 (Adaptive Reasoning, Max Effort) scores the highest with 63, followed by Claude Opus 5 (Xhigh Effort) at 63, and Claude Fable 5 (Max Effort, Opus 4.8 Fallback) at 62.</cite> ✅

<cite index="104-1">On the aggregate Artificial Analysis Intelligence Index, Kimi K3 scores 57, the top open-weight result, with GLM-5.2 next at 51.</cite> 🟡 · <cite index="108-1">On v4.1 (June 2026), GLM-5.2 scored 51 and ranked 5th overall, ahead of MiniMax M3 (44) and DeepSeek V4 Pro (44).</cite> 🟡

> † Fable 5's index entry explicitly carries "Opus 4.8 Fallback" — not a clean single-model result.
> ⚠️ Ranks mix snapshot dates; the open-weight figures come from a different pass than the top-3. Treat ordering between the two groups as indicative.

**AA Agentic Index:** <cite index="75-1">Claude Opus 5 took #1 at 55.3, ahead of GPT-5.6 Sol at 54.0 and Claude Fable 5 at 52.8.</cite> 🟡

---

# 2️⃣ Coding — Terminal-Bench v2.1

> <cite index="39-1">89 curated tasks across software engineering, system administration, data processing, model training, and security.</cite> <cite index="39-1">The 2.0 paper reported frontier models scoring under 65%.</cite>

| Model | Creator | Score | Type | Status |
|:---|:---|:---:|:---:|:---:|
| **GPT-5.6 Sol** (xhigh) ⚡ | OpenAI | **89.5%** (AA) / 88.8% / 85.77% | Paid | ⚠️ |
| **Grok 4.6** ⚡ | xAI | 88.4% | Paid | ⚠️ |
| **Kimi K3** ⚡ ★ | Moonshot | **88.3%** | **Open** | ⚠️ |
| **Claude Opus 5** ⚡ | Anthropic | 84.64% (81.27% w/o fallback) | Paid | 🟡 |
| **Claude Mythos 5** ⚡ | Anthropic | 88.0% (v2.0) | Paid | ⚠️ |
| **DeepSeek V4 Pro 0813** ⚡ ★ | DeepSeek | 87.9% | **Open** | ⚠️ |
| **GPT-5.6 Terra** ⚡ | OpenAI | 87.4% (v2.0) | Paid | ⚠️ |
| **Qwen3.8 Max** ⚡ ★ | Alibaba | 86.6% | **Open** | ⚠️ |
| **Gemini 3.7 Flash** ⚡ | Google | 85.8% | Paid | ⚠️ |
| **Claude Fable 5** ⚡ | Anthropic | 84.3% (v2.0) | Paid | ⚠️ |
| **Muse Spark 1.2** | Meta | 82.9% (Muse Code harness) | Paid | ⚠️ |
| **GLM-5.2** ⚡ ★ | Z.ai | **81%** | **Open** | 🟡 |
| **Muse Spark 1.1** | Meta | 80.0% | Paid | ⚠️ |

<cite index="45-1">On the hard split, Sol and Opus 5 are tied at 84.44%, with a sharp cliff to third place at 74.44%.</cite> 🟡

> 🔑 **The headline ranking is decided by medium-difficulty tasks.** On hard tasks the two leaders tie and everything else is 10 points back. And an open-weight model (Kimi K3, 88.3%) sits inside the top three.

---

# 3️⃣ SWE-bench Verified

> ⚠️ **Read the noise floor first:** <cite index="71-1">most scores are vendor-reported and vary ±2–3% by scaffold and configuration.</cite> The top cluster is narrower than the error bar.

## 💼 Paid / Closed

| Model | Creator | Score | Input $/1M | Output $/1M | Status |
|:---|:---|:---:|:---:|:---:|:---:|
| Claude Opus 5 ⚡ | Anthropic | **96.0%** (vendor) / **97.0%** (vals.ai) | $5.00 | $25.00 | ⚠️ |
| GPT-5.6 Sol ⚡ | OpenAI | **96.2%** | $5.00 | $30.00 | ⚠️ |
| Claude Mythos 5 ⚡ | Anthropic | 95.5% | $10.00 | $50.00 | 🟡 |
| Claude Fable 5 ⚡ | Anthropic | 95.0% | $10.00 | $50.00 | 🟡 |
| Gemini 3.1 Pro ⚡ | Google | 80.6% | $2.00 | $12.00 | 🟡 |
| Claude Opus 4.8 ⚡ | Anthropic | — | $5.00 | $25.00 | — |
| GPT-5.6 Terra ⚡ | OpenAI | — | $2.00 | $12.00 | — |
| Claude Sonnet 5 ⚡ | Anthropic | — | $2.00 | $10.00 | — |
| Gemini 3.7 Flash ⚡ | Google | — | $0.75 | $3.75 | — |
| Grok 4.6 ⚡ | xAI | — | — | — | — |
| Muse Spark 1.1 | Meta | — | $1.25 | $4.25 | ⚠️ |
| GPT-5.6 Luna ⚡ | OpenAI | — | $0.20 | $1.20 | — |
| Claude Haiku 4.5 ⚡ | Anthropic | — | $1.00 | $5.00 | — |

## 🆓 Free / Open Weights

| Model | Creator | Score | Input $/1M | Output $/1M | Licence | Status |
|:---|:---|:---:|:---:|:---:|:---|:---:|
| **Kimi K3** ⚡ ★ | Moonshot | **93.4%** (Vals AI) / 76.8% (Vellum) | $3.00 | $15.00 | Custom | ⚠️ |
| **DeepSeek V4 Pro-Max** ⚡ ★ | DeepSeek | **80.6%** | $0.435 | $0.87 | MIT | 🟡 |
| **MiniMax M3** ⚡ ★ | MiniMax | **80.5%** | ~$0.30 | ~$1.20 | Community | 🟡 |
| **DeepSeek V4 Flash-Max** ⚡ ★ | DeepSeek | **79.0%** | $0.14 | $0.28 | MIT | 🟡 |
| **Qwen3.6-27B** ⚡ ★ | Alibaba | **77.2%** / 68.9% | local | local | Apache 2.0 | ⚠️ |
| **Qwen3-Coder-Next** ⚡ ★ | Alibaba | **70.6%** (3B active) | — | — | Apache 2.0 | ⚠️ |
| **GLM-5.2** ⚡ ★ | Z.ai | 62.1% *(3rd-party; Z.ai published none)* | ~$1.40 | ~$4.40 | MIT | ⚠️ |
| Kimi K2.7 Code ⚡ ★ | Moonshot | — | $0.95 | $4.00 | Apache 2.0 | — |
| Kimi K2.6 ⚡ ★ | Moonshot | — | $0.95 | $4.00 | Apache 2.0 | — |
| Qwen3.8 Max ⚡ ★ | Alibaba | — | ~$2.00 | ~$6.00 | — | ⚠️ |
| Qwen3.7 Max ⚡ ★ | Alibaba | — | — | — | — | — |
| MiMo-V2.5 / Pro ⚡ ★ | Xiaomi | — | — | — | — | — |
| Hy3 ⚡ ★ | — | — | — | — | — | — |
| GLM-5.3 ⚡ ★ | Z.ai | — *(weights promised, not shipped)* | — | — | — | ⚠️ |
| Gemma 4 ⚡ ★ | Google | — | free (local) | free | **Apache 2.0** | — |
| Nemotron 3 ★ | NVIDIA | — | — | — | — | — |
| gpt-oss:20b ★ | OpenAI | — | free (local) | free | Apache 2.0 | — |
| Llama 4 Maverick / Scout ★ | Meta | — *(line effectively frozen)* | — | — | Llama | ⚠️ |

<cite index="102-1">On general SWE-bench Verified the top open model (DeepSeek V4 Pro, 80.6%) still trails the frontier (GPT-5.6 Sol 96.2%, Fable 5 95.0%, Kimi K3 93.4% on Vals AI), but at roughly a tenth of the output price, and on frontend UI the open leader is already on top.</cite> 🟡

---

# 4️⃣ SWE-bench Pro — ⚠️ Four Competing "Best" Scores

<cite index="66-1">Three numbers all claim to be the best SWE-bench Pro score: 59.1% (GPT-5.4 xHigh, Scale's standardized public set), 80.0% (Claude Fable 5, the llm-stats vendor aggregate), and 47.1% (Claude Opus 4.6, Scale's private commercial set). All three are real. The spread is scaffolding and data splits, and most pages quoting a score never say which one they mean.</cite> ⚠️

| Harness | Leader | Score |
|:---|:---|:---:|
| Vendor aggregate (CodingFleet) | Claude Mythos 5 / Fable 5 | 80.3% |
| Vendor aggregate (llm-stats) | Claude Fable 5 | 80.0% |
| **Scale SEAL standardized** | **Muse Spark 1.1** | **61.5%** |
| Scale standardized public set | GPT-5.4 (xHigh) | 59.1% |
| Scale private commercial set | Claude Opus 4.6 | 47.1% |

**Cross-source table** (vendor-reported unless noted): <cite index="70-1">Claude Mythos 5 80.3%, Claude Fable 5 80.3%, Claude Opus 5 79.2%, Qwen3.8 Max 67.7%, GPT-5.6 Sol 64.6%, Muse Spark 1.1 61.5%, Qwen3.7 Max 60.6%, GLM-5.1 58.4%.</cite> ⚠️

Plus: <cite index="105-1">GLM-5.2 scores 62.1% on SWE-bench Pro against GPT-5.5's 58.6%</cite> 🟡 and <cite index="111-1">Kimi K2.6 reaches ~58.6 on SWE-Bench Pro, tying top cloud models</cite> ⚠️

**Why the gap is structural:** <cite index="66-1">SWE-bench Pro is Scale AI's contamination-resistant benchmark — 1,865 tasks across 41 professional repositories, scored Pass@1, which the same models clearing 80–95% on Verified solve only ~59% of under standardized scaffolding.</cite>

> 🔑 When someone quotes a Pro number, ask **which harness**. The answer moves it by up to 33 points.

---

# 5️⃣ GPQA Diamond (Scientific Reasoning)

> <cite index="89-1">448 expert-written questions in biology, physics and chemistry; PhD experts reach 65% (74% discounting identified errors), skilled non-experts 34% despite unrestricted web access.</cite> Diamond = hardest 198.

| Model | Creator | Score | Type | Status |
|:---|:---|:---:|:---:|:---:|
| **Grok 4.6** (high) ⚡ | xAI | **94.9%** | Paid | ✅ |
| **Gemini 3.7 Flash** (high) ⚡ | Google | **94.5%** | Paid | ✅ |
| **GPT-5.6 Sol** (max) ⚡ | OpenAI | **94.1%** | Paid | ✅ |
| **Claude Opus 5 / Mythos 5** ⚡ | Anthropic | 94.1 | Paid | 🟡 |
| **Kimi K3** ⚡ ★ | Moonshot | **93.5** | **Open** | 🟡 |
| **GLM-5.2** ⚡ ★ | Z.ai | **91.2** | **Open** | 🟡 |
| Gemini 3.1 Pro ⚡ | Google | 94.1% (v2 figure) | Paid | ⚠️ |
| **Qwen3.6-27B** ⚡ ★ | Alibaba | **87.8** *(runs on one 24GB GPU)* | **Open/local** | ⚠️ |
| DeepSeek V4 Pro ⚡ ★ | DeepSeek | — | Open | — |
| MiniMax M3 ⚡ ★ | MiniMax | — | Open | — |
| Qwen3.8 Max ⚡ ★ | Alibaba | — | Open | — |
| Gemma 4 ⚡ ★ | Google | — | Open | — |

<cite index="89-1">Grok 4.6 (high) scores the highest on GPQA with 94.9%, followed by Gemini 3.7 Flash (high) at 94.5%, and GPT-5.6 Sol (max) at 94.1%.</cite> ✅

> 🔑 **Two things.** The top six are inside 1.4 points — **this benchmark is saturated**. And **Gemini 3.7 Flash at 94.5% costs $0.75/$3.75**, matching flagships costing 7–40x more. Open-weight Kimi K3 (93.5) and GLM-5.2 (91.2) are within 3.7 points of the leader.

---

# 6️⃣ HLE — Humanity's Last Exam

> <cite index="11-1">2,500 expert-vetted questions across mathematics, sciences and humanities.</cite> <cite index="90-1">Built by Scale AI with the Center for AI Safety to address benchmark saturation.</cite>

### ⚠️ The protocol split — why HLE numbers differ by 20 points

| Protocol | Frontier score |
|:---|:---:|
| **Closed-book, no tools** (official CAIS/Scale) | **mid-40s%** |
| **Tool-assisted / mixed aggregate** | **~55–65%** |

<cite index="84-1">By August 2026 the text-only (no-tools) frontier has reached the mid-40s percent on the official CAIS/Scale leaderboard.</cite> 🟡 BenchLM states the limit plainly: <cite index="87-1">a model with search, browsing, or code execution is not taking the same test as a closed-book model — BenchLM cannot make differently disclosed HLE configurations fully comparable.</cite> ⚠️

| Model | Creator | Score (tool-assisted) | Type | Status |
|:---|:---|:---:|:---:|:---:|
| **Claude Opus 5** ⚡ | Anthropic | **64.7%** | Paid | 🟡 |
| **Claude Mythos 5** ⚡ | Anthropic | 64.5% | Paid | 🟡 |
| **Muse Spark 1.1** | Meta | 62.1% | Paid | 🟡 |
| **Kimi K3** ⚡ ★ | Moonshot | **56** | **Open** | 🟡 |
| **Claude Fable 5** ⚡ | Anthropic | 55.5% | Paid | ⚠️ |
| **GLM-5.2** ⚡ ★ | Z.ai | **54.7** | **Open** | 🟡 |
| **GPT-5.6 Sol** ⚡ | OpenAI | 49.5% | Paid | ⚠️ |
| Gemini 3.1 Pro Preview ⚡ | Google | 46.44 *(closed-book)* | Paid | 🟡 |
| GPT-5.4 Pro ⚡ | OpenAI | 44.32 *(closed-book)* | Paid | 🟡 |
| Muse Spark | Meta | 40.56 *(closed-book)* | Paid | 🟡 |
| Claude Opus 4.6 (Thinking) ⚡ | Anthropic | 34.44 *(closed-book)* | Paid | 🟡 |
| Kimi K2.5 ⚡ ★ | Moonshot | 24.37 *(closed-book)* | Open | 🟡 |
| GLM 4.5 ⚡ ★ | Z.ai | 8.32 *(closed-book)* | Open | 🟡 |
| Mistral Medium 3 | Mistral | 4.52 *(closed-book)* | Paid | 🟡 |
| Nova Pro | Amazon | 4.40 *(closed-book)* | Paid | 🟡 |

**Reasoning effort dominates here:** <cite index="84-1">reasoning-configured models occupy the entire top of the text-only board, and the same base model in a low-effort configuration scores materially lower — a gap far wider than the 1–2 points on MMLU-Pro or 3–4 on GPQA-Diamond.</cite>

### 🚨 Validity warning

<cite index="88-1">An independent investigation by FutureHouse, published in July 2025, suggested that around 30% of the HLE answers for text-only chemistry and biology questions could be incorrect; the benchmark's team partially replicated the findings and said they hope to institute a continuous revisions process.</cite> ⚠️

**If a third of the answer key in two major subjects is wrong, a 5-point HLE gap carries almost no information.**

---

# 7️⃣ AIME 2026 (Math) — ❌ Not Verified

v2 published a full AIME 2026 table. **It could not be reproduced.** Artificial Analysis tracks **AIME 2025**, not 2026; one dedicated 2026 tracker shows no models scored. <cite index="93-1">MathArena is the credible primary source — it publishes a leaderboard per competition and runs each model 4 times per problem, computing average score.</cite>

One local-model figure surfaced: <cite index="113-1">Gemma 4 26B-A4B reports 89% AIME 2026 at ~15 GB RAM.</cite> ⚠️ single-sourced.

**Treat v2's AIME 2026 table as suspect.**

---

# 8️⃣ Arena Elo (Human Preference)

Arena's own changelog ✅ confirms the roster: <cite index="78-1">claude-opus-5-high and claude-opus-5-max added to Text, Vision, Document and Code Arena; gpt-5.6-sol-xhigh, terra-xhigh and luna-xhigh added to Code, Document, Vision and Text Arena; Claude Opus 5 (Max) and (High) added to Agent Arena; deepseek-v4-flash-high added to Code Arena.</cite>

| Board | Leader | Elo | Status |
|:---|:---|:---:|:---:|
| **Text** | **Claude Fable 5** | ~1508–1525 | ⚠️ |
| Text #14 | GPT-5.6 Sol | 1482.8 | 🟡 |
| **Coding** | Claude Fable 5 | 1553 | 🟡 |
| **Math** | Claude Fable 5 | 1543 | 🟡 |
| **Vision** | Claude Fable 5 | 1334 | 🟡 |
| **Agent** | **Claude Opus 5** (Kimi K3 third) | — | 🟡 |
| **Frontend Code** | **Kimi K3** ★ — *first open model to lead* | — | 🟡 |
| **Best open-weight** | GLM-5.1 | 1475 | 🟡 |

<cite index="75-1">On the August 1 cutoff, GPT-5.6 Sol sits #14 on Arena text at 1482.8, while Claude Fable 5 leads at 1508.6.</cite> · <cite index="80-1">Arena re-baselined Fable 5 on July 12 to count only votes cast since its July 1 restoration.</cite> · <cite index="81-1">The highest-rated openly licensed model is glm-5.1 at 1475, trailing claude-opus-4-6-thinking by 37 points.</cite> · <cite index="102-1">Kimi K3 is #1 on the Arena.ai Frontend Code Arena, the first open model to lead frontend coding, ahead of Claude Fable 5.</cite>

> ⚠️ <cite index="74-1">Treat any Elo gap under 30 points as procurement-equivalent noise; 60% of models within 30 Elo swap ranks within a single quarter.</cite> <cite index="74-1">Methodology updates such as the January 2026 rebrand caused 30+ Elo shifts unrelated to model quality.</cite> **The entire Text Arena top cluster sits inside that band.**

---

# 9️⃣ 🆕 Local / Self-Hostable Tier

New section — v2 didn't cover this, and it's where the practical decisions live for privacy-routed work.

### ⚠️ "Open weights" ≠ runnable

<cite index="105-1">The leading open models are trillion-parameter MoEs — GLM-5.2 needs ~1TB VRAM in BF16 (~8x H200 at FP8), Kimi K3 needs 64+ accelerators. The ecosystem has bifurcated into giant open MoEs and genuinely small models (Qwen 3.6 27B, Gemma 4, Nemotron 3 Nano Omni) that run on one GPU or a phone, with little in between.</cite> 🟡

### Actually runnable, by hardware

| Model | Footprint (Q4) | Context | Benchmark | Status |
|:---|:---:|:---:|:---|:---:|
| **Qwen3.6-27B** ★ | ~17 GB | 262K (→1M) | **77.2% SWE-bench V**, 84% MMLU, 87.8 GPQA | ⚠️ |
| **Qwen3-Coder 30B** ★ | ~18 GB | 256K | MoE — small-model speed | 🟡 |
| **gpt-oss:20b** ★ | ~16 GB | — | fits 16GB unified comfortably | 🟡 |
| **Gemma 4 26B-A4B** ★ | ~15 GB | — | 89% AIME 2026 | ⚠️ |
| **Gemma 4 12B** ★ | ~16 GB unified | 256K | strongest multimodal local | 🟡 |
| **glm-4.7-flash** ★ | ~19 GB | 198K | "strongest in the 30B class" | ⚠️ |
| **Qwen 3.5 9B** ★ | <10 GB | — | **— no published benchmarks** | — |
| Qwen2.5-Coder 7B ★ | ~5 GB | — | 88% HumanEval | 🟡 |
| Phi-4-mini | ~2.5 GB | — | 74.4% HumanEval | 🟡 |
| Gemma 4 E2B ★ | ~2 GB | — | — | — |

<cite index="115-1">For a single 24 GB GPU, Qwen3.6 27B is the best all-rounder — it scores 77.2% on SWE-bench Verified, the highest verified coding result of the models that run on consumer hardware.</cite> 🟡

<cite index="111-1">The honest truth: a top local coder rivals mid-tier cloud assistants; the very best cloud models still lead on the hardest, multi-file tasks.</cite>

**On Qwen 3.5 9B specifically** — the model in your Ollama config: <cite index="117-1">Qwen 3.5 9B is the newest sub-10B model, with multimodal input included.</cite> But <cite index="117-1">the newest models (Gemma 4 E-series, Qwen 3.5, Ministral 3) do not yet have like-for-like MMLU/HumanEval numbers published, so they appear in rankings without benchmark rows rather than with invented ones.</cite> ⚠️ **No published benchmarks exist for it.** That's a real gap in the roadmap's plan-model choice — not a knock on the model, but it means the selection rests on hands-on feel rather than evidence.

⚠️ **Ollama cloud-only tags:** <cite index="112-1">verified cloud-only on August 8, 2026: glm-5.1, minimax-m2.7, kimi-k2.6, deepseek-v4-flash, nemotron-3-super, qwen3-coder:480b-cloud. qwen3.5 and gemma4 publish a :cloud tag alongside their local ones, so check the tag before you pull.</cite> ⚠️ **Pulling a `:cloud` tag does not give you local inference** — directly relevant to any privacy-routing guarantee.

**Licences:** <cite index="104-1">Google moved Gemma 4 to plain Apache 2.0, dropping the separate agreement Gemma 3 required, and Moonshot shipped Kimi K3 under a custom licence that most people assumed was MIT and is not. Qwen 3.6 and Gemma 4 under Apache 2.0; DeepSeek V4 and GLM-5.2 under MIT.</cite> 🟡

---

# 💰 Complete Pricing Table

### Anthropic — ✅ PRIMARY (platform.claude.com/docs, Aug 17, 2026)

| Model | Input | 5m Cache Write | 1h Cache Write | Cache Hit | Output |
|:---|:---:|:---:|:---:|:---:|:---:|
| Claude Fable 5 | $10 | $12.50 | $20 | $1.00 | $50 |
| Claude Mythos 5 *(limited)* | $10 | $12.50 | $20 | $1.00 | $50 |
| Claude Opus 5 | $5 | $6.25 | $10 | $0.50 | $25 |
| Claude Opus 4.8 / 4.7 / 4.6 / 4.5 | $5 | $6.25 | $10 | $0.50 | $25 |
| **Claude Sonnet 5** | **$2** | $2.50 | $4 | $0.20 | **$10** |
| Claude Sonnet 4.6 / 4.5 | $3 | $3.75 | $6 | $0.30 | $15 |
| Claude Haiku 4.5 | $1 | $1.25 | $2 | $0.10 | $5 |

**🔑 Correction to widespread reporting:** <cite index="28-1">the $2/$10 pricing for Claude Sonnet 5, announced as introductory through August 31, 2026, is now the standard price. The previously scheduled increase to $3/$15 on September 1, 2026 will not occur.</cite> ✅

**🔑 Tokenizer caveat:** <cite index="28-1">Claude 4.7 and later use a newer tokenizer producing approximately 30% more tokens for the same text. Sonnet 4.6 and earlier use the previous tokenizer.</cite> ✅ — **every cross-vendor per-token comparison in this document understates Claude's real bill by roughly 30%.**

Other mechanics: <cite index="28-1">Batch API −50%; cache hits 0.1x input; Claude 4.6+ include the full 1M context at standard pricing; `inference_geo: "us"` applies 1.1x; Fast mode (Opus 5 / 4.8) $10/$50, unavailable with Batch.</cite> ✅

### OpenAI

| Model | Input | Output | Long-context meter | Status |
|:---|:---:|:---:|:---:|:---:|
| GPT-5.5 Pro | $30 | $180 | — | 🟡 |
| GPT-5.6 Sol | $5 | $30 | $10 / $45 | 🟡 |
| GPT-5.5 | $5 | $30 | $10 / $45 | 🟡 |
| GPT-5.4 | $2.50 | $15 | $5 / $22.50 | 🟡 |
| **GPT-5.6 Terra** | **$2** | **$12** | $4 / $18 | ✅ |
| GPT-5.4 mini | $0.75 | $4.50 | — | 🟡 |
| **GPT-5.6 Luna** | **$0.20** | **$1.20** | $0.40 / $1.80 | ✅ |

<cite index="29-1">Starting July 30, API pricing is $2/$12 per million tokens for Terra, and $0.20/$1.20 for Luna.</cite> ✅ <cite index="36-1">The GPT-5.6 family went GA July 9, 2026 with a 1.05M-token context window on all three tiers.</cite> 🟡

### Google

| Model | Input | Output | Note | Status |
|:---|:---:|:---:|:---|:---:|
| Gemini 3.1 Pro | $2 | $12 | ≤200K; $4/$18 above | 🟡 |
| **Gemini 3.7 Flash** | **$0.75** | **$3.75** | ⏰ **doubles Jan 1, 2027** | 🟡 |
| Gemini 3.6 Flash | $0.75–1.50 | $3.75–7.50 | ⚠️ sources conflict | ⚠️ |
| Gemini 3.5 Flash-Lite | $0.30 | $2.50 | | 🟡 |
| Gemini 2.5 Flash-Lite | $0.10 | $0.40 | current floor | 🟡 |

### Open weights (hosted API rates)

| Model | Creator | Input | Output | Params / Context | Licence | Status |
|:---|:---|:---:|:---:|:---|:---|:---:|
| Kimi K3 ★ | Moonshot | $3.00 | $15.00 | 2.8T / 1.05M | **Custom** | 🟡 |
| Qwen3.8 Max ★ | Alibaba | ~$2.00 | ~$6.00 | — | — | ⚠️ |
| GLM-5.2 ★ | Z.ai | ~$1.40 | ~$4.40 | 744–753B / 1M | MIT | ⚠️ |
| Muse Spark 1.1 | Meta | $1.25 | $4.25 | closed weights | — | ⚠️ |
| Kimi K2.7 Code ★ | Moonshot | $0.95 | $4.00 | — | Apache 2.0 | 🟡 |
| Kimi K2.6 ★ | Moonshot | $0.95 | $4.00 | ~1T / 256K | Apache 2.0 | 🟡 |
| DeepSeek V4 Pro ★ | DeepSeek | $0.435 | $0.87 | 1.6T / 49B active / 1M | MIT | 🟡 |
| MiniMax M3 ★ | MiniMax | ~$0.30 | ~$1.20 | — / 1M | Community | ⚠️ |
| DeepSeek V4 Flash ★ | DeepSeek | $0.14 | $0.28 | 284B / 13B active / 1M | MIT | 🟡 |
| GLM-5.3 ★ | Z.ai | — | — | weights promised | — | ⚠️ |
| Gemma 4 ★ | Google | free (local) | free | — | **Apache 2.0** | 🟡 |
| gpt-oss:20b ★ | OpenAI | free (local) | free | 20B | Apache 2.0 | 🟡 |
| Qwen3.6-27B ★ | Alibaba | free (local) | free | 27B dense / 262K | Apache 2.0 | 🟡 |

<cite index="56-1">On a blended cost-per-task basis, Artificial Analysis puts K3 at $0.94 per task and DeepSeek V4 Pro at $0.04.</cite> 🟡 — **a 23x spread**, which matters more than the per-token headline.

---

# 📉 Corrections to the June 2026 (v2) Report

| # | v2 claim | August 2026 status |
|:---:|:---|:---|
| 1 | GLM-5.2 at $0.45 / $1.80 | ⚠️ Now **~$1.40 / ~$4.40** — roughly 3x higher |
| 2 | DeepSeek V4 Pro at $0.23 / $1.10 | 🟡 Now **$0.435 / $0.87** |
| 3 | DeepSeek V4 Flash at $0.09 / $0.18 | 🟡 Now **$0.14 / $0.28** |
| 4 | Claude Fable 5 "marked unavailable" | ✅ **Restored July 1, 2026** |
| 5 | Claude Opus 4.8 as flagship | ✅ Superseded by **Opus 5** at identical $5/$25 |
| 6 | GPT-5.5 as OpenAI flagship | 🟡 Superseded by **GPT-5.6 Sol** |
| 7 | SWE-bench as headline coding measure | ✅ **Removed from the AA Index**; Terminal-Bench replaced it |
| 8 | AIME 2026 table | ❌ **Could not be reproduced.** Treat as suspect |
| 9 | Blended = (3×input + output)/4 | ⚠️ <cite index="55-1">Artificial Analysis prices on a blended 7:2:1 cache/input/output basis.</cite> Ignoring cache misstates agentic cost |
| 10 | Per-token cross-vendor comparison | ⚠️ **Broken by the Claude 4.7+ tokenizer change** ✅ |
| 11 | Llama 4 Maverick / Scout as Meta's open line | 🟡 Meta **exited the open frontier**; Llama 5 forecast 2027 |
| 12 | Qwen3.5 9B at $0.10 / $0.15 with 78.6% GPQA | ⚠️ **No published benchmarks found.** GPQA figure not reproducible |
| 13 | Gemma 4 31B "Free" | 🟡 Gemma 4 now **plain Apache 2.0**; sizes E2B–26B |

---

# 🏅 Key Takeaways

| Category | 🥇 Best Paid | 🥈 Best Open/Free | Status |
|:---|:---|:---|:---:|
| **Composite (AA Index)** | Claude Opus 5, 63 | **Kimi K3, 57** | ✅ / 🟡 |
| **Terminal-Bench 2.1** | GPT-5.6 Sol, 89.5% | **Kimi K3, 88.3%** | ⚠️ |
| **Terminal-Bench hard split** | **Tie — Sol & Opus 5, 84.44%** | — | 🟡 |
| **SWE-bench Verified** | *No verifiable #1* (top 4 within 1.0 pt) | **Kimi K3 93.4%** / DeepSeek V4 Pro 80.6% | ⚠️ |
| **SWE-bench Pro (SEAL)** | Muse Spark 1.1, 61.5% | GLM-5.2, 62.1% | 🟡 |
| **GPQA Diamond** | Grok 4.6, 94.9% | **Kimi K3, 93.5** | ✅ / 🟡 |
| **HLE (tool-assisted)** | Claude Opus 5, 64.7% | **Kimi K3, 56** | 🟡 |
| **Arena Elo (text)** | Claude Fable 5, ~1508–1525 | GLM-5.1, 1475 | ⚠️ |
| **Arena Frontend Code** | — | **Kimi K3 — first open model to lead** | 🟡 |
| **AIME 2026** | ❌ not verified | ❌ not verified | ❌ |

### Best value

| Category | Winner | Basis |
|:---|:---|:---|
| 🏆 **Intelligence per dollar** | **Gemini 3.7 Flash** | 94.5% GPQA at $0.75/$3.75 |
| 🏆 **Cheapest frontier-tier** | **GPT-5.6 Luna** | $0.20/$1.20 |
| 🏆 **Open-weight cost leader** | **DeepSeek V4 Pro** | $0.04/task blended vs K3's $0.94 |
| 🏆 **Hosted price floor** | **DeepSeek V4 Flash** | $0.14/$0.28 |
| 🏆 **Best open all-rounder** | **Kimi K3** | #3 overall AA Index; #1 Frontend Code Arena |
| 🏆 **Best self-hostable (datacentre)** | **GLM-5.2** | MIT, 1M context, 81% Terminal-Bench |
| 🏆 **Best local (24GB GPU)** | **Qwen3.6-27B** | 77.2% SWE-bench V, Apache 2.0, ~17GB |
| 🏆 **Best local (16GB unified)** | **gpt-oss:20b / Gemma 4 12B** | fits Apple Silicon 16GB |
| 🏆 **Most permissive licence** | **Gemma 4 / Qwen 3.6** | plain Apache 2.0 |

### Three conclusions

1. **The open tier reached the frontier.** Kimi K3 is #3 on the AA composite ahead of every proprietary model except two, and leads Frontend Code Arena outright. GLM-5.2 outscores GPT-5.5 on SWE-bench Pro at a fraction of the price. Any 2026 comparison that reads as Claude-vs-GPT is missing the actual story.
2. **Four of the six benchmark leaders are inside their own measurement error.**
3. **Routing beats model choice on cost.** Luna at $0.20/$1.20 and DeepSeek V4 Flash at $0.14/$0.28 against Fable 5 at $10/$50 is a 50–170x spread.

---

# 🔧 Relevance to a Cursor + OpenCode Stack

| Go model | Go tier | Direct API | Evidence |
|:---|:---:|:---:|:---|
| `glm-5.2` | ✅ $60/mo | ~$1.40/~$4.40 | 81% TB2.1, 91.2 GPQA, 62.1% SWE Pro, MIT |
| `minimax-m3` | ✅ $60/mo | ~$0.30/~$1.20 | 80.5% SWE-bench V |
| `qwen3.7-max` | ✅ $60/mo | — | 60.6% SWE Pro |
| `kimi-k3` | ⚠️ $15/mo | $3.00/$15.00 | **Best open all-rounder** — 88.3% TB2.1, 93.5 GPQA |
| `deepseek-v4-pro` | ⚠️ $15/mo | $0.435/$0.87 | **Cheapest per task** — 80.6% SWE-bench V |
| `glm-5.3` | ⚠️ $15/mo | — | Weights promised, not shipped |

**Three observations:**

1. **GLM-5.2 is well-supported as the Go default** — full tier, MIT-licensed, 81% Terminal-Bench, 91.2 GPQA. The evidence backs the existing choice.
2. **DeepSeek V4 Pro is cheapest on direct API but reduced-tier on Go.** If it becomes the primary build model, OpenRouter or direct API beats Go.
3. **Kimi K3 is the strongest open model but the worst Go value** — ~490 requests/month on the reduced tier, at $3/$15 direct. Reserve it for the hardest 10%.

**On the local plan model:** Qwen 3.5 9B has **no published benchmarks** ⚠️. If evidence matters for the choice, **Qwen3.6-27B** (77.2% SWE-bench Verified, Apache 2.0) is the benchmarked alternative — but at ~17GB Q4 it is tight on a 16GB Mac Mini. **gpt-oss:20b** or **Gemma 4 12B** are the documented 16GB-unified-memory fits. ⚠️ And check Ollama tags: several models publish `:cloud` tags that do **not** run locally — which would silently break a privacy-routing guarantee.

---

# 📝 Methodology & Sources

### Source hierarchy

1. **Vendor primary** — pricing pages, docs, announcements
2. **Single-evaluator independent** — Artificial Analysis, vals.ai, Scale SEAL
3. **Multi-source aggregators** — used where two independent trackers agree
4. **Rejected** — figures appearing in one aggregator with no primary trace

### Sources

| Source | Data used | Tier |
|:---|:---|:---:|
| platform.claude.com/docs | Full Anthropic pricing, tokenizer note, cache/batch/fast-mode | ✅ 1 |
| openai.com (GPT-5.6 announcement) | Terra/Luna July 30 rates | ✅ 1 |
| artificialanalysis.ai | AA Index v4.1.1, Terminal-Bench v2.1, GPQA Diamond | 2 |
| vals.ai | Terminal-Bench splits, fallback caveat, Kimi K3 SWE-bench | 2 |
| labs.scale.com (SEAL) | SWE-bench Pro standardized/private sets | 2 |
| tbench.ai, matharena.ai | Benchmark provenance | 2 |
| arena.ai changelog | Model roster confirmation | ✅ 1 |
| BenchLM, evals.report, CodingFleet, PricePerToken, llm-stats, DataLearner, Vellum, swfte | Divergence analysis, open-weight scores | 3 |
| MarkTechPost, ComputingForGeeks, morphllm, localaimaster, atomic.chat | Open-weight & local tier, licences, hardware | 3 |

### Caveats

1. **Harness dependence is the dominant error source** in every coding score here.
2. <cite index="102-1">The llm-stats tracker lists 0 of 104 SWE-bench Verified entries as independently verified.</cite>
3. **Refusal fallbacks** materially alter Anthropic scores — check for Opus 4.8 substitution.
4. **The Claude 4.7+ tokenizer change (~30% more tokens)** invalidates naive per-token comparison. ✅
5. **Blended-price formulas ignoring cache** misstate agentic cost.
6. **Scheduled increase:** Gemini 3.7/3.6 Flash double January 1, 2027.
7. **Open weights ≠ self-hostable** at trillion-parameter scale.
8. **Licences differ per checkpoint** — Kimi K3 is custom, not MIT, despite common assumption.

### ❌ Still unverified

AIME 2026 (MathArena is the primary source; not retrieved) · per-model context windows beyond those cited · Grok 4.5/4.6 pricing · Qwen3.8 Max pricing (single-sourced ~$2/$6) · Muse Spark pricing (single-sourced $1.25/$4.25) · Nemotron 3, Mistral current line, Amazon Nova current line · Qwen 3.5 9B benchmarks (**none published**).

---

> **Legend:** ⚡ reasoning · ★ open weights · ✅ primary · 🟡 corroborated · ⚠️ disputed/vendor-reported · — no published score
> **Last Updated:** August 17, 2026
> **Next Update:** re-verify before any procurement decision — pricing moved three times in the eight weeks covered.