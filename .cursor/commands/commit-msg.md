Generate a commit message for the currently staged changes.

1. Run `git diff --staged` to see exactly what is staged
2. Run `git diff --staged --stat` for a file-level summary
3. Write a commit message following conventional commits format:

   type(scope): subject in imperative mood (max 72 characters)

   Body explaining what changed and why. Wrap lines at 72 characters.
   Focus on the "why" — the diff already shows the "what".

   Refs #XX (or Closes #XX if this completes the issue)

4. Use these types: feat, fix, refactor, docs, test, chore, style, perf, ci
5. Scope = the module or area affected (e.g., guardrails, ingest, analytics, adr, observability)
6. `style` means `ruff format` or `ruff check --fix`. Black is retired — never reference it
   in a commit message, a hook, or a Makefile target
7. If the staged diff removes or relocates content, state in the body where each piece landed.
   Git will not detect a rename when one file becomes several, so the message has to carry
   the mapping or it is lost
8. Keep production figures out of the message — the deposition test applies to git history
   too: no absolute dollar amounts, participant data, or client identifiers. Crucible carries
   a parallel rule: no P&L, returns, or account figures
9. If the diff contains a decision with a real rejected alternative and no ADR is staged,
   say so before writing the message
10. Output the complete message in a code block I can copy
11. Do NOT run git commit — I will commit manually after reviewing the message