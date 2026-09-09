# ADR-0005 — Both harnesses may write plan artifacts; Claude Code's `/task-brief` runs unforked

- **Status:** Proposed
- **Date:** 2026-09-04
- **Deciders:** Manuel Reyes
- **Amends:** ADR-0002 (plan artifact ownership) — the "OpenCode owns the write" clause only
- **Related:** ADR-0003 (command shell trust boundary), ADR-0004 (subagent routing)

> **Numbering note:** ADR-0004 is contested between subagent routing and the still-unwritten
> local-planner fitness record. Confirm the chain with `ls docs/adr` before committing.

## Context

ADR-0002 assigned the plan-artifact write to OpenCode alone, on the grounds that
OpenCode's permission model is a versioned glob that either matches or does not, while
Claude Code's depends on `context: fork` + `agent:` — a path with open defects against
it ([#17283](https://github.com/anthropics/claude-code/issues/17283),
[#49559](https://github.com/anthropics/claude-code/issues/49559)) that fails *open* to
`general-purpose` when `agent:` fails to resolve.

That reasoning was sound but the conclusion was scoped too widely. It rejected Claude
Code as a writer when what it should have rejected was **the forked path** as the
mechanism. The distinction matters in practice: VS Code with Claude Code is where
planning actually happens in this workflow, and ADR-0002 made the primary planning
surface unable to persist its own primary artifact. Under it, `/task-brief` in VS Code
falls through to shared-body rule 5 — output the brief, state it was not persisted —
which is correct behaviour for a decision that was optimising the wrong thing.

Two further facts, established in ADR-0004, close off the alternatives:

- `Plan` and `Explore` are **both read-only**. Neither can write, whatever
  `allowed-tools` says, because `allowed-tools` grants pre-approval rather than
  capability and the forked subagent supplies the tool set.
- `agent: general-purpose` restores write capability but reintroduces dependence on the
  one field with reliability defects filed against it.

Removing `context: fork` removes the unreliable component from the picture entirely.
With no fork there is no subagent, no `agent:` field to resolve, and no fail-open path.
The boundary moves to `.claude/settings.json`, which is deterministic, versioned and
reviewable — the same relocation ADR-0003 performed for command-template shell.

## Decision

**Both harnesses may write plan artifacts, each scoped to `.github/plans/**` by its own
permission layer.**

- **OpenCode:** unchanged from ADR-0002 —
  `"edit": { "*": "deny", ".github/plans/**": "allow" }` on `plan-cloud`.
- **Claude Code:** `.claude/skills/task-brief/SKILL.md` drops **both** `context: fork`
  and `agent:`, adds `Write` to `allowed-tools`, and relies on
  `.claude/settings.json` → `{ "permissions": { "allow": ["Write(.github/plans/**)"] } }`.

Everything else in ADR-0002 stands unchanged: the path, the one-file-per-Issue naming,
the `status: PROPOSAL` frontmatter, the prohibition on the agent ever writing
`APPROVED`, the staleness stamp, and shared-body rule 5 — which now serves as the
fallback when a permission layer refuses rather than as the expected Claude Code
behaviour.

This makes `/task-brief` the second unforked skill in the set, after `labels`, and for
the same stated reason: a consequential action belongs in the main conversation where it
is visible, not hidden in a background subagent.

## Alternatives considered

**Keep ADR-0002 as written; plan in VS Code, generate briefs in OpenCode.** Rejected: it
splits one Gate 1 step across two applications and makes the artifact's location depend
on which window happened to be open. The copy-paste handoff ADR-0002 existed to
eliminate would return in a new form.

**`agent: general-purpose` with `context: fork`.** Rejected: restores write capability
but keeps the dependency on `agent:` resolving, and its failure mode is a *wider* tool
pool than requested. Trading a working boundary for an isolated context window is the
wrong side of that trade for a command that writes.

**Add `Write` to `allowed-tools` while keeping `agent: Plan`.** Rejected as
non-functional — this was attempted and is inert, since `allowed-tools` cannot grant a
tool the forked subagent does not hold.

**Give Claude Code a custom non-forked subagent in `.claude/agents/`.** Rejected as
premature: it adds a file to the drift surface to express what removing two frontmatter
lines already expresses.

## Consequences

**Positive.** The primary planning surface can persist its primary artifact. The Claude
Code boundary sits in `settings.json` rather than in a field with open defects. Brief
generation is visible in the main thread — for an artifact read line by line before
approval, that is arguably better than isolation.

**Negative.** Two permission layers now grant the same write, so a future change to the
plan path must be made in two places; both are named here and in the stub comment to
limit the drift. Claude Code loses context isolation for this command, so a long brief
occupies the main conversation. The single-owner property of ADR-0002 is gone, and with
it the simplicity of "only OpenCode writes here."

**Unverified at time of writing.** Whether `$1` substitutes *before* the `!` shell runs
on Claude Code — confirmed on OpenCode, and `task_brief_context.sh` cannot resolve the
Issue without it. Whether a `settings.json` `allow` rule silently pre-approves the path.
Both are settled by the probe below; this ADR should not be marked Accepted until they are.

## Verification

Throwaway skill at `.claude/skills/_probe/SKILL.md`, deleted after the run. Invoke as
`/_probe 42`, then check on disk:

```
cat /tmp/cc_probe.txt        # expect: ARG=[42]  then  SHELL_RAN
cat .github/plans/_probe.txt # expect: OK
```

| Observation | Meaning |
|---|---|
| `ARG=[42]` | Args substitute before shell. Design holds. |
| `ARG=[]` or `ARG=[$1]` | Args substitute *after* shell — the Issue number never reaches the script. Fallback: the body instructs the agent to run the script itself via its Bash tool, which this session permits. |
| `/tmp/cc_probe.txt` absent | Level-1 `!` did not run. Check `allowed-tools` includes the Bash pattern. |
| `.github/plans/_probe.txt` exists, no prompt reported | The `allow` rule works; write is silent. |
| Written but prompted | Rule not matching — check the glob and that `settings.json` is project-scoped. |
| Refused | Write unavailable; this decision is not implementable as written. |
| Probe echoes `SHELL_RAN` back as its first line | `!` output reached the model as context, not literal text. |

## Falsifier

Reverse to ADR-0002's single-owner rule if the `settings.json` path scope proves
unenforced, or if unforked skills turn out to inherit permissions in a way that grants
writes beyond `.github/plans/**`. Re-run the probe after any Claude Code minor-version
bump, and re-open the forked option if #17283 and #49559 close.
