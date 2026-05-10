# 🚀 WEEKS 7-8 MASTER ACTIVATION PLAN
## GenAI-First Career Transformation | January 1–14, 2026

**Document Version:** 2.1 (v8.3 alignment — provider-agnostic SDK terminology)  
**Covers:** January 1, 2026 – January 14, 2026  
**Continues From:** Weeks 5-6 Activation Plan (Dec 18 – Dec 31)  
**Aligned To:** Career Roadmap v8.3 — Stage 1: GenAI-First Data Analyst & AI Engineer  
**Weekly Hours:** 25 hours/week (full intensity returns)  
**Month Position:** Month 2 — Weeks 1-2  
**Theme:** "BUILD MODE — DataVault Analyst Phase 1: Pipeline + Traditional Dashboard"

**🔑 Project Focus:** DataVault Analyst (Project #2 in portfolio) — AI-Powered PII-Safe Data Intelligence  
**Scope Document:** `DATAVAULT_ANALYST_SCOPE_v1.md` — Phase 1: Data Pipeline & Traditional Analytics

---

## 📋 TABLE OF CONTENTS

1. [Where You Stand After Week 6](#-where-you-stand-after-week-6)
2. [Week 7-8 Strategic Context: Month 2 Launch](#-week-7-8-strategic-context-month-2-launch)
3. [WEEK 7: DataVault Setup + PII Pipeline + First Dashboard (Jan 1–7)](#-week-7-datavault-setup--pii-pipeline--first-dashboard-jan-1--jan-7-2026)
4. [WEEK 8: Dashboard Pages + Metrics + Deploy (Jan 8–14)](#-week-8-dashboard-pages--metrics--deploy-jan-8--jan-14-2026)
5. [Week 7-8 Cumulative Metrics](#-week-7-8-cumulative-metrics)
6. [Troubleshooting Guide: Week 7-8 Specific](#-troubleshooting-guide-week-7-8-specific)
7. [What Comes Next: Week 9-10 Preview](#-what-comes-next-week-9-10-preview)

---

## 📊 WHERE YOU STAND AFTER WEEK 6

Confirm these milestones from Weeks 1-6. **Any gaps must be addressed in Week 7 mornings before adding new material.**

| Skill | Week 6 Exit State | Ready? |
|-------|-------------------|--------|
| **Python** | PY4E Course 1-2 COMPLETE | ✅ Functions, loops, dicts, lists, files, regex, APIs, JSON |
| **Pandas** | 5-6 DataCamp courses, EDA preview on project data | ✅ merge, groupby, filtering, agg, rolling |
| **SQL** | SQLZoo (70+), MODE (Basic→Advanced), DataCamp Intro done | ✅ JOINs, aggregations, CASE, window functions conceptual |
| **Visualization** | Matplotlib + Seaborn, 2+ dashboards | ✅ Line, bar, pie, scatter, hist, box, violin, heatmap |
| **Statistics** | Descriptive stats, correlation, distributions intro | ✅ Mean, median, std dev, quartiles, normal dist |
| **Google DA** | Course 1 DONE, Course 2 ~50% | ✅ Foundations + analytical thinking |
| **CS50** | Week 0-1 PS done, Week 2 lecture | ✅ Computational thinking, arrays |
| **AI Awareness** | 5 DeepLearning.AI courses complete | ✅ LLM APIs, LangChain, prompt engineering |
| **Git** | 42+ commits, 6-week streak | ✅ Daily commit habit |
| **Certificates** | 4-5 earned (Kaggle ×3-4, HackerRank) | ✅ LinkedIn updated |
| **Career** | 20 companies, 5 job descriptions saved, Upwork drafted | ✅ Foundation set |
| **1099 ETL Pipeline** | ✅ DEPLOYED in production — $15K/yr savings | ✅ Project #1 COMPLETE |

**Critical catch-up if behind:** If you haven't completed the EDA preview or Streamlit "Hello World", do that FIRST on January 1 before starting this plan.

---

## 🧠 WEEK 7-8 STRATEGIC CONTEXT: MONTH 2 LAUNCH

### The Big Shift: From Learning to Building

Weeks 1-6 were about **accumulating skills** — syntax, concepts, tools, certificates. Starting NOW, the emphasis shifts dramatically:

| Weeks 1-6 | Weeks 7-12 |
|-----------|-----------|
| Learn Python syntax | Build with Python |
| Practice SQL exercises | Query real datasets |
| Watch visualization tutorials | Create portfolio-grade charts |
| Study AI courses | Integrate AI into projects |
| Learn alone | Start networking and freelancing |

**Your portfolio project is now the #1 priority.** Everything else supports it.

### Why DataVault Analyst First (Not ODI or AFC)

Your README defines a deliberate project progression where each project introduces new skills building on the previous:

```
1. 1099 ETL Pipeline ✅ → ETL, pytest, CI/CD
2. DataVault Analyst ⭐ → + LLM SDK, PandasAI, Streamlit, Pydantic, PII handling
3. PolicyPulse 🧠 → + Embeddings, ChromaDB, RAG pipeline, semantic search
4. FormSense 📄 → + Multimodal AI, Vision LLM
5. ODI 📊 → + Enterprise real data, advanced analytics
6. StreamSmart 📺 → + External APIs, async HTTP, consumer UX
7. AFC 🚀 → + Statistical methodology, DuckDB, async data collection
```

**DataVault Analyst is your FIRST AI PROJECT to publish.** It establishes the SDK-first AI architecture (Gemini/OpenAI/Anthropic provider-agnostic pattern) that every subsequent project reuses. DataVault uses Gemini as primary (cost-effective for analytics queries); PolicyPulse + AFC will swap to **Anthropic Claude as primary** later (better RAG synthesis + financial reasoning per v8.3). Speed to publish is critical — recruiters need to see GenAI skills in the first 30 seconds of scanning your GitHub.

### Week 7-8 Hour Allocation (25 hrs/week × 2 = 50 hrs)

| Activity | Hrs/Week | Purpose |
|----------|---------|---------|
| **DataVault Analyst (Phase 1)** | **10** | PII pipeline, dashboard pages, Streamlit, Plotly |
| **Google DA Certificate** | **4** | Course 2 completion + Course 3 start |
| **DataCamp SQL** | **3** | Intermediate SQL + Joining Data |
| **Statistics (Coursera + Khan)** | **3** | UMich Stats with Python Course 1 |
| **CS50** | **2** | Week 3 progress |
| **Interview Prep (StrataScratch)** | **1.5** | SQL interview questions |
| **Career/Networking** | **1.5** | LinkedIn, Upwork launch |

### New Tools Introduced

| Tool | What It Is | Why Now |
|------|-----------|---------|
| **Streamlit** | Python framework for building web dashboards | DataVault needs a web interface — Streamlit turns Python scripts into interactive apps in <50 lines |
| **Plotly** | Interactive charting library | Streamlit + Plotly = interactive charts with hover/zoom/filters |
| **Faker** | Python library for generating synthetic data | DataVault needs realistic fake PII (SSN, names, DOB) for GitHub-safe demos |
| **Pydantic** | Data validation with Python type hints | DataVault schema validation + structured AI outputs (Phase 2) |
| **StrataScratch** | Real interview SQL questions from FAANG | You know enough SQL now to start practicing actual interview questions |

---

## 🗓 WEEK 7: DATAVAULT SETUP + PII PIPELINE + FIRST DASHBOARD (Jan 1 – Jan 7, 2026)

### Week 7 Goals

By January 7, you will have:

1. ✅ DataVault Analyst — Repository created with production structure
2. ✅ DataVault Analyst — Synthetic data generator producing realistic PII (Faker)
3. ✅ DataVault Analyst — Data ingestion pipeline loading Excel → validated DataFrame
4. ✅ DataVault Analyst — First Streamlit dashboard page rendering with charts
5. ✅ DataVault Analyst — GitHub Actions CI pipeline green
6. ✅ Google DA Certificate — Course 2 COMPLETE
7. ✅ Statistics with Python — Course 1 started (UMich on Coursera)
8. ✅ DataCamp — "Intermediate SQL" near complete
9. ✅ StrataScratch — First 3-4 interview SQL problems solved
10. ✅ 49+ total GitHub commits (7-week streak)

---

### 📌 DAY 43 — Wednesday, January 1, 2026

# 🎆 NEW YEAR'S DAY — MONTH 2 LAUNCH

**Theme: "While they set resolutions, you BUILD"**

#### Morning Block: 5:00 AM – 8:30 AM (3.5 hours — POWER DAY)

You're off work. Maximum focus. This is the day your first AI portfolio project goes from "planned" to "in progress."

**5:00 – 5:30 AM | Month 2 Ritual: Set Intentions (30 min)**
- [ ] Re-read `DATAVAULT_ANALYST_SCOPE_v1.md` — especially Phase 1 deliverables
- [ ] Open a fresh terminal. Create the DataVault Analyst repository:

```bash
# DataVault Analyst — SEPARATE repo from learning_journey
mkdir datavault-analyst
cd datavault-analyst
git init
mkdir data src tests notebooks docs
touch README.md requirements.txt .gitignore .env.example
touch src/__init__.py
touch src/data_loader.py
touch src/analytics.py
touch src/dashboard.py
touch src/synthetic_data.py
touch src/config.py
touch tests/__init__.py tests/test_data_loader.py tests/test_analytics.py
```

- [ ] **Why a SEPARATE repo?** Your learning_journey shows your GROWTH. This repo shows your PRODUCT.

**5:30 – 7:00 AM | DataVault: Synthetic Data Generator (90 min)**
- [ ] Create `src/synthetic_data.py` — critical because real PII NEVER goes on GitHub:

```python
"""
Synthetic Data Generator — DataVault Analyst
=============================================
Generates realistic retirement plan transaction data with fake PII
for GitHub-safe demos. Mirrors real OnBase export schema (15 columns).

Author: Manuel Reyes
"""

import pandas as pd
import random
from datetime import datetime, timedelta
from faker import Faker
from typing import Optional
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

fake = Faker()
Faker.seed(42)
random.seed(42)

DOCUMENT_TYPES = ["Distribution", "Loan"]
PRODUCT_TYPES = ["MBDI", "MBDII", "PLAT"]
PAYMENT_METHODS = ["ACH", "Wire", "Check"]
STATUSES = ["Processed", "Pending", "Rejected"]

PLAN_NAMES = [
    "Acme Corp 401(k)", "TechStart Retirement", "Metro Health Pension",
    "Pacific Foods 401(k)", "Summit Energy Savings", "Valley Credit Union Plan",
    "Heartland Manufacturing 401(k)", "Coastal Living Retirement",
    "Mountain View Partners", "River City Benefits Plan",
    "Golden State Savings", "Evergreen Industries 401(k)",
    "Sunrise Healthcare Plan", "Atlas Logistics Retirement",
    "Pinnacle Financial Group", "Heritage Mutual Fund",
    "Frontier Services 401(k)", "Liberty National Pension",
    "Cascade Employee Savings", "Prairie Holdings Plan"
]


def generate_synthetic_dataset(
    n_records: int = 2000,
    start_date: str = "2025-06-01",
    end_date: str = "2026-01-31"
) -> pd.DataFrame:
    """
    Generate synthetic OnBase-style retirement plan transaction data.

    Parameters
    ----------
    n_records : int
        Number of transaction records to generate.
    start_date, end_date : str
        Date range for document dates (YYYY-MM-DD).

    Returns
    -------
    pd.DataFrame
        DataFrame with 15 columns matching real OnBase export schema.
        Includes fake PII (SSN, names, DOB) for demo mode.
    """
    logger.info(f"Generating {n_records} synthetic records...")
    start = datetime.strptime(start_date, "%Y-%m-%d")
    end = datetime.strptime(end_date, "%Y-%m-%d")
    date_range = (end - start).days

    records = []
    for i in range(n_records):
        doc_date = start + timedelta(days=random.randint(0, date_range))
        stored_offset = random.choices([0, 1, 2], weights=[70, 25, 5])[0]
        date_stored = doc_date + timedelta(days=stored_offset)

        records.append({
            "Document Handle": f"DH-2025-{i+1:05d}",
            "Document Type": random.choices(DOCUMENT_TYPES, weights=[65, 35])[0],
            "Document Date": doc_date.strftime("%Y-%m-%d"),
            "Date Stored": date_stored.strftime("%Y-%m-%d"),
            "Time Stored": fake.time(),
            "Plan ID": f"PLN-{random.randint(1, 20):03d}",
            "Plan Name": random.choice(PLAN_NAMES),
            "Product Type": random.choices(PRODUCT_TYPES, weights=[50, 35, 15])[0],
            "SSN": fake.ssn(),
            "First Name": fake.first_name(),
            "Last Name": fake.last_name(),
            "Date of Birth": fake.date_of_birth(minimum_age=25, maximum_age=75).strftime("%Y-%m-%d"),
            "Amount": round(random.lognormvariate(9.5, 1.2), 2),
            "Payment Method": random.choices(PAYMENT_METHODS, weights=[60, 25, 15])[0],
            "Status": random.choices(STATUSES, weights=[80, 15, 5])[0],
        })

    df = pd.DataFrame(records)
    logger.info(f"Generated {len(df)} records with {df['Plan Name'].nunique()} plans")
    return df


if __name__ == "__main__":
    df = generate_synthetic_dataset(n_records=2000)
    df.to_csv("data/synthetic_transactions.csv", index=False)
    df.to_excel("data/synthetic_transactions.xlsx", index=False)
    print(f"Shape: {df.shape}")
    print(f"\nDocument Types:\n{df['Document Type'].value_counts()}")
    print(f"\nAmount stats:\n{df['Amount'].describe()}")
```

- [ ] Run it: `python src/synthetic_data.py`
- [ ] Verify: `data/synthetic_transactions.xlsx` exists with 2000 rows, 15 columns

**7:00 – 7:45 AM | DataVault: Data Loader Module (45 min)**
- [ ] Create `src/data_loader.py` with Excel loading, schema validation, PII column separation
- [ ] Key functions: `load_excel(file_path)` → validated DataFrame, `get_analytics_df(df)` → PII-free DataFrame
- [ ] Expected schema: 15 columns matching OnBase exports (Document Handle through Status)
- [ ] PII columns identified: SSN, First Name, Last Name, Date of Birth

**7:45 – 8:30 AM | DataVault: Config + .gitignore + Requirements + CI (45 min)**
- [ ] `src/config.py` — app title, data paths, demo file location
- [ ] `.gitignore` — exclude .env, .xlsx (except synthetic), __pycache__
- [ ] `requirements.txt` — pandas, openpyxl, plotly, streamlit, faker, pydantic, python-dotenv, pytest
- [ ] `.env.example` — template for API keys (Phase 2)
- [ ] `.github/workflows/ci.yml` — GitHub Actions CI
- [ ] Initial commit + push to GitHub

#### Evening Block: 8:00 PM – 10:00 PM (2 hours)

**8:00 – 8:45 PM | Google DA Certificate — Course 2 Push (45 min)**
**8:45 – 9:30 PM | Statistics with Python — Course 1 Week 1 (45 min)**
- [ ] Data types, measurement scales, descriptive statistics
- [ ] Connect to DataVault: "Distribution amounts follow a log-normal distribution"

**9:30 – 10:00 PM | StrataScratch — First Interview SQL Problems (30 min)**

```bash
git commit -m "Day 43: DataVault Analyst repo LIVE! Synthetic data gen + loader + CI 🚀"
```

---

### 📌 DAY 44 — Thursday, January 2, 2026

**Theme: "Streamlit Hello World + First Dashboard Page"**

#### Morning Block: 4:30 AM – 6:00 AM (1.5 hours)

**4:30 – 5:15 AM | DataVault: Streamlit App Shell (45 min)**
- [ ] Create `src/app.py` — entry point with:
  - Page config (title, icon, wide layout)
  - Sidebar: Data source selector (Demo Mode vs Upload Excel)
  - Demo mode loads `data/synthetic_transactions.xlsx` automatically
  - Upload mode accepts .xlsx file
  - KPI cards row: Total Records, Plans, Avg Amount, Distribution %

**5:15 – 6:00 AM | DataVault: Analytics Module DV01-DV05 (45 min)**
- [ ] Create `src/analytics.py` with first 5 pre-built metrics:
  - DV01: Total volume by document type
  - DV02: Product type distribution (MBDI/MBDII/PLAT)
  - DV03: Payment method breakdown (ACH/Wire/Check)
  - DV04: Day-of-week volume patterns
  - DV05: Top plans by transaction volume

#### Evening Block: 8:00 PM – 10:00 PM (2 hours)

**8:00 – 9:00 PM | DataCamp: Intermediate SQL (60 min)**
- [ ] CASE statements, aggregation with HAVING, subqueries

**9:00 – 9:30 PM | CS50 — Week 3 Lecture Start (30 min)**
**9:30 – 10:00 PM | Git Commit**

---

### 📌 DAY 45 — Friday, January 3, 2026

**Theme: "Dashboard Pages + Plotly Visualizations"**

#### Morning Block: 4:30 AM – 6:00 AM (1.5 hours)

**4:30 – 5:30 AM | DataVault: Tabbed Dashboard with Plotly (60 min)**
- [ ] Add 4 tabbed pages: Volume Overview, Plan Intelligence, Payment & Product, Temporal Patterns
- [ ] Interactive Plotly charts: line (daily trend), bar (top plans), pie (payment mix), heatmap (day-of-week)

**5:30 – 6:00 AM | DataVault: Sidebar Filters (30 min)**
- [ ] Filters: Document Type, Date Range, Product Type, Payment Method
- [ ] All charts respond to filter changes

#### Evening Block: 8:00 PM – 10:00 PM (2 hours)

**8:00 – 9:00 PM | Google DA Course 2 — Push to Complete (60 min)**
- [ ] **TARGET: Course 2 COMPLETE** ✅

**9:00 – 9:30 PM | StrataScratch (30 min)** — try first Medium problem
**9:30 – 10:00 PM | Git Commit**

---

### 📌 DAY 46 — Saturday, January 4, 2026

# 🔋 POWER DAY

**Theme: "All 10 Metrics + Tests + CI"**

#### Morning Block: 5:00 AM – 8:30 AM (3.5 hours)

**5:00 – 6:30 AM | DataVault: Complete Metrics DV06-DV10 (90 min)**
- [ ] DV06: Amount distribution (percentiles, tiers: <$10K, $10-50K, $50K+)
- [ ] DV07: Status breakdown (Processed/Pending/Rejected rates)
- [ ] DV08: Week-over-week volume change
- [ ] DV09: Month-over-month trend
- [ ] DV10: Distribution vs Loan comparative metrics

**6:30 – 7:30 AM | DataVault: Wire Metrics into Dashboard (60 min)**
- [ ] All 4 tabs populated with DV01-DV10 metrics and Plotly charts

**7:30 – 8:00 AM | DataVault: Tests + CI (30 min)**
- [ ] `tests/test_data_loader.py` — schema validation, PII column detection
- [ ] `tests/test_analytics.py` — metric functions with synthetic data
- [ ] Run: `pytest tests/ -v` → all green
- [ ] Push → GitHub Actions CI green

**8:00 – 8:30 AM | Google DA — Course 3 Start (30 min)**
- [ ] **MILESTONE: Google DA Course 2 COMPLETE** ✅

#### Evening Block: 8:00 PM – 10:00 PM (2 hours)

**8:00 – 9:00 PM | Statistics Course 1 Week 2 (60 min)**
- [ ] Histograms, box plots, summary statistics applied to DataVault data

**9:00 – 9:30 PM | DataCamp: Intermediate SQL continued (30 min)**
**9:30 – 10:00 PM | Git Commit**

---

### 📌 DAY 47 — Sunday, January 5, 2026

**Theme: "README Foundation + Career"**

#### Evening Block: 7:30 PM – 9:30 PM (2 hours)

**7:30 – 8:30 PM | DataVault: Professional README Draft (60 min)**
- [ ] Hero section: title, badges (Python, Streamlit, Gemini SDK, PandasAI, Pydantic, CI)
- [ ] One-liner for recruiters: *"Upload Excel → Ask questions in English → Get answers with PII protection"*
- [ ] Screenshots placeholder, live demo link placeholder
- [ ] Architecture overview, setup instructions

**8:30 – 9:00 PM | Upwork Profile Finalization (30 min)**
- [ ] Reference 1099 ETL (production) + DataVault (in development)

**9:00 – 9:30 PM | Git Commit**

---

### 📌 DAYS 48-49 — Monday-Tuesday, January 6-7, 2026

**Theme: "Weekday Momentum"**

#### Each Day:

Morning (4:30-6:00 AM):
- [ ] DataVault: Dashboard polish + data export feature (45 min)
- [ ] Google DA Course 3 progress (45 min)

Evening (8:00-10:00 PM):
- [ ] DataCamp: Intermediate SQL / Joining Data (45 min)
- [ ] StrataScratch: 2 problems/day (30 min)
- [ ] CS50 Week 3 / Stats Course 1 (45 min)

---

## 🗓 WEEK 8: DASHBOARD PAGES + METRICS + DEPLOY (Jan 8 – Jan 14, 2026)

### Week 8 Goals

By January 14, you will have:

1. ✅ DataVault Phase 1 — All 4 dashboard pages polished with Plotly charts
2. ✅ DataVault — 10 pre-built metrics (DV01-DV10) working
3. ✅ DataVault — DEPLOYED to Streamlit Cloud (traditional analytics — AI comes Week 9-10)
4. ✅ DataVault — Test coverage >80%, CI green
5. ✅ DataVault — README with demo GIF
6. ✅ Google DA — Course 2 COMPLETE, Course 3 in progress
7. ✅ Upwork — Profile LIVE, first proposal sent
8. ✅ StrataScratch — 12+ problems solved
9. ✅ 56+ total GitHub commits

---

### 📌 DAY 50 — Wednesday, January 8, 2026

**Theme: "Chart Polish + Deploy Prep"**

#### Morning Block: 4:30 AM – 6:00 AM

**4:30 – 5:30 AM | DataVault: Publication-Quality Charts (60 min)**
- [ ] Consistent color schemes, proper titles, axis labels, hover tooltips
- [ ] Plotly template="plotly_white", responsive sizing

**5:30 – 6:00 AM | DataVault: Streamlit Cloud Deploy Prep (30 min)**
- [ ] `.streamlit/config.toml`, verify requirements.txt, test locally

#### Evening Block: 8:00 PM – 10:00 PM

**8:00 – 8:45 PM | DataVault: DEPLOY to Streamlit Cloud (45 min)**
- [ ] Connect repo → deploy → test live URL → all 4 pages working 🎉

**8:45 – 9:30 PM | Google DA Course 3 (45 min)**
**9:30 – 10:00 PM | Git Commit**

---

### 📌 DAY 51 — Thursday, January 9, 2026

**Theme: "Upwork Launch + SQL Grind"**

Morning (4:30-6:00 AM):
- [ ] Upwork: Profile LIVE + first proposal (45 min)
- [ ] Stats Course 1 Week 3 (45 min)

Evening (8:00-10:00 PM):
- [ ] DataCamp: Joining Data in SQL (60 min)
- [ ] StrataScratch: 2 Medium problems (30 min)
- [ ] Git commit

---

### 📌 DAY 52 — Friday, January 10, 2026

**Theme: "Insights Discovery + Test Coverage"**

Morning (4:30-6:00 AM):
- [ ] DataVault: Discover 5+ insights from synthetic data (60 min)
  - Plan volume leaders? Day-of-week patterns? Payment trends? Amount outliers?
  - Add insight callout boxes to dashboard pages
- [ ] Google DA Course 3 (30 min)

Evening (8:00-10:00 PM):
- [ ] DataVault: Push test coverage >80% (60 min)
- [ ] StrataScratch + HackerRank (30 min)
- [ ] Git commit

---

### 📌 DAY 53 — Saturday, January 11, 2026

# 🔋 POWER DAY — Phase 1 Completion

Morning (5:00-8:30 AM):
- [ ] DataVault: README with screenshots + demo GIF (60 min) — the "30-second recruiter test"
- [ ] DataVault: Final Phase 1 review as a recruiter would experience it (60 min)
- [ ] **MILESTONE: DataVault Analyst Phase 1 COMPLETE** ✅
- [ ] Statistics Course 1 Week 4 (60 min)
- [ ] Kaggle micro-course completion (30 min)

Evening (8:00-10:00 PM):
- [ ] Google DA Course 3 accelerate (60 min)
- [ ] StrataScratch: 2 Medium problems → 12+ total (30 min)
- [ ] Git commit

---

### 📌 DAY 54 — Sunday, January 12, 2026

**Theme: "Career Actions + Week 8 Review"**

Evening (7:30-9:30 PM):
- [ ] LinkedIn Post: DataVault Analyst announcement with GIF + live URL (30 min)
- [ ] Upwork: Second proposal (30 min)
- [ ] Google DA Course 3 (30 min)
- [ ] **Week 8 Milestone Assessment** — DataVault Phase 1 deployed, all metrics working, CI green

---

### 📌 DAYS 55-56 — Monday-Tuesday, January 13-14, 2026

Morning each day: Google DA 3 + Stats Course 1 (45 min each)
Evening each day: StrataScratch + DataCamp SQL + CS50 (2 hrs each)

---

## 🏆 WEEK 7-8 CUMULATIVE METRICS

### By January 14, 2026 — 8 Weeks Complete!

| Category | Metric | Status |
|----------|--------|--------|
| **Study Hours** | Weeks 7-8 total | ~50 hrs |
| **Study Hours** | Grand total (8 weeks) | ~190 hrs |
| **GitHub** | Total commits | 56+ |
| **DataVault Analyst** | Phase 1 Status | DEPLOYED to Streamlit Cloud ✅ |
| **DataVault Analyst** | Dashboard Pages | 4/4 rendering ✅ |
| **DataVault Analyst** | Pre-built Metrics | DV01-DV10 all working ✅ |
| **DataVault Analyst** | README | Professional with demo GIF ✅ |
| **DataVault Analyst** | CI | GitHub Actions green ✅ |
| **1099 ETL Pipeline** | Status | Production — $15K/yr ✅ |
| **Google DA** | Progress | Course 2 DONE, Course 3 ~40% |
| **DataCamp SQL** | Courses | Intro ✅, Intermediate ✅, Joining started |
| **Statistics** | UMich Course 1 | ~50-60% complete |
| **StrataScratch** | Interview problems | 12+ solved (Easy + Medium) |
| **CS50** | Progress | Through Week 3 |
| **Upwork** | Status | Profile LIVE, 2 proposals sent |
| **LinkedIn** | Project post | Published with demo GIF |

---

## 🔧 TROUBLESHOOTING GUIDE: WEEK 7-8 SPECIFIC

### "Streamlit won't deploy to Cloud"
- Check `requirements.txt` — every import must be listed
- Use relative paths, not absolute
- Common fix: Add `sys.path.insert(0, "src")` at top of `app.py`
- Test locally with `streamlit run src/app.py` first

### "Synthetic data doesn't look realistic"
- Use `random.lognormvariate(9.5, 1.2)` for amounts — creates right-skewed distributions matching real financial data
- Use weighted `random.choices()` for categorical fields — 65/35 Distribution/Loan mirrors real data
- Set `Faker.seed(42)` for reproducible demo data

### "PII columns showing in wrong places"
- Use `get_analytics_df()` from data_loader for PII-free DataFrame
- PII columns exist in DataFrame but NEVER display in charts
- In demo mode, all PII is fake (Faker) — safe for GitHub

### "StrataScratch Medium problems too hard"
- Break into steps: tables → joins → aggregation → filters
- Write pseudo-code first, then translate to SQL
- OK to check hints after 15 minutes — the goal is learning patterns

---

## 🔮 WHAT COMES NEXT: WEEK 9-10 PREVIEW

**Week 9-10 = DataVault Analyst Phase 2: AI Chat Interface**

Your project transforms from "good dashboard" to "GenAI-powered intelligence tool":

- Gemini SDK setup (provider-agnostic abstraction)
- `ai_chat.py` module — natural language queries with code transparency
- PandasAI integration for "chat with your data"
- Pydantic structured outputs — type-safe AI responses
- PII leak prevention guardrails (governance as code)
- AI observability (token usage, cost, latency per query)
- Deploy Phase 2 to Streamlit Cloud
- Demo GIF/video with AI features

**Why this matters:** <1% of DA candidates can demonstrate LLM SDK + PandasAI + Pydantic + PII guardrails in a production app.

---

*Document updated: February 2026 (v2.0)*  
*Aligned to: GenAI-First Career Roadmap v8.3 + Portfolio Project Ecosystem*  
*Project: DataVault Analyst Phase 1 (Pipeline + Traditional Analytics)*  
*Previous: Weeks 5-6 Activation Plan*  
*Next: Weeks 9-10 — DataVault Analyst Phase 2 (AI Chat + Deploy)*
