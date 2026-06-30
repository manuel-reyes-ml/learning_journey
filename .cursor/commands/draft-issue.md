Draft a GitHub Issue for the goal described after this command.

Usage: `/draft-issue Add PII scanning for AI response guardrails`

1. Read `.github/templates/issue_template.md` for the required Issue format
2. Read `.github/templates/project_labels.md` for approved labels
3. Review all modules in `src/` to identify affected files globally
4. Write a complete GitHub Issue following the template, including:

   - Context / problem statement
   - Scope and non-scope
   - Acceptance criteria (checkboxes — explicit and testable)
   - Implementation notes (likely files and functions to change)
   - Edge cases
   - Validation / smoke test plan (commands + expected outcomes)
   - Suggested labels from `.github/templates/project_labels.md` only — explain each choice
   - Risks / impact

5. Suggest an Issue title that is production-grade and recruiter-friendly
6. Output the final Issue body as a Markdown block I can copy and paste into GitHub
7. Do NOT create the Issue — I will create it manually
