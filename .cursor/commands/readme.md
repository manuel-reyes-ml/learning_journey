Generate a production-grade README for this repository, following the flagship standard.

Usage: `/readme` (run from the repository you want a README for)

1. Read `.github/docs/templates/README_template.md` for the required structure
2. Read `.github/docs/FLAGSHIP_CHECKLIST.md` for the production-grade bar
3. Read `.cursor/rules/architecture-docs.mdc` for the ADR / C4 / README standard
4. Gather project context so the README reflects the actual code:
   - Run `cat pyproject.toml` (dependencies, tooling, Python version)
   - Run `find src -name '*.py'` to map the modules
   - Run `ls docs/adr` and `ls architecture.dsl docs/diagrams` to see what architecture
     artifacts already exist
   - Run `git log --oneline -15` for recent work
5. PRIVACY: this reads source code. For a finance/proprietary repo, use a local model
   (Ollama) — do not send proprietary code to a cloud provider. Public portfolio repos are fine.
6. Fill the template in its required order. The header and demo carry the 40-second scan;
   the first three **sections** are Production, Cost, Architecture:
   - One-line, finance-framed value prop (what it is + who for + why different)
   - Functional badges only (CI, coverage, python, license, eval-gate) — no vanity badges
   - Problem (domain-specific) + a **defensible outcome** in the first ~200 words
   - **① Production** — where it runs, what depends on it, deploy path, structlog
     observability, reliability posture, the blocking merge gates. A stack list is not a
     production claim: if nothing depends on it and nothing watches it, say so plainly and
     describe it under Architecture instead
   - **② Cost** — the number AND the mechanism, plus the SLA that did not regress.
     **Omit this section entirely rather than manufacture one** (optional for FormSense and
     AFC; thin by design for DataVault)
   - **③ Architecture** — Mermaid diagram, C4 Context (plus Container on lead flagships),
     link to `architecture.dsl`, links to `docs/adr/` with the rejected alternative named
   - 3-step quick start using `uv sync --frozen` (no `requirements.txt`, no `pip install`)
   - Evaluation table with thresholds/gates: answer relevancy > 0.80, faithfulness > 0.85,
     hallucination < 0.15. The raised bar (≥ 0.90 / < 0.10) applies **only to AFC and
     Crucible**. Note the judge model and the labeled-set size
   - "Data quality & reliability" line only if this is a pipeline/DE repo
   - LLM/RAG and Agentic sections only if the code actually uses them
   - "What I Learned" — 3-5 honest bullets (the finance-to-tech narrative hook)
7. Use ONLY facts you can confirm from the code — never invent metrics, benchmarks, or
   features. Leave a `<TODO: ...>` placeholder wherever a real number or demo link is needed.
8. HONESTY DISCIPLINE (binding): use a number only where it could be defended in an
   interview. Where a metric cannot be shared, substitute scale and reliability outcomes
   (tables, jobs, refresh cadence, match rate, incidents). Never invent a figure to fill a token.
9. DISCLOSURE: no absolute dollar amounts, participant/plan data, client identifiers, or
   identifying record volumes. Crucible carries a parallel rule — no P&L, returns, or account
   figures, ever. Every figure must clear the "would I say this in a deposition" test.
10. DIAGRAM PROVENANCE: if `architecture.dsl` exists, the Mermaid block is an **export** of it —
    mark it `%% GENERATED` and tell me to run `make diagrams`. Do NOT hand-author a C4 diagram.
    If `architecture.dsl` does not exist yet, infer a flow diagram from the code and flag that
    the DSL and C4 Context are missing against the standard.
11. If `docs/adr/` is empty or missing, list the decisions visible in the code that have a real
    rejected alternative and flag them as ADRs I still need to write.
12. Include the model-card link only if the repo trains/fine-tunes a model
    (then reference `.github/docs/templates/MODEL_CARD.md`).
13. Output the complete README as one Markdown block I can paste into `README.md`
14. Do NOT write or commit any file — I create `README.md` manually after review