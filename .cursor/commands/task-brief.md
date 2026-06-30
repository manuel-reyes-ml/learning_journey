Generate a complete Cursor Agent Task Brief for the Issue number provided after this command.

Usage: `/task-brief 12` (where 12 is the GitHub Issue number)

1. Read `.github/templates/cursor_task_brief.md` for the required Task Brief format
2. Fetch the Issue details: run `gh issue view <number>` to get scope, acceptance criteria, and context
3. Review all modules in `src/` and `tests/` to identify the exact files that need to change
4. Fill in every section of the template:

   - **Metadata:** Issue number, branch name (`feature/<number>-<short-description>`), today's date
   - **Objective:** One paragraph from the Issue context
   - **Hard Constraints:** Keep the 5 standard constraints (no commits, minimal changes, etc.)
   - **Files to Change:** Table with exact file paths, change type, and reason for each
   - **Execution Steps:** Ordered steps with specific edits, each ending with "STOP and report diff"
   - **Acceptance Criteria:** Copy from Issue + add "no breaking changes" and "output compatible with downstream"
   - **Edge Cases:** From the Issue + any you discover from reviewing the codebase
   - **Validation Commands:** Exact commands: `python -m compileall`, `pytest`, `make lint`
   - **Deliverable Summary:** Keep the standard 5-item deliverable format
   - **Stop Conditions:** Keep the standard 4 stop conditions

5. If any file not listed in the Issue appears to need changes, flag it explicitly
6. Save the completed brief to `.cursor/plans/issue-<number>-task-brief.md`
7. Output the brief so I can review and approve before implementation begins
8. Do NOT start implementing — brief review is Gate 1
