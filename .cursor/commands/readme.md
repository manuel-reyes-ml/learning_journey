Generate a production-grade README for this repository, following the flagship standard.

Usage: `/readme` (run from the repository you want a README for)

1. Read `.github/docs/templates/README_template.md` for the required structure
2. Read `.github/docs/FLAGSHIP_CHECKLIST.md` for the production-grade bar
3. Gather project context so the README reflects the actual code:
   - Run `cat pyproject.toml` (dependencies, tooling, Python version)
   - Run `find src -name '*.py'` to map the modules
   - Run `git log --oneline -15` for recent work
4. PRIVACY: this reads source code. For a finance/proprietary repo, use a local model
   (Ollama) — do not send proprietary code to a cloud provider. Public portfolio repos are fine.
5. Fill the template using the 40-second-scan ordering:
   - One-line, finance-framed value prop (what it is + who for + why different)
   - Functional badges only (CI, coverage, python, license, eval-gate) — no vanity badges
   - Problem (domain-specific) + quantified result in the first ~200 words
   - Mermaid architecture diagram inferred from the actual code flow
   - 3-step quick start (uv / pyproject; no requirements.txt)
   - Evaluation table with thresholds/gates (faithfulness >= 0.90 for AFC)
   - "Data quality & reliability" line only if this is a pipeline/DE repo
   - LLM/RAG and Agentic sections only if the code actually uses them
   - "What I Learned" — 3-5 honest bullets (the finance-to-tech narrative hook)
6. Use ONLY facts you can confirm from the code — never invent metrics, benchmarks, or
   features. Leave a `<TODO: ...>` placeholder wherever a real number or demo link is needed.
7. Include the model-card link only if the repo trains/fine-tunes a model
   (then reference `.github/docs/templates/MODEL_CARD.md`).
8. Output the complete README as one Markdown block I can paste into `README.md`
9. Do NOT write or commit any file — I create `README.md` manually after review
