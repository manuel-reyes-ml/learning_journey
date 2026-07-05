---
description: Draft a production-grade README from the repo + template (does not write files)
agent: build
---

Draft a complete `README.md` for this repository, following the flagship standard.

README template: @.github/docs/templates/README_template.md
Flagship bar:    @.github/docs/FLAGSHIP_CHECKLIST.md

Project context (read to fill the template accurately):
!`cat pyproject.toml 2>/dev/null | head -60`
!`find src -name '*.py' | head -60`
!`git log --oneline -15`
!`ls -1`

> PRIVACY NOTE: this reads source code. For a finance/proprietary repo, run this from a
> mode using a LOCAL model (e.g. `ollama/qwen3.5-16k`) — do not send proprietary code to a
> cloud provider. Public portfolio repos are fine on the default build model.

Fill the template following its structure and the 40-second-scan ordering:
- One-line, **finance-framed** value prop (what it is + who for + why different)
- Functional badges only (CI, coverage, python, license, eval-gate) — no vanity badges
- Problem (domain-specific) + **quantified** result in the first ~200 words
- Mermaid architecture diagram, inferred from the code's actual flow
- 3-step copy-paste quick start (pyproject / uv; **no** `requirements.txt`)
- Evaluation table with thresholds/gates (DeepEval/RAGAS/GEval; faithfulness ≥ 0.90 for AFC)
- "Data quality & reliability" line ONLY if this is a pipeline/DE repo
- LLM/RAG and Agentic `<details>` sections ONLY if the code actually uses them
- "What I Learned" — 3–5 honest bullets (the finance-to-tech narrative hook)

Rules:
- Use ONLY facts you can confirm from the code — never invent metrics, benchmarks, or
  features. Leave a `<TODO: …>` placeholder wherever a real number or demo link is needed.
- Include the model-card link line ONLY if the repo trains/fine-tunes a model
  (then reference @.github/docs/templates/MODEL_CARD.md).
- Keep the top scannable; push depth into `<details>`. No table of contents.

Output the complete README as one Markdown block I can paste into `README.md`.
Do **NOT** write or commit any file — I create `README.md` manually after review.
