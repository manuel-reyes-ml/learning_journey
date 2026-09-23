# ADR-0008 — `.claude/rules/` files are generated from `.cursor/rules/`, not imported

- **Status:** Proposed
- **Date:** 2026-09-22
- **Deciders:** Manuel Reyes
- **Related:** ADR-0001 (command context loading), ADR-0006 (per-harness mechanisms)

> **Numbering note:** ADR-0004 is still contested between subagent routing and the
> local-planner fitness record, and 0007 was issued against that unresolved chain.
> Confirm with `ls docs/adr` before committing this as 0008.

## Context

The Claude Code harness was installed with `.claude/rules/*.md` as thin pointer files.
Each carried a one-line description and an `@` import of the canonical rule body:

```markdown
---
paths:
  - "**/app/**"
  - "**/pages/**"
---

Streamlit structure, masking at display boundaries.

@.cursor/rules/streamlit-patterns.mdc
```

The setup document recorded this as **the one uncertain piece** in the harness: Claude
Code documents `@path` imports for `CLAUDE.md` and `AGENTS.md`, and the `.claude/rules/`
section of the documentation never claims them. The failure mode would be silent, and
the check was deferred. It was never run — for roughly three weeks, whether eight rule
bodies reached Claude Code at all was unknown.

It has now been probed directly.

## The probe

A canary line, `MARKER_STREAMLIT_RULE_LIVE_4417`, was appended to the bottom of
`.cursor/rules/streamlit-patterns.mdc`. An empty `app/test.md` was created to give the
`**/app/**` glob something to match. Each run was a fresh session in plan mode, and each
asked for a context-only search with no tools after the triggering Read — with tools, the
model could grep the file and answer yes regardless of what loaded.

| # | Condition | Stub text present | Marker present |
|---|---|---|---|
| 1 | No file under `app/` read (control) | No | No |
| 2 | `ls app/` only, no Read (accidental second control) | No | No |
| 3 | `Read app/test.md`, stub as written (`@.cursor/...`) | **Yes** | **No** |
| 4 | `Read app/test.md`, stub rewritten (`@../../.cursor/...`) | **Yes** | **No** |

Runs 1 and 2 confirm the `paths:` glob is honoured and that the trigger is a Read, not a
directory listing — consistent with the documented behaviour that path-scoped rules fire
when Claude reads a matching file.

Runs 3 and 4 are decisive. In both, the injected `<system-reminder>` block showed the
rule file's own text followed by the import line **as literal characters**:

```
Streamlit structure, masking at display boundaries.
@../../.cursor/rules/streamlit-patterns.mdc
```

Run 4 rules out the obvious alternative explanation. Relative import paths resolve
against the file containing the import, not the working directory, so the original
`@.cursor/...` would have resolved to the non-existent
`.claude/rules/.cursor/rules/streamlit-patterns.mdc`. Correcting the path to `../../`
changed nothing: the line still arrived literally. **The cause is the mechanism, not the
path.**

One incidental finding, worth its own note: in run 3 the agent classified the injected
rule block as a prompt-injection attempt and declined to trust it, because the text
arrived after a tool result it had not requested. That is correct instinct on unfamiliar
input, but it means a path-scoped rule can be *received and then discounted*. Rules are
context, not enforcement; anything that must hold regardless belongs in `guard.py`.

## Decision

**`.claude/rules/*.md` are generated artifacts, built from `.cursor/rules/*.mdc` by
`scripts/build_claude_rules.py`, and never hand-edited.**

This is the third instance of the same pattern already used in this repo — `make
diagrams` renders Mermaid from `architecture.dsl`, and `make claude-agents` renders
`.claude/agents/` from the shared prompt bodies, for the same reason: the consuming tool
has no import mechanism, so one source is rendered to a committed copy, and a
`--check` mode in pre-commit fails the commit when the copy drifts.

Mapping rules:

- Cursor's `globs:` becomes Claude Code's `paths:`. Inline lists, comma-separated
  scalars and block lists are all accepted.
- Cursor's `alwaysApply: true` emits **no** `paths:` field. A Claude rule without one
  loads unconditionally, which is the same semantics.
- A source with neither field emits no `paths:` and prints a note. Loading
  unconditionally is the safe failure; a rule that never loads is worse than one that
  always does.
- `learning-mode.mdc` is excluded: it is consumed by the `learn` output style, which
  `build_claude_agents.py` already generates.
- Rendering happens for every source before any file is written, so a malformed `.mdc`
  leaves the rules directory untouched rather than half-regenerated.
- A generated file whose `.mdc` source has been deleted fails `--check`. It would
  otherwise keep injecting a retired standard into every session.

## Consequences

**Each rule body now exists twice on disk.** That is the real cost and it is not hidden:
`.cursor/rules/<name>.mdc` is the source, `.claude/rules/<name>.md` is a machine copy
carrying a `GENERATED FILE — DO NOT EDIT` banner. The copy cannot drift silently because
`claude-rules-check` runs in pre-commit and fails on any divergence in either direction —
an edited source, or a hand-edited output.

**Block-level HTML comments in memory files are stripped before injection**, so the
banner costs no context tokens.

**Every rule that Claude Code has ever loaded until now was a one-line description.**
Any judgement it made against "the project standards" during that window was made
without them. Work produced in Claude Code sessions since the harness install is
unreviewed against the actual rule bodies.

**OpenCode is unaffected** — it reads the `.mdc` files through its `instructions` array.
`CLAUDE.md → @AGENTS.md` is also unaffected: imports work in `CLAUDE.md`, and `/context`
confirms both files load.

## Alternatives considered

**Symlink `.claude/rules/<name>.md` to the `.mdc` file.** No generator, no second copy;
`.claude/rules/` supports symlinks. Rejected because the symlinked file would carry
Cursor's frontmatter (`description`, `globs`, `alwaysApply`) and no `paths:` field, so
every rule would load unconditionally and the context saving of path scoping would be
lost. Adding `paths:` to the `.mdc` frontmatter to serve both tools is possible but
untested on the Cursor side, and a failure there breaks the canonical source rather than
a generated copy.

**Import the `.mdc` files from `CLAUDE.md` instead.** Documented to work, and it was the
fallback named in the setup guide. Rejected because imports load at launch
unconditionally: all eight rule bodies would enter every session, which is the 85%
always-on load reduction from the earlier rules restructure given straight back.

**Inline the rule bodies into `.claude/rules/` by hand.** Same on-disk result as the
generator, minus the guarantee. Rejected — a hand-maintained second copy is drift
waiting to happen, which is the failure this repo's single-source discipline exists to
prevent.

## Falsifier

Re-run the probe after any Claude Code minor-version bump, and drop the generator if
`.claude/rules/` gains `@` import expansion: the pointer form is strictly better when it
works. The probe is cheap — marker line, empty file under a matching glob, fresh session,
context-only question.

Also re-run it if the `InstructionsLoaded` hook is adopted, which logs which memory and
rules files loaded and when. That log is stronger evidence than a model's self-report and
would settle the question without a canary.
