Draft a complete `README.md` for this repository, following the flagship standard.

README template: @.github/docs/templates/README_template.md
Flagship bar:    @.github/docs/FLAGSHIP_CHECKLIST.md
Doc standard:    @.cursor/rules/architecture-docs.mdc

Project context (read to fill the template accurately):
!`cat pyproject.toml 2>/dev/null | head -60`
!`find src -name '*.py' | head -60`
!`ls docs/adr 2>/dev/null`
!`ls architecture.dsl docs/diagrams 2>/dev/null`
!`git log --oneline -15`
!`ls -1`

> ⚠️ **This skill reads source code.** In this harness there is no local-model option,
> so run it only in a public, synthetic-only repo. For the proprietary 1099 / DataVault
> production repo, use OpenCode with a local model instead.

Fill the template following its structure:
- One-line, **finance-framed** value prop (what it is + who for + why different)
- Functional badges only (CI, coverage, python, license, eval-gate) — no vanity badges
- Problem (domain-specific) + a **defensible outcome** in the first ~200 words
- Then the three leading sections, **in this order**:
  - **① Production** — where it runs, what depends on it, deploy path, structlog
    observability, reliability posture, the blocking gates. *A stack list is not a
    production claim* — if nothing depends on it and nothing watches it, say so and
    describe it under Architecture instead.
  - **② Cost** — the number **and the mechanism**, plus the SLA that did not regress.
    **Omit this section entirely rather than manufacture one** (optional for FormSense
    and AFC; thin by design for DataVault).
  - **③ Architecture** — Mermaid diagram, C4 Context (+ Container on lead flagships),
    `architecture.dsl` link, `docs/adr/` links with the rejected alternative named.
- 3-step copy-paste quick start (`uv sync --frozen`; **no** `requirements.txt`, **no** `pip install`)
- Evaluation table with thresholds/gates: answer relevancy > 0.80, faithfulness > 0.85,
  hallucination < 0.15. **Raised bar (≥ 0.90 / < 0.10) applies only to AFC and Crucible.**
  Note the judge model and the labeled-set size.
- "Data quality & reliability" line ONLY if this is a pipeline/DE repo
- LLM/RAG and Agentic `<details>` sections ONLY if the code actually uses them
- "What I Learned" — 3–5 honest bullets (the finance-to-tech narrative hook)

Rules:
- Use ONLY facts you can confirm from the code — never invent metrics, benchmarks, or
  features. Leave a `<TODO: …>` placeholder wherever a real number or demo link is needed.
- **Honesty discipline (binding):** use a number only where it could be defended in an
  interview. Where a metric can't be shared, substitute **scale and reliability outcomes**
  (tables, jobs, refresh cadence, match rate, incidents). Never invent a figure to fill a token.
- **Disclosure:** no absolute dollar amounts, participant/plan data, client identifiers, or
  identifying record volumes. *(Crucible: no P&L, returns, or account figures.)* Every figure
  must clear the "would I say this in a deposition" test.
- **Diagram provenance:** if `architecture.dsl` exists, the Mermaid block is an **export** of
  it — mark it `%% GENERATED` and tell me to run `make diagrams`. Do **not** hand-author a C4
  diagram. If `architecture.dsl` does not exist yet, infer a flow diagram from the code and
  flag that the DSL and C4 Context are missing against the standard.
- If `docs/adr/` is empty or missing, list the decisions visible in the code that have a real
  rejected alternative and flag them as ADRs to write.
- Include the model-card link line ONLY if the repo trains/fine-tunes a model
  (then reference @.github/docs/templates/MODEL_CARD.md).
- Keep the top scannable; push depth into `<details>`. No table of contents.

Output the complete README as one Markdown block I can paste into `README.md`.
Do **NOT** write or commit any file — I create `README.md` manually after review.
