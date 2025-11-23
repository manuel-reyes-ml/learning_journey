# Data, AI & Trading Learning Journey 🚀

Week-by-week practice projects and exercises for my roadmap:
**Bookkeeping & Trading → Data Analyst → Data Engineer → ML Engineer → LLM Engineer**  

I’m building a unique mix of **data analytics, machine learning, LLM engineering, and trading** skills, and documenting everything here.

---

## 👨‍💻 About Me

- Transitioning from **retirement bookkeeping** to **Data & AI** roles  
- Background in **finance and trading** (swing/day trading, market structure)  
- Long-term goal: work remotely as a **Data/ML/LLM Engineer** with a focus on **trading & quantitative systems**  
- This repo is my public notebook: small scripts, experiments, and projects as I level up

---

## 🧭 Roadmap (High Level)

1. **Data Analyst** – Python, SQL, Excel, statistics, dashboards, real-world datasets  
2. **Data Engineer** – ETL, data pipelines, databases, cloud tooling  
3. **ML Engineer** – advanced ML, model training, evaluation, deployment  
4. **LLM Engineer** – prompt engineering, fine-tuning, RAG, LLM-powered apps  
5. **Trading Integration (parallel)** – continuously apply skills to **trading algorithms & analytics**

I’m working on **trading algorithmic ideas** throughout the journey (data pipelines, signals, backtests).

---

## 🎓 Goals

- Short term (next 6–9 months)
  - Land a **remote Data Analyst** role  
  - Build **5+ portfolio projects** (finance/trading flavored where possible)
  - Be comfortable with **Python, SQL, Excel, and basic statistics**
- Long term
  - Grow into **ML Engineer → LLM Engineer**  
  - Develop and maintain **algorithmic trading & analytics systems**

---

## 📈 Progress Tracker

- ✅ Stage 1 - Data Analyst Foundations (Months 1-5)  
  - CS50 Harvard: Computer Science Fundamentals 
  - Python for Everybody specialization (University of Michigan)
  - Google Data Analytics Certification
  - IBM Data Analyst Professional Certification
  - SQL with Mode, SQLZoo, HackerRank
  - Statistics with Python (University of Michigan)

- ⏳ Stage 2 - Data Engineer Professional  
  - Coming soon...
  - 
  - 

---

## 🌐 Connect

Follow my journey and projects on LinkedIn:  
👉 **[LinkedIn]** *(link coming soon)*

---

## 🐍 Python Environment Setup

This project uses a local **virtual environment** stored in `.venv` inside the `python/` folder.

Recommended structure:

```text
~/dev/learning_journey/
  ├── python/
  │   ├── .venv/          # virtual environment (NOT committed to git)
  │   ├── check_env.py    # optional environment check script
  │   ├── requirements.txt
  │   └── ...your code...
  └── ...

cd ~/dev/learning_journey/python

# Create the virtual environment (only once)
python3 -m venv .venv

# Activate it
source .venv/bin/activate

# Upgrade pip inside the venv
python -m pip install --upgrade pip

# If there is no requirements.txt yet, install a basic dev stack
pip install numpy pandas matplotlib jupyter ipython
pip freeze > requirements.txt

#If requirements.txt already exists, just do:
pip install -r requirements.txt

#Each time you open a new terminal to work on this project:
cd ~/dev/learning_journey/python
source .venv/bin/activate
#You should see (.venv) at the beginning of your shell prompt, meaning the environment is active.

#When you are done working:
deactivate

