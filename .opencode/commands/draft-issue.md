---
description: Draft a production-grade GitHub Issue from a one-line goal (does not create it)
agent: plan
---

Draft a GitHub Issue for this goal: **$ARGUMENTS**

Reference material:
- Issue format: @.github/ISSUE_TEMPLATE/task.md
- Approved labels: @.github/docs/project_labels.md

Repository modules (to identify affected files):
!`find src -name '*.py' | head -100`

Write a complete Issue following the template, including:
- Context / problem statement
- Scope and non-scope
- Acceptance criteria (explicit, testable checkboxes)
- Implementation notes (likely files/functions to change)
- Edge cases
- Validation / smoke-test plan (commands + expected outcomes)
- Suggested labels — from `project_labels.md` ONLY — one sentence each on why
- Risks / impact

Also suggest a production-grade, recruiter-friendly Issue title.

Output the final Issue body as one Markdown block I can paste into GitHub.
Do **NOT** create the Issue — I create it manually.