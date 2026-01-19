# 📊 Portfolio Projects

**All projects are maintained as separate repositories** for clarity, version control independence, and recruiter-friendly presentation.

This README serves as a **directory and roadmap** to all my project work across the 37-month journey.

---

## 📂 Repository Strategy

### Why Separate Repos?

**For Each Project:**
- ✅ **Independent version control** - Clear commit history per project
- ✅ **Focused README** - Each project has its own comprehensive documentation
- ✅ **Clean dependencies** - Project-specific requirements.txt
- ✅ **Easy sharing** - Send specific repo link to recruiters/interviewers
- ✅ **Better organization** - No single monolithic repo

**For This Repo (learning_journey):**
- 📚 Course materials, notes, and weekly summaries
- 🎓 Certifications tracking
- 📋 Activation plans and learning guides
- 🗺️ Roadmap and overall journey documentation

### Flagship Project Strategy

Rather than building many disconnected projects, I'm building **one flagship project** that evolves through all 5 career stages:

```
Attention-Flow Catalyst Evolution:

Stage 1 (DA):  SQLite → Backtest engine → Trigger leaderboard → Signals
                                    │
Stage 2 (DE):  AWS → Airflow → 500+ tickers → Real-time pipeline
                                    │
Stage 3 (ML):  XGBoost → LSTM → Ensemble → Auto-optimization
                                    │
Stage 4 (LLM): RAG → Natural language → AI Trading Assistant
                                    │
Stage 5 (Sr):  Production → Monitoring → Monetization ($2-50K/mo)
```

---

## 🔒 Data Privacy & Test Data Strategy

### Professional Approach to Sensitive Data

All production projects follow strict data privacy principles:

**1099 Reconciliation Pipeline:**
- ✅ **No client data in repository** - All sensitive data stays in production environment
- ✅ **Synthetic test data** - Uses `faker` module to generate realistic but fake data
- ✅ **Same structure, zero risk** - Test files match production format exactly
- ✅ **Runnable examples** - Anyone can clone and test with provided data
- ✅ **Privacy by design** - Architecture separates logic from data

**Example Test Data Generation:**
```python
from faker import Faker
fake = Faker()

# Generate realistic test participant data
test_data = {
    'name': fake.name(),
    'ssn': fake.ssn(),
    'distribution_amount': fake.random_number(digits=5),
    'distribution_date': fake.date_this_year()
}
```

**Benefits of This Approach:**
- 🔓 **Code is reviewable** - Recruiters can see actual implementation
- ✅ **Compliance maintained** - No risk of exposing client data
- 🧪 **Testability** - Easy to run and verify functionality
- 📚 **Educational** - Others can learn from real production patterns
- 💼 **Professional** - Shows understanding of data governance

---

## ✅ Production Projects

### 1099 Reconciliation ETL Pipeline
**Repo:** [1099_reconciliation_pipeline](https://github.com/manuel-reyes-ml/1099_reconciliation_pipeline) 🌐 *Public*  
**Company:** Daybright Financial  
**Status:** ✅ In Production  
**Tech Stack:** Python • pandas • Excel (openpyxl) • Data Validation • Matplotlib • Faker (test data)  

**Business Problem:**  
Manual reconciliation of retirement plan distributions between Relius and Matrix systems took 4-6 hours weekly, was error-prone, and blocked critical 1099-R tax reporting.

**Solution:**  
Automated ETL pipeline that extracts, transforms, validates, and reconciles data from both systems.

**Impact:**  
- ⚡ **95% time reduction** (4-6 hrs → 15-20 min weekly)
- ✅ **Error reduction** through automated validation
- 📊 **10x scalability** (30 → 300+ accounts)
- 💰 **Frees 15-20 hrs/month** for higher-value work

**Skills Demonstrated:**  
Data engineering, ETL pipelines, data validation, production deployment, business impact, test data generation

**Repository Highlights:**
- ✅ **Full source code available** - Review actual production-grade code
- ✅ **Comprehensive README** - Problem, solution, architecture, usage
- ✅ **Sample data included** - Synthetic test data generated with `faker` module
- ✅ **No client data** - All test cases use realistic but fake data for privacy
- ✅ **Runnable examples** - Clone and run with provided test data
- ✅ **Professional structure** - Clear organization, documentation, error handling

---

## 🚀 Flagship Project

### Attention-Flow Catalyst
**Repo:** [attention-flow-catalyst](https://github.com/manuel-reyes-ml/attention-flow-catalyst) 🌐 *Public*  
**Started:** December 2025 (Month 1)  
**Status:** 🚧 Phase 1A Active  
**Tech Stack:** Python • SQLite • pandas • edgartools • yfinance • Wikipedia API • RSS/GDELT • matplotlib  

> **Research Question:** Which trigger or combination best predicts +10% price moves within 3 trading days?

**Project Purpose:**  
Flagship project demonstrating complete career progression from Data Analyst to Senior LLM Engineer. Predictive trigger analysis system for small-cap stocks using alternative data sources.

**System Architecture:**
```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│  Stock Screener │ ──► │  Data Pipeline  │ ──► │ Trigger Detection│
│  50 small-caps  │     │  3yr history    │     │  T1-T4 signals   │
│  (<$5, listed)  │     │  per ticker     │     │  + combinations  │
└─────────────────┘     └─────────────────┘     └─────────────────┘
                                                        │
                                                        ▼
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│ Signal Generator│ ◄── │   Leaderboard   │ ◄── │ Backtest Engine │
│  daily watchlist│     │  rank by hit    │     │  test all combos│
└─────────────────┘     └─────────────────┘     └─────────────────┘
```

**Stock Screening Criteria:**
- Price < $5 (bigger % move potential)
- Listed exchanges only (NYSE, NASDAQ, AMEX — NO OTC)
- Small float (limited shares = faster moves)
- Strong sector (auto-detected by relative strength)

**Triggers Being Tested:**

| ID | Trigger | Data Source | What It Detects |
|----|---------|-------------|-----------------|
| **T1** | SEC Form 4 Insider Buy | edgartools | Smart money activity |
| **T2** | Wikipedia Attention Spike | Wikipedia API | Public attention surge |
| **T3** | News Mention Spike | RSS/GDELT | Media coverage |
| **T4** | Volume Accumulation | yfinance | Institutional buying patterns |

**Volume Signals (T4 Breakdown):**
- **T4a:** Relative Volume (RVOL ≥ 1.5x) — Unusual activity
- **T4b:** Accumulation Score Rising — Sustained buying pressure
- **T4c:** OBV Breakout (20-day high) — Cumulative buying strength
- **T4d:** Quiet Accumulation — Stealth institutional buying
- **T4e:** Volume Dry-Up — Sellers exhausted (pre-breakout)

**Combination Testing:**
- All individual triggers (T1, T2, T3, T4)
- All 2-trigger combinations (T1+T2, T1+T4, etc.)
- All 3-trigger combinations (T1+T2+T3, T1+T2+T4, etc.)
- All 4-trigger combination (T1+T2+T3+T4)
- Each tested with context filters (sector strength, index trend)

**Phase 1A Deliverables (Current):**
- ✅ Dynamic stock screener with auto-detection of strong sectors
- ✅ 3+ years historical data collection for 50 stocks
- ✅ All trigger detection (T1-T4) with context analysis
- ✅ Backtest engine testing all combinations
- ✅ Trigger leaderboard ranked by +10% hit rate
- ✅ Forward signal generator using winning triggers

**Skills Demonstrated:**  
Dynamic screening, API integration, database design, statistical backtesting, feature engineering, volume analysis, alternative data integration

**Project Evolution Through 5 Career Stages:**

| Stage | Version | Focus | Key Deliverable |
|-------|---------|-------|-----------------|
| **1 (DA)** | v2.0-v3.0 | Backtest engine | Trigger leaderboard, signal generator, dashboard |
| **2 (DE)** | v4.0 | Cloud scale | 500+ tickers, Airflow automation, AWS |
| **3 (ML)** | v5.0 | Predictions | ML ensemble, XGBoost/LSTM, auto-optimization |
| **4 (LLM)** | v6.0 | AI Assistant | Natural language interface, RAG system |
| **5 (Sr)** | v7.0 | Production | Monetization platform ($2-50K/mo potential) |

**Why This Project Stands Out:**
- ✅ **Dynamic screening** — Program finds stocks automatically (not manual list)
- ✅ **Real SEC data** — Form 4 insider transactions via edgartools
- ✅ **Statistical rigor** — Proper backtesting with combination testing
- ✅ **Volume analysis** — RVOL, OBV, accumulation patterns (institutional footprint)
- ✅ **Domain expertise** — 6 years trading knowledge codified into algorithms
- ✅ **Progressive architecture** — Evolves through all 5 career stages
- ✅ **Clear path to monetization** — Not just a learning project

---

## 📋 Planned Projects (Stage 1)

### Trading Dashboard (Phase 1B Component)
**Status:** 📅 Planned (Attention-Flow Catalyst Phase 1B)  
**Type:** Interactive Web Application

Interactive Streamlit dashboard built on Attention-Flow Catalyst data.

**Features:**
- Interactive trigger leaderboard visualization
- Stock screener results with filtering
- Active signals watchlist
- Backtest performance charts
- Export capabilities

**New Skills:** Streamlit, Plotly (interactive charts), UI/UX design  
**Relationship:** Component within flagship project (not separate repo)

---

### OnBase Workflow Intelligence System
**Planned Repo:** `onbase-workflow-intelligence` 🌐 *Public*  
**Status:** 📅 Next Major Project  
**Type:** Enterprise Analytics

Enterprise workflow analytics for retirement plan operations at Daybright Financial.

**Business Challenge:**  
No visibility into demand patterns or processing bottlenecks across workflows (distributions, contributions, enrollments, transfers), making resource allocation suboptimal.

**Planned Solution:**
- Data extraction from OnBase document management system
- Demand analysis per workflow type
- Processing time analysis per stage and queue
- Interactive dashboards for stakeholder visibility
- Actionable recommendations with ROI estimates

**Expected Impact:**
- Identify processing bottlenecks
- Enable data-driven resource allocation
- Reduce average processing times
- Improve capacity planning

**Skills to Demonstrate:**
- Enterprise system integration
- Business intelligence
- Stakeholder communication
- Process optimization
- Data-driven recommendations

**Tech Stack:** Python • SQL • pandas • data visualization • business intelligence

---

### ML Trading Models (Stage 3 Evolution)
**Status:** 📅 Planned (Attention-Flow Catalyst v5.0)  
**Type:** Machine Learning Application

Machine learning models predicting price movements using triggers and features from Phase 1.

**Planned Approach:**
- Feature engineering from trigger combinations
- XGBoost for tabular signal data
- LSTM for time-series patterns
- Ensemble strategies combining models
- Comprehensive backtesting framework

**New Skills:** scikit-learn, XGBoost, LSTM, feature engineering, ML backtesting  
**Relationship:** Stage 3 evolution of flagship project

---

## 📈 Project Progression Roadmap

### Stage 1: Data Analyst (Months 1-5) - **CURRENT**

| Month | Project | Status | Key Skills |
|-------|---------|--------|------------|
| **Current** | 1099 Reconciliation Pipeline | ✅ Production | ETL, validation, business impact |
| **1-2** | Attention-Flow Catalyst Phase 1A | 🚧 In Progress | APIs, database, backtesting, signals |
| **3** | Attention-Flow Catalyst Phase 1B | 📅 Planned | VSA metrics, Streamlit dashboard |
| **3-4** | OnBase Workflow Intelligence | 📅 Planned | Enterprise analytics, BI |

**Goal:** 2 major projects + 1 production system by Month 5

---

### Stage 2: Data Engineer (Months 6-15)

**Focus:** Cloud infrastructure, production pipelines, big data

**Key Deliverable:** Attention-Flow Catalyst v4.0
- Cloud migration (AWS S3, Glue, Redshift)
- Airflow orchestration for daily pipeline runs
- Scale to 500+ tickers
- Real-time data streaming

**Evolution:** Migrate flagship project to cloud with scheduled pipelines

---

### Stage 3: ML Engineer (Months 16-29)

**Focus:** Production ML models, deployment, MLOps

**Key Deliverable:** Attention-Flow Catalyst v5.0
- ML models (XGBoost, LSTM) for trigger prediction
- Ensemble strategies combining models
- Feature store implementation
- Model deployment (FastAPI + Docker)
- ML monitoring & retraining pipelines

**Evolution:** Add ML layer to flagship project with full MLOps workflow

---

### Stage 4-5: LLM Specialist → Senior (Months 30-37)

**Focus:** LLMs, RAG systems, AI agents, thought leadership

**Key Deliverable:** Attention-Flow Catalyst v6.0 & v7.0
- AI Trading Assistant (natural language interface)
- RAG system for market research
- Multi-agent orchestration
- Production deployment with monitoring
- Monetization ($2-50K/mo potential)

**Evolution:** Add LLM intelligence layer to complete AI trading platform

---

## 🎯 Integrated Project: Flagship Evolution

**Core Thread:** Attention-Flow Catalyst evolves across all 5 stages

```
Stage 1 (DA):    Dynamic screener → Backtest engine → Trigger leaderboard → Signals
                                    │
Stage 2 (DE):    AWS → Airflow → 500+ tickers → Real-time pipeline
                                    │
Stage 3 (ML):    XGBoost → LSTM → Ensemble → Auto-optimization
                                    │
Stage 4 (LLM):   RAG → Natural language → AI Trading Assistant
                                    │
Stage 5 (Sr):    Production → Monitoring → Monetization ($2-50K/mo)
```

**By Month 37:** Complete production-grade AI trading platform demonstrating full-stack expertise: data analysis → data engineering → ML → LLMs

---

## 🔗 Quick Links

### View All Repositories
**GitHub Profile:** [github.com/manuel-reyes-ml](https://github.com/manuel-reyes-ml)

### Public Repos
- [1099_reconciliation_pipeline](https://github.com/manuel-reyes-ml/1099_reconciliation_pipeline) - Production ETL system ✅
- [attention-flow-catalyst](https://github.com/manuel-reyes-ml/attention-flow-catalyst) - Flagship trading project 🚧
- [learning_journey](https://github.com/manuel-reyes-ml/learning_journey) - Course materials & roadmap 📚
- [data-portfolio](https://github.com/manuel-reyes-ml/data-portfolio) - Portfolio overview 💼

*All repositories are public with comprehensive documentation and runnable examples.*

---

## 💼 For Recruiters

### What These Projects Show

**1. Production Readiness**
- ✅ Real business problem solved (1099 pipeline)
- ✅ Measurable ROI (95% efficiency gain, $15K savings)
- ✅ **Production code publicly available** (review actual implementation)
- ✅ Domain expertise + technical skills
- ✅ Professional test data generation (faker module)

**2. Technical Depth**
- ✅ End-to-end data pipelines
- ✅ Dynamic stock screening algorithms
- ✅ Statistical backtesting methodology
- ✅ Multiple data sources (APIs, SEC filings, databases)
- ✅ Database design and SQL
- ✅ Volume analysis and feature engineering
- ✅ **Clear, production-grade code** (see for yourself!)
- ✅ Comprehensive documentation

**3. Growth Trajectory**
- ✅ Started with business automation
- 🚧 Building statistical analysis and backtesting skills
- 📅 Progressing toward ML and AI
- 🎯 Clear 37-month roadmap with one flagship project

**4. Self-Direction**
- ✅ Identified opportunities autonomously
- ✅ Built solutions without formal CS degree
- ✅ Learning in public with consistent progress
- ✅ Production-grade quality from Day 1
- ✅ **Open source mindset** (all code public for review)

### Why This Matters

**Immediate Value:**
- Already delivering production systems at current company
- Building flagship project with real SEC data and statistical rigor
- Can hit the ground running on data projects

**Unique Combination:**
- 10+ years finance domain expertise
- 6 years active trading experience
- New technical skills in Python/data/SQL
- Bridge between business and technology

**Future Potential:**
- Clear vision (37-month roadmap to Senior LLM Engineer)
- One flagship project evolving through all stages
- Systematic skill development
- Progressive career path with income at each stage

---

## 🛠️ Project Quality Standards

All projects follow these principles:

### Documentation
- ✅ Comprehensive README with problem, solution, impact
- ✅ Clear setup instructions and dependencies
- ✅ Architecture diagrams where applicable
- ✅ Code comments and docstrings
- ✅ CLAUDE.md for AI assistant context

### Code Quality
- ✅ Clean, readable code with consistent style
- ✅ Type hints on all function signatures
- ✅ Error handling and validation
- ✅ Modular design (functions, classes, modules)
- ✅ Version control with clear commit messages
- ✅ Config-driven (no hardcoded values)

### Business Focus
- ✅ Every project solves a real problem
- ✅ Measurable outcomes or learning objectives
- ✅ Demonstrated impact (time saved, insights gained)
- ✅ Scalability and maintainability considered

### Progressive Complexity
- ✅ Each stage builds on previous work
- ✅ Clear progression from simple to advanced
- ✅ New technologies/concepts introduced systematically
- ✅ One flagship project evolving through career stages

---

## 📊 Projects by Technology

### Python
- 1099 Reconciliation Pipeline (pandas, openpyxl)
- Attention-Flow Catalyst (all stages)

### Databases
- Attention-Flow Catalyst (SQLite → PostgreSQL → Cloud)
- Future: Redshift, BigQuery

### Data Sources
- edgartools (SEC Form 4 filings)
- yfinance API (market data, volume)
- Wikipedia Pageviews API (attention metrics)
- RSS feeds / GDELT (news headlines)
- Excel files (business data)

### Analysis & Backtesting
- Statistical z-scores (attention signals)
- Volume analysis (RVOL, OBV, accumulation)
- Combination testing (trigger pairs, triples)
- Forward return calculation

### Visualization
- Matplotlib (current)
- Plotly (planned)
- Streamlit (Phase 1B)

### Cloud (Future - Stage 2)
- AWS: S3, Glue, Redshift, Lambda
- Airflow orchestration
- Docker containerization

### ML/AI (Future - Stage 3-5)
- scikit-learn, XGBoost (Stage 3)
- TensorFlow/PyTorch, LSTM (Stage 3)
- LangChain, RAG systems (Stage 4)
- Multi-agent systems (Stage 5)

---

## 📈 Project Statistics

### Current Status (Month 1-2)
```
Total Projects:          2 (1 production, 1 flagship)
In Production:           1 (1099 pipeline - publicly viewable!)
In Development:          1 (Attention-Flow Catalyst Phase 1A)
Planned (Stage 1):       2 (Phase 1B dashboard, OnBase analytics)

Key Metrics:
├─ Production savings:   $15,000+/year
├─ Trigger types:        4 (T1-T4) + 5 volume sub-signals
├─ Combination tests:    15+ trigger combinations
├─ Backtest period:      3 years
├─ Target stocks:        50 small-caps
└─ Repositories:         4 (all public)
```

### Target by Month 5
```
Total Projects:          3 (1 production, 1 flagship, 1 enterprise)
Flagship Phases:         1A + 1B complete (backtest + dashboard)
Certifications:          3 (Python, Google DA, IBM DA)
Key Deliverable:         Trigger leaderboard with winning signals
```

### Target by Month 37
```
Flagship Version:        v7.0 (Production AI Trading Platform)
Revenue Potential:       $2-50K/month
Full Stack:              Data → Engineering → ML → LLM → Production
```

---

## 🤝 Collaboration & Feedback

While these are solo projects for learning and portfolio purposes, I'm open to:
- **Code reviews** from experienced developers
- **Feedback** on architecture and design decisions
- **Suggestions** for improvements or extensions
- **Discussions** about approaches and tradeoffs
- **Trading strategy** discussions and market analysis

**Connect with me:**
- LinkedIn: [Manuel Reyes](https://www.linkedin.com/in/mr410/)
- GitHub: [@manuel-reyes-ml](https://github.com/manuel-reyes-ml)
- Email: [manuelreyesv410@gmail.com](mailto:manuelreyesv410@gmail.com)

---

## 📄 License

All public projects are MIT licensed - feel free to learn from or adapt for your own use!

---

**Last Updated:** January 2026  
**Current Stage:** Stage 1 (Data Analyst), Month 1-2  
**Status:** 🔥 Building flagship project with statistical rigor  
**Next Update:** Phase 1A complete (backtest engine + trigger leaderboard)

---

*This directory is actively maintained and updated as new projects are added throughout the 37-month journey.*