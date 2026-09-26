# ADR-002 — Claude Code Model Ladder

**Status:** Accepted · **Date:** 2026-08-31 · **Supersedes:** nothing — first record of this routing
**Roadmap:** v10.0, CORRECTION 42 · **Deciders:** Manuel Reyes
**Companion:** ADR-001 §5 records the *OpenCode* ladder. This is the *Claude Code* ladder. **Two harnesses, two ladders, one governing invariant.**
**Review gate:** first `/usage` reading after two weeks of dual-harness operation (see §8)

---

## 1. Context

CORRECTION 42 reverses the CORRECTION 39 §9 decline and adopts Claude Code as a scoped
read-only reviewer alongside OpenCode. That adoption shipped **five generated subagents,
nine skills and an output style with no recorded model routing** — the same gap ADR-001
§1 was written to close for OpenCode, reproduced one harness over.

The routing in use today is *a preference with no record behind it*. This ADR converts it
into a decision with falsifiers.

Three constraints shape it:

| Constraint | Implication |
|:---|:---|
| **Subscription, not API billing** | The scarce resource is **allowance**, not dollars |
| **Claude Code is read-only here** | Errors surface as bad *advice*, not bad *diffs* |
| **25 hrs/week** (CORRECTION 42 §2) | Escalation must be default-off, not default-on |

---

## 2. Decision

**A three-tier ladder, assigned per agent, with Sonnet as the unstated default and both
ends of the range requiring a reason.**

| Agent | Tier | Why |
|:---|:---|:---|
| `docs-sync` (report) | **Haiku** | Diff-and-report. Mechanical by construction |
| `docs-fix` (writes docs) | **Haiku** | Prose edits against a known template |
| `eval-guardian` | **Sonnet** | A blocking gate. Judgement, and a wrong pass is silent |
| `security-auditor` | **Sonnet** | Judgement — ⚠️ but see §6, this one has a hazard |
| `pattern-scout` | **Opus** | Cross-cutting pattern recognition across unfamiliar code |
| 9 skills (`/review`, `/test`, …) | **inherit** | One-shot; §6 of ADR-001 applies — commands inherit |
| Session default | **Sonnet** | Escalate on evidence, not on anticipation |

**Aliases, not pinned versions.** `haiku` · `sonnet` · `opus` — full names go stale, and
a model family alias resolves to the newest version of its family. ⚠️ Aliases can resolve
differently across the API, AWS, Bedrock, Vertex and Foundry, so **this ruling is dated
and applies to the Claude Code extension on a personal subscription.**

---

## 3. Why Sonnet is the floor and not Haiku

The naive reading of a three-tier ladder is "put everything cheap on Haiku and escalate."
That is wrong here for a specific reason.

Haiku's documented sweet spot is **volume** — exploration subagents, mechanical fan-out
stages such as file reading, searching and formatting, and high-throughput workflow
stages. `docs-sync` and `docs-fix` are exactly that shape. `eval-guardian` is not.

> 🔑 **The dividing line is not effort, it is whether a wrong answer is visible.**
> A bad docs diff is caught by reading it. A bad *pass* from `eval-guardian` is caught by
> nothing — it is the thing that was supposed to do the catching.

This is the §7 gate logic of ADR-001 applied to model choice instead of write permission:
spend where errors propagate silently.

---

## 4. Why `pattern-scout` gets Opus

`pattern-scout` is the only agent asked to find something the human did not already know
to look for. Every other agent checks a *named* condition. The published guidance points
the same way: pairing a strong planner with cheaper workers is described as the
highest-leverage routing decision most teams make.

Volume is the reason this is affordable — `pattern-scout` runs on request, not on every
session.

⚠️ **Recorded honestly:** Anthropic has not published a Sonnet 5 versus Opus 5
head-to-head. Sonnet 5 scores 63.2% on SWE-bench Pro against Opus 4.8's 69.2%, and Opus 5
more than doubled Opus 4.8 on Frontier-Bench — so the Sonnet-to-Opus-5 gap is **probably
wider than six points, not narrower.** That is an inference, not a measurement, and the
ADR-001 §9 rule applies: **treat any leaderboard delta under ~5 points as noise.**

---

## 5. ❗ The cost model is not the one you would assume

**On a subscription there is no per-token bill.** The list prices — Sonnet 5 at an
introductory $2/$10 moving to the standard $3/$15, Fable 5 at $10/$50 — describe API
billing, not this account.

What is actually consumed is **allowance**, and every forked skill and subagent opens its
own context window drawing on the same pool as claude.ai chat.

> ⚠️ **Consequence that inverts the intuition:** a Haiku subagent that opens a context
> window is not free. **Fan-out costs more than tier choice saves.** The lever with real
> leverage is *how many subagents fire*, not which model each one runs.

**`/usage` is the instrument.** It breaks the draw down per skill and per agent. Until a
reading exists, every number in this section is a list price, not an observation.

---

## 6. ⚠️ The hazard: classifier fallback on `security-auditor`

This is the finding that most affects the routing, and it is not obvious.

Opus 5 and Fable 5 run safety classifiers for cybersecurity and biology. On Opus 5,
**cybersecurity-flagged requests re-run on Opus 4.8**, and after a fallback **the session
stays on the fallback model** until `/model` is run. The trigger can fire on the first
request of a session, because that request already carries repository content.

| Consequence | Why it matters here |
|:---|:---|
| A `security-auditor` run may silently change model mid-session | The agent whose job is security is the likeliest to trip a security classifier |
| The switch persists | Later, unrelated work runs on the fallback without notice |
| `pattern-scout` on Opus inherits the same exposure | It reads broadly, including security-adjacent code |

**Ruling:** `security-auditor` stays on **Sonnet**, not Opus — not because it needs less
judgement, but because it is the agent most likely to trip the classifier, and a silent
mid-session model change is exactly the kind of unrecorded state this file exists to
prevent. **Run `/model` after any `security-auditor` session** to confirm the tier.

Separately, availability fallback chains are configurable via `--fallback-model
sonnet,haiku` or a `fallbackModel` array, and fire on overload — **authentication,
billing, rate-limit, request-size and transport errors explicitly never trigger a
switch.** Not configured here; noted so a future reader does not confuse the two
mechanisms.

---

## 7. Alternatives evaluated and declined

Every decline carries a falsifier.

| Option | Why declined | Falsifier |
|:---|:---|:---|
| **Flat Sonnet everywhere** | The honest baseline, and cheaper to reason about. Declined because it puts the same tier on `docs-sync` (mechanical, high volume) and `pattern-scout` (open-ended discovery) — the one routing distinction that carries real value | `/usage` shows tier choice accounts for <10% of variance in allowance draw → collapse to flat Sonnet and delete this ADR |
| **Flat Haiku, escalate manually** | Puts a silent-failure agent (`eval-guardian`) on the weakest tier. The failure mode is a false pass, which no later step catches | Two weeks of `eval-guardian` on Haiku produce zero missed findings on a seeded test |
| **`opusplan` mode** | Genuinely attractive — Opus plans, Sonnet implements. Declined **only because Claude Code is read-only in this harness** and there is no implementation phase for it to cheapen | Claude Code is ever granted write permission → revisit immediately; this becomes the obvious default |
| **Opus as session default** | Escalation-by-anticipation. Also maximises §6 classifier exposure across all work, not just security work | A recorded case where Sonnet's session-level output caused a wrong architectural call |
| **Fable 5 for `pattern-scout`** | Loses seven of eight quantified head-to-head evals against Opus 5 at double the price. **Worse and dearer** | Anthropic publishes a head-to-head where Fable leads on discovery-shaped tasks |
| **Pinned version strings** (`claude-sonnet-5`) | Full model names are the ones that go stale; aliases track the family | A reproducibility requirement appears that needs a frozen version |

---

## 8. Consequences

### Positive

- **Routing is now recorded and falsifiable** rather than a preference
- The §6 classifier hazard is **written down before it bites**, not after
- `/usage` gives a real instrument; §5 replaces guessed economics with a measurement plan

### Negative — accepted

- **Three tiers is more state to hold** than flat Sonnet, for benefit that is asserted and not yet measured
- **Every §4 and §5 figure is a list price or a third-party benchmark**, not an observation from this account
- **Subagent frontmatter is generated** by `scripts/build_claude_agents.py` — a model change means editing the `AGENTS` table and re-running `make claude-agents`, then **restarting Claude Code**, because agent files are read once at session start

### ❓ Open — by observation, not assumption

1. **What does fan-out actually cost against tier choice?** Run `/usage` after two weeks. **If fan-out dominates, §2 is close to irrelevant and should be simplified.**
2. **Does `security-auditor` trip the cybersecurity classifier in practice?** Run it once on a repo with `guard.py` and the gitleaks config present — both are security-shaped by content.
3. **Does the `model:` frontmatter field survive the generator round-trip?** The `skills:` field silently resolved to nothing once already; that defect is precedent, not paranoia.

---

## 9. Review

**Trigger:** first `/usage` reading after two weeks of dual-harness operation.

**Decide:**
1. Fan-out dominates the draw → **collapse to flat Sonnet**, keep only the `pattern-scout` exception
2. `eval-guardian` produces no findings Haiku would have missed → demote it, record why
3. `security-auditor` trips the classifier → record the observed behaviour in §6 and add `/model` to the skill's closing step
4. Claude Code gains write permission → `opusplan` is reconsidered first, before anything else in §7

---

> **Legend:** ✅ full tier · ⚠️ caveat / hazard · 🔒 binding · ❓ open · 🔑 key distinction
> **Verification date:** 2026-08-31, against Claude Code model-configuration docs and
> published model-selection guidance. **Model rosters, aliases and prices move monthly —
> re-verify §2 and §5 before treating any figure here as current.**
