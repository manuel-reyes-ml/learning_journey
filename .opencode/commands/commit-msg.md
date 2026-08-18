---
description: Generate a conventional-commits message for staged changes (does not commit)
agent: plan-cloud
model: opencode-go/minimax-m3
subtask: true
---

Generate a commit message for the currently staged changes.

Staged changes (full):
!`git diff --staged`

File-level summary:
!`git diff --staged --stat`

Write a commit message in **conventional commits** format:

    type(scope): subject in imperative mood (max 72 characters)

    Body explaining what changed and WHY (the diff shows the what).
    Wrap body lines at 72 characters.

    Refs #XX   (or Closes #XX if this completes the issue)

Rules:
- Types: feat, fix, refactor, docs, test, chore, style, perf, ci
- Scope = module/area affected (e.g. guardrails, ingest, analytics, adr, observability)
- Subject: imperative, lowercase, no trailing period
- `style` means `ruff format` / `ruff check --fix`. **Black is retired** — never reference
  it in a commit message.
- If the staged diff removes or relocates content, state in the body **where each piece
  landed** — a deletion commit that doesn't carry the mapping loses it (git won't detect a
  rename when one file becomes several).
- **Keep production figures out of the message.** The deposition test applies to git history
  too: no absolute dollar amounts, participant data, or client identifiers. *(Crucible: no
  P&L, returns, or account figures.)*
- If the diff contains a decision with a real rejected alternative and no ADR is staged,
  say so before writing the message.
- Output the complete message in a single code block I can copy
- Do **NOT** run `git commit` — I commit manually after review