Generate a PR description for the current branch.

All context you need has already been injected above this text by
`.github/scripts/pr_prep_context.sh`.

**Do not attempt to load any of it yourself.** This body contains no `!` blocks and no
`@` references by design: command-template substitution is single-pass, so either would
arrive as literal text and silently never run (ADR-0001).

**Check the context first.** If a block above is missing, empty, or shows a line
beginning `CONTEXT_ERROR`, **STOP and report which one**. Do not infer, reconstruct, or
reason from the rules files in place of the missing output.

The `PR TEMPLATE` block defines the structure; follow it **exactly**, in its section
order. The `APPROVED LABELS` block is the only permitted label source.

- **Packs active** — tick only the packs this change touches; they must match the linked
  Issue and the task brief. Cross-check against the `TASK BRIEF FOR THIS BRANCH` block
  and flag any mismatch rather than guessing. Expand and fill only the ticked packs;
  delete the rest.
- **Objective** — problem solved + concrete deliverable
- **Scope** — in scope / out of scope
- **What changed** — files changed/added by area (from `CHANGE SUMMARY`), then the
  high-level approach
- **Architecture & decisions** — ADR added where an alternative was rejected (or state
  why none was needed) · `architecture.dsl` updated if boundaries changed · diagrams
  regenerated via `make diagrams` · README ① Production ② Cost ③ Architecture still
  accurate. Read the `ADR / ARCHITECTURE CHANGES` block; if it is empty and the diff
  contains a real rejected alternative, say so.
- **Acceptance Criteria** — observable outcomes mirrored from the Issue
- **Validation** — the uv-native commands from the template, with pasted results
- **Reproducibility & environment** — `uv.lock` in sync, seeds, config
- **Security & data hygiene** — the template's checklist
- **Risks / Edge Cases** — risk, edge cases covered, rollback
- **Reviewer Notes** — the 2–3 things most likely to be wrong
- **Linking** — `Closes #XX`, taken from the `COMMIT FOOTERS` block. If that block
  reports no footer, leave `<TODO: link Issue>` and flag it.

Also provide:
- A PR title in conventional-commits form: `type(scope): description`, imperative,
  lowercase, <= 72 chars, stating the outcome
- Suggested labels from the `APPROVED LABELS` block only — one sentence each on why
- One paragraph for the GitHub "extended description" / merge body

Rules:
- Do not invent validation results — leave `<TODO: paste output>` where a command
  hasn't run. This command loads no test output by design; `/review` and `/test` are
  where results come from.
- Keep production figures out of the description: the deposition test applies to PR
  text too.

Output everything as one Markdown block I can paste into GitHub.
Do **NOT** create the PR — I create it manually.