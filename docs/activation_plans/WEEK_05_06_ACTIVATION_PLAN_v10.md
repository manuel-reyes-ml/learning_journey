# 🚀 WEEKS 5–6 MASTER ACTIVATION PLAN (v10.0)
## The SDK Era Opens | August 17–30, 2026

**Document Version:** 1.1 (realigned to roadmap Corrections 21–43)
**Covers:** Monday, August 17 – Sunday, August 30, 2026 (Stage 1 · Month 2 · Weeks 5–6)
**Aligned To:** Career Roadmap v10.0, **Corrections 1–43** · ⚠️ delta recorded below — **you are inside this fortnight now (Day 39 = Thu 27 Aug)**, so read the block before Friday.
**Prerequisite:** Weeks 3–4 metrics ≥80% (non-negotiables: recon-toy shipped + AI-901 kickoff)
**Weekly Hours:** 25 (same block schedule)

> **Plans get terser from here — deliberately.** Weeks 1–4 spelled out every line because you couldn't yet fill gaps. Now you can. From this fortnight, code examples cover genuinely NEW patterns; familiar ground ("write tests," "make ruff clean") is stated as a requirement, not walked through. That growing gap between instruction and execution is your skill, made visible.

> 🤖 **Agent Policy — Phase 3 begins.** Cursor Tab back ON. Agents may now *generate* under the permanent standard: file-by-file diff review, explain-back test on every accepted line. Two carve-outs remain through Quarter 1: **eval/test logic and ADRs stay human-authored** — your tests encode your understanding of the business rules, and an agent-written test proving agent-written code is circular. Update `.cursor/rules/learning-phase.mdc` accordingly (rename it `phase-3.mdc` — second rules-file rep).

---

---

## 🔄 REALIGNMENT PASS — ROADMAP CORRECTIONS 21–43 (applied 27 Aug 2026)

⏰ **You are mid-fortnight** — today is Day 39 (Thu 27 Aug). Three items below change what you do **this week**, not next quarter.

1. **🔴 Day 33's exam booking is self-funded.** Corrections 22/32/37: **all certifications are self-funded**, no employer reimbursement applies, and the Month-6 scope conversation is closed (**employment ends 9 Oct 2026**). Book AI-901 and pay the **$99** yourself. Check for a voucher first (Correction 38 notes Cloud Skills Challenge / virtual training day vouchers recur).
2. **🐍 The Day 34 Dockerfile now says `python:3.14-slim`** — Correction 28 pins **Python 3.14** as the floor, standard GIL build only (never `python3.14t`). If you already built the recon-toy image on 3.12, rebuild it on 3.14 when you do retrofit item **R2**; the two-stage pattern and the `--frozen` idiom are unchanged.
3. **✅ Python 3.14 retrofit is APPROVED and scheduled Day 41 (Sat 29 Aug)** — both `learning-journey` and `recon-toy`, before DataVault scaffolds on 3.14 on Day 43. Full command block is inline at Day 41.
4. **🪝 Add pre-commit to `recon-toy` before the Day 34 Docker block** — ~20 minutes, and it belongs in the same session as the Dockerfile because both are "the build is reproducible" claims. Tier A pinned set: `pre-commit-hooks` basics + `detect-private-key` · `ruff-check --fix` **ordered before** `ruff-format` (the linter's fixes can emit changes that then need reformatting; the hook id is `ruff-check`, not the retired bare `ruff`) · `uv-lock` (this is what turns your Correction 13 reproducibility claim from an assertion into an enforced invariant) · `gitleaks`. **The set must be a strict subset of CI** — never a local check that CI does not also run, because hooks and CI silently disagreeing is exactly the defect an interviewer finds.

**Not urgent this fortnight, but now standing policy:** Polars is the default dataframe engine (C35) · Cursor moves to Hobby, OpenCode is the sole harness (C39/40) · the reading layer is live and you are in S1, so *Robust Python* and *AI Engineering* are buy-now (C34) · PostCheck is Flagship #4 (C33).

---

## 📊 WHERE YOU STAND

Environment complete, recon-toy shipped (pipeline + CLI + structlog + ADR 0001), P4E Courses 1–2 done, Mode SQL through aggregation, Docker ~50%, AI-901 underway (~~with reimbursement filed~~ → **self-funded, $99** — C22/32/37). This fortnight: **your code starts talking to Claude**, and recon-toy earns its Dockerfile.

## 🧠 STRATEGIC CONTEXT

Three threads:
1. **Building with the Claude API** (Anthropic Academy — free, first-party, official completion certificate; the Correction 19 ladder's noted Tier-5 anomaly). This is the provider source-of-truth for the SDK that underwrites both flagships and the eventual CCA-F. Target ~40–50% of the 84 lessons this fortnight: messages, system prompts, parameters, streaming, error handling.
2. **Config + validation discipline arrives with the SDK** — the moment secrets and JSON enter your code, Correction 16's `pydantic-settings` (typed config, `SecretStr`) and pydantic models (validating LLM output) stop being abstract standards and become the obvious tool. You'll learn both on real need.
3. **Docker completes** → recon-toy ships its first Dockerfile using the roadmap's `uv sync --frozen` idiom (Correction 13) — your first full production-checklist pass on a project.

Also: Mode SQL Advanced (window functions — the #1 DE interview SQL topic), *AI Prompting for Everyone* videos (no lab slot — the roadmap explicitly says videos suffice here), AI-901 to ~70% with the exam **scheduled** for Week 8.

### New concepts
```
SDK:     Anthropic client, messages API, roles, system prompts, max_tokens/
         temperature, streaming, API error handling
Python:  pydantic BaseModel validation · pydantic-settings BaseSettings +
         SecretStr (Correction 16) · mocking external APIs in tests
SQL:     window functions (ROW_NUMBER, RANK, LAG, SUM OVER), CASE, subqueries
Docker:  writing a Dockerfile · uv sync --frozen · .dockerignore · compose basics
```

---

## 🗓 WEEK 5 (Aug 17–23)

### Week 5 goals
```
□ Claude API course: first 3 sections     □ First 5+ SDK scripts committed
□ Mode SQL: window functions section      □ Docker for Beginners COMPLETE
□ recon-toy Dockerfile builds & runs      □ AI-901 Learn modules 3–4
□ pydantic-settings config in place       □ Post #5 · exam DATE booked
```

### 📌 DAY 29 — Monday, August 17
**Morning:** Anthropic Academy — enroll in *Building with the Claude API*; complete the intro + first messages lessons.
**Evening:**
- [ ] 70 min — **Your first API call.** New project area: `src/learning_journey/claude/`. Create `day29_first_call.py`:

```python
"""Day 29: first Claude API call — the moment the SDK era opens.

Install first:  uv add anthropic
(Runtime dependency — no --dev. Commit pyproject.toml + uv.lock together.)
"""

import anthropic

# The client reads ANTHROPIC_API_KEY from your environment automatically —
# which is WHY Step 8 put it in ~/.zshrc and never in code. If this line
# errors with "api_key not set", your env var isn't loaded (new terminal?).
client = anthropic.Anthropic()

response = client.messages.create(
    model="claude-sonnet-4-6",     # model id — check docs for current names
    max_tokens=500,                # HARD CAP on response length. Always set it:
                                   # it is your cost + runaway guard.
    system=(                       # the SYSTEM prompt sets persistent behavior —
        "You are a retirement-plan communications assistant. "
        "Explain concepts for plan participants: plain English, no jargon, "
        "4 sentences maximum."
    ),
    messages=[                     # the conversation: a list of role+content turns
        {
            "role": "user",
            "content": "What does Box 7 code G on my 1099-R mean?",
        }
    ],
)

# response.content is a LIST of blocks (text, tool calls...). Text lives in .text:
print(response.content[0].text)

# The response also carries USAGE — tokens in/out. Log it from day one;
# cost-awareness is literally a heading in your README standard (Correction 18).
print(f"\ntokens: in={response.usage.input_tokens} out={response.usage.output_tokens}")
```
Run it. Then experiment deliberately: change `max_tokens` to 50 (watch truncation), remove the system prompt (watch the tone change), ask a question outside the system prompt's domain (watch how it handles scope). **Every parameter is a lever; pull each one once.**
- [ ] 30 min — Claude API course: next lesson, replicating its examples in your own files
- [ ] 20 min — Journal + commit (`feat: first anthropic sdk call with usage logging`)

### 📌 DAY 30 — Tuesday, August 18
**Morning:** Claude API course — roles & multi-turn conversations section.
**Evening:**
- [ ] 60 min — Multi-turn: build `day30_conversation.py` — a loop that keeps a `messages` list, appends each user turn and assistant reply, and lets you converse in the terminal. Key learning: **the API is stateless — YOU carry the history**, and history = tokens = cost (print running token totals each turn).
- [ ] 40 min — Mode SQL Advanced: window functions intro. Transcribe with comments:
```sql
-- Window functions: aggregate WITHOUT collapsing rows.
-- GROUP BY answers "total per code"; a window answers "each row AND its
-- share of the total" — both rows and context survive.

-- Running total of distributions by date:
SELECT dist_date,
       gross,
       SUM(gross) OVER (ORDER BY dist_date) AS running_total
  FROM distributions;                -- OVER (...) = "the window"

-- Rank distributions within each Box-7 code:
SELECT box7_code,
       gross,
       RANK() OVER (PARTITION BY box7_code ORDER BY gross DESC) AS rank_in_code
  FROM distributions;               -- PARTITION BY = "restart per group"
-- Interview-famous shape: "top N per group" = wrap this + WHERE rank <= N.
```
Run both against your recon.db.
- [ ] 20 min — Journal + commit

### 📌 DAY 31 — Wednesday, August 19
**Morning:** AI-901 Learn module 3.
**Evening:**
- [ ] 70 min — **Typed config — Correction 16 lands.** Your SDK scripts currently trust the raw environment. Production code validates config at startup. Create `src/learning_journey/claude/settings.py`:

```python
"""Typed configuration via pydantic-settings — Correction 16's named standard.

Install:  uv add pydantic-settings
"""

from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Single config entrypoint. Reads environment variables by field name.

    Why this beats os.environ.get():
    1. FAIL FAST: no default on anthropic_api_key → missing key crashes at
       STARTUP with a clear error, not at 2am mid-pipeline (Correction 16's
       exact phrase).
    2. SecretStr: repr() and any debug print shows '**********', so the key
       cannot leak through a traceback, a log line, or a config dump.
    3. Typed: model gets a str, max_tokens gets an int — typos in .env
       become validation errors, not silent weirdness.
    """

    model_config = SettingsConfigDict(env_prefix="", extra="forbid")

    anthropic_api_key: SecretStr          # ← no default = REQUIRED
    claude_model: str = "claude-sonnet-4-6"
    default_max_tokens: int = 500


settings = Settings()                      # import this everywhere; construct once

# Usage in a client module:
#   from learning_journey.claude.settings import settings
#   client = anthropic.Anthropic(api_key=settings.anthropic_api_key.get_secret_value())
# .get_secret_value() is the ONLY way to read it — leaks require intent.
```
Refactor Days 29–30 scripts to use it. Then prove the mask: `print(settings)` → key shows as `**********`. **That print is the lesson.**
- [ ] 30 min — Claude API course: continue
- [ ] 20 min — Journal + commit (`feat: pydantic-settings config with SecretStr`)

### 📌 DAY 32 — Thursday, August 20
**Morning:** Claude API course — parameters/streaming section.
**Evening:**
- [ ] 60 min — Streaming + graceful errors: `day32_streaming.py` — stream a response chunk-by-chunk (`client.messages.stream(...)`), and wrap a call in try/except for `anthropic.APIStatusError` / `anthropic.APIConnectionError`, logging the failure with structlog instead of crashing. (Note the roadmap's full retry standard is `stamina` — it arrives with the flagship builds; today is just "never let a network blip kill a pipeline.")
- [ ] 40 min — Mode SQL: LAG/LEAD + month-over-month deltas on your synthetic data
- [ ] 20 min — Journal + commit

### 📌 DAY 33 — Friday, August 21
**Morning:** Docker for Beginners — final sections → **course COMPLETE**.
**Evening:**
- [ ] 50 min — AI-901 Learn module 4
- [ ] 30 min — **Book the AI-901 exam** for Week 8 (target Fri Sep 11 or Sat Sep 12 slot; Pearson VUE online or center). Booked = committed. **Pay it yourself — $99, self-funded (C22/32/37); there is no pre-approval and no claim.** ⚠️ Verify the price at checkout: Correction 38 records that Microsoft voucher programs recur through Cloud Skills Challenges and virtual training days — check before paying full price. Add to the **evidence file**.
- [ ] 20 min — Claude API course lesson
- [ ] 20 min — Journal + commit

### 📌 DAY 34 — Saturday, August 22 (5.5h)
**Morning (5:00–8:30):**
- [ ] 120 min — **recon-toy gets its Dockerfile** ⭐ — the roadmap's exact idiom (Correction 13):

```dockerfile
# Dockerfile — recon-toy
# Two-stage pattern: tiny, reproducible, exactly what uv.lock says.

FROM python:3.14-slim AS base

# Install uv inside the image by copying its binary from Astral's image —
# faster and more reproducible than curl-piping an installer at build time.
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

# Copy ONLY the dependency manifests first. Docker caches layers: as long as
# these two files don't change, rebuilds skip dependency installation
# entirely. This ordering trick is the single biggest Docker speed lesson.
COPY pyproject.toml uv.lock ./

# THE ROADMAP IDIOM: --frozen = install EXACTLY uv.lock, refuse to resolve
# anything new. If code demands a package the lockfile lacks, the build
# FAILS — which is correct: byte-reproducible images or nothing.
RUN uv sync --frozen --no-dev
#            └ --no-dev: pytest/ruff don't ship to production images.

# Now the code (changes often → last, so it never busts the dep cache):
COPY src/ src/

# Run through uv so the project's environment is used:
ENTRYPOINT ["uv", "run", "python", "-m", "learning_journey.projects.recon_toy"]
CMD ["--participants", "50"]
# ENTRYPOINT = fixed command · CMD = default args, overridable at run time.
```
Plus `.dockerignore` (`.venv`, `.git`, `__pycache__`, `output/`, `notebooks/`). Build & run:
```bash
docker build -t recon-toy .
docker run --rm recon-toy                       # default 50 participants
docker run --rm recon-toy --participants 200    # CMD overridden
```
**The payoff sentence for your README:** "runs identically on any machine via Docker, dependencies pinned by uv.lock." Update recon-toy's ① Production section with it — a claim you can now actually make.
- [ ] 60 min — Write ADR 0002: `two-stage-docker-with-uv-sync-frozen` (Nygard; consequences: --no-dev means tests don't run *in* the image — they gate *before* the build, in CI, which is coming Week 7)
- [ ] 30 min — Claude API course

**Evening:** 60 min AI Prompting for Everyone (videos — start) · 45 min draft post #5 (artifact: the Dockerfile — "my toy pipeline now ships like production software") · 15 min journal + commit

### 📌 DAY 35 — Sunday, August 23 (2h)
Week summary · publish post #5 · plan Week 6 · check meetup calendar · journal 🎉

---

## 🗓 WEEK 6 (Aug 24–30)

### Week 6 goals
```
□ Claude API course ~50% total            □ Mini-project #3 shipped (see Day 41)
□ pydantic output validation mastered     □ Mode SQL Advanced COMPLETE
□ Tests mock the API (no live calls)      □ AI Prompting videos COMPLETE
□ AI-901 module 5 + practice test #1      □ Post #6 · meetup attended if scheduled
```

### 📌 DAY 36 — Monday, August 24
**Morning:** Claude API course — structured output / JSON section.
**Evening:**
- [ ] 70 min — **Validated structured output** ⭐ — the pattern both flagships live on. `day36_structured.py`:

```python
"""Day 36: LLM output you can TRUST — pydantic validation at the boundary.

The problem: LLMs return text. Text that LOOKS like JSON usually is —
until the one time it isn't, and your pipeline writes garbage downstream.
The pattern: ask for JSON → parse → VALIDATE against a typed schema →
only validated objects cross into your system. Same boundary rule as
Day 4's float(input()), scaled up to AI.
"""

import json

import anthropic
from pydantic import BaseModel, Field, ValidationError

from learning_journey.claude.settings import settings


class Box7Explanation(BaseModel):
    """The CONTRACT for what the model must return.

    pydantic raises ValidationError on any violation — wrong type, missing
    field, out-of-range value. The model doesn't get to be creative here.
    """

    code: str = Field(pattern=r"^[1-9A-Z]$")        # exactly one code char
    meaning: str = Field(min_length=10, max_length=300)
    taxable_generally: bool
    participant_action_needed: bool
    confidence: float = Field(ge=0.0, le=1.0)        # ge/le = bounds


SYSTEM = """You classify IRS 1099-R Box 7 codes. Respond with ONLY a JSON
object matching this schema, no prose, no markdown fences:
{"code": str, "meaning": str, "taxable_generally": bool,
 "participant_action_needed": bool, "confidence": float 0-1}"""


def explain_box7(code: str) -> Box7Explanation:
    client = anthropic.Anthropic(
        api_key=settings.anthropic_api_key.get_secret_value()
    )
    response = client.messages.create(
        model=settings.claude_model,
        max_tokens=settings.default_max_tokens,
        system=SYSTEM,
        messages=[{"role": "user", "content": f"Code: {code}"}],
    )
    raw = response.content[0].text

    try:
        return Box7Explanation.model_validate(json.loads(raw))
    except (json.JSONDecodeError, ValidationError) as err:
        # Boundary rule: report loudly, never pass unvalidated data on.
        # (Flagship version will retry-with-feedback here; v0 fails clean.)
        raise ValueError(f"Model returned invalid output for {code!r}: {err}") from err


if __name__ == "__main__":
    result = explain_box7("G")
    print(f"{result.code}: {result.meaning}")
    print(f"taxable={result.taxable_generally} confidence={result.confidence:.0%}")
```
- [ ] 30 min — Claude API course continue
- [ ] 20 min — Journal + commit (`feat: pydantic-validated structured llm output`)

### 📌 DAY 37 — Tuesday, August 25
**Morning:** Mode SQL — CASE statements + subqueries.
**Evening:** 🎪 Meetup if scheduled (Greenville Data Science ~2nd Thursday is this week — RSVP now). Else: 60 min Claude API course · 40 min SQL practice: rewrite the recon "mismatch buckets" as ONE query with CASE · journal + commit.

### 📌 DAY 38 — Wednesday, August 26
**Morning:** Claude API course.
**Evening:**
- [ ] 70 min — **Testing code that calls an API** ⭐ — without paying per test run. `tests/test_box7_explain.py`:

```python
"""Mocking: tests must be fast, free, deterministic — three things a live
API call is not. So tests replace ("mock") the client and check YOUR logic:
prompt construction, parsing, validation, failure handling. The model's
QUALITY is a different question with a different tool — that's what eval
harnesses measure, and they arrive in Weeks 9–10. Tests ≠ evals; knowing
the difference is a hiring signal in itself.
"""

import json
from unittest.mock import MagicMock, patch

import pytest

from learning_journey.claude.day36_structured import Box7Explanation, explain_box7


def _fake_response(payload: dict) -> MagicMock:
    """Build an object shaped like the SDK's response."""
    fake = MagicMock()
    fake.content = [MagicMock(text=json.dumps(payload))]
    return fake


VALID = {
    "code": "G", "meaning": "Direct rollover to another qualified plan.",
    "taxable_generally": False, "participant_action_needed": False,
    "confidence": 0.97,
}


@patch("learning_journey.claude.day36_structured.anthropic.Anthropic")
def test_valid_payload_parses(mock_cls):
    # patch() swaps the real class for a fake INSIDE the module under test.
    mock_cls.return_value.messages.create.return_value = _fake_response(VALID)
    result = explain_box7("G")
    assert isinstance(result, Box7Explanation)
    assert result.taxable_generally is False


@patch("learning_journey.claude.day36_structured.anthropic.Anthropic")
def test_invalid_confidence_rejected(mock_cls):
    bad = VALID | {"confidence": 1.7}          # dict merge; 1.7 breaks le=1.0
    mock_cls.return_value.messages.create.return_value = _fake_response(bad)
    with pytest.raises(ValueError):
        explain_box7("G")                       # boundary must refuse it


@patch("learning_journey.claude.day36_structured.anthropic.Anthropic")
def test_non_json_rejected(mock_cls):
    fake = MagicMock(); fake.content = [MagicMock(text="Sure! Here's the JSON:")]
    mock_cls.return_value.messages.create.return_value = fake
    with pytest.raises(ValueError):
        explain_box7("G")
```
`uv run pytest -v` — note the suite runs in milliseconds with zero API cost.
- [ ] 30 min — AI-901 module 5
- [ ] 20 min — Journal + commit (`test: mocked api boundary tests`)

### 📌 DAY 39 — Thursday, August 27
**Morning:** AI Prompting for Everyone — videos (finish or near).
**Evening:** 60 min Claude API course · 40 min Mode SQL Advanced final sections → **COMPLETE** · 20 min journal + commit

### 📌 DAY 40 — Friday, August 28
**Morning:** AI-901 practice test #1 — score it honestly; list weak areas in `notebooks/ai901-notes.md`.
**Evening:** 60 min drill the weak areas on Microsoft Learn · 40 min Claude API course · 20 min journal + commit

### 📌 DAY 41 — Saturday, August 29 (5.5h)
**Morning (5:00–8:30):**
- [ ] 150 min — **Mini-project #3: `plan-doc-summarizer`** ⭐ — everything this fortnight taught, composed. Requirements (build it; the plan no longer hands you the file):
  - Input: 3 synthetic plan-document excerpts you write (`data/spd_excerpts/*.txt` — invented plan rules, ~300 words each; NEVER real plan language)
  - For each: one Claude call producing a pydantic-validated `PlanSummary` (plan_name, eligibility_summary, vesting_summary, three_key_facts: `list[str]`, reading_level_ok: bool)
  - structlog events per document (tokens in/out, validation pass/fail); settings via pydantic-settings; failures logged and skipped, never crashing the batch
  - Report written to `output/` · 6+ mocked tests · ruff clean · README section in ①Production/③Architecture order (Cost omitted honestly — or included if you note real token costs: your call, defend it in the ADR)
  - ADR 0003: one real decision you made and its trade-off
- [ ] 30 min — ✅ **PYTHON 3.14 RETROFIT** (approved 27 Aug) ⭐ · 🆕 **Correction 28**. Do it today, before DataVault scaffolds on 3.14 on Day 43 — two repos on two interpreters is exactly the drift the single-source rule exists to prevent.

```bash
# Do this in BOTH repos: learning-journey and recon-toy
uv python install 3.14        # standard GIL build. NEVER python3.14t (Correction 28)
cd ~/dev/learning-journey
uv python pin 3.14            # rewrites .python-version
```
Then edit `pyproject.toml` — **`requires-python` is the single source; four consumers read from it:**
```toml
[project]
requires-python = ">=3.14"     # ← THE single declaration

[tool.ruff]
target-version = "py314"       # consumer 1

[tool.mypy]
python_version = "3.14"        # consumer 2
```
```bash
# consumer 3: Dockerfile   -> FROM python:3.14-slim AS base
# consumer 4: CI matrix    -> python-version: "3.14"  (if pinned explicitly)
rm -rf .venv && uv sync        # rebuild the env against the new floor
uv run pytest && uv run mypy src/ && uv run ruff check .
git commit -m "build: raise python floor 3.12 -> 3.14 (roadmap correction 28)"
```
> **Why a mismatch is a CI failure, not a lint warning.** Correction 28 makes `requires-python` authoritative and the other four sites *derived*. If ruff targets py312 while the interpreter is 3.14, ruff will happily pass code that the runtime treats differently — a green build that proves nothing. Same one-source-no-drift discipline as `uv.lock` under the pre-commit `uv-lock` hook, and as Structurizr→Mermaid under Correction 14.
> **Why 3.14 and not 3.13 or 3.15:** 3.12 went security-only around Oct 2025 (no bug fixes — every non-security defect becomes yours to work around); 3.13's bug-fix window closes ~Oct 2026, two months out, so it is a dead end rather than a safe middle; 3.15 ships Oct 2026 and is **explicitly not adopted on release**. Falsifier: raise the floor only when a named dependency in a committed lockfile requires it, or when 3.14 leaves security support — never to chase a release.
> ⚠️ **Banked for Stage 2:** Airflow's 3.14 constraint files are reported out of sync between the published Docker image and pip/uv. Documented workaround — fall back to `constraints-3.13.txt` **for the Airflow service only**. That is a constraint-file selection, not a second Python version; the interpreter stays 3.14.

**Evening:** 60 min Claude API course · 45 min draft post #6 (finance→tech bridge: "I taught an AI to summarize plan documents — and taught my tests not to trust it") · 15 min journal + commit

### 📌 DAY 42 — Sunday, August 30 (2h)
Week summary · publish post #6 · **AI Prompting videos done → log as Tier-5 evidence** · plan Weeks 7–8 · journal 🎉

---

## 📊 2-WEEK SUCCESS METRICS
```
□ Claude API course ~50% (sections logged) □ Dockerfile builds; --frozen idiom used
□ 5+ SDK scripts · streaming · errors      □ ADRs 0002–0003 written (yours)
□ pydantic + pydantic-settings in use      □ Mode SQL Advanced complete
□ SecretStr masking proven                 □ AI Prompting videos done (Tier 5 log)
□ 8+ mocked tests, zero live-API tests     □ AI-901 exam BOOKED + practice test #1
□ Mini-project #3 shipped                  □ Posts #5–6 · 24+ commits · rules file
□ ✅ Python 3.14 retrofit: both repos green  □ pre-commit on recon-toy
                                             at Phase 3 · Tab re-enabled
```
**Passing bar: 80%.** Non-negotiables: mini-project #3 (the SDK-fluency proof) and the booked AI-901 exam.

---

## 🔭 WHAT COMES NEXT
**Weeks 7–8 (Aug 31 – Sep 13): the flagship era opens.** DataVault S1 v0 gets its own production-scaffolded repo — synthetic Matrix/Relius-shaped generators, a pydantic canonical model, recon engine, Box-7 rules skeleton — plus your first **CI pipeline** (GitHub Actions running ruff + pytest as a blocking gate). Claude API course reaches tool use + prompt caching. CS50P starts. And Week 8 ends with the **AI-901 exam** — **evidence-file item #1** (self-funded, $99).

---
*Aligned to Career Roadmap v10.0 (Corrections 1–20). No roadmap edits made; propose→approve governance applies.*