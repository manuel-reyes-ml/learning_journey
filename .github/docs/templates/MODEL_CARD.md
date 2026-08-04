<!--
=====================================================================
 MODEL CARD  (copy to <repo>/docs/MODEL_CARD.md; link it from the README eval section)
 Include ONLY for projects that train / fine-tune a model:
   • FormSense — Stage-3 fine-tuned extraction/classification model
   • Crucible  — prediction engine (calibrated base-rate / probability model)
 RAG-only, rules-only, or ETL projects don't need one (AFC, plain pipelines).
 Structure follows the Mitchell et al. (2019) / Google "Model Cards" standard.
 Re-review and update this file on EVERY model change — a stale model card erodes trust.
 Never include real client data, SSNs/DOBs/account numbers, or secrets here.
 Under roadmap v10.0, ML is a compressed literacy module inside Stage 3, not a career
 stage. Adaptation sequence: Prompt → RAG → Fine-tune → Distill. A model card means a
 fine-tune was EARNED against a baseline — not that a model was reached for.
=====================================================================
-->

# Model Card — <model name / version>

**One line:** <what this model does, in the project's finance context>
**Owner:** Manuel Reyes (`manuel-reyes-ml`) · **Status:** <research / candidate / production> · **Date:** <YYYY-MM-DD>

## 1. Model details
- **Type / architecture:** <e.g. fine-tuned vision-language extractor · gradient-boosted classifier · calibrated logistic base-rate model>
- **Base model / framework:** <e.g. local Ollama fine-tune · Anthropic SDK · scikit-learn · PyTorch>
- **Version + git SHA:** <semver> · <commit>
- **Training run:** <MLflow run id> · **seed(s):** <value> · **artifact size:** <MB>
- **Where it runs:** <local / container / hosted> · **privacy tier:** <proprietary → local only | public → cloud permitted>
- **License:** <model + any base-model license constraints>
- **Decision record:** [`docs/adr/000N-…`](docs/adr/) — why this model, and what was rejected

## 2. Intended use
- **Primary use:** <the specific task, e.g. extract structured fields from retirement-plan distribution forms>
- **Intended users:** <you as portfolio author / downstream module that consumes it>
- **Out-of-scope / must NOT be used for:** <e.g. NOT a compliance determination; NOT financial advice; NOT for real client PII in this repo>
- **Workflow vs agent:** <where this model sits in the taxonomy — is it a step in a fixed
  path, or does it direct tool use?>

## 3. Factors
<!-- The conditions under which performance can vary — the "when is it weaker?" section. -->
- **Input conditions:** <handwriting vs typed · scan quality · form type · small-cap vs large-cap regime>
- **Known sensitivity:** <e.g. degraded on low-DPI scans; weaker in high-volatility regimes>

## 4. Metrics
<!-- Mirror the README eval table; state the GATE, not just the number.
     Report only figures you could defend in an interview. -->
| Metric | Definition | Threshold (gate) | Value |
|--------|-----------|------------------|------:|
| <field-extraction accuracy (GEval)> | <per-field vs labeled set> | ≥ baseline | <0.xx> |
| <precision / recall / F1> | <on labeled complete/incomplete> | <gate> | <0.xx> |
| <calibration (Brier / reliability)> | <predicted vs realized> | <gate> | <0.xx> |

- **Baseline it must beat (earned-overlay):** <baseline + value>; ships only if it wins.
- **Gate is blocking in CI** — a regression fails the build and the PR does not merge.
- **Judge model** (if LLM-judged): <local Ollama — required for finance/proprietary eval data | cloud — public data only>

## 5. Evaluation data
- **Source:** <labeled hold-out set> · **size / split:** <train/val/test> · **snapshot version:** <hash/date>
- [ ] **Leakage check done** (no target/temporal leakage across splits)
- [ ] Set includes edge cases, out-of-scope inputs, and adversarial / PII-probing cases
- **Synthetic only** — no real client data.

## 6. Training data
- **Source + provenance:** <where it came from; how labeled> · **snapshot version:** <hash/date>
- **Known biases / gaps:** <e.g. under-represented form types; survivorship in market data>
- [ ] No real client data, PII, or secrets in the training corpus or its committed artifacts

## 7. Quantitative analyses
- **Overall vs by-factor:** <performance broken out by the factors in §3, e.g. by form type / by regime>
- **Failure modes observed:** <the concrete cases where it breaks>

## 8. Ethical considerations
- <e.g. extraction errors could misroute a distribution → mitigated by confidence gate + human review below threshold>
- <e.g. trading prediction is confirmation-only; deterministic engine owns the trade; not financial advice>
- **Irreversibility:** <does any output feed an irreversible action? If yes, name the human
  sign-off gate and the kill-switch. Model confidence never substitutes for either.>

## 9. Caveats & recommendations
- <what you'd improve next; when to retrain; monitoring/drift signal to watch>
- **Provenance:** every reported figure ties to a run manifest (`run_id` · git SHA ·
  config/params hash · data-snapshot version · seeds)
- **Disclosure:** no absolute dollar amounts, participant/plan data, or client identifiers.
  *(Crucible: no P&L, returns, or account figures.)* Every figure clears the deposition test.
- **Change log:** <date — what changed — new metric values>