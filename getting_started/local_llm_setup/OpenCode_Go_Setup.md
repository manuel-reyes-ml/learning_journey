# OpenCode Go — Account Setup & Configuration Guide

**Purpose:** Create an OpenCode Go subscription and wire it into OpenCode as a provider.
**Audience:** Anyone running OpenCode; written for a Cursor + local-Ollama workflow but provider setup is universal.
**Verified against:** `opencode.ai/docs/go` (page last updated **16 Aug 2026**)
**Version:** 1.0 (17 Aug 2026)

> ⚠️ Go's model roster, pricing tiers and limits change as OpenCode negotiates provider deals. The docs page carries a "limits may change" notice. **Re-verify the tier table (§6) before making it a default in a project config.**

---

## 1. What Go is — and what it is not

Three separate things get confused constantly. They are not the same product:

| Product | What it is | Billing |
|---|---|---|
| **OpenCode** | The agent itself. MIT-licensed, free, model-agnostic. | Free forever |
| **OpenCode Zen** | OpenCode's own model gateway + account system. | Pay-as-you-go balance |
| **OpenCode Go** | A flat subscription *on top of* your Zen account, giving curated access to open coding models. | **$5 first month, then $10/month** |
| **OpenRouter** | An unrelated third-party aggregator. | Pay-per-token, you load credits |

Go is **completely optional** — you don't need it to use OpenCode. It is one provider among many, and it coexists with Ollama, OpenRouter, and direct API keys in the same config. No lock-in.

**You sign in to Zen to subscribe to Go.** That's why the auth URL says Zen.

---

## 2. The cost model — read this before subscribing

This is the single most misunderstood part of Go.

### The $12 / $30 / $60 numbers are NOT money you spend

They are **usage allowances measured in dollar-equivalent value** at model API list prices. You pay $10. Full stop.

From the docs, verbatim on the arrangement: *"With Go, you pay $10/month and we aim to give you 6x that in usage."*

$10 × 6 = $60.

| | |
|---|---|
| **What leaves your bank account** | $5 first month, **$10/month** thereafter. Never more. |
| **What you receive** | Up to **$60/month** of model usage |
| **What the three windows do** | Throttle *how fast* you can burn that $60 |

### The three rolling windows

| Window | Allowance |
|---|---|
| **5-hour** (rolling) | $12 of usage |
| **Weekly** | $30 of usage |
| **Monthly** | $60 of usage |

### What happens when you hit a limit

Requests for that model **block**. You are **not** charged. Your options:

1. **Wait** for the window to reset
2. **Switch to a free model** — the docs confirm free models remain available after you hit the limit
3. **Switch providers** — local Ollama or OpenRouter, configured in the same `opencode.json`
4. **Opt in to overflow** — if you hold credits on your Zen balance, enabling **"Use balance"** in the console makes Go fall back to that balance instead of blocking

> 🔒 **Leave "Use balance" OFF and $10/month is a hard ceiling.** This is the setting that determines whether Go is a fixed cost or a variable one. Verify it after signup.

### ⚠️ The planning trap: the monthly cap binds first

The windows are nested, and they don't multiply out consistently:

```
$30/week × ~4.3 weeks = ~$129   ← what the weekly cap alone would imply
$60/month                       ← the actual ceiling
```

**Burn $30 in week 1 and $30 in week 2, and weeks 3–4 are dead.** The 5-hour and weekly caps exist specifically to stop bursty usage from draining the month early.

**Pace at roughly $15/week** to spread $60 evenly across a month.

### Worked example — 25 hrs/week of gated, review-every-diff work

```
25 hrs/week × 4.3 = ~107 hrs/month
$60 ÷ 107 hrs      = ~$0.56/hour of development time
A 5-hour session   = ~$2.80 budget   (vs the $12 cap — huge headroom)
```

**Conclusion for this profile: the 5-hour cap will essentially never bind. Only the monthly cap matters.** Budget by the month, not the session.

Translated into requests on a full-tier model: GLM-5.2 at ~4,300 requests/month ÷ 107 hrs ≈ **40 requests/hour**. For a plan-first workflow where every diff is reviewed by a human, that is comfortable. On a reduced-tier model like Kimi K3 (~490/month), it's ~4.5/hour — tight.

---

## 3. Decision gate — should you subscribe?

Subscribe if **all** of these hold:

- [ ] You want a **predictable, capped monthly cost** rather than metered spend
- [ ] Open-weight models (GLM, Qwen, Kimi, MiniMax, DeepSeek) are adequate for your build work
- [ ] You're comfortable with **curated model access** rather than provider-level routing control
- [ ] You have a **fallback** configured (local Ollama and/or OpenRouter) for when limits hit

Stay on pure pay-as-you-go (OpenRouter) if:

- You use **very few tokens** per month — metered will be cheaper than $10
- You need **frontier proprietary models** (Claude, Gemini) as your daily driver — Go doesn't carry them
- You need **provider routing control** (`:nitro`, throughput sorting, excluding slow hosts) — Go is single-curated-provider per model

**Falsifier for this decision:** after the $5 first month, check the console. If actual usage came in under ~$10 of value, cancel and go metered. If you hit the monthly wall repeatedly, keep Go and add OpenRouter as overflow.

> 💡 **Start on the $5 first month specifically to measure this.** It is a one-month, low-cost experiment with a clean exit.

---

## 4. Creating the account

**Note:** Only **one member per workspace** can subscribe to Go. On a team, decide who holds it before anyone pays.

1. Go to **`https://opencode.ai/auth`** and sign in (this is the OpenCode Zen console).
2. Subscribe to **Go** from the console.
3. **Copy your API key.** It has the form `sk-…`.
4. **Immediately check the "Use balance" toggle** and confirm it is **OFF** if you want a hard $10 ceiling (§2).

Store the key like any other credential. OpenCode writes it to `~/.local/share/opencode/auth.json` — **that path must never be committed to Git.**

---

## 5. Connecting Go inside OpenCode

### Option A — TUI (recommended)

```
/connect          → select "OpenCode Go" → paste your sk-… key
/models           → confirm the Go models now appear
```

### Option B — CLI

```bash
opencode auth login          # interactive: pick OpenCode Go, paste key
opencode models              # verify the list
```

### Verify it worked

```bash
opencode -m opencode-go/glm-5.2 run "print the python version you would target"
```

If you get a `404 / model not found`, the model ID prefix is wrong — see §6.

---

## 6. Model IDs and the tier table

**ID format:** `opencode-go/<model-id>` — e.g. `opencode-go/kimi-k3`, `opencode-go/glm-5.2`.

> Same prefix discipline as OpenRouter: the provider prefix is mandatory. `glm-5.2` alone will 404.

### ⚠️ Not every model gets the full 6× multiplier

For some models OpenCode hasn't secured a bulk discount, so those carry a **$15/month** allowance instead of $60. This is the most important table on the page:

| **Full tier — $60/month** | **Reduced tier — $15/month** |
|---|---|
| `glm-5.2` · `glm-5.1` | `glm-5.3` |
| `kimi-k2.7-code` · `kimi-k2.6` | `kimi-k3` |
| `minimax-m3` · `minimax-m2.7` | `grok-4.5` |
| `qwen3.7-max` · `qwen3.7-plus` · `qwen3.6-plus` | `qwen3.8-max` |
| `mimo-v2.5` · `hy3` | `mimo-v2.5-pro` |
| | `gpt-5.6-luna` |
| | `deepseek-v4-pro` · `deepseek-v4-flash` |

**🔑 Counterintuitive and worth internalizing: GLM-5.3 is reduced tier, GLM-5.2 is full tier.** Newer is not better here — GLM-5.2 yields roughly **4,300 requests/month** vs GLM-5.3's **~1,080**. Unless you specifically need 5.3's capability, **default to GLM-5.2.**

### Indicative monthly request counts (full tier highlighted)

| Model | /5 hr | /week | /month |
|---|---|---|---|
| **MiMo-V2.5** ✅ | 30,100 | 75,200 | **150,400** |
| **Qwen3.7 Plus** ✅ | 4,300 | 10,800 | **21,600** |
| **Hy3** ✅ | 4,300 | 10,750 | **21,500** |
| **MiniMax M2.7** ✅ | 3,400 | 8,500 | **17,000** |
| **MiniMax M3** ✅ | 3,200 | 8,000 | **16,000** |
| **Kimi K2.7 Code** ✅ | 1,350 | 3,380 | **6,750** |
| **GLM-5.2 / 5.1** ✅ | 880 | 2,150 | **4,300** |
| **Qwen3.7 Max** ✅ | 340 | 840 | **1,690** |
| GPT 5.6 Luna ⚠️ | 2,050 | 5,100 | 10,250 |
| DeepSeek V4 Flash ⚠️ | 3,800 | 9,450 | 18,900 |
| DeepSeek V4 Pro ⚠️ | 1,050 | 2,600 | 5,200 |
| GLM-5.3 ⚠️ | 220 | 540 | 1,080 |
| Grok 4.5 ⚠️ | 120 | 300 | 600 |
| Kimi K3 ⚠️ | 110 | 250 | **490** |

✅ full tier · ⚠️ reduced tier. Counts are OpenCode's estimates from observed request patterns, not guarantees — heavy-context sessions burn faster.

---

## 7. Config: a plan/build split using Go

Go slots in exactly like any other provider. This pattern keeps planning local and private, sends build work to Go, and denies commits to the agent:

```jsonc
// opencode.json
{
  "$schema": "https://opencode.ai/config.json",

  "agent": {
    // Plan: local, free, private — no Go usage burned on planning
    "plan":  {
      "model": "ollama/qwen3.5:9b",
      "permission": { "edit": "deny", "bash": "ask" }
    },
    // Build: Go full-tier model
    "build": { "model": "opencode-go/minimax-m3" }
  },

  // Keep session titles local so metadata never leaves the machine
  "small_model": "ollama/qwen3.5:9b",

  "permission": {
    "edit": "ask",
    "bash": {
      "*": "ask",
      "git status*": "allow",
      "git diff*": "allow",
      "git commit*": "deny",
      "git push*": "deny",
      "rm -rf*": "deny"
    }
  }
}
```

Switch models mid-session with **`F2`** (cycle recent) or **`/models`** (pick).

**Suggested build ladder, all full tier:**
`opencode-go/minimax-m3` (default, high volume) → `opencode-go/glm-5.2` (stronger reasoning) → `opencode-go/qwen3.7-max` (hardest 20%, most expensive per request).

---

## 8. Monitoring your usage

Track consumption in the console at **`https://opencode.ai/auth`**.

**There is currently no public usage API.** A community request for a `GET /zen/go/v1/usage` endpoint exists (issue #31084) — the server computes rolling/weekly/monthly usage internally but only exposes it to the console UI. `opencode stats` reads the *local* session DB and **will not match** server-side rolling windows, since the 5-hour window is tied to server timestamps rather than a literal "last 5 hours."

**Practical habit:** check the console at the start of week 3. If you're past $30, throttle to a cheaper full-tier model (MiMo-V2.5, MiniMax M2.7) for the rest of the month.

---

## 9. Privacy

Per OpenCode's published table:

| Retention | Models |
|---|---|
| **0 days, not used for training** | GLM (all), Kimi (all), Qwen (all), MiniMax, MiMo, Hy3, DeepSeek\* |
| **30 days** | Grok 4.5, GPT 5.6 Luna |

\* **DeepSeek's zero-retention agreement is renewed monthly**; the version documented on the page runs **through 31 Aug 2026**. Treat this as a recurring watch item, not a settled fact.

**Grok 4.5 caveat:** enabling ZDR disables the stateful Responses API, Files/Collections, and the Batch API.

> 🔒 **Go does not change a local-only data policy.** Regulated, proprietary or personally-identifying data still belongs on local Ollama. Go is for synthetic-data and public-repo work. Keep `small_model` pinned local so even session titles stay on-device.

---

## 10. Migrating from OpenRouter — near drop-in

A typical Ollama + OpenRouter setup maps almost one-to-one. Only the prefix and slug change:

| Before (OpenRouter) | After (Go) | Tier |
|---|---|---|
| `openrouter/minimax/minimax-m3` | `opencode-go/minimax-m3` | ✅ Full |
| `openrouter/z-ai/glm-5.2` | `opencode-go/glm-5.2` | ✅ Full |
| `openrouter/qwen/qwen3.7-max` | `opencode-go/qwen3.7-max` | ✅ Full |
| `openrouter/deepseek/deepseek-v4-pro` | `opencode-go/deepseek-v4-pro` | ⚠️ Reduced |
| `ollama/qwen3.5:9b` | *unchanged* | Local |

Note the **vendor sub-path disappears**: OpenRouter needs `z-ai/glm-5.2`; Go needs just `glm-5.2`.

### What you gain
- Flat, capped cost instead of metered spend
- Curated, benchmarked model/provider pairings — OpenCode tested these specifically for agent use
- One key instead of several billing pages

### What you give up
- **Provider routing control.** No `:nitro`, no throughput sorting, no excluding slow hosts. You rely on OpenCode's failover.
- **Frontier proprietary models.** No Claude or Gemini through Go — those still need OpenRouter or a direct API key.
- **Hard blocking at limits** instead of "it just keeps billing."

> **Recommended posture:** keep both providers configured. Go as primary, OpenRouter as overflow. Costs nothing extra — OpenRouter only charges when used.

**Slow-model note carries over:** DeepSeek V4 Pro's long time-to-first-token in Plan mode is a model/SDK behaviour, not a routing issue. Go does not fix it. Use a fast local model for Plan.

---

## 11. Troubleshooting

| Symptom | Cause / fix |
|---|---|
| `404` / model not found | Missing prefix. Use `opencode-go/glm-5.2`, not `glm-5.2`. Note Go slugs drop the vendor sub-path OpenRouter requires. |
| Go models don't appear in `/models` | Provider not connected → `/connect` → OpenCode Go → paste key. Verify with `opencode auth list`. |
| Requests blocked mid-session | A usage window is exhausted. Check the console, switch to a free model, fall back to Ollama/OpenRouter, or wait for reset. |
| Burning the month too fast | You're on a reduced-tier model (§6). Switch to a full-tier equivalent — `glm-5.3` → `glm-5.2` is the common one. |
| Charged more than $10 | "Use balance" is enabled in the console. Turn it off. |
| Can't subscribe — teammate already has it | One subscriber per workspace by design. |
| `opencode stats` disagrees with the console | Expected. Local DB ≠ server rolling windows. Trust the console. |

---

## 12. Sources & verification

- `opencode.ai/docs/go` — pricing, limits, model list, tier table, endpoints, privacy (page updated 16 Aug 2026)
- `opencode.ai/docs/providers`, `/config`, `/permissions` — provider and permission configuration
- `opencode.ai/auth` — Zen console, subscription management, usage tracking
- GitHub `anomalyco/opencode` issue #31084 — public usage API request (open)

**Re-verify before relying on:** the tier table (§6), the model roster, and the limit values. All three are explicitly flagged as subject to change by OpenCode.

---

*Model rosters and pricing tiers in AI tooling move monthly. Check the docs page's "last updated" date against this guide's verification date before treating any table here as current.*
