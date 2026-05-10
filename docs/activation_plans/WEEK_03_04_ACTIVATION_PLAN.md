# 🚀 WEEKS 3-4 MASTER ACTIVATION PLAN
## GenAI-First Career Transformation | December 4–17, 2025

**Document Version:** 1.0  
**Covers:** December 4, 2025 – December 17, 2025  
**Continues From:** Weeks 1-2 Activation Plan (Nov 20 – Dec 3)  
**Aligned To:** Career Roadmap v8.3 — Stage 1: GenAI-First Data Analyst & AI Engineer  
**Weekly Hours:** 25 hours/week  
**Month Position:** End of Month 1 → Start of Month 2 transition

---

## 📋 TABLE OF CONTENTS

1. [Where You Stand After Week 2](#-where-you-stand-after-week-2)
2. [Week 3-4 Strategic Context](#-week-3-4-strategic-context)
3. [WEEK 3: APIs, JOINs & AI Python (Dec 4–10)](#-week-3-apis-joins--ai-python-dec-4--dec-10-2025)
4. [WEEK 4: First Visualizations & Google DA Cert (Dec 11–17)](#-week-4-first-visualizations--google-da-cert-dec-11--dec-17-2025)
5. [4-Week Cumulative Metrics](#-4-week-cumulative-metrics)
6. [Troubleshooting Guide: Week 3-4 Specific](#-troubleshooting-guide-week-3-4-specific)
7. [What Comes Next: Week 5-6 Preview](#-what-comes-next-week-5-6-preview)

---

## 📊 WHERE YOU STAND AFTER WEEK 2

Before diving in, confirm these milestones from Weeks 1-2. If any are incomplete, **prioritize finishing them in Week 3 morning blocks before moving forward.**

| Skill | Week 2 Exit State | Ready for Week 3? |
|-------|-------------------|-------------------|
| **Python** | PY4E Ch.1-10 (Variables → Tuples) | ✅ You can write scripts with variables, conditionals, loops, functions, lists, dicts |
| **Pandas** | DataCamp "Data Manipulation with pandas" started | ✅ You understand DataFrames, basic filtering, groupby |
| **SQL** | SQLZoo Tutorials 0-5 (SELECT, WHERE, aggregates, subqueries) | ✅ You can write basic queries |
| **CS50** | Week 0 complete, Week 1 lecture partially watched | ✅ You understand computational thinking |
| **AI Awareness** | Prompt Engineering + Building Systems complete | ✅ You understand LLM APIs conceptually |
| **Git/GitHub** | 14+ commits, README.md written, streak established | ✅ You commit daily without thinking about it |
| **DataCamp** | 2 courses complete (Intro + Intermediate Python) | ✅ Interactive practice habit formed |

**If you're behind:** That's OK. Focus Week 3 mornings on catching up Python for Everybody through Ch.10 and finishing DataCamp Intermediate Python. Shift everything else by 3-4 days. The plan is designed with buffer.

---

## 🧠 WEEK 3-4 STRATEGIC CONTEXT

### Why These 2 Weeks Are a Turning Point

Weeks 1-2 built your **foundation** — you learned the grammar of programming. Weeks 3-4 shift you into **connecting to the real world:**

1. **APIs & JSON** — Your programs will fetch LIVE data from the internet (stocks, weather, news)
2. **SQL JOINs** — The single most important SQL concept for analyst interviews (asked in 90%+ of them)
3. **AI Python for Beginners** — Your first time writing Python that CONTROLS an LLM (GenAI-first moment!)
4. **Data Visualization** — Your first charts and graphs with Matplotlib (visual storytelling)
5. **Google DA Certificate** — Start your first industry-recognized credential

### The Big Unlock: "My Code Does Things in the Real World"

After Week 2, your scripts processed data YOU typed in. After Week 4, your scripts will:
- Fetch live stock prices from Yahoo Finance APIs
- Parse JSON responses from web services
- Join multiple data tables together (SQL)
- Create charts that tell stories about data
- Send prompts to LLMs and process the responses

This is the moment programming stops feeling like homework and starts feeling like a **superpower**.

### New Concepts Introduced in Weeks 3-4

| Concept | Why It Matters | Where You'll Learn It |
|---------|---------------|----------------------|
| **Regular Expressions (Regex)** | Pattern matching in text — extracting emails, dates, amounts from messy data | PY4E Ch.11 |
| **HTTP & Networking** | How the internet works — how your code talks to servers | PY4E Ch.12 |
| **APIs & JSON** | How programs exchange data — EVERY modern app uses this | PY4E Ch.13 |
| **SQL JOINs** | Combining data from multiple tables — #1 interview topic | SQLZoo Tutorial 6-7 |
| **Matplotlib** | Creating charts with code — visual storytelling | DataCamp + practice scripts |
| **LLM API Calls** | Writing Python that controls AI models — YOUR differentiator | AI Python for Beginners |
| **LangChain Basics** | Industry-standard framework for building LLM apps | DeepLearning.AI short course |

---

## 🗓 WEEK 3: APIs, JOINs & AI PYTHON (Dec 4 – Dec 10, 2025)

### Week 3 Goals

By Sunday night December 10, you will have:

1. ✅ Python for Everybody Ch.11-13 complete (Regex, Networking, Web Services/JSON)
2. ✅ CS50 Week 1 Problem Set submitted + Week 2 lecture started
3. ✅ DataCamp "Data Manipulation with pandas" COMPLETE
4. ✅ DataCamp "Joining Data with pandas" started
5. ✅ SQLZoo Tutorial 6 (JOIN) + Tutorial 7 (More JOIN) — at least 15 exercises
6. ✅ Andrew Ng's "AI Python for Beginners" COMPLETE (4-6 hours)
7. ✅ Kaggle "Intro to Python" micro-course started
8. ✅ First script that fetches live data from an API
9. ✅ First script that sends a prompt to an LLM and processes the response
10. ✅ 21+ total GitHub commits (3-week streak)

### Week 3 Total Hours: ~25 hours

---

### 📌 DAY 15 — Thursday, December 4, 2025

**Theme: "Regular Expressions" — Finding patterns in messy data**

#### Morning Block: 4:30 AM – 6:00 AM (1.5 hours)

**4:30 – 5:30 AM | Python for Everybody — Chapter 11: Regular Expressions (60 min)**
- [ ] Start **Chapter 11: "Regular Expressions"**
- [ ] Watch all video lectures for this chapter
- [ ] **What are regular expressions?** Think of them as super-powered Find & Replace:
  - Excel's Find only matches exact text
  - Regex matches PATTERNS: "any email address," "any phone number," "any dollar amount"
- [ ] **Key patterns to learn today:**
  - `.` — matches any single character
  - `*` — zero or more of the previous character
  - `+` — one or more of the previous character
  - `\d` — any digit (0-9)
  - `\s` — any whitespace (space, tab, newline)
  - `[A-Z]` — any uppercase letter
  - `^` — start of line, `$` — end of line
- [ ] **Why this matters for YOUR career:** Financial data is MESSY. Account numbers, SSNs, dates in different formats, dollar amounts with commas — regex extracts them all. Your 1099 ETL Pipeline? Regex is how you'd parse those tax forms.

**5:30 – 6:00 AM | Python for Everybody — Chapter 11: Exercises (30 min)**
- [ ] Complete the Chapter 11 quiz/exercises on Coursera
- [ ] Try the interactive regex practice in the course

#### Evening Block: 8:00 PM – 10:00 PM (2 hours)

**8:00 – 9:00 PM | Practice: Regex for Financial Data (60 min)**
- [ ] Create `day_015_regex.py`:

```python
# Day 15: Regular Expressions for Financial Data
# The power tool for extracting patterns from messy text

import re

# --- BASIC PATTERN MATCHING ---
# Imagine you received a messy text report from a financial system:
report = """
Transaction Report - Q4 2025
Account: 401K-78234 | Amount: $12,450.00 | Date: 12/15/2025
Account: IRA-99012  | Amount: $3,200.50  | Date: 11/30/2025
Account: 401K-45678 | Amount: $8,775.25  | Date: 12/01/2025
Contact: john.doe@company.com | Phone: (555) 123-4567
Contact: jane.smith@firm.org  | Phone: (555) 987-6543
Total distributions: $24,425.75
Tax withholding: 20% federal, 5% state
SSN references: ***-**-1234, ***-**-5678
"""

# Extract all dollar amounts
amounts = re.findall(r'\$[\d,]+\.\d{2}', report)
print("💰 Dollar amounts found:")
for amt in amounts:
    print(f"  {amt}")

# Extract all account numbers (pattern: LETTERS-DIGITS)
accounts = re.findall(r'[A-Z]+[a-z]*-\d{4,5}', report)
print(f"\n📋 Accounts found: {accounts}")

# Extract all email addresses
emails = re.findall(r'[\w.]+@[\w.]+\.\w+', report)
print(f"\n📧 Emails found: {emails}")

# Extract all phone numbers
phones = re.findall(r'\(\d{3}\)\s\d{3}-\d{4}', report)
print(f"\n📞 Phones found: {phones}")

# Extract all dates (MM/DD/YYYY format)
dates = re.findall(r'\d{2}/\d{2}/\d{4}', report)
print(f"\n📅 Dates found: {dates}")

# --- PRACTICAL: Clean and parse dollar amounts ---
def parse_dollar_amount(text):
    """Extract dollar amount from text and convert to float."""
    match = re.search(r'\$([\d,]+\.\d{2})', text)
    if match:
        # Remove commas and convert to float
        clean = match.group(1).replace(',', '')
        return float(clean)
    return 0.0

test_strings = [
    "The total was $12,450.00 for Q4",
    "Refund amount: $3,200.50",
    "No amount here",
    "Multiple: $100.00 and $200.00",
]

print("\n💵 Parsed amounts:")
for s in test_strings:
    result = parse_dollar_amount(s)
    print(f"  '{s[:40]}...' → ${result:,.2f}")

# --- VALIDATION: Check if string matches pattern ---
def is_valid_account(account_str):
    """Validate retirement account number format."""
    pattern = r'^(401K|IRA|ROTH|403B)-\d{5}$'
    return bool(re.match(pattern, account_str))

test_accounts = ["401K-78234", "IRA-99012", "INVALID", "401K-123", "ROTH-55555"]
print("\n✅ Account validation:")
for acct in test_accounts:
    valid = is_valid_account(acct)
    status = "✅ Valid" if valid else "❌ Invalid"
    print(f"  {acct:15} → {status}")
```

- [ ] Run it. Experiment with changing the patterns. Break them and fix them.
- [ ] **Key insight:** This script demonstrates a skill that 80% of junior analysts DON'T have. Regex + financial domain = instant value at any company.

**9:00 – 9:30 PM | SQLZoo — Tutorial 6: JOIN (30 min)**
- [ ] Start **Tutorial 6: "JOIN"** — **THE most important SQL tutorial in this entire journey**
- [ ] Complete the first 6-8 exercises
- [ ] **What is a JOIN?** It combines rows from two or more tables based on a related column
  - Think of it like VLOOKUP in Excel, but MUCH more powerful
  - Example: Table 1 has employee names + department_id. Table 2 has department_id + department_name. JOIN connects them.
- [ ] **Types of JOINs to understand:**
  - `INNER JOIN` — only rows that match in BOTH tables (most common)
  - `LEFT JOIN` — all rows from left table + matching from right (used for "find what's missing")
- [ ] **In your notebook:** Draw a Venn diagram of INNER JOIN vs LEFT JOIN

**9:30 – 10:00 PM | HackerRank — 2 SQL + 1 Python Challenge (30 min)**
- [ ] Do 2 HackerRank SQL challenges (Basic Select section)
- [ ] Do 1 HackerRank Python challenge (Strings section)

**10:00 PM | Git Commit**
```bash
git add .
git commit -m "Day 15: Regex for financial data extraction + SQL JOINs started 🔍"
git push
```

#### Day 15 Checklist
- [ ] PY4E Ch.11 (Regular Expressions) watched + exercises done
- [ ] `day_015_regex.py` — regex patterns for financial data
- [ ] SQLZoo Tutorial 6 (JOIN) — first 6-8 exercises
- [ ] HackerRank: 3 challenges (2 SQL + 1 Python)
- [ ] Git commit pushed (Day 15)
- [ ] **Total study time: ~3.5 hours** ✅

---

### 📌 DAY 16 — Friday, December 5, 2025

**Theme: "HTTP & Networking" — How your code talks to the internet**

#### Morning Block: 4:30 AM – 6:00 AM (1.5 hours)

**4:30 – 5:30 AM | Python for Everybody — Chapter 12: Networked Programs (60 min)**
- [ ] Start **Chapter 12: "Networked Programs"**
- [ ] Watch all video lectures
- [ ] **Key concepts:**
  - HTTP protocol — how browsers (and your code) request web pages
  - URLs, request/response cycle
  - `urllib` library — Python's built-in tool for fetching web data
  - Sockets — the low-level connection between your computer and a server
- [ ] **Why this matters:** Every AI API call, every stock price fetch, every data pipeline — they all use HTTP. Understanding the request/response cycle is fundamental to everything you'll build.

**5:30 – 6:00 AM | PY4E Ch.12 Exercises (30 min)**
- [ ] Complete the Chapter 12 quiz on Coursera
- [ ] Try the socket exercise if time permits

#### Evening Block: 8:00 PM – 10:00 PM (2 hours)

**8:00 – 8:45 PM | Practice: Fetching Data from the Web (45 min)**
- [ ] Create `day_016_web_requests.py`:

```python
# Day 16: Networked Programs — Fetching Data from the Web
# Your code reaches out to the internet for the first time!

import urllib.request
import json

# --- FETCH A WEB PAGE ---
print("=== Fetching a web page ===")
url = "http://www.example.com"
try:
    response = urllib.request.urlopen(url)
    html = response.read().decode('utf-8')
    print(f"Status: {response.status}")
    print(f"Content length: {len(html)} characters")
    print(f"First 200 chars:\n{html[:200]}...")
except Exception as e:
    print(f"Error: {e}")

# --- FETCH JSON DATA (this is how APIs work!) ---
print("\n=== Fetching JSON data from an API ===")
# Free public API - no key needed
api_url = "https://jsonplaceholder.typicode.com/users/1"
try:
    response = urllib.request.urlopen(api_url)
    data = json.loads(response.read().decode('utf-8'))

    # data is now a Python dictionary!
    print(f"Name: {data['name']}")
    print(f"Email: {data['email']}")
    print(f"Company: {data['company']['name']}")
    print(f"City: {data['address']['city']}")

    # The JSON → Python conversion:
    # JSON object {} → Python dict {}
    # JSON array  [] → Python list []
    # JSON string "" → Python str  ""
    # JSON number    → Python int or float
    print(f"\nData type: {type(data)}")  # <class 'dict'>
except Exception as e:
    print(f"Error: {e}")

# --- FETCH MULTIPLE RECORDS ---
print("\n=== Fetching multiple records ===")
api_url = "https://jsonplaceholder.typicode.com/users"
try:
    response = urllib.request.urlopen(api_url)
    users = json.loads(response.read().decode('utf-8'))

    print(f"Total users: {len(users)}")
    for user in users[:5]:  # First 5 only
        print(f"  {user['name']:25} | {user['email']:30} | {user['address']['city']}")
except Exception as e:
    print(f"Error: {e}")

print("\n💡 KEY INSIGHT: This is EXACTLY how stock APIs, AI APIs, and")
print("   every web service works — request URL → get JSON → parse as dict!")
```

- [ ] Run it. You should see data fetched from the internet!
- [ ] **Milestone moment:** Your code just reached across the internet and pulled back data. This is the foundation of EVERY data pipeline, EVERY API call, EVERY AI integration you'll ever build.

**8:45 – 9:30 PM | SQLZoo — Tutorial 6: JOIN continued (45 min)**
- [ ] Continue **Tutorial 6: "JOIN"** — complete all remaining exercises
- [ ] Focus on understanding the JOIN syntax:
```sql
SELECT player, teamname
FROM goal
JOIN eteam ON goal.teamid = eteam.id
WHERE goal.teamid = 'GER'
```
- [ ] **Read this as:** "Get me the player and team name, by connecting the goal table to the eteam table where the teamid matches the id."

**9:30 – 10:00 PM | DataCamp — "Data Manipulation with pandas" push to complete (30 min)**
- [ ] Work on remaining chapters to FINISH this course
- [ ] If already complete, start **"Joining Data with pandas"** Ch.1

**10:00 PM | Git Commit**
```bash
git add .
git commit -m "Day 16: HTTP networking + first API data fetch + SQL JOINs deeper"
git push
```

#### Day 16 Checklist
- [ ] PY4E Ch.12 (Networked Programs) watched + exercises
- [ ] `day_016_web_requests.py` — first script that fetches internet data!
- [ ] SQLZoo Tutorial 6 (JOIN) — complete or nearly complete
- [ ] DataCamp "Data Manipulation with pandas" — pushing to finish
- [ ] Git commit pushed (Day 16)
- [ ] **Total study time: ~3.5 hours** ✅

---

### 📌 DAY 17 — Saturday, December 6, 2025

**Theme: "POWER DAY — APIs & JSON + AI Python for Beginners Start"**

This is your deep work day — 5.5 hours of the most important content in Week 3.

#### Morning Block: 5:00 AM – 8:30 AM (3.5 hours)

**5:00 – 6:30 AM | Python for Everybody — Chapter 13: Web Services & JSON (90 min)**
- [ ] Start and complete **Chapter 13: "Using Web Services"**
- [ ] This is one of the MOST IMPORTANT chapters in the entire PY4E course
- [ ] **Key concepts:**
  - JSON (JavaScript Object Notation) — THE data format of the modern web
  - XML vs JSON — JSON won (simpler, lighter, universally used)
  - Parsing JSON with Python's `json` library
  - API keys and authentication basics
  - Rate limiting (don't overwhelm servers with requests)
- [ ] **Critical understanding:** JSON is just Python dictionaries and lists written as text:
  ```json
  {"name": "Manuel", "skills": ["Python", "SQL"], "years_exp": 15}
  ```
  When Python reads this, it becomes a normal dict you already know how to use!

**6:30 – 7:30 AM | Practice: Real Financial API Script (60 min)**
- [ ] First, install the `requests` library (easier than `urllib`):
  ```bash
  pip install requests
  ```
- [ ] Create `day_017_api_finance.py`:

```python
# Day 17: Fetching REAL Financial Data from APIs
# Your code now pulls live data from the financial world!

import requests
import json
from datetime import datetime

# =============================================
# PART 1: Free Public APIs (no key needed)
# =============================================

# --- Exchange Rates API ---
print("=== 💱 LIVE EXCHANGE RATES ===")
url = "https://open.er-api.com/v6/latest/USD"
try:
    response = requests.get(url)
    data = response.json()  # Automatically parses JSON!

    currencies = ["EUR", "GBP", "JPY", "MXN", "CAD"]
    print(f"Base: USD | Last updated: {data.get('time_last_update_utc', 'N/A')[:16]}")
    for curr in currencies:
        rate = data["rates"].get(curr, "N/A")
        print(f"  USD → {curr}: {rate}")
except Exception as e:
    print(f"Error fetching rates: {e}")

# --- CoinGecko Crypto API (free, no key) ---
print("\n=== 🪙 CRYPTO PRICES ===")
url = "https://api.coingecko.com/api/v3/simple/price"
params = {
    "ids": "bitcoin,ethereum,solana",
    "vs_currencies": "usd",
    "include_24hr_change": "true"
}
try:
    response = requests.get(url, params=params)
    data = response.json()

    for coin, info in data.items():
        price = info.get("usd", 0)
        change = info.get("usd_24h_change", 0)
        direction = "📈" if change > 0 else "📉"
        print(f"  {coin.capitalize():12} ${price:>12,.2f}  {direction} {change:+.2f}%")
except Exception as e:
    print(f"Error fetching crypto: {e}")

# =============================================
# PART 2: Understanding API Response Structure
# =============================================
print("\n=== 🔍 ANATOMY OF AN API RESPONSE ===")
# Let's examine what we actually get back
url = "https://jsonplaceholder.typicode.com/posts/1"
response = requests.get(url)

print(f"Status Code: {response.status_code}")        # 200 = success
print(f"Content Type: {response.headers['Content-Type']}")
print(f"Response is dict? {type(response.json()) == dict}")

data = response.json()
print(f"\nKeys in response: {list(data.keys())}")
print(f"Title: {data['title'][:50]}...")

# =============================================
# PART 3: Error Handling for APIs (production skill!)
# =============================================
print("\n=== ⚠️ ROBUST API CALLS ===")

def safe_api_call(url, params=None, timeout=10):
    """Production-grade API call with error handling."""
    try:
        response = requests.get(url, params=params, timeout=timeout)
        response.raise_for_status()  # Raises error for 4xx/5xx status codes
        return {"success": True, "data": response.json()}
    except requests.exceptions.Timeout:
        return {"success": False, "error": "Request timed out"}
    except requests.exceptions.ConnectionError:
        return {"success": False, "error": "Connection failed"}
    except requests.exceptions.HTTPError as e:
        return {"success": False, "error": f"HTTP error: {e}"}
    except json.JSONDecodeError:
        return {"success": False, "error": "Invalid JSON response"}

# Test with good URL
result = safe_api_call("https://jsonplaceholder.typicode.com/posts/1")
if result["success"]:
    print(f"  ✅ Success: Got post titled '{result['data']['title'][:30]}...'")

# Test with bad URL
result = safe_api_call("https://jsonplaceholder.typicode.com/posts/99999")
print(f"  {'✅' if result['success'] else '❌'} {result.get('error', 'OK')}")

print("\n💡 This safe_api_call pattern is used in EVERY production system.")
print("   Your 1099 ETL Pipeline and future AI projects all use this pattern!")
```

- [ ] Run it. You should see LIVE exchange rates and crypto prices!
- [ ] **This is real data engineering.** Fetching, parsing, error handling — this is what you'll do daily.

**7:30 – 8:30 AM | 🤖 AI Python for Beginners — Start! (60 min)**
- [ ] Go to [deeplearning.ai/courses/ai-python-for-beginners/](https://www.deeplearning.ai/courses/ai-python-for-beginners/)
- [ ] Start **Course 1 of 4: "Basics of AI Python Coding"**
- [ ] Work through as much as possible in 60 minutes
- [ ] **Why this is a PIVOTAL moment in your journey:**
  - Weeks 1-2: You learned Python fundamentals
  - NOW: You see those SAME concepts (variables, lists, loops) used to CONTROL LLMs
  - This is the bridge between "Python programmer" and "AI engineer"
- [ ] **Andrew Ng teaches Python differently here:**
  - Variables aren't just numbers — they're API keys and model parameters
  - Lists aren't just data — they're conversation histories sent to ChatGPT
  - Loops aren't just repetition — they're processing batches of AI responses
  - f-strings aren't just formatting — they're prompt templates

#### Evening Block: 8:00 PM – 10:00 PM (2 hours)

**8:00 – 9:00 PM | 🤖 AI Python for Beginners — Continue (60 min)**
- [ ] Continue working through Course 1
- [ ] Complete as many lessons as possible
- [ ] **Focus on understanding:** How Python connects to LLM APIs
  - You send a prompt (string) → API returns a response (JSON/dict) → you extract the text
  - This is the exact pattern used in ChatGPT, Gemini, Claude APIs

**9:00 – 9:45 PM | SQLZoo — Tutorial 7: More JOIN (45 min)**
- [ ] Start **Tutorial 7: "More JOIN operations"**
- [ ] This tutorial uses a movie database — more complex JOINs
- [ ] Complete at least 8 exercises
- [ ] **New patterns:**
  - Joining 3+ tables together
  - Using JOINs with GROUP BY and aggregate functions
  - Filtering JOINed results with WHERE and HAVING

**9:45 – 10:00 PM | Git Commit**
```bash
git add .
git commit -m "Day 17: Financial APIs live! + AI Python for Beginners started 🤖📈"
git push
```

#### Day 17 Checklist
- [ ] PY4E Ch.13 (Web Services/JSON/APIs) — COMPLETE
- [ ] `day_017_api_finance.py` — live financial data fetching!
- [ ] AI Python for Beginners — Course 1 started (significant progress)
- [ ] SQLZoo Tutorial 7 (More JOIN) — started, 8+ exercises
- [ ] Git commit pushed (Day 17)
- [ ] **Total study time: ~5.5 hours** ✅

---

### 📌 DAY 18 — Sunday, December 7, 2025

**Theme: "Review + AI Python + Career Research"**

#### Evening Block: 7:30 PM – 9:30 PM (2 hours)

**7:30 – 8:30 PM | 🤖 AI Python for Beginners — Continue (60 min)**
- [ ] Continue through the AI Python courses
- [ ] Target: Finish Course 1, start Course 2 ("Automating Tasks with Python")
- [ ] **Key moment to watch for:** When you see `openai.ChatCompletion.create()` or similar API call patterns, connect this to the `requests.get()` pattern you learned yesterday — it's the SAME concept (send request → get response → parse JSON)

**8:30 – 9:00 PM | Career Research: 20 Target Companies (30 min)**
- [ ] Your roadmap says "Research 20 target companies" in Month 1
- [ ] Open a spreadsheet or create `target_companies.md` in your learning_journey repo
- [ ] Research and document 10 companies today (you'll do 10 more next Sunday):

```markdown
| Company | Role Type | Location | Why Target | Job Board Link |
|---------|-----------|----------|------------|----------------|
| Fidelity | Data Analyst | Remote | Finance domain match | careers.fidelity.com |
| Vanguard | Junior Analyst | Remote/PA | Retirement plan expertise | vanguard.com/careers |
| ... | ... | ... | ... | ... |
```

- [ ] **How to find companies:** Search LinkedIn for "Data Analyst" → filter Remote → note the companies that appear frequently
- [ ] **Prioritize:** Companies in financial services, retirement plans, insurance — your domain expertise gives you an edge

**9:00 – 9:30 PM | Week 3 Mid-Review + Git Commit (30 min)**
- [ ] Review what you've accomplished Days 15-18
- [ ] In your notebook: What clicked? What's still fuzzy?
- [ ] Rate yourself 1-10: APIs/JSON understanding, SQL JOINs comfort, AI Python excitement

```bash
git add .
git commit -m "Day 18: AI Python progress + target company research started"
git push
```

#### Day 18 Checklist
- [ ] AI Python for Beginners — Course 1 complete or nearly complete
- [ ] 10 target companies researched and documented
- [ ] Week 3 mid-review written
- [ ] Git commit pushed (Day 18)
- [ ] **Total study time: ~2 hours** ✅

---

### 📌 DAY 19 — Monday, December 8, 2025

**Theme: "Python for Everybody Completion Push + Pandas JOINs"**

#### Morning Block: 4:30 AM – 6:00 AM (1.5 hours)

**4:30 – 5:30 AM | Python for Everybody — Review Ch.11-13 + Start Course 2 (60 min)**
- [ ] If Ch.11-13 aren't fully done, complete them now
- [ ] If they ARE done: Start **Course 2: "Python Data Structures"**
  - Course 2 reviews and deepens: strings, files, lists, dictionaries, tuples
  - Since you've already covered these in Course 1, you can move through Course 2 FASTER (1.5-2x speed on videos)
- [ ] **Note:** Python for Everybody has 5 courses total. Course 1 (Ch.1-5) + Course 2 (Ch.6-10) + Course 3 (Ch.11-13) cover the core. You're approaching the end of the essential Python fundamentals!

**5:30 – 6:00 AM | DataCamp — "Joining Data with pandas" Ch.1 (30 min)**
- [ ] Start **"Joining Data with pandas"** course
- [ ] Complete **Chapter 1: "Data Merging Basics"**
  - `pd.merge()` — the Pandas equivalent of SQL JOIN
  - inner merge, left merge, right merge, outer merge
  - merge on specific columns with `on=` parameter
- [ ] **Connect the dots:** You just learned SQL JOINs in SQLZoo. Now you see the SAME concept in Pandas. Data analysis requires BOTH skills.

#### Evening Block: 8:00 PM – 10:00 PM (2 hours)

**8:00 – 9:00 PM | Practice: Pandas Merging with Financial Data (60 min)**
- [ ] Create `day_019_pandas_joins.py`:

```python
# Day 19: Pandas Merging — The Python Equivalent of SQL JOINs
# Combining multiple datasets to answer business questions

import pandas as pd

# Create sample datasets (simulating real financial data)
# Table 1: Employee info
employees = pd.DataFrame({
    "emp_id": [101, 102, 103, 104, 105],
    "name": ["Alice Chen", "Bob Martinez", "Carol Williams", "David Kim", "Eva Brown"],
    "department_id": [10, 20, 10, 30, 20],
    "hire_date": ["2020-01-15", "2019-06-01", "2021-03-10", "2022-08-20", "2020-11-05"],
})

# Table 2: Department info
departments = pd.DataFrame({
    "dept_id": [10, 20, 30, 40],
    "dept_name": ["Operations", "Finance", "Engineering", "Marketing"],
    "budget": [500000, 750000, 1200000, 300000],
})

# Table 3: 401K contributions
contributions = pd.DataFrame({
    "emp_id": [101, 101, 102, 103, 105, 105],
    "quarter": ["Q1", "Q2", "Q1", "Q1", "Q1", "Q2"],
    "amount": [4500, 4500, 6000, 3000, 5500, 5500],
})

print("=== RAW TABLES ===")
print(f"\nEmployees:\n{employees}")
print(f"\nDepartments:\n{departments}")
print(f"\nContributions:\n{contributions}")

# --- INNER MERGE (like SQL INNER JOIN) ---
# Only employees that have a matching department
print("\n=== INNER MERGE: Employees + Departments ===")
merged = pd.merge(
    employees, departments,
    left_on="department_id", right_on="dept_id",
    how="inner"
)
print(merged[["name", "dept_name", "budget"]])

# --- LEFT MERGE (like SQL LEFT JOIN) ---
# ALL employees, even if no contributions (find who's NOT contributing!)
print("\n=== LEFT MERGE: Who's NOT contributing to 401K? ===")
emp_contrib = pd.merge(employees, contributions, on="emp_id", how="left")
not_contributing = emp_contrib[emp_contrib["amount"].isna()]["name"].unique()
print(f"Employees with NO 401K contributions: {list(not_contributing)}")

# --- AGGREGATE after merge ---
print("\n=== 401K Summary by Department ===")
full_data = pd.merge(employees, departments, left_on="department_id", right_on="dept_id")
full_data = pd.merge(full_data, contributions, on="emp_id", how="left")

dept_summary = full_data.groupby("dept_name").agg(
    employee_count=("name", "nunique"),
    total_contributions=("amount", "sum"),
    avg_contribution=("amount", "mean"),
).round(2)

print(dept_summary)
print(f"\nTotal 401K contributions: ${full_data['amount'].sum():,.2f}")

# --- THIS IS REAL DATA ANALYSIS ---
# You just:
# 1. Merged 3 tables together (like SQL JOINs)
# 2. Found employees with missing data (LEFT JOIN pattern)
# 3. Aggregated by department (like GROUP BY)
# 4. Produced a summary report
# This is EXACTLY what data analysts do at companies like Daybright Financial!
```

- [ ] Run it. Change the data. Add new employees. See how merges work.
- [ ] **Key insight:** This script mirrors REAL retirement plan analysis — the kind of work you'll do as a GenAI Data Analyst, but now with code instead of Excel.

**9:00 – 9:30 PM | 🤖 AI Python for Beginners — Continue (30 min)**
- [ ] Keep progressing through the courses
- [ ] Target: Finish Course 2, start Course 3

**9:30 – 10:00 PM | SQLZoo Tutorial 7 continued + Git Commit (30 min)**
- [ ] Complete more Tutorial 7 exercises
- [ ] Aim to finish Tutorial 7 by end of Week 3

```bash
git add .
git commit -m "Day 19: Pandas merging (JOINs in Python!) + AI Python continued"
git push
```

#### Day 19 Checklist
- [ ] PY4E Course 2 started (or Ch.11-13 catch-up complete)
- [ ] DataCamp "Joining Data with pandas" Ch.1 complete
- [ ] `day_019_pandas_joins.py` — multi-table merging with financial data
- [ ] AI Python for Beginners — continued progress
- [ ] SQLZoo Tutorial 7 — additional exercises
- [ ] Git commit pushed (Day 19)
- [ ] **Total study time: ~3.5 hours** ✅

---

### 📌 DAY 20 — Tuesday, December 9, 2025

**Theme: "AI Python Completion + Kaggle Introduction"**

#### Morning Block: 4:30 AM – 6:00 AM (1.5 hours)

**4:30 – 5:30 AM | 🤖 AI Python for Beginners — Completion Push (60 min)**
- [ ] Work through remaining courses (Course 3: "Working with Your Own Data and Documents" + Course 4: "Extending Python with Packages and APIs")
- [ ] **Course 3 is particularly valuable** — it teaches you to use Python + LLMs to process YOUR OWN data files. This directly connects to your DataVault Analyst project concept.
- [ ] **Course 4** covers packages and APIs — reinforcing what you learned in PY4E Ch.12-13 but now in the context of AI applications.

**5:30 – 6:00 AM | Kaggle — Start "Intro to Python" Micro-Course (30 min)**
- [ ] Go to [kaggle.com/learn/python](https://www.kaggle.com/learn/python)
- [ ] Start the **"Intro to Python"** micro-course
- [ ] Complete Lesson 1: "Hello, Python" + Lesson 2: "Functions and Getting Help"
- [ ] **Why Kaggle NOW?**
  - Kaggle certificates look great on LinkedIn and resumes
  - The platform is where data analysts showcase work
  - Kaggle notebooks become portfolio pieces
  - You already know the Python — this will feel like review, but you get a CERTIFICATE

#### Evening Block: 8:00 PM – 10:00 PM (2 hours)

**8:00 – 9:00 PM | Practice: YOUR First LLM API Script (60 min)**

This is the moment your GenAI-first journey becomes REAL. You're going to write Python that talks to an AI.

- [ ] Create `day_020_first_llm_call.py`:

```python
# Day 20: My First LLM API Call
# The moment my code talks to AI for the first time!
# Using the free Gemini API (Google's LLM — generous free tier)

# SETUP: You need a Gemini API key (free)
# 1. Go to: https://aistudio.google.com/apikey
# 2. Click "Create API Key"
# 3. Copy the key
# 4. Set it as environment variable (see below)

import os

# Option 1: Set API key directly (for learning only — never do this in production!)
# os.environ["GEMINI_API_KEY"] = "your-key-here"

# Option 2: Read from environment variable (production practice)
api_key = os.environ.get("GEMINI_API_KEY")

if not api_key:
    print("⚠️ No API key found!")
    print("To set up:")
    print("  1. Get free key: https://aistudio.google.com/apikey")
    print("  2. Set in terminal: export GEMINI_API_KEY='your-key'")
    print("  3. Or uncomment Option 1 above for quick testing")
    print("\n📝 Showing what the code WOULD do with a key:\n")

    # Demo mode — show the structure without actual API call
    print("=== DEMO: Financial Analysis LLM Call ===")
    print("Prompt: 'Analyze this stock data and give a brief opinion:'")
    print("        'AAPL: +15% YTD, P/E 28, RSI 65'")
    print("")
    print("Response would be: [LLM analysis of the stock data]")
    print("")
    print("=== DEMO: Data Formatting LLM Call ===")
    print("Prompt: 'Convert this messy data to clean CSV format:'")
    print("        'john doe, age 35, salary $85000'")
    print("")
    print("Response would be: name,age,salary")
    print("                   John Doe,35,85000")

else:
    # REAL API CALLS — uncomment when you have your key!
    import requests
    import json

    def ask_gemini(prompt, api_key):
        """Send a prompt to Gemini and return the response."""
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={api_key}"
        headers = {"Content-Type": "application/json"}
        payload = {
            "contents": [{"parts": [{"text": prompt}]}]
        }

        try:
            response = requests.post(url, headers=headers, json=payload, timeout=30)
            response.raise_for_status()
            data = response.json()
            return data["candidates"][0]["content"]["parts"][0]["text"]
        except Exception as e:
            return f"Error: {e}"

    # --- USE CASE 1: Financial Analysis ---
    print("=== 📊 FINANCIAL ANALYSIS ===")
    prompt = """You are a financial analyst assistant. 
    Analyze this stock data briefly (3-4 sentences max):
    - AAPL: +15% YTD, P/E ratio 28, RSI 65
    - Current market conditions: mixed signals
    Give a balanced, educational perspective (not financial advice)."""

    result = ask_gemini(prompt, api_key)
    print(f"Analysis:\n{result}\n")

    # --- USE CASE 2: Data Cleaning ---
    print("=== 🧹 DATA CLEANING WITH AI ===")
    prompt = """Convert this messy data into clean CSV format.
    Return ONLY the CSV, no explanation:
    
    john doe works at acme corp earning 85k started jan 2020
    jane smith - tech industries - $92,000 - march 2019  
    bob jones, freelance, 75000/year, 2021"""

    result = ask_gemini(prompt, api_key)
    print(f"Cleaned data:\n{result}\n")

    # --- USE CASE 3: Code Explanation ---
    print("=== 💻 CODE EXPLANATION ===")
    code_to_explain = "df.groupby('department')['salary'].agg(['mean','median','std']).round(2)"
    prompt = f"Explain this Pandas code in simple terms for a beginner:\n{code_to_explain}"

    result = ask_gemini(prompt, api_key)
    print(f"Explanation:\n{result}")

print("\n" + "=" * 60)
print("🤖 YOU JUST WROTE CODE THAT CONTROLS AN LLM!")
print("This is what separates you from 95% of data analyst candidates.")
print("=" * 60)
```

- [ ] Run it (even in demo mode first, then with API key when ready)
- [ ] **Getting a free Gemini API key takes 2 minutes** — do it!
- [ ] **THIS IS YOUR GenAI-FIRST DIFFERENTIATOR IN ACTION.** Most analyst candidates can't do this.

**9:00 – 9:30 PM | Kaggle — Continue "Intro to Python" (30 min)**
- [ ] Complete Lessons 3-4 of the Kaggle Intro to Python micro-course
- [ ] Aim to complete or nearly complete the entire micro-course

**9:30 – 10:00 PM | HackerRank Challenge Push (30 min)**
- [ ] Do 2 SQL challenges + 2 Python challenges
- [ ] **Target:** Getting close to HackerRank Python Basic Certificate (need ~15 challenges)

```bash
git add .
git commit -m "Day 20: FIRST LLM API CALL! 🤖 + Kaggle Python started + HackerRank push"
git push
```

#### Day 20 Checklist
- [ ] AI Python for Beginners — COMPLETE (or very close) 🎉
- [ ] Kaggle "Intro to Python" — 4+ lessons done
- [ ] `day_020_first_llm_call.py` — your first code that talks to AI!
- [ ] HackerRank: 4 challenges (2 SQL + 2 Python)
- [ ] Git commit pushed (Day 20)
- [ ] **Total study time: ~3.5 hours** ✅

---

### 📌 DAY 21 — Wednesday, December 10, 2025

**Theme: "Week 3 Capstone — API + AI Integration Script"**

#### Morning Block: 4:30 AM – 6:00 AM (1.5 hours)

**4:30 – 5:15 AM | DataCamp — "Joining Data with pandas" Ch.2 (45 min)**
- [ ] Complete **Chapter 2: "Merging Tables With Different Join Types"**
  - LEFT, RIGHT, OUTER joins in Pandas
  - Handling duplicates during merges
  - merge indicator (`_merge` column to track which rows matched)

**5:15 – 6:00 AM | CS50 Week 1 Problem Set — Work Session (45 min)**
- [ ] Work on **CS50 Problem Set 1** (the C programming exercises)
- [ ] At minimum, complete the "Hello" problem and start "Mario"
- [ ] **Don't panic about C:** The syntax is different but the LOGIC is the same as Python
  - C's `printf()` = Python's `print()`
  - C's `int x = 5;` = Python's `x = 5`
  - C's `if (x > 0) { }` = Python's `if x > 0:`
- [ ] Submit what you can. CS50 builds problem-solving muscle that transfers to Python.

#### Evening Block: 8:00 PM – 10:00 PM (2 hours)

**8:00 – 9:30 PM | Week 3 Capstone: "Financial Data API + AI Analyzer" (90 min)**
- [ ] Create `week_03_capstone.py` — The most ambitious script yet:

```python
# Week 3 Capstone: Financial Data API + AI Analyzer
# Combines: APIs, JSON, Pandas, regex, functions, error handling + LLM integration
# Manuel Reyes | Week 3 | Learning Journey

import requests
import pandas as pd
import re
import json
from datetime import datetime

print("=" * 60)
print("📊 WEEK 3 CAPSTONE: Financial Data Pipeline + AI Analysis")
print(f"   Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
print("=" * 60)

# =============================================
# STEP 1: Fetch live data from API
# =============================================
print("\n--- STEP 1: Fetching Live Exchange Rates ---")

def fetch_exchange_rates(base="USD"):
    """Fetch current exchange rates from free API."""
    url = f"https://open.er-api.com/v6/latest/{base}"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"  ⚠️ API Error: {e}")
        return None

rates_data = fetch_exchange_rates()
if rates_data:
    print(f"  ✅ Fetched rates for {len(rates_data['rates'])} currencies")
    print(f"  📅 Last updated: {rates_data.get('time_last_update_utc', 'N/A')[:25]}")

# =============================================
# STEP 2: Process into Pandas DataFrame
# =============================================
print("\n--- STEP 2: Processing into DataFrame ---")

target_currencies = ["EUR", "GBP", "JPY", "MXN", "CAD", "AUD", "CHF", "BRL"]
currency_names = {
    "EUR": "Euro", "GBP": "British Pound", "JPY": "Japanese Yen",
    "MXN": "Mexican Peso", "CAD": "Canadian Dollar", "AUD": "Australian Dollar",
    "CHF": "Swiss Franc", "BRL": "Brazilian Real"
}

if rates_data:
    rows = []
    for curr in target_currencies:
        rate = rates_data["rates"].get(curr)
        if rate:
            rows.append({
                "currency_code": curr,
                "currency_name": currency_names.get(curr, curr),
                "rate_per_usd": rate,
                "usd_per_unit": round(1 / rate, 4),
                "usd_1000_value": round(1000 / rate, 2),
            })

    df = pd.DataFrame(rows)
    print(f"  ✅ Created DataFrame: {df.shape[0]} rows × {df.shape[1]} columns")
    print(f"\n{df.to_string(index=False)}")

    # Analysis
    print(f"\n--- STEP 3: Analysis ---")
    strongest = df.loc[df["usd_per_unit"].idxmax()]
    weakest = df.loc[df["usd_per_unit"].idxmin()]
    print(f"  💪 Strongest vs USD: {strongest['currency_name']} (1 {strongest['currency_code']} = ${strongest['usd_per_unit']:.4f})")
    print(f"  📉 Weakest vs USD: {weakest['currency_name']} (1 {weakest['currency_code']} = ${weakest['usd_per_unit']:.4f})")

# =============================================
# STEP 4: Regex validation on messy input
# =============================================
print(f"\n--- STEP 4: Regex Data Cleaning ---")

messy_transactions = [
    "Transfer $5,000.00 to account 401K-12345 on 12/10/2025",
    "Withdrawal of $12,500.50 from IRA-99887 dated 11/30/2025",
    "Deposit: $750.00 into ROTH-45678 (12/05/2025)",
    "INVALID ENTRY - no amounts here",
    "401K-AB123 bad account format $100.00",
]

def parse_transaction(text):
    """Extract structured data from messy transaction text using regex."""
    amount = re.search(r'\$([\d,]+\.\d{2})', text)
    account = re.search(r'(401K|IRA|ROTH)-\d{5}', text)
    date = re.search(r'(\d{2}/\d{2}/\d{4})', text)
    return {
        "raw_text": text[:50],
        "amount": float(amount.group(1).replace(',', '')) if amount else None,
        "account": account.group(0) if account else None,
        "date": date.group(1) if date else None,
        "valid": all([amount, account, date]),
    }

parsed = [parse_transaction(t) for t in messy_transactions]
parsed_df = pd.DataFrame(parsed)
print(parsed_df.to_string(index=False))

valid_count = parsed_df["valid"].sum()
print(f"\n  ✅ Valid transactions: {valid_count}/{len(parsed)}")
print(f"  ❌ Invalid transactions: {len(parsed) - valid_count}/{len(parsed)}")
if parsed_df["amount"].notna().any():
    print(f"  💰 Total amount (valid): ${parsed_df.loc[parsed_df['valid'], 'amount'].sum():,.2f}")

# =============================================
# SUMMARY
# =============================================
print(f"\n{'=' * 60}")
print("📋 SKILLS DEMONSTRATED IN THIS CAPSTONE:")
print("  ✅ API calls with error handling (requests library)")
print("  ✅ JSON parsing into Python dictionaries")
print("  ✅ Pandas DataFrame creation and analysis")
print("  ✅ Regular expressions for financial data extraction")
print("  ✅ Functions with docstrings and return values")
print("  ✅ String formatting and professional output")
print("  ✅ Data validation and quality checking")
print("  ✅ Finance domain expertise (accounts, transactions)")
print(f"{'=' * 60}")
```

- [ ] Run it. This script shows a DRAMATIC improvement from your Week 1 capstone.
- [ ] **Portfolio impact:** This demonstrates API integration, data processing, regex extraction, and financial domain knowledge — all in one script.

**9:30 – 10:00 PM | Git Commit + Week 3 Reflection (30 min)**
```bash
git add .
git commit -m "Week 3 Capstone: Financial Data API + AI Analyzer - APIs, JOINs, Regex, Pandas 🎉🚀"
git push
```
- [ ] **Week 3 Reflection** in your notebook:
  - Rate yourself 1-10: Python, SQL, Pandas, APIs, AI understanding
  - What was the most exciting moment? (Probably Day 20 — your first LLM call!)
  - What needs more practice?

#### Day 21 Checklist
- [ ] DataCamp "Joining Data with pandas" Ch.2 done
- [ ] CS50 Problem Set 1 — worked on (Hello + start Mario)
- [ ] `week_03_capstone.py` — API + Pandas + Regex + Finance capstone
- [ ] Week 3 reflection written
- [ ] Git commit pushed (Day 21 — **3-week streak!** 🎉)
- [ ] **Total study time: ~3.5 hours** ✅

---

## 📊 WEEK 3 CUMULATIVE PROGRESS

| Metric | Target | Status |
|--------|--------|--------|
| Study hours (Week 3) | ~25 hrs | ~25 hrs ✅ |
| Git commits (total) | 21+ | ✅ |
| PY4E chapters | Ch.11-13 (Regex, Networking, APIs) complete | ✅ |
| DataCamp | "Data Manipulation" done, "Joining Data" started | ✅ |
| SQLZoo | Tutorials 6-7 (JOINs!) — 15+ exercises | ✅ |
| AI Python for Beginners | COMPLETE (4-6 hours) | ✅ |
| Kaggle | "Intro to Python" started | ✅ |
| CS50 | Problem Set 1 in progress | ✅ |
| **NEW concepts** | APIs, JSON, regex, JOINs (SQL+Pandas), LLM API calls, Matplotlib | ✅ |

---

## 🗓 WEEK 4: FIRST VISUALIZATIONS & GOOGLE DA CERT (Dec 11 – Dec 17, 2025)

### Week 4 Goals

By Wednesday night December 17, you will have:

1. ✅ Google Data Analytics Certificate — Course 1 "Foundations" started
2. ✅ DataCamp "Joining Data with pandas" — mostly complete
3. ✅ DataCamp "Introduction to Data Visualization with Matplotlib" — started
4. ✅ DeepLearning.AI "LangChain for LLM Application Development" — COMPLETE
5. ✅ SQLZoo Tutorials 7-8 complete + Tutorial 9 started
6. ✅ Kaggle "Intro to Python" micro-course — COMPLETE + certificate earned
7. ✅ HackerRank Python Basic Certificate earned (or very close)
8. ✅ First data visualization script (charts with Matplotlib)
9. ✅ Your biggest capstone yet — combining ALL 4 weeks of learning
10. ✅ 28+ total GitHub commits (4-week streak, Month 1 complete!)

---

### 📌 DAY 22 — Thursday, December 11, 2025

**Theme: "LangChain + Data Visualization Begins"**

#### Morning Block: 4:30 AM – 6:00 AM (1.5 hours)

**4:30 – 5:30 AM | DeepLearning.AI — LangChain for LLM Application Development (60 min)**
- [ ] Go to [deeplearning.ai/short-courses/langchain-for-llm-application-development/](https://www.deeplearning.ai/short-courses/langchain-for-llm-application-development/)
- [ ] Start watching — taught by **Harrison Chase** (LangChain CEO)
- [ ] Total course is 1-2 hours. Cover first half today.
- [ ] **Key concepts to absorb:**
  - **Chains:** Connect multiple LLM calls together (output of one → input of next)
  - **Memory:** Give your chatbot the ability to remember previous messages
  - **Document Q&A:** Upload documents → ask questions → get answers with sources
  - **Agents:** LLMs that can USE TOOLS (search the web, run code, query databases)
- [ ] **Why LangChain matters for YOUR roadmap:**
  - Your Stage 1 projects (PolicyPulse, DataVault Analyst) will use LangChain concepts
  - LangChain appears in 90%+ of LLM job descriptions
  - Your IBM GenAI Engineering cert (Months 3-5) includes a LangChain capstone
  - This 1-hour course gives you the mental model BEFORE you dive deep later

**5:30 – 6:00 AM | Google Data Analytics Certificate — Start Course 1 (30 min)**
- [ ] Go to Coursera → Search **"Google Data Analytics Professional Certificate"** → Enroll (included in Plus)
- [ ] Start **Course 1: "Foundations: Data, Data, Everywhere"**
- [ ] Watch the first 2-3 videos (introduction + what is data analytics)
- [ ] **This is your FIRST industry-recognized certificate** — it carries weight on resumes and LinkedIn
- [ ] **Speed tip:** You already know some of this from your business ops experience. Watch at 1.5x speed for familiar concepts, normal speed for new ones.

#### Evening Block: 8:00 PM – 10:00 PM (2 hours)

**8:00 – 8:45 PM | Practice: First Matplotlib Visualization (45 min)**
- [ ] Install matplotlib if needed: `pip install matplotlib`
- [ ] Create `day_022_first_charts.py`:

```python
# Day 22: First Data Visualizations with Matplotlib
# Your data now tells VISUAL stories!

import matplotlib.pyplot as plt
import pandas as pd

# --- CHART 1: Line Chart (Stock Price Over Time) ---
days = list(range(1, 21))  # 20 trading days
prices = [150, 152, 148, 155, 158, 156, 160, 162, 159, 165,
          163, 168, 170, 167, 172, 175, 173, 178, 180, 176]

plt.figure(figsize=(10, 5))
plt.plot(days, prices, color='#2196F3', linewidth=2, marker='o', markersize=4)
plt.title('AAPL Stock Price — 20 Trading Days', fontsize=14, fontweight='bold')
plt.xlabel('Trading Day')
plt.ylabel('Price ($)')
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('chart_01_line.png', dpi=150)
plt.close()
print("✅ Chart 1 saved: chart_01_line.png")

# --- CHART 2: Bar Chart (Portfolio Allocation) ---
sectors = ['Technology', 'Finance', 'Healthcare', 'Energy', 'Consumer']
allocations = [35, 25, 20, 12, 8]
colors = ['#2196F3', '#4CAF50', '#FF9800', '#F44336', '#9C27B0']

plt.figure(figsize=(8, 5))
bars = plt.bar(sectors, allocations, color=colors, edgecolor='white', linewidth=1.5)
plt.title('Portfolio Allocation by Sector', fontsize=14, fontweight='bold')
plt.ylabel('Allocation (%)')

# Add value labels on bars
for bar, val in zip(bars, allocations):
    plt.text(bar.get_x() + bar.get_width()/2., bar.get_height() + 0.5,
             f'{val}%', ha='center', va='bottom', fontweight='bold')

plt.tight_layout()
plt.savefig('chart_02_bar.png', dpi=150)
plt.close()
print("✅ Chart 2 saved: chart_02_bar.png")

# --- CHART 3: Multi-line Chart (Comparing Stocks) ---
aapl = [150, 155, 160, 158, 165, 170, 168, 175, 180, 176]
googl = [140, 138, 145, 150, 148, 155, 160, 157, 163, 165]
msft = [370, 375, 380, 378, 385, 390, 388, 395, 400, 397]

# Normalize to starting price (percentage change)
aapl_pct = [(p / aapl[0] - 1) * 100 for p in aapl]
googl_pct = [(p / googl[0] - 1) * 100 for p in googl]
msft_pct = [(p / msft[0] - 1) * 100 for p in msft]

days = list(range(1, 11))

plt.figure(figsize=(10, 5))
plt.plot(days, aapl_pct, label='AAPL', linewidth=2, color='#007AFF')
plt.plot(days, googl_pct, label='GOOGL', linewidth=2, color='#34A853')
plt.plot(days, msft_pct, label='MSFT', linewidth=2, color='#FF6D00')
plt.axhline(y=0, color='gray', linestyle='--', alpha=0.5)
plt.title('Stock Performance Comparison (% Change)', fontsize=14, fontweight='bold')
plt.xlabel('Trading Day')
plt.ylabel('Change from Start (%)')
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('chart_03_comparison.png', dpi=150)
plt.close()
print("✅ Chart 3 saved: chart_03_comparison.png")

print("\n📊 3 charts created! Open the PNG files to see your first visualizations.")
print("💡 Data visualization is a CORE data analyst skill — you just started building it!")
```

- [ ] Run it. Open the PNG files. You just created professional-looking charts with code!
- [ ] **Experiment:** Change colors, add more data points, try `plt.pie()` for a pie chart

**8:45 – 9:30 PM | SQLZoo — Tutorial 8: Using Null + Tutorial 9 start (45 min)**
- [ ] Complete **Tutorial 8: "Using Null"** (handling missing data in SQL)
  - `IS NULL`, `IS NOT NULL`, `COALESCE()`, `CASE WHEN`
  - Critical skill — real data ALWAYS has missing values
- [ ] Start **Tutorial 9: "Self join"** (joining a table to itself)

**9:30 – 10:00 PM | Kaggle — Complete "Intro to Python" (30 min)**
- [ ] Push to finish remaining lessons
- [ ] Take the final exercise/quiz
- [ ] **Earn your Kaggle "Intro to Python" certificate!**
- [ ] Download the certificate → Add to LinkedIn (Licenses & Certifications section)

```bash
git add .
git commit -m "Day 22: First Matplotlib charts! + LangChain started + Kaggle Python near complete"
git push
```

---

### 📌 DAY 23 — Friday, December 12, 2025

**Theme: "LangChain Complete + Google DA Deep Dive"**

#### Morning Block: 4:30 AM – 6:00 AM (1.5 hours)

**4:30 – 5:15 AM | DeepLearning.AI — LangChain Complete (45 min)**
- [ ] Finish the remaining sections of the LangChain course
- [ ] **Key takeaways to write in your notebook:**
  - Chains = Sequential LLM calls (prompt → response → use as next prompt)
  - Memory = ConversationBufferMemory stores chat history
  - Agents = LLMs that decide WHICH tool to use (revolutionary concept)
  - Document Q&A = Load docs → split → embed → retrieve → answer
- [ ] **After completing:** You now have AI awareness of 4 key technologies:
  1. ✅ LLM APIs (Prompt Engineering course)
  2. ✅ Multi-step LLM systems (Building Systems course)
  3. ✅ Python for AI (AI Python for Beginners)
  4. ✅ LangChain framework (this course)
  - This puts you ahead of 95%+ of beginner data analyst candidates!

**5:15 – 6:00 AM | Google DA Certificate — Course 1 continued (45 min)**
- [ ] Continue **Course 1: "Foundations: Data, Data, Everywhere"**
- [ ] Watch Week 1 videos and complete quizzes
- [ ] Topics: Data analytics lifecycle, analytical thinking, tools overview

#### Evening Block: 8:00 PM – 10:00 PM (2 hours)

**8:00 – 8:45 PM | DataCamp — "Joining Data with pandas" Ch.3-4 (45 min)**
- [ ] Complete **Chapter 3: "Advanced Merging and Concatenating"**
  - `pd.concat()` — stacking DataFrames (like appending rows)
  - Verifying merge integrity
- [ ] Start **Chapter 4: "Merging Ordered and Time-Series Data"**
  - `merge_asof()` — merging by nearest time value (critical for financial data!)

**8:45 – 9:30 PM | DataCamp — Start "Introduction to Data Visualization with Matplotlib" (45 min)**
- [ ] Begin this new course
- [ ] Complete **Chapter 1: "Introduction to Matplotlib"**
- [ ] This will formalize and deepen the Matplotlib skills from yesterday's practice script

**9:30 – 10:00 PM | HackerRank — Certificate Push (30 min)**
- [ ] Focus on Python challenges to reach the **Python Basic Certificate**
- [ ] You need to pass the HackerRank Python certification test
- [ ] If ready, take the test! It covers: strings, lists, basic data types, classes basics
- [ ] **This certificate goes on LinkedIn and your resume immediately**

```bash
git add .
git commit -m "Day 23: LangChain complete! Google DA started + Matplotlib DataCamp + HackerRank push"
git push
```

---

### 📌 DAY 24 — Saturday, December 13, 2025

**Theme: "POWER DAY — Visualization Deep Dive + Google DA Push"**

#### Morning Block: 5:00 AM – 8:30 AM (3.5 hours)

**5:00 – 6:30 AM | Google DA Certificate — Course 1 continued (90 min)**
- [ ] Push through Course 1 videos and quizzes
- [ ] Target: Complete Week 1 and start Week 2 of Course 1
- [ ] **Speed strategy:** Your business ops experience means some concepts are review. Use 1.5x speed on familiar material.

**6:30 – 7:30 AM | DataCamp — Matplotlib course Ch.2-3 (60 min)**
- [ ] Complete **Chapter 2: "Plotting Time-Series"** (financial data visualization!)
- [ ] Complete **Chapter 3: "Quantitative Comparisons and Statistical Visualizations"**
  - Bar charts, histograms, box plots, scatter plots
  - These are the charts you'll build in EVERY data analyst job

**7:30 – 8:30 AM | Practice: Advanced Visualization with Real-ish Data (60 min)**
- [ ] Create `day_024_advanced_viz.py`:

```python
# Day 24: Advanced Data Visualization
# Creating charts that tell stories — the core skill of data analysts

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

# Simulate 6 months of retirement plan data (your domain!)
np.random.seed(42)
months = pd.date_range('2025-07-01', periods=6, freq='MS')
month_labels = [m.strftime('%b %Y') for m in months]

data = pd.DataFrame({
    'month': months,
    'distributions': np.random.randint(80, 150, 6),
    'loans': np.random.randint(30, 70, 6),
    'new_enrollments': np.random.randint(20, 50, 6),
    'avg_processing_hours': [4.5, 4.2, 3.8, 3.5, 2.0, 0.5],  # Improving with automation!
})

# --- FIGURE 1: Multi-panel dashboard (2x2 grid) ---
fig, axes = plt.subplots(2, 2, figsize=(14, 10))
fig.suptitle('Retirement Plan Operations Dashboard — H2 2025',
             fontsize=16, fontweight='bold', y=0.98)

# Panel 1: Distribution vs Loan volumes (stacked bar)
ax = axes[0, 0]
x = range(len(month_labels))
ax.bar(x, data['distributions'], label='Distributions', color='#2196F3', alpha=0.8)
ax.bar(x, data['loans'], bottom=data['distributions'], label='Loans', color='#FF9800', alpha=0.8)
ax.set_xticks(x)
ax.set_xticklabels(month_labels, rotation=45, fontsize=8)
ax.set_title('Workflow Volume: Distributions vs Loans')
ax.set_ylabel('Count')
ax.legend(fontsize=8)

# Panel 2: Processing time trend (line with annotation)
ax = axes[0, 1]
ax.plot(month_labels, data['avg_processing_hours'], color='#F44336',
        linewidth=2.5, marker='o', markersize=8)
ax.axhline(y=1.0, color='green', linestyle='--', alpha=0.5, label='Target: 1hr')
ax.set_title('Avg Processing Time (ETL Pipeline Impact)')
ax.set_ylabel('Hours')
ax.set_xticklabels(month_labels, rotation=45, fontsize=8)
ax.annotate('ETL Pipeline\nDeployed!', xy=(4, 2.0),
            fontsize=9, fontweight='bold', color='green',
            arrowprops=dict(arrowstyle='->', color='green'),
            xytext=(2.5, 3.5))
ax.legend(fontsize=8)

# Panel 3: New enrollments (bar)
ax = axes[1, 0]
colors = ['#4CAF50' if v >= 35 else '#FF9800' for v in data['new_enrollments']]
ax.bar(month_labels, data['new_enrollments'], color=colors)
ax.axhline(y=35, color='gray', linestyle='--', alpha=0.5, label='Monthly target')
ax.set_title('New Plan Enrollments')
ax.set_ylabel('Count')
ax.set_xticklabels(month_labels, rotation=45, fontsize=8)
ax.legend(fontsize=8)

# Panel 4: Text summary
ax = axes[1, 1]
ax.axis('off')
total_workflows = data['distributions'].sum() + data['loans'].sum()
avg_dist = data['distributions'].mean()
time_saved = (4.5 - 0.5) * 6 * 4  # hours saved over 6 months (weekly savings * weeks)
summary = (
    f"📊 H2 2025 Summary\n\n"
    f"Total Workflows: {total_workflows:,}\n"
    f"Avg Monthly Distributions: {avg_dist:.0f}\n"
    f"Avg Monthly Loans: {data['loans'].mean():.0f}\n"
    f"New Enrollments: {data['new_enrollments'].sum()}\n\n"
    f"⏱️ ETL Pipeline Impact:\n"
    f"Processing time: 4.5hrs → 0.5hrs\n"
    f"Estimated time saved: ~{time_saved:.0f} hours\n"
    f"Annual savings: ~$15,000+"
)
ax.text(0.1, 0.9, summary, transform=ax.transAxes, fontsize=11,
        verticalalignment='top', fontfamily='monospace',
        bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.3))

plt.tight_layout()
plt.savefig('dashboard_operations.png', dpi=150, bbox_inches='tight')
plt.close()
print("✅ Operations dashboard saved: dashboard_operations.png")
print("📊 This is the kind of dashboard that gets you hired as a data analyst!")
```

- [ ] Run it. Open the dashboard PNG.
- [ ] **This is portfolio-quality work.** It shows: domain expertise, data visualization, business storytelling, AND references your real ETL pipeline.

#### Evening Block: 8:00 PM – 10:00 PM (2 hours)

**8:00 – 8:45 PM | SQLZoo — Tutorial 9: Self Join (45 min)**
- [ ] Continue **Tutorial 9: "Self join"**
- [ ] Self joins are advanced but appear in interviews
- [ ] Complete as many exercises as possible

**8:45 – 9:30 PM | Google DA Certificate — Course 1 push (45 min)**
- [ ] Continue working through Course 1 content
- [ ] Target: Complete Course 1 Week 2

**9:30 – 10:00 PM | Git Commit**
```bash
git add .
git commit -m "Day 24: Operations dashboard visualization! + Google DA + SQL self joins"
git push
```

---

### 📌 DAY 25 — Sunday, December 14, 2025

**Theme: "Career Actions + 10 More Target Companies"**

#### Evening Block: 7:30 PM – 9:30 PM (2 hours)

**7:30 – 8:15 PM | Career Research: Complete 20 Target Companies (45 min)**
- [ ] Research and add 10 more companies to your `target_companies.md`
- [ ] Now you should have 20 companies total
- [ ] **Categorize them:**
  - 8-10 companies in financial services / retirement plans (your strongest domain)
  - 5-6 companies with "AI-first" or "GenAI" in their data analyst job descriptions
  - 4-5 stretch companies (tech companies that value finance domain expertise)

**8:15 – 9:00 PM | LinkedIn Activity (45 min)**
- [ ] Add your Kaggle "Intro to Python" certificate to LinkedIn
- [ ] If you earned HackerRank Python Basic cert, add that too
- [ ] Post a Week 3-4 learning update:
  - "Month 1 of my career transformation is nearly complete! In 4 weeks: learned Python fundamentals, SQL JOINs, built my first API integrations, made my first LLM API call, and created data visualizations. Building in public at [GitHub link]. Next: Google Data Analytics certification and my first portfolio project."
- [ ] Connect with 10 data analysts or AI engineers

**9:00 – 9:30 PM | Week 4 Planning + Git Commit (30 min)**
- [ ] Review Week 4 remaining days
- [ ] Identify your #1 weak area to focus on Mon-Wed
- [ ] Write your top 3 priorities for the final 3 days

```bash
git add .
git commit -m "Day 25: 20 target companies complete + LinkedIn certificates added"
git push
```

---

### 📌 DAY 26 — Monday, December 15, 2025

**Theme: "Pandas Mastery + Google DA Progress"**

#### Morning Block: 4:30 AM – 6:00 AM (1.5 hours)

**4:30 – 5:15 AM | Google DA Certificate — Continue (45 min)**
- [ ] Continue Course 1 — push through Week 3 content
- [ ] Topics: Data types, data tools, spreadsheets basics
- [ ] Watch at accelerated speed where content is familiar

**5:15 – 6:00 AM | DataCamp — Complete "Joining Data with pandas" (45 min)**
- [ ] Complete **Chapter 4** if not already done
- [ ] **Milestone: 4th DataCamp course complete!** 🎉

#### Evening Block: 8:00 PM – 10:00 PM (2 hours)

**8:00 – 9:00 PM | Practice: Complete Data Analysis Pipeline (60 min)**
- [ ] Create `day_026_full_pipeline.py`:
- [ ] Build a script that does the COMPLETE data analysis cycle:
  1. Load data from CSV (or create sample financial data)
  2. Clean it (handle missing values, fix data types)
  3. Merge multiple DataFrames together
  4. Calculate key metrics using groupby
  5. Create a visualization
  6. Print a summary report
- [ ] This exercise combines EVERYTHING: file I/O, Pandas, merging, groupby, Matplotlib, functions

**9:00 – 9:30 PM | Kaggle — Start "Pandas" Micro-Course (30 min)**
- [ ] Go to [kaggle.com/learn/pandas](https://www.kaggle.com/learn/pandas)
- [ ] Start the **"Pandas"** micro-course
- [ ] Complete Lessons 1-2
- [ ] **Another certificate for your collection!**

**9:30 – 10:00 PM | HackerRank — SQL challenges (30 min)**
- [ ] Do 3 SQL challenges (Basic Join section if available)
- [ ] Start working toward **HackerRank SQL Basic Certificate**

```bash
git add .
git commit -m "Day 26: Full data pipeline script + DataCamp Joining complete + Kaggle Pandas started"
git push
```

---

### 📌 DAY 27 — Tuesday, December 16, 2025

**Theme: "Interview SQL Prep + Capstone Preparation"**

#### Morning Block: 4:30 AM – 6:00 AM (1.5 hours)

**4:30 – 5:30 AM | Python for Everybody — Course 2 Progress (60 min)**
- [ ] Continue working through **Course 2: "Python Data Structures"**
- [ ] Since you already know the content from Course 1 + DataCamp, use this as review and reinforcement
- [ ] Watch at 1.5-2x speed. Complete exercises and quizzes.
- [ ] **Goal:** Be well into Course 2 by end of week

**5:30 – 6:00 AM | Kaggle Pandas — Continue (30 min)**
- [ ] Complete Lessons 3-4 of Kaggle Pandas micro-course

#### Evening Block: 8:00 PM – 10:00 PM (2 hours)

**8:00 – 8:45 PM | SQLZoo — Final Review + New Tutorials (45 min)**
- [ ] Complete any remaining exercises in Tutorials 8-9
- [ ] **Quick review:** Can you write these from memory?
  - `SELECT ... FROM ... JOIN ... ON ... WHERE ... GROUP BY ... ORDER BY`
  - `LEFT JOIN` to find missing records
  - `HAVING` to filter after GROUP BY
  - Subqueries in WHERE clause
- [ ] Start **Tutorial 10: "Tutorial Quiz"** (self-assessment)

**8:45 – 9:30 PM | DataCamp — Matplotlib course progress (45 min)**
- [ ] Complete **Chapter 4** of Matplotlib course if not done
- [ ] **Or** start another DataCamp course from the analyst track

**9:30 – 10:00 PM | Capstone Prep + Git Commit (30 min)**
- [ ] Think about what your Week 4 capstone should include
- [ ] Sketch it out on paper: What data? What analysis? What charts? What AI element?

```bash
git add .
git commit -m "Day 27: SQL review + Kaggle Pandas + Matplotlib + capstone prep"
git push
```

---

### 📌 DAY 28 — Wednesday, December 17, 2025

**Theme: "MONTH 1 CAPSTONE — Everything You've Learned in 4 Weeks"**

#### Morning Block: 4:30 AM – 6:00 AM (1.5 hours)

**4:30 – 5:15 AM | Google DA Certificate — Complete Course 1 Week 3-4 (45 min)**
- [ ] Push to complete as much of Course 1 as possible
- [ ] You'll continue this into Month 2, but get through as much as you can

**5:15 – 6:00 AM | Kaggle Pandas — Completion Push (45 min)**
- [ ] Complete remaining lessons of Kaggle Pandas micro-course
- [ ] Earn your **Kaggle "Pandas" certificate!**
- [ ] Add to LinkedIn immediately

#### Evening Block: 8:00 PM – 10:00 PM (2 hours)

**8:00 – 9:30 PM | 🏆 MONTH 1 CAPSTONE: "Financial Portfolio Intelligence Report" (90 min)**
- [ ] Create `month_01_capstone.py` — Your most complete script ever:

```python
# MONTH 1 CAPSTONE: Financial Portfolio Intelligence Report
# Demonstrates ALL skills from 4 weeks of learning
# Manuel Reyes | Month 1 Complete | Learning Journey
#
# SKILLS DEMONSTRATED:
# ✅ Week 1: Variables, conditionals, loops, functions, lists, dicts
# ✅ Week 2: File I/O, Pandas basics, error handling, tuples
# ✅ Week 3: APIs, JSON, regex, SQL JOINs (conceptual), LLM awareness
# ✅ Week 4: Data visualization, merging DataFrames, production patterns

import pandas as pd
import matplotlib.pyplot as plt
import requests
import re
import json
from datetime import datetime

print("=" * 70)
print("📊 MONTH 1 CAPSTONE: Financial Portfolio Intelligence Report")
print(f"   Manuel Reyes | Generated: {datetime.now().strftime('%B %d, %Y at %I:%M %p')}")
print("=" * 70)

# =============================================
# DATA LAYER: Create realistic portfolio data
# =============================================
holdings = pd.DataFrame({
    "ticker": ["AAPL", "GOOGL", "MSFT", "NVDA", "JPM", "V", "JNJ"],
    "shares": [50, 30, 40, 25, 60, 45, 35],
    "avg_cost": [145.00, 135.00, 365.00, 420.00, 170.00, 250.00, 155.00],
    "sector": ["Tech", "Tech", "Tech", "Tech", "Finance", "Finance", "Healthcare"],
})

current_prices = pd.DataFrame({
    "ticker": ["AAPL", "GOOGL", "MSFT", "NVDA", "JPM", "V", "JNJ"],
    "current_price": [178.00, 158.00, 395.00, 520.00, 195.00, 275.00, 148.00],
    "pe_ratio": [28.5, 22.1, 34.2, 65.3, 11.8, 30.5, 15.2],
    "rsi": [62, 55, 71, 78, 45, 58, 38],
})

# =============================================
# ANALYSIS LAYER: Merge & calculate
# =============================================
print("\n📋 STEP 1: Merging holdings with market data...")
portfolio = pd.merge(holdings, current_prices, on="ticker")

portfolio["market_value"] = portfolio["current_price"] * portfolio["shares"]
portfolio["cost_basis"] = portfolio["avg_cost"] * portfolio["shares"]
portfolio["gain_loss"] = portfolio["market_value"] - portfolio["cost_basis"]
portfolio["return_pct"] = ((portfolio["current_price"] - portfolio["avg_cost"]) / portfolio["avg_cost"]) * 100
portfolio["weight"] = (portfolio["market_value"] / portfolio["market_value"].sum()) * 100

# Signal classification using conditionals
def classify_signal(row):
    """Classify stock signal based on RSI and return."""
    if row["rsi"] > 70:
        return "⚠️ OVERBOUGHT"
    elif row["rsi"] < 30:
        return "🟢 OVERSOLD"
    elif row["return_pct"] > 20:
        return "📈 STRONG"
    elif row["return_pct"] < 0:
        return "📉 UNDERWATER"
    else:
        return "✅ HOLD"

portfolio["signal"] = portfolio.apply(classify_signal, axis=1)

# Display portfolio
print("\n📊 PORTFOLIO OVERVIEW:")
display_cols = ["ticker", "shares", "current_price", "market_value", "gain_loss", "return_pct", "signal"]
for _, row in portfolio.iterrows():
    print(f"  {row['ticker']:5} | {row['shares']:3} shares | "
          f"${row['current_price']:>8.2f} | "
          f"Value: ${row['market_value']:>10,.2f} | "
          f"G/L: ${row['gain_loss']:>+10,.2f} ({row['return_pct']:>+6.1f}%) | "
          f"{row['signal']}")

# =============================================
# SECTOR ANALYSIS (GroupBy — like SQL GROUP BY)
# =============================================
print("\n📊 SECTOR ANALYSIS:")
sector_summary = portfolio.groupby("sector").agg(
    positions=("ticker", "count"),
    total_value=("market_value", "sum"),
    total_gain=("gain_loss", "sum"),
    avg_return=("return_pct", "mean"),
    avg_pe=("pe_ratio", "mean"),
).round(2)

for sector, row in sector_summary.iterrows():
    print(f"  {sector:12} | {row['positions']} positions | "
          f"Value: ${row['total_value']:>12,.2f} | "
          f"Gain: ${row['total_gain']:>+10,.2f} | "
          f"Avg Return: {row['avg_return']:>+6.1f}%")

# =============================================
# API INTEGRATION: Live exchange rates
# =============================================
print("\n🌍 LIVE EXCHANGE RATE CONTEXT:")
try:
    response = requests.get("https://open.er-api.com/v6/latest/USD", timeout=10)
    rates = response.json().get("rates", {})
    total_value_usd = portfolio["market_value"].sum()
    print(f"  Portfolio in USD: ${total_value_usd:>12,.2f}")
    for curr in ["EUR", "GBP", "JPY"]:
        converted = total_value_usd * rates.get(curr, 0)
        print(f"  Portfolio in {curr}: {converted:>15,.2f}")
except Exception as e:
    print(f"  ⚠️ Could not fetch rates: {e}")

# =============================================
# REGEX: Parse transaction log
# =============================================
print("\n📝 TRANSACTION LOG PARSING (Regex):")
transactions = [
    "BUY 50 shares AAPL @ $145.00 on 03/15/2025",
    "BUY 30 shares GOOGL @ $135.00 on 04/20/2025",
    "SELL 10 shares MSFT @ $395.00 on 11/01/2025",
]

for txn in transactions:
    action = re.search(r'(BUY|SELL)', txn)
    shares = re.search(r'(\d+) shares', txn)
    ticker_match = re.search(r'shares (\w+)', txn)
    price = re.search(r'\$([\d,.]+)', txn)
    date = re.search(r'(\d{2}/\d{2}/\d{4})', txn)

    if all([action, shares, ticker_match, price, date]):
        print(f"  {action.group(1):4} | {shares.group(1):3} x {ticker_match.group(1):5} | "
              f"${price.group(1):>8} | {date.group(1)}")

# =============================================
# VISUALIZATION: Multi-panel dashboard
# =============================================
print("\n📈 Generating dashboard...")

fig, axes = plt.subplots(2, 2, figsize=(14, 10))
fig.suptitle('Portfolio Intelligence Dashboard — Month 1 Capstone',
             fontsize=16, fontweight='bold')

# Chart 1: Holdings by value (horizontal bar)
ax = axes[0, 0]
sorted_portfolio = portfolio.sort_values("market_value")
colors = ['#4CAF50' if gl > 0 else '#F44336' for gl in sorted_portfolio["gain_loss"]]
ax.barh(sorted_portfolio["ticker"], sorted_portfolio["market_value"], color=colors)
ax.set_title('Holdings by Market Value')
ax.set_xlabel('Value ($)')

# Chart 2: Sector allocation (pie)
ax = axes[0, 1]
sector_values = portfolio.groupby("sector")["market_value"].sum()
ax.pie(sector_values, labels=sector_values.index, autopct='%1.1f%%',
       colors=['#2196F3', '#4CAF50', '#FF9800'])
ax.set_title('Sector Allocation')

# Chart 3: Return by stock (bar)
ax = axes[1, 0]
colors = ['#4CAF50' if r > 0 else '#F44336' for r in portfolio["return_pct"]]
ax.bar(portfolio["ticker"], portfolio["return_pct"], color=colors)
ax.axhline(y=0, color='black', linewidth=0.5)
ax.set_title('Return by Stock (%)')
ax.set_ylabel('Return %')

# Chart 4: RSI Signals (scatter)
ax = axes[1, 1]
ax.scatter(portfolio["pe_ratio"], portfolio["rsi"], s=portfolio["weight"]*20,
           c=portfolio["return_pct"], cmap='RdYlGn', edgecolors='black', alpha=0.8)
ax.axhline(y=70, color='red', linestyle='--', alpha=0.5, label='Overbought (70)')
ax.axhline(y=30, color='green', linestyle='--', alpha=0.5, label='Oversold (30)')
for _, row in portfolio.iterrows():
    ax.annotate(row["ticker"], (row["pe_ratio"], row["rsi"]), fontsize=8, fontweight='bold')
ax.set_title('RSI vs P/E Ratio (size = portfolio weight)')
ax.set_xlabel('P/E Ratio')
ax.set_ylabel('RSI')
ax.legend(fontsize=8)

plt.tight_layout()
plt.savefig('month_01_capstone_dashboard.png', dpi=150, bbox_inches='tight')
plt.close()
print("  ✅ Dashboard saved: month_01_capstone_dashboard.png")

# =============================================
# FINAL SUMMARY
# =============================================
total_value = portfolio["market_value"].sum()
total_gain = portfolio["gain_loss"].sum()
total_cost = portfolio["cost_basis"].sum()

print(f"\n{'=' * 70}")
print(f"💼 PORTFOLIO SUMMARY")
print(f"{'=' * 70}")
print(f"  Total Market Value:  ${total_value:>12,.2f}")
print(f"  Total Cost Basis:    ${total_cost:>12,.2f}")
print(f"  Total Gain/Loss:     ${total_gain:>+12,.2f}")
print(f"  Portfolio Return:    {(total_gain/total_cost)*100:>+11.1f}%")
print(f"  Positions:           {len(portfolio)}")
print(f"  Winners:             {(portfolio['gain_loss'] > 0).sum()}")
print(f"  Losers:              {(portfolio['gain_loss'] < 0).sum()}")
print(f"\n{'=' * 70}")
print(f"🎯 MONTH 1 SKILLS DEMONSTRATED:")
print(f"  ✅ Python: functions, loops, conditionals, error handling, f-strings")
print(f"  ✅ Pandas: DataFrames, merging, groupby, apply, sorting")
print(f"  ✅ APIs: Live data fetching with requests library")
print(f"  ✅ Regex: Pattern extraction from unstructured text")
print(f"  ✅ Matplotlib: Multi-panel dashboard with 4 chart types")
print(f"  ✅ Finance: Portfolio analysis, RSI, P/E, sector allocation")
print(f"  ✅ Production: Error handling, clean output, documentation")
print(f"{'=' * 70}")
```

- [ ] Run it. Take a screenshot of the output AND the dashboard PNG.
- [ ] **This capstone is RECRUITER-READY.** It shows everything you've learned in 4 weeks.

**9:30 – 10:00 PM | Final Git Commit + Month 1 Reflection (30 min)**
```bash
git add .
git commit -m "🏆 MONTH 1 CAPSTONE: Portfolio Intelligence Report - 4 weeks complete! 🎉🚀"
git push
```

- [ ] **Month 1 Reflection** in your notebook:
  - Rate yourself 1-10 on: Python, SQL, Pandas, APIs, Visualization, AI awareness
  - Compare to Day 1 ratings — you'll be amazed at the progress
  - What's your strongest skill? Weakest?
  - Is the schedule sustainable? Adjustments needed?
  - **Write your "Month 2 Declaration":** One sentence on what you'll achieve

---

## 🏆 4-WEEK CUMULATIVE METRICS

### By December 17, 2025 — Month 1 Complete!

| Category | Metric | Target |
|----------|--------|--------|
| **Study Hours** | Total (4 weeks) | ~95-100 hours |
| **GitHub** | Total commits | 28+ |
| **GitHub** | Contribution streak | 28 days |
| **Python Scripts** | Original files written | 20+ |
| **Python** | PY4E Progress | Course 1 complete, Course 2 in progress |
| **DataCamp** | Courses completed | 4 complete + 1-2 in progress |
| **SQL** | SQLZoo tutorials | Tutorials 0-9 (70+ exercises) |
| **SQL** | HackerRank SQL | 15+ challenges |
| **Kaggle** | Certificates earned | 2 (Intro to Python + Pandas) |
| **HackerRank** | Certificates earned | Python Basic (target) |
| **AI Awareness** | Courses completed | 5 (Prompt Eng, Building Systems, AI Python, LangChain + 1 partial) |
| **Google DA** | Progress | Course 1 in progress |
| **CS50** | Progress | Week 0 done, Week 1 PS done, Week 2 started |
| **LinkedIn** | Certificates posted | 2-3 |
| **Career** | Target companies | 20 researched |
| **Visualization** | Charts created | 10+ (including 2 dashboards) |
| **Concepts Mastered** | Full list | Variables, types, conditionals, loops, functions, lists, dicts, tuples, file I/O, regex, HTTP, APIs, JSON, Pandas (merge/groupby/viz), SQL JOINs, Matplotlib, LLM API calls |

---

## 🔧 TROUBLESHOOTING GUIDE: WEEK 3-4 SPECIFIC

### "My API call returned an error"
- **Status 401/403:** API key is wrong or expired. Regenerate it.
- **Status 429:** Too many requests. Wait 60 seconds and try again.
- **Status 500:** Server error (not your fault). Try again later.
- **ConnectionError:** Check your internet connection. Try `requests.get("https://google.com")` to verify.
- **JSONDecodeError:** The response isn't JSON. Print `response.text` to see what you actually got.

### "My Matplotlib chart looks wrong"
- **Blank chart:** Make sure you have `plt.show()` or `plt.savefig()` at the end
- **Labels overlapping:** Add `plt.tight_layout()` before save/show
- **Colors wrong:** Use hex codes like `'#2196F3'` for precise colors
- **Text too small:** Add `fontsize=12` parameter to labels and titles

### "SQL JOINs are confusing"
- Think of it as VLOOKUP: "I have employee_id in this table and I want the department_name from THAT table"
- Draw Venn diagrams: INNER = overlap only, LEFT = all of left + matching right
- Practice on paper before writing SQL
- SQLZoo's JOIN tutorial is hard for EVERYONE. If you're getting 60% right, you're on track.

### "I can't keep up with all the platforms"
- **Priority order for Week 3-4:** (1) Practice scripts (your own code), (2) DataCamp, (3) PY4E videos, (4) SQLZoo, (5) Kaggle, (6) Google DA, (7) HackerRank
- DataCamp and your own scripts build skills fastest. If short on time, cut Google DA first (it runs for months).

---

## 🔮 WHAT COMES NEXT: WEEK 5-6 PREVIEW

**Week 5-6 (Dec 18-31):** Holiday season — slightly lighter schedule but still productive:
- Google DA Certificate Course 1 completion + Course 2 start
- Python for Everybody Course 2 completion
- MODE Analytics SQL Tutorial begins (business analytics SQL)
- DataCamp SQL track introduction
- Start planning your FIRST PORTFOLIO PROJECT: "Financial Data Analysis Dashboard"
- CS50 Week 2-3 progress

**Month 2 Launch (January 2026):**
- First portfolio project BUILD begins
- Pandas deep dive (8 hrs/week)
- Data visualization mastery (5 hrs/week)
- Statistics basics start (6 hrs/week)
- Upwork profile creation
- Google DA Certificate acceleration

---

## 💪 MONTH 1 CELEBRATION

Four weeks ago, you couldn't write `print("Hello")`. Today you've:

- Built scripts that fetch live financial data from APIs
- Written your first code that controls an AI model
- Created multi-panel dashboards with Matplotlib
- Learned SQL JOINs — the #1 interview topic for data analysts
- Extracted patterns from messy data with regex
- Merged multiple datasets with Pandas
- Started your first industry certificate (Google DA)
- Earned certificates on Kaggle and HackerRank
- Committed code EVERY SINGLE DAY for 28 days

You're not "learning to code" anymore. **You're a programmer who builds things.** Month 2 is where the real magic starts — your first portfolio project.

---

*Document created: December 2025*  
*Aligned to: GenAI-First Career Roadmap v8.3*  
*Previous: Weeks 1-2 Activation Plan (Nov 20 – Dec 3)*  
*Next activation plan: Weeks 5-6 (December 18-31, 2025)*
