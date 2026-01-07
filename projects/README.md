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

**Future Projects:**
- Same approach for any work with sensitive data
- Documentation includes data privacy considerations
- Test suites use synthetic data exclusively
- Production deployment guides separate from code

---

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

## 🚀 Learning Capstone Projects

### Trading Attention Tracker
**Repo:** [trading_attention_tracker](https://github.com/manuel-reyes-ml/trading_attention_tracker) 🌐 *Public*  
**Started:** December 2025 (Month 1)  
**Status:** 🚧 v1.0 in Development  
**Tech Stack:** Python • SQLite • pandas • yfinance • Wikipedia API • RSS • Matplotlib  

**Project Purpose:**  
Capstone for _Python for Everybody_ specialization. End-to-end data pipeline integrating multiple APIs, database design, and analytical visualization.

**Description:**  
Correlates **stock trading volume**, **news headlines**, and **Wikipedia pageviews** for FAANG companies to analyze the relationship between public attention and market activity.

**Data Pipeline:**  
```
APIs/RSS → Python → SQLite → pandas → Analysis → Visualization
├── Market data: yfinance (historical prices & volume)
├── Attention: Wikipedia Pageviews API (JSON)
├── News: RSS feeds (XML) + BeautifulSoup
└── Storage: Normalized SQLite database
```

**Features:**
- Automated multi-source data ingestion
- Normalized database design (5 tables, foreign keys, joins)
- Basic sentiment analysis on headlines
- Time-series correlation analysis
- Clear visualizations (volume vs attention vs news)

**Skills Demonstrated:**  
End-to-end pipelines, API integration, database design, data wrangling, visualization, text processing

**Progression Plan:**
- **v1.0** (Month 1): Core pipeline, 3 tickers → *Capstone requirement* ✅
- **v1.1** (Month 2): Expand to 10+ tickers, CSV exports
- **v2.0** (Month 3): Interactive Streamlit dashboard
- **v3.0** (Month 4): ML models predicting volume from attention

---

## 📋 Planned Projects

### Financial Data Dashboard (Month 2-3)
**Planned Repo:** `financial-dashboard` 🌐 *Public*  
**Status:** 📅 Planned  
**Type:** Interactive Web Application (v2.0 of Trading Tracker)

**Features:**
- Interactive Streamlit/Plotly dashboard
- Company selector and date range filtering
- Dynamic multi-ticker comparisons
- Exportable PDF/PNG reports

**New Skills:** Web frameworks (Streamlit), interactive viz (Plotly), UI/UX design

---

### ML Trading Strategy Prototype (Month 3-4)
**Planned Repo:** `ml-trading-strategy` 🌐 *Public*  
**Status:** 📅 Planned  
**Type:** Machine Learning Application (v3.0 evolution)

**Features:**
- Feature engineering (returns, volatility, technical indicators)
- Baseline ML models (logistic regression, decision trees)
- Backtesting framework on historical data
- Model evaluation and performance metrics

**New Skills:** Scikit-learn, feature engineering, ML evaluation, backtesting

---

## 📈 Project Progression Roadmap

### Stage 1: Data Analyst (Months 1-5) - **CURRENT**

| Month | Project | Status | Key Skills |
|-------|---------|--------|------------|
| **Current** | 1099 Reconciliation Pipeline | ✅ Production | ETL, validation, business impact |
| **1** | Trading Attention Tracker v1.0 | 🚧 In Progress | APIs, database, visualization |
| **2** | Trading Tracker v1.1 | 📅 Planned | Scaling, exports, reporting |
| **2-3** | Financial Dashboard | 📅 Planned | Web apps, interactive viz |
| **3-4** | ML Trading Prototype | 📅 Planned | ML basics, backtesting |

**Goal:** 4 public portfolio projects + 1 production system by Month 5

---

### Stage 2: Data Engineer (Months 6-15)

**Focus:** Cloud infrastructure, production pipelines, big data

Planned projects:
- Cloud ETL Pipeline (AWS S3 + Glue + Redshift)
- Real-time Streaming Pipeline (Kafka/Kinesis)
- Airflow Orchestration for Trading Data
- Data Warehouse Design & Optimization

**Evolution:** Migrate Trading Tracker to cloud, add scheduled pipelines, scale to 100+ tickers

---

### Stage 3: ML Engineer (Months 16-29)

**Focus:** Production ML models, deployment, MLOps

Planned projects:
- Production ML Trading Models
- Model Deployment (FastAPI + Docker)
- ML Monitoring & Retraining Pipelines
- Feature Store Implementation

**Evolution:** Deploy ML models to production with full MLOps workflow

---

### Stage 4-5: LLM Specialist → Senior (Months 30-37)

**Focus:** LLMs, RAG systems, AI agents, thought leadership

Planned projects:
- AI Trading Assistant (natural language interface)
- RAG System for Financial Research
- Fine-tuned LLM for Financial Analysis
- Multi-Agent Trading System

**Evolution:** Add LLM intelligence layer to complete AI trading platform

---

## 🎯 Integrated Project: Trading System Evolution

**Core Thread:** Trading Attention Tracker evolves across all 5 stages

```
Stage 1 (DA):    Data pipeline, SQLite, analysis
                 ↓
Stage 2 (DE):    Cloud infrastructure, Airflow, scale
                 ↓
Stage 3 (ML):    ML models, predictions, deployment
                 ↓
Stage 4 (LLM):   AI assistant, RAG, natural language
                 ↓
Stage 5 (Sr):    Production platform, monetization, thought leadership
```

**By Month 37:** Complete production-grade AI trading platform demonstrating full-stack expertise: data engineering → ML → LLMs

---

## 🔗 Quick Links

### View All Repositories
**GitHub Profile:** [github.com/manuel-reyes-ml](https://github.com/manuel-reyes-ml)

### Public Repos
- [1099_reconciliation_pipeline](https://github.com/manuel-reyes-ml/1099_reconciliation_pipeline) - Production ETL system (public)
- [trading_attention_tracker](https://github.com/manuel-reyes-ml/trading_attention_tracker) - Learning capstone (public)
- [learning_journey](https://github.com/manuel-reyes-ml/learning_journey) - Course materials (public)

*All repositories are public with comprehensive documentation and runnable examples.*

---

## 💼 For Recruiters

### What These Projects Show

**1. Production Readiness**
- ✅ Real business problem solved (1099 pipeline)
- ✅ Measurable ROI (95% efficiency gain)
- ✅ **Production code publicly available** (review actual implementation)
- ✅ Domain expertise + technical skills
- ✅ Professional test data generation (faker module)

**2. Technical Depth**
- ✅ End-to-end data pipelines
- ✅ Multiple data sources (APIs, files, databases)
- ✅ Database design and SQL
- ✅ Data validation frameworks
- ✅ **Clear, production-grade code** (see for yourself!)
- ✅ Comprehensive documentation

**3. Growth Trajectory**
- ✅ Started with business automation
- 🚧 Building data analysis skills
- 📅 Progressing toward ML and AI
- 🎯 Clear 37-month roadmap

**4. Self-Direction**
- ✅ Identified opportunities autonomously
- ✅ Built solutions without formal CS degree
- ✅ Learning in public with consistent progress
- ✅ Production-grade quality from Day 1
- ✅ **Open source mindset** (all code public for review)

### Why This Matters

**Immediate Value:**
- Already delivering production systems at current company
- Can hit the ground running on data projects

**Unique Combination:**
- 10+ years finance domain expertise
- New technical skills in Python/data/SQL
- Bridge between business and technology

**Future Potential:**
- Clear vision (37-month roadmap to Senior LLM Engineer)
- Systematic skill development
- Each project more complex than the last
- Progressive career path with income at each stage

---

## 🛠️ Project Quality Standards

All projects follow these principles:

### Documentation
- ✅ Comprehensive README with problem, solution, impact
- ✅ Clear setup instructions and dependencies
- ✅ Architecture diagrams where applicable
- ✅ Code comments and docstrings

### Code Quality
- ✅ Clean, readable code with consistent style
- ✅ Error handling and validation
- ✅ Modular design (functions, classes, modules)
- ✅ Version control with clear commit messages

### Business Focus
- ✅ Every project solves a real problem
- ✅ Measurable outcomes or learning objectives
- ✅ Demonstrated impact (time saved, insights gained)
- ✅ Scalability and maintainability considered

### Progressive Complexity
- ✅ Each project builds on previous skills
- ✅ Clear progression from simple to advanced
- ✅ New technologies/concepts introduced systematically
- ✅ Integration of previous learnings

---

## 📊 Projects by Technology

### Python
- 1099 Reconciliation Pipeline (pandas, openpyxl)
- Trading Attention Tracker (all projects)

### Databases
- Trading Attention Tracker (SQLite, schema design)
- Future: PostgreSQL, Redshift, BigQuery

### Data Sources
- yfinance API (market data)
- Wikipedia Pageviews API (attention metrics)
- RSS feeds (news headlines)
- Excel files (business data)

### Visualization
- Matplotlib (current)
- Plotly (planned)
- Streamlit (planned)

### Cloud (Future)
- AWS: S3, Glue, Redshift, Lambda
- Airflow orchestration
- Docker containerization

### ML/AI (Future)
- Scikit-learn (Stage 3)
- TensorFlow (Stage 3)
- Transformers/LLMs (Stage 4-5)
- RAG systems (Stage 4-5)

---

## 📈 Project Statistics

### Current Status (Month 1)
```
Total Projects:          2 (1 production, 1 learning)
In Production:           1 (1099 pipeline - publicly viewable!)
In Development:          1 (Trading Tracker v1.0)
Planned (Stage 1):       2 (Dashboard, ML prototype)

Lines of Code:           ~2,500+ (and growing)
Repositories:            3 (all public)
Public Repos:            3 (100% transparency)
GitHub Stars:            Building community
```

### Target by Month 5
```
Total Projects:          5 (1 production, 4 learning)
Completed Learning:      4 portfolio projects
Certifications:          3 (Python, Google DA, IBM DA)
GitHub Stars:            TBD
Community Engagement:    Active on LinkedIn, Kaggle
```

---

## 🤝 Collaboration & Feedback

While these are solo projects for learning and portfolio purposes, I'm open to:
- **Code reviews** from experienced developers
- **Feedback** on architecture and design decisions
- **Suggestions** for improvements or extensions
- **Discussions** about approaches and tradeoffs

**Connect with me:**
- LinkedIn: [Manuel Reyes](https://www.linkedin.com/in/mr410/)
- GitHub: [@manuel-reyes-ml](https://github.com/manuel-reyes-ml)
- Email: [manuelreyesv410@gmail.com]

---

## 📄 License

All public projects are MIT licensed - feel free to learn from or adapt for your own use!

---

**Last Updated:** December 2025  
**Current Stage:** Stage 1 (Data Analyst), Month 1  
**Status:** 🔥 Building production-grade portfolio from Day 1  
**Next Update:** End of Month 1 (Trading Tracker v1.0 complete)

---

*This directory is actively maintained and updated as new projects are added throughout the 37-month journey.*