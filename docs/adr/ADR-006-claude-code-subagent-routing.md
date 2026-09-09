# ADR-0006 — Claude Code skills route to `Plan`, not `Explore`, whenever they judge against project standards

- **Status:** Proposed
- **Date:** 2026-09-04
- **Deciders:** Manuel Reyes
- **Related:** ADR-0001 (command context loading), ADR-0002 (plan artifact ownership), ADR-0003 (command shell trust boundary)

> **Numbering note:** ADR-0004 was previously reserved for local-planner fitness (the
> Qwen3.5 9B confabulation finding). That ADR is still owed and unwritten. Either
> renumber it to 0005 or renumber this one — resolve before committing, and check
> `ls docs/adr` for anything already occupying the slot.



## Context

The nine Claude Code skill stubs carry an `agent:` field alongside `context: fork`. The
stubs were not consistent: several existing skills specified `Explore`, and the nine
wrappers written under ADR-0001 specified `Plan`, inherited from the incumbent
`task-brief` stub. No decision had been recorded either way, so the field was being set
by copy rather than by intent.

Claude Code ships built-in subagents. Each is a named, isolated instance with its own
system prompt, context window, tool list and permission mode; intermediate work stays
inside the subagent and only the final output returns to the parent.

`Explore` is a read-only agent for quickly understanding a codebase — search, locate,
map. It runs on Haiku by default for speed and cost, and it **deliberately skips**
`CLAUDE.md` **and git status** to stay cheap.

`Plan` is a read-only research agent used in plan mode to gather context before
proposing a strategy. It loads the project's instruction files.

`general-purpose` has full tool access, including writes.

Both `Explore` and `Plan` are read-only, so the choice between them is not a permission
question. It is a question of what arrives in the subagent's context and what model
runs there.

That distinction is decisive for this command set. Every one of the nine commands
*judges output against project standards* rather than merely locating things:

- `/review` verifies 20+ conventions — structlog kwargs vs `%s` interpolation,
`SecretStr` unwrapping, `stamina` retry shape, layer boundaries
- `/eval` reports scores against thresholds and emits a PASS/FAIL verdict
- `/readme` enforces the flagship bar and the disclosure discipline
- `/commit-msg` applies the conventional-commits rules and the deposition test
- `/task-brief` reproduces nine hard constraints verbatim

An agent that skips `CLAUDE.md` cannot apply standards written in `CLAUDE.md`. Routing
these to `Explore` would strip exactly the context they exist to enforce — and would do
it silently, producing confident output built on general knowledge instead of the house
standard. That is the same failure shape as ADR-0001: the command appears to work.

## Decision

**Route by whether the command judges or merely locates.**

- **Judges output against project standards →** `agent: Plan`**.** Rules must be in context.
- **Only locates or retrieves, applying no standard →** `agent: Explore`**.** The
`CLAUDE.md` skip is a feature there, not a loss.
- **Needs to write → neither.** Both are read-only; see ADR-0002, where the write was
assigned to OpenCode for this reason.

Under this rule **all nine current commands route to** `Plan`**.** No command in the set is
a pure lookup.

Existing skills specifying `Explore` are to be audited against the same question. Any
that apply a convention, threshold or checklist move to `Plan`; any that only find
things stay on `Explore` and the choice gets a one-line comment in the stub recording
why, so the field is never again set by copy.

## Alternatives considered

`Explore` **everywhere, for cost.** Rejected. Haiku with no `CLAUDE.md` is a thin
instrument for a production-readiness verdict or an eval PASS/FAIL, and the savings are
small against a command set that runs a handful of times a day. The failure mode —
standards-shaped output not actually grounded in the standards — is the expensive one.

`general-purpose` **for uniformity.** Rejected. It carries write tools these commands
have no need for, widening the surface for no benefit. `Plan` being read-only is a
property worth keeping.

**Custom subagents in** `.claude/agents/`**, one per command.** Rejected for now as
premature: it duplicates the routing that `agent:` already expresses and adds nine more
files to the drift surface. Revisit if per-command tool restriction becomes necessary.

**Leave the field unset and let Claude route automatically.** Rejected. Auto-selection
is reported as imperfect, and a command whose whole purpose is enforcing a standard
should not have its context composition decided heuristically.

## Consequences

**Positive.** The routing rule is stated once and testable per command: *does this
command apply a project standard?* Stubs get a recorded reason rather than an inherited
value. Read-only is preserved across the set.

**Negative.** `Plan` inherits the session model rather than defaulting to Haiku, so
these skills cost more than an `Explore` route would. Accepted deliberately.

**This decision is conditional, and may currently be inert.** Anthropic issues
[#17283](https://github.com/anthropics/claude-code/issues/17283) and
[#49559](https://github.com/anthropics/claude-code/issues/49559) report `context: fork`
and `agent:` being ignored when a skill is invoked through the Skill tool, in which case
it runs inline in the main session and no subagent is spawned at all. An unresolved
`agent:` also falls back to `general-purpose` — a *wider* tool pool, so it fails open.
There is additionally no way to configure which model a built-in subagent uses; they
inherit the parent, so "Explore runs on Haiku" describes automatic routing and may not
hold for an explicit `agent: Explore`.

Consequently this ADR records intent that the harness may not currently honour. That is
still worth recording: when the field does take effect, it will take effect correctly,
and the reasoning is on paper rather than in one person's memory.

## Verification

One probe settles whether any of this is live. Run a skill with `agent: Explore` and ask
it to quote a line from `CLAUDE.md`.

- **It can quote it** → the fork did not happen; the skill ran inline and `agent:` is
decorative today.
- **It cannot** → the fork is real, `Explore` is genuinely skipping the rules, and the
routing rule above is load-bearing.

Run the same probe with `agent: Plan` as a control; `Plan` should be able to quote it
either way.

## Falsifier

Reverse the blanket `Plan` routing if a per-agent model override lands (requested in
[#35746](https://github.com/anthropics/claude-code/issues/35746)) **and** `Explore`
gains a way to load project instructions — at that point a cheap, rules-aware Explore
would be the better default for the lighter commands such as `/test` and `/commit-msg`.
Re-run the `CLAUDE.md` quote probe after any Claude Code minor-version bump.