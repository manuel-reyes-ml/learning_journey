---
description: Generate a pull request description for the current branch (does not create the PR)
agent: plan-cloud
model: opencode-go/minimax-m3
---

Generate a PR description for the current branch.

PR format: @.github/pull_request_template.md
Approved labels: @.github/docs/project_labels.md

Change summary:
!`git diff main...HEAD --stat`

Commits on this branch:
!`git log main..HEAD --oneline`

ADR / architecture changes on this branch:
!`git diff main...HEAD --name-only -- docs/adr architecture.dsl docs/diagrams README.md`

Write the PR description following the template **exactly**, in its section order:
- **Packs active** — tick only the packs this change touches; they must match the linked
  Issue and the task brief. Expand and fill only those; delete the rest.
- **Objective** — problem solved + concrete deliverable
- **Scope** — in scope / out of scope
- **What changed** — files changed/added by area, then the high-level approach
- **Architecture & decisions** — ADR added where an alternative was rejected (or state why
  none was needed) · `architecture.dsl` updated if boundaries changed · diagrams regenerated
  via `make diagrams` · README ① Production ② Cost ③ Architecture still accurate
- **Acceptance Criteria** — observable outcomes mirrored from the Issue
- **Validation** — the uv-native commands from the template, with pasted results
- **Reproducibility & environment** — `uv.lock` in sync, seeds, config
- **Security & data hygiene** — the template's checklist
- **Risks / Edge Cases** — risk, edge cases covered, rollback
- **Reviewer Notes** — the 2–3 things most likely to be wrong
- **Linking** — `Closes #XX` (read commit footers — Refs/Closes — to find the number)

Also provide:
- A PR title in conventional-commits form: `type(scope): description`, imperative,
  lowercase, ≤72 chars, stating the outcome
- Suggested labels from `project_labels.md` only — one sentence each on why
- One paragraph for the GitHub "extended description" / merge body

Rules:
- Do not invent validation results — leave `<TODO: paste output>` where a command hasn't run.
- Keep production figures out of the description: the deposition test applies to PR text too.
- Ticked packs must match the Issue and the task brief; flag any mismatch rather than guessing.

Output everything as one Markdown block I can paste into GitHub.
Do **NOT** create the PR — I create it manually.