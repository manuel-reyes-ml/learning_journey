# 📚 Learning Journey: Financial Services Professional → LLM Engineer

**37-Month Public Documentation** | Week-by-week practice, experiments, and enhancements

This repository documents my complete transition from **financial services professional & independent trader** to **Senior LLM Engineer** building AI-powered trading systems.

> 🎯 **Immediate Goal:** Land Data Analyst job (Month 5)  
> 🚀 **Long-term Goal:** Build production AI Trading Assistant (Month 37)
> 📋 **[View Complete Roadmap](https://manuel-reyes-ml.github.io/learning_journey/roadmap.html)**
---

## 👨‍💻 About This Repository

**What makes this different from typical learning repos:**

✅ **Not just homework** - Every exercise is enhanced, optimized, and tested with variations  
✅ **Building in public** - Commit history shows real learning process, struggles, and breakthroughs  
✅ **Finance + Tech fusion** - Applying data/ML/AI skills to trading and quantitative finance  
✅ **Production mindset** - Writing code with best practices, documentation, and testing from day 1  
✅ **37-month journey** - Complete transformation documented start to finish  

**What you'll find here:**
- Daily practice exercises (enhanced beyond course requirements)
- Experiments and alternative solutions
- Trading research and analysis
- Course notes and summaries
- Mini-projects and proof-of-concepts
- Code optimizations and refactoring

---

## 🧭 The Roadmap

Following a structured 37-month path from beginner to senior engineer:

### **Stage 1: Data Analyst (Months 1-5)** 🟢 *IN PROGRESS*
**Goal: Land first tech job!**

**Courses:**
- ✅ CS50 (Harvard) - Computer Science fundamentals *(Week 1)*
- 🔄 Python for Everybody (University of Michigan)
- 🔄 Google Data Analytics Professional Certificate
- 🔄 IBM Data Analyst Professional Certificate (11 courses)
- ⏳ Statistics with Python (University of Michigan)
- ⏳ SQL (Mode, SQLZoo, HackerRank)

**Trading Deliverable:**
- 📈 Market Data Analysis Dashboard with 10+ technical indicators

**Skills Acquired:**
- Python (Pandas, NumPy, Matplotlib, Plotly)
- SQL (queries, joins, aggregations, window functions)
- Statistics & probability
- Data cleaning & EDA
- Data visualization & storytelling
- Excel & business intelligence

---

### **Stage 2: Data Engineer (Months 6-15)** ⚪ *PLANNED*
**Goal: Build production data systems**

**Focus:**
- AWS (Data Engineer Associate, Solutions Architect)
- PostgreSQL, PySpark, Airflow
- ETL pipelines, data warehousing
- Cloud infrastructure

**Trading Deliverable:**
- 🔧 Real-time Trading Data Pipeline (production-grade)

---

### **Stage 3: ML Engineer (Months 16-29)** ⚪ *PLANNED*
**Goal: Apply ML to trading**

**Focus:**
- Mathematics for ML (Linear Algebra, Calculus)
- ML Specialization (Andrew Ng)
- Deep Learning, Neural Networks
- Model training, evaluation, deployment

**Trading Deliverable:**
- 🤖 ML-Powered Trading Models & Portfolio Optimizer

---

### **Stage 4: LLM Engineer (Months 30-34)** ⚪ *PLANNED*
**Goal: Build AI-powered systems**

**Focus:**
- Prompt Engineering
- RAG (Retrieval-Augmented Generation)
- Vector databases
- Fine-tuning LLMs
- Multi-agent systems

**Trading Deliverable:**
- 🚀 **AI Trading Assistant V1** (LLM-powered market analysis & signals)

---

### **Stage 5: Senior Engineer (Months 35-37)** ⚪ *PLANNED*
**Goal: Production deployment & monetization**

**Focus:**
- Production systems & scalability
- MLOps & monitoring
- Thought leadership (blog, YouTube, courses)
- Consulting & business development

**Trading Deliverable:**
- 💰 **AI Trading Assistant V2** (fully automated, production-deployed)

---

## 📁 Repository Structure

```
learning_journey/
│
├── 📄 README.md                  # Main documentation (you're reading this!)
│
├── 📂 docs/                      # GitHub Pages - Public website
│   ├── index.html                # Landing page at manuel-reyes-ml.github.io/learning_journey/
│   └── roadmap.html              # Interactive 37-month roadmap (v5.4)
│
├── 📂 cs50_harvard/              # CS50 problem sets & notes
│   ├── scratch/                  # Week 0 - Scratch projects
│   └── notes_cs50.md             # Course notes & key concepts
│
├── 📂 python/                    # Python practice & experiments
│   ├── .venv/                    # Virtual environment (not committed to git)
│   ├── week1_basics/             # Variables, loops, functions
│   ├── week2_flowcontrol/        # Conditionals, iterations
│   ├── week3_data_struct/        # Lists, dicts, sets
│   ├── experiments/              # My enhancements & tests
│   ├── requirements.txt          # Python dependencies
│   └── check_env.py              # Environment verification script
│
├── 📂 sql/                       # SQL query practice
│   ├── basics/                   # SELECT, WHERE, ORDER BY
│   ├── intermediate/             # JOINs, subqueries
│   ├── advanced/                 # Window functions, CTEs, optimization
│   └── notes_sqlbasics.md        # SQL concepts & patterns
│
├── 📂 trading/                   # Trading research & analysis
│   └── notes_trading_ideas.md    # Market analysis, strategy notes
│
├── 📂 notes/                     # General course notes
│   ├── week1_summary.md          # Week 1 learning summary
│   └── week2_summary.md          # Week 2 learning summary
│
├── .gitignore                    # Ignore .venv, __pycache__, etc.
└── README.md                     # This file
```

**Key Folders:**

- **`docs/`** - GitHub Pages hosting for interactive roadmap and landing page
- **`python/`** - All Python practice with virtual environment setup
- **`sql/`** - SQL practice organized by difficulty level
- **`cs50_harvard/`** - CS50 course materials and notes
- **`trading/`** - Trading-specific research and strategies
- **`notes/`** - Weekly summaries and general notes

**Not Committed to Git:**
- `python/.venv/` - Virtual environment (local only)
- `**/__pycache__/` - Python cache files
- `.DS_Store` - macOS system files

---

## 🎯 Current Progress (Stage 1)

### ✅ **Completed:**
- Week 1: CS50 Week 0 (Scratch)
- Python basics setup (virtual environment)
- SQL basics (SELECT, WHERE)

### 🔄 **In Progress (Week 1-2):**
- CS50 Week 1 (C fundamentals)
- Python for Everybody Week 1-2
- SQL practice (JOINs, aggregations)
- Setting up trading data sources

### ⏳ **Coming Next:**
- IBM Data Analyst courses (starting Month 2)
- Google Data Analytics case studies
- Statistics with Python
- First mini-project: Basic market data dashboard

---

## 💻 Environment Setup

This repo uses a **local virtual environment** for Python dependencies.

### **Initial Setup (One-time):**

```bash
# Navigate to python folder
cd ~/dev/learning_journey/python

# Create virtual environment
python3 -m venv .venv

# Activate it
source .venv/bin/activate

# Upgrade pip
python -m pip install --upgrade pip

# Install dependencies
pip install -r requirements.txt
```

### **Daily Workflow:**

```bash
# Activate environment
cd ~/dev/learning_journey/python
source .venv/bin/activate

# You should see (.venv) in your prompt
# Now you can run Python scripts, Jupyter, etc.

# When done
deactivate
```

### **Current Dependencies:**
```
numpy
pandas
matplotlib
seaborn
plotly
jupyter
ipython
yfinance        # For trading data
scipy           # Statistical analysis
requests        # API calls
```

---

## 📝 Commit Message Conventions

To keep the repo organized and show my thinking process, I use prefixed commit messages:

### **Categories:**

**🔧 Environment & Config**
```
Config: add virtualenv setup instructions
Config: ignore .venv in git
Config: add initial requirements.txt
Config: update dependencies for data viz
```

**🐍 Python Practice**
```
Python: add check_env.py script
Python: implement hours calculator exercise
Python: add solution for regex assignment
Python: refactor file parsing into function
Python: enhance exercise with error handling
Python: optimize performance by 40%
```

**🗄️ SQL Practice**
```
SQL: create mode_practice.sql with basic SELECTs
SQL: add JOIN and GROUP BY examples
SQL: add practice queries for album analysis
SQL: clean up comments and formatting
SQL: optimize query using indexes
SQL: add window function examples
```

**📊 Trading & Analysis**
```
Trading: add technical indicators research
Trading: implement RSI calculation
Trading: test backtesting framework
Trading: add market data fetching script
```

**📚 Documentation & Notes**
```
Docs: document daily workflow for venv
Docs: add notes on TRIM and COALESCE in SQL
Docs: summarize IBM course week 1 concepts
Docs: trading strategy research notes
```

**✨ Enhancements**
```
Enhance: add 3 alternative solutions to exercise
Enhance: optimize query performance
Enhance: add comprehensive error handling
Enhance: create visualization for results
```

**🔨 Refactoring**
```
Refactor: extract repeated code into functions
Refactor: improve code readability
Refactor: apply DRY principle to SQL queries
```

---

## 🚀 What Makes This Different

### **Not Just Following Tutorials:**

**Typical learner:**
```python
# Exercise: Calculate average
numbers = [1, 2, 3, 4, 5]
average = sum(numbers) / len(numbers)
print(average)
```

**My approach:**
```python
# Exercise: Calculate average
# ENHANCED: Added error handling, edge cases, multiple approaches

def calculate_average(numbers, method='arithmetic'):
    """
    Calculate average with multiple methods and robust error handling.
    
    Args:
        numbers: List of numbers
        method: 'arithmetic', 'geometric', 'harmonic'
    
    Returns:
        float: Calculated average
    
    Raises:
        ValueError: If list is empty or contains invalid values
    """
    if not numbers:
        raise ValueError("Cannot calculate average of empty list")
    
    if method == 'arithmetic':
        return sum(numbers) / len(numbers)
    elif method == 'geometric':
        from functools import reduce
        import operator
        product = reduce(operator.mul, numbers, 1)
        return product ** (1/len(numbers))
    elif method == 'harmonic':
        return len(numbers) / sum(1/x for x in numbers)
    else:
        raise ValueError(f"Unknown method: {method}")

# Testing with edge cases
assert calculate_average([1, 2, 3]) == 2.0
assert calculate_average([5]) == 5.0

# Compare methods
prices = [100, 102, 98, 101, 99]
print(f"Arithmetic: {calculate_average(prices, 'arithmetic'):.2f}")
print(f"Geometric: {calculate_average(prices, 'geometric'):.2f}")

# Performance testing with larger dataset
import time
large_data = list(range(1, 10001))
start = time.time()
result = calculate_average(large_data)
print(f"Time: {(time.time() - start)*1000:.2f}ms")
```

**Commit:**
```
Enhance: implement 3 average methods with comprehensive testing
- Added arithmetic, geometric, harmonic calculations
- Robust error handling for edge cases
- Performance benchmarking on 10K dataset
- Unit tests for validation
```

---

## 📊 Learning Stats

**Time Investment:**
- Daily: 3.5 hours (M-F: 4:30-6am + 8-10pm)
- Saturday: 5.5 hours (5-8:30am + 8-10pm)
- Sunday: 2 hours (7:30-9:30pm)
- **Total: 25 hours/week**
- **Bonus: 20 min/day Sololearn practice**

**Progress Tracking:**
- Week 1: ✅ 25 hours completed
- Week 2: 🔄 In progress
- Total hours: ~25/5,000+ (37-month journey)

**Completion Metrics:**
- CS50: Week 0/11 completed
- Python for Everybody: 0/5 courses
- IBM Data Analyst: 0/11 courses
- Portfolio projects: 0/6 Stage 1 projects

---

## 🎯 Stage 1 Goals (Months 1-5)

### **Technical Skills:**
- ✅ Python fundamentals (variables, loops, functions, data structures)
- ✅ SQL basics (SELECT, WHERE, JOIN)
- 🔄 Advanced Python (Pandas, NumPy, data analysis)
- 🔄 SQL intermediate (subqueries, window functions, CTEs)
- ⏳ Statistics & probability
- ⏳ Data visualization (Matplotlib, Plotly, Tableau)

### **Portfolio Projects (Must Complete):**
1. 📈 **Algorithmic Trading Dashboard** - Real-time market analysis with 10+ indicators
2. 📊 **IBM Data Analyst Capstone** - Professional end-to-end analysis
3. 📉 **Google Analytics Case Study** - Business intelligence project
4. 🔍 **SQL Data Warehouse Analysis** - Complex query practice
5. 📈 **Statistical Analysis Project** - Hypothesis testing, distributions
6. 🏆 **Kaggle Competition Entry** - Public notebook, community engagement

### **Job Search Prep:**
- ⏳ Resume with 5 major certificates
- ⏳ LinkedIn profile optimization
- ⏳ GitHub portfolio (4-6 pinned repos)
- ⏳ Interview prep (SQL, Python, behavioral)
- ⏳ 50-100 job applications

### **Target Outcome:**
- 🎯 **Data Analyst job offer by Month 5**
- 💰 $60-75K remote position
- 🇪🇸 Visa secured, income established
- 🚀 Continue learning while employed (Stage 2)

---

## 🌟 The Unique Value Proposition

### **What Recruiters See:**

**Most Data Analyst Candidates:**
- Know Python, SQL, Excel ✅
- Can make dashboards ✅
- Completed online courses ✅
- Generic projects ⚠️
- No domain expertise ⚠️

**What I Bring:**
- Python, SQL, Excel ✅
- Advanced data visualization ✅
- 5 major certifications ✅
- **Trading/finance domain expertise** 🌟
- **10+ years market experience** 🌟
- **Quantitative mindset** 🌟
- **Building toward ML/AI** 🌟
- **Unique projects (trading analytics)** 🌟

**The Pitch:**
> "I'm not just a data analyst who can make charts. I'm someone who understands markets, can build trading algorithms, and is on a path to becoming an LLM engineer. I bring both finance expertise AND cutting-edge technical skills."

---

## 📈 Trading Integration (All Stages)

Every stage includes trading-focused deliverables:

| Stage | Trading Project | Technologies |
|-------|----------------|--------------|
| **1. Data Analyst** | Market Analysis Dashboard | Python, Pandas, Plotly, yfinance |
| **2. Data Engineer** | Real-time Data Pipeline | AWS, PostgreSQL, Airflow, streaming |
| **3. ML Engineer** | ML Trading Models | scikit-learn, TensorFlow, backtesting |
| **4. LLM Engineer** | AI Trading Assistant V1 | LangChain, RAG, GPT-4, agents |
| **5. Senior** | Production AI System | MLOps, monitoring, deployment |

**End Result:**
> A complete, production-grade **AI Trading Assistant** that combines:
> - Real-time market data processing
> - ML-powered signal generation
> - LLM-based analysis and insights
> - Multi-agent orchestration
> - Automated execution capabilities

---

## 🔗 Related Repositories

**Portfolio Projects (Pinned):**
1. 🤖 **[algorithmic-trading-dashboard]** - Stage 1 capstone (WIP)
2. 📊 **[ibm-data-analyst-capstone]** - Professional certification project (Coming Month 4)
3. 📈 **[google-analytics-case-study]** - Business intelligence (Coming Month 4)
4. 💼 **[sql-data-analysis]** - Advanced SQL projects (Coming Month 3)

**This Repo:**
- 📚 Daily practice and experiments
- 🧪 Testing and optimization
- 📝 Course notes and summaries
- 🔬 Research and exploration

---

## 📚 Resources & References

**Main Roadmap:**
- [View complete 37-month roadmap](https://manuel-reyes-ml.github.io/learning_journey/roadmap.html)

**Courses & Platforms:**
- [CS50](https://cs50.harvard.edu/)
- [Python for Everybody](https://www.py4e.com/)
- [Google Data Analytics](https://www.coursera.org/google-certificates/data-analytics-certificate)
- [IBM Data Analyst](https://www.coursera.org/ibm-certifications/data-analyst)
- [Kaggle](https://www.kaggle.com/)
- [HackerRank](https://www.hackerrank.com/)

**Trading & Finance:**
- [Investopedia](https://www.investopedia.com/)
- [Machine Learning for Trading (Book)](https://www.ml4trading.io/)
- [QuantConnect](https://www.quantconnect.com/)

---

## 🤝 Contributing & Feedback

While this is primarily a personal learning repository, I welcome:

✅ **Feedback on code quality**  
✅ **Suggestions for improvements**  
✅ **Trading strategy discussions**  
✅ **Best practice recommendations**  
✅ **Resource suggestions**  

**Not accepting:**
❌ Solutions to exercises (I want to learn by doing!)  
❌ Direct answers without explanation  

**How to engage:**
- Open an issue for discussion
- Comment on specific commits
- Share your own learning journey
- Connect on LinkedIn

---

## 📫 Connect

**LinkedIn:** [Your Profile](https://www.linkedin.com/in/mr410/)  
**Email:** manuelreyesv410@gmail.com

**Open to:**
- Data Analyst job opportunities (remote, finance/trading sector)
- Networking with data professionals
- Trading + tech collaborations
- Learning accountability partners
- Mentorship (giving or receiving)

---

## 🏆 Milestones & Achievements

### **Week 1 (November 2025):**
- ✅ Completed CS50 Week 0 (Scratch)
- ✅ Set up development environment
- ✅ Created learning_journey repository
- ✅ Established daily practice routine (25 hrs/week)
- ✅ Committed to building in public

### **Coming Milestones:**
- 📅 Week 4: Complete CS50
- 📅 Month 2: Start IBM Data Analyst courses
- 📅 Month 3: Launch first trading dashboard
- 📅 Month 4: Complete capstone projects
- 📅 Month 5: Land Data Analyst job! 🎯

---

## 💭 Philosophy & Approach

### **Why I'm Building in Public:**

**Transparency:** Real learning is messy. Showing the process, not just the results.

**Accountability:** Public commits = public commitment. Can't fake progress.

**Community:** Others can learn from my journey, and I from theirs.

**Portfolio:** This repo IS the proof I can code, learn, and deliver.

**Future content:** Foundation for blog posts, tutorials, courses (Stage 5).

### **Learning Principles:**

1. **Practice > Theory:** Code every single day, even if just 20 minutes
2. **Enhance Everything:** Never just "complete" an exercise - make it better
3. **Document Thinking:** Commit messages explain WHY, not just WHAT
4. **Real-World Focus:** Every skill learned is applied to trading/finance
5. **Quality > Quantity:** Deep understanding beats surface-level completion
6. **Sustainable Pace:** 25 hrs/week for 37 months = marathon, not sprint

---

## 📊 Weekly Routine

**Monday - Friday:**
- 4:30-6:00 AM: Video lectures, reading (1.5 hrs)
- During work: Sololearn practice (20 min)
- 8:00-10:00 PM: Coding, projects, exercises (2 hrs)
- **Daily total: 3.5 hrs + 20 min bonus**

**Saturday:**
- 5:00-8:30 AM: Deep work - complex projects (3.5 hrs)
- 8:00-10:00 PM: Continue projects or catch-up (2 hrs)
- **Total: 5.5 hrs**

**Sunday:**
- 7:30-9:30 PM: Week review, planning, community (2 hrs)
  - 30 min: Review week's commits
  - 30 min: LinkedIn posts, networking
  - 30 min: Read 1 article (Real Python, trading research)
  - 30 min: Plan next week's focus

**Weekly Total: 25 hours** (sustainable long-term!)

---

## 🎯 Success Metrics

**Technical:**
- Lines of code committed (quality > quantity)
- Projects completed
- Certificates earned
- Kaggle competitions entered

**Career:**
- Job applications sent
- Interviews scheduled
- Offers received
- Salary progression

**Community:**
- LinkedIn connections (data professionals)
- GitHub stars/followers
- Helpful discussions participated in
- Knowledge shared

**Personal:**
- Consistency (days of 25 hrs/week maintained)
- Skills mastered (Python, SQL, ML, LLMs)
- Trading strategies developed
- AI system built

---

## 🚀 The Long Game

**This repo represents:**
- 37 months of dedicated learning
- 5,000+ hours of practice
- Transition from Financial Services Professional to LLM engineer
- Foundation for 6-figure career
- Path to Spain citizenship
- Potential for $400-700K/year by Month 37

**Every commit is a step toward:**
- Financial freedom through tech skills
- Location independence (remote work)
- Building AI systems that generate value
- Combining passion (trading) with profession (engineering)
- Creating opportunities to teach and mentor others

---

## 📖 Reading This?

If you're here, you're witnessing a complete career transformation in real-time.

**Bookmark this repo** to follow the journey from Day 1 to production AI system.

**Star it** if you appreciate the transparency and want to support the journey!

**Fork it** if you want to build your own learning journey structure.

---

### 💡 *"The journey of 37 months begins with a single commit."*

**Current Week:** 1 of 160  
**Current Stage:** Data Analyst (1 of 5)  
**Hours Invested:** 25 / 5,000+  
**Next Milestone:** CS50 completion (Week 4)  

---

⭐ **Star this repo to follow the journey!**  
🔔 **Watch for weekly updates!**  
💬 **Open an issue to discuss or connect!**

*Last updated: November 2025 | Week 1 of 160*