# ADR-001 — Agentic Harness Architecture

**Status:** Accepted · **Date:** 2026-08-18 · **Supersedes:** dual-harness Cursor + OpenCode framing
**Roadmap:** v10.0, CORRECTIONS 39–41 · **Deciders:** Manuel Reyes
**Review gate:** one full billing cycle (see §8)

---

## 1. Context

The harness is where the governing constraint — *no line, pattern, or architecture is committed without being understood first* — is either enforced or merely hoped for. Prior to this decision the roadmap recorded a "dual-harness Cursor + OpenCode" workflow with **no record of how models were routed, what the agent surface was, or which alternatives had been rejected**.

Three constraints shape the decision:

| Constraint | Implication |
|:---|:---|
| **25 hrs/week**, Q1 2027 apply window | Speed penalties compound; a 78% slowdown is a real cost |
| **Post-employment cost sensitivity** | Predictable flat spend beats metered; surprise bills are unacceptable |
| **Understand-before-commit is non-negotiable** | The gate must be structural, not willpower |

---

## 2. Decision

**OpenCode is the sole agentic harness, hosted inside Cursor running on the free Hobby tier, with OpenCode Go as the primary model provider and OpenRouter retained as metered overflow.**

```
┌─────────────────────────────────────────────────────────┐
│  Cursor IDE — Hobby ($0)                                │
│  editor · file tree · extensions · git · terminal       │
│                                                          │
│   ┌──────────────────────────────────────────────────┐  │
│   │  OpenCode  (integrated terminal)                 │  │
│   │  6 primary agents · 5 subagents · 9 commands     │  │
│   └───────────┬──────────────┬───────────────┬───────┘  │
└───────────────┼──────────────┼───────────────┼──────────┘
                │              │               │
        ┌───────▼──────┐ ┌─────▼──────┐ ┌──────▼───────┐
        │ OpenCode Go  │ │ OpenRouter │ │ local Ollama │
        │ $10/mo flat  │ │  metered   │ │     free     │
        │  PRIMARY     │ │  OVERFLOW  │ │   PLANNING   │
        └──────────────┘ └────────────┘ └──────────────┘
```

**Setup note:** Cursor is a VS Code fork, so setup is identical. OpenCode must run in Cursor's **integrated** terminal — detection relies on terminal environment variables, and an external terminal will not work. The extension auto-installs on first run.

---

## 3. Why Cursor drops to Hobby

Under this architecture, **Cursor Pro pays for capacity that OpenCode replaces.**

| Tier | Provides | Needed here? |
|:---|:---|:---:|
| Hobby ($0) | Full editor, file tree, extensions, git, integrated terminal | ✅ All of it |
| Pro ($20) | Agent requests, premium-model access | ❌ OpenCode's job |
| Pro ($20) | Inline Tab autocomplete (throttled on Hobby) | ⚠️ The only real loss |

### ⚠️ Factual correction recorded

Cursor Pro was **never a flat $20/month**, and treating it as one understated the commitment:

- Pro includes roughly **$20 of API agent usage against a metered pool**
- Unused usage **does not roll over**
- At exhaustion the editor notifies; you enable on-demand billing or upgrade
- **Requests are never silently downgraded** to a cheaper model — no automatic quality fallback
- A separate first-party "Cursor Models" pool exists, and **its dollar value is unpublished**

**$20 was a floor, not a ceiling.** Downside is bounded only by explicitly disabling on-demand usage or setting a spend limit.

**The `.cursor/rules/*.mdc` layer survives intact** — OpenCode's `instructions` array reads those files directly, so no rule is rewritten or duplicated by the tier change.

---

## 4. The cost model — what the numbers actually mean

### $10 is what you pay. $60 is what you get.

The $12 / $30 / $60 figures are **usage allowances denominated in list-price value**, not spend. OpenCode's stated arrangement is $10/month for roughly 6× that in usage.

| | |
|:---|:---|
| **Leaves your account** | $5 first month, then **$10/month. Never more.** |
| **You receive** | Up to **$60/month** of model usage |
| **Three windows** | $12 per 5h · $30 per week · $60 per month — throttle the burn rate |

**At a limit, requests block. You are not charged.** Options: wait for reset, switch to a free model, fall back to OpenRouter or Ollama, or opt in to Zen-balance overflow.

> 🔒 **"Use balance" must stay OFF in the Zen console.** It is the single setting that determines whether Go is a fixed cost or a variable one. Off = hard $10 ceiling.

### ⚠️ The monthly cap binds before the weekly one

```
$30/week × ~4.3 weeks = ~$129   ← what the weekly cap alone implies
$60/month                        ← the actual ceiling
```

Burn $30 in week 1 and $30 in week 2 and **weeks 3–4 are dead.** Pace at **~$15/week**.

At 25 hrs/week that is **~$0.56/hour**; a 5-hour session budgets to ~$2.80 against a $12 cap, so **the 5-hour window will effectively never bind.** Budget monthly; check the console at the start of week 3.

### ⚠️ Tier is *value*, not volume — and the ordering is counter-intuitive

Not every model gets the 6× multiplier. A cheap reduced-tier model can buy **more** requests than an expensive full-tier one:

| Model | Tier | Req/5h | Req/week | **Req/month** | Per hour @ 25hr/wk |
|:---|:---:|---:|---:|---:|---:|
| **MiniMax M3** | ✅ $60 | 3,200 | 8,000 | **16,000** | ~150 |
| **DeepSeek V4 Pro** | ⚠️ $15 | 1,050 | 2,600 | **5,200** | ~49 |
| **GLM-5.2** | ✅ $60 | 880 | 2,150 | **4,300** | ~40 |
| **GLM-5.3** | ⚠️ $15 | 220 | 540 | **1,080** | ~10 |
| **Kimi K3** | ⚠️ $15 | 110 | 250 | **490** | **~4.6** |

> 🔑 **DeepSeek V4 Pro on the reduced tier outruns GLM-5.2 on the full tier**, because at $0.435/$0.87 it is cheap enough that $15 buys more of it than $60 buys of GLM-5.2.

**Full tier ($60):** `glm-5.2` `glm-5.1` `minimax-m3` `minimax-m2.7` `qwen3.7-max` `qwen3.7-plus` `qwen3.6-plus` `kimi-k2.7-code` `kimi-k2.6` `mimo-v2.5` `hy3`
**Reduced tier ($15):** `glm-5.3` `kimi-k3` `grok-4.5` `qwen3.8-max` `gpt-5.6-luna` `mimo-v2.5-pro` `deepseek-v4-pro` `deepseek-v4-flash`

⚠️ **GLM-5.3 is reduced tier while GLM-5.2 is full tier** — newer is worse here. Default to 5.2.

### ❓ Open question — flagged, not assumed

**Whether the $15 and $60 figures are separate per-model allowances or proportional draws on one shared $60 pool.** The vendor docs do not say plainly. **Watch the console during month 1**; if mixed usage drains faster than expected, it is a shared pool.

### Slug format

Go **drops the vendor sub-path** OpenRouter requires:

```
OpenRouter   openrouter/z-ai/glm-5.2
Go           opencode-go/glm-5.2
```

Migrating a config means editing the slug, not just swapping the prefix.

---

## 5. Model allocation — critical work gets the better models

**Allocation principle: spend reasoning quality where errors propagate silently; spend allowance where volume is high and reasoning is shallow.**

| Role | Model | Tier | Why this model |
|:---|:---|:---:|:---|
| **Plan — regulated** | `ollama/qwen3.5-16k` | free | Local. Planning may carry data *shapes* not in the repo |
| **Plan — standard** | `opencode-go/glm-5.2` | ✅ $60 | AA Index **51** vs M3's 44. Architecture errors propagate silently |
| **Plan — hard** | `opencode-go/kimi-k3` | ⚠️ $15 | AA **57**, GPQA **93.5**. ADR-worthy decisions only |
| **Build — default** | `opencode-go/glm-5.2` | ✅ $60 | MIT, ~168 tok/s (fastest), 81% Terminal-Bench, beats GPT-5.5 on SWE-bench Pro |
| **Build — gated** | `opencode-go/glm-5.2` | ✅ $60 | Same model; the gate differs, not the capability |
| **Build — alternate** | `opencode-go/deepseek-v4-pro` | ⚠️ $15 | 80.6% SWE-bench Verified (top open), **$0.04/task vs K3's $0.94** |
| **Hard / frontend** | `opencode-go/kimi-k3` | ⚠️ $15 | **#1 Arena Frontend Code Arena** — first open model to lead it |
| **Learn** | `ollama/qwen3.5-16k` → GLM-5.2 | free / $60 | Explanations have no downstream verification gate |
| **Docs / GitHub** | `opencode-go/minimax-m3` | ✅ $60 | High volume, long context, shallow reasoning — **16,000/mo fits exactly** |
| **Review** | `opencode-go/kimi-k3` | ⚠️ $15 | Highest reasoning; low volume makes the scarce tier affordable |
| **Cheap overflow** | `openrouter/deepseek/deepseek-v4-flash` | metered | $0.14/$0.28 — a sixth of V4 Pro when Go blocks |

### Why plan gets a better model than its volume suggests

The instinct is that planning is high-frequency and should get the biggest allowance. The actual volume:

```
25 hrs/week × 1–3 plan sessions per work session, a few turns each
  ≈ 80–120 plan calls/month   (against MiniMax M3's 16,000)
```

**The largest allowance was allocated to the smallest-volume task.** Plan output is the architecture every later build depends on — and a bad plan propagates silently where a bad diff surfaces in tests. Reasoning quality is the right purchase here; allowance is not.

**DeepSeek V4 Pro declined for planning:** tied with M3 at AA 44, and it can look frozen in Plan mode (reasoning-MoE plus ai-sdk thinking-stream). Not a hang, but a poor fit for an interactive loop. *Hands-on finding; it outranks the benchmark tie.*

**GLM-5.3 excluded from the standing ladder:** reduced tier, first-party benchmarks only, weights promised but not shipped, while GLM-5.2 sits on full tier with ~4× the requests. **Falsifier:** adopt only on independent benchmarks plus published weights.

### ⚠️ Contention to watch

`plan-cloud`, `build`, `build-gated` and `learn-cloud` all draw GLM-5.2's 4,300/month. Planning and learning are low-volume enough that build should retain ~3,500+. **If the console shows it tightening, push `learn-cloud` down to MiniMax M3 before touching build.**

---

## 6. Agent surface — 11 agents, 9 commands

### Primary agents (`Tab`-selectable)

| Agent | Model | `edit` | Purpose |
|:---|:---|:---:|:---|
| `plan` | local Ollama | deny | Read-only planning; regulated default |
| `plan-cloud` | GLM-5.2 | deny | Standard session planning |
| `plan-cloud-hard` | Kimi K3 | deny | ADR-worthy, cross-cutting architecture |
| `build` | GLM-5.2 | **allow** | Post-write gate via `git diff` |
| `build-gated` | GLM-5.2 | **ask** | Pre-write gate, per edit |
| `learn` | local Ollama | deny | Teaching pair-programmer; never writes |

### Subagents (`@`-invoked)

`docs-sync` (report) · `docs-fix` (writes docs) · `eval-guardian` · `pattern-scout` · `security-auditor`

### Commands (`/`-invoked)

`/commit-msg` `/draft-issue` `/eval` `/labels` `/pr-prep` `/readme` `/review` `/task-brief` `/test`

### 🔑 Agents vs commands — a security boundary, not a style preference

> **An agent is a *who*. A command is a *what*.**
> **Command = "please don't." Agent = "you can't."**

A prohibition in a command body is **persuasion** — the model reads it and probably complies. A permission denied in an agent is **architecture** — the tool is never handed to the model.

| | Agents | Commands |
|:---|:---|:---|
| Own model | ✅ | via override only |
| Own **permissions** | ✅ **the dividing line** | ❌ inherits |
| Lifetime | persists for session | one-shot |

**Consequence that is easy to miss:** a command specifying `agent: build` executes with **build's write permissions even when invoked from a read-only plan agent**. A command is a legitimate route *into* a more permissive agent. `subtask: true` and a `model:` override decouple it further from the active session.

**Three independent dials:**

| Dial | Controls | Default |
|:---|:---|:---|
| `agent` | what it *may do* | current agent |
| `model` | what *thinks* | that agent's model |
| `subtask` | *where* it thinks | inline |

**Decision rule:** *if the model ignored my instructions here, would I care?* Yes → agent. No → command.

### ⚠️ Frontmatter syntax defect

Agent and command files are Markdown, but the block between `---` fences is **YAML**. HTML comments there are parsed as part of the scalar value, **silently invalidating the field with no error**:

```yaml
---
agent: build   <!-- WRONG — value becomes "build <!-- ... -->" -->
agent: build   # correct
---

<!-- HTML comments are correct from here down -->
```

---

## 7. Two build gates — the distinction *is* the ruling

**Neither gate is universally correct.**

| | `build` | `build-gated` |
|:---|:---|:---|
| Gate timing | **after** write (`git diff`) | **before** write (per edit) |
| Keys | — | `y` accept · `n` reject · `d` full diff · `e` edit |
| Best for | multi-file refactors | unfamiliar code, single-file, learning |
| Failure mode | you skim the diff | **reflex `y` after 15 prompts** |

**Pre-write gating is wrong for large multi-file refactors** — the S2 Polars ingestion rewrite is the named case. Per-edit approval hides the whole-change picture, and long prompt chains produce reflex approval: *a gate that feels real but is not.* This is the same pattern as the "iterative AI debugging" cluster in the evidence below — scored under 40% comprehension **and** was slower.

> ⚠️ **OpenCode's inline diff shows ~4 lines of context.** Press `Ctrl+F` for fullscreen before accepting anything non-trivial — an unexpanded `ask` prompt reviews *less* than `git diff` does.

> 🔒 **Binding precondition on both agents: start every session on a clean tree.** Commit or stash first, or `git diff` mixes agent edits with your uncommitted work and the review stops being trustworthy. This is arguably a bigger integrity win than the gate choice itself.

---

## 8. Alternatives evaluated and declined

Every decline carries a falsifier.

| Option | Why declined | Falsifier |
|:---|:---|:---|
| **Claude Code** as scoped secondary | `build-gated` enforces the same invariant by configuration; a second $20/mo harness is unjustified against a $10 flat subscription already covering the work. Its `Learning` output style (`TODO(human)` markers) is the only *native* mechanisation of conceptual inquiry found — a genuine loss, accepted | S2 Polars rewrite shows OpenCode's ~78% speed penalty costs more than $20/mo of the 25 hr/wk budget |
| **Cursor Pro retained** | Paying a metered $20 floor for agentic capacity deliberately replaced | Hobby Tab throttling *measurably* blocks S2 work → upgrade **on recorded evidence, not discomfort** |
| **Roo Code** | Repository **archived 15 May 2026**, read-only. A flagship workflow on a dead project | — |
| **Windsurf / Devin Desktop** | Three ownership changes in two years (Codeium → Windsurf → Cognition, renamed June 2026); two pricing-model changes in twelve months. **Platform risk unacceptable for a 32-month roadmap** | — |
| **Claude Code desktop GUI** | Writes to disk with **no pre-write diff review** — incompatible with the governing constraint even where the CLI is not | — |
| **OpenCode via Claude subscription OAuth** | 🚫 **Prohibited.** 9 Jan 2026 server-side block; 19 Feb 2026 terms bar Free/Pro/Max OAuth from third-party tools *and the Agent SDK*; OpenCode removed the code same day. **Account ban on record.** API-key and OpenRouter routing were never affected | Anthropic publishes a sanctioned third-party auth path |
| **OpenRouter as sole provider** | Metered with no ceiling; breakeven against Go is ~$10–12/mo of usage, cleared in week 1 at this volume | Monthly usage falls below ~$10 of value → cancel Go |

---

## 9. Evidence base

### The interaction pattern beats the tool choice

Anthropic RCT (Jan 2026, arXiv 2601.20245), 52 mostly-junior engineers:

- AI-assisted group scored **50%** on comprehension vs **67%** hand-coding — ~2 letter grades (*d* = 0.738, *p* = 0.01)
- **Largest gap on debugging questions** — precisely the skill needed to catch AI errors
- Speed gain was **not statistically significant**

| Pattern | n | Comprehension |
|:---|:---:|:---:|
| AI delegation | 4 | <40% (fastest) |
| Progressive AI reliance | 4 | <40% |
| Iterative AI debugging | 4 | <40% **and slower** |
| Generation-then-comprehension | 2 | ≥65% |
| Hybrid code-explanation | 3 | ≥65% |
| **Conceptual inquiry** | **7** | **≥65%, fastest among high scorers** |

**Anthropic's own caveat, which cuts against Anthropic:** the study used a chat sidebar; the paper notes that for agentic products like Claude Code, *"the impacts on skill development are likely to be more pronounced."* **Agentic harnesses raise the risk — the gate must be structural.**

### ⚠️ Benchmarks are not comparable across sources

Terminal-Bench, six trackers, checked within days: **65.9% → 91.9%** for the same models. Causes: version confusion (2.0 vs 2.1 are different task sets), harness variation (xAI reported Grok 4.6 at 26.0% on v3.0 while AA reports 88.4% on v2.1), and refusal-fallback accounting.

SWE-bench Pro has **four competing "best" scores**, 47.1% → 80.3%, depending on harness. And llm-stats lists **0 of 104** SWE-bench Verified entries as independently verified.

> 🔑 **Treat any leaderboard delta under ~5 points as noise.** Every model choice above rests on tier economics, speed, licence, or a hands-on finding — not on a benchmark gap inside the error bar.

### Speed cost, accepted

One head-to-head found OpenCode **78% longer** than Claude Code on identical tasks — part client-server overhead, part an LSP loop that catches real bugs, part thoroughness (21 more tests written). **Not pure waste, but a real tax on a 25 hr/week budget.** This is the single strongest argument against the decision and is recorded as such.

---

## 10. Privacy posture

**The boundary is the repository, not the model.** Flagship repos are **public with synthetic data only** — so a real participant record in a fixture is a disclosure whether or not a cloud model ever reads it.

**Enforcement lives in pre-commit hooks** — `gitleaks` and `detect-private-key` (Tier A). The prohibitions written into command prompts are **advisory reinforcement, not gates** — the §6 command-vs-agent distinction applied to data rather than permissions.

> ⚠️ **Gap recorded, not closed:** `gitleaks` is tuned for credentials and keys, **not SSN-shaped strings or personal names in a CSV fixture.** A custom rule is the obvious remedy and is outstanding work.

**Local planning retained regardless.** `plan` stays on Ollama and `small_model` stays local so session titles never reach a provider. The justification changes rather than disappears: not because repo code is sensitive, but because **a planning session may carry production data shapes, real record structures, or operational detail typed by the human that never enters the repository.**

⚠️ **Ollama `:cloud` tags are a live hazard** — several models publish one alongside the local tag. **Pulling the cloud tag does not give local inference** and would silently void the guarantee while appearing to honour it. Verify the tag, not the model name.

⚠️ **Local plan model evidence gap:** Qwen 3.5 9B has **no published benchmarks**; at least one tracker lists it without benchmark rows rather than inventing them. The selection rests on hands-on judgement, recorded as such. **Falsifier:** if planning quality proves inadequate, the benchmarked alternative is **Qwen3.6-27B** (77.2% SWE-bench Verified, Apache 2.0) — but ~17 GB Q4 is tight on 16 GB unified memory; documented 16 GB fits are `gpt-oss:20b` and Gemma 4 12B.

---

## 11. Consequences

### Positive

- **Net −$10/mo** — Cursor $20 → $0, Go $0 → $10
- **Hard-capped spend** with no surprise-bill path (given "Use balance" off)
- **Structural enforcement** of understand-before-commit, via permissions rather than willpower
- **No vendor lock-in** — MIT harness, portable `AGENTS.md`, three interchangeable providers
- **`.cursor/rules/*.mdc` retained** and read directly by OpenCode
- Provider redundancy: a blocked Go window is an `F2` away from OpenRouter

### Negative — accepted

- **~78% slower** than the fastest alternative on identical tasks
- **No inline Tab autocomplete** at usable volume (Hobby throttles it)
- **Terminal diffs, not Cursor's native side-by-side viewer** — the GUI benefit is the *editor*, not the review surface
- **Contingent saving.** If the §8 Cursor falsifier fires, the position becomes **+$10/mo** against the pre-decision baseline. Stated so it does not arrive as a surprise
- **Kimi K3 is scarce** at ~4.6 req/hour — roughly one call per 13 minutes of work

### ❓ Open — by observation, not assumption

1. **Do `!`shell`` template expansions respect the active agent's `bash` permission?** If yes, shell-running commands break under `bash: deny`. If no, `bash: deny` is not a boundary against commands. **Run `/test` once from local `plan` to settle it.**
2. **Are Go's $15 and $60 tiers separate or shared allowances?** Watch the console in month 1.
3. **Does Hobby-tier Tab throttling actually impede work?** One billing cycle decides.

---

## 12. Setup checklist

- [ ] Downgrade Cursor to Hobby
- [ ] Subscribe to OpenCode Go at `opencode.ai/auth` ($5 first month)
- [ ] **Confirm "Use balance" is OFF** ← the hard-cap setting
- [ ] `/connect` → OpenCode Go → paste `sk-…` key
- [ ] `/models` → verify all `opencode-go/*` entries appear
- [ ] Verify Ollama tags are local, not `:cloud`
- [ ] Run `/test` from local `plan` → settle open question 1
- [ ] Week 3: check console burn rate → settle open question 2
- [ ] End of cycle: assess Tab throttling → settle open question 3

---

## 13. Review

**Trigger:** one full billing cycle of OpenCode-primary operation.

**Decide:**
1. Go usage under ~$10 of value → cancel, go metered on OpenRouter
2. Repeatedly hitting the $60 monthly wall → keep Go, lean on OpenRouter overflow
3. Tab throttling measurably blocking → Cursor Pro **on recorded evidence**
4. GLM-5.2 allowance contended → move `learn-cloud` to MiniMax M3, **never build**

---

> **Legend:** ✅ full tier · ⚠️ reduced tier / caveat · 🔒 binding · ❓ open
> **Verification date:** 2026-08-18. AI tooling pricing and model rosters move monthly — **re-verify tier tables before treating any figure here as current.**
