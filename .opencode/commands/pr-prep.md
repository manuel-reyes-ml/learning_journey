---
description: Generate a pull request description for the current branch (does not create the PR)
agent: build
---

Generate a PR description for the current branch.

PR format: @.github/templates/pull_request_template.md
Approved labels: @.github/templates/project_labels.md

Change summary:
!`git diff main...HEAD --stat`

Commits on this branch:
!`git log main..HEAD --oneline`

Write the PR description following the template exactly:
- Summary (what and why)
- Changes (organized by module/area with file paths)
- Verification Steps (exact commands + expected outcomes)
- Risk / Impact
- Closes #XX  (read commit footers — Refs/Closes — to find the number)

Also provide:
- A PR title in conventional-commits form showing business impact:
  `type(scope): description`
- Suggested labels from `project_labels.md` only — one sentence each on why
- One paragraph for the GitHub "extended description" / merge body

Output everything as one Markdown block I can paste into GitHub.
Do **NOT** create the PR — I create it manually.
