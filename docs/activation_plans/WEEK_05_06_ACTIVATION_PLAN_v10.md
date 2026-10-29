# 🚀 WEEKS 5–6 MASTER ACTIVATION PLAN (v10.0)

## The SDK Era Opens | August 17–30, 2026

**Document Version:** 3.3 — 📈 **TRADING LANE EXPANSION** (13 Oct 2026, roadmap C63–C64) on the 3.2 🎯 **READINESS GATE** (9 Oct 2026, roadmap C59) on the 3.1 ⚖️ **PRIORITY REBALANCE** (8 Oct 2026, C58) and the 3.0 job-first re-cut · fresh 12-week template from Mon 20 Jul 2026
**Covers:** Monday, August 17 – Sunday, August 30, 2026 (Stage 1 · Month 2 · Weeks 5–6)
**Aligned To:** Career Roadmap v10.0, **Corrections 1–64** (C58 applied 8 Oct 2026 · C59 applied 9 Oct 2026 · 📈 C63–C64 applied 13 Oct 2026; C60–C62 do not touch these weeks) · Target: **Analytics Engineer first door · Data Engineer parallel** (C22 §3, C54)
**Prerequisite:** Weeks 3–4 metrics ≥80% (non-negotiables: recon-toy shipped + ~~AI-901 kickoff~~ 🆕 Kimball Ch. 1–2)
**Weekly Hours:** 25 (same block schedule)

> **Plans get terser from here — deliberately.** Weeks 1–4 spelled out every line because you couldn't yet fill gaps. Now you can. From this fortnight, code examples cover genuinely NEW patterns; familiar ground ("write tests," "make ruff clean") is stated as a requirement, not walked through. That growing gap between instruction and execution is your skill, made visible.

> 🤖 **Agent Policy — Phase 3 begins.** Cursor Tab back ON. Agents may now *generate* under the permanent standard: file-by-file diff review, explain-back test on every accepted line. Two carve-outs remain through Quarter 1: **eval/test logic and ADRs stay human-authored** — your tests encode your understanding of the business rules, and an agent-written test proving agent-written code is circular. Update `.cursor/rules/learning-phase.mdc` accordingly (rename it `phase-3.mdc` — second rules-file rep).

---

---



## 🧭 v3.0 JOB-FIRST RE-CUT — this fortnight (approved 6 Oct 2026)

Part of the fresh 12-week template from Mon 20 Jul 2026, 25 hrs/week, aligned to Corrections 1–64. Full rationale: the v3.0, v3.1 and v3.2 blocks in Weeks 1–2. **This is the fortnight dbt arrives.**


| Lane              | This fortnight in v3.0                                                                                                                                                                                                                                                                                                                                          |
| ----------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| L1 Foundations    | 🆕 **dbt Fundamentals** (dbt Labs, free, ~5 hrs, certificate — roadmap S2 row 5️⃣ taken early under C54 §5) in the slots *AI Prompting for Everyone* held (→ flex/Q2). Mode SQL Advanced finishes — dbt is that SQL, modular and tested · ⚖️ **v3.1:** **Kimball Ch. 3–4** + **AE interview reps #0** in the freed AI-901 slots; dbt Fundamentals starts Friday |
| L2 AE/DE flagship | recon-toy's Dockerfile (unchanged)                                                                                                                                                                                                                                                                                                                              |
| L3 Applied AI     | Claude API course target **~35%** (slots went to dbt and Kimball); mini-project #3 unchanged · ~~AI-901 modules 3–5, practice test #1, booking~~ → ⏭️ **Q2, Weeks 13–14** (C58)                                                                                                                                                                                 |
| L4 Trading 🆕     | **Day 41 — the trading lane opens:** a market-data dbt rehearsal that proves the knowledge-time rule in a test · 📈 **v3.3:** Day 41 fixed in place (two clocks, `asof left join`, boundary events) + twins on Day 32 (bars + the generator, pulled forward) and Day 40 (volume dry-up islands)                                                                 |
| L5 Job search     | Day 35: list 15 → 20 + résumé v0 skeleton · Day 42: tracker update                                                                                                                                                                                                                                                                                              |
| Retired           | The Day-41 Python 3.14 retrofit — the template starts on 3.14; its block stays as collapsed reference                                                                                                                                                                                                                                                           |


---



## 🔄 REALIGNMENT PASS — ROADMAP CORRECTIONS 21–43 (applied 27 Aug 2026)

Standing rulings from Corrections 21–43 that land in this fortnight, in template form (Corrections 44–54 are applied in the v3.0 block above):

1. ⏭️ **v3.1 (C58): AI-901 is not booked this fortnight** — the exam moves to Q2 (Weeks 13–14). The funding facts below still apply when you book it then. ~~**🔴 Day 33's exam booking is self-funded.**~~ Corrections 22/32/37: **all certifications are self-funded**, no employer reimbursement applies, and the Month-6 scope conversation is closed (**employment ends 9 Oct 2026**). Book AI-901 and pay the **$99** yourself. Check for a voucher first (Correction 38 notes Cloud Skills Challenge / virtual training day vouchers recur).
2. **🐍 The Day 34 Dockerfile now says** `python:3.14-slim` — Correction 28 pins **Python 3.14** as the floor, standard GIL build only (never `python3.14t`). If you already built the recon-toy image on 3.12, rebuild it on 3.14 when you do retrofit item **R2**; the two-stage pattern and the `--frozen` idiom are unchanged.
3. ~~**✅ Python 3.14 retrofit is APPROVED and scheduled Day 41 (Sat 29 Aug)** — both~~ `learning-journey` ~~and~~ `recon-toy`~~, before DataVault scaffolds on 3.14 on Day 43.~~ → ⏭️ **v3.0: not needed** — the template starts every repo on 3.14 at setup. Day 41's 30-minute slot now finishes dbt Fundamentals; the command block stays at Day 41, collapsed, as reference.
4. **🪝 Add pre-commit to** `recon-toy` **before the Day 34 Docker block** — ~20 minutes, and it belongs in the same session as the Dockerfile because both are "the build is reproducible" claims. Tier A pinned set: `pre-commit-hooks` basics + `detect-private-key` · `ruff-check --fix` **ordered before** `ruff-format` (the linter's fixes can emit changes that then need reformatting; the hook id is `ruff-check`, not the retired bare `ruff`) · `uv-lock` (this is what turns your Correction 13 reproducibility claim from an assertion into an enforced invariant) · `gitleaks`. **The set must be a strict subset of CI** — never a local check that CI does not also run, because hooks and CI silently disagreeing is exactly the defect an interviewer finds.

**Not urgent this fortnight, but now standing policy:** Polars is the default dataframe engine (C35) · Cursor moves to Hobby, ~~OpenCode is the sole harness (C39/40)~~ → 📈 v3.3 text fix: **dual harness** — OpenCode (in Cursor) writes, Claude Code (in VS Code) reviews read-only (C42 §1 superseded C39 §9) · the reading layer is live and you are in S1, so *Robust Python* and *AI Engineering* are buy-now (C34) · PostCheck is Flagship #4 (C33).

---



## 📊 WHERE YOU STAND

Environment complete, recon-toy shipped (pipeline + CLI + structlog + ADR 0001), P4E Courses 1–2 done, Mode SQL through aggregation, Docker ~50%, 🆕 Kimball Ch. 1–2 read (~~AI-901 underway~~ → ⏭️ Q2, C58). This fortnight: **your code starts talking to Claude**, and recon-toy earns its Dockerfile.

## 🧠 STRATEGIC CONTEXT

Three threads:

1. **Building with the Claude API** (Anthropic Academy — free, first-party, official completion certificate; the Correction 19 ladder's noted Tier-5 anomaly). This is the provider source-of-truth for the SDK that underwrites both flagships and the eventual CCA-F. Target ~35% of the 84 lessons this fortnight (🆕 v3.0/v3.1: slots went to dbt and Kimball): messages, system prompts, parameters, streaming, error handling.
2. **Config + validation discipline arrives with the SDK** — the moment secrets and JSON enter your code, Correction 16's `pydantic-settings` (typed config, `SecretStr`) and pydantic models (validating LLM output) stop being abstract standards and become the obvious tool. You'll learn both on real need.
3. **Docker completes** → recon-toy ships its first Dockerfile using the roadmap's `uv sync --frozen` idiom (Correction 13) — your first full production-checklist pass on a project.
4. 🆕 **dbt arrives (v3.0)** — *dbt Fundamentals* (dbt Labs Learn, free, ~5 hrs, certificate; roadmap Stage 2 core row 5️⃣, pulled forward under C54 §5's "S2 work done first"). It lands now because Mode SQL Advanced — window functions, CASE, subqueries — finishes this fortnight, and dbt is that SQL made modular, version-controlled and tested. Do the course's setup on **dbt Core 1.12 + DuckDB locally** (see the tooling note in the Weeks 1–2 v3.0 block). Then **the trading lane opens**: a small market-data dbt rehearsal on Day 41.

Also: Mode SQL Advanced (window functions — the #1 DE interview SQL topic), ~~*AI Prompting for Everyone* videos~~ (🆕 v3.0: moved to flex/Q2 — still videos-only when you take it), ~~AI-901 to ~70% with the exam scheduled for Week 8~~ → ⏭️ Q2 (C58). 🆕 **Kimball Ch. 3–4**: declare the grain of the distributions fact *before* DataVault builds it on Day 43.

### New concepts

```
SDK:     Anthropic client, messages API, roles, system prompts, max_tokens/
         temperature, streaming, API error handling
Python:  pydantic BaseModel validation · pydantic-settings BaseSettings +
         SecretStr (Correction 16) · mocking external APIs in tests
SQL:     window functions (ROW_NUMBER, RANK, LAG, SUM OVER), CASE, subqueries
Docker:  writing a Dockerfile · uv sync --frozen · .dockerignore · compose basics
dbt:     models · ref() · sources · seeds · staging → marts · generic +
         singular tests · dbt build (🆕 v3.0)
SQL:     window frames that exclude the current row · DuckDB ASOF JOIN (🆕)
Model:   four-step design · declaring the grain · transaction / periodic /
         accumulating snapshot facts (Kimball Ch. 3–4, 🆕 v3.1)
```

---



## 🗓 WEEK 5 (Aug 17–23)



### Week 5 goals

- [ ] Claude API course: first 3 sections
- [ ] Mode SQL: window functions section
- [ ] recon-toy Dockerfile builds & runs
- [ ] pydantic-settings config in place
- [ ] 🆕 dbt Fundamentals started (Fri)

- [ ] First 5+ SDK scripts committed
- [ ] Docker for Beginners COMPLETE
- [ ] ~~AI-901 Learn modules 3–4~~ → 🆕 Kimball Ch. 3 + grain notes
- [ ] Post #5 · ~~exam DATE booked~~ (Q2)



### 📌 DAY 29 — Monday, August 17

**Morning:** Anthropic Academy — enroll in *Building with the Claude API*; complete the intro + first messages lessons.
**Evening:**

- [x] 70 min — **Your first API call.** New project area: `src/learning_journey/claude/`. Create `day29_first_call.py`:

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
    model="claude-sonnet-4-6",  # model id — check docs for current names
    max_tokens=500,  # HARD CAP on response length. Always set it:
    # it is your cost + runaway guard.
    system=(  # the SYSTEM prompt sets persistent behavior —
        "You are a retirement-plan communications assistant. "
        "Explain concepts for plan participants: plain English, no jargon, "
        "4 sentences maximum."
    ),
    messages=[  # the conversation: a list of role+content turns
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

- [x] 30 min — Claude API course: next lesson, replicating its examples in your own files
- [ ] 20 min — Journal + commit (`feat: first anthropic sdk call with usage logging`)



### 📌 DAY 30 — Tuesday, August 18

**Morning:** Claude API course — roles & multi-turn conversations section.
**Evening:**

- [x] 60 min — Multi-turn: build `day30_conversation.py` — a loop that keeps a `messages` list, appends each user turn and assistant reply, and lets you converse in the terminal. Key learning: **the API is stateless — YOU carry the history**, and history = tokens = cost (print running token totals each turn).
- [x] 40 min — Mode SQL Advanced: window functions intro. Transcribe with comments:

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

**Morning:** ~~AI-901 Learn module 3~~ → ⏭️ Q2 (C58). 🆕 **Kimball Ch. 3 — finish**, then write `docs/modeling-notes.md` in `learning_journey`: the **business process** (a plan distribution), the **grain** of its fact (*one row per distribution per source system*), its **dimensions** (participant, plan, Box-7 code, date) and its **facts** (gross, taxable, withholding). This page is DataVault's design input on Day 43.
**Evening:**

- [x] 70 min — **Typed config — Correction 16 lands.** Your SDK scripts currently trust the raw environment. Production code validates config at startup. Create `src/learning_journey/claude/settings.py`:

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

    anthropic_api_key: SecretStr  # ← no default = REQUIRED
    claude_model: str = "claude-sonnet-4-6"
    default_max_tokens: int = 500


settings = Settings()  # import this everywhere; construct once

# Usage in a client module:
#   from learning_journey.claude.settings import settings
#   client = anthropic.Anthropic(api_key=settings.anthropic_api_key.get_secret_value())
# .get_secret_value() is the ONLY way to read it — leaks require intent.
```

Refactor Days 29–30 scripts to use it. Then prove the mask: `print(settings)` → key shows as `**********`. **That print is the lesson.**

- [x] 30 min — Claude API course: continue
- [ ] 20 min — Journal + commit (`feat: pydantic-settings config with SecretStr`)



### 📌 DAY 32 — Thursday, August 20

**Morning:** Claude API course — parameters/streaming section.
**Evening:**

- [x] 60 min — Streaming + graceful errors: `day32_streaming.py` — stream a response chunk-by-chunk (`client.messages.stream(...)`), and wrap a call in try/except for `anthropic.APIStatusError` / `anthropic.APIConnectionError`, logging the failure with structlog instead of crashing. (Note the roadmap's full retry standard is `stamina` — it arrives with the flagship builds; today is just "never let a network blip kill a pipeline.")
- [x] 40 min — Mode SQL: LAG/LEAD + month-over-month deltas on your synthetic data
- [x] 📈 **Trading twin #6 (+40 min · v3.3, C64)** — the same window functions on market bars, and Day 41's generator written early so Saturday starts ahead. *(Day full? →* `notes/trading/twin-queue.md`*; Day 41 then writes the generator as originally planned.)*
  1. `uv add duckdb`, then type `scripts/gen_market_seed.py` — the bars half of the generator (Day 41 adds the events):

```python
"""Seeded synthetic market data for practice — invented tickers, invented prices.

Nothing here is vendor data, so a public repo raises no licence question.
Run:  uv run python scripts/gen_market_seed.py --out data/market_seed
"""

import argparse
import csv
import random
from datetime import date, timedelta
from pathlib import Path

SEED = 41  # same seed -> same files, every run
TICKERS = ["ALFA", "BRVO", "CHRL", "DLTA", "ECHO"]
N_SESSIONS = 120
FIRST_DAY = date(2026, 1, 5)  # a Monday


def trading_days(first: date, n: int) -> list[date]:
    """Weekdays only. Holidays are ignored: a documented simplification."""
    days, d = [], first
    while len(days) < n:
        if d.weekday() < 5:  # 0=Mon ... 4=Fri
            days.append(d)
        d += timedelta(days=1)
    return days


def make_bars(rng: random.Random, days: list[date]) -> list[dict]:
    rows = []
    for ticker in TICKERS:
        close = rng.uniform(8, 60)
        for i, d in enumerate(days):
            open_ = round(close * (1 + rng.gauss(0, 0.01)), 2)  # overnight gap
            close = round(open_ * (1 + rng.gauss(0, 0.02)), 2)
            high = round(max(open_, close) * (1 + abs(rng.gauss(0, 0.01))), 2)
            low = round(min(open_, close) * (1 - abs(rng.gauss(0, 0.01))), 2)
            volume = int(rng.lognormvariate(13, 0.4))
            if ticker == "DLTA" and 60 <= i < 65:  # PLANTED: a 5-session volume dry-up
                volume = int(volume * 0.3)
            rows.append(
                {
                    "ticker": ticker,
                    "session_date": d.isoformat(),
                    "open": open_,
                    "high": high,
                    "low": low,
                    "close": close,
                    "volume": volume,
                }
            )
    return rows


def write_csv(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", type=Path, default=Path("data/market_seed"))
    args = parser.parse_args()
    rng = random.Random(SEED)  # never the global random: reproducibility
    days = trading_days(FIRST_DAY, N_SESSIONS)
    write_csv(args.out / "bars_daily.csv", make_bars(rng, days))


if __name__ == "__main__":
    main()
```

1. `sql/twins/day32_bar_windows.sql` — run it with `uv run python -c "import duckdb, pathlib; print(duckdb.sql(pathlib.Path('sql/twins/day32_bar_windows.sql').read_text()))"`:

```sql
-- Daily return, overnight gap, next open — and the RVOL leak, side by side
select ticker, session_date, close,
       close / lag(close) over w - 1  as daily_return,
       open  / lag(close) over w - 1  as overnight_gap,   -- today's open vs yesterday's close
       lead(open) over w              as next_open,       -- fine in a LABEL, a leak in a FEATURE
       volume / avg(volume) over (partition by ticker order by session_date
                rows between 20 preceding and 1 preceding) as rvol_clean,
       volume / avg(volume) over (partition by ticker order by session_date
                rows between 19 preceding and current row) as rvol_leaky
from read_csv('data/market_seed/bars_daily.csv')
window w as (partition by ticker order by session_date)
order by ticker, session_date;
```

> Same `LAG` as the month-over-month drill, different grain: one row per security per **session**, not per month. `rvol_leaky` puts today's volume inside its own baseline. On quiet days the two columns barely differ; on the highest-volume day of each ticker the leaky one reads lower, because the spike dilutes itself — and spikes are exactly what a trigger is built to catch. Sort by `rvol_clean desc` to see it, then read Day 41's step 3 again. Commit the CSVs? **No** — `data/market_seed/` goes in `.gitignore`; the seeded generator *is* the data.

- [ ] 20 min — Journal + commit



### 📌 DAY 33 — Friday, August 21

**Morning:** Docker for Beginners — final sections → **course COMPLETE**.
**Evening:**

- [ ] 80 min — 🆕 **dbt Fundamentals — start** (moved up a day, C58): learn.getdbt.com, free; set it up on **dbt Core 1.12 + DuckDB locally** rather than a cloud trial; intro + models sections.
- [ ] ~~50 min — AI-901 Learn module 4~~ · ~~30 min — Book the AI-901 exam for Week 8~~ → ⏭️ **Q2 (C58)**: one calendar reminder for Week 13 to book it — the self-funded $99 and the voucher check (Correction 38) still apply then.
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
- [ ] 30 min — 🆕 **Kimball Ch. 3 exercise** (v3.1): draw DataVault's bus-matrix row — the distribution process against its four dimensions — and add it to `docs/modeling-notes.md` ~~· Claude API course~~

**Evening:** 60 min 🆕 **dbt Fundamentals — sources + seeds sections** (continuing from Friday) · ~~AI Prompting for Everyone~~ (flex) · 45 min draft post #5 (artifact: the Dockerfile — "my toy pipeline now ships like production software") · 15 min journal + commit

### 📌 DAY 35 — Sunday, August 23 (2h)

Week summary + 🆕 lane-hours total (C58) · publish post #5 · plan Week 6 · check meetup calendar · 🆕 20 min **Job lane:** targets 15 → 20; start a **résumé v0 skeleton** in the private workspace, built from `evidence.md` (sections only — content arrives as artifacts ship) · journal 🎉

---



## 🗓 WEEK 6 (Aug 24–30)



### Week 6 goals

- [ ] Claude API course ~35% total (v3.1)
- [ ] pydantic output validation mastered
- [ ] Tests mock the API (no live calls)
- [ ] ~~AI-901 module 5 + practice test #1~~ → 🆕 Kimball Ch. 4 + AE reps #0
- [ ] 🆕 Trading lane: market-data dbt rehearsal — `dbt build` green, lookahead test proven

- [ ] Mini-project #3 shipped (see Day 41)
- [ ] Mode SQL Advanced COMPLETE
- [ ] 🆕 dbt Fundamentals COMPLETE (certificate)

- [ ] Post #6 · meetup attended if scheduled



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

    code: str = Field(pattern=r"^[1-9A-Z]$")  # exactly one code char
    meaning: str = Field(min_length=10, max_length=300)
    taxable_generally: bool
    participant_action_needed: bool
    confidence: float = Field(ge=0.0, le=1.0)  # ge/le = bounds


SYSTEM = """You classify IRS 1099-R Box 7 codes. Respond with ONLY a JSON
object matching this schema, no prose, no markdown fences:
{"code": str, "meaning": str, "taxable_generally": bool,
 "participant_action_needed": bool, "confidence": float 0-1}"""


def explain_box7(code: str) -> Box7Explanation:
    client = anthropic.Anthropic(api_key=settings.anthropic_api_key.get_secret_value())
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

- [ ] 30 min — 🆕 **SQL rep** (v3.1): one CTE chain + one window function on `recon.db`, timed — the shape every dbt model and AE screen uses ~~· Claude API course continue~~
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
    "code": "G",
    "meaning": "Direct rollover to another qualified plan.",
    "taxable_generally": False,
    "participant_action_needed": False,
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
    bad = VALID | {"confidence": 1.7}  # dict merge; 1.7 breaks le=1.0
    mock_cls.return_value.messages.create.return_value = _fake_response(bad)
    with pytest.raises(ValueError):
        explain_box7("G")  # boundary must refuse it


@patch("learning_journey.claude.day36_structured.anthropic.Anthropic")
def test_non_json_rejected(mock_cls):
    fake = MagicMock()
    fake.content = [MagicMock(text="Sure! Here's the JSON:")]
    mock_cls.return_value.messages.create.return_value = fake
    with pytest.raises(ValueError):
        explain_box7("G")
```

`uv run pytest -v` — note the suite runs in milliseconds with zero API cost.

- [ ] 30 min — ~~AI-901 module 5~~ → 🆕 **Kimball Ch. 4, part 1** — the three fact-table types: transaction, periodic snapshot, accumulating snapshot
- [ ] 20 min — Journal + commit (`test: mocked api boundary tests`)



### 📌 DAY 39 — Thursday, August 27

**Morning:** 🆕 **dbt Fundamentals** — tests section (generic + singular) and its exercises. ~~AI Prompting for Everyone~~ (flex/Q2).
**Evening:** 30 min Claude API course · 30 min 🆕 **dbt from memory**: rebuild the course's staging and mart models on DuckDB with the notes closed · 40 min Mode SQL Advanced final sections → **COMPLETE** · 20 min journal + commit

### 📌 DAY 40 — Friday, August 28

**Morning:** ~~AI-901 practice test #1~~ → ⏭️ Q2 (C58). 🆕 **dbt Fundamentals — documentation + deployment sections → finish.**
**Evening:** 60 min 🆕 **Kimball Ch. 4, part 2** — periodic and accumulating snapshots; add to `docs/modeling-notes.md` which DataVault output is a **periodic snapshot** (the weekly corrections mart, Day 55) and which future fact is **accumulating** (a distribution's lifecycle: received → IGO/NIGO → processed → 1099 issued — PostCheck's core) · 40 min 🆕 **AE interview reps #0** on `recon.db` — the three screen staples: top-N per group, dedupe with `ROW_NUMBER`, gaps-and-islands · 20 min journal + commit ~~· 60 min AI-901 drill~~

📈 **Trading twin #7 (+15 min · v3.3, C64)** — after the `recon.db` reps (top-N and dedupe stay there), one more gaps-and-islands on Day 32's bars: **the longest run of sessions with volume under 50% of its trailing 20-session average** — the volume dry-up AFC's T4e and Crucible's SW-B both read. *(Needs twin #6's generator; if #6 is queued, queue this too.)*

```sql
with flagged as (
    select ticker, session_date,
           row_number() over (partition by ticker order by session_date) as session_n,
           volume < 0.5 * avg(volume) over (partition by ticker order by session_date
                      rows between 20 preceding and 1 preceding)     as is_dry
    from read_csv('data/market_seed/bars_daily.csv')
),
dry as (
    -- consecutive dry sessions share one value of (session_n − row number among dry rows)
    select ticker, session_date,
           session_n - row_number() over (partition by ticker order by session_date) as island
    from flagged
    where is_dry
),
runs as (
    select ticker, island, min(session_date) as run_start, max(session_date) as run_end,
           count(*) as dry_sessions
    from dry
    group by ticker, island
)
select ticker, run_start, run_end, dry_sessions
from runs
qualify row_number() over (partition by ticker order by dry_sessions desc, run_start) = 1
order by dry_sessions desc;
```

Expected: DLTA's planted 5-session run tops the list. Count sessions, not calendar days — `session_n` is why a weekend doesn't break a run. Then spot the trap: a 2-session ALFA run in early January, built on a baseline of one or two sessions. AFC requires a full 20-session window, so add `count(volume) over (… same frame …) = 20` to the dry flag and watch it disappear.

### 📌 DAY 41 — Saturday, August 29 (5.5h)

**Morning (5:00–8:30):**

- [ ] 150 min — **Mini-project #3:** `plan-doc-summarizer` ⭐ — everything this fortnight taught, composed. Requirements (build it; the plan no longer hands you the file):
  - Input: 3 synthetic plan-document excerpts you write (`data/spd_excerpts/*.txt` — invented plan rules, ~300 words each; NEVER real plan language)
  - For each: one Claude call producing a pydantic-validated `PlanSummary` (plan_name, eligibility_summary, vesting_summary, three_key_facts: `list[str]`, reading_level_ok: bool)
  - structlog events per document (tokens in/out, validation pass/fail); settings via pydantic-settings; failures logged and skipped, never crashing the batch
  - Report written to `output/` · 6+ mocked tests · ruff clean · README section in ①Production/③Architecture order (Cost omitted honestly — or included if you note real token costs: your call, defend it in the ADR)
  - ADR 0003: one real decision you made and its trade-off
- [ ] 30 min — 🆕 **dbt Fundamentals — final quiz → certificate into** `evidence.md`**.**

⏭️ **Python 3.14 retrofit — reference only in the v3.0 template** (every repo starts on 3.14 at setup; keep this for any repo created on an older floor)

~~✅ **PYTHON 3.14 RETROFIT** (approved 27 Aug) · Correction 28. Do it today, before DataVault scaffolds on 3.14 on Day 43.~~

```bash
# Do this in BOTH repos: learning-journey and recon-toy
uv python install 3.14        # standard GIL build. NEVER python3.14t (Correction 28)
cd ~/dev/learning-journey
uv python pin 3.14            # rewrites .python-version
```

Then edit `pyproject.toml` — `requires-python` **is the single source; four consumers read from it:**

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

**Evening (8:00–10:00):** 🆕 **TRADING LANE OPENS — market-data dbt rehearsal** ⭐ (105 min · 📈 **+15 min in v3.3** — the evening runs to ~10:15, or test 4 below moves to the twin queue) · 15 min journal + commit. ~~60 min Claude API course · 45 min draft post #6~~ → post #6 moves to Sunday.

> 🆕 **Why this rehearsal, and why trading data.** recon-toy rehearsed DataVault's *Python* shape; this rehearses its **dbt** shape before Day 43 — on the kind of data your trading projects run on. It also proves, in a test, the rule AFC's backtest lives or dies by (C46 §3): **an event may drive an entry only if it was known before that session's open.** The data is **synthetic** (a seeded generator), so a public repo raises no market-data licensing question. It lives in `learning_journey` (practice), not in AFC — AFC's Stage-1 sheet keeps dbt out of S1.

```bash
cd ~/dev/learning-journey
uv add --group dbt "dbt-core>=1.12" dbt-duckdb        # dbt Core 1.12 = first line on Python 3.14
mkdir -p dbt && cd dbt && uv run dbt init market_rehearsal --skip-profile-setup
```

`dbt/market_rehearsal/profiles.yml` — no secrets, because DuckDB is a local file (gitignore `*.duckdb` and `target/`):

```yaml
market_rehearsal:
  target: dev
  outputs:
    dev:
      type: duckdb
      path: rehearsal.duckdb
```

**Build (75 min):**

1. `scripts/gen_market_seed.py` — seeded generator → `seeds/bars_daily.csv` (5 invented tickers × 120 sessions: ticker, session_date, open, high, low, close, volume) and `seeds/insider_events.csv` (ticker, event_id, txn_code `P`, `filed_at` ~~timestamp~~ 📈 **two clocks**: `filing_date` and `accepted_at` — plant some filings before the open, some during the session, some after the close). Times are naive America/New_York — note it as a deliberate simplification. *(Twin #6 already wrote the bars half? Add only the events below.)*
  > 📈 **v3.3 fix (C64) — why two clocks.** AFC's knowledge time is the EDGAR **acceptance datetime**, not the filing date (AFC v9.1 §4.2, §5.3). They differ in exactly the case that leaks: Forms 3, 4 and 5 accepted between 5:30 and 10:00 p.m. ET keep **that day's** filing date, so a date-only join lets a filing accepted at 18:00 "trade" at that morning's open. The SEC's own quarterly *Insider Transactions Data Sets* carry `FILING_DATE` only — no acceptance time — so this is the trap real data sets for you.

```python
from datetime import datetime, time  # add to the imports


def make_events(rng: random.Random, days: list[date]) -> tuple[list[dict], dict]:
    """Form 4 purchases (code P). Two clocks per filing: filing_date and accepted_at."""
    events = []

    def add(event_id, ticker, d, t, boundary_case=""):
        # Forms 3/4/5 accepted up to 10 p.m. ET keep that day's filing date;
        # most other EDGAR forms accepted after 5:30 p.m. get the NEXT business day.
        events.append(
            {
                "event_id": event_id,
                "ticker": ticker,
                "txn_code": "P",
                "filing_date": d.isoformat(),
                "accepted_at": datetime.combine(d, t).isoformat(sep=" "),
                "boundary_case": boundary_case,
            }
        )

    for n in range(30):  # random times from 6 a.m. to 9:59 p.m.
        d = rng.choice(days[20:-3])
        t = time(rng.randint(6, 21), rng.randint(0, 59), rng.randint(0, 59))
        add(f"EVT-{n:03d}", rng.choice(TICKERS), d, t)

    # PLANTED boundary cases: each must trade on the NEXT session, never the same day
    add("EVT-B1", "ALFA", days[40], time(18, 0, 0), "after_close_1800")
    add("EVT-B2", "CHRL", days[50], time(9, 30, 0), "at_open_0930")
    # PLANTED: accepted after the LAST session's open -> no later session exists
    add("EVT-U1", "BRVO", days[-1], time(16, 30, 0))
    add("EVT-U2", "ECHO", days[-1], time(19, 5, 0))

    manifest = {"seed": SEED, "n_events": len(events), "expected_unmatched": 2}
    return events, manifest
```

   In `main()`, after the bars: `events, manifest = make_events(rng, days)`, then write `insider_events.csv` and `gen_manifest.csv` (one row) the same way. Call it **after** `make_bars` so the same seed still gives the same bars. Run `uv run python scripts/gen_market_seed.py --out dbt/market_rehearsal/seeds`.
2. Staging: `stg_bars.sql`, `stg_insider_events.sql` (cast, rename, one row per grain), and `stg_session_opens.sql` (each session's 09:30 open as a timestamp). 📈 `stg_insider_events` keeps both clocks — `cast(filing_date as date)`, `cast(accepted_at as timestamp)` — and `nullif(boundary_case, '') as boundary_case`.
3. `marts/fct_rvol.sql` — relative volume = today's volume ÷ the average of the **previous** 20 sessions: `avg(volume) over (partition by ticker order by session_date rows between 20 preceding and 1 preceding)`. Including today in its own baseline is the classic leak.
4. `marts/fct_event_entries.sql` — each event joined to the first session it could legally trade:

```sql
-- DuckDB ASOF LEFT JOIN: for each filing, the nearest session open strictly AFTER
-- its acceptance time. LEFT keeps filings that have no later session (entry = NULL);
-- a plain ASOF JOIN is an INNER join and would drop them without a word.
select e.event_id, e.ticker, e.filing_date, e.accepted_at, e.boundary_case,
       o.session_date as entry_session, o.session_open_at
from {{ ref('stg_insider_events') }} e
asof left join {{ ref('stg_session_opens') }} o
  on e.ticker = o.ticker
 and e.accepted_at < o.session_open_at
```

> 📈 **v3.3 fix (C64):** v3.2 used `asof join` on one `filed_at`. DuckDB's plain `ASOF JOIN` is an inner join, so a filing accepted after the last session's open simply disappeared — and a test cannot catch a row that is no longer there. The two `EVT-U` filings exist to prove the fix.
> **Tests (30 min · 📈 +10 in v3.3):**

- `schema.yml`: `unique` + `not_null` on each model's grain key; `accepted_values` on `txn_code`.
- `tests/assert_no_lookahead.sql` — a **singular test** that returns any entry whose session opened at or before its `filed_at` 📈 `accepted_at`. Zero rows = pass.
- 📈 `tests/assert_unmatched_equals_manifest.sql` — the generator knows how many filings have no later session; dbt must agree:

```sql
with unmatched as (
    select count(*) as n from {{ ref('fct_event_entries') }} where entry_session is null
)
select u.n as unmatched, m.expected_unmatched
from unmatched u
cross join {{ ref('gen_manifest') }} m
where u.n <> m.expected_unmatched
```

- 📈 `tests/assert_boundary_events_trade_next_session.sql` — test 4: the 18:00 acceptance and the one at exactly 09:30:00 must both trade on a **later** session:

```sql
select event_id, boundary_case, filing_date, accepted_at, entry_session
from {{ ref('fct_event_entries') }}
where boundary_case is not null
  and (entry_session is null or entry_session <= filing_date)
```

`uv run dbt build --project-dir dbt/market_rehearsal --profiles-dir dbt/market_rehearsal` → green. Then break it on purpose (`<` → `<=` in the join, or drop `1 preceding` from the window), watch a test fail, revert. 📈 Two more breaks: `asof left join` → `asof join` (the manifest test fails — two filings vanished), and `e.accepted_at < o.session_open_at` → `e.filing_date <= o.session_date` (the boundary and look-ahead tests fail — the 18:00 filing "trades" at that morning's open). **Know both colors.**

> ⚠️ If `dbt-duckdb` won't resolve on 3.14 the day you run this, don't downgrade the repo's floor: log it in the journal, pin the newest dbt-duckdb that resolves, and record the outcome as an ADR — the same falsifier discipline as C28.



### 📌 DAY 42 — Sunday, August 30 (2h)

Week summary + ⚖️ **priority check (C58)**: fortnight AE/DE vs Applied-AI hours from the journal · draft + publish post #6 — 🆕 artifact: the rehearsal's lineage graph (`dbt docs generate`): *"I wrote a test that fails if my data can see the future"* (or the original plan-doc-summarizer angle — pick the one with the stronger artifact) · ~~AI Prompting videos done~~ → **dbt Fundamentals certificate →** `evidence.md` · 10 min Job lane: tracker update · plan Weeks 7–8 · journal 🎉

---



## 📊 2-WEEK SUCCESS METRICS

- [ ] Claude API course ~35% (sections logged)
- [ ] 5+ SDK scripts · streaming · errors
- [ ] pydantic + pydantic-settings in use
- [ ] SecretStr masking proven
- [ ] 8+ mocked tests, zero live-API tests
- [ ] Mini-project #3 shipped
- [ ] ✅ all repos on 3.14 since setup
- [ ] 🆕 Market-data rehearsal: dbt build green · lookahead singular test fails when broken
- [ ] 📈 Rehearsal v3.3: two clocks · `asof left join` · manifest + boundary tests green, each seen failing
- [ ] 📈 Twins #6–#7: bar windows + generator · volume dry-up islands (or queued)

- [ ] Dockerfile builds; --frozen idiom used
- [ ] ADRs 0002–0003 written (yours)
- [ ] Mode SQL Advanced complete
- [ ] 🆕 dbt Fundamentals done (certificate)
- [ ] ~~AI-901 exam BOOKED~~ (Q2) → 🆕 grain declared in `modeling-notes.md` (Kimball Ch. 3–4)
- [ ] Posts #5–6 · 24+ commits · rules file at Phase 3 · Tab re-enabled
- [ ] pre-commit on recon-toy
- [ ] 🆕 Job lane: targets 20 · résumé v0 skeleton

**Passing bar: 80%.** Non-negotiables: mini-project #3 (the SDK-fluency proof), ~~the booked AI-901 exam~~ → 🆕 **the grain declaration** (v3.1), and 🆕 **dbt Fundamentals complete** — DataVault's dbt project opens on Day 43 on top of it.

---



## 🔭 WHAT COMES NEXT

**Weeks 7–8 (Aug 31 – Sep 13): the flagship era opens.** DataVault S1 v0 gets its own production-scaffolded repo — synthetic Matrix/Relius-shaped generators, a pydantic canonical model, recon engine, Box-7 rules skeleton — plus your first **CI pipeline** (GitHub Actions running ruff + pytest as a blocking gate). Claude API course reaches tool use + prompt caching. CS50P starts. ~~And Week 8 ends with the AI-901 exam~~ → ⏭️ **v3.1: the exam moves to Q2**; Week 8 builds DataVault's **Kimball star** instead (fact + four conformed dimensions).

> 🆕 **v3.0: DataVault opens dbt-first.** Python generates, ingests and validates rows (pydantic contract + quarantine, Polars → Parquet); **reconciliation and Box-7 checks are dbt models with tests**, not a Python engine (C35 §2 made literal). The rehearsal you just built is its template, and Weeks 7–8 build most of the soft trigger — ⚖️ due **Day 63** in v3.1 (Day 70 fallback).

---

*Aligned to Career Roadmap v10.0 (Corrections 1–64) · v3.0 job-first re-cut (6 Oct 2026) · v3.1 priority rebalance (C58, 8 Oct 2026) · v3.2 readiness gate (C59, 9 Oct 2026) · v3.3 trading lane expansion (C63–C64, 13 Oct 2026). No other roadmap edits made; propose→approve governance applies.*
