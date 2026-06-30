Generate a commit message for the currently staged changes.

1. Run `git diff --staged` to see exactly what is staged
2. Run `git diff --staged --stat` for a file-level summary
3. Write a commit message following conventional commits format:

   type(scope): subject in imperative mood (max 72 characters)

   Body explaining what changed and why. Wrap lines at 72 characters.
   Focus on the "why" — the diff already shows the "what".

   Refs #XX (or Closes #XX if this completes the issue)

4. Use these types: feat, fix, refactor, docs, test, chore, style, perf, ci
5. Scope = the module or area affected (e.g., guardrails, ingest, analytics)
6. Output the complete message in a code block I can copy
7. Do NOT run git commit — I will commit manually after reviewing the message
