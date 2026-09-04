Draft a complete `README.md` for this repository, following the flagship standard.

All context you need has already been injected above this text by
`.github/scripts/readme_context.sh`.

**Do not attempt to load any of it yourself.** This body contains no `!` blocks and no
`@` references by design: command-template substitution is single-pass, so either would
arrive as literal text and silently never run (ADR-0001).

**Check the context first.** If a block above is missing, empty, or shows a line
beginning `CONTEXT_ERROR`, **STOP and report which one**. Do not infer, reconstruct, or
reason from the rules files in place of the missing output.

The `README TEMPLATE` block defines the structure and the `FLAGSHIP CHECKLIST` block
defines the bar. Both are blocking — if either reports `CONTEXT_ERROR`, STOP.

> ⚠️ **This command reads source code.** Run it only in a public, synthetic-only repo.
> For the proprietary 1099 / DataVault production repo, run it on a local-model agent
> (`plan` on OpenCode) so no source reaches a cloud provider.

Fill the template following its structure:
- One-line, **finance-framed** value prop (what it is + who for + why different)
- Functional badges only (CI, coverage, python, license, eval-gate) — no vanity badges.
  Claim a CI or eval badge only if the `CI WORKFLOWS` and `EVAL SUITE PRESENT?` blocks
  show one exists.
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
  hallucination < 0.15. **Raised bar (>= 0.90 / < 0.10) applies only to AFC and Crucible.**
  Note the judge model and the labeled-set size. Include this table only if the
  `EVAL SUITE PRESENT?` block found a suite.
- "Data quality & reliability" line ONLY if this is a pipeline/DE repo
- LLM/RAG and Agentic `<details>` sections ONLY if the code actually uses them
- "What I Learned" — 3–5 honest bullets (the finance-to-tech narrative hook)

Rules:
- Use ONLY facts confirmable from the context blocks — never invent metrics, benchmarks,
  or features. Leave a `<TODO: …>` placeholder wherever a real number or demo link is
  needed.
- **Honesty discipline (binding):** use a number only where it could be defended in an
  interview. Where a metric can't be shared, substitute **scale and reliability outcomes**
  (tables, jobs, refresh cadence, match rate, incidents). Never invent a figure to fill a token.
- **Disclosure:** no absolute dollar amounts, participant/plan data, client identifiers, or
  identifying record volumes. *(Crucible: no P&L, returns, or account figures.)* Every figure
  must clear the "would I say this in a deposition" test.
- **Diagram provenance:** if the `ARCHITECTURE DSL / DIAGRAMS` block shows
  `architecture.dsl`, the Mermaid block is an **export** of it — mark it `%% GENERATED`
  and tell me to run `make diagrams`. Do **not** hand-author a C4 diagram. If the DSL
  does not exist, infer a flow diagram from the source modules and flag that the DSL and
  C4 Context are missing against the standard.
- If the `DECISION RECORDS` block is empty, list the decisions visible in the code that
  have a real rejected alternative and flag them as ADRs to write.
- Include the model-card link line ONLY if the repo trains/fine-tunes a model, using the
  `MODEL CARD TEMPLATE` block.
- Keep the top scannable; push depth into `<details>`. No table of contents.

Output the complete README as one Markdown block I can paste into `README.md`.
Do **NOT** write or commit any file — I create `README.md` manually after review.