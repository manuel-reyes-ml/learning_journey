# ADR-0004 — OpenCode owns the plan artifact; `.github/plans/` is the only writable path for a planner

- **Status:** Accepted
- **Date:** 2026-09-03
- **Deciders:** Manuel Reyes
- **Related:** ADR-0003 (command context loading), ADR-0005 (command shell trust boundary)

## Context

`/task-brief` is Gate 1: it produces the execution contract every later build depends
on. The incumbent `.cursor/commands/task-brief.md` saved its output to
`.cursor/plans/issue-<n>-task-brief.md`; the migration to `.github/docs/prompts/`
dropped that step, and the brief became terminal output only.

Under a single harness that was survivable. Under the dual harness it is not: the
planner and the builder are separate processes with separate context windows, so a file
on disk is the only handoff medium. Without it the contract crosses the boundary by
copy-paste — ungoverned, unversioned, and with no record of what was approved.

All 13 project scope documents still document `.cursor/plans/`.

Two constraints shape where the write can happen:

- OpenCode agent `plan-cloud` is `{"edit": "deny", "bash": "deny"}` — the write is
refused as configured.
- Claude Code's `allowed-tools` grants pre-approval, not capability; with `context: fork`
the named subagent supplies the tool set. `agent: Plan` is read-only, so adding `Write`
to `allowed-tools` is inert. Anthropic issues
[#17283](https://github.com/anthropics/claude-code/issues/17283) and
[#49559](https://github.com/anthropics/claude-code/issues/49559) further report that
`context: fork` and `agent:` are sometimes ignored, and an unresolved `agent:` falls
back to `general-purpose` — a *wider* tool pool. That fails open.



## Decision

**OpenCode owns the write. Claude Code reads and reviews briefs but does not produce
them.** `plan-cloud` gains a narrow allowance:

```jsonc
"permission": {
  "edit": { "*": "deny", ".github/plans/**": "allow" },
  "bash": "deny"
}
```

Plan artifacts live at `.github/plans/issue-<n>-task-brief.md`, one file per Issue,
overwritten on regeneration — git history is the audit trail. Every brief carries
frontmatter with `issue`, `issue_updated_at`, `branch`, `generated`, `template`, and
`status: PROPOSAL`. **The agent may never write** `status: APPROVED`**;** only the human
sets it, and a brief at `PROPOSAL` is not an execution contract.

The shared body instructs that if a harness denies the write, the agent outputs the
brief, states it was not persisted, and does not route around the denial. The same body
therefore runs correctly on both harnesses.

## Alternatives considered

**Both harnesses write.** Rejected: duplicated permission surface, no single owner of
the artifact, and the Claude Code path is not reliable enough to carry a boundary given
the fail-open behaviour above.

**Claude Code owns the write** (it is nominally the planner). Rejected on determinism.
OpenCode's permission model is a glob in a versioned config that either matches or does
not; Claude Code's depends on fork behaviour with open defects against it.

`.opencode/plans/` — OpenCode's built-in plan agent natively permits edits to plan
files there. Rejected: harness-specific, so Claude Code could never read briefs from a
neutral path. `.github/` already holds the harness-neutral shared material.

`docs/plans/` — beside `docs/adr/`, recruiter-visible. Rejected: briefs arrive one
per Issue and would bury the ADRs, which carry higher signal. Selected exemplar briefs
can be linked from the README instead.

**Keep** `.cursor/plans/`**.** Rejected: `.cursor/` is a third harness's directory and
neither active harness has a reason to write there.

**Keep the brief as terminal output; human saves it.** Rejected: reintroduces the
copy-paste handoff the file exists to remove, and loses the staleness stamp.

## Consequences

**Positive.** `plan-cloud` stays read-only against all source; the allowance mirrors
what OpenCode's own built-in plan agent does. The brief becomes a versioned artifact
sitting beside the PR it produced — evidence for the plan-then-execute discipline rather
than a claim about it. `issue_updated_at` makes a stale brief detectable.

**Negative.** `plan-cloud` is no longer absolutely read-only; the `// true read-only gate` comment becomes inaccurate and must change. Propagation is owed to 13 scope
documents. Briefs add repository volume.

**Risk.** OpenCode matches edit patterns against worktree-relative paths; absolute or
`~` patterns silently never match, and for a deny rule that fails open
([#40945](https://github.com/anomalyco/opencode/issues/40945)). The pattern must stay
relative, and the allowance must be smoke-tested before it is trusted.

## Falsifier

Reverse if Claude Code's `context: fork` + `agent:` contract becomes reliable and a
scoped `Write(.github/plans/**)` settings rule is confirmed enforced — at which point
planner-writes-plan becomes the more natural division. Re-test after the referenced
Anthropic issues close.