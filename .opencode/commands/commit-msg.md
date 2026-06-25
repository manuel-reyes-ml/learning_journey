---
description: Generate a conventional-commits message for staged changes (does not commit)
agent: build
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
- Scope = module/area affected (e.g. guardrails, ingest, analytics)
- Subject: imperative, lowercase, no trailing period
- Output the complete message in a single code block I can copy
- Do **NOT** run `git commit` — I commit manually after review
