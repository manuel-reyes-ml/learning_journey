# 🚀 WEEKS 1–2 MASTER ACTIVATION PLAN (v10.0)
## Internal AI Builder Track | Starting Monday, July 20, 2026

**Document Version:** 2.2 (realigned to roadmap Corrections 13–20: uv official + uv.lock, DL.AI Pro-tier ruling, ADR learning pack, credential ladder)
**Covers:** Monday, July 20 – Sunday, August 2, 2026 (Stage 1 · Month 1 · Weeks 1–2)
**Aligned To:** Career Roadmap v10.0, Corrections 1–20 — Stage 1: Internal AI Builder (Months 1–8)
**Weekly Hours:** 25 (Mon–Fri 4:30–6:00 AM + 8:00–10:00 PM · Sat 5:00–8:30 AM + 8:00–10:00 PM · Sun 7:30–9:30 PM)
**Your Level:** Beginning the tech build from scratch — 15+ years business ops, 2 years ERISA-regulated financial operations, 5+ years trading

> **How to use the code in this plan:** TYPE every example yourself — never copy/paste, and never let Cursor Tab or an agent complete it (Tab stays OFF these two weeks; the Agent Policy section below governs the rest). Typing is how syntax enters your fingers. Read the comments (lines starting with `#`) as you type; they carry the "why." Then run the file, break it on purpose, and fix it. When you're confused, that's what Cursor **Ask** mode is for: paste YOUR code, ask WHY — the agent explains, you type. That loop — type → run → break → ask → fix — is how programmers who can later *supervise agents* are made. This is the roadmap's "no vibe coding" rule: every line understood before it's committed.

---

## ⚠️ WHAT CHANGED FROM THE OLD (Nov 2025) PLANS — READ FIRST

The previous activation plans were aligned to Roadmap **v8.3** (GenAI Data Analyst path). v10.0 **archived that path**. These plans replace them completely:

| Old (v8.3 plans) | New (v10.0 plans) | Why |
|---|---|---|
| DataCamp daily exercises | ❌ Removed | Declined in Corrections 4 & 7 — redundant paid subscription, near-zero credential weight |
| HackerRank badge grinding | ❌ Removed | Correction 7: badges ≠ credentials; <16% of hiring managers rank certs top-3 |
| SQLZoo tutorials | ❌ Removed | Correction 7: redundant with Mode SQL Tutorial + daily project SQL |
| Kaggle | ❌ Removed | Correction 7: competition portfolios read as academic — antithesis of the real-deployed-system thesis |
| "Data Analyst" job tracker in Week 1 | ❌ Removed | v10.0: NO external analyst search, ever. Stage 1 exit = internal elevation |
| Editor unspecified agent policy | **Cursor (primary, with Cursor Agents) + OpenCode agents · VS Code secondary** | Your stated workflow: build with agents while understanding every script and line — governed by the graduated agent policy below, which operationalizes the roadmap's no-vibe-coding + diff-review-before-merge rules |
| pip + requirements.txt | **uv + pyproject.toml + committed uv.lock** | 🆕 Correction 13 makes uv the OFFICIAL default across every project (Stage 1 Core Course #15); uv.lock now sits in the non-negotiable production standard; requirements.txt banned everywhere |
| 37-month / 5-stage framing | **32-month / 3-stage** | v10.0 structural restructure |

Carried forward: the 25 hrs/week schedule, morning-theory/evening-practice split, GitHub-first habit, learning journal, inline code examples, and production-grade discipline from Day 1.

---

## 📋 TABLE OF CONTENTS

1. [Critical Context](#-critical-context)
2. [Pre-Day-1 Checklist](#-pre-day-1-setup-do-before-monday-july-20)
3. [Complete From-Scratch Setup (step-by-step, with explanations)](#-complete-setup-step-by-step)
4. [Weekly Schedule Template](#-weekly-schedule-template)
5. [WEEK 1: Environment + First Code (Jul 20–26)](#-week-1-environment--first-code-jul-2026)
6. [WEEK 2: Functions, Tests & Production Habits (Jul 27–Aug 2)](#-week-2-functions-tests--production-habits-jul-27--aug-2)
7. [2-Week Success Metrics](#-2-week-success-metrics)
8. [Troubleshooting](#-troubleshooting)
9. [What Comes Next](#-what-comes-next)

---

## 🧠 CRITICAL CONTEXT

### Why these 2 weeks matter

You're building three things at once:

1. **The environment** — the workspace for ~3,500 hours over 32 months, set up once with the 2026-standard toolchain (`uv`, `ruff`, Cursor + OpenCode agents, VS Code as fallback) so every project starts at the roadmap's production standard from its first commit.
2. **The habit engine** — morning theory + evening practice, journaled and committed daily.
3. **First skills** — Python + SQL from the v10.0 course canon only: CS50x, Python for Everybody (P4E), Mode SQL. No filler platforms.

### The v10.0 mindset

You are training an **Internal AI Builder → AI-Focused Data Engineer → Applied AI Engineer**, not a Data Analyst. Three rules from Day 1:

- **Evidence over credentials** — every study session ends with a commit; your GitHub is the resume.
- **Production-grade from the start** — even Week 1 practice code lives in a `pyproject.toml` + `src/` repo with ruff and Conventional Commits.
- **No vibe coding — with agents in the loop.** You build WITH Cursor Agents and OpenCode, but the roadmap's rule is absolute: every line understood before merge, diff reviewed file-by-file. In Weeks 1–4 that means a *graduated* agent policy (see the Agent Policy section below): agents explain and review while YOU type the foundations — because the fundamentals you're installing this month are exactly what lets you supervise agents credibly for the next 32 months.

### Your moat

15 years of finance operations + ERISA-regulated domain depth is the structural differentiator the roadmap's Thesis is built on. That's why every exercise below runs on retirement-plan data (vesting, deferrals, 1099-R codes) instead of generic tutorial data — you're compounding the moat while learning syntax.

### Flagships are the lighthouse, not the Week 1 task

PolicyPulse, DataVault, and Crucible S1 cores start once foundations exist (~Weeks 7+). This fortnight's only flagship touches: the habits, the environment, and (Week 2, ten minutes) the free Alpaca account that seeds Crucible later.

---

### 🤖 THE AGENT POLICY (Weeks 1–4) — how to use Cursor Agents & OpenCode without vibe coding

Your workflow is agent-driven, and that's the right long-term call — your roadmap's own harness pattern (`.cursor/rules/`, OpenCode agents) assumes it. But there's a hard truth about Month 1: **you cannot review what you cannot write.** The roadmap's no-vibe-coding rule ("every line understood before merge") is only enforceable by someone whose fingers know the syntax. So the policy ramps:

| Phase | You | Agents (Cursor Agent / OpenCode) |
|---|---|---|
| **Weeks 1–2 (foundations)** | TYPE every example and exercise yourself | **Tutor mode only**: explain concepts, explain YOUR code back to you, explain error messages, answer "why" questions. Never generate exercise solutions — if an agent writes your first for-loop, you didn't learn for-loops. |
| **Weeks 3–4 (first pipeline)** | Type all core logic (matching rules, SQL, tests) | Tutor mode + **boilerplate under review**: agents may draft mechanical scaffolding (a CSV-writer block, an argparse skeleton) — then you read the diff line-by-line, ask the agent to explain anything unclear, and only accept when you could have written it yourself. Reject anything you can't explain. |
| **Weeks 5+ (SDK era onward)** | Design, review, decide | Progressively more generation, always gated by file-by-file diff review — the roadmap's permanent standard. |

**Three standing rules, all four weeks:**
1. **The explain-back test:** before accepting ANY agent-written line, you must be able to explain it out loud without looking at the agent's explanation. If you can't, don't accept — ask, learn, then accept.
2. **Tests and ADRs are always yours.** An agent-written test proving agent-written code is circular. Your tests encode YOUR understanding of the business rules — that's non-negotiable (it's also the eval-first muscle).
3. **Daily reps stay manual.** The course exercises (P4E, CS50x, Mode SQL) are typed by hand, full stop. They're the gym; agents don't lift your weights.

You'll codify this policy as a `.cursor/rules` file in Step 4 below — your first taste of the rules-file pattern that governs all 14 of your future project scopes.

---

## ✅ PRE-DAY-1 SETUP (do before Monday, July 20)

Budget ~4–5 hours across July 18–19 (includes the ~2 h uv docs reading = Core Course #15). One-time work.

### Hardware check
```
□ Mac Mini M4 (16GB) — primary workstation, ready
□ MacBook Air M2 (8GB) — secondary/mobile
□ Stable internet, quiet workspace, desk cleared
□ Phone alarms: 4:15 AM Mon–Fri, 4:45 AM Sat
□ Family informed of the schedule (protect the blocks)
```

### Accounts (~40 min, one consistent email)
```
□ GitHub — manuel-reyes-ml (verify access; enable 2FA)
□ Coursera Plus — verify active (P4E, Docker/KodeKloud, IBM GenAI later)
□ edX — free account (CS50x + CS50P; free CS50 cert via cs50.harvard.edu)
□ DeepLearning.AI — FREE account only. ⚠️ Correction 17: the free tier is videos-only
  (labs/quizzes/certificates are Pro-gated since Oct 2025). Do NOT buy Pro now — the
  roadmap's ruling is Pro gets RENTED for one timeboxed lab-sprint month later
  (timed to the PolicyPulse eval-harness build, possibly $0 via the optional AMD
  free month). Never annual, never rolling.
□ Anthropic Academy — anthropic.com/learn (Claude API course, Weeks 5+)
□ Anthropic Console — console.anthropic.com (API key, created now, used Weeks 5+)
□ Mode Analytics — free (SQL tutorial, Week 2+)
□ LinkedIn — headline: "Plan Administrator | Building toward AI-Focused Data Engineering"
□ Meetup.com — free (Distribution layer)
□ HackGreenville Slack — hackgreenville.com → Join (~10 min)
```

**Deliberately NOT created:** DataCamp, HackerRank, SQLZoo, Kaggle, LeetCode, StrataScratch — all evaluated and declined/deferred in Roadmap v10.0 (Corrections 4 & 7).

---

## 🛠️ COMPLETE SETUP (step-by-step)

Do this Saturday/Sunday July 18–19. All commands go in **Terminal** (⌘+Space → type "Terminal" → Enter). The Terminal is just a text way of telling your Mac what to do — you'll live in it daily, so start now. Type everything yourself.

### Step 1 — Xcode Command Line Tools (~10 min)
**What/why:** Apple's developer basics — includes `git`, the version-control tool that records every change you make (and powers GitHub).
```bash
xcode-select --install
# A popup appears → click "Install" → wait. Then verify:
git --version        # "verify" = confirm it worked. Should print: git version 2.x
```
> **Concept — what a command is:** `git --version` means "run the program named git, with the option --version." Options start with `-` or `--`. If Terminal prints the version, the install worked. If it prints "command not found," the program isn't installed or the Terminal needs restarting.

### Step 2 — Homebrew (~5 min)
**What/why:** the app store for command-line tools on macOS. One installer command, then `brew install <thing>` forever after.
```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
# When finished it prints "Next steps" with 2 commands — run those too (they add brew to your PATH).
brew --version
```
> **Concept — PATH:** the list of folders your Mac searches when you type a command name. "Adding to PATH" = telling the Mac where a new tool lives.

### Step 3 — uv: the Python toolchain (~5 min install + ~2 h reading) ⭐ ROADMAP-OFFICIAL (Correction 13 · Stage 1 Core Course #15)
**What/why:** ONE tool that installs Python itself, creates isolated project environments, and manages dependencies via `pyproject.toml`. It replaces four older tools (pip, venv, pyenv, pip-tools). Correction 13 made uv the **official default across every project in your roadmap**, and added `uv.lock` to the non-negotiable production standard — so this isn't just the 2026 community default, it's *your* documented standard from Day 0. No `requirements.txt`, ever.
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
# Quit and reopen Terminal, then:
uv --version
uv python install 3.12      # downloads & installs Python 3.12
uv python list              # confirm 3.12 appears in the list
```
> **Concept — why "environments" matter:** two projects may need different library versions. uv gives each project its own private set (a "virtual environment" in `.venv/`), so projects never contaminate each other. You'll never think about this — `uv run` handles it — but you should know *why* it exists: reproducibility, the first production virtue.
>
> **Concept — the lockfile (`uv.lock`):** `pyproject.toml` says *what* you depend on ("pytest"); `uv.lock` records the *exact* version of everything, including dependencies-of-dependencies, that actually got installed. Committing it means anyone (including future-you, or a Docker build using the roadmap's `uv sync --frozen` idiom) reproduces your environment byte-for-byte. **`uv.lock` is always committed to git** — that's what makes the "reproducible build" claim real (Correction 13's exact point).
>
> 📖 **Core Course #15 (do this weekend, ~2 h total):** read Astral's official uv docs — the "Projects" guide especially — plus Al Sweigart's uv quickstart as the terse command reference. This is a formal course row in your roadmap's Stage 1 table (docs + one tutorial, no certificate — the vendor-official pattern). Log it complete in your README evidence list when done.

### Step 4 — Cursor (primary) + VS Code (secondary) + OpenCode (~30 min) ⭐ YOUR EDITOR + AGENT STACK

**4a. Cursor — your primary editor.** Cursor is a fork of VS Code with AI agents built in, so everything VS Code does (extensions, settings, keybindings) works identically — you're not learning two editors.
1. Download https://cursor.com → drag to Applications → open → sign in ($20/mo Pro when the free tier runs out; treat it as a committed tool cost).
2. ⌘+Shift+P → "Shell Command: Install 'cursor' command" (lets you type `cursor .` in Terminal).
3. Extensions (⌘+Shift+X — Cursor uses the same marketplace):
```
□ Python (Microsoft)        □ Pylance (Microsoft)     □ Jupyter (Microsoft)
□ Ruff (Astral Software)    □ GitLens                 □ Docker (Microsoft)
□ Even Better TOML          □ SQLite Viewer           □ Markdown All in One
```
4. Settings (⌘+,): "format on save" → ✅ enable; "default formatter" → **Ruff** for Python.
> **Why Ruff + format-on-save:** ruff is the 2026-standard linter/formatter (same maker as uv). Format-on-save means professionally formatted code every ⌘+S — a senior habit installed on Day 0 for free.
>
> **Know your three Cursor modes** (⌘+L opens the panel): **Ask** = chat about code without changing it (your Weeks 1–2 tutor mode); **Agent** = it edits files and runs commands (gated by the policy above — Weeks 3–4 boilerplate only, under diff review); **Tab** = inline autocomplete — **turn Tab OFF for Weeks 1–2** (Settings → Cursor Tab → disable): autocomplete finishing your for-loops defeats the typing reps. Re-enable it Week 5.

**4b. VS Code — secondary.** Install from https://code.visualstudio.com (same extensions auto-sync if you enable Settings Sync). It's your agent-free fallback: if you ever wonder "can I still do this without the agent?", open VS Code and find out. That check is a feature.

**4c. OpenCode — terminal agent harness.**
```bash
brew install anomaly/tap/opencode 2>/dev/null || npm install -g opencode-ai   # use the current install method from opencode.ai docs
opencode --version
```
OpenCode runs agents from the terminal — the harness your roadmap's project scopes standardize on (`.opencode/agents/`, `.opencode/commands/`). For Weeks 1–4 you only need it installed and authenticated (it can use your Anthropic key from Step 8); its real workload starts with the flagship era. If the install method differs from the above, follow opencode.ai's current docs — and note in your journal what changed (that's a build-in-public artifact).

**4d. Your first rules file — codify the agent policy.** In the learning-journey repo (after Step 7), create `.cursor/rules/learning-phase.mdc`:
```markdown
---
description: Learning-phase agent policy (Weeks 1-4, Roadmap v10.0 Stage 1)
alwaysApply: true
---

# Learning-Phase Rules — Manuel is in foundations training

- I am learning Python/SQL fundamentals. DO NOT write solutions to course
  exercises (P4E, CS50x, Mode SQL) or to scripts I am typing from my
  activation plan. Explain concepts, review MY code, explain errors.
- When I ask for help: explain WHY, show the smallest possible example on
  DIFFERENT data than my exercise, and let me write my own version.
- Weeks 3-4 exception: mechanical boilerplate (CSV writer blocks, argparse
  skeletons) may be drafted WHEN I EXPLICITLY ASK — small diffs, heavily
  commented, and quiz me on one line before we move on.
- Never write my tests or my ADRs. Ever.
- Production standard applies to all suggestions: type hints, docstrings,
  uv (never pip), no requirements.txt, Conventional Commits, no print()
  inside functions.
```
> **Why this matters beyond Week 4:** rules files are how your roadmap governs agents across all 14 project scopes (`.cursor/rules/*.mdc` + shared OpenCode rules). Writing this one teaches the pattern on Day 0 — and it makes the agent itself enforce your learning discipline, which is exactly what a production guardrail is.

### Step 5 — Git identity + GitHub CLI (~10 min)
```bash
git config --global user.name "Manuel Reyes"
git config --global user.email "YOUR_GITHUB_EMAIL"     # same email as your GitHub account
git config --global init.defaultBranch main

brew install gh          # GitHub's official command-line tool
gh auth login            # choose: GitHub.com → HTTPS → Login with a web browser
gh auth status           # should show: Logged in to github.com as manuel-reyes-ml
```
> **Concept — git vs GitHub:** git is the tool on YOUR machine that records snapshots ("commits") of your work. GitHub is the website where you publish those snapshots. Commit locally → push to GitHub.

### Step 6 — Docker Desktop (~15 min)
**What/why:** Docker packages a program with everything it needs so it runs identically anywhere — the shipping-container of software. Needed from Week 3 (course) and required in every flagship repo per your README standard. Install now so it's ready.
1. https://www.docker.com/products/docker-desktop → Mac (Apple Silicon) → install → open once → accept terms.
2. Verify, then quit Docker Desktop (it uses RAM; start it only when needed):
```bash
docker --version
```

### Step 7 — Workspace + first repo (~30 min)
```bash
mkdir -p ~/dev                       # mkdir = make directory; -p = create parents if needed; ~ = your home folder
cd ~/dev                             # cd = change directory ("go into this folder")
uv init learning-journey --python 3.12   # scaffolds a project: pyproject.toml, .python-version, README
cd learning-journey
mkdir -p src/learning_journey notebooks journal weekly-summaries sql tests
```
> **What `uv init` just gave you:** `pyproject.toml` (the single config file describing your project + dependencies — the modern standard) and `.python-version` (pins Python 3.12 for this project, so it behaves the same on any machine). The `src/` folder is where real code lives — the professional layout your roadmap standard requires, from literally your first repo.

Open it (`code .`), replace `README.md` contents:
```markdown
# Learning Journey — AI-Focused Data Engineering

Daily practice, notes, and weekly summaries from my structured career
transition (Roadmap v10.0 · Stage 1: Internal AI Builder).

- **Stack:** Python 3.12 · uv · ruff · Cursor (+ Agents) · OpenCode · VS Code · Jupyter
- **Standard:** pyproject.toml + src/ layout · Conventional Commits · no vibe coding
- **Cadence:** 25 hrs/week · started July 20, 2026
```
Add dev tools and make your first commit:
```bash
uv add --dev ruff pytest    # --dev = tools for developing, not part of the program itself
# ^ this also creates/updates uv.lock — the exact-versions record. It gets
#   committed along with pyproject.toml, every time, per Correction 13.
git add .                                    # stage everything (mark it "to be committed")
git commit -m "chore: scaffold learning-journey with uv + src layout"
gh repo create learning_journey --public --source=. --push
```
> **Concept — the commit message format:** `chore: ...` is a **Conventional Commit** — a `type: description` convention (`feat`, `fix`, `docs`, `test`, `refactor`, `chore`). Your roadmap standard requires it; machines can parse it and humans can scan it. You'll formalize this Week 2; use it loosely from Day 1.
>
> ✅ **Checkpoint:** repo visible at github.com/manuel-reyes-ml/learning_journey. **If the repo already exists** from the 2025 era: don't delete anything — move old content to `archive/2025-analyst-era/` untouched and build the new structure at root. *Flag to Claude before executing if unsure.*

### Step 8 — Anthropic API key (create now, use Weeks 5+) (~10 min)
1. console.anthropic.com → API Keys → Create Key → name `learning-macmini` → buy $5 credit (lasts months at Stage 1 usage).
2. Store the key in your **password manager**. NEVER in a repo file or notebook cell — leaked keys get abused within minutes.
3. Make it available to future programs via an environment variable:
```bash
echo 'export ANTHROPIC_API_KEY="PASTE_KEY_HERE"' >> ~/.zshrc
# >> appends a line to ~/.zshrc, the file that runs every time Terminal opens.
# An environment variable is a named value programs can read — keys live there, never in code.
```

### Step 9 — Journal template (~10 min)
Create `journal/TEMPLATE.md`:
```markdown
# Journal — YYYY-MM-DD (Day N)
**Blocks completed:** Morning ☐ · Evening ☐ · Hours: X.X
**Today I learned:** (3 bullets max)
**Today I built:** (link to commit/file)
**Stuck on / question for tomorrow:**
**One win:** 🎉
```
Every day ends by copying it to `journal/2026-07-XX.md`, filling it, committing it. The journal is your future interview story bank — "tell me about a time you were stuck" gets answered from here.

---

## 📅 WEEKLY SCHEDULE TEMPLATE

| Day | Morning | Evening | Hours | Focus |
|---|---|---|---|---|
| Mon–Fri | 4:30–6:00 AM | 8:00–10:00 PM | 3.5/day | AM: courses + notes · PM: hands-on + commit |
| Saturday | 5:00–8:30 AM | 8:00–10:00 PM | 5.5 | Deep work |
| Sunday | — | 7:30–9:30 PM | 2.0 | Review · LinkedIn post · plan |
| **Total** | | | **25** | Consistency > intensity |

Course-load note: CS50x and P4E overlap on basics **by design** (Correction 11 — move fast through overlap; the value is rigor + credential). Mornings alternate: CS50x M/W/F, P4E T/Th. If overloaded: **P4E is the priority thread**; CS50x can stretch.

---

## 🗓 WEEK 1: ENVIRONMENT + FIRST CODE (Jul 20–26)

### Week 1 goals
```
□ Setup 100% verified            □ CS50x Week 0 + Week 1 attempted
□ P4E Course 1 Ch.1–3 complete   □ 10+ commits · 5 journal entries
□ HackGreenville joined + intro  □ Both Greenville meetups joined
□ LinkedIn post #1 (Sunday)
```

---

### 📌 DAY 1 — Monday, July 20

**Morning (4:30–6:00):**
- [ ] 10 min — Verify: `uv --version`, `git --version`, open Cursor (check Tab autocomplete is OFF, rules file present)
- [ ] 45 min — CS50x Week 0 lecture (1.25x speed; notes in `notebooks/cs50x-notes.md`)
- [ ] 25 min — The Scratch problem (yes, really — it teaches **decomposition**, the exact skill FDE interviews test: breaking a big problem into small steps)
- [ ] 10 min — Journal + commit (`docs: day 1 journal + cs50x week 0 notes`)

**Evening (8:00–10:00):**
- [ ] 60 min — Your first real program. Create `src/learning_journey/day01_hello.py` and TYPE this:

```python
# Day 1: My first Python program
# Manuel Reyes — Learning Journey (Roadmap v10.0, Stage 1)
#
# Theme: a 401(k) contribution calculator — because every exercise in this
# journey runs on retirement-plan data. Domain + code = the moat.

# --- PRINT: making the program talk ---
# print() sends text to the screen. Text in quotes is called a "string".
print("Day 1 — Manuel's 401(k) contribution calculator")

# --- VARIABLES: named boxes that hold values ---
# A variable is created the moment you assign to it with =
# Naming rule (production habit #1): full descriptive words, lowercase_with_underscores.
# BAD:  s = 85000        (what is s?)
# GOOD:
annual_salary = 85_000        # Python lets you write 85_000 for readability — same as 85000
deferral_rate = 0.06          # 6% — rates are stored as decimals, not percents

# --- TYPES: every value has a kind ---
# 85_000 is an int (whole number). 0.06 is a float (decimal).
# "Day 1..." is a str (text). Python tracks this for you, but YOU should know it too.
print(type(annual_salary))    # <class 'int'>   — try it, then delete this line
print(type(deferral_rate))    # <class 'float'>

# --- CALCULATION ---
annual_contribution = annual_salary * deferral_rate

# --- F-STRINGS: putting values inside text ---
# f"..." lets you embed variables with {curly_braces}.
# :,.2f  is a format spec: thousands separator, 2 decimal places.
# This is THE way to print money in Python.
print(f"Salary: ${annual_salary:,.2f}")
print(f"Deferral rate: {deferral_rate:.1%}")          # .1% formats 0.06 as 6.0%
print(f"Annual contribution: ${annual_contribution:,.2f}")

# --- INPUT: making it interactive ---
# input() pauses and waits for the user to type. It ALWAYS returns a string,
# so we convert ("cast") it to float before doing math. This str→number
# conversion is the #1 beginner stumble — meet it on purpose today.
user_salary_text = input("\nEnter a salary to try: ")
user_salary = float(user_salary_text)
user_contribution = user_salary * deferral_rate
print(f"At {deferral_rate:.0%}, that salary contributes ${user_contribution:,.2f}/year")
```

Run it from the project root:
```bash
uv run python src/learning_journey/day01_hello.py
# "uv run" = run inside this project's private environment. Always run code this way.
```
Then **break it on purpose**: type `abc` when asked for a salary. Read the error (`ValueError`). Errors are information, not failure — Thursday you'll learn to handle this one gracefully.

- [ ] 30 min — P4E: enroll, watch Ch.1 videos
- [ ] 20 min — Read your roadmap's Stage 1 section start to finish (know your own map)
- [ ] 10 min — Journal + commit (`feat: day 1 contribution calculator`)

**Deliverable:** environment verified, first script running, first deliberate error read.

---

### 📌 DAY 2 — Tuesday, July 21

**Morning:** P4E Ch.2 (variables/expressions) videos; type every example from the lecture into `src/learning_journey/day02_variables.py` as you watch.

**Evening:**
- [ ] 60 min — P4E Ch.2 assignments, then extend the calculator. Create `day02_limits.py`:

```python
# Day 2: Contribution limits & catch-up — first taste of DECISIONS in code
# New concepts: constants, comparison operators, if-statements (preview), min()

# --- CONSTANTS: values that never change while the program runs ---
# Convention: ALL_CAPS names. Production habit #2: no "magic numbers" buried
# in calculations — name them at the top, once, where they're easy to verify.
IRS_DEFERRAL_LIMIT = 23_500       # TODO: verify current-year IRS 402(g) limit
CATCH_UP_LIMIT = 7_500            # TODO: verify current-year catch-up amount
CATCH_UP_AGE = 50
# Those TODOs are deliberate: honesty over guessing. In regulated finance,
# an unverified number labeled as fact is a compliance problem. Same rule
# as your roadmap: unverified figures get flagged, not stated.

annual_salary = 120_000
deferral_rate = 0.25              # aggressive saver — will they hit the cap?
age = 52

# --- COMPARISON OPERATORS produce True/False (a "bool" type) ---
is_catch_up_eligible = age >= CATCH_UP_AGE     # >= means "greater than or equal"
print(f"Age {age} → catch-up eligible: {is_catch_up_eligible}")

# --- IF/ELSE: the program chooses a path ---
# Indentation (4 spaces) is not decoration in Python — it defines which
# lines belong to which branch. Cursor/VS Code + Ruff keep this tidy for you.
if is_catch_up_eligible:
    effective_limit = IRS_DEFERRAL_LIMIT + CATCH_UP_LIMIT
else:
    effective_limit = IRS_DEFERRAL_LIMIT

requested = annual_salary * deferral_rate

# --- min(): built-in that returns the smaller value ---
# The actual contribution is the requested amount, CAPPED at the limit.
# One line of business rule — exactly what plan administration does daily.
actual = min(requested, effective_limit)

print(f"Requested deferral:  ${requested:,.2f}")
print(f"Effective limit:     ${effective_limit:,.2f}")
print(f"Actual contribution: ${actual:,.2f}")

if requested > effective_limit:
    excess = requested - effective_limit
    print(f"⚠️  Deferral request exceeds limit by ${excess:,.2f} — capped.")
```
Run it. Change `age` to 45 and run again — watch the limit change. That's the point: **code encodes business rules you already know.**
- [ ] 40 min — CS50x Week 1 lecture, first half
- [ ] 20 min — Journal + commit (`feat: deferral limit checker with catch-up rule`)

---

### 📌 DAY 3 — Wednesday, July 22

**Morning:** CS50x Week 1 second half + start the problem set (in C — the struggle is the point; note what C forces you to see about types that Python hides).

**Evening:**
- [ ] 70 min — CS50x Week 1 pset (finish or timebox)
- [ ] 40 min — Full if/elif/else. Create `day03_vesting.py`:

```python
# Day 3: Vesting schedule checker — multi-branch decisions
# New concepts: elif chains, comparison chaining, why branch ORDER matters

years_of_service = 4
schedule_type = "graded"     # "cliff" (3-yr) or "graded" (2–6 yr)

# --- ELIF: check conditions top to bottom, take the FIRST true branch ---
if schedule_type == "cliff":
    # == asks "equal?" (one = assigns, two == compares — classic beginner trap)
    if years_of_service >= 3:
        vested_pct = 1.0     # 100% — cliff means all-or-nothing at 3 years
    else:
        vested_pct = 0.0

elif schedule_type == "graded":
    # 6-year graded: 0% <2yrs, then 20% per year from year 2, 100% at 6.
    # ORDER MATTERS: we check the highest tier first, because the first
    # true condition wins. If we checked >= 2 first, a 6-year employee
    # would wrongly stop at 20%.
    if years_of_service >= 6:
        vested_pct = 1.0
    elif years_of_service >= 2:
        vested_pct = 0.20 * (years_of_service - 1)
    else:
        vested_pct = 0.0

else:
    # Defensive branch: if data is bad, SAY SO loudly instead of guessing.
    # Silent wrong answers are the cardinal sin of financial software.
    print(f"❌ Unknown schedule type: {schedule_type!r}")   # !r shows quotes → reveals typos
    vested_pct = None

if vested_pct is not None:
    print(f"{schedule_type} schedule, {years_of_service} yrs → {vested_pct:.0%} vested")
```
Test it against your real-world knowledge: does year 5 on graded print 80%? If your domain brain and the program disagree, one of them has a bug — find out which. **That instinct (verify code against domain truth) is your permanent edge.**
- [ ] 10 min — Journal + commit (`feat: vesting schedule checker`)

---

### 📌 DAY 4 — Thursday, July 23

**Morning:** P4E Ch.3 (conditional execution) videos + quiz.

**Evening:**
- [ ] 60 min — Error handling — fixing Day 1's crash. Create `day04_safe_input.py`:

```python
# Day 4: try/except — programs that survive bad input
# Monday, typing "abc" as a salary crashed the program with ValueError.
# Production code NEVER crashes on user input. It anticipates, catches, recovers.

# --- WHILE LOOP + TRY/EXCEPT: ask until we get a valid answer ---
while True:                            # loop forever... until `break` exits it
    salary_text = input("Enter annual salary (or q to quit): ")

    if salary_text.lower() == "q":     # .lower() → accepts q or Q
        print("Goodbye!")
        break                          # break = leave the loop immediately

    try:
        # The RISKY line goes inside try:
        salary = float(salary_text)
    except ValueError:
        # If float() fails, Python "raises" ValueError. Instead of crashing,
        # control jumps HERE. We explain, then the loop asks again.
        print(f"  '{salary_text}' is not a number — try again (e.g., 85000).")
        continue                       # continue = skip to the next loop round

    # Catching the error is not enough — VALIDATE the business rule too.
    # -50000 is a valid float and an invalid salary.
    if salary <= 0:
        print("  Salary must be positive.")
        continue

    print(f"  ✅ ${salary:,.2f} accepted.")
    break

# Rule of thumb you now own: try/except for things that can FAIL,
# if-checks for things that can be WRONG. Both, always, at every boundary
# where data enters a system. (DataVault will live and die by this rule.)
```
- [ ] 40 min — **Distribution setup** ⭐: HackGreenville Slack → join, one-line bio ("career-changer into AI-focused data engineering · Greenville"), hello in #introductions; Meetup → join *Greenville Data Science & Analytics* + *Greenville Python*; RSVP anything this month
- [ ] 20 min — Journal + commit (`feat: input validation loop with try/except`)

---

### 📌 DAY 5 — Friday, July 24

**Morning:** CS50x — finish anything open from Weeks 0–1; else start Week 2 lecture.

**Evening:**
- [ ] 60 min — Consolidation: everything so far in one program. Create `day05_box7.py`:

```python
# Day 5: 1099-R Box 7 sanity checker — Week 1 consolidation
# Uses: constants, input loop, try/except, if/elif, f-strings.
# (Box 7 = the distribution code on Form 1099-R. You explain these codes
# at work; today your program does.)

print("=" * 50)                      # strings can be multiplied — instant divider
print("1099-R BOX 7 SANITY CHECKER — v0.1")
print("=" * 50)

while True:
    code = input("\nEnter a Box 7 code (or q to quit): ").strip().upper()
    # .strip() removes accidental spaces; .upper() normalizes '7 ' → '7'.
    # Cleaning input BEFORE using it: boundary habit, every time.

    if code == "Q":
        break

    # elif chain today; next week a dictionary makes this elegant —
    # feeling the clunky version FIRST is how you'll appreciate the fix.
    if code == "1":
        meaning = "Early distribution, no known exception (under 59½)"
        watch = "10% early-withdrawal penalty likely applies"
    elif code == "2":
        meaning = "Early distribution, exception applies"
        watch = "Verify the exception is documented"
    elif code == "7":
        meaning = "Normal distribution"
        watch = "Confirm participant is 59½+"
    elif code == "G":
        meaning = "Direct rollover"
        watch = "Should be non-taxable — gross vs taxable amounts must differ"
    else:
        print(f"  ❓ Code {code!r} not in this checker yet — add it! (That's the exercise.)")
        continue

    print(f"  Code {code}: {meaning}")
    print(f"  ⚠️  Check: {watch}")
```
Your task after typing it: **add two more codes you know from work** (e.g., 4, H). Extending existing code is a distinct skill from writing new code — practice both.
- [ ] 40 min — Read your `REPO_STRUCTURE_TEMPLATE.md` + `ACCEPTANCE_CRITERIA.md`; list gaps vs v10.0 (uv? ADRs? C4?) in `journal/` — **don't edit them; flag the list for Claude review**
- [ ] 20 min — Journal + commit (`feat: box7 sanity checker v0.1`)

---

### 📌 DAY 6 — Saturday, July 25 (deep work, 5.5h)

**Morning (5:00–8:30):**
- [ ] 90 min — P4E Ch.1–3: all remaining assignments + quizzes (target 100%)
- [ ] 60 min — CS50x Week 2 lecture
- [ ] 60 min — **First Jupyter session:**
```bash
uv add --dev jupyter        # notebooks are a dev tool → --dev group
uv run jupyter lab          # opens in your browser; Ctrl+C in Terminal to stop
```
Create `notebooks/week01_playground.ipynb`. Redo 2–3 of the week's exercises interactively. Then write this in a Markdown cell — it's the professional dividing line most self-taught people never learn:
> **Notebooks are for exploring** (try things, see results instantly, keep notes beside code). **Scripts in `src/` are for keeping** (tested, linted, runnable by anyone). Explore in notebooks → graduate good code to `src/`. Never let a notebook be the only home of important logic.

**Evening (8:00–10:00):**
- [ ] 60 min — Repo polish: run the linter and fix everything it flags:
```bash
uv run ruff check .        # lists problems with rule codes (F401, E501...)
uv run ruff format .       # auto-formats every file
```
For each rule code you don't understand: look it up in the Ruff docs, understand it, then fix. **Never silence a rule you can't explain.** Add a one-line comment ("docstring") at the top of each script saying what it does. Update README with a Week 1 section.
- [ ] 45 min — Draft Sunday's LinkedIn post
- [ ] 15 min — Journal + commit (`chore: week 1 lint pass + readme update`)

---

### 📌 DAY 7 — Sunday, July 26 (2h)
- [ ] 40 min — Week review: run every script, re-read every note; write `weekly-summaries/week-01.md` (shipped / hours / hard parts / next focus)
- [ ] 30 min — **Publish LinkedIn post #1** (pillar: frontline building). Formula: what I set up → one thing that surprised me → one artifact (repo screenshot). Never "I'm looking for a job."
- [ ] 30 min — Plan Week 2; block calendar
- [ ] 20 min — Journal + commit 🎉

---

## 🗓 WEEK 2: FUNCTIONS, TESTS & PRODUCTION HABITS (Jul 27 – Aug 2)

### Week 2 goals
```
□ P4E Ch.4–5 → Course 1 DONE        □ Mode SQL Basic section complete
□ CS50x Week 2 done, Week 3 started  □ First pytest tests passing
□ Conventional Commits formalized    □ Alpaca account created (parked)
□ Mini-project #1 shipped            □ LinkedIn post #2
```

---

### 📌 DAY 8 — Monday, July 27

**Morning:** P4E Ch.4 (functions) videos + notes.

**Evening:**
- [ ] 60 min — **The week's most important refactor.** Your scripts work, but their logic is trapped inside them — unusable elsewhere, untestable. Functions fix that. Create `src/learning_journey/retirement.py`:

```python
"""Retirement-plan calculation functions.

Week 1 logic, promoted from scripts into a reusable, testable module.
This triple-quoted string is a DOCSTRING — documentation that lives in the
code. Every module and function gets one. `help(retirement)` will print it.
"""

# --- Constants live at module level, named once ---
IRS_DEFERRAL_LIMIT = 23_500   # TODO: verify current-year limit
CATCH_UP_LIMIT = 7_500        # TODO: verify
CATCH_UP_AGE = 50


def annual_contribution(salary: float, deferral_rate: float, age: int) -> float:
    """Return the capped annual deferral for a participant.

    Anatomy of this line (new concepts):
      def              = define a function
      salary: float    = parameter with a TYPE HINT — documents what kind
                         of value belongs here. Python doesn't enforce hints,
                         but tools (mypy, Pylance) and humans rely on them.
                         Production habit: every signature is hinted. Always.
      -> float         = this function RETURNS a float.

    Args:
        salary: Annual gross salary in dollars. Must be positive.
        deferral_rate: Elected deferral as a decimal (0.06 = 6%).
        age: Participant age (drives catch-up eligibility).

    Raises:
        ValueError: If salary or rate is invalid. Bad input should fail
            LOUDLY at the boundary, not produce a quiet wrong number.
    """
    if salary <= 0:
        raise ValueError(f"salary must be positive, got {salary}")
    if not 0 <= deferral_rate <= 1:
        raise ValueError(f"deferral_rate must be 0–1, got {deferral_rate}")

    limit = IRS_DEFERRAL_LIMIT
    if age >= CATCH_UP_AGE:
        limit += CATCH_UP_LIMIT          # += means limit = limit + CATCH_UP_LIMIT

    return min(salary * deferral_rate, limit)
    # `return` hands the result back to whoever called the function.
    # No print() in here! Functions COMPUTE; callers decide what to show.
    # (Roadmap trajectory note: the production standard's named answer to
    # "then how does a running system talk?" is STRUCTURED LOGGING via
    # structlog — Correction 16. You'll take a first taste of it in Week 4;
    # for now, the habit is simply: no print() inside functions.)


def vested_percent(years_of_service: int, schedule: str = "graded") -> float:
    """Return vested fraction (0.0–1.0) under a cliff or graded schedule.

    `schedule: str = "graded"` gives the parameter a DEFAULT — callers can
    omit it. Day 3's if/elif logic now lives here, reusable forever.
    """
    if schedule == "cliff":
        return 1.0 if years_of_service >= 3 else 0.0
        # ^ conditional expression: "A if condition else B" — one-line if/else

    if schedule == "graded":
        if years_of_service >= 6:
            return 1.0
        if years_of_service >= 2:
            return 0.20 * (years_of_service - 1)
        return 0.0

    raise ValueError(f"unknown schedule: {schedule!r}")


# --- The main guard: makes the file BOTH importable and runnable ---
if __name__ == "__main__":
    # This block runs ONLY when you execute the file directly
    # (uv run python src/learning_journey/retirement.py) — NOT when another
    # file imports it. Standard Python structure; you'll type it forever.
    print("Demo:")
    print(f"  $120k @ 25%, age 52 → ${annual_contribution(120_000, 0.25, 52):,.2f}")
    print(f"  4 yrs graded → {vested_percent(4):.0%} vested")
```
- [ ] 40 min — **Conventional Commits, formalized:** read conventionalcommits.org (10 min). From tonight, every commit is `type: imperative description` (`feat:`, `fix:`, `docs:`, `test:`, `refactor:`, `chore:`). Commit tonight's work: `refactor: extract retirement calcs into typed module`
- [ ] 20 min — Journal + commit

---

### 📌 DAY 9 — Tuesday, July 28

**Morning:** Mode SQL Tutorial — Basic: SELECT & WHERE. Type every query in Mode's editor AND transcribe to `sql/01_basics.sql` with comments:

```sql
-- Mode SQL Basic — my transcript (Day 9)
-- SQL reads like a sentence: SELECT columns FROM table WHERE conditions.

-- Everything from a table (fine to explore; wasteful in production —
-- always name your columns in real code):
SELECT * FROM tutorial.us_housing_units;

-- Specific columns:
SELECT year, month, south
  FROM tutorial.us_housing_units;

-- Filtering. Note: SQL uses ONE = for comparison (Python uses ==) —
-- keep the two languages' rules separate in your head from day one.
SELECT *
  FROM tutorial.us_housing_units
 WHERE south > 60;
```
**Evening:**
- [ ] 60 min — Mode SQL: ORDER BY, LIMIT, logical operators (AND/OR/NOT, BETWEEN, IN) — keep transcribing with your own comments
- [ ] 40 min — CS50x Week 2 pset
- [ ] 20 min — Journal + commit (`docs: mode sql basics transcript`)

---

### 📌 DAY 10 — Wednesday, July 29

**Morning:** P4E Ch.5 (loops/iteration) videos.

**Evening:**
- [ ] 60 min — Loops on your domain. Add to `retirement.py`:

```python
def project_balance(
    starting_balance: float,
    annual_contribution_amt: float,
    annual_return: float,
    years: int,
) -> list[float]:
    """Project year-end balances for `years` years.

    Returns a LIST — Python's ordered collection type: [year1, year2, ...].
    list[float] in the hint reads "a list of floats."
    Model (deliberately simple): contribute at year start, then grow.
    """
    balances: list[float] = []           # start empty
    balance = starting_balance

    for year in range(1, years + 1):
        # range(1, years+1) counts 1,2,...,years — the end is EXCLUSIVE,
        # which surprises everyone once. Now it's surprised you; done.
        balance = (balance + annual_contribution_amt) * (1 + annual_return)
        balances.append(balance)         # .append() adds to the end of a list

    return balances


if __name__ == "__main__":
    projection = project_balance(50_000, 12_000, 0.07, 10)
    # enumerate() gives you position AND value while looping:
    for year_num, bal in enumerate(projection, start=1):
        print(f"  Year {year_num:>2}: ${bal:,.2f}")   # :>2 right-aligns
```
- [ ] 40 min — **First tests** ⭐ — the eval-first mindset starts here. Create `tests/test_retirement.py`:

```python
"""First pytest suite.

Why tests, and why NOW:
1. Proof — not "it seems to work" but "these cases verifiably pass."
2. A safety net — refactor freely; tests catch what breaks.
3. The habit that becomes your eval-gate discipline: PolicyPulse's RAGAS
   gates are this exact idea aimed at LLM outputs. Same muscle, Week 2.

How pytest works: it finds files named test_*.py, runs functions named
test_*, and `assert <claim>` passes silently or fails loudly.
"""

from learning_journey.retirement import annual_contribution, vested_percent
# ^ imports work because of the src/ layout + pyproject.toml. This line IS
# the payoff of Day-0 structure: your code is a real, importable package.


def test_basic_contribution():
    # 60k at 10% = 6k — under every limit, simple math must hold.
    assert annual_contribution(60_000, 0.10, age=35) == 6_000.0


def test_limit_caps_high_earner():
    # 500k at 20% requests 100k → must cap at the base IRS limit (age < 50).
    assert annual_contribution(500_000, 0.20, age=40) == 23_500.0


def test_catch_up_raises_limit():
    # Same request at age 55 → base + catch-up.
    assert annual_contribution(500_000, 0.20, age=55) == 31_000.0


def test_graded_vesting_year_four():
    # Domain truth: 6-yr graded, year 4 → 60%.
    # pytest.approx handles float rounding fuzz — exact == on floats bites.
    import pytest
    assert vested_percent(4, "graded") == pytest.approx(0.60)
```
Run:
```bash
uv run pytest -v        # -v (verbose) lists each test by name
# Green dots = passing. Now break one on purpose (change 0.60 to 0.50),
# run again, READ the failure output, fix it back. Know both colors.
```
- [ ] 20 min — Journal + commit (`test: first pytest suite for retirement module`)

---

### 📌 DAY 11 — Thursday, July 30

**Morning:** CS50x Week 3 (algorithms) — searching/sorting; write Big-O notes in plain English ("how much slower does it get as data grows?").

**Evening:**
- [ ] 60 min — Mode SQL: finish Basic section + self-test from memory
- [ ] 30 min — Edge-case tests. Add to `tests/test_retirement.py`:

```python
import pytest


def test_negative_salary_rejected():
    # Testing that bad input FAILS CORRECTLY is as important as testing
    # that good input succeeds. pytest.raises asserts "this MUST raise".
    with pytest.raises(ValueError):
        annual_contribution(-50_000, 0.10, age=40)


def test_rate_above_one_rejected():
    with pytest.raises(ValueError):
        annual_contribution(60_000, 1.5, age=40)     # 150% deferral = nonsense


def test_unknown_schedule_rejected():
    with pytest.raises(ValueError):
        vested_percent(4, "immediate-maybe")
```
- [ ] 20 min — **Crucible seed:** create the free Alpaca paper-trading account; keys → password manager; build nothing; park it
- [ ] 10 min — Journal + commit (`test: edge cases for invalid inputs`)

---

### 📌 DAY 12 — Friday, July 31

**Morning:** P4E Course 1 final assignments/quizzes → **Course 1 complete** 🎉

**Evening:**
- [ ] 60 min — CS50x Week 3 pset (timebox; spill to Saturday if needed)
- [ ] 40 min — Repo hygiene: `uv run ruff check .` + `format` clean; docstring on every function; README Week 2 section
- [ ] 20 min — Journal + commit (`chore: week 2 lint + docs pass`)

---

### 📌 DAY 13 — Saturday, August 1 (deep work, 5.5h)

**Morning (5:00–8:30):**
- [ ] 90 min — Finish anything open (CS50x pset, P4E)
- [ ] 90 min — **Mini-project #1** ⭐ — first end-to-end program: file in → your functions → report out. Two files.

`src/learning_journey/projects/participants.csv` (synthetic — invent 10 rows; **synthetic-data-only is the public-repo governance rule, practiced from project #1**):
```csv
name,age,salary,deferral_pct,years_service
Ana Torres,34,62000,0.06,3
Luis Vega,51,98000,0.15,7
Mia Chen,45,120000,0.22,1
```
`src/learning_journey/projects/contribution_report.py`:
```python
"""Mini-project #1: contribution & vesting report from a participant CSV.

Pipeline shape (the same shape DataVault will have, in miniature):
    read file → validate each row → compute → report
Pure stdlib `csv` on purpose — feel the manual work now; pandas (later)
will then be a convenience you understand, not magic you depend on.
"""

import csv
from pathlib import Path
# pathlib.Path = the modern way to handle file paths (portable, readable).

from learning_journey.retirement import annual_contribution, vested_percent

DATA_FILE = Path(__file__).parent / "participants.csv"
# __file__ = this script's own location; .parent = its folder; / joins paths.
# Why not just "participants.csv"? Because that breaks when the program is
# run from a different folder. Path-relative-to-file always works.


def load_participants(path: Path) -> list[dict[str, str]]:
    """Read the CSV into a list of dicts (one dict per row).

    DictReader maps each row to {"name": "Ana Torres", "age": "34", ...}.
    NOTE: every value arrives as a STRING — files don't carry types.
    Converting str→int/float at the boundary is OUR job (Day 4's lesson,
    now at file scale).
    """
    with path.open() as f:
        # `with` = context manager: guarantees the file closes, even on error.
        return list(csv.DictReader(f))


def build_report(participants: list[dict[str, str]]) -> list[str]:
    """Compute one report line per participant. Returns lines, prints nothing.

    (Separating computation from printing = testable computation.)
    """
    lines = []
    for p in participants:
        contribution = annual_contribution(
            salary=float(p["salary"]),           # ← boundary conversions,
            deferral_rate=float(p["deferral_pct"]),  #   explicit and visible
            age=int(p["age"]),
        )
        vested = vested_percent(int(p["years_service"]))
        lines.append(
            f"{p['name']:<12} contributes ${contribution:>9,.2f}  |  {vested:>4.0%} vested"
        )   # :<12 pads name to 12 chars → columns align like a real report
    return lines


if __name__ == "__main__":
    participants = load_participants(DATA_FILE)
    print(f"CONTRIBUTION REPORT — {len(participants)} participants")
    print("-" * 55)
    for line in build_report(participants):
        print(line)
```
Run: `uv run python -m learning_journey.projects.contribution_report`
(`-m` runs it *as a module inside the package* — the professional invocation; it makes the imports resolve.)
- [ ] 30 min — Two tests for `build_report` (row count matches input; a known row computes correctly)

**Evening (8:00–10:00):**
- [ ] 60 min — P4E Course 2 (Data Structures): enroll, Ch.6 (strings) videos
- [ ] 45 min — Draft LinkedIn post #2 (pillar: finance→tech bridge — "I rebuilt a slice of my day job in 80 lines of Python; testing taught me more than the syntax did")
- [ ] 15 min — Journal + commit (`feat: mini-project 1 contribution report with tests`)

---

### 📌 DAY 14 — Sunday, August 2 (2h)
- [ ] 40 min — `weekly-summaries/week-02.md` + full `uv run pytest` + re-read all code
- [ ] 30 min — Publish post #2
- [ ] 30 min — Read the Weeks 3–4 plan
- [ ] 20 min — Journal + commit 🎉

---

## 📊 2-WEEK SUCCESS METRICS
```
TECHNICAL                                  HABITS & DISTRIBUTION
□ uv/Cursor/OpenCode/VS Code/git/gh/       □ 11+ journal entries (of 13 days)
  Docker verified · Tab off · rules file
□ uv Core Course #15 read + logged         □ 22+ commits, Conventional from Wk 2
□ uv.lock committed alongside pyproject    □ 2 LinkedIn posts published
□ P4E Course 1 complete                    □ HackGreenville joined + intro
□ CS50x Weeks 0–2 done, Wk 3 started       □ 2 meetups joined, 1 RSVP
□ Mode SQL Basic complete                  □ 80%+ of blocks completed
□ 7+ pytest tests passing (incl. raises)   □ Alpaca created (parked)
□ Mini-project #1 shipped (synthetic CSV)  □ No DL.AI Pro purchased (sprint
□ ruff clean repo                            months come later — Correction 17)
```
**Passing bar: 80%.** Below it, the calendar pauses — gaps close in Week 3's flex slots first. Eval-first applies to you too.

---

## 🚨 TROUBLESHOOTING

**`command not found` after installing:** restart Terminal first; then check `~/.zshrc` for the PATH lines the installer printed.
**Import error in tests (`No module named learning_journey`):** run from the project root, always via `uv run pytest`; confirm `src/learning_journey/` contains your files and `pyproject.toml` is present.
**`IndentationError`:** Python's indentation is structure. Select the block in the editor and check every line in a branch aligns at the same depth (4 spaces).
**CS50's C feels brutal:** normal and temporary. Timebox psets; understanding > completion; P4E is the priority thread.
**Ruff flags something cryptic:** look up the rule code, understand, fix. Never blanket-disable a rule you can't explain.
**Missed a block:** make up ≥1h same day or +time Saturday. Never let two days stack.
**Old-platform temptation (DataCamp/HackerRank/etc.):** the decision is made and documented — re-read the top table.
**Tempted to let the Agent "just write it":** that temptation is strongest exactly when the exercise is working (i.e., when you're learning the most). Switch to Ask mode, get the concept explained, type it yourself. The rules file will push back — let it. In 8 weeks you'll be directing agents across a real pipeline; this month buys that authority.

---

## 🔭 WHAT COMES NEXT

**Weeks 3–4 (Aug 3–16):** P4E Course 2 (data structures — the real workhorse), Mode SQL Intermediate (JOINs — the ~79%-of-DE-postings skill), *AI Python for Beginners* videos on the free tier with exercises replicated locally (labs are Pro-gated — Correction 17), Docker begins, your **first ADR** using the roadmap's new ADR learning pack (Correction 14), a first taste of **structlog** (Correction 16), and **AI-901 kickoff** (employer-reimbursed cert #1 + reimbursement paper trail = elevation-file evidence), plus mini-project #2: a two-system reconciliation toy that is deliberately DataVault's S1 pattern in miniature.

---
*Aligned to Career Roadmap v10.0 (Corrections 1–20). Propose→approve governance: this plan edits nothing; items flagged for review are in Day 5 and the Step-7 checkpoint.*