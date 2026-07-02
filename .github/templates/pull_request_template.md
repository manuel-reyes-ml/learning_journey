<!--
PULL REQUEST TEMPLATE
Purpose: Keep PRs consistent, reviewable, and portfolio-ready (DA/DE showcase).
Notes:
- Do NOT include real SSNs/DOBs/account numbers or any sensitive client data.
- Prefer screenshots of masked/synthetic outputs if needed.
-->

# ✅ PR Summary

## 🎯 Objective
**What problem does this PR solve?**  
<!-- Example: Fix Roth Engine 59½ year-end attainment logic and normalize rollover code handling -->

**Expected output / deliverable**  
<!-- Example: Corrected Engine C logic + updated notebook validation cells -->
---
## 📌 Scope

### In scope
- [ ] <!-- e.g., Update Engine logic in `src/...` -->
- [ ] <!-- e.g., Expand correction_reason traceability -->
- [ ] <!-- e.g., Update notebooks for validation -->

### Out of scope
- <!-- e.g., Backfilling historical years or refactoring unrelated modules -->
---
## 🧩 Implementation Plan (What changed)

### Files changed / added
- [ ] `src/...`
- [ ] `docs/...`
- [ ] `notebooks/...`
- [ ] `tests/...`

### High-level approach
1. <!-- Step 1: Describe the change at a conceptual level -->
2. <!-- Step 2 -->
3. <!-- Step 3 -->
---
## 🧠 Data + Logic Notes

### Business rules implemented / updated
- **Rule(s):** <!-- concise description -->
- **Threshold(s):** <!-- e.g., 59.5 (attained by 12/31), 55 rule -->
- **Exclusions / locks:** <!-- e.g., excluded-from-engine vs tax-code-locked -->

### Canonical schema impact
- **New columns added:** <!-- list if any -->
- **Columns modified:** <!-- list if any -->
- **No schema change:** [ ] (check if true)

### Data quality considerations
- **Join keys:** <!-- e.g., plan_id + ssn -->
- **Null-handling:** <!-- e.g., missing DOB/term_date behavior -->
- **Type enforcement:** <!-- e.g., dates/numerics normalized -->
- **Idempotence:** <!-- does rerunning produce stable results? -->
---
## 🧪 Validation (Local)

### Smoke checks
- [ ] `python -c "import src"` passes
- [ ] Key module import(s) run without error
- [ ] Notebook cell(s) run without error

### Data quality checks
- [ ] No duplicate keys where uniqueness is required
- [ ] Expected columns exist in canonical schema
- [ ] Dtypes verified (dates/Int64/Float64)

### Validation (executed)
```bash
source .venv/bin/activate
python -m pytest tests/
```

Results:

### Rule verification (recommended)
- [ ] Added/updated notebook examples for key scenarios:
  - [ ] Attained 59½ within txn_year
  - [ ] Under 59½ with term_date (attained 55 within term_year)
  - [ ] Under 59½ without term_date (attained 55 within txn_year)
  - [ ] Rollover normalization cases (B+G, G+blank, blank+G)
  - [ ] “tax-code locked” rows still evaluated for taxable/basis/year logic

### Export checks (if applicable)
- [ ] Output opens in Excel and columns populate correctly
- [ ] Template headers found (no misalignment)
---
## ✅ Acceptance Criteria
- [ ] AC1: <!-- measurable outcome -->
- [ ] AC2:
- [ ] AC3:
---
## 🧯 Risks / Edge Cases

- **Potential risk:** <!-- e.g., DOB missing leads to skipped age logic -->
- **Edge cases covered:** <!-- missing DOB/term_date; NaNs; duplicate SSN per plan -->
- **Mitigation:** <!-- e.g., INVESTIGATE action + correction_reason tokens -->
---
## 📎 Reviewer Notes

### What to focus on
- <!-- correctness of business rules -->
- <!-- correctness of masks / precedence -->
- <!-- clarity of correction_reason -->
- <!-- no sensitive data committed -->

### Screenshots / sample outputs (optional)
<!-- Attach masked screenshots or paste small masked tables. Avoid any sensitive values. -->
<details>
<summary>pytest run output (local)</summary>

<!-- attach screenshot here -->

</details>
---
## 🔗 Linking
- Closes #<issue-number>
