# Cursor Agent Task Brief

## Metadata
- **Issue:** #[NUMBER] — [TITLE]
- **Branch:** feature/[number]-[description]
- **Date:** [YYYY-MM-DD]

## Objective
[One paragraph describing the deliverable]

## Hard Constraints
1. **No commits. No pushes.** Human reviews and commits manually.
2. Make minimal, incremental changes.
3. Do not change behavior outside scope.
4. Follow patterns in existing codebase.
5. Keep changes testable: add/adjust tests or validations where appropriate.

## Files to Change
| File | Change | Why |
|------|--------|-----|
| `path/to/file.py` | modify | [reason] |

If additional files need to change, stop and justify before proceeding.

## Execution Steps (do in order)
### Step 1: [Name]
- Edit: `file.py`
- Change: [what to do]
- Validation: `[command]`
- **STOP and report diff**

### Step 2: [Name]
[repeat pattern]

## Acceptance Criteria
- [ ] <criterion 1, written as an observable outcome>
- [ ] <criterion 2>
- [ ] <criterion 3>
- [ ] No breaking changes to existing behavior outside scope.
- [ ] Output remains compatible with: `<downstream function/module>`.

## Edge cases to handle explicitly

- <edge case 1>
- <edge case 2>
- <edge case 3>

If an edge case cannot be addressed without scope expansion, stop and explain tradeoffs.

## Validation Commands
```bash
python -m compileall <relevant_dir>
python -m pytest tests/
python -c "from src import module"
```

## Deliverable summary

When you finish editing files (without committing), provide:

1. **What changed and brief description** (bullet list)
2. **Files changed** (list)
3. **Key logic decisions** (brief)
4. **Exactly what I should review in `git diff`** (callouts)
5. **Exact validation commands** (copy/paste-ready)

## Stop Conditions
Stop and ask if:
- Requirements conflict with existing patterns
- Need to change unlisted files
- Cannot meet criteria without scope expansion
- Unsure about business logic or thresholds.