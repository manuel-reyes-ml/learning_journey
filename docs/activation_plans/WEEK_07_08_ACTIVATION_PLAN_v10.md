# 🚀 WEEKS 7–8 MASTER ACTIVATION PLAN (v10.0)
## Flagship Era Opens — DataVault S1 v0 + AI-901 Exam | August 31 – September 13, 2026

**Document Version:** 1.0
**Covers:** Monday, August 31 – Sunday, September 13, 2026 (Stage 1 · Month 2 · Weeks 7–8)
**Aligned To:** Career Roadmap v10.0, Corrections 1–20
**Prerequisite:** Weeks 5–6 metrics ≥80% (non-negotiables: mini-project #3 + AI-901 exam booked)
**Weekly Hours:** 25 · 🇺🇸 Labor Day (Mon Sep 7) is a day off work — an optional bonus deep-work block if family plans allow; never mandatory.

> 🤖 **Agent Policy — Phase 3 continues.** Flagship rule stays: eval/test logic and ADRs human-authored through Q1. New rep this fortnight: before each DataVault build session, write the requirement as a comment block FIRST, then decide build-vs-delegate per function. Requirements-first is the decomposition habit FDE interviews test.

---

## 📊 WHERE YOU STAND
SDK fluency proven (mini-project #3: validated structured outputs, mocked tests, typed config), recon-toy fully production-checked (Docker + `uv sync --frozen`), SQL through window functions, AI-901 exam booked. **You are ready to open the DE flagship.**

## 🧠 STRATEGIC CONTEXT

### Why DataVault opens NOW (and what "S1 core" means)
Per the Build Progression (Correction 6), DataVault leads when hours are scarce because its evidence feeds the first external move. Its S1 core = the **1099 reconciliation core**: two source systems (Matrix-shaped + Relius-shaped) → canonical model → reconcile → Box-7 derivation/validation → corrections analytics. Explicitly NOT "chat with Excel" — the Applied-AI layer is S3.

**recon-toy was the rehearsal; DataVault is the performance.** Same shape, real architecture: a proper repo with the FULL production standard from commit #1 — uv + lockfile, src/ + py.typed, ruff + mypy, structlog, pydantic models, Docker, **CI as a blocking gate**, docs/adr/, README in Production/Cost/Architecture order.

**The data-boundary rule (Correction 18's ERISA framework, applied from day one):** the public repo contains ONLY synthetic data your generators invent. Real Matrix/Relius exports, real participant data, real volumes NEVER touch this repo. What crosses over is *shape knowledge* — you know what these files look like structurally, and encoding that shape in synthetic generators is itself the domain moat at work. Test everything you write here against the deposition test.

### The fortnight's second thread: AI-901
Exam target **Fri Sep 11 / Sat Sep 12**. Weeks of Learn modules + practice test #1 are done; this fortnight is drilling + practice tests #2–3 + the exam. A pass = the reimbursement path proven + elevation-file evidence #1 + AB-620 unlocked.

Also: Claude API course (tool use + prompt caching sections), **CS50P starts** (the testing/debugging rigor layer — and per Correction 20, your modern-Python idiom source), P4E Course 3 (web data: regex, JSON, APIs) begins.

### New concepts
```
Engineering: GitHub Actions CI (blocking gate) · mypy strict-ish · py.typed ·
             dataclass→pydantic canonical modeling · dict-driven rules engines
SDK:         tool use (Claude calls YOUR functions) · prompt caching
Python:      regex (P4E C3 — Day 15's pain, relieved) · CS50P test discipline
```

---

## 🗓 WEEK 7 (Aug 31 – Sep 6)

### Week 7 goals
```
□ datavault repo live: full production scaffold + CI green
□ Synthetic Matrix-shaped + Relius-shaped generators (seeded, defect-planted)
□ Canonical model (pydantic) + normalizers for both sources, tested
□ Scope doc v0.1 + ADRs 0001–0002 (DataVault's own docs/adr/)
□ Claude API course: tool use section · CS50P Week 0–1 · Post #7
```

### 📌 DAY 43 — Monday, August 31
**Morning:** **DataVault scoping session** (no code): write `docs/SCOPE_v0.1.md` — S1 boundary (recon core only), the S1→S3 arc one-liner, data-boundary rule, and the S1 exit checklist. 30 min cap on prose; then read your roadmap's DataVault portfolio entry once more.
**Evening:**
- [ ] 70 min — Scaffold the repo (you know this dance now — from memory, not notes):
```bash
cd ~/dev && uv init datavault --python 3.12 && cd datavault
mkdir -p src/datavault/{ingest,models,recon,rules} tests docs/adr data output
uv add pydantic pydantic-settings structlog
uv add --dev ruff pytest mypy
touch src/datavault/py.typed        # marker file: "this package ships type info"
```
Add `mypy` config to `pyproject.toml`:
```toml
[tool.mypy]
python_version = "3.12"
strict = false              # honest start; ratchet to true as the code matures
warn_unused_ignores = true
disallow_untyped_defs = true   # every function signature MUST be typed — the
                               # habit you've had since Week 2, now enforced
```
README skeleton in ①Production/②Cost/③Architecture order (all three sections stubbed with honest one-liners: "not yet deployed" is a valid Production statement for v0).
- [ ] 30 min — DataVault ADR 0001: `synthetic-only-public-boundary` (context: ERISA environment; decision: generators produce all public data; consequences: shape-fidelity burden on generators, Cost section will be thin — and that's correct per Correction 18)
- [ ] 20 min — Journal + commit + push (`chore: scaffold datavault with full production standard`)

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
- [ ] 30 min — normalizer #1: `ingest/normalize_matrix.py` — Matrix CSV row → `CanonicalDistribution` (start it; finish Saturday)
- [ ] 20 min — Journal + commit (`ci: blocking quality gates via github actions`)

### 📌 DAY 48 — Saturday, September 5 (5.5h)
**Morning (5:00–8:30):**
- [ ] 120 min — Finish both normalizers (Matrix + Relius → canonical), each with parse-failure handling that **reports and quarantines** bad rows (never silently drops — the Week 3 rule, now with a `quarantine/` output and structlog events per rejection)
- [ ] 60 min — **Recon engine v0**: port the Week 4 matcher pattern to canonical records — matched / missing-per-side / amount-mismatch (Decimal tolerance from settings, not hardcoded — that ADR 0001 consequence from recon-toy, resolved properly this time) / code-disagreement buckets
- [ ] 30 min — Tests: recon finds EXACTLY the generators' planted defect counts (the golden-dataset assertion, now on the flagship)

**Evening:** 60 min Claude API course (prompt caching) · 45 min draft post #7 (artifact: CI badge + canonical model — "two systems, one truth: I opened my data-engineering flagship this week") · 15 min journal + commit

### 📌 DAY 49 — Sunday, September 6 (2h)
Week summary · publish post #7 · plan Week 8 (exam week — front-load DataVault, protect Thu–Sat for AI-901) · journal 🎉

---

## 🗓 WEEK 8 (Sep 7–13) — EXAM WEEK

### Week 8 goals
```
□ Box-7 rules engine v0 + exceptions report end-to-end (pipeline runs via CLI)
□ AI-901: practice test #3 ≥85% → EXAM TAKEN (Fri/Sat)
□ Reimbursement claim filed same day as pass · elevation file updated
□ CS50P Week 2 · P4E C3 continues · Post #8
```

### 📌 DAY 50 — Monday, September 7 (Labor Day)
**Standard blocks; optional bonus block if the day allows.**
- [ ] Morning — **Box-7 rules engine v0** `src/datavault/rules/box7.py`: dict-driven, not if/elif-driven:

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
- [ ] Evening — AI-901 drill block + CS50P Week 2

### 📌 DAY 51 — Tuesday, September 8
**Morning:** AI-901 practice test #3 — target ≥85%. Below it? Thursday evening becomes a drill block too.
**Evening:** 70 min — wire DataVault end-to-end: `uv run python -m datavault ...` runs generate→normalize→recon→rules→exceptions report (structlog events throughout; report to `output/`) · 30 min AI-901 flashcard review · journal + commit

### 📌 DAY 52 — Wednesday, September 9
**Morning:** P4E C3 — JSON/APIs chapter.
**Evening:** 60 min DataVault polish: mypy clean, CI green, README ①Production updated honestly ("runs end-to-end locally via one command; CI-gated; not yet deployed") · 40 min AI-901 weak-area drill · journal + commit

### 📌 DAY 53 — Thursday, September 10
**Morning:** Light AI-901 review only (no cramming — sleep is the better prep).
**Evening:** 45 min flashcards max · prep exam logistics (ID, quiet room if online-proctored, system check done TONIGHT not tomorrow) · early night.

### 📌 DAY 54 — Friday, September 11 · 🎯 **AI-901 EXAM** (or Sat slot)
- [ ] Take the exam. Pass → **file the reimbursement claim the SAME DAY** (the program's proof-of-completion step), screenshot the score report, add both to the elevation file, and tell Jen the good news in writing (one line — it plants the seed for the Month-6 conversation).
- [ ] Evening: celebrate properly. No study. 🎉 (If the attempt misses: the program covers two attempts — book the retake within 48h, log the gap areas, no spiral. The evidence layer doesn't care about attempt counts.)

### 📌 DAY 55 — Saturday, September 12 (flex 5.5h)
If exam was today: same protocol as Day 54. Otherwise:
**Morning:** 120 min DataVault — corrections-analytics stub: aggregate rule findings by type × week (SQL window functions ON your own pipeline output — the Week 5 skill, deployed) · 60 min CS50P pset · 30 min buffer
**Evening:** 60 min Claude API course · 45 min draft post #8 ("I passed my first cloud cert — here's how the employer-reimbursement play works" OR the rules-engine artifact) · journal + commit

### 📌 DAY 56 — Sunday, September 13 (2h)
Week summary + **Month-2 retro** (hours honest, exam outcome, DataVault v0 state) · publish post #8 · read Weeks 9–10 plan **and make the Sprint-1 decision** (next section explains) · journal 🎉

---

## 📊 2-WEEK SUCCESS METRICS
```
□ datavault repo: scaffold + CI green      □ AI-901 TAKEN (pass or retake booked)
□ Both generators, seeded + defect-logged  □ Reimbursement claim filed on pass
□ Canonical model + validators tested      □ Elevation file: 3+ artifacts now
□ Both normalizers + quarantine path       □ CS50P Weeks 0–2 · P4E C3 ~60%
□ Recon engine matches planted defects     □ Claude API course ~75%
□ Box-7 rules engine, test per rule        □ Posts #7–8 · ADRs 0001–0002 (DV)
□ End-to-end CLI run works                 □ 26+ commits
```
**Passing bar: 80%.** Non-negotiables: the exam attempt and the end-to-end DataVault run.

---

## 🔭 WHAT COMES NEXT
**Weeks 9–10: eval-first engineering** — the 2026 differentiator skill (39.6% of AI-first roles require it; ~5.5% of candidates list it). The **Sprint-1 DL.AI Pro month activates** (Correction 17: all nine S1+S2 lab rows batched, every notebook downloaded; optionally $0 via the AMD free month — decide Sunday). You build your first real eval harness — golden datasets, LLM-as-judge vs code-based checks, DeepEval — and point it at the Box-7 explainer. AB-620 study opens on the AI-901 pass. DataVault's corrections analytics matures.

---
*Aligned to Career Roadmap v10.0 (Corrections 1–20). No roadmap edits made; propose→approve governance applies.*
