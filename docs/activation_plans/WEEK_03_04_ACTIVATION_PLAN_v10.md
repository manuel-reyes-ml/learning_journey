# 🚀 WEEKS 3–4 MASTER ACTIVATION PLAN (v10.0)
## Internal AI Builder Track | August 3–16, 2026

**Document Version:** 2.2 (realigned to roadmap Corrections 13–20: DL.AI Pro-tier ruling, ADR learning pack + Nygard template, structlog first touch, RPF written-determination ask)
**Covers:** Monday, August 3 – Sunday, August 16, 2026 (Stage 1 · Month 1 → 2 · Weeks 3–4)
**Aligned To:** Career Roadmap v10.0, Corrections 1–20
**Prerequisite:** Weeks 1–2 metrics ≥80% (below that: close gaps in this fortnight's flex slots first)
**Weekly Hours:** 25 (same block schedule)

> **Same rule as Weeks 1–2:** TYPE every example, read every comment, run it, break it, fix it. Every line understood before it's committed.

---

## 📋 TABLE OF CONTENTS
1. [Where You Stand](#-where-you-stand-after-week-2)
2. [Strategic Context](#-strategic-context)
3. [WEEK 3: Data Structures + SQL Joins + AI Python (Aug 3–9)](#-week-3-aug-39)
4. [WEEK 4: Dictionaries, Docker + AI-901 Kickoff (Aug 10–16)](#-week-4-aug-1016)
5. [2-Week Success Metrics](#-2-week-success-metrics)
6. [What Comes Next](#-what-comes-next)

---

## 📊 WHERE YOU STAND AFTER WEEK 2

You have: a 2026-standard environment (uv + Cursor/OpenCode + VS Code + ruff + pytest), P4E Course 1 done, CS50x Weeks 0–3 in motion, Mode SQL basics, a typed + tested `retirement.py` module, mini-project #1 shipped, 2 public posts, and a two-week commit streak. The engine works. This fortnight adds the payload.

## 🧠 STRATEGIC CONTEXT

### Three threads converge

1. **Data structures (P4E Course 2)** — lists, dictionaries, tuples: 80% of working Python for data. Every DataVault concept later (canonical models, reconciliation keys) is "dictionaries with discipline."
2. **SQL becomes real (Mode Intermediate)** — JOINs and aggregation, the ~79%-of-DE-postings skill, practiced against **your own SQLite database**, not just tutorial tables.
3. **The AI bridge opens** — *AI Python for Beginners* (Andrew Ng) teaches Python in the context of prompting/API calls → on-ramp to *Building with the Claude API* in Weeks 5–6. ⚠️ **Correction 17 changes how you take it:** the DeepLearning.AI free tier is now videos-only (labs, quizzes, and the Accomplishment are Pro-gated). The ruling: **watch free, replicate every exercise yourself in your own Jupyter notebook** — which is better practice than the hosted lab anyway (no vibe coding, your scaffolding, your repo) — and defer the lab month + Accomplishment to the Sprint-1 Pro rental later this quarter (timed to the PolicyPulse eval-harness build; possibly $0 via the optional AMD free month). Do not subscribe to Pro now.

### 🤖 Agent policy — Phase 2 unlocks this fortnight

Per the Weeks 1–2 Agent Policy, you now graduate from tutor-mode-only to **boilerplate under review**: Cursor Agent (or OpenCode) may draft mechanical scaffolding *when you explicitly ask* — CSV-writer blocks, the argparse skeleton on Day 27 — but never the core logic. The matching rules, the SQL, the tolerance policy, every test, and ADR 0001 are typed by you: they encode YOUR understanding of the business, which is the entire portfolio thesis.

**The discipline when an agent drafts something:** read the diff line-by-line in Cursor's review pane → ask it to explain any line you can't explain yourself → pass the explain-back test → accept or reject per line. Update `.cursor/rules/learning-phase.mdc` on Day 22 to reflect Phase 2 (change is one line: the Weeks 3–4 exception is now active — a nice first rules-file edit). One good weekly rep: after finishing a script yourself, ask the Agent to *review* it against your production standard (type hints? docstrings? boundary validation?) and judge whether its critiques are right — reviewing the reviewer is the skill FDE work runs on. Cursor Tab may come back ON from Week 5, not yet.

### AI-901 kickoff = the elevation engine starts

Week 4 opens **Azure AI Fundamentals (AI-901)** study — employer-reimbursed cert #1. Per the roadmap, every cert doubles as evidence for the Month-6 scope-change conversation with Jen. **Action this fortnight: submit the reimbursement pre-approval** through the Financial Industry Professional Education Program — the paper trail starts now.

### New concepts
```
Python: string parsing, file I/O, lists, dictionaries, tuples, random with seeds
SQL:    INNER/LEFT JOIN, GROUP BY, aggregates, HAVING — via sqlite3
Tools:  SQLite, Docker basics, structlog first taste (Correction 16's named
        logging standard)
AI:     prompting an LLM from Python (Ng course — free-tier videos, exercises
        replicated locally per Correction 17)
Docs:   your first ADR, written from the roadmap's ADR learning pack
        (Correction 14 — Core Course #17, ADR half; Nygard template)
Certs:  AI-901 exam structure + Microsoft Learn path · RPF written-determination
        ask (Correction 15 open item)
```

---

## 🗓 WEEK 3 (Aug 3–9)

### Week 3 goals
```
□ P4E Ch.6–8 (strings, files, lists) complete   □ Mode SQL joins→GROUP BY done
□ AI Python videos: Modules 1–2 (free tier;     □ Synthetic 2-system dataset built
  exercises replicated in own notebook)
□ Dataset loaded into SQLite + recon queries    □ CS50x Week 4 lecture
□ LinkedIn post #3 · meetup RSVP for the month
```

---

### 📌 DAY 15 — Monday, August 3

**Morning:** P4E Ch.6 (strings) wrap-up + assignments.

**Evening:**
- [ ] 60 min — String parsing on messy finance text — the daily reality of data work. Create `src/learning_journey/day15_parsing.py`:

```python
"""Day 15: parsing messy financial text with string methods.

Real systems export ugly text. Before regex (later), master the manual
tools: .split(), .strip(), .replace(), slicing. Feeling this pain is the
point — regex will then be a relief you understand, not an incantation.
"""

# Simulated export lines from a legacy system (note inconsistent spacing —
# that's realism, not sloppiness):
raw_lines = [
    "ACCT-10023 | GROSS: $12,450.00 | CODE: 7",
    "ACCT-10087 | GROSS: $3,200.50  | CODE: 1",
    "ACCT-10112 | GROSS: $45,000.00 | CODE: G",
]

for line in raw_lines:
    # STEP 1 — split the line into parts on the delimiter:
    parts = line.split("|")            # → ["ACCT-10023 ", " GROSS: $12,450.00 ", " CODE: 7"]

    # STEP 2 — clean each part. Chaining methods reads left→right:
    account = parts[0].strip()                         # kill stray spaces
    # [0] is INDEXING: Python counts from 0. parts[0] = first item.

    # STEP 3 — the amount needs surgery:
    gross_text = parts[1].strip()                      # "GROSS: $12,450.00"
    gross_text = gross_text.removeprefix("GROSS:")     # " $12,450.00"
    gross_text = gross_text.strip().removeprefix("$")  # "12,450.00"
    gross_text = gross_text.replace(",", "")           # "12450.00" — commas break float()
    gross = float(gross_text)                          # NOW it converts

    code = parts[2].split(":")[1].strip()              # split "CODE: 7" on ":", take part 1

    print(f"{account}: ${gross:>10,.2f}  code={code}")

# Exercise (do it now): add a malformed line like "ACCT-9 | GROSS: N/A | CODE:"
# and make the loop survive it with try/except, printing a clear warning.
# Data that can't be parsed must be REPORTED, never silently dropped —
# in a 1099 pipeline, a silently dropped row is a participant who doesn't
# get a form. Boundary rule, always.
```
- [ ] 40 min — Mode SQL: INNER JOIN section (transcribe to `sql/02_joins.sql` with your own comments)
- [ ] 20 min — Journal + commit (`feat: messy-text parser with boundary handling`)

---

### 📌 DAY 16 — Tuesday, August 4

**Morning:** Mode SQL: LEFT/RIGHT JOIN + join logic.

**Evening:**
- [ ] 60 min — **Build the synthetic two-system dataset** ⭐ — the DataVault reconciliation pattern in miniature. Create `src/learning_journey/projects/make_data.py`:

```python
"""Generate synthetic data simulating TWO systems that should agree — but don't.

This mirrors the real DataVault S1 problem (Matrix vs Relius): two systems
about the same participants, with discrepancies hiding between them.
Public-repo governance: 100% synthetic, invented names, fake IDs. Always.
"""

import csv
import random
from pathlib import Path

# --- SEEDING: the reproducibility habit ---
# random normally differs every run. seed(42) makes the "random" sequence
# IDENTICAL every run → teammates (and tests!) see exactly your data.
# Reproducibility is a pillar of production data work; it starts here.
random.seed(42)

OUT_DIR = Path(__file__).parent / "data"

FIRST = ["Ana", "Luis", "Mia", "Omar", "Sara", "Ken", "Rita", "Jon", "Eva", "Max"]
LAST = ["Torres", "Vega", "Chen", "Ali", "Kim", "Ruiz", "Cole", "Diaz", "Wu", "Ford"]
BOX7_CODES = ["1", "2", "4", "7", "G"]


def make_participants(n: int) -> list[dict]:
    """System A: the recordkeeper's participant file."""
    rows = []
    for i in range(n):
        rows.append({
            "participant_id": f"P{1000 + i}",
            "name": f"{random.choice(FIRST)} {random.choice(LAST)}",
            "salary": round(random.uniform(40_000, 180_000), 2),
            "deferral_pct": round(random.uniform(0.03, 0.15), 3),
        })
    return rows


def make_distributions(participants: list[dict]) -> list[dict]:
    """System B: the payer's distribution file — WITH planted defects.

    We inject known discrepancies ON PURPOSE, so we can verify our recon
    logic finds exactly them. This is the golden-dataset idea: you can't
    trust a checker you haven't checked. (Your future eval gates — RAGAS
    thresholds on PolicyPulse — are this same principle aimed at LLMs.)
    """
    rows = []
    for p in participants:
        if random.random() < 0.15:
            continue                     # DEFECT 1: ~15% missing from System B

        gross = round(random.uniform(1_000, 50_000), 2)
        if random.random() < 0.10:
            gross = round(gross + 0.10, 2)   # DEFECT 2: ~10% off-by-10-cents

        rows.append({
            "participant_id": p["participant_id"],
            "gross": gross,
            "box7_code": random.choice(BOX7_CODES),
            "dist_date": f"2026-{random.randint(1, 6):02d}-{random.randint(1, 28):02d}",
            # :02d pads to 2 digits → "2026-03-07" not "2026-3-7".
            # Consistent date formats: tiny habit, prevents entire bug species.
        })
    return rows


def write_csv(path: Path, rows: list[dict]) -> None:
    """-> None: this function performs an ACTION, returns nothing."""
    path.parent.mkdir(parents=True, exist_ok=True)   # ensure folder exists
    with path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


if __name__ == "__main__":
    participants = make_participants(50)
    distributions = make_distributions(participants)
    write_csv(OUT_DIR / "system_a_participants.csv", participants)
    write_csv(OUT_DIR / "system_b_distributions.csv", distributions)
    print(f"System A: {len(participants)} participants")
    print(f"System B: {len(distributions)} distributions")
    print(f"Planted gap: {len(participants) - len(distributions)} missing rows to find")
```
Run it twice: `uv run python -m learning_journey.projects.make_data` — identical output both times. **That's the seed working.** Change 42 → 7, run, observe different data; change back to 42.
- [ ] 40 min — AI Python for Beginners: Module 1 videos (free tier). ⚠️ Per Correction 17 the hosted labs are Pro-gated — so as you watch, **retype each exercise into your own notebook** `notebooks/ai-python-exercises.ipynb` and run it there. Your replication IS the lab; the Accomplishment waits for the Sprint-1 Pro month.
- [ ] 20 min — Journal + commit (`feat: seeded synthetic two-system generator with planted defects`)

---

### 📌 DAY 17 — Wednesday, August 5

**Morning:** P4E Ch.7 (files) videos + assignments.

**Evening:**
- [ ] 70 min — Load the CSVs into a real database. Create `src/learning_journey/projects/load_db.py`:

```python
"""Load the synthetic CSVs into SQLite.

SQLite = a full SQL database in a single file, built into Python (import
sqlite3 — nothing to install). Perfect for learning; also genuinely used
in production for embedded cases. Your Mode tutorial SQL now runs against
data YOU made.
"""

import csv
import sqlite3
from pathlib import Path

DATA_DIR = Path(__file__).parent / "data"
DB_PATH = DATA_DIR / "recon.db"


def load() -> None:
    conn = sqlite3.connect(DB_PATH)      # opens (or creates) the DB file

    # Schema = the table blueprint: column names + types.
    # SQL types here: TEXT (string), REAL (float).
    # PRIMARY KEY = unique identifier; the DB REFUSES duplicate ids.
    # The database enforcing rules itself (not trusting the app to behave)
    # is a core data-engineering idea — your first data contract.
    conn.execute("DROP TABLE IF EXISTS participants")     # clean slate on rerun
    conn.execute("DROP TABLE IF EXISTS distributions")
    conn.execute("""
        CREATE TABLE participants (
            participant_id TEXT PRIMARY KEY,
            name           TEXT NOT NULL,
            salary         REAL NOT NULL,
            deferral_pct   REAL NOT NULL
        )
    """)
    conn.execute("""
        CREATE TABLE distributions (
            participant_id TEXT NOT NULL,
            gross          REAL NOT NULL,
            box7_code      TEXT NOT NULL,
            dist_date      TEXT NOT NULL
        )
    """)

    for table, filename in [
        ("participants", "system_a_participants.csv"),
        ("distributions", "system_b_distributions.csv"),
    ]:
        with (DATA_DIR / filename).open() as f:
            rows = list(csv.DictReader(f))
        cols = list(rows[0].keys())
        placeholders = ", ".join("?" for _ in cols)   # "?, ?, ?, ?"
        # The ?s are PARAMETERIZED values — sqlite fills them safely.
        # NEVER build SQL by pasting values into the string (f-strings here
        # = SQL injection, the classic security hole). ?s, always.
        conn.executemany(
            f"INSERT INTO {table} ({', '.join(cols)}) VALUES ({placeholders})",
            [tuple(r.values()) for r in rows],
        )

    conn.commit()          # commit = actually save the changes
    n_p = conn.execute("SELECT COUNT(*) FROM participants").fetchone()[0]
    n_d = conn.execute("SELECT COUNT(*) FROM distributions").fetchone()[0]
    print(f"Loaded {n_p} participants, {n_d} distributions → {DB_PATH.name}")
    conn.close()


if __name__ == "__main__":
    load()
```
Run it, then open `recon.db` with the SQLite Viewer extension (works identically in Cursor) and browse both tables — seeing your data in a real DB is a milestone.
- [ ] 30 min — Mode SQL: aggregation functions (COUNT/SUM/AVG/MIN/MAX)
- [ ] 20 min — Journal + commit (`feat: sqlite loader with schema + parameterized inserts`)

---

### 📌 DAY 18 — Thursday, August 6

**Morning:** CS50x Week 4 (memory) — notes on what Python hides from you.

**Evening:**
- [ ] 60 min — **First reconciliation queries** ⭐ — this is the job, in miniature. Create `sql/03_recon_v0.sql` and run each query via the SQLite viewer (or `sqlite3` CLI):

```sql
-- Recon v0: find the defects we planted on Day 16.
-- If these queries find EXACTLY the planted defects, the logic is proven.

-- Q1: Participants with NO distribution (the ~15% missing rows).
-- LEFT JOIN keeps every row from the LEFT table (participants) and fills
-- NULL where the right side has no match. Filtering WHERE right-side IS NULL
-- = "left rows with no partner" — THE find-the-missing-rows pattern.
-- You will write this shape a thousand times in your DE career.
SELECT p.participant_id, p.name
  FROM participants   AS p                 -- AS p = table alias (shorthand)
  LEFT JOIN distributions AS d
    ON p.participant_id = d.participant_id -- ON = the matching rule
 WHERE d.participant_id IS NULL;           -- NULL needs IS, not =

-- Q2: Distribution totals per Box-7 code (GROUP BY = collapse rows into
-- one summary row per group; aggregates like SUM/COUNT compute per group).
SELECT box7_code,
       COUNT(*)          AS n_distributions,
       SUM(gross)        AS total_gross,
       ROUND(AVG(gross), 2) AS avg_gross
  FROM distributions
 GROUP BY box7_code
 ORDER BY total_gross DESC;

-- Q3: Codes with unusually high totals — HAVING filters AFTER grouping
-- (WHERE filters rows BEFORE grouping; HAVING filters the groups).
SELECT box7_code, SUM(gross) AS total_gross
  FROM distributions
 GROUP BY box7_code
HAVING SUM(gross) > 100000;

-- Q4 (stretch): expected vs actual — join and compare per participant.
SELECT p.participant_id,
       p.name,
       ROUND(p.salary * p.deferral_pct, 2) AS expected_annual_deferral,
       d.gross                              AS actual_distribution
  FROM participants AS p
  JOIN distributions AS d USING (participant_id);
```
**Verify against ground truth:** does Q1's row count match Day 16's "planted gap" printout? If yes — your recon logic is *proven*, not assumed. That verification loop is the whole discipline.
- [ ] 40 min — AI Python for Beginners: Module 2 videos + replicate exercises in your notebook
- [ ] 20 min — Journal + commit (`feat: recon queries v0 — missing rows + code aggregates`)

---

### 📌 DAY 19 — Friday, August 7

**Morning:** P4E Ch.8 (lists) videos + assignments.

**Evening:**
- [ ] 60 min — Make the recon **testable from Python**. Add `src/learning_journey/projects/recon.py`:

```python
"""Reconciliation queries, callable (and therefore testable) from Python."""

import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent / "data" / "recon.db"


def missing_in_b(conn: sqlite3.Connection) -> list[tuple[str, str]]:
    """Participants with no distribution row. Returns (id, name) tuples.

    A TUPLE is like a list but immutable (can't be changed after creation) —
    the natural shape for a fixed-size record like a query row.
    """
    query = """
        SELECT p.participant_id, p.name
          FROM participants p
          LEFT JOIN distributions d ON p.participant_id = d.participant_id
         WHERE d.participant_id IS NULL
    """
    return conn.execute(query).fetchall()


def totals_by_code(conn: sqlite3.Connection) -> list[tuple[str, int, float]]:
    """(box7_code, count, total_gross) per code, largest total first."""
    query = """
        SELECT box7_code, COUNT(*), ROUND(SUM(gross), 2)
          FROM distributions
         GROUP BY box7_code
         ORDER BY SUM(gross) DESC
    """
    return conn.execute(query).fetchall()


if __name__ == "__main__":
    conn = sqlite3.connect(DB_PATH)
    missing = missing_in_b(conn)
    print(f"⚠️  {len(missing)} participants missing from System B:")
    for pid, name in missing:            # tuple UNPACKING: two names, one tuple
        print(f"   {pid}  {name}")
    print("\nTotals by Box-7 code:")
    for code, n, total in totals_by_code(conn):
        print(f"   code {code}: {n:>3} rows   ${total:>12,.2f}")
    conn.close()
```
And `tests/test_recon.py`:
```python
"""Prove the recon finds EXACTLY the planted defects — the golden-dataset test."""

import sqlite3

from learning_journey.projects.load_db import load, DB_PATH
from learning_journey.projects.recon import missing_in_b, totals_by_code


def test_missing_count_matches_planted_gap():
    load()                                   # rebuild DB fresh → deterministic (seed 42)
    conn = sqlite3.connect(DB_PATH)
    n_participants = conn.execute("SELECT COUNT(*) FROM participants").fetchone()[0]
    n_distributions = conn.execute("SELECT COUNT(*) FROM distributions").fetchone()[0]
    planted_gap = n_participants - n_distributions
    assert len(missing_in_b(conn)) == planted_gap
    conn.close()


def test_every_code_total_positive():
    conn = sqlite3.connect(DB_PATH)
    for _code, n, total in totals_by_code(conn):
        # _code: leading underscore = "unpacked but deliberately unused"
        assert n > 0 and total > 0
    conn.close()
```
`uv run pytest -v` → green.
- [ ] 40 min — Mode SQL: GROUP BY + HAVING → finish Intermediate joins/aggregation
- [ ] 20 min — Journal + commit (`test: recon proven against planted defects`)

---

### 📌 DAY 20 — Saturday, August 8 (5.5h)

**Morning (5:00–8:30):**
- [ ] 120 min — **Mini-project #2: `recon-toy` v0.1** ⭐ — wire it into ONE pipeline. Create `src/learning_journey/projects/recon_toy.py`:

```python
"""recon-toy v0.1 — end-to-end pipeline: generate → load → reconcile → report.

One command, four stages — the shape of every data pipeline you will
ever build, including DataVault's real one:
    EXTRACT (make_data) → LOAD (load_db) → TRANSFORM/CHECK (recon) → REPORT
"""

import sqlite3
from pathlib import Path

from learning_journey.projects import load_db, make_data, recon

OUTPUT_DIR = Path(__file__).parent / "output"


def run_pipeline() -> Path:
    """Run all stages; write the exceptions report; return its path.

    Returning the path (instead of just printing) makes the pipeline
    TESTABLE — a test can open the file and check its contents.
    """
    print("[1/4] Generating synthetic data...")
    participants = make_data.make_participants(50)
    distributions = make_data.make_distributions(participants)
    make_data.write_csv(make_data.OUT_DIR / "system_a_participants.csv", participants)
    make_data.write_csv(make_data.OUT_DIR / "system_b_distributions.csv", distributions)

    print("[2/4] Loading SQLite...")
    load_db.load()

    print("[3/4] Reconciling...")
    conn = sqlite3.connect(load_db.DB_PATH)
    missing = recon.missing_in_b(conn)
    totals = recon.totals_by_code(conn)
    conn.close()

    print("[4/4] Writing report...")
    OUTPUT_DIR.mkdir(exist_ok=True)
    report_path = OUTPUT_DIR / "exceptions_report.txt"
    lines = [
        "RECONCILIATION EXCEPTIONS REPORT (synthetic data)",
        "=" * 50,
        f"Participants missing from System B: {len(missing)}",
        *(f"  {pid}  {name}" for pid, name in missing),
        # *( ... ) unpacks a generator into the list — a compact way to
        # splice many lines in. If it reads like magic today, write the
        # for-loop version instead; elegance is optional, clarity is not.
        "",
        "Totals by Box-7 code:",
        *(f"  code {c}: {n:>3} rows  ${t:>12,.2f}" for c, n, t in totals),
    ]
    report_path.write_text("\n".join(lines))
    print(f"✅ Report → {report_path}")
    return report_path


if __name__ == "__main__":
    run_pipeline()
```
Run: `uv run python -m learning_journey.projects.recon_toy` — then open the report file. **You just shipped your first pipeline.**
- [ ] 60 min — Tests to 12+ total passing (add: report file exists + contains the missing count); ruff clean
- [ ] 30 min — CS50x Week 4 pset start (timebox)

**Evening:**
- [ ] 60 min — AI Python for Beginners: continue videos + local replication
- [ ] 45 min — Draft post #3 (artifact: the exceptions report screenshot — "I taught Python to catch the mismatches I used to catch by eye")
- [ ] 15 min — Journal + commit (`feat: recon-toy v0.1 end-to-end pipeline`)

---

### 📌 DAY 21 — Sunday, August 9 (2h)
- [ ] 40 min — `weekly-summaries/week-03.md` + full test run
- [ ] 30 min — Publish post #3
- [ ] 30 min — Plan Week 4; check meetup calendar (Greenville Python ~2nd Tuesday → likely Aug 11 → RSVP)
- [ ] 20 min — Journal + commit 🎉

---

## 🗓 WEEK 4 (Aug 10–16)

### Week 4 goals
```
□ P4E Ch.9–10 → Course 2 DONE          □ AI Python videos COMPLETE + exercises
                                          replicated locally (Accomplishment
                                          deferred to Sprint-1 — Correction 17)
□ Docker for Beginners ~50%             □ AI-901 Learn path started (2 modules)
□ Reimbursement pre-approval submitted  □ recon-toy v0.2 dict matcher + ADR 0001
□ RPF written-determination question    □ ADR pack read (Core Course #17,
  sent (Correction 15 open item)          ADR half) · Nygard template chosen
□ Greenville Python meetup attended     □ structlog first touch in recon-toy
□ LinkedIn post #4
```

---

### 📌 DAY 22 — Monday, August 10

**Morning:** P4E Ch.9 (dictionaries) videos.

**Evening:**
- [ ] 60 min — Dictionary drills on your own data. Create `day22_dicts.py`:

```python
"""Day 22: dictionaries — THE data structure of data work.

A dict maps keys → values with instant lookup. Your mental model from
work: a dict is an indexed filing cabinet. participant_id → their record,
in one step, no searching. DataVault's canonical model will be exactly
'dicts with discipline.'
"""

import csv
from pathlib import Path

DATA = Path(__file__).parent / "projects" / "data"

with (DATA / "system_b_distributions.csv").open() as f:
    distributions = list(csv.DictReader(f))

# --- Pattern 1: COUNT per key (top-3 most useful loop in data work) ---
count_by_code: dict[str, int] = {}
for row in distributions:
    code = row["box7_code"]
    # .get(key, default) reads a key OR returns the default if absent —
    # this line means "current count, or 0 if first sighting, plus one":
    count_by_code[code] = count_by_code.get(code, 0) + 1
print("Distributions per code:", count_by_code)

# --- Pattern 2: SUM per key (same shape, different aggregate) ---
total_by_participant: dict[str, float] = {}
for row in distributions:
    pid = row["participant_id"]
    total_by_participant[pid] = total_by_participant.get(pid, 0.0) + float(row["gross"])

# --- Pattern 3: INDEX for instant lookup (the join, in Python form) ---
with (DATA / "system_a_participants.csv").open() as f:
    participants = list(csv.DictReader(f))
by_id = {p["participant_id"]: p for p in participants}
# ^ a DICT COMPREHENSION: builds {id: row} in one line.
# Looking up by_id["P1007"] is instant — no scanning. This index IS what
# a SQL JOIN does under the hood. Yesterday SQL; today you see the gears.

sample_id = distributions[0]["participant_id"]
print(f"{sample_id} belongs to {by_id[sample_id]['name']}, "
      f"total distributed ${total_by_participant[sample_id]:,.2f}")
```
- [ ] 40 min — **AI-901 + RPF admin** ⭐: open the official Microsoft Learn AI-901 path; skim the exam outline (know the map before studying); then draft + send ONE email to the Financial Industry Professional Education Program administrator covering two things: (1) **AI-901 reimbursement pre-approval** per the program process, and (2) **the RPF written-determination question** (Correction 15's open item): the program schedule lists "RPF-1, RPF-2" — the superseded two-exam structure — while ASPPA's current course is a single six-module certificate, so ask in writing how the bonus maps onto the current structure *before* any enrollment. You are NOT enrolling in RPF now (it's a later, ~30–50 h item); you're just closing the open item while the pre-approval channel is open anyway. **BCC yourself — this email is elevation-file evidence.**
- [ ] 20 min — Journal + commit (`feat: dict aggregation + index patterns`)

---

### 📌 DAY 23 — Tuesday, August 11

**Morning:** P4E Ch.9 assignments.

**Evening:** 🎪 **Greenville Python Meetup** (if tonight — confirm via HackGreenville directory). Arrive early; the casual first 30 min is where referral relationships form. Intro line: "career-changer building AI-focused data engineering skills — 15 years in financial ops." *If no meetup:* AI Python for Beginners modules + 30 min AI-901 Learn path.
- [ ] 15 min — Journal (note 2 names you met) + commit

---

### 📌 DAY 24 — Wednesday, August 12

**Morning:** AI-901 Learn: Module 1 (AI workloads overview) — notes in `notebooks/ai901-notes.md`.

**Evening:**
- [ ] 70 min — **recon-toy v0.2: a dict-based matcher** — same business question as the SQL, answered in Python, so you can compare the two approaches honestly. Add `src/learning_journey/projects/matcher.py`:

```python
"""Dict-based record matcher — the Python counterpart to the recon SQL.

Why build BOTH? (1) Each is the right tool in different situations —
SQL where data lives in a DB; Python where logic gets complex (fuzzy
matching, tolerances, multi-step rules). (2) Comparing their outputs
tests both: two independent implementations that agree are strong
evidence both are right. That's a verification technique you'll reuse
on real financial pipelines — and it becomes ADR 0001 on Friday.
"""

from dataclasses import dataclass, field


@dataclass
class MatchResult:
    """A small typed container for the three outcome buckets.

    @dataclass auto-writes the boilerplate (__init__ etc.) for a class
    that just holds data. First touch of classes — gentle on purpose;
    OOP proper arrives with CS50P.
    """
    matched: list[dict] = field(default_factory=list)
    missing_in_b: list[dict] = field(default_factory=list)
    amount_mismatch: list[dict] = field(default_factory=list)


def match_records(
    participants: list[dict],
    distributions: list[dict],
    amount_tolerance: float = 0.01,
) -> MatchResult:
    """Bucket every participant: matched / missing-in-B / amount-mismatch.

    `amount_tolerance` (default 1 cent) exists because floats and rounding
    make exact equality on money fragile — a tolerance is honest about
    that. In real reconciliation, tolerance thresholds are POLICY (a
    business decision, documented), not convenience. Note it as a
    consequence in Friday's ADR.
    """
    result = MatchResult()

    # Index B by participant_id — one pass, then instant lookups:
    dist_by_id: dict[str, dict] = {d["participant_id"]: d for d in distributions}

    for p in participants:
        pid = p["participant_id"]
        if pid not in dist_by_id:                 # `in` on a dict checks KEYS, fast
            result.missing_in_b.append(p)
            continue

        dist = dist_by_id[pid]
        expected = round(float(p["salary"]) * float(p["deferral_pct"]), 2)
        actual = float(dist["gross"])

        if abs(actual - expected) <= amount_tolerance:
            # abs() = distance regardless of sign — the tolerance test.
            result.matched.append(p)
        else:
            result.amount_mismatch.append({
                "participant_id": pid,
                "expected": expected,
                "actual": actual,
                "difference": round(actual - expected, 2),
            })

    return result
```
Then a cross-check test in `tests/test_matcher.py`:
```python
import csv
import sqlite3

from learning_journey.projects.load_db import load, DB_PATH
from learning_journey.projects.make_data import OUT_DIR
from learning_journey.projects.matcher import match_records
from learning_journey.projects.recon import missing_in_b


def _read(name):
    with (OUT_DIR / name).open() as f:
        return list(csv.DictReader(f))


def test_python_and_sql_agree_on_missing():
    """Two independent implementations, one answer — or a bug exists."""
    load()
    result = match_records(_read("system_a_participants.csv"),
                           _read("system_b_distributions.csv"))
    conn = sqlite3.connect(DB_PATH)
    assert len(result.missing_in_b) == len(missing_in_b(conn))
    conn.close()
```
- [ ] 30 min — AI Python for Beginners: continue videos + local replication
- [ ] 20 min — Journal + commit (`feat: dict matcher with tolerance + sql cross-check test`)

---

### 📌 DAY 25 — Thursday, August 13

**Morning:** Docker for Beginners (Coursera/KodeKloud): sections 1–2 with the in-browser labs.

**Evening:**
- [ ] 60 min — Docker hands-on locally (start Docker Desktop first):

```bash
docker run hello-world
# Watch what happened: Docker (1) looked for the image locally, (2) pulled
# it from Docker Hub, (3) created a CONTAINER from it, (4) ran it, printed,
# exited. Image = frozen recipe; container = a running instance of it.

docker run -it python:3.12-slim python
# -it = interactive terminal. You are now INSIDE a container, at a Python
# prompt, in a minimal Linux that has exactly Python 3.12 and nothing else.
# Try: import sys; print(sys.version)  → then exit() to leave.
# THE point: this identical Python runs on any machine on earth. "Works on
# my machine" stops being an excuse — that's why your README standard
# requires a Dockerfile in every flagship.

docker ps -a       # list containers (running and exited)
docker images      # list downloaded images
```
Write 5 lines in your journal, own words: image vs container, and why a hiring manager cares that your repos ship one.
- [ ] 40 min — P4E Ch.10 (tuples) videos + assignments
- [ ] 20 min — Journal + commit (`docs: docker first-run notes`)

---

### 📌 DAY 26 — Friday, August 14

**Morning:** AI-901 Learn: Module 2 (ML fundamentals concepts).

**Evening:**
- [ ] 75 min — **Your first ADR** ⭐ (Corrections 8 + 14: docs/adr/ on every project — the artifact hiring managers can interrogate; now with an official learning row).
  **Step 1 — read the pack (~30 min, the ADR half of Core Course #17):** skim adr.github.io (template comparison), read Michael Nygard's original ADR article, and skim the intro of AWS's Prescriptive Guidance ADR guide (the AWS idiom doubles as DEA-C01 pre-fluency later). The C4 half of Course #17 waits for the 1099-pipeline retro-migration pass — one pass, per Correction 14's rollout rule.
  **Step 2 — pick ONE template and record it:** the roadmap's rule is MADR or Nygard, one only ("take ONE, never stack" applies to templates too). This plan uses **Nygard** — the simplest: Status / Context / Decision / Consequences — which is what the example below follows. Land 4–5 real records before ever considering a variant.
  **Step 3 — write it:** create `docs/adr/0001-dual-matcher-sql-and-python.md`:

```markdown
# ADR 0001: Keep both SQL and Python implementations of the matcher

**Status:** Accepted
**Date:** 2026-08-14

## Context
recon-toy needs to find missing and mismatched records between two
systems. I built a SQL version (LEFT JOIN / IS NULL, aggregates) and a
Python dict-based version (indexing + tolerance logic). Keeping both
costs maintenance; a learning repo could justify either alone.

## Decision
Keep both, permanently, with a test asserting they agree.

## Consequences
+ Cross-verification: two independent implementations agreeing is
  evidence of correctness — the golden-dataset principle extended.
+ Each demonstrates the tool where it wins: SQL for set operations in
  the DB; Python for policy logic (the cent-level tolerance).
− Two implementations to update when matching rules change; the
  agreement test is the guard against silent drift.
− The tolerance threshold (±$0.01) is policy encoded in code — in a
  real system this belongs in configuration, decided by the business.
  Flagged for the DataVault S1 design.
```
> **Why ADRs matter (the 30-second version):** code shows *what* you built; ADRs show *why you chose it and what it cost* — precisely what FDE decomposition interviews probe. Ten honest lines per decision, immutable, numbered, stored in `docs/adr/` in the same repo as the code (ThoughtWorks' ADOPT-ring guidance, per Correction 14). Superseded ADRs get marked, never deleted — the same additive discipline as your roadmap. No certificate exists for this practice anywhere; the artifact in the repo IS the signal.
- [ ] 25 min — Finish AI Python for Beginners videos → replicate the final exercises in `notebooks/ai-python-exercises.ipynb` → log the completion in your README's evidence list. Per the Correction 19 credential ladder this is **Tier 5 evidence** (skills/portfolio only, never a "Certifications" line) — and per Correction 17 the actual Accomplishment PDF arrives later, in the Sprint-1 Pro month, at zero extra study cost since progress persists on your account.
- [ ] 20 min — Journal + commit (`docs: adr 0001 dual-matcher decision`)

---

### 📌 DAY 27 — Saturday, August 15 (5.5h)

**Morning (5:00–8:30):**
- [ ] 150 min — **recon-toy v0.3 hardening** — CLI + report integration + two production-standard upgrades:

**Sanctioned agent rep (optional):** the argparse skeleton below is exactly the "mechanical boilerplate" Phase 2 allows. If you want the rep, ask Cursor Agent to draft it — then review the diff against the version printed here line-by-line, and make it match your standard. If you'd rather type it (also correct), do that. Either way, the `run_pipeline` refactor and its tests are yours alone.

```python
# Add argparse to recon_toy.py — the standard way scripts take options.
# Replace the __main__ block with:

import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="recon-toy: generate, load, reconcile, and report."
    )
    parser.add_argument(
        "--participants", type=int, default=50,
        help="number of synthetic participants to generate (default: 50)",
    )
    parser.add_argument(
        "--tolerance", type=float, default=0.01,
        help="amount tolerance in dollars for matching (default: 0.01)",
    )
    args = parser.parse_args()
    run_pipeline(n_participants=args.participants, tolerance=args.tolerance)
    # (Refactor run_pipeline to accept these two parameters — thread them
    # through to make_participants() and match_records(). ~15 lines of
    # changes; your tests tell you immediately if you broke anything.
    # THAT is why we wrote them.)
```
Try it:
```bash
uv run python -m learning_journey.projects.recon_toy --help          # free documentation!
uv run python -m learning_journey.projects.recon_toy --participants 200
```
Then two production-standard upgrades from the new roadmap corrections:

**(a) structlog first touch (~30 min — Correction 16's named logging standard).** Your pipeline currently narrates itself with `print("[1/4] ...")`. Production systems emit *structured events* instead — data a machine can filter and query, not prose. Swap them:
```bash
uv add structlog        # note: a runtime dependency, so no --dev this time
```
```python
# At the top of recon_toy.py:
import structlog

log = structlog.get_logger()
# get_logger() gives you a logger. With structlog, you log EVENTS with
# KEY-VALUE data, not sentences with numbers baked in:

# BEFORE (prose — a human can read it, a machine can't query it):
#   print(f"[3/4] Reconciling... found {len(missing)} missing")
# AFTER (an event + data — both human AND machine readable):
log.info("recon_complete", missing=len(missing), mismatched=len(mismatch), matched=len(matched))
# Output: 2026-08-15 ... [info] recon_complete matched=38 mismatched=4 missing=8
#
# Why this matters (Correction 16): when DataVault runs nightly in production,
# "show me every run where missing > 0" is a QUERY against structured logs —
# impossible against print() prose. The full standard (ProcessorFormatter so
# third-party library logs render through the same chain, plus a PII-redaction
# processor as the choke point) arrives with the 1099-pipeline retro-migration
# pass — today is just the mental model: events + key-values, never sentences.
```
Replace all four stage prints with `log.info` events, run the pipeline, look at the output.

**(b) README ordering practice (~15 min — Correction 18).** Rewrite recon-toy's README section with the roadmap's new flagship heading order: **① Production** (honest: "runs locally via one command, 15+ tests as blocking gates, structured logging" — no deployment claim, because none exists) then **③ Architecture** (the 4-stage pipeline, link to ADR 0001). **Deliberately omit ② Cost** — Correction 18's rule: never manufacture a Cost section where there's nothing to report. Practicing the frame honestly on a toy now means it's second nature when DataVault's README carries it for real.

Also: integrate the Day-24 matcher's mismatch bucket into the exceptions report; 15+ tests passing; ruff + format clean; commit `pyproject.toml` + `uv.lock` together (the structlog add changed both).
- [ ] 60 min — Docker for Beginners: sections 3–4 (Compose intro). Note for Weeks 5–6: when recon-toy gets its Dockerfile, it will use the roadmap's `uv sync --frozen` idiom (Correction 13) — install *exactly* what uv.lock records, byte-reproducible images. The lockfile you've been committing is what makes that possible.

**Evening:**
- [ ] 60 min — P4E Course 2 final wrap → **Course 2 complete** 🎉
- [ ] 45 min — Draft post #4 (pillar: the ADR habit — "I started writing down my decisions like an engineering team of one")
- [ ] 15 min — Journal + commit (`feat: recon-toy v0.3 — cli, mismatch report, hardened tests`)

---

### 📌 DAY 28 — Sunday, August 16 (2h)
- [ ] 40 min — `weekly-summaries/week-04.md` + **Month-1 retro**: hours actual vs planned, 4:30 AM energy (honest), what to change in Month 2
- [ ] 30 min — Publish post #4
- [ ] 30 min — Read the Weeks 5–6 plan (generated after your Month-1 retro — so it fits reality, not assumptions)
- [ ] 20 min — Journal + commit 🎉

---

## 📊 2-WEEK SUCCESS METRICS
```
□ P4E Course 2 complete                □ AI-901 started + reimbursement filed
□ AI Python videos done + replicated   □ recon-toy v0.3: pipeline + CLI + 15+ tests
□ Mode SQL joins/aggregation done      □ ADR 0001 written (Nygard) + ADR pack read
□ Docker ~50% + containers run local   □ SQL ↔ Python cross-check test green
□ CS50x Week 4 in progress             □ structlog events replace pipeline prints
□ 24+ commits · 11+ journal entries    □ RPF written-determination question sent
□ rules file updated to Phase 2        □ agent diffs reviewed line-by-line (0
                                          unexplained accepted lines)
□ recon-toy README uses ①Production/   □ 1 meetup attended (or none scheduled)
  ③Architecture order (Cost omitted)   □ Posts #3 and #4 published · no DL.AI
                                          Pro purchased
```
**Passing bar: 80%.** Non-negotiables: the recon-toy thread (feeds DataVault S1) and the AI-901 kickoff (feeds the elevation file).

---

## 🔭 WHAT COMES NEXT

**Weeks 5–6 (Aug 17–30):** *Building with the Claude API* (Anthropic Academy — free, first-party, official certificate: the Correction 19 ladder's noted Tier-5 anomaly with better provenance than its tier implies) — your first real SDK work, using the key from setup: messages, structured outputs, tool use; *AI Prompting for Everyone* (videos only suffice — the roadmap explicitly says don't spend a lab slot here); Mode SQL Advanced (window functions); Docker completed and **recon-toy gets its first Dockerfile using `uv sync --frozen`** (first full production-checklist pass); AI-901 study intensifies toward a Month-2/3 exam date; and the PolicyPulse S1 scoping session lands on the calendar. Further out: the **Sprint-1 DL.AI Pro month** (all nine S1+S2 lab rows batched, every notebook downloaded before the month ends, possibly $0 via the optional AMD free month) stays timed to the PolicyPulse eval-harness build around Weeks 9–12 — not before.

---
*Aligned to Career Roadmap v10.0 (Corrections 1–20). No roadmap edits made; propose→approve governance applies.*