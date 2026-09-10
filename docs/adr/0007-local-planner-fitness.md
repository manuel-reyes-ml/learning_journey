# ADR-0007 — The local `plan` agent is not fit to author plans; it is demoted to retrieval

- **Status:** Proposed
- **Date:** 2026-09-04
- **Deciders:** Manuel Reyes
- **Related:** ADR-0001 (command context loading), ADR-0003 (command shell trust boundary)

> **Numbering note:** this record was reserved as ADR-0004 during the harness session and
> renumbered when subagent routing took that slot. Confirm with `ls docs/adr`.

## Context

`opencode.jsonc` defines `plan` as the local planning agent —
`ollama/qwen3.5-16k`, `{"edit": "deny", "bash": "deny"}` — and it carries the privacy
role in the harness. It is the only agent permitted to read DataVault and PostCheck with
non-synthetic data, because a local model means no proprietary content leaves the
machine. Cloud agents are restricted to public, synthetic repos.

During the ADR-0001 investigation this agent was invoked five times with prompts that
contained little or no real content — probe files consisting of a single `echo`, a bare
path, or one literal instruction. It never once reported that it had received nothing.
Every run produced confident, specific, plausible output:

| Run | Prompt actually received | Output produced |
|---|---|---|
| 1 | A bare file path (unresolved `@`) | Plan-mode capability table, offer to read four rule files |
| 2 | One literal `echo` line | "Executive Plan — PII Leakage Remediation", with `basicConfig()` in multiple modules, `sk-abc123…` in plain text, SSNs in raw CSV rows, all marked Critical, prefaced *"After scanning your repo"* |
| 3 | One literal `echo` line | Reconciliation-project requirements questionnaire — data volumes, guardrail modes, LLM choices |
| 4 | One literal `echo` line | DocSync design review with HAML templates, conflict policy, CI integration depth |
| 5 | One `echo` plus "Say DONE" | Multi-phase implementation plan; never said DONE |

Each set of "findings" is a restatement of the `.mdc` rule files loaded through
`instructions[]` — `observability.mdc` supplies structlog, PII redaction and secrets;
`project-scaffold.mdc` supplies uv, `.env`, ruff, mypy, CI. The model converted standards
it had been given into observations it had not made, and attributed them to a repository
scan that took 8.4 seconds and involved no tool calls.

This is not a prompt defect. The prompts were minimal by design, and the correct response
to each was one sentence: *I received no content.* The failure is the model's inability to
represent an empty input as empty.

The consequence is specific to this harness. `plan` exists to plan on regulated
repositories. A task brief's **Files to Change** table is an execution contract that a
build agent then acts on. A planner that invents a PII audit from a rules file will
invent files, line numbers and findings in that table, and — as runs 2 through 5 show —
will do so in the register of a confident specialist. On a repo containing real
participant data, a fabricated "finding" is worse than no finding: it directs attention
and effort at something that does not exist while the real state goes unexamined.

The behaviour has also not been observed on the cloud agents. GLM-5.2 (`plan-cloud`) and
Sonnet (Claude Code) both returned accurate "I received a path, not a file" style reports
in equivalent conditions. The problem tracks the model, not the harness.

## Decision

**`plan` is demoted from planner to retrieval. It may read, locate and quote. It may not
author a plan, a task brief, or any artifact that a build agent will execute against.**

Concretely:

1. **No `/task-brief` on `plan`.** Gate 1 artifacts for regulated repositories are
   authored by a human, optionally assisted by `plan` for retrieval only — "show me every
   file that imports `settings`", not "what should change".
2. **`plan`'s permitted outputs are quotation and location.** File paths, line numbers,
   literal excerpts. Anything it asserts must be traceable to text it can quote.
3. **Every `plan` response is treated as unverified** until a claim is checked against the
   file it names. This is a review obligation on me, not an instruction to the model —
   the model cannot be trusted to flag its own fabrication, which is the finding.
4. **Regulated-repo planning has no agent author.** DataVault and PostCheck task briefs
   are written by hand until a fit local model is available. This is a real cost and is
   accepted rather than worked around.
5. **The privacy story is unchanged.** Proprietary content still never reaches a cloud
   provider. What changes is the claim about what the local agent produces.

## Alternatives considered

**Run a larger local model** — Qwen3.5 32B or similar on the Mac Mini M4. Rejected for
now on hardware: 16GB unified memory makes a 32B model at usable context impractical
alongside Docker and the editor. Revisit on a memory upgrade; this is the most likely
route back to an agent-authored regulated brief.

**Fix it with prompting** — a stronger "say so if context is empty" instruction.
Rejected on evidence. Run 5's prompt ended with "Say DONE. Do nothing else." and the
model produced a multi-phase implementation plan instead. Instruction-following at 9B is
not a control surface for this failure.

**Add a deterministic guard** — a `CONTEXT_ERROR` check the model must acknowledge.
Already implemented in ADR-0001, and worth having, but it does not close this. A model
that fabricates a repo scan can fabricate an acknowledgement.

**Route regulated planning to `plan-cloud`.** Rejected outright: it sends participant
and plan data to a cloud provider. The privacy boundary is not negotiable for a
capability convenience.

**Accept the risk and review the output carefully.** Rejected as the default. It is the
current de facto position and it is exactly the position that let five fabrications pass
as plausible until they were probed deliberately. Careful review is the mitigation for
occasional error, not for a model that fabricates whenever context is thin.

## Consequences

**Positive.** The gap between what `plan` is documented to do and what it can do is
closed. The privacy boundary is preserved. Retrieval — the thing it does reliably —
remains available, and it is genuinely useful for the "where is this used" questions that
dominate early work on an unfamiliar module.

**Negative.** Regulated-repo planning loses agent authorship entirely, which is real
friction on DataVault and PostCheck, the two projects where a brief is most valuable
because the domain rules are most intricate. `AGENTS.md` and the scope documents describe
`plan` as a planning agent and need amending.

**Broader.** This is the same class of finding as ADR-0001 and ADR-0006: a component
documented as doing something it does not do. In those cases the failure was silent
because substitution failed quietly. Here it is silent because the model narrates
success. Both argue for the same discipline — verify by observation, on disk, not by
asking the component whether it worked.

## Verification

Reproducible in one run. Invoke `plan` with a prompt containing only:

```
Say the word DONE.
```

- Replies `DONE` and nothing else → the behaviour has changed; re-open this ADR.
- Produces an analysis, a plan, or a set of "findings" → confirmed, five of five becomes
  six of six.

Run the same prompt against `plan-cloud` as a control.

## Falsifier

Reverse this decision if a local model available within 16GB reports empty input as empty
across five consecutive runs of the probe above, **and** produces a task brief whose
**Files to Change** table contains no path absent from the repository. Both conditions,
not either. Re-test on any Ollama model upgrade or a hardware change.
