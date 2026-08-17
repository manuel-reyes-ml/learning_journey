# AI Coding Harness Evaluation — Decision Brief

**Prepared for:** Manuel Reyes
**Date:** 16 August 2026
**Decision:** Which agentic coding harness to standardize on for flagship, production-grade portfolio projects
**Governing constraint:** *No line, pattern, or architecture is committed without being understood first*
**Budget context:** 25 hrs/week development capacity; Q1 2027 apply window; post-employment cost sensitivity

---

## 0. Scope and Sources

Two prior analyses were produced by another agent and stored in Google Drive:

| Ref | Document | Thrust |
|---|---|---|
| **Doc A** | *AI Agentic Code Dev EDI* | Landscape comparison — Cursor / OpenCode+Cline / Claude Code CLI / Claude Code Desktop |
| **Doc B** | *AI Codebase dev + learning* | Learning-first recommendation — Cursor + Roo Code (BYOK), with Aider and Windsurf as alternates |

This document summarizes both, fact-checks them against primary sources, adds independent research, and issues a final verdict for the specific stack under consideration: **OpenCode → OpenRouter, running inside Cursor IDE.**

**Disclosure:** This analysis was produced by Claude (Anthropic). Anthropic-product claims below are cited to Anthropic's own documentation and to third-party/adversarial sources wherever possible. Treat the Claude Code recommendations as the ones requiring the most independent verification.

**Repo alignment gap:** `manuel-reyes-ml/learning_journey` and `data-portfolio` could not be reached (private or rate-limited). Recommendations are aligned to `roadmap.html` v10.0 only. Repo-level alignment is an open item.

---

## 1. Doc A — Summary of the Other Agent's Analysis

**Framing:** The 2026 landscape has fractured into IDE-native integrations, terminal agents, and open harnesses. Choose based on visual ergonomics vs. autonomous execution vs. model flexibility.

| Tool | Doc A's claim — UX | Doc A's claim — Cost | Doc A's claim — Accuracy |
|---|---|---|---|
| Cursor AI | Benchmark for visual ergonomics; visual diffs, Composer agent | "**Flat rate** $20/mo" | Excellent; strong local indexing/RAG |
| OpenCode / Cline harness | Ultimate control, extension panel, transparent | Free + BYOK API | Variable — depends on model routed |
| Claude Code CLI | Terminal-native, aggressively autonomous, no visual diffs | $20/mo with Pro | "Unmatched"; automatic context compaction |
| Claude Code Desktop | Visual diff viewer, branch isolation, preview pane | $20/mo with Pro | Same engine as CLI |

**Doc A's conclusion:** Run an OpenCode/Cline harness *inside* Cursor as a hybrid — Composer for everyday editing, the open harness for routing specific problems to cheaper specialized models, preserving premium rate limits.

---

## 2. Doc B — Summary of the Other Agent's Analysis

**Framing:** If the non-negotiable rule is "no script committed without understanding," highly autonomous agents like Claude Code CLI must be avoided — they are designed to loop, execute, and write files automatically, which works against reviewing every change.

**Doc B's recommendation: Cursor IDE + Roo Code (BYOK)**, justified on three grounds:

1. **Strict visual diffs** — Roo Code defaults to "ask before write," never modifying a file without a side-by-side diff
2. **Separation of planning and coding** — Architect mode teaches the pattern without writing code; switch to Code mode once understood
3. **Cost efficiency** — BYOK with DeepSeek / MiniMax / "GLP 5.3" instead of a flat subscription

**Doc B's alternates:** Aider (git-native, one commit per change, revertible audit trail) and "Windsurf by Codeium" (Cascade agent, transparent real-time context display).

**Doc B's proposed workflow:** Sandbox (Ctrl+K inline questions) → Architect (learn the pattern) → Builder (generate) → Gatekeeper (read the diff; reject anything you can't mentally trace).

---

## 3. Fact-Check — What Both Documents Got Wrong

Every correction below is verified against a primary or independent source.

| # | Claim | Verdict | Evidence |
|---|---|---|---|
| 1 | **Doc B:** "Roo Code — the 2026 evolution of Cline" is the winning setup | ❌ **Dead project** | Roo Code's repo was **archived 15 May 2026** and is read-only; the original team moved to Roomote. Continuity depends on a community handoff (Zoo Code) or the Kilo Code fork. Roo Code was a *fork of* Cline (early 2024), never its successor — Cline remains actively maintained. |
| 2 | **Doc B:** Avoid Claude Code CLI — it writes files automatically | ❌ **Backwards** | Plan Mode is a read-only permission mode: Claude inspects and proposes without editing. Hooks enforce hard rules regardless of mode. Claude Code is *more* gateable than Cursor's native agent, not less. |
| 3 | **Doc A:** Cursor is a "flat rate $20/month" | ❌ **Materially wrong — the costliest error** | Cursor Pro includes "$20 of API agent usage" against a metered pool. Unused usage does not roll over. $20 is a **floor**, not a ceiling. |
| 4 | **Doc A:** Premium models are "Claude 3.5 Sonnet and GPT-4o" | ❌ Stale | Two model generations out of date. |
| 5 | **Doc B:** "Windsurf by Codeium" | ❌ Stale | Codeium → Windsurf → acquired by Cognition → **renamed Devin Desktop, June 2026**. |
| 6 | **Both:** "GLP 5.3" | ⚠️ Misnamed | The model family is **GLM** (Zhipu AI). GLM-5.3 exists; GLM-5.2 is the established coding tier. |
| 7 | **Both:** No mention of the Anthropic/OpenCode rupture | ❌ **Critical omission** | See §4. This is the single most consequential fact for the proposed stack. |

**Doc B's core insight was right; its execution was wrong.** The Architect-then-Code, gate-every-diff workflow is sound and matches the strongest available evidence (§5). It was attached to an archived extension and justified by a false claim about Claude Code.

---

## 4. The Omitted Fact — Anthropic vs. Third-Party Harnesses

Neither document surfaced this, and it directly touches the roadmap's documented "provider-agnostic model-routing" for OpenCode.

**Timeline:**

- **9 Jan 2026, 02:20 UTC** — Anthropic silently deployed server-side checks rejecting subscription OAuth tokens outside official Claude Code. Error: *"This credential is only authorized for use with Claude Code."* OpenCode, Cline, Roo Code and dozens of IDE extensions broke overnight.
- **5 Jan 2026** — OpenCode issue #6930: a developer reported an **account ban** after OAuth login plus a Max plan upgrade.
- **19 Feb 2026** — Anthropic's terms added an "Authentication and credential use" section: OAuth tokens from Free, Pro and Max plans may not be used with third-party tools **or the Agent SDK**. The same day, OpenCode removed all Claude OAuth code — commit message: *"anthropic legal requests."*
- **Aftermath** — OpenAI counter-positioned by explicitly permitting subscription use in third-party tools. OpenCode launched Zen (pay-as-you-go) and Go ($10/mo open-weight models).

### What this means for the roadmap

| Path | Status |
|---|---|
| OpenCode → Claude **subscription OAuth** | 🚫 **ToS violation. Ban precedent exists.** |
| OpenCode → **OpenRouter** | ✅ **Unaffected and always was.** Users on API keys or OpenRouter were never impacted — only the "Login with Claude" OAuth flow broke. |
| OpenCode → Anthropic **API key** (direct, metered) | ✅ Permitted |
| OpenCode → local Ollama | ✅ Permitted, and the privacy-routing path |

**The proposed OpenRouter setup is clean.** The roadmap's OpenCode entry still needs a correction to remove any implication that Claude flows through it via subscription.

---

## 5. Independent Research — The Evidence That Actually Decides This

### 5.1 The interaction pattern beats the tool choice

Neither document cited the most relevant study. Anthropic RCT, published 29 Jan 2026 (arXiv 2601.20245), 52 mostly-junior engineers learning the Trio Python library:

- AI-assisted group scored **50%** on a comprehension quiz vs **67%** hand-coding — ~17 points, roughly two letter grades (Cohen's *d* = 0.738, *p* = 0.01)
- **Largest gap was on debugging questions** — precisely the skill needed to catch AI errors
- The AI group finished ~2 minutes faster; **not statistically significant**
- Several participants spent up to **11 minutes (30% of allotted time) composing queries**

The decisive finding is not the headline number — it is that *how* AI was used determined retention:

| Pattern | n | Outcome |
|---|---|---|
| AI delegation | 4 | <40% — fastest, fewest errors, lowest understanding |
| Progressive AI reliance | 4 | <40% |
| Iterative AI debugging | 4 | <40% — and *slower* |
| Generation-then-comprehension | 2 | ≥65% |
| Hybrid code-explanation | 3 | ≥65% |
| **Conceptual inquiry** | **7** | **≥65% — fastest among high scorers, 2nd fastest overall** |

**Conceptual inquiry** — asking only conceptual questions and resolving one's own errors — beat delegation on comprehension *and* nearly matched it on speed. This is the empirical vindication of Doc B's Architect-mode instinct.

**Anthropic's own caveat, which cuts against Anthropic:** the study used a chat sidebar, and the paper's footnote states that for agentic products like Claude Code, *"the impacts on skill development are likely to be more pronounced."* Agentic harnesses raise the risk. The gate must be structural, not willpower.

### 5.2 Supporting context

- **METR RCT (2025, 246 tasks, 16 experienced devs):** 19% *slower* with AI while feeling 20% faster — a 39-point perception gap. METR's own 2026 follow-up held at roughly 18% slowdown but flagged selection effects making the estimate unreliable. Scope limit: experienced devs on large, familiar repos.
- **Builder.io head-to-head (early 2026, identical tasks, same model):** OpenCode took **78% longer** than Claude Code — part client-server overhead, part an LSP feedback loop that catches bugs, part thoroughness (21 more tests written). The gap is real but not pure waste.

### 5.3 Diff review — the myth both documents propagated

Doc A claimed the CLI has "no visual diffs"; Doc B implied diff gating is an IDE advantage. **All three harnesses gate. The real axis is *when*.**

| Harness | Gate timing | Trade-off |
|---|---|---|
| **Claude Code CLI** | Per-edit, **before disk write** — `y` accept / `n` reject / `d` full diff / `e` edit before accepting | Strongest gate; approve edit-by-edit without seeing the whole multi-file picture |
| **Cursor native agent** | Batch, **after disk write** — all changes made, then presented together for individual or bulk accept/reject | Best for reasoning about a refactor as a whole; git is the only backstop |
| **OpenCode TUI** | Per-edit, before write — `"permission": {"edit": "ask"}`, glob-pattern bash maps (`"git *": "allow"`, `"rm *": "deny"`), last matching rule wins | **Most granular permission config of the three**; 4-line context diff by default, Ctrl+F fullscreen |

**Two corrections to earlier advice given in this thread:**

1. **Claude Code Desktop app writes to disk immediately with no pre-write diff review** (issue #38831). For this policy, **CLI or the VS Code extension only — never the desktop GUI.** Doc A's claim that Desktop offers a diff viewer is wrong for the write path.
2. **Cursor's batch review is a genuine advantage Claude Code lacks.** Issue #31888 documents Cursor migrants finding neither Claude Code mode acceptable: "Ask before edits" forces blind line-by-line decisions; "Edit automatically" is silent. For a multi-file refactor like the DataVault Polars rewrite, this matters.

### 5.4 Cost mechanics — verified against vendor documentation

**Cursor** (official docs, `cursor.com/help/models-and-usage/usage-limits`):

- Two pools: **Cursor Models** (Composer 2.5, Cursor Grok 4.5/4.6) and **Other Models** (third-party at provider prices)
- Pro ($20/mo) = "$20 of API agent usage + generous First-party models pool usage." **The first-party pool's dollar value is not published.**
- At exhaustion: *"You'll see a notification in the editor. You can either enable on-demand usage (pay-as-you-go) or upgrade to a higher plan."*
- **No automatic downgrade** — Cursor states requests are never downgraded in quality or speed
- Unused usage does **not** roll over
- Protections: on-demand must be explicitly enabled; it can be disabled to hard-stop; spend limits can be set

> **Answer to the direct question:** Cursor will **not** silently swap to a cheaper model to keep you running. You get a notification, and then you either pay on-demand, upgrade, manually switch to the first-party Cursor Models pool, or wait for reset. **$20 is a floor.**

**Claude Code:** Pro $20/mo ($17/mo on the $200 annual plan), includes Claude Code in terminal, web and desktop. Flat — hard rate limits rather than surprise bills. Anthropic does not publish exact token quotas, only multipliers (Pro 1x, Max 5x at $100, Max 20x at $200).

**OpenCode:** MIT-licensed, free. Cost is model usage only.
- **OpenRouter / any BYOK** — pure metered, no floor, no ceiling
- **OpenCode Go** — $10/mo ($5 first month), ~18 open models incl. GLM-5.2, DeepSeek V4, MiniMax M3, Kimi K3. Dollar-based caps: **$12/5h, $30/week, $60/month**. Caveat: Grok 4.5, GPT 5.6 Luna, Kimi K3, Qwen 3.8 Max and DeepSeek V4 Pro carry only ~$15/month of included usage, not $60.
- **OpenCode Zen** — pay-as-you-go gateway, includes several genuinely free models

---

## 6. The Proposed Stack: OpenCode → OpenRouter, inside Cursor

This is officially supported, not a hack.

**Setup (per OpenCode docs):** Cursor is a VS Code fork, so setup is identical to VS Code. Open Cursor's **integrated terminal** (detection relies on terminal environment variables — an external terminal will not work), run `opencode`, and the extension auto-installs. If it fails, run `Cmd+Shift+P` → "Shell Command: Install 'cursor' command in PATH". Shortcuts carry over: `Cmd+Esc` quick launch into split terminal, `Cmd+Shift+Esc` new session, `Cmd+Option+K` file references (`@File#L37-42`), plus automatic sharing of the current selection or tab.

### What you gain

| Benefit | Assessment |
|---|---|
| Cursor's editor GUI, file tree, extensions, git integration | ✅ Real — you keep the graphical environment |
| Model freedom via OpenRouter (GLM-5.2, DeepSeek V4, MiniMax M3, Kimi) | ✅ Real, and dramatically cheaper per token than frontier models |
| ToS-clean | ✅ OpenRouter was never affected by the Anthropic block |
| Granular permission gating (`edit: ask` + bash glob maps) | ✅ Best-in-class; satisfies the understand-before-commit rule |
| Local Ollama fallback for ERISA/proprietary data | ✅ Same harness, privacy-routed — strong portfolio evidence |
| No vendor lock-in; `AGENTS.md` portable contract | ✅ Aligns with existing governance |

### What you must accept

| Cost | Assessment |
|---|---|
| **OpenCode diffs render in the terminal, not Cursor's native diff viewer** | The GUI benefit is the *editor*, not the review surface. You do not get Cursor-quality side-by-side diffs for OpenCode's edits. |
| **~78% slower** on identical tasks (Builder.io) | On a 25 hrs/week budget this is the dominant hidden cost |
| No inline Tab autocomplete from OpenCode | This is the one thing OpenCode cannot replace — it is Cursor's job |
| OpenRouter is unbudgeted metered spend | Set hard limits, or use Go ($10 flat, $60/mo hard cap) for predictability |
| More manual configuration | Real, but you already run a governed `.mdc` + `opencode.jsonc` harness |

### 🔑 The cost finding this setup exposes

**If OpenCode does the agentic work, Cursor Pro is largely redundant.**

Cursor's **Hobby tier is free** and includes the full editor, limited Tab completions, and limited Agent requests. The $20 Pro fee buys agent capacity and premium-model access — exactly what OpenCode+OpenRouter is replacing.

The only genuine reason to keep Pro under this architecture is **inline Tab autocomplete**, which OpenCode cannot provide and which Hobby throttles.

| Configuration | Monthly | Predictable? |
|---|---|---|
| Cursor **Hobby** (free) + OpenCode + OpenCode Go | **$10** | ✅ Hard caps |
| Cursor **Hobby** (free) + OpenCode + OpenRouter | **metered only** | ⚠️ Only with limits set |
| Cursor **Pro** + OpenCode + OpenRouter | **$20 floor + metered** | ❌ Paying twice for agentic capability |
| Claude Code Pro (CLI/VS Code ext.) | **$20 flat** | ✅ Rate limits, no bill surprise |

**Recommendation: run Cursor on Hobby for one full billing cycle** while OpenCode handles agentic work. If throttled Tab completions genuinely impede you, upgrade to Pro on evidence. Do not pay $20/month for agent capacity you have decided not to use.

---

## 7. Final Verdict

### ✅ Primary — OpenCode → OpenRouter (or Go), inside Cursor on Hobby

**This is endorsed.** The instinct behind it is correct, and prior advice in this thread under-weighted it.

Rationale:

1. **It satisfies the governing constraint as well as any alternative.** `"permission": {"edit": "ask"}` with glob-scoped bash rules is the most granular gate available. The diff-before-write property is not a Claude Code exclusive.
2. **It is ToS-clean.** OpenRouter was never touched by the January block.
3. **Cost per token is genuinely far lower**, and Go converts it to a hard-capped flat rate if predictability is preferred.
4. **It is the only option that keeps one harness across cloud and local Ollama** — which is what makes privacy routing a portfolio artifact rather than a claim.
5. **It preserves `AGENTS.md` portability** and the existing dual-harness governance rather than requiring a teardown.

**Mandatory configuration for the understand-every-line policy:**

```jsonc
// opencode.jsonc
{
  "$schema": "https://opencode.ai/config.json",
  "permission": {
    "*": "ask",
    "edit": "ask",
    "bash": {
      "*": "ask",
      "git status*": "allow",
      "git diff*":   "allow",
      "uv run pytest*": "allow",
      "rm -rf*":     "deny"
    }
  },
  "agent": {
    "plan": { "permission": { "edit": "deny", "bash": "ask" } }
  }
}
```

**Mandatory workflow (from §5.1 — this is the part that actually determines learning):**
Plan/Architect agent first, conceptual questions only, no code → understand the pattern → switch to build agent → gate every diff → never accept a diff you cannot mentally trace. **Never enable TUI yolo mode or `--auto` on flagship repos.**

### ✅ Secondary — Claude Code CLI (Pro, $20 flat), scoped narrowly

Retained as a **second harness, not a replacement**, for three specific jobs:

1. **Long multi-file refactors** where the 78% speed penalty compounds — e.g. the DataVault S2 Polars ingestion rewrite
2. **Learning-mode sessions on unfamiliar territory.** The `Learning` output style inserts `TODO(human)` markers asking you to implement strategic pieces yourself; `Explanatory` adds Insights on implementation choices. This is the only *native mechanization* of the conceptual-inquiry pattern — set via `"outputStyle": "Learning"` in `.claude/settings.local.json`.
3. **Flat-rate ceiling on heavy weeks**, capping downside when OpenRouter spend would spike

**Strict conditions:** CLI or VS Code extension only — **never the desktop GUI** (no pre-write diff review). Never route Claude subscription credentials through OpenCode.

Honest caveat: the `Learning` style is a convenience, not decisive. Everything it enforces can be enforced by discipline in OpenCode. If the $20 is not comfortable, **drop this tier entirely** — the primary stack stands on its own.

### ❌ Rejected

| Option | Reason |
|---|---|
| **Roo Code** | Repo archived 15 May 2026. Do not build a flagship workflow on it. |
| **Cursor Pro under this architecture** | Paying a $20 floor for agentic capacity being deliberately replaced. Revisit only if Hobby Tab throttling proves blocking. |
| **Claude Code Desktop GUI** | Writes to disk before review — incompatible with the governing constraint. |
| **OpenCode → Claude subscription OAuth** | ToS violation with documented ban precedent. |
| **Windsurf / Devin Desktop** | Three ownership changes in two years, two pricing-model changes in twelve months. Platform risk unacceptable for a two-year roadmap. |

---

## 8. Consolidated Comparison

| Harness | Cost | Predictable | Diff gate | Speed | Model freedom | Verdict |
|---|---|---|---|---|---|---|
| **OpenCode + OpenRouter (in Cursor)** | Metered | ⚠️ w/ limits | ✅ Pre-write, most granular | ⚠️ ~78% slower | ✅ 75+ providers + local | ✅ **PRIMARY** |
| **OpenCode + Go (in Cursor)** | $10 flat | ✅ $60/mo cap | ✅ Same | ⚠️ Same | ✅ 18 open models | ✅ **PRIMARY (predictable variant)** |
| **Claude Code CLI / VS Code ext.** | $20 flat | ✅ | ✅ Pre-write, per-edit | ✅ Fastest | ❌ Claude only | ✅ **SECONDARY, scoped** |
| **Cursor Pro native agent** | $20 **floor** | ❌ | ⚠️ Post-write batch | ✅ | ✅ | ❌ Redundant here |
| **Cursor Hobby (editor only)** | **$0** | ✅ | n/a | n/a | n/a | ✅ **Host IDE** |
| **Claude Code Desktop GUI** | $20 flat | ✅ | ❌ **None pre-write** | ✅ | ❌ | ❌ Rejected |
| **Roo Code** | — | — | — | — | — | 🚫 Archived |

---

## 9. Proposed Roadmap Corrections — *Awaiting Approval, No Edits Made*

Following the additive-only, propose-then-approve convention. Each declined option carries a falsifier.

**Correction 36 — OpenCode provider routing clarified**
Amend the OpenCode entry to state routing explicitly: **OpenRouter (primary cloud), OpenCode Go (optional flat-rate), local Ollama (privacy-routed).** Add an explicit prohibition on Anthropic subscription OAuth through any third-party harness, citing the 19 Feb 2026 ToS change and the §4 ban precedent.
*Falsifier:* Anthropic publishes a sanctioned third-party harness authentication path.

**Correction 37 — Cursor re-tiered from Pro to Hobby, provisionally**
Change the Cursor line from `$20/mo` to `$0 (Hobby)` with a review gate: reassess after one full billing cycle of OpenCode-primary operation. Record that Cursor Pro is a metered floor, not a flat rate.
*Falsifier:* Hobby-tier Tab completion throttling measurably blocks work in the DataVault S2 rewrite → upgrade to Pro on evidence, and record the evidence.

**Correction 38 — Claude Code added as scoped secondary harness**
Add Claude Code (CLI / VS Code extension only, desktop GUI explicitly excluded) for long multi-file refactors and Learning-mode sessions. Cite arXiv 2601.20245 as the evidentiary basis for the conceptual-inquiry workflow. Candidate for an ADR — the harness-selection decision is itself portfolio evidence.
*Falsifier:* OpenCode closes the speed gap, or the $20 fails a cost review → drop the tier.

**Correction 39 — Understand-before-commit encoded as configuration**
Add the `opencode.jsonc` permission block from §7 to the production standard, alongside a prohibition on yolo/`--auto` modes in flagship repos. Elevates the policy from discipline to enforced configuration.
*Falsifier:* None — this is the governing constraint made executable.

**Open item carried forward:** repo-level alignment (`learning_journey`, `data-portfolio`) pending access.

---

## 10. Sources

**Primary / vendor**
- Anthropic, *How AI assistance impacts the formation of coding skills* (29 Jan 2026) — anthropic.com/research/AI-assistance-coding-skills; paper: arXiv 2601.20245
- Claude Code docs — permission modes, output styles, permissions (code.claude.com/docs)
- Cursor docs — Usage and limits; Usage-based charges (cursor.com/help)
- OpenCode docs — Permissions; IDE integration; Zen/Go (opencode.ai/docs)

**Issue trackers (adversarial / user-reported)**
- anthropics/claude-code #38831 — desktop GUI writes without diff review
- anthropics/claude-code #31888 — no batch diff review vs Cursor's native agent
- anthropics/claude-code #27708 — CLI inline diff editing request
- anomalyco/opencode #6930 — account ban following OAuth login

**Independent research and reporting**
- METR RCT (2025) and 2026 follow-up on developer productivity
- Builder.io head-to-head, OpenCode vs Claude Code, early 2026
- Roo Code archival (15 May 2026) — multiple independent confirmations
- Coverage of the Jan–Feb 2026 Anthropic third-party harness restrictions (The Register, The Verge, DEV, Hacker News threads)
- O'Reilly Radar, *Comprehension Debt: The Hidden Cost of AI-Generated Code* (Apr 2026)

---

*All figures verified against sources dated on or before 16 August 2026. AI tooling pricing and model rosters change frequently — re-verify vendor pricing before any purchase decision.*
