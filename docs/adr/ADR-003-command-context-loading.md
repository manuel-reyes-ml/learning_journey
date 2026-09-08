# ADR-0001 — Command context is loaded by level-1 shell; shared bodies are instructions-only

- **Status:** Accepted
- **Date:** 2026-09-03
- **Deciders:** Manuel Reyes
- **Supersedes:** none
- **Related:** ADR-0002 (plan artifact ownership), ADR-0003 (command shell trust boundary)

> **Numbering note:** verify with `ls docs/adr` and renumber if `0001` is taken.

## Context

The dual harness shares one prompt body per command. `.github/docs/prompts/commands/*.md`
is the single source; `.opencode/command/*.md` imports it with `@`, and
`.claude/skills/*/SKILL.md` imports it with `` !`cat` ``. Each body carried its own
context via `` !`shell` `` blocks and `@file` references.

Four probes run on OpenCode 1.17.9 (agent `plan`, Ollama Qwen3.5 9B) established:

| # | Observation | Result |
|---|---|---|
| 1 | `` !`echo` `` in a command file | Executes |
| 2 | `` !`…` `` under agent `"bash": "deny"` | **Still executes** |
| 3 | `@path` in a command file | Injects nothing — literal string only |
| 4 | `` !`…` `` inside a `cat`-imported body | **Never executes** — marker file absent |
| 5 | `$1` inside a level-1 `` !`…` `` | Substitutes before the shell runs |

Probes 3 and 4 were disk-verified (`/tmp` marker files), so they are independent of
model behaviour.

Substitution is single-pass. Every `!` block and `@` reference written inside a shared
body has been arriving at the model as literal text. **No command in the set has ever
received the context it was written to consume.** Nine commands are affected.

The consequences are not uniform in severity:

- `/eval` emits a **PASS/FAIL verdict on eval gates** with no `deepeval` output in
  context. A fabricated PASS propagates into README claims and the flagship checklist.
- `/review` emits a production-readiness report with no `ruff`, `mypy`, `pytest` or
  `uv lock --check` output.
- `/labels` invokes `setup-labels.sh` from inside the body, so **the script has never
  run** and `.github/docs/project_labels.md` may not exist. `/draft-issue` and `/pr-prep`
  both reference that file, so the failure cascades.
- `/commit-msg` writes commit messages without seeing the staged diff.

Observed alongside: the local `plan` agent produced fabricated repository findings on
five of five runs when handed empty context, never once reporting that it had received
nothing. See ADR-0004 (owed).

## Decision

**All command shell moves to level 1, in a per-command context script. Shared bodies
contain instructions only — no `!`, no `@`.**

```
.github/scripts/<command>_context.sh     # the only place shell lives
.github/docs/prompts/commands/<cmd>.md   # instructions only
.opencode/command/<cmd>.md               # 2 level-1 lines
.claude/skills/<cmd>/SKILL.md            # same 2 lines
```

Each wrapper contains exactly:

```
!`bash .github/scripts/<command>_context.sh $1`
!`cat .github/docs/prompts/commands/<command>.md`
```

Every context script emits `CONTEXT_ERROR: …` on any unreadable input, and every body
opens with an instruction to **STOP and report** if a `CONTEXT_ERROR` appears or a
context block is missing. Silent degradation to fabrication is the failure mode this
guards against.

## Alternatives considered

**Swap `@` for `` !`cat` `` inside the bodies.** Rejected: probe 4 shows level-2 `!`
never fires. Fixes the symptom on one reference type and leaves the shell dead.

**Duplicate the `!` blocks into both wrappers.** Rejected: `/review` alone has six
blocks; across nine commands that is 54 lines maintained in two places. This is the
`cursor_workflow.md` defect of April 2026 — a pasted prompt body taught an inverted
logging standard for months. Single-source-no-drift is the invariant.

**One dispatcher script with a `case` per command.** Rejected: couples nine unrelated
context contracts into one file, so a change to `/eval` context can break `/review`.
Per-command scripts are independently reviewable and independently testable.

**Keep bodies as-is and have the agent fetch its own context via tools.** Rejected on
evidence: `plan` runs under `"bash": "deny"`, and a 9B local model that fabricates five
times out of five is not a dependable executor of "read this file first." Deterministic
shell removes the model from the loop.

## Consequences

**Positive.** Context arrival becomes deterministic and disk-verifiable. `CONTEXT_ERROR`
converts a silent fabrication into a visible stop. Single-source is preserved — one
script and one body per command, wrappers stay at two lines. The pattern is identical
on both harnesses.

**Negative.** File count rises by nine scripts. Shell is no longer visible in the body,
so a reader must open two files to see a command whole; each body header names its
script to offset this. Scripts need `bash -n` in pre-commit and are a new executable
surface in the repo.

**Unresolved.** Claude Code's substitution order for `$1` inside `!` is unverified — its
documented order may substitute arguments *after* shell execution, the reverse of
OpenCode. Blocking for the Claude Code wrappers only; the OpenCode side is confirmed.

## Falsifier

Reverse this decision if a harness release makes body-level substitution multi-pass, in
which case shell may return to the shared body and the scripts collapse. Re-test with
probe 4 (level-2 marker file) after any OpenCode or Claude Code minor-version bump.
