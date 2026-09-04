Generate a commit message for the currently staged changes.

All context you need has already been injected above this text by
`.github/scripts/commit_msg_context.sh`.

**Do not attempt to load any of it yourself.** This body contains no `!` blocks and no
`@` references by design: command-template substitution is single-pass, so either would
arrive as literal text and silently never run (ADR-0001).

**Check the context first.** If a block above is missing, empty, or shows a line
beginning `CONTEXT_ERROR`, **STOP and report which one**. Do not infer, reconstruct, or
reason from the rules files in place of the missing output.

Write a commit message in **conventional commits** format, from the `STAGED DIFF` block:

    type(scope): subject in imperative mood (max 72 characters)

    Body explaining what changed and WHY (the diff shows the what).
    Wrap body lines at 72 characters.

    Refs #XX   (or Closes #XX if this completes the issue)

Rules:
- Types: feat, fix, refactor, docs, test, chore, style, perf, ci
- Scope = module/area affected (e.g. guardrails, ingest, analytics, adr, observability)
- Subject: imperative, lowercase, no trailing period
- `style` means `ruff format` / `ruff check --fix`. **Black is retired** — never
  reference it in a commit message.
- If the staged diff removes or relocates content, state in the body **where each piece
  landed** — a deletion commit that doesn't carry the mapping loses it (git won't detect
  a rename when one file becomes several).
- **Keep production figures out of the message.** The deposition test applies to git
  history too: no absolute dollar amounts, participant data, or client identifiers.
  *(Crucible: no P&L, returns, or account figures.)*
- If the diff contains a decision with a real rejected alternative and the `ADRs STAGED`
  block is empty, say so before writing the message.
- Do not add a Co-Authored-By trailer. `includeCoAuthoredBy` is off in this repo.
- Output the complete message in a single code block I can copy.
- Do **NOT** run `git commit` — I commit manually after review. The PreToolUse hook
  blocks it in any case.