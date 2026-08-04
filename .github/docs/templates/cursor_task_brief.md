# Cursor / OpenCode Agent Task Brief

<!--
 Feed this to the coding agent. The agent EXECUTES but never commits.
 Fill CORE, tick the packs, and fill ONLY the ticked packs at the bottom.
 Packs here must match the linked Issue and the eventual PR.
 Standards source: AGENTS.md (contract) + .cursor/rules/ (detail). Roadmap v10.0.
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
3. **Gap analysis before any edit.** State what exists, what's missing, and the exact proposed
   change. Any **destructive** edit needs a **capability audit** first — enumerate every heading
   and item between the target boundaries and say where each one lands.
4. Do not change behavior outside scope.
5. Follow the production standard (`src/` layout · full type hints ·
   `from __future__ import annotations` · **structlog kwargs, never `print()`, never f-strings or
   `%s` interpolation of payload data** · config through `settings` (pydantic-settings), never raw
   `os.environ` · retries via `stamina` · `pyproject.toml` + `uv.lock`, never `requirements.txt`).
6. Keep changes testable: add/adjust tests or validations where appropriate.
7. **No secrets, no real client data** in code, tests, fixtures, or notebook output.
   Credentials are `SecretStr`. Synthetic data only.
8. **Autonomy limit:** propose-and-pause. The agent must **not** trigger any irreversible or
   external side-effect (network writes, deletes, live orders, posting). Surface them for human action.
9. **If a decision in this task has a real rejected alternative, an ADR is required** —
   draft it in `docs/adr/` as part of the change. ADRs are immutable once accepted; supersede,
   never rewrite.

## Files to Change
| File | Change | Why |
|------|--------|-----|
| `path/to/file.py` | modify | [reason] |
| `docs/adr/000N-….md` | add | [decision + rejected alternative] |

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
- [ ] `uv.lock` still in sync with `pyproject.toml` if deps changed.

## Edge Cases to Handle Explicitly
- <edge case 1: nulls / dupes / missing keys>
- <edge case 2: empty input / malformed row>
- <edge case 3: retry on a non-idempotent write — needs an idempotency key>

If an edge case needs scope expansion, **stop and explain tradeoffs.**

## Validation Commands
```bash
uv sync --frozen
uv run python -c "import <package>"
uv run ruff check src/ tests/
uv run ruff format --check src/ tests/
uv run mypy src/
uv run pytest -q
```

## Deliverable Summary (report back, no commit)
1. **What changed** (bullets)
2. **Files changed** (list)
3. **Key logic decisions** (brief) — flag any that warrant an ADR
4. **Exactly what to review in `git diff`** (callouts)
5. **Copy/paste validation commands**
6. **Any pack-specific results** (metrics table / eval scores / autonomy notes)
7. **Commit-gate status** — which items in the `AGENTS.md` gate are not yet clean

## Stop Conditions — stop and ask if:
- Requirements conflict with existing patterns or with a `.cursor/rules/` standard.
- An unlisted file must change.
- Criteria can't be met without scope expansion.
- Business logic or thresholds are unclear.
- A step would require an irreversible or external side-effect.
- Proprietary data would need to reach a cloud model.
- A destructive edit is required and no capability audit has been run.



<!-- ============ CAPABILITY PACKS — fill the ticked ones; delete the rest ============ -->

<details>
<summary><b>🟦 DE PACK — what the agent must produce/verify</b></summary>

- Preserve **canonical schema**; report any new/modified columns explicitly.
- Enforce **business rule(s) + threshold(s)**: <!-- e.g. 59½ by 12/31; 55-rule; exclusions/locks -->
- **Data quality:** join keys `<...>`; null-handling `<...>`; dtype enforcement (dates/Int64/Float64).
- Assert **no duplicate keys** where uniqueness required; confirm **idempotent** rerun.
- Any retried write carries an **idempotency key** — a retry without one double-books.
- Report **lineage**: input source + version/hash; backfill range + rollback step.
- Note **data contracts / freshness SLA** if downstream consumers exist.
- Export: verify template headers align; output opens in Excel.
</details>

<details>
<summary><b>🟩 ML PACK</b></summary>

<!-- Under v10.0 ML is a compressed literacy module inside Stage 3, not a career stage.
     Adaptation sequence: Prompt → RAG → Fine-tune → Distill. This pack applies when a
     project actually carries a model. -->

- Add/update the **model card** (intended use, limitations, metrics) alongside code.
- Produce a **baseline-vs-candidate metric table**; do **not** ship if it fails to beat baseline — stop and report.
- Log **experiment** (MLflow run id, params); set and report **seed** + run count.
- State **dataset version + train/val/test split**; assert **no leakage** across splits.
- Report inference **latency/size** change and any monitoring hook.
</details>

<details>
<summary><b>🟪 LLM / RAG PACK</b></summary>

- Run the **eval set** (DeepEval / RAGAS / GEval) and report **before→after** vs threshold.
  **Do not treat a single passing example as validation.** Baseline gates: answer relevancy > 0.80,
  faithfulness > 0.85, hallucination < 0.15. **Raised bar for AFC and Crucible:
  faithfulness ≥ 0.90, hallucination < 0.10.**
- Confirm the **judge model**: local Ollama for finance/proprietary eval data; cloud only on public data.
- If prompts changed: report the **prompt diff**; keep prompts **versioned** in repo.
- Report **retrieval config** (chunking, top-k, embedding model) and whether the index was rebuilt (ChromaDB / Neo4j).
- Report **tokens/call, est. $/run, p95 latency** vs budget — this feeds the README **② Cost** section.
- Enforce **privacy-first routing**: provider from `settings.ai_provider`; fallback is **local, never
  cloud**; never free/training-eligible tiers on project data.
- Validate output with **Pydantic/schema**; confirm the response-side PII scan runs before display.
- Log per query: provider · model · tokens · latency · cost · guardrail status (structlog kwargs).
</details>

<details>
<summary><b>🟧 AGENTIC PACK</b></summary>

- Declare **workflow vs agent** (Anthropic taxonomy) and the **autonomy tier** for this change.
- Declare the **action space**: exact tools + least-privilege scopes; nothing broader.
- Specify **loop**: trigger, plan→act→check→retry steps, state persistence.
- Specify **exits & budgets**: max iterations, cost/action caps, rate limits.
- 🛑 **Do NOT execute irreversible actions.** Ensure a **human sign-off gate + kill-switch** exists on
  any live/irreversible path (e.g. Crucible live trade) — no auto-approve, no timeout-approve, no
  confidence-threshold bypass. Write a full **action audit log**.
- Emit `human_signoff_required` and `killswitch_engaged` as canonical events.
- Keep backtest/paper and live paths separated **in the type system**, not by a runtime flag.
- **Eval scores never authorize execution** — report that explicitly on any Crucible change.
- Run a **trajectory / tool-use eval**; report Tool Correctness and Task Completion.
- A2A: N/A for solo tools; flag if multi-agent (defer to Stage 3).
</details>