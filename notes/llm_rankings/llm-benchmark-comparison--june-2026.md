# 🏆 LLM Benchmark Comparison — June 2026

> **Last Updated:** June 18, 2026  
> **Sources:** Artificial Analysis (artificialanalysis.ai), Scale AI SEAL Leaderboard, LMSys Chatbot Arena, PricePerToken, llm-stats.com, and official vendor reports (OpenAI, Anthropic, Google, DeepSeek, Meta, Alibaba, Z AI)

---

## 📊 Benchmarks Covered

| # | Benchmark | Category | Description |
|:---:|:---|:---|:---|
| 1 | **SWE-bench Verified** | Coding | 500 real-world GitHub issues; models must produce patches that pass unit tests. |
| 2 | **SWE-bench Pro** | Coding | Scale AI's contamination-resistant coding benchmark with 1,865 fresh tasks. |
| 3 | **GPQA Diamond** | Scientific Reasoning | 198 graduate-level "Google-proof" questions in physics, chemistry, biology. |
| 4 | **HLE (Humanity's Last Exam)** | Frontier Reasoning | 3,000 extremely difficult questions across all academic domains. |
| 5 | **AIME 2026** | Math | American Invitational Mathematics Examination — 15 questions, 0-15 score. |
| 6 | **Arena Elo** | Community Preference | LMSys Chatbot Arena blind pairwise human preference ranking. |
| 7 | **Context Window** | Long-Context | Maximum token capacity the model can process in one prompt. |

---

## 💰 Pricing Legend

| Pricing Tier | Price per 1M Input Tokens | Price per 1M Output Tokens |
|:---|:---|:---|
| _All prices in USD, accessed June 18, 2026._ | Base input rate | Base output rate |

---

# 1️⃣ SWE-bench Verified (Coding)

> **What it tests:** Real-world software engineering — models fix actual GitHub issues and submit patches that must pass unit tests.  
> **Scale:** 500 tasks from popular Python repositories.  
> **Important:** OpenAI deprecated SWE-bench Verified from official reporting in Feb 2026, citing concerns about contamination. Anthropic and others continue reporting.

---

## 🏆 SWE-bench Verified — Top Performers

| Rank | Model | Score | Input $/1M | Output $/1M | Type |
|:---:|:---|:---:|:---:|:---:|:---:|
| 1 | **Claude Fable 5** (Max Effort) ⚡ | **95.0%** | $3.00 | $15.00 | Paid |
| 2 | **Claude Opus 4.8** (Max) ⚡ | **87.6%** | $5.00 | $25.00 | Paid |
| 3 | **Claude Opus 4.7** (Max) ⚡ | **85.2%** | $5.00 | $25.00 | Paid |
| 4 | **GPT-5.5** (xhigh) ⚡ | **83.4%** | $3.75 | $15.00 | Paid |
| 5 | **GPT-5.3 Codex** (xhigh) ⚡ | **80.2%** | $2.50 | $10.00 | Paid |
| 6 | **DeepSeek V4 Pro** (Max) ⚡ ★ | **80.6%** | $0.23 | $1.10 | Free / Open |
| 7 | **Qwen3.7 Max** ⚡ ★ | **79.8%** | $0.80 | $3.20 | Free / Open |
| 8 | **MiniMax-M3** ⚡ ★ | **78.4%** | $0.20 | $0.80 | Free / Open |

---

## 💼 SWE-bench Verified — Paid Models (Detailed)

| Model | Creator | Score | Input $/1M | Output $/1M | Context |
|:---|:---|:---:|:---:|:---:|:---:|
| Claude Fable 5 (Max Effort) ⚡ | Anthropic | **95.0%** | $3.00 | $15.00 | 1M |
| Claude Opus 4.8 (Max) ⚡ | Anthropic | **87.6%** | $5.00 | $25.00 | 1M |
| Claude Opus 4.7 (Max) ⚡ | Anthropic | **85.2%** | $5.00 | $25.00 | 1M |
| GPT-5.5 (xhigh) ⚡ | OpenAI | **83.4%** | $3.75 | $15.00 | 922k |
| GPT-5.3 Codex (xhigh) ⚡ | OpenAI | **80.2%** | $2.50 | $10.00 | 400k |
| Claude Sonnet 4.6 (Max) ⚡ | Anthropic | **78.1%** | $3.00 | $15.00 | 1M |
| Gemini 3.5 Flash ⚡ | Google | **74.3%** | $0.50 | $2.00 | 1M |
| GPT-5.4 mini (xhigh) ⚡ | OpenAI | **64.1%** | $0.50 | $2.00 | 400k |
| Gemini 3.1 Pro ⚡ | Google | **56.4%** | $1.25 | $5.00 | 1M |
| Gemini 2.5 Pro | Google | **46.0%** | $1.25 | $5.00 | 1M |

---

## 🆓 SWE-bench Verified — Free / Open Weights

| Model | Creator | Score | Input $/1M | Output $/1M | Context |
|:---|:---|:---:|:---:|:---:|:---:|
| DeepSeek V4 Pro (Max) ⚡ ★ | DeepSeek | **80.6%** | $0.23 | $1.10 | 1M |
| Qwen3.7 Max ⚡ ★ | Alibaba | **79.8%** | $0.80 | $3.20 | 1M |
| MiniMax-M3 ⚡ ★ | MiniMax | **78.4%** | $0.20 | $0.80 | 1M |
| GLM-5.2 (max) ⚡ ★ | Z AI | **76.0%** | $0.45 | $1.80 | 1M |
| Kimi K2.7 Code ⚡ ★ | Kimi | **72.1%** | $0.60 | $2.40 | 256k |
| DeepSeek V4 Flash (Max) ⚡ ★ | DeepSeek | **70.1%** | $0.07 | $0.50 | 1M |
| Qwen3.6 Plus ⚡ ★ | Alibaba | **60.3%** | $0.40 | $1.60 | 1M |
| MiMo-V2.5-Pro ⚡ ★ | Xiaomi | **58.7%** | $0.20 | $0.80 | 1M |
| Nemotron 3 Ultra ⚡ ★ | NVIDIA | **52.0%** | $0.50 | $2.00 | 262k |
| Gemma 4 31B ⚡ ★ | Google | **38.5%** | Free | Free | 256k |
| Llama 4 Maverick ★ | Meta | **28.2%** | $0.30 | $1.20 | 1M |

---

## 📋 SWE-bench Verified — Methodology & Notes

- **SWE-bench Verified** contains 500 hand-validated GitHub issues with unit tests.
- **OpenAI deprecated** this benchmark in Feb 2026, citing training data contamination.
- **Anthropic** continues reporting independently; scores cross-referenced with Artificial Analysis.
- **DeepSWE** (third-party audit project) released independent evals confirming Claude's lead.
- **Scaffold matters:** Results use each model's recommended agentic scaffold (e.g., Claude Code for Anthropic, Codex CLI for OpenAI).

---

# 2️⃣ SWE-bench Pro (Coding — Contamination-Resistant)

> **What it tests:** Identical task format to SWE-bench but with **1,865 freshly created tasks** (post-training-cutoff for all major models). Developed by Scale AI's SEAL team specifically to prevent benchmark leakage.  
> **Two scoring columns:**
> - **Score (SEAL):** Scale AI's independently verified results using standardized scaffold.
> - **Score (Vendor):** Self-reported results from model creators, sometimes using optimized scaffolds.

---

## 🏆 SWE-bench Pro — Top Performers (SEAL-Verified)

| Rank | Model | Score (SEAL) | Input $/1M | Output $/1M | Type |
|:---:|:---|:---:|:---:|:---:|:---:|
| 1 | **GPT-5.4** (xHigh, Aug 2025) ⚡ | **59.1%** | $5.00 | $20.00 | Paid |
| 2 | **Claude Fable 5** (Jan 2026) ⚡ | **55.0%** | $3.00 | $15.00 | Paid |
| 3 | **Claude Opus 4.8** (Jun 2026) ⚡ | **53.0%** | $5.00 | $25.00 | Paid |
| 4 | **GLM-5.1** (Jan 2026) ⚡ ★ | **52.8%** | $0.45 | $1.80 | Free / Open |
| 5 | **Qwen3.7 Max** (May 2026) ⚡ ★ | **52.6%** | $0.80 | $3.20 | Free / Open |
| 6 | **GPT-5.3 Codex** (Sep 2025) ⚡ | **51.0%** | $2.50 | $10.00 | Paid |
| 7 | **DeepSeek V4 Pro** (Mar 2026) ⚡ ★ | **50.6%** | $0.23 | $1.10 | Free / Open |

---

## 💼 SWE-bench Pro — Paid Models (Detailed)

| Model | Creator | Score (SEAL) | Score (Vendor) | Input $/1M | Output $/1M | Context |
|:---|:---|:---:|:---:|:---:|:---:|:---:|
| GPT-5.4 (xHigh) ⚡ | OpenAI | **59.1%** | 68.2% | $5.00 | $20.00 | 1M |
| Claude Fable 5 ⚡ | Anthropic | **55.0%** | 72.0% | $3.00 | $15.00 | 1M |
| Claude Opus 4.8 ⚡ | Anthropic | **53.0%** | 78.0% | $5.00 | $25.00 | 1M |
| GPT-5.3 Codex ⚡ | OpenAI | **51.0%** | 63.0% | $2.50 | $10.00 | 400k |
| Gemini 3.1 Pro ⚡ | Google | **44.1%** | — | $1.25 | $5.00 | 1M |
| GPT-5.5 (xhigh) ⚡ | OpenAI | **40.2%** | 75.0% | $3.75 | $15.00 | 922k |
| Claude Sonnet 4.6 ⚡ | Anthropic | **38.9%** | 62.0% | $3.00 | $15.00 | 1M |
| Gemini 3.5 Flash ⚡ | Google | **32.0%** | — | $0.50 | $2.00 | 1M |
| Grok 4.3 (high) ⚡ | xAI | **30.1%** | — | $0.50 | $2.00 | 1M |
| Nova 2.0 Pro ⚡ | Amazon | **20.0%** | — | $2.00 | $8.00 | 256k |

---

## 🆓 SWE-bench Pro — Free / Open Weights

| Model | Creator | Score (SEAL) | Score (Vendor) | Input $/1M | Output $/1M | Context |
|:---|:---|:---:|:---:|:---:|:---:|:---:|
| GLM-5.1 ⚡ ★ | Z AI | **52.8%** | 58.4% | $0.45 | $1.80 | 200k |
| Qwen3.7 Max ⚡ ★ | Alibaba | **52.6%** | 58.7% | $0.80 | $3.20 | 1M |
| DeepSeek V4 Pro ⚡ ★ | DeepSeek | **50.6%** | 62.0% | $0.23 | $1.10 | 1M |
| MiniMax-M3 ⚡ ★ | MiniMax | **48.1%** | — | $0.20 | $0.80 | 1M |
| Kimi K2.7 Code ⚡ ★ | Kimi | **47.2%** | — | $0.60 | $2.40 | 256k |
| DeepSeek V4 Flash ⚡ ★ | DeepSeek | **43.0%** | 52.0% | $0.07 | $0.50 | 1M |
| Qwen3.6 Plus ⚡ ★ | Alibaba | **38.4%** | — | $0.40 | $1.60 | 1M |
| MiMo-V2.5-Pro ⚡ ★ | Xiaomi | **36.5%** | — | $0.20 | $0.80 | 1M |
| Nemotron 3 Ultra ⚡ ★ | NVIDIA | **33.6%** | — | $0.50 | $2.00 | 262k |
| DeepSWE-72B (RL) ⚡ ★ | DeepSWE | **33.2%** | — | Open | Open | — |
| Llama 4 Maverick ★ | Meta | **24.6%** | — | $0.30 | $1.20 | 1M |

---

## 📋 SWE-bench Pro — Methodology & Notes

- **1,865 tasks** created by Scale AI with post-cutoff dates to prevent leakage.
- **SEAL scores** use standardized scaffold; vendor scores often use optimized scaffolds.
- **Gap between SEAL and vendor scores** shows the impact of scaffold engineering (e.g., Claude Fable 5: 55.0% SEAL vs 72.0% vendor).
- **DeepSWE-72B** is a fine-tuned open model specifically for coding benchmarks — demonstrates that specialized training can boost SWE-bench scores.
- **GPT-5.5 (xhigh)** shows an unusually large gap (40.2% SEAL vs 75.0% vendor), raising questions about scaffold dependency.

---

# 3️⃣ GPQA Diamond (Scientific Reasoning)

> **What it tests:** 198 graduate-level multiple-choice questions in physics, chemistry, and biology. Designed to be "Google-proof" — questions cannot be answered by simple web search.  
> **Scale:** 198 questions. Human PhD baseline: ~65-74%.  
> **Top human score:** ~81%.

---

## 🏆 GPQA Diamond — Top Performers

| Rank | Model | Score | Input $/1M | Output $/1M | Type |
|:---:|:---|:---:|:---:|:---:|:---:|
| 1 | **Gemini 3.1 Pro** ⚡ | **94.1%** | $1.25 | $5.00 | Paid |
| 2 | **MiniMax-M3** ⚡ ★ | **92.9%** | $0.20 | $0.80 | Free / Open |
| 3 | **Claude Fable 5** (Max Effort) ⚡ | **92.0%** | $3.00 | $15.00 | Paid |
| 4 | **GPT-5.3 Codex** (xhigh) ⚡ | **91.9%** | $2.50 | $10.00 | Paid |
| 5 | **Claude Opus 4.8** (Max) ⚡ | **91.0%** | $5.00 | $25.00 | Paid |
| 6 | **DeepSeek V4 Pro** (Max) ⚡ ★ | **89.4%** | $0.23 | $1.10 | Free / Open |
| 7 | **GPT-5.5** (xhigh) ⚡ | **88.8%** | $3.75 | $15.00 | Paid |
| 8 | **Qwen3.7 Max** ⚡ ★ | **87.6%** | $0.80 | $3.20 | Free / Open |

---

## 💼 GPQA Diamond — Paid Models (Detailed)

| Model | Creator | Score | Input $/1M | Output $/1M | Context |
|:---|:---|:---:|:---:|:---:|:---:|
| Gemini 3.1 Pro ⚡ | Google | **94.1%** | $1.25 | $5.00 | 1M |
| Claude Fable 5 (Max Effort) ⚡ | Anthropic | **92.0%** | $3.00 | $15.00 | 1M |
| GPT-5.3 Codex (xhigh) ⚡ | OpenAI | **91.9%** | $2.50 | $10.00 | 400k |
| Claude Opus 4.8 (Max) ⚡ | Anthropic | **91.0%** | $5.00 | $25.00 | 1M |
| GPT-5.5 (xhigh) ⚡ | OpenAI | **88.8%** | $3.75 | $15.00 | 922k |
| Claude Opus 4.7 (Max) ⚡ | Anthropic | **88.2%** | $5.00 | $25.00 | 1M |
| Gemini 3.5 Flash ⚡ | Google | **82.0%** | $0.50 | $2.00 | 1M |
| GPT-5.4 mini (xhigh) ⚡ | OpenAI | **78.3%** | $0.50 | $2.00 | 400k |
| Claude Sonnet 4.6 (Max) ⚡ | Anthropic | **78.0%** | $3.00 | $15.00 | 1M |
| Grok 4.3 (high) ⚡ | xAI | **76.0%** | $0.50 | $2.00 | 1M |
| Gemini 2.5 Pro | Google | **72.4%** | $1.25 | $5.00 | 1M |
| Mistral Medium 3.5 | Mistral | **64.1%** | $1.00 | $4.00 | 256k |

---

## 🆓 GPQA Diamond — Free / Open Weights

| Model | Creator | Score | Input $/1M | Output $/1M | Context |
|:---|:---|:---:|:---:|:---:|:---:|
| MiniMax-M3 ⚡ ★ | MiniMax | **92.9%** | $0.20 | $0.80 | 1M |
| DeepSeek V4 Pro (Max) ⚡ ★ | DeepSeek | **89.4%** | $0.23 | $1.10 | 1M |
| Qwen3.7 Max ⚡ ★ | Alibaba | **87.6%** | $0.80 | $3.20 | 1M |
| GLM-5.2 (max) ⚡ ★ | Z AI | **86.3%** | $0.45 | $1.80 | 1M |
| DeepSeek V4 Flash (Max) ⚡ ★ | DeepSeek | **85.4%** | $0.07 | $0.50 | 1M |
| Kimi K2.7 Code ⚡ ★ | Kimi | **85.0%** | $0.60 | $2.40 | 256k |
| Qwen3.6 Plus ⚡ ★ | Alibaba | **78.6%** | $0.40 | $1.60 | 1M |
| MiMo-V2.5-Pro ⚡ ★ | Xiaomi | **76.0%** | $0.20 | $0.80 | 1M |
| Nemotron 3 Ultra ⚡ ★ | NVIDIA | **72.0%** | $0.50 | $2.00 | 262k |
| Gemma 4 31B ⚡ ★ | Google | **68.5%** | Free | Free | 256k |
| DeepSeek V4 Pro (Non-reasoning) ★ | DeepSeek | **65.2%** | $0.23 | $1.10 | 1M |
| Llama 4 Maverick ★ | Meta | **54.3%** | $0.30 | $1.20 | 1M |
| Qwen3.5 9B ⚡ ★ | Alibaba | **50.0%** | $0.10 | $0.40 | 262k |

---

## 📋 GPQA Diamond — Methodology & Notes

- **198 multiple-choice questions** across physics, chemistry, biology.
- PhD-level difficulty; human PhDs score ~65-74%, top human ~81%.
- **All top models now exceed human expert performance.**
- **MiniMax-M3** at 92.9% is remarkable for an open-weights model.
- **Gemini 3.1 Pro** leads at 94.1% — nearly 13 points above best human.
- Questions designed to be "Google-proof" — not answerable through simple information retrieval.
- **Contamination risk:** Despite being "Google-proof," some questions may have leaked into training sets. No formal depreciation yet.

---

# 4️⃣ HLE — Humanity's Last Exam (Frontier Reasoning)

> **What it tests:** 3,000 extremely difficult questions across 100+ academic subjects, co-created by 1,000+ experts from 500+ institutions globally. Designed as "the hardest benchmark" — questions that even top experts find challenging.  
> **Human expert baseline:** ~10% (estimated).  
> **Scale:** 3,000 questions.

---

## 🏆 HLE — Top Performers

| Rank | Model | Score | Input $/1M | Output $/1M | Type |
|:---:|:---|:---:|:---:|:---:|:---:|
| 1 | **Claude Fable 5** (Max Effort) ⚡ | **53.3%** | $3.00 | $15.00 | Paid |
| 2 | **Claude Opus 4.8** (Max) ⚡ | **48.9%** | $5.00 | $25.00 | Paid |
| 3 | **Claude Opus 4.7** (Max) ⚡ | **47.0%** | $5.00 | $25.00 | Paid |
| 4 | **GPT-5.5** (xhigh) ⚡ | **45.5%** | $3.75 | $15.00 | Paid |
| 5 | **GLM-5.2** (max) ⚡ ★ | **44.1%** | $0.45 | $1.80 | Free / Open |
| 6 | **GPT-5.4** (xHigh) ⚡ | **41.6%** | $5.00 | $20.00 | Paid |
| 7 | **DeepSeek V4 Pro** (Max) ⚡ ★ | **40.8%** | $0.23 | $1.10 | Free / Open |
| 8 | **Gemini 3.1 Pro** ⚡ | **40.4%** | $1.25 | $5.00 | Paid |

---

## 💼 HLE — Paid Models (Detailed)

| Model | Creator | Score | Input $/1M | Output $/1M | Context |
|:---|:---|:---:|:---:|:---:|:---:|
| Claude Fable 5 (Max Effort) ⚡ | Anthropic | **53.3%** | $3.00 | $15.00 | 1M |
| Claude Opus 4.8 (Max) ⚡ | Anthropic | **48.9%** | $5.00 | $25.00 | 1M |
| Claude Opus 4.7 (Max) ⚡ | Anthropic | **47.0%** | $5.00 | $25.00 | 1M |
| GPT-5.5 (xhigh) ⚡ | OpenAI | **45.5%** | $3.75 | $15.00 | 922k |
| GPT-5.4 (xHigh) ⚡ | OpenAI | **41.6%** | $5.00 | $20.00 | 1M |
| Gemini 3.1 Pro ⚡ | Google | **40.4%** | $1.25 | $5.00 | 1M |
| GPT-5.3 Codex (xhigh) ⚡ | OpenAI | **38.0%** | $2.50 | $10.00 | 400k |
| Claude Sonnet 4.6 (Max) ⚡ | Anthropic | **36.7%** | $3.00 | $15.00 | 1M |
| Gemini 3.5 Flash ⚡ | Google | **33.0%** | $0.50 | $2.00 | 1M |
| GPT-5.4 mini (xhigh) ⚡ | OpenAI | **29.0%** | $0.50 | $2.00 | 400k |
| Grok 4.3 (high) ⚡ | xAI | **27.5%** | $0.50 | $2.00 | 1M |
| Gemini 2.5 Pro | Google | **22.1%** | $1.25 | $5.00 | 1M |

---

## 🆓 HLE — Free / Open Weights

| Model | Creator | Score | Input $/1M | Output $/1M | Context |
|:---|:---|:---:|:---:|:---:|:---:|
| GLM-5.2 (max) ⚡ ★ | Z AI | **44.1%** | $0.45 | $1.80 | 1M |
| DeepSeek V4 Pro (Max) ⚡ ★ | DeepSeek | **40.8%** | $0.23 | $1.10 | 1M |
| Qwen3.7 Max ⚡ ★ | Alibaba | **39.2%** | $0.80 | $3.20 | 1M |
| MiniMax-M3 ⚡ ★ | MiniMax | **38.8%** | $0.20 | $0.80 | 1M |
| Kimi K2.7 Code ⚡ ★ | Kimi | **36.5%** | $0.60 | $2.40 | 256k |
| DeepSeek V4 Flash (Max) ⚡ ★ | DeepSeek | **35.3%** | $0.07 | $0.50 | 1M |
| Qwen3.6 Plus ⚡ ★ | Alibaba | **33.0%** | $0.40 | $1.60 | 1M |
| MiMo-V2.5-Pro ⚡ ★ | Xiaomi | **32.1%** | $0.20 | $0.80 | 1M |
| Nemotron 3 Ultra ⚡ ★ | NVIDIA | **30.3%** | $0.50 | $2.00 | 262k |
| Gemma 4 31B ⚡ ★ | Google | **27.0%** | Free | Free | 256k |
| Llama 4 Maverick ★ | Meta | **17.2%** | $0.30 | $1.20 | 1M |

---

## 📋 HLE — Methodology & Notes

- **3,000 questions** across 100+ domains — designed to resist memorization.
- **Human experts score ~10%** — making this the hardest public benchmark.
- **Claude Fable 5 at 53.3%** represents a massive leap over human experts.
- **All top models > 40%** means frontier models are now 4-5x human expert level.
- Benchmark was designed by the Center for AI Safety (CAIS) and Scale AI.
- **Questions span:** Mathematics, physics, chemistry, biology, medicine, law, philosophy, linguistics, history, and 90+ other fields.

---

# 5️⃣ AIME 2026 (Math Competition)

> **What it tests:** The 2026 American Invitational Mathematics Examination — 15 integer-answer questions (0-999), 3-hour time limit. Designed for the top 5% of US high school math students.  
> **Scale:** 15 questions. Top human score: 15 (perfect).  
> **Average qualifying AIME participant:** ~6-8.

---

## 🏆 AIME 2026 — Top Performers

| Rank | Model | Score (out of 15) | Input $/1M | Output $/1M | Type |
|:---:|:---|:---:|:---:|:---:|:---:|
| 1 | **GPT-5.2** (xhigh) ⚡ | **14.8** | $3.75 | $15.00 | Paid |
| 2 | **Claude Fable 5** (Max Effort) ⚡ | **14.5** | $3.00 | $15.00 | Paid |
| 3 | **Gemini 3 Flash** ⚡ | **14.6** | $0.50 | $2.00 | Paid |
| 4 | **Claude Opus 4.8** (Max) ⚡ | **14.2** | $5.00 | $25.00 | Paid |
| 5 | **DeepSeek V4 Pro** (Max) ⚡ ★ | **13.8** | $0.23 | $1.10 | Free / Open |
| 6 | **Qwen3.7 Max** ⚡ ★ | **13.5** | $0.80 | $3.20 | Free / Open |
| 7 | **GPT-5.3 Codex** (xhigh) ⚡ | **13.2** | $2.50 | $10.00 | Paid |

---

## 💼 AIME 2026 — Paid Models (Detailed)

| Model | Creator | Score (out of 15) | Input $/1M | Output $/1M | Context |
|:---|:---|:---:|:---:|:---:|:---:|
| GPT-5.2 (xhigh) ⚡ | OpenAI | **14.8** | $3.75 | $15.00 | 1M |
| Gemini 3 Flash ⚡ | Google | **14.6** | $0.50 | $2.00 | 1M |
| Claude Fable 5 (Max Effort) ⚡ | Anthropic | **14.5** | $3.00 | $15.00 | 1M |
| Claude Opus 4.8 (Max) ⚡ | Anthropic | **14.2** | $5.00 | $25.00 | 1M |
| GPT-5.3 Codex (xhigh) ⚡ | OpenAI | **13.2** | $2.50 | $10.00 | 400k |
| Claude Opus 4.7 (Max) ⚡ | Anthropic | **13.0** | $5.00 | $25.00 | 1M |
| Gemini 3.1 Pro ⚡ | Google | **13.0** | $1.25 | $5.00 | 1M |
| Claude Sonnet 4.6 (Max) ⚡ | Anthropic | **12.4** | $3.00 | $15.00 | 1M |
| GPT-5.4 mini (xhigh) ⚡ | OpenAI | **11.0** | $0.50 | $2.00 | 400k |
| Grok 4.3 (high) ⚡ | xAI | **9.5** | $0.50 | $2.00 | 1M |
| Gemini 2.5 Pro | Google | **8.0** | $1.25 | $5.00 | 1M |

---

## 🆓 AIME 2026 — Free / Open Weights

| Model | Creator | Score (out of 15) | Input $/1M | Output $/1M | Context |
|:---|:---|:---:|:---:|:---:|:---:|
| DeepSeek V4 Pro (Max) ⚡ ★ | DeepSeek | **13.8** | $0.23 | $1.10 | 1M |
| Qwen3.7 Max ⚡ ★ | Alibaba | **13.5** | $0.80 | $3.20 | 1M |
| GLM-5.2 (max) ⚡ ★ | Z AI | **13.2** | $0.45 | $1.80 | 1M |
| MiniMax-M3 ⚡ ★ | MiniMax | **12.5** | $0.20 | $0.80 | 1M |
| DeepSeek V4 Flash (Max) ⚡ ★ | DeepSeek | **12.2** | $0.07 | $0.50 | 1M |
| Kimi K2.7 Code ⚡ ★ | Kimi | **11.8** | $0.60 | $2.40 | 256k |
| Qwen3.6 Plus ⚡ ★ | Alibaba | **11.0** | $0.40 | $1.60 | 1M |
| MiMo-V2.5-Pro ⚡ ★ | Xiaomi | **10.6** | $0.20 | $0.80 | 1M |
| Nemotron 3 Ultra ⚡ ★ | NVIDIA | **9.0** | $0.50 | $2.00 | 262k |
| Gemma 4 31B ⚡ ★ | Google | **7.5** | Free | Free | 256k |
| Llama 4 Maverick ★ | Meta | **5.0** | $0.30 | $1.20 | 1M |

---

## 📋 AIME 2026 — Methodology & Notes

- **15 integer-answer questions** (0-999 range), 3-hour competition.
- Top human score: 15; average qualifier: ~6-8.
- **GPT-5.2 at 14.8** is near-perfect — would rank among the top 0.1% of human competitors.
- **Gemini 3 Flash** at 14.6 with far lower cost ($0.50/$2.00 per 1M tokens) is the best value for math.
- Scores typically represent pass@1 (single attempt) with chain-of-thought reasoning.
- **AIME is annual**, so 2026 scores reflect the most recent exam — very low contamination risk.
- Most models now effectively "solve" AIME, reducing its usefulness as a differentiator.

---

# 6️⃣ Arena Elo (Chatbot Arena — Human Preference)

> **What it tests:** Head-to-head blind pairwise comparisons by human voters. Models respond to the same prompt; users pick the better response without knowing which model produced it.  
> **Scale:** 2M+ human votes across 200+ models.  
> **Elo reference:** GPT-4 (original) anchored at ~1,185.

---

## 🏆 Arena Elo — Top 25

| Rank | Model | Arena Elo | Input $/1M | Output $/1M | Type |
|:---:|:---|:---:|:---:|:---:|:---:|
| 1 | **Claude Fable 5** (Max Effort) ⚡ | **1,467** | $3.00 | $15.00 | Paid |
| 2 | **GPT-5.5** (xhigh) ⚡ | **1,452** | $3.75 | $15.00 | Paid |
| 3 | **GPT-5.4** (xHigh) ⚡ | **1,448** | $5.00 | $20.00 | Paid |
| 4 | **Claude Opus 4.8** (Max) ⚡ | **1,441** | $5.00 | $25.00 | Paid |
| 5 | **Gemini 3.1 Pro** ⚡ | **1,438** | $1.25 | $5.00 | Paid |
| 6 | **GPT-5.2** (xhigh) ⚡ | **1,435** | $3.75 | $15.00 | Paid |
| 7 | **GLM-5.2** (max) ⚡ ★ | **1,431** | $0.45 | $1.80 | Free / Open |
| 8 | **Qwen3.7 Max** ⚡ ★ | **1,427** | $0.80 | $3.20 | Free / Open |
| 9 | **Claude Opus 4.7** (Max) ⚡ | **1,425** | $5.00 | $25.00 | Paid |
| 10 | **DeepSeek V4 Pro** (Max) ⚡ ★ | **1,422** | $0.23 | $1.10 | Free / Open |
| 11 | **DeepSeek V4 Flash** (Max) ⚡ ★ | **1,419** | $0.07 | $0.50 | Free / Open |
| 12 | **Gemini 3 Flash** ⚡ | **1,416** | $0.50 | $2.00 | Paid |
| 13 | **MiniMax-M3** ⚡ ★ | **1,414** | $0.20 | $0.80 | Free / Open |
| 14 | **Kimi K2.7 Code** ⚡ ★ | **1,410** | $0.60 | $2.40 | Free / Open |
| 15 | **GPT-5.3 Codex** (xhigh) ⚡ | **1,409** | $2.50 | $10.00 | Paid |
| 16 | **Claude Sonnet 4.6** (Max) ⚡ | **1,404** | $3.00 | $15.00 | Paid |
| 17 | **MiMo-V2.5-Pro** ⚡ ★ | **1,398** | $0.20 | $0.80 | Free / Open |
| 18 | **GPT-5.4 mini** (xhigh) ⚡ | **1,377** | $0.50 | $2.00 | Paid |
| 19 | **Grok 4.3** (high) ⚡ | **1,367** | $0.50 | $2.00 | Paid |
| 20 | **Qwen3.6 Plus** ⚡ ★ | **1,365** | $0.40 | $1.60 | Free / Open |
| 21 | **Nemotron 3 Ultra** ⚡ ★ | **1,352** | $0.50 | $2.00 | Free / Open |
| 22 | **Gemma 4 31B** ⚡ ★ | **1,336** | Free | Free | Free / Open |
| 23 | **Gemini 2.5 Pro** | **1,320** | $1.25 | $5.00 | Paid |
| 24 | **Mistral Medium 3.5** | **1,310** | $1.00 | $4.00 | Paid |
| 25 | **Llama 4 Maverick** ★ | **1,288** | $0.30 | $1.20 | Free / Open |

---

## 📋 Arena Elo — Methodology & Notes

- **2M+ human votes** as of June 2026, making this the largest human evaluation dataset.
- **Elo is calculated** using Bradley-Terry model with confidence intervals typically ±5-10 points.
- **Style bias:** Arena Elo reflects both capability AND stylistic preference (formatting, verbosity, tone).
- **Top models cluster tightly** — 1,467 to 1,404 is a ~60-point spread among the top 16.
- **Open weights models** are now competitive: GLM-5.2 (#7), Qwen3.7 Max (#8), DeepSeek V4 Pro (#10) all in top 10.
- **GPT-4 (original)** baseline: ~1,185. Modern models are 250+ Elo ahead.
- **Categories tracked separately:** Coding, Creative Writing, Hard Prompts, Longer Query, Multi-Turn.

---

# 7️⃣ Context Window (Maximum Capacity)

> **What it measures:** The maximum number of tokens a model can process in a single prompt (input + output).  
> **Larger context** enables processing of entire books, codebases, or long conversations.

---

## 🏆 Context Window — Largest Available

| Rank | Model | Context Window | Effective RULER Score | Input $/1M | Type |
|:---:|:---|:---:|:---:|:---:|:---:|
| 1 | **Llama 4 Scout** ★ | **10,000,000** | TBD | $0.20 | Free / Open |
| 2 | **Claude Fable 5** ⚡ | **2,000,000** | High | $3.00 | Paid |
| 3 | **Claude Opus 4.8** ⚡ | **1,000,000** | High | $5.00 | Paid |
| 4 | **Claude Opus 4.7** ⚡ | **1,000,000** | High | $5.00 | Paid |
| 5 | **Claude Sonnet 4.6** ⚡ | **1,000,000** | High | $3.00 | Paid |
| 6 | **Gemini 3 Flash** ⚡ | **1,000,000** | High | $0.50 | Paid |
| 7 | **Gemini 3.1 Pro** ⚡ | **1,000,000** | Med-High | $1.25 | Paid |
| 8 | **Gemini 3.5 Flash** ⚡ | **1,000,000** | Med-High | $0.50 | Paid |
| 9 | **GPT-5.4** ⚡ | **1,000,000** | Med-High | $5.00 | Paid |
| 10 | **DeepSeek V4 Pro** ⚡ ★ | **1,000,000** | Med | $0.23 | Free / Open |
| 11 | **DeepSeek V4 Flash** ⚡ ★ | **1,000,000** | Med | $0.07 | Free / Open |
| 12 | **GLM-5.2** (max) ⚡ ★ | **1,000,000** | Med | $0.45 | Free / Open |
| 13 | **MiniMax-M3** ⚡ ★ | **1,000,000** | Med | $0.20 | Free / Open |
| 14 | **Qwen3.7 Max** ⚡ ★ | **1,000,000** | Med | $0.80 | Free / Open |
| 15 | **MiMo-V2.5-Pro** ⚡ ★ | **1,000,000** | Med | $0.20 | Free / Open |
| 16 | **Nemotron 3 Super** ★ | **1,000,000** | Med-Low | $0.30 | Free / Open |
| 17 | **Llama 4 Maverick** ★ | **1,000,000** | Med-Low | $0.30 | Free / Open |
| 18 | **GPT-5.5** ⚡ | **922,000** | Med-High | $3.75 | Paid |
| 19 | **GPT-5.3 Codex** ⚡ | **400,000** | High | $2.50 | Paid |
| 20 | **GPT-5.4 mini** ⚡ | **400,000** | High | $0.50 | Paid |

---

## 📋 Context Window — Methodology & Notes

- **RULER benchmark** (by NVIDIA) evaluates *effective* context utilization — many models degrade well before their theoretical limit.
- **Llama 4 Scout** at 10M tokens is unprecedented but likely has significant quality degradation at extremes.
- **Anthropic** claims "near-perfect" retrieval at 200K+ tokens (Claude 4 series).
- **Google's Gemini 3 series** achieves 1M tokens with strong retrieval via RingAttention.
- **"Needle in a Haystack"** tests show real-world effective context is typically 50-80% of advertised.
- For most use cases, 128K-200K is more than sufficient; 1M+ is useful for codebase analysis, book-length content, and multi-day conversations.

---

# 📊 Complete Pricing Table (All Models)

> **Input/Output prices** per 1 million tokens. "Blended" uses 7:2:1 cache-hit:input:output ratio.

| Model | Creator | Type | Input $/1M | Output $/1M | Blended $/1M |
|:---|:---|:---|:---:|:---:|:---:|
| Claude Opus 4.8 | Anthropic | Paid | $5.00 | $25.00 | $5.50 |
| Claude Opus 4.7 | Anthropic | Paid | $5.00 | $25.00 | $5.50 |
| GPT-5.4 (xHigh) | OpenAI | Paid | $5.00 | $20.00 | $5.35 |
| GPT-5.5 | OpenAI | Paid | $3.75 | $15.00 | $4.35 |
| Claude Fable 5 | Anthropic | Paid | $3.00 | $15.00 | $3.50 |
| Claude Sonnet 4.6 | Anthropic | Paid | $3.00 | $15.00 | $3.50 |
| GPT-5.3 Codex | OpenAI | Paid | $2.50 | $10.00 | $2.85 |
| GPT-5.2 | OpenAI | Paid | $2.50 | $10.00 | $2.85 |
| Nova 2.0 Pro | Amazon | Paid | $2.00 | $8.00 | $2.55 |
| Gemini 3.1 Pro | Google | Paid | $1.25 | $5.00 | $1.74 |
| Gemini 2.5 Pro | Google | Paid | $1.25 | $5.00 | $1.74 |
| Mistral Medium 3.5 | Mistral | Paid | $1.00 | $4.00 | $1.30 |
| Qwen3.7 Max | Alibaba | Free/Open | $0.80 | $3.20 | $1.10 |
| Grok 4.3 | xAI | Paid | $0.50 | $2.00 | $0.70 |
| Gemini 3 Flash | Google | Paid | $0.50 | $2.00 | $0.70 |
| GPT-5.4 mini | OpenAI | Paid | $0.50 | $2.00 | $0.70 |
| Kimi K2.7 Code | Kimi | Free/Open | $0.60 | $2.40 | $0.85 |
| Nemotron 3 Ultra | NVIDIA | Free/Open | $0.50 | $2.00 | $0.70 |
| Qwen3.6 Plus | Alibaba | Free/Open | $0.40 | $1.60 | $0.55 |
| GLM-5.2 | Z AI | Free/Open | $0.45 | $1.80 | $0.60 |
| Llama 4 Maverick | Meta | Free/Open | $0.30 | $1.20 | $0.42 |
| Nemotron 3 Super | NVIDIA | Free/Open | $0.30 | $1.20 | $0.42 |
| DeepSeek V4 Pro | DeepSeek | Free/Open | $0.23 | $1.10 | $0.33 |
| MiniMax-M3 | MiniMax | Free/Open | $0.20 | $0.80 | $0.28 |
| MiMo-V2.5-Pro | Xiaomi | Free/Open | $0.20 | $0.80 | $0.28 |
| Llama 4 Scout | Meta | Free/Open | $0.20 | $0.80 | $0.28 |
| DeepSeek V4 Flash | DeepSeek | Free/Open | $0.07 | $0.50 | $0.11 |
| Qwen3.5 9B | Alibaba | Free/Open | $0.10 | $0.40 | $0.14 |
| Gemma 4 31B | Google | Free/Open | Free | Free | Free |

---

# 🏅 Key Takeaways & Winners

## Best by Benchmark

| Benchmark | 🥇 Best Paid | 🥈 Best Free/Open | Notes |
|:---|:---|:---|:---|
| **SWE-bench Verified** | Claude Fable 5 (95.0%) | DeepSeek V4 Pro Max (80.6%) | Anthropic dominates coding |
| **SWE-bench Pro (SEAL)** | GPT-5.4 xHigh (59.1%) | GLM-5.1 (52.8%) | SEAL-verified scores much lower than vendor claims |
| **GPQA Diamond** | Gemini 3.1 Pro (94.1%) | MiniMax-M3 (92.9%) | All top models exceed human experts |
| **HLE** | Claude Fable 5 (53.3%) | GLM-5.2 (44.1%) | Claude leads hardest benchmark by 4.4 points |
| **AIME 2026** | GPT-5.2 xhigh (14.8/15) | DeepSeek V4 Pro Max (13.8/15) | Near-perfect math scores by multiple models |
| **Arena Elo** | Claude Fable 5 (1,467) | GLM-5.2 (1,431) | Human preference: Claude #1 overall |

## Best Value (Intelligence per Dollar)

| Model | GPQA Diamond | Blended Price | Intelligence/Price Ratio |
|:---|:---:|:---:|:---:|
| **DeepSeek V4 Flash** | 85.4% | $0.11/M | **776** |
| **MiniMax-M3** | 92.9% | $0.28/M | **332** |
| **Gemma 4 31B** | 68.5% | Free | ∞ |
| **Gemini 3 Flash** | 82.0% | $0.70/M | **117** |
| **DeepSeek V4 Pro** | 89.4% | $0.33/M | **271** |

## Best Overall Model

| Category | Winner |
|:---|:---|
| 🏆 **Overall Intelligence** | **Claude Fable 5** (Anthropic) — #1 in SWE-bench, HLE, Arena Elo; top 3 in GPQA, AIME |
| 🏆 **Coding** | **Claude Fable 5** — #1 SWE-bench Verified; #2 SWE-bench Pro (SEAL) |
| 🏆 **Science/Math** | **GPT-5.2** — #1 AIME 2026; top 3 GPQA |
| 🏆 **Best Value** | **DeepSeek V4 Flash** — 85.4% GPQA at $0.11/M tokens |
| 🏆 **Best Open Weights** | **GLM-5.2** — #7 overall Arena Elo; top 5 HLE, SWE-bench Pro |
| 🏆 **Largest Context** | **Llama 4 Scout** — 10M tokens |
| 🏆 **Fastest** | **Mercury 2** (Inception) — 924 tokens/s |
| 🏆 **Cheapest** | **Gemma 4 31B** — Free (Google) |

---

# 📝 Methodology & Sources

## Data Sources

| Source | URL | Data Used |
|:---|:---|:---|
| **Artificial Analysis** | artificialanalysis.ai | GPQA Diamond, HLE, pricing, speed, cross-validation |
| **Scale AI SEAL Leaderboard** | scale.com/leaderboard | SWE-bench Pro (SEAL-verified scores) |
| **LMSys Chatbot Arena** | chat.lmsys.org | Arena Elo rankings |
| **llm-stats.com** | llm-stats.com | Cross-reference for pricing, benchmark aggregation |
| **PricePerToken** | pricepertoken.com | Pricing verification |
| **DeepSWE Audit** | github.com/deepswe | Independent SWE-bench Verified evaluation |
| **OpenAI Reports** | openai.com/research | GPT-5.x system cards and benchmark results |
| **Anthropic Reports** | anthropic.com/research | Claude 4.x model cards |
| **Google AI Blog** | ai.googleblog.com | Gemini 3.x benchmark reports |

## Important Caveats

1. **Vendor self-reported scores** may use optimized scaffolds, majority voting, or multiple samples — not directly comparable across providers.
2. **SEAL-verified scores** (SWE-bench Pro) use standardized evaluation — preferred for comparisons but fewer models covered.
3. **Arena Elo** reflects human stylistic preference, not just raw capability.
4. **Benchmark contamination** is a growing concern — some benchmarks (SWE-bench Verified) have been deprecated by certain vendors.
5. **Pricing** is as of June 18, 2026 and subject to change.
6. **Free models** listed with pricing are available via API providers (DeepSeek, Alibaba Cloud, etc.); truly free models (Gemma) have no API cost.
7. **Context window** effective utilization may be significantly lower than advertised maximum.

---

> **Legend:** ⚡ = Reasoning model | ★ = Open Weights | * = Estimated score (pending third-party verification)

> **Last Updated:** June 18, 2026  
> **Next Update:** When new models or scores are released by major labs.
