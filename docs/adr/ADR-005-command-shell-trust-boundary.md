# ADR-0005 — Command-template shell sits outside the agent permission boundary

- **Status:** Proposed
- **Date:** 2026-09-03
- **Deciders:** Manuel Reyes
- **Related:** ADR-0001 (command context loading), ADR-0002 (plan artifact ownership)
- **Amends:** CORRECTION 39 §11

## Context

CORRECTION 39 §11 rules that *a prohibition written in a command body is persuasion; a
permission denied in an agent is architecture.* The permission block is treated as the
enforcement layer — and on `plan` specifically, as the ERISA privacy boundary for
DataVault and PostCheck non-synthetic runs. `opencode.jsonc` says so in a comment:

```jsonc
"plan": {
  "model": "ollama/qwen3.5-16k",
  "permission": { "edit": "deny", "bash": "deny" }   // true read-only gate
}
```

That claim is false for command-template shell.

Two probes on OpenCode 1.17.9, run on agent `plan` with `"bash": "deny"` in force,
executed shell and wrote marker files to `/tmp`:


| Probe | Body                                                                               | Outcome                  |
| ----- | ---------------------------------------------------------------------------------- | ------------------------ |
| 1     | `!`echo EXPANSION_OK``                                                             | Output reached the model |
| 3     | `!`{ echo NESTED_BASH_OK; ls -la .github/docs/templates/; } > /tmp/probe_out.txt`` | **File created on disk** |


The mechanism explains it: `!` is resolved by the client during template expansion,
before any agent or model is invoked. The agent's `permission` map governs the agent's
*Bash tool*. It does not govern template expansion, because at expansion time there is
no agent yet. `bash: "deny"` and command-template `!` are simply not the same gate.

This is not a defect to route around — it is how the layering works, and ADR-0001
depends on it (the context scripts must run under `plan-cloud`, which is `bash: "deny"`).
The problem is that the boundary was documented in the wrong place, so a reader — or a
future me — could reasonably conclude that a `deny` in `opencode.jsonc` prevents shell
execution on a regulated repository. It does not.

Compounding evidence: the local `plan` agent fabricated repository findings on five of
five runs when handed empty or contentless context (a PII remediation audit, a
reconciliation questionnaire, a DocSync design review), each a restatement of the loaded
`.mdc` rules presented as observation. It never once reported receiving nothing. So the
model cannot be relied on as a backstop either. See ADR-0004 (owed).

## Decision

**The** `permission` **map is the boundary for agent-initiated actions only. Command files
and the scripts they invoke are trusted code, and their boundary is human review plus
pre-commit — not** `opencode.jsonc`**.**

Concretely:

1. `opencode.jsonc` **comments are corrected.** `// true read-only gate` becomes
  `// read-only for AGENT-INITIATED actions; command-template ! is NOT gated here`
   on all three plan agents. A comment that overstates a guarantee is worse than none.
2. **All command shell lives in** `.github/scripts/*.sh` — one reviewable file per
  command, per ADR-0001. Ad-hoc `!` in a wrapper is not permitted; the wrapper's two
   lines are the whole of its shell surface.
3. **Those scripts are read-only by convention, enforced by review.** The one
  deliberate exception is `labels_run.sh`, which writes to GitHub; it is named `_run`
   rather than `_context` precisely so the exception is visible in the wrapper.
4. `bash -n` **on every** `.github/scripts/*.sh` **is added to pre-commit.** Shell that the
  permission layer will not stop must at least be syntax-gated before it lands.
5. **The regulated-data boundary is restated** in `AGENTS.md` as: *no proprietary data
  leaves the machine because the model is local, and no command script exfiltrates
   because every script is reviewed.* Provider routing plus script review — not the
   permission map.



## Alternatives considered

**Treat the bypass as a bug and wait for an upstream fix.** Rejected: it is a layering
consequence, not a defect, and ADR-0001's context scripts require the behaviour. Waiting
would leave the false comment in place indefinitely.

**Forbid** `!` **in command files entirely; have agents fetch context via tools.** Rejected
on evidence. `plan` runs under `bash: "deny"` so its Bash tool genuinely is blocked, and
a 9B model that fabricates five times out of five is not a dependable executor of "read
this file first." This would trade deterministic shell for the exact failure mode ADR-0001
was written to eliminate.

**Route regulated work through a harness without template shell.** Rejected as
unverified: Claude Code's stub uses `!`cat`` at level 1 too, and whether its
`allowed-tools` gates that is untested. Worth probing, but not a basis for a decision
today.

**Leave the comments and rely on knowing the caveat.** Rejected. The whole point of the
`cursor_workflow.md` defect of April 2026 is that an inaccurate written standard
propagates silently for months. A comment asserting a gate that does not exist is that
same defect in config form.

## Consequences

**Positive.** The boundary is now documented where it actually sits. Shell surface is
enumerable — nine scripts, greppable, reviewable in isolation. Pre-commit catches
syntax breakage in files no permission layer will stop. The `_context` / `_run` naming
makes the single side-effecting script visible at the call site.

**Negative.** CORRECTION 39 §11 needs amending rather than merely extending; its
sentence is right for agent actions and wrong for commands, and that distinction has to
be carried in the correction. `plan`'s privacy story becomes two-part (local model +
reviewed scripts) where it read as one-part before, which is more to hold in mind.

**Unresolved.** Whether Claude Code's `allowed-tools` gates level-1 `!` — one probe.
Whether `{file:...}` imports inside `.opencode/agents/*.md` resolve at all; if they
share the single-pass ceiling, the six specialist rule routes (`eval-guardian` →
`testing-and-eval.mdc`, `security-auditor` → `observability.mdc` +
`ai-sdk-patterns.mdc`, and the rest) have never loaded, and the specialist agents have
been running on the three `instructions` rules alone. **This is the highest-value
untested item in the harness and should be probed before the next build session.**

## Falsifier

Reverse if OpenCode gates command-template `!` through the agent `permission` map in a
future release — at which point `bash: "deny"` becomes a true gate, ADR-0001's scripts
break under `plan-cloud`, and both decisions need revisiting together. Re-run probe 3
(marker file to `/tmp` under `bash: "deny"`) after any OpenCode minor-version bump.