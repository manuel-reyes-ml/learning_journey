# 🚀 WEEKS 7–8 MASTER ACTIVATION PLAN (v10.0)
## Flagship Era Opens — DataVault S1 v0 + AI-901 Exam | August 31 – September 13, 2026

**Document Version:** 3.0 — 🧭 **JOB-FIRST RE-CUT** (6 Oct 2026): fresh 12-week template from Mon 20 Jul 2026 · supersedes 1.1
**Covers:** Monday, August 31 – Sunday, September 13, 2026 (Stage 1 · Month 2 · Weeks 7–8)
**Aligned To:** Career Roadmap v10.0, **Corrections 1–54** (+ proposed C55/C56) · Target: **Analytics Engineer first door · Data Engineer parallel** (C22 §3, C54)
**Prerequisite:** Weeks 5–6 metrics ≥80% (non-negotiables: mini-project #3 + AI-901 exam booked + 🆕 dbt Fundamentals done)
**Weekly Hours:** 25 · 🇺🇸 Labor Day (Mon Sep 7) is a day off work — an optional bonus deep-work block if family plans allow; never mandatory.

> 🤖 **Agent Policy — Phase 3 continues.** Flagship rule stays: eval/test logic and ADRs human-authored through Q1. New rep this fortnight: before each DataVault build session, write the requirement as a comment block FIRST, then decide build-vs-delegate per function. Requirements-first is the decomposition habit FDE interviews test.

---

---

## 🧭 v3.0 JOB-FIRST RE-CUT — this fortnight (approved 6 Oct 2026)
Part of the fresh 12-week template from Mon 20 Jul 2026, 25 hrs/week, aligned to Corrections 1–54. Full rationale: the v3.0 block in Weeks 1–2. **This fortnight builds the first half of the Day-70 soft trigger.**

| Lane | This fortnight in v3.0 |
|---|---|
| L2 AE/DE flagship | DataVault scaffolds **with a dbt project from commit one**. **Python ingests** (generators → normalizers → pydantic row contract → quarantine → canonical Parquet); **dbt decides** (staging per source → union → recon buckets → Box-7 checks → findings), each rule with a dbt **unit test** |
| L1 Foundations | CS50P starts · P4E C3 (unchanged) |
| L3 Applied AI | Claude API course (tool use, caching) → ~65% · AI-901 exam Week 8 (unchanged) |
| L4 Trading | Rest (exam fortnight) |
| L5 Job search | Day 49: list → 30 + one request · Day 56: one conversation held · résumé v0 filled with DataVault's first lines |

---

## 🔄 REALIGNMENT PASS — ROADMAP CORRECTIONS 21–43 (applied 27 Aug 2026)

Standing rulings from Corrections 21–43 for this fortnight (Corrections 44–54 are applied in the v3.0 block above):

1. **🔴 Every reimbursement task is void.** Corrections 22/32/37: all certifications are **self-funded**, and the Month-6 scope-change conversation with Jen **cannot occur** — employment ends **9 Oct 2026**. AI-901 is a **$99 purchase you make**, a retake is another $99, and there is no claim to file on Day 54. The "elevation file" is renamed the **evidence file**: its audience is now the Q1 2027 external AE/DE interviewer, not an internal manager.
2. **⚠️ AI-901 content re-weighting** — the highest-value change in this pass, and it is *not* from a correction. Verified against Microsoft Learn (Aug 2026): AI-901 replaced AI-900 on 30 June 2026 and is **~55–60% Microsoft Foundry implementation**. Your Weeks 3–6 module plan used AI-900-era concept labels, which map to the smaller half. See the re-weighting note in the AI-901 section below before you drill.
3. **🪝 pre-commit lands on Day 47**, in the same session as CI — because they are the same gate at two boundaries, and Correction 21's governing rule is that the hook set is a **strict subset of CI**. Full pinned config is inline below.
4. **🐍🐻‍❄️ DataVault scaffolds on Python 3.14 with Polars as the default engine** (Corrections 28, 35). `uv add polars` is in the scaffold block. Keep pandas out of DataVault except at the two named boundaries — writing into an existing `.xlsx` template via openpyxl, and hand-off to matplotlib/plotly/scikit-learn/PandasAI. **Name the boundary in an ADR when you first cross it.**
5. **🗺️ Dual harness** (your ruling, 27 Aug): OpenCode in Cursor, Claude Code in VS Code, one shared `AGENTS.md`. The DataVault scaffold on Day 43 is the first repo built with both — **put `AGENTS.md` in the scaffold from commit one**, so the contract exists before either harness has a chance to diverge from it.
6. **🎯 The reframe worth more than the engine choice** (Correction 35 §2): for an Analytics-Engineer-first target, the first question is not pandas-vs-Polars, it is **how much logic leaves dataframes entirely for dbt**. DataVault's reconciliation engines belong in **tested dbt models** in S2, not in either dataframe library. ~~Build the S1 Python version knowing it is the "before"; do not over-invest in it.~~ → 🆕 **v3.0 makes this literal:** the S1 reconciliation and Box-7 logic are built *as dbt models* this fortnight; the Python layer stops at the row-level contract.

> 🧭 **What this fortnight is really producing now.** Under the old premise, DataVault + AI-901 were exhibits for an internal elevation case. Under Correction 22 they are the **first two artifacts of an external application package** with a hard date on it. Nothing about the build changes. What changes is that the README, the CI badge and the score report are now read by strangers — so write them for a stranger.

---

## 📊 WHERE YOU STAND
SDK fluency proven (mini-project #3: validated structured outputs, mocked tests, typed config), recon-toy fully production-checked (Docker + `uv sync --frozen`), SQL through window functions, AI-901 exam booked, 🆕 dbt Fundamentals certificate + a green market-data dbt rehearsal. **You are ready to open the DE flagship — dbt-first.**

## 🧠 STRATEGIC CONTEXT

### Why DataVault opens NOW (and what "S1 core" means)
Per the Build Progression (Correction 6), DataVault leads when hours are scarce because its evidence feeds the first external move. Its S1 core = the **1099 reconciliation core**: two source systems (Matrix-shaped + Relius-shaped) → canonical model → reconcile → Box-7 derivation/validation → corrections analytics. Explicitly NOT "chat with Excel" — the Applied-AI layer is S3.

**recon-toy was the rehearsal; DataVault is the performance.** Same shape, real architecture: a proper repo with the FULL production standard from commit #1 — uv + lockfile, src/ + py.typed, ruff + mypy, structlog, pydantic models, Docker, **CI as a blocking gate**, docs/adr/, README in Production/Cost/Architecture order.

> 🆕 **v3.0 architecture split — ADR 0002, written Day 43.** Python owns **generation → ingestion → the row-level contract**: generators, normalizers, the pydantic canonical model, quarantine of bad rows, Polars → Parquet. **dbt owns every set-level rule**: staging per source → a unioned canonical model → reconciliation buckets → Box-7 checks → findings marts, each tested. It's the split an AE interviewer probes ("where does business logic live, and how do you know it's right?"), and it turns this fortnight into the first half of the soft trigger.

**The data-boundary rule (Correction 18's ERISA framework, applied from day one):** the public repo contains ONLY synthetic data your generators invent. Real Matrix/Relius exports, real participant data, real volumes NEVER touch this repo. What crosses over is *shape knowledge* — you know what these files look like structurally, and encoding that shape in synthetic generators is itself the domain moat at work. Test everything you write here against the deposition test.

> 🔄 **Note (27 Aug 2026):** you have confirmed the 1099 codebase is **not company-private**, which resolves the *ownership* question for that project. **It does not touch this rule.** Ownership and data are separate axes: code you are free to publish still cannot carry participant records. This data-boundary rule applies unchanged to DataVault, to the 1099 repo, and to every public repo in the portfolio — synthetic only, always.

### The fortnight's second thread: AI-901
Exam target **Fri Sep 11 / Sat Sep 12**. Weeks of Learn modules + practice test #1 are done; this fortnight is drilling + practice tests #2–3 + the exam. ~~A pass = the reimbursement path proven + elevation-file evidence #1 + AB-620 unlocked.~~ → **A pass = evidence-file item #1, self-funded, and a Tier-3 line for the Q1 2027 applications.** AB-620 is **conditional** in the roadmap (Correction 37); you have elected to commit it as a **self-funded (~$165) extra-time thread** opening Week 9 — exam booked **after 9 Oct**, not before.

> ⚠️ **EXAM-CONTENT CORRECTION — verify before you drill (checked against Microsoft Learn, Aug 2026).** AI-901 replaced the retired AI-900 on 30 June 2026 and is **not** an AI-900 reskin. The current exam is split into two areas: identifying AI concepts and responsibilities (~40–45%) and **implementing AI solutions using Microsoft Foundry (~55–60%)**, passing score **700**. Weeks 3–6 scheduled your Learn modules with AI-900-era labels ("AI workloads overview," "ML fundamentals concepts") — those map to the *smaller* half of the exam. **Re-weight this fortnight's drilling toward Foundry**: deploying models, building with the Foundry SDK, creating agents, and information extraction with Azure Content Understanding. Practice tests #2–3 that are AI-900-derived will over-report your readiness — score them, but weight the Foundry gaps heavier than the raw number suggests. Price is **$99**, self-funded; the credential does not expire.

Also: Claude API course (tool use + prompt caching sections), **CS50P starts** (the testing/debugging rigor layer — and per Correction 20, your modern-Python idiom source), P4E Course 3 (web data: regex, JSON, APIs) begins.

### New concepts
```
Engineering: GitHub Actions CI (blocking gate) · mypy strict-ish · py.typed ·
             dataclass→pydantic canonical modeling · dict-driven rules engines
SDK:         tool use (Claude calls YOUR functions) · prompt caching
Python:      regex (P4E C3 — Day 15's pain, relieved) · CS50P test discipline
dbt:         sources on Parquet (dbt-duckdb) · staging per source · intermediate
             union · vars for tolerances · seeds as catalogues · unit tests
             (given/expect) · singular tests (🆕 v3.0)
```

---

## 🗓 WEEK 7 (Aug 31 – Sep 6)

### Week 7 goals
```
□ datavault repo live: full production scaffold + CI green
□ Synthetic Matrix-shaped + Relius-shaped generators (seeded, defect-planted)
□ Canonical model (pydantic) + normalizers for both sources, tested
□ 🆕 dbt project in the repo: sources on canonical Parquet · 2 staging models · generic tests
□ Scope doc v0.1 + ADRs 0001–0002 (DataVault's own docs/adr/)
□ Claude API course: tool use section · CS50P Week 0–1 · Post #7
```

### 📌 DAY 43 — Monday, August 31
**Morning:** **DataVault scoping session** (no code): write `docs/SCOPE_v0.1.md` — S1 boundary (recon core only), the S1→S3 arc one-liner, data-boundary rule, and the S1 exit checklist. 30 min cap on prose; then read your roadmap's DataVault portfolio entry once more.
**Evening:**
- [ ] 70 min — Scaffold the repo (you know this dance now — from memory, not notes):
```bash
cd ~/dev && uv init datavault --python 3.14 && cd datavault   # 3.14 floor — Correction 28
mkdir -p src/datavault/{ingest,models} tests docs/adr data/canonical output   # 🆕 v3.0: recon + rules live in dbt
uv add polars pydantic pydantic-settings structlog   # 🐻❄️ Polars = the default engine (Correction 35)
uv add --dev ruff pytest mypy pre-commit             # 🪝 pre-commit — Correction 21
uv add --group dbt "dbt-core>=1.12" dbt-duckdb      # 🆕 v3.0 — dbt from commit one (1.12 = first line on 3.14)
uv run dbt init datavault_dbt --skip-profile-setup && mv datavault_dbt dbt   # the dbt project lives in ./dbt
touch src/datavault/py.typed        # marker file: "this package ships type info"
```
Add `mypy` config to `pyproject.toml`:
```toml
[tool.mypy]
python_version = "3.14"
strict = false              # honest start; ratchet to true as the code matures
warn_unused_ignores = true
disallow_untyped_defs = true   # every function signature MUST be typed — the
                               # habit you've had since Week 2, now enforced
```
README skeleton in ①Production/②Cost/③Architecture order (all three sections stubbed with honest one-liners: "not yet deployed" is a valid Production statement for v0).
- [ ] 20 min — DataVault ADR 0001: `synthetic-only-public-boundary` (context: ERISA environment; decision: generators produce all public data; consequences: shape-fidelity burden on generators, Cost section will be thin — and that's correct per Correction 18)
- [ ] 15 min — 🆕 DataVault ADR 0002: `python-ingests-dbt-decides` — row-level contract in Python, set-level logic in dbt (C35 §2); **dbt Core 1.12 CLI over dbt v2/Fusion** while DuckDB-on-Fusion is beta — revisit at GA
- [ ] 15 min — Journal + commit + push (`chore: scaffold datavault with full production standard`)

### 📌 DAY 44 — Tuesday, September 1
**Morning:** CS50P — Week 0 (functions/variables — fast; the value layer is ahead).
**Evening:**
- [ ] 70 min — **Matrix-shaped generator.** `src/datavault/ingest/gen_matrix.py`: a seeded generator producing a CSV shaped like a recordkeeper distribution export — your domain knowledge decides the columns (participant key, plan id, gross/taxable amounts, fed/state withholding, Box-7 code, dates). Deliberately include the format quirks real exports have (dollar signs? date format? trailing spaces?) — *shape realism is the moat encoded*. Plant defects with logged counts (the golden-dataset pattern from Week 3, now standard practice).
- [ ] 30 min — Claude API course: tool use lesson 1
- [ ] 20 min — Journal + commit

### 📌 DAY 45 — Wednesday, September 2
**Morning:** P4E Course 3 — regex chapter (Day 15's manual parsing pain, finally relieved — note in your journal what regex replaces).
**Evening:**
- [ ] 70 min — **Relius-shaped generator** — same participants, DIFFERENT structure: different column names, different key format, different date convention, amounts that mostly-but-not-always agree. The disagreement between two systems describing one reality IS the product. Plant: missing records, amount drifts, code disagreements — all counted and logged.
- [ ] 30 min — CS50P Week 1 + problem set start
- [ ] 20 min — Journal + commit

### 📌 DAY 46 — Thursday, September 3
**Morning:** Claude API course — tool use lesson 2 (multi-tool, tool results).
**Evening:**
- [ ] 70 min — **The canonical model** ⭐ — the architectural heart of S1. `src/datavault/models/canonical.py`:

```python
"""The canonical distribution record — one truth both systems normalize INTO.

THE architectural idea of DataVault S1: instead of comparing Matrix-format
to Relius-format directly (N×M format-pair logic that grows forever), each
source gets ONE normalizer into a shared canonical form, and reconciliation
runs canonical-vs-canonical. Adding a third source someday = one new
normalizer, zero changes to recon. This is the pattern warehouses, dbt
staging layers, and every serious integration use — you're learning the
Stage 2 mental model by building it small.
"""

from datetime import date
from decimal import Decimal
from enum import Enum

from pydantic import BaseModel, Field, field_validator


class Box7Code(str, Enum):
    """Closed set of supported codes — an enum makes 'valid code' a TYPE.

    An unsupported code fails at parse time with a clear error instead of
    flowing downstream as a mystery string. Extend deliberately, per code,
    with a test each time.
    """

    EARLY_NO_EXCEPTION = "1"
    EARLY_EXCEPTION = "2"
    DEATH = "4"
    NORMAL = "7"
    DIRECT_ROLLOVER = "G"


class CanonicalDistribution(BaseModel):
    """One distribution, source-agnostic.

    Decimal, not float, for money: floats do binary arithmetic and
    0.1 + 0.2 != 0.3. In an ERISA context, cent-level drift is not a
    quirk — it's a finding. Decimal does exact decimal arithmetic.
    ADR topic if ever revisited.
    """

    source_system: str                       # "matrix" | "relius" — provenance
    participant_key: str = Field(min_length=1)
    plan_id: str
    gross_amount: Decimal = Field(gt=0)
    taxable_amount: Decimal = Field(ge=0)
    fed_withholding: Decimal = Field(ge=0)
    box7_code: Box7Code
    distribution_date: date

    @field_validator("taxable_amount")
    @classmethod
    def taxable_not_above_gross(cls, v: Decimal, info) -> Decimal:
        """Cross-field business rule enforced AT THE TYPE.

        A record violating domain law cannot even be constructed —
        the data contract idea (Week 3's PRIMARY KEY lesson) moved
        from the database into the model layer.
        """
        gross = info.data.get("gross_amount")
        if gross is not None and v > gross:
            raise ValueError(f"taxable {v} exceeds gross {gross}")
        return v
```
Write 5+ tests: valid record round-trips; taxable>gross rejected; unknown code rejected; Decimal precision preserved.
> 🆕 **v3.0 role of this model:** it is the **row-level contract at the ingestion boundary** — a row that violates domain law is quarantined in Python and never reaches the warehouse. Set-level questions (does Matrix agree with Relius? which codes break which rule?) belong to dbt from Saturday on. The `taxable_not_above_gross` rule also gets a dbt test, so the warehouse never trusts the loader blindly.
- [ ] 30 min — Journal + commit (`feat: canonical distribution model with domain validators`)

### 📌 DAY 47 — Friday, September 4
**Morning:** AI-901 practice test #2 → drill gaps.
**Evening:**
- [ ] 70 min — **CI: your first blocking gate** ⭐ `.github/workflows/ci.yml`:

```yaml
# CI = Continuous Integration: every push, GitHub runs this on a fresh
# machine. If any step fails, the commit is publicly marked failing.
# This is the "eval-first blocking gates" principle applied to code
# quality — and the first thing a hiring manager checks (green badge?).

name: ci
on: [push, pull_request]      # triggers

jobs:
  checks:
    runs-on: ubuntu-latest    # fresh Linux VM — which is exactly the point:
                              # "works on my machine" gets tested against
                              # NOT-your-machine on every single push
    steps:
      - uses: actions/checkout@v4              # step 1: get the code
      - uses: astral-sh/setup-uv@v5            # step 2: install uv (official action)
      - run: uv sync --frozen                  # step 3: EXACT lockfile deps —
                                               # same idiom as the Dockerfile
      - run: uv run ruff check .               # gate 1: lint
      - run: uv run ruff format --check .      # gate 2: formatting (—check = fail, don't fix)
      - run: uv run mypy src/                  # gate 3: types
      - run: uv run pytest                     # gate 4: tests
# Order cheapest→slowest: fail fast on the 2-second check before the
# 30-second one. Add the badge to README ①Production — your first
# externally verifiable production claim.
```
Push, watch the Actions tab run, fix anything red until green. Then break it on purpose (push a lint error), watch it fail, revert. **Know both colors — same lesson as Week 2's tests.**
- [ ] 25 min — 🪝 **pre-commit: the local half of the same gate** ⭐ · 🆕 **Correction 21**. CI is authoritative, but it catches defects at the *last* place anyone looks. Hooks catch them at the commit boundary. `.pre-commit-config.yaml`:

```yaml
# THE GOVERNING RULE (matters more than the tool): this hook set is a STRICT
# SUBSET of the CI gate above. Nothing runs locally that CI does not also run.
# Hooks and CI silently disagreeing is a portfolio defect an interviewer finds.
repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v5.0.0                      # PINNED — never floating
    hooks:
      - id: end-of-file-fixer
      - id: trailing-whitespace
      - id: check-yaml
      - id: check-added-large-files
      - id: detect-private-key       # commit-time enforcement of synthetic-data-only
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.8.4
    hooks:
      - id: ruff-check               # the hook id is ruff-check; the bare `ruff` id is retired
        args: [--fix]
      - id: ruff-format              # ORDER MATTERS: fixes can emit changes that need reformatting
  - repo: https://github.com/astral-sh/uv-pre-commit
    rev: 0.5.11
    hooks:
      - id: uv-lock                  # turns the Correction 13 reproducibility CLAIM into an
                                     # enforced invariant — lockfile can never drift from pyproject
  - repo: https://github.com/gitleaks/gitleaks
    rev: v8.21.2
    hooks:
      - id: gitleaks                 # secret scanning
```
```bash
uv run pre-commit install            # installs the git hook
uv run pre-commit run --all-files    # first run is slow (it builds envs) — expected
```
> **Verify the rev pins against the current releases before committing** — pinned means pinned to something real, and these were current at roadmap-writing time, not necessarily today. Then prove the invariant: edit `pyproject.toml` to add a dependency, `git add` + commit, and watch `uv-lock` regenerate `uv.lock` and *block the commit* until you stage it. That block is the whole point.
- [ ] 30 min — normalizer #1: `ingest/normalize_matrix.py` — Matrix CSV row → `CanonicalDistribution` (start it; finish Saturday)
- [ ] 20 min — Journal + commit (`ci: blocking quality gates via github actions`)

### 📌 DAY 48 — Saturday, September 5 (5.5h)
**Morning (5:00–8:30):**
- [ ] 120 min — Finish both normalizers (Matrix + Relius → canonical), each with parse-failure handling that **reports and quarantines** bad rows (never silently drops — the Week 3 rule, now with a `quarantine/` output and structlog events per rejection) — and write validated rows to `data/canonical/{matrix,relius}.parquet` (Polars)
- [ ] 60 min — 🆕 **Recon v0, in dbt** (v3.0 — replaces the Python recon engine): `sources.yml` points at the canonical Parquet (dbt-duckdb `meta: external_location`) → `stg_matrix__distributions` + `stg_relius__distributions` → `int_distributions__unioned` → `int_recon__compared` with the four buckets: matched / missing-per-side / amount-mismatch (tolerance as a dbt **`var`**, not a literal — the recon-toy ADR 0001 consequence, resolved properly this time) / code-disagreement. `unique` + `not_null` on every grain key.
- [ ] 30 min — Tests: load the generators' planted-defect manifest as a **seed**, then a **singular test** fails if any bucket's count differs from it — the golden-dataset assertion, now in dbt

**Evening:** 60 min Claude API course (prompt caching) · 45 min draft post #7 (artifact: CI badge + canonical model — "two systems, one truth: I opened my data-engineering flagship this week") · 15 min journal + commit

### 📌 DAY 49 — Sunday, September 6 (2h)
Week summary · publish post #7 · plan Week 8 (exam week — front-load DataVault, protect Thu–Sat for AI-901) · 🆕 20 min **Job lane:** targets → 30 across all three tiers; send one more informational-conversation request · journal 🎉

---

## 🗓 WEEK 8 (Sep 7–13) — EXAM WEEK

### Week 8 goals
```
□ ~~Box-7 rules engine v0 (Python)~~ → 🆕 **recon + Box-7 checks as dbt models**, a unit test per rule
□ Exceptions exported end-to-end with one command (`make run`: generate → normalize → dbt build → export)
□ AI-901: practice test #3 ≥85% → EXAM TAKEN (Fri/Sat)
□ ~~Reimbursement claim filed same day as pass~~ ❌ VOID (C22/32/37) · **evidence file** updated
□ CS50P Week 2 · P4E C3 continues · Post #8
□ 🆕 Job lane: targets at 30 · 1 informational conversation held
```

### 📌 DAY 50 — Monday, September 7 (Labor Day)
**Standard blocks; optional bonus block if the day allows.**
- [ ] Morning — 🆕 **Box-7 checks v0, in dbt** (v3.0 — replaces the Python rules engine, which stays below as collapsed reference):
  - `seeds/box7_rules.csv` — the rule **catalogue as data** (rule_name, box7_code, severity, description). Adding a rule = one catalogue row + one check column + one unit test; a reviewer (or an auditor) reads the table, not control flow. Same open/closed idea as the dict engine — in the layer AE teams actually run.
  - `models/intermediate/int_box7__checks.sql` — one boolean column per rule over the canonical rows, e.g. `box7_code = 'G' and taxable_amount > 0 as rollover_should_be_nontaxable`.
  - `models/marts/fct_box7_findings.sql` — unpivot the true flags into one row per finding (participant_key, box7_code, rule_name) and join the catalogue for severity.
  - **One dbt unit test per rule** — a triggering and a non-triggering row each, proven before any generated data touches the rule:
```yaml
unit_tests:
  - name: rollover_with_taxable_amount_is_flagged
    model: int_box7__checks
    given:
      - input: ref('int_distributions__unioned')
        rows:
          - {participant_key: "P1", box7_code: "G", gross_amount: 1000, taxable_amount: 50, fed_withholding: 0}
    expect:
      rows:
        - {participant_key: "P1", rollover_should_be_nontaxable: true}
```
  Your day job is still the source of which rules matter — that transfer is the moat, whatever the layer.

<details><summary>Reference only — the same rules as a Python dict engine (v2.x). Do not build it; v3.0 moves rule logic into dbt.</summary>

~~**Box-7 rules engine v0** `src/datavault/rules/box7.py`: dict-driven, not if/elif-driven:~~

```python
"""Box-7 validation rules — data-driven, so adding a rule is adding DATA.

Week 1's Box-7 checker was an elif chain: adding a code = editing logic.
Production version: rules live in a dict; the engine is a tiny loop that
never changes. New code, new rule, new test — engine untouched. This
open/closed shape is what makes rules AUDITABLE: a reviewer (or an
auditor) reads the table, not the control flow.
"""

from collections.abc import Callable
from decimal import Decimal

from datavault.models.canonical import Box7Code, CanonicalDistribution

# A rule = (name, predicate that flags a PROBLEM, severity)
Rule = tuple[str, Callable[[CanonicalDistribution], bool], str]

RULES: dict[Box7Code, list[Rule]] = {
    Box7Code.DIRECT_ROLLOVER: [
        (
            "rollover_should_be_nontaxable",
            lambda d: d.taxable_amount > Decimal("0"),
            "error",
        ),
        (
            "rollover_withholding_unusual",
            lambda d: d.fed_withholding > Decimal("0"),
            "warning",
        ),
    ],
    Box7Code.EARLY_NO_EXCEPTION: [
        (
            "early_dist_zero_withholding_flag",
            lambda d: d.fed_withholding == Decimal("0"),
            "warning",       # not illegal — worth an operator's eyes
        ),
    ],
    # Extend code-by-code, WITH a test per rule. Your day job is the
    # source of which rules matter — that transfer is the moat.
}


def validate(dist: CanonicalDistribution) -> list[dict]:
    """Run every rule for the record's code; return findings (empty = clean)."""
    findings = []
    for name, is_problem, severity in RULES.get(dist.box7_code, []):
        if is_problem(dist):
            findings.append({
                "rule": name,
                "severity": severity,
                "participant_key": dist.participant_key,
                "code": dist.box7_code.value,
            })
    return findings
```
Tests: one per rule (triggering + non-triggering record each).

</details>

- [ ] Evening — AI-901 drill block + CS50P Week 2

### 📌 DAY 51 — Tuesday, September 8
**Morning:** AI-901 practice test #3 — target ≥85%. Below it? Thursday evening becomes a drill block too.
**Evening:** 70 min — 🆕 wire DataVault end-to-end with **one command**: a `Makefile` (or `justfile`) target `run` = generate → normalize (Python, structlog events) → `uv run dbt build --project-dir dbt --profiles-dir dbt` → export `fct_box7_findings` and the recon mart to `output/` (DuckDB `COPY ... TO 'output/....csv'`) · 30 min AI-901 flashcard review · journal + commit

### 📌 DAY 52 — Wednesday, September 9
**Morning:** P4E C3 — JSON/APIs chapter.
**Evening:** 60 min DataVault polish: mypy clean, CI green, README ①Production updated honestly ("runs end-to-end locally via one command; CI-gated; not yet deployed") · 🆕 README states the split in one line — *"Python ingests, dbt decides"* — with the model count and test count · 40 min AI-901 weak-area drill · journal + commit

### 📌 DAY 53 — Thursday, September 10
**Morning:** Light AI-901 review only (no cramming — sleep is the better prep).
**Evening:** 45 min flashcards max · prep exam logistics (ID, quiet room if online-proctored, system check done TONIGHT not tomorrow) · early night.

### 📌 DAY 54 — Friday, September 11 · 🎯 **AI-901 EXAM** (or Sat slot)
- [ ] Take the exam. Pass → screenshot the score report, save the Credly badge link, and add both to the **evidence file**. ~~file the reimbursement claim the SAME DAY~~ · ~~tell Jen the good news in writing (one line — it plants the seed for the Month-6 conversation)~~ → ❌ **both void (C22/32/37): the cert is self-funded and the Month-6 conversation cannot occur.** Instead: **draft the résumé line and the LinkedIn post the same day**, while the detail is fresh — that is where this credential now does its work, pointed at the **Q1 2027** applications.
- [ ] Evening: celebrate properly. No study. 🎉 (If the attempt misses: ~~the program covers two attempts~~ — **there is no program; a retake is another $99 out of pocket.** Book it within 48h anyway, log the gap areas, no spiral. The evidence layer doesn't care about attempt counts — your wallet does, so use the free Microsoft practice assessment before rebooking.)

### 📌 DAY 55 — Saturday, September 12 (flex 5.5h)
If exam was today: same protocol as Day 54. Otherwise:
**Morning:** 120 min DataVault — corrections-analytics stub 🆕 **as a dbt mart** `fct_corrections_by_type_week` over `fct_box7_findings` (window functions in SQL — the Week 5 skill, deployed in the warehouse layer) · 60 min CS50P pset · 30 min buffer
**Evening:** 60 min Claude API course · 45 min draft post #8 (~~"I passed my first cloud cert — here's how the employer-reimbursement play works"~~ ❌ that post is now false — use **the rules-engine artifact**, or "what a self-funded cert ladder actually costs and why I still bought this one") · journal + commit

### 📌 DAY 56 — Sunday, September 13 (2h)
Week summary + **Month-2 retro** (hours honest, exam outcome, DataVault v0 state) · 🆕 Job lane check: targets at 30? one conversation held? résumé v0 carries DataVault's first lines? · publish post #8 · read Weeks 9–10 plan **and make the Sprint-1 decision** (next section explains) · journal 🎉

---

## 📊 2-WEEK SUCCESS METRICS
```
□ datavault repo: scaffold + CI green      □ AI-901 TAKEN (pass or retake booked)
□ Both generators, seeded + defect-logged  □ pre-commit installed + uv-lock invariant proven
□ Canonical model + validators tested      □ Evidence file: 3+ artifacts now
□ Both normalizers + quarantine path       □ CS50P Weeks 0–2 · P4E C3 ~60%
□ 🆕 dbt recon matches planted defects     □ Claude API course ~65%
  (singular test vs the defect manifest)
□ 🆕 Box-7 checks in dbt, unit test/rule   □ Posts #7–8 · ADRs 0001–0002 (DV)
□ End-to-end `make run` works (dbt inside)  □ 26+ commits
□ 🆕 Job lane: targets 30 · 1 conversation held
```
**Passing bar: 80%.** Non-negotiables: the exam attempt and the end-to-end DataVault run — 🆕 **through dbt**.

---

## 🔭 WHAT COMES NEXT
**Weeks 9–10: eval-first engineering** — the 2026 differentiator skill (39.6% of AI-first roles require it; ~5.5% of candidates list it). The **Sprint-1 DL.AI Pro month activates** (Correction 17: all nine S1+S2 lab rows batched, every notebook downloaded; optionally $0 via the AMD free month — decide Sunday). You build your first real eval harness — golden datasets, LLM-as-judge vs code-based checks, DeepEval — and point it at the Box-7 explainer. AB-620 study opens on the AI-901 pass. DataVault's corrections analytics matures.

> 🆕 **v3.0: Weeks 9–10 finish the soft trigger.** `dbt build` becomes a blocking CI step (Day 61), the corrections mart hardens, dbt docs publish to GitHub Pages, and DataVault **v0.1.0** is tagged public on Day 69 — C54's four artifacts. Day 70 checks the gate and, if green, opens the narrow search.

---
*Aligned to Career Roadmap v10.0 (Corrections 1–54) · v3.0 job-first re-cut, approved 6 Oct 2026. No roadmap edits made; propose→approve governance applies.*
