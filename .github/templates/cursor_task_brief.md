# Cursor / OpenCode Agent Task Brief

<!--
 Feed this to the coding agent. The agent EXECUTES but never commits.
 Fill CORE, tick the packs, and fill ONLY the ticked packs at the bottom.
 Packs here must match the linked Issue and the eventual PR.
-->

## Metadata
- **Issue:** #[NUMBER] — [TITLE]
- **Branch:** `feature/[number]-[slug]`
- **Date:** [YYYY-MM-DD]
- **Packs active:** [ ] 🟦 DE  [ ] 🟩 ML  [ ] 🟪 LLM/RAG  [ ] 🟧 Agentic  [ ] ⬜ None

## Objective
[One paragraph describing the deliverable.]

## Hard Constraints
1. **No commits. No pushes.** Human reviews and commits manually (final gate).
2. Minimal, incremental, **additive-first** changes. Replacements require explicit approval.
3. Do not change behavior outside scope.
4. Follow existing codebase patterns (`src/` layout, typed, `logging` not `print`, `pyproject.toml`).
5. Keep changes testable: add/adjust tests or validations where appropriate.
6. **No secrets, no real client data** in code, tests, or notebook output.
7. **Autonomy limit:** propose-and-pause. The agent must **not** trigger any irreversible or
   external side-effect (network writes, deletes, live orders, posting). Surface them for human action.

## Files to Change
| File | Change | Why |
|------|--------|-----|
| `path/to/file.py` | modify | [reason] |

If additional files must change, **stop and justify** before proceeding.

## Execution Steps (in order)
### Step 1: [Name]
- Edit: `file.py`
- Change: [what to do]
- Validation: `[command]`
- **STOP and report the diff.**

### Step 2: [Name]
[repeat pattern — one reviewable diff at a time]

## Acceptance Criteria
- [ ] <observable outcome 1>
- [ ] <observable outcome 2>
- [ ] No breaking changes outside scope.
- [ ] Output stays compatible with: `<downstream module/function>`.

## Edge Cases to Handle Explicitly
- <edge case 1: nulls / dupes / missing keys>
- <edge case 2: empty input / malformed row>
- <edge case 3>

If an edge case needs scope expansion, **stop and explain tradeoffs.**

## Validation Commands
```bash
source .venv/bin/activate
python -m compileall src
python -c "import <package>"
python -m pytest -q
```

## Deliverable Summary (report back, no commit)
1. **What changed** (bullets)
2. **Files changed** (list)
3. **Key logic decisions** (brief)
4. **Exactly what to review in `git diff`** (callouts)
5. **Copy/paste validation commands**
6. **Any pack-specific results** (metrics table / eval scores / autonomy notes)

## Stop Conditions — stop and ask if:
- Requirements conflict with existing patterns.
- An unlisted file must change.
- Criteria can't be met without scope expansion.
- Business logic or thresholds are unclear.
- A step would require an irreversible or external side-effect.



<!-- ============ CAPABILITY PACKS — fill the ticked ones; delete the rest ============ -->

<details>
<summary><b>🟦 DE PACK — what the agent must produce/verify</b></summary>

- Preserve **canonical schema**; report any new/modified columns explicitly.
- Enforce **business rule(s) + threshold(s)**: <!-- e.g. 59½ by 12/31; 55-rule; exclusions/locks -->
- **Data quality:** join keys `<...>`; null-handling `<...>`; dtype enforcement (dates/Int64/Float64).
- Assert **no duplicate keys** where uniqueness required; confirm **idempotent** rerun.
- Report **lineage**: input source + version/hash; backfill range + rollback step.
- Export: verify template headers align; output opens in Excel.
</details>

<details>
<summary><b>🟩 ML PACK</b></summary>

- Add/update the **model card** (intended use, limitations, metrics) alongside code.
- Produce a **baseline-vs-candidate metric table**; do **not** ship if it fails to beat baseline — stop and report.
- Log **experiment** (MLflow run id, params); set and report **seed** + run count.
- State **dataset version + train/val/test split**; assert **no leakage** across splits.
- Report inference **latency/size** change and any monitoring hook.
</details>

<details>
<summary><b>🟪 LLM / RAG PACK</b></summary>

- Run the **eval set** (DeepEval / RAGAS / GEval) and report **before→after** vs threshold.
  **Do not treat a single passing example as validation.** (AFC gate: faithfulness ≥ 0.90.)
- If prompts changed: report the **prompt diff**; keep prompts **versioned** in repo.
- Report **retrieval config** (chunking, top-k, embedding model) and whether the index was rebuilt (ChromaDB / Neo4j).
- Report **tokens/call, est. $/run, p95 latency** vs budget.
- Enforce **privacy-first routing** (finance/proprietary → local Ollama; never free/training-eligible cloud for sensitive data).
- Validate output with **Pydantic/schema**; note PII + prompt-injection handling.
</details>

<details>
<summary><b>🟧 AGENTIC PACK</b></summary>

- Declare **workflow vs agent** and the **autonomy tier** for this change.
- Declare the **action space**: exact tools + least-privilege scopes; nothing broader.
- Specify **loop**: trigger, plan→act→check→retry steps, state persistence.
- Specify **exits & budgets**: max iterations, cost/action caps, rate limits.
- 🛑 **Do NOT execute irreversible actions.** Ensure a **human sign-off gate + kill-switch** exists on
  any live/irreversible path (e.g. Crucible live trade); write a full **action audit log**.
- Run a **trajectory / tool-use eval**; report results.
- A2A: N/A for solo tools; flag if multi-agent (Stage 4–5).
</details>