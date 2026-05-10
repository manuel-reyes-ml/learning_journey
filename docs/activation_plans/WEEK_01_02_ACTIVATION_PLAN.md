# 🚀 WEEKS 1-2 MASTER ACTIVATION PLAN
## GenAI-First Career Transformation | Starting Thursday, November 20, 2025

**Document Version:** 1.0  
**Covers:** November 20, 2025 – December 3, 2025  
**Aligned To:** Career Roadmap v8.3 — Stage 1: GenAI-First Data Analyst & AI Engineer  
**Weekly Hours:** 25 hours/week  
**Your Level:** Complete Beginner in Tech (15+ years business ops, 6 years trading)

---

## 📋 TABLE OF CONTENTS

1. [Before You Start: Critical Context](#-before-you-start-critical-context)
2. [Pre-Day 1 Checklist (Do This BEFORE Nov 20)](#-pre-day-1-checklist-do-this-before-nov-20)
3. [Your Weekly Schedule Template](#-your-weekly-schedule-template)
4. [WEEK 1: Foundation & First Code (Nov 20–26)](#-week-1-foundation--first-code-nov-20--nov-26-2025)
5. [WEEK 2: Build Momentum (Nov 27–Dec 3)](#-week-2-build-momentum-nov-27--dec-3-2025)
6. [2-Week Success Metrics](#-2-week-success-metrics)
7. [Troubleshooting Guide](#-troubleshooting-guide)
8. [What Comes Next: Week 3-4 Preview](#-what-comes-next-week-3-4-preview)

---

## 🧠 BEFORE YOU START: CRITICAL CONTEXT

### Why These 2 Weeks Matter

These first 14 days are about building **three things simultaneously:**

1. **Your Development Environment** — The workspace where you'll spend 5,000+ hours over 37 months
2. **Your Learning Habits** — The daily rhythm of morning theory + evening practice that becomes automatic
3. **Your First Technical Skills** — Python fundamentals + SQL basics + AI awareness that compound exponentially

### The "Beginner's Advantage" Mindset

You're starting from zero in tech, but you bring **massive advantages** most CS students don't have:

- **15+ years** managing real business data (you understand what data *means*)
- **6 years** of trading (you know financial markets, risk, and pattern recognition)
- **Production mindset** from managing operations (deadlines, accuracy, accountability)
- **Domain expertise** in retirement plans and financial services (companies pay premium for this)

These 2 weeks are NOT about "catching up" — they're about **laying foundations that leverage your unique strengths**.

### What "Complete Beginner" Actually Means for Your Plan

Since you're starting with no prior programming experience, every instruction below is written assuming:

- You've never opened a terminal/command prompt before
- You've never written a line of code
- You've never used Git or GitHub
- You've never installed developer tools
- You ARE comfortable with computers, Excel, and web browsing (which you are)

Every step includes the **exact commands to type**, **what you should see on screen**, and **what to do if something goes wrong**.

---

## ✅ PRE-DAY 1 CHECKLIST (Do This BEFORE Nov 20)

**Time needed:** ~2-3 hours on November 18 or 19 (evening is fine)  
**Why before Day 1:** You don't want to waste your first precious morning session installing software. Show up ready to CODE.

### Hardware Check

- [ ] **Computer:** Windows 10/11 or Mac (either works; this plan covers both)
- [ ] **RAM:** At least 8GB (check: Windows → Task Manager → Performance tab; Mac → Apple Menu → About This Mac)
- [ ] **Storage:** At least 20GB free space
- [ ] **Internet:** Stable connection (you'll stream video courses and download tools)
- [ ] **Second monitor (optional but recommended):** Course video on one screen, code on the other

### Account Creation (Do ALL of these — takes ~30 minutes)

- [ ] **GitHub account** → Go to [github.com](https://github.com) → Sign up
  - Username recommendation: `firstname-lastname-ml` (example: `manuel-reyes-ml`)
  - This becomes your professional portfolio URL — choose carefully!
  - Use your personal email (not work email)
  - Choose the FREE plan

- [ ] **Coursera account** → Go to [coursera.org](https://coursera.org) → Sign up
  - Do NOT subscribe to Coursera Plus yet (wait until Day 1 to start your billing cycle)
  - Just create the account

- [ ] **DataCamp account** → Go to [datacamp.com](https://datacamp.com) → Sign up
  - Do NOT subscribe yet (wait until Day 1)
  - Just create the account

- [ ] **edX account** → Go to [edx.org](https://edx.org) → Sign up
  - For CS50 (Harvard's Introduction to Computer Science)
  - Free account is fine

- [ ] **DeepLearning.AI account** → Go to [deeplearning.ai](https://www.deeplearning.ai) → Sign up
  - For the free short courses (ChatGPT Prompt Engineering, etc.)
  - Free account

- [ ] **Anthropic Console account** → Go to [console.anthropic.com](https://console.anthropic.com) → Sign up ⭐ v8.3
  - Anthropic SDK is the **primary provider** for PolicyPulse + AFC per Roadmap v8.3
  - Sign up is free; you'll add billing in the API Keys section below
  - Used for: RAG synthesis (PolicyPulse), financial reasoning (AFC), agent patterns (Stage 4)

- [ ] **Google AI Studio account** → Go to [aistudio.google.com](https://aistudio.google.com) → Sign in with Google ⭐ v8.3
  - For Gemini API access (embeddings + Gemini Vision multimodal)
  - Used for: Embeddings in PolicyPulse (semantic search), Gemini Vision in FormSense (form reading)
  - Free tier is generous and covers all of Stage 1 — no billing needed

- [ ] **HackerRank account** → Go to [hackerrank.com](https://hackerrank.com) → Sign up
  - For SQL and Python practice challenges
  - Free account

- [ ] **LinkedIn account** → Make sure your existing profile is accessible
  - You'll update it in Week 2 (don't change anything yet)

### Software Installation (Do ALL of these — takes ~1-2 hours)

#### Step 1: Install Python 3.11+

**Windows:**
1. Go to [python.org/downloads](https://python.org/downloads)
2. Click the big yellow "Download Python 3.12.x" button
3. Run the installer
4. **CRITICAL:** Check the box that says ✅ "Add Python to PATH" (bottom of installer window)
5. Click "Install Now"
6. Verify: Open Command Prompt (search "cmd" in Start menu), type: `python --version`
7. You should see: `Python 3.12.x` — if you see this, you're good!

**Mac:**
1. Go to [python.org/downloads](https://python.org/downloads)
2. Download the macOS installer
3. Run the .pkg file, click through the steps
4. Verify: Open Terminal (search "Terminal" in Spotlight), type: `python3 --version`
5. You should see: `Python 3.12.x`

**If something goes wrong:** Google "install Python 3.12 [your operating system] 2025" — there are hundreds of video tutorials. Don't spend more than 20 minutes; ask ChatGPT for help if stuck.

#### Step 2: Install VS Code (Free)

1. Go to [code.visualstudio.com](https://code.visualstudio.com)
2. Download for your operating system
3. Run the installer (accept all defaults)
4. Open VS Code after installation
5. Install the **Python extension:** Click the Extensions icon (4 squares) on the left sidebar → Search "Python" → Install the one by Microsoft (it has millions of downloads)
6. Install the **Jupyter extension:** Same process, search "Jupyter" → Install the one by Microsoft

#### Step 3: Install Docker Desktop (Free) ⭐ v8.2/v8.3 STANDARD

Every project in your portfolio ships with a Dockerfile — Docker Desktop is required to build and test containers locally.

**Windows:**
1. Go to [docker.com/products/docker-desktop](https://www.docker.com/products/docker-desktop/)
2. Download Docker Desktop for Windows
3. Run the installer (it may prompt to enable WSL 2 — accept and let it install)
4. After install, restart your computer
5. Open Docker Desktop → accept the terms → it should start automatically
6. Verify: Open Command Prompt, type: `docker --version` → you should see something like `Docker version 24.x.x`

**Mac:**
1. Same URL → download for Mac (choose Apple Silicon or Intel based on your Mac)
2. Drag Docker.app to Applications
3. Open Docker → grant permissions when asked
4. Verify: Open Terminal, type: `docker --version`

**Don't worry about learning Docker now** — Month 5 has the Docker for Beginners course. You're just installing it so it's ready when you need it.

#### Step 4: Install Cursor AI IDE ($20/month — your PRIMARY editor)

1. Go to [cursor.com](https://cursor.com)
2. Download for your operating system
3. Run the installer
4. Open Cursor → It will ask you to sign in → Create account
5. Subscribe to Pro ($20/month) — this is your **#1 learning accelerator tool**
6. Cursor looks almost identical to VS Code (it's built on the same foundation) but has AI built in

**Why pay $20/month as a beginner?** Cursor's AI will:
- Explain any code you don't understand (highlight code → press Ctrl+K → ask "explain this")
- Help you debug errors (paste the error → it explains what went wrong in plain English)
- Auto-complete code as you type (learning by seeing patterns)
- Answer questions about Python/SQL right inside your editor

#### Step 5: Install Claude Desktop (Free) ⭐ v8.3

Claude Desktop is Anthropic's free desktop app. You'll use it later (Week 11-12) to test PolicyPulse's FastMCP server integration — recruiter-visible "MCP server in production" demonstration.

**Windows / Mac:**
1. Go to [claude.ai/download](https://claude.ai/download)
2. Download for your OS
3. Install + sign in with the Anthropic account you created above
4. Free tier is fine — you're using it as an MCP client, not for chat usage

**You won't use this on Day 1** — it's part of the v8.3 setup foundation that pays off in Week 11-12 when PolicyPulse exposes its FastMCP server.

#### Step 6: Install Git (Version Control)

**Windows:**
1. Go to [git-scm.com/download/win](https://git-scm.com/download/win)
2. Download and run the installer
3. Accept ALL default options (just click Next → Next → Next → Install)
4. Verify: Open Command Prompt, type: `git --version`
5. You should see: `git version 2.x.x`

**Mac:**
1. Open Terminal
2. Type: `git --version`
3. If not installed, it will prompt you to install Xcode Command Line Tools → Click "Install"
4. Wait for installation → Verify with `git --version` again

#### Step 7: Configure Git with Your Identity

Open your terminal (Command Prompt on Windows, Terminal on Mac) and type these two commands (replace with YOUR info):

```bash
git config --global user.name "Manuel Reyes"
git config --global user.email "your-email@gmail.com"
```

This tells Git who you are for every code commit you make.

#### Step 8: Install GitHub CLI (Free) ⭐ Important

GitHub CLI (`gh`) accelerates your "no vibe coding" workflow — manual PR creation, branch management, issue tracking from terminal.

**Windows:**
1. Go to [cli.github.com](https://cli.github.com/) → Download for Windows
2. Run installer with defaults
3. Verify: `gh --version`
4. Authenticate: `gh auth login` → choose GitHub.com → HTTPS → Yes (auth git) → Login with web browser

**Mac:**
1. Install Homebrew first if you don't have it: [brew.sh](https://brew.sh)
2. Run: `brew install gh`
3. Authenticate: `gh auth login` (same flow as Windows)

**Why this matters:** Your Cursor 8-step development cycle uses `gh issue create`, `gh pr create`, etc. Without `gh`, you'd click through GitHub's web UI for every action.

#### Step 9: Create Your Project Folder Structure

Open your terminal and type these commands one by one:

**Windows (Command Prompt):**
```bash
mkdir C:\Users\%USERNAME%\coding
mkdir C:\Users\%USERNAME%\coding\learning_journey
mkdir C:\Users\%USERNAME%\coding\projects
```

**Mac (Terminal):**
```bash
mkdir -p ~/coding/learning_journey
mkdir -p ~/coding/projects
```

This creates an organized workspace:
```
coding/
├── learning_journey/    ← Course exercises, notes, experiments
└── projects/            ← Portfolio projects (separate repos later)
```

**Then create the GitHub remote:**
1. Go to [github.com/new](https://github.com/new)
2. Repository name: `learning_journey`
3. Description: "37-month GenAI-First career transformation — public learning record"
4. **Public** (recruiter-visible)
5. Initialize with README — UNCHECK (you'll create your own)
6. Click **Create repository**

You'll connect your local folder to this remote on Day 1 (Day 1 instructions handle the `git remote add origin` step).

### API Key Setup (Do BEFORE Day 1) ⭐ v8.3

**Why before Day 1:** You won't use these on Day 1, but having them ready means zero blockers in Week 7-8 (DataVault) and Week 11-12 (PolicyPulse). Get them now while you're in setup mode.

#### Step 1: Get Your Anthropic API Key (PRIMARY PROVIDER per v8.3)

1. Log in to [console.anthropic.com](https://console.anthropic.com) (account created above)
2. Click your initials (top-right) → **API Keys** → **Create Key**
3. Name it: `stage1-portfolio-development`
4. **COPY IT IMMEDIATELY** — you can't view it again after closing
5. Save in a password manager (or temporarily in `~/.api-keys-backup.txt` outside any git repo)
6. **Add billing**: Go to **Plans & Billing** → add ~$10 in credits to start
7. **Set spending limits**: Set monthly cap to $20 to avoid surprises

**Cost expectations at Stage 1 volume:** ~$5-15/month thanks to Anthropic's prompt caching (90% discount on cached tokens). This is your highest-value AI investment.

#### Step 2: Get Your Gemini API Key (Embeddings + Vision)

1. Log in to [aistudio.google.com](https://aistudio.google.com)
2. Click **Get API Key** (top-left) → **Create API Key**
3. Choose: **Create API key in new project**
4. **COPY IT IMMEDIATELY**
5. Save alongside your Anthropic key

**No billing needed** — Gemini's free tier (15 requests/min, 1500/day) covers all of Stage 1.

#### Step 3: Securely Store Your Keys

Create `~/.env-keys` (or equivalent on Windows: `C:\Users\<you>\.env-keys`) with:

```
ANTHROPIC_API_KEY=sk-ant-xxxxx
GEMINI_API_KEY=AIzaXXXX
```

**CRITICAL:** This file should NEVER be committed to git. Each project will have its own `.env.example` (which IS committed) and `.env` (which is in `.gitignore`).

**Don't worry about how to use these on Day 1** — you'll set up your first project's `.env` in Week 7 when DataVault starts integrating LLMs.

> **📌 Note for catch-up scenarios:** If you're picking up this plan after some self-directed learning (e.g., CS50 in C and Python — common detour for the "no vibe coding" mindset), some software/accounts above may already exist. Confirm each line in the checklist; skip what's done. The v8.3 AI Provider Setup (Anthropic + Gemini API keys, Claude Desktop) is the most likely gap for catch-up learners.

### Subscriptions to Activate on Day 1 (November 20)

Have your payment method ready. You will activate these on the MORNING of Day 1:

- [ ] **Coursera Plus** — $59/month (gives access to ALL courses in your roadmap)
- [ ] **DataCamp** — $25/month (interactive Python/SQL practice)
- [ ] **Cursor Pro** — $20/month (AI-powered code editor)
- [ ] **Anthropic API credits** — ~$10 initial (~$5-15/month at Stage 1 volume per v8.3)
- [ ] **Total Day 1 cost:** ~$110-120/month (subscriptions $104 + API usage $5-15)
- [ ] **Free additions per v8.3:** Gemini API key, Claude Desktop, Docker Desktop, GitHub CLI ($0 added)

---

## 📅 YOUR WEEKLY SCHEDULE TEMPLATE

This is your schedule for the next 37 months. Memorize it.

| Day | Time Block | Hours | Focus |
|-----|-----------|-------|-------|
| **Monday–Friday** | 4:30 AM – 6:00 AM | 1.5 hrs | **MORNING:** Video courses, reading, theory (fresh mind) |
| **Monday–Friday** | 8:00 PM – 10:00 PM | 2.0 hrs | **EVENING:** Hands-on coding, practice, projects |
| **Saturday** | 5:00 AM – 8:30 AM | 3.5 hrs | **DEEP WORK:** Complex projects, difficult concepts |
| **Saturday** | 8:00 PM – 10:00 PM | 2.0 hrs | **EVENING:** Continue projects, review week |
| **Sunday** | 7:30 PM – 9:30 PM | 2.0 hrs | **PLANNING:** Week review, LinkedIn, plan next week |
| | | **25 hrs/week** | |

**Pro Tips for These First 2 Weeks:**
- Set phone alarms for EVERY time block (4:25 AM, 7:55 PM, etc.)
- Prepare your desk the night before (water, notebook, charger)
- Morning sessions: NO email, NO social media until AFTER 6:00 AM
- Keep a physical notebook next to your keyboard for jotting questions
- If you miss a morning session, do NOT try to "make it up" — just hit the next block

---

## 🗓 WEEK 1: FOUNDATION & FIRST CODE (Nov 20 – Nov 26, 2025)

### Week 1 Goals

By Sunday night November 26, you will have:

1. ✅ Full development environment installed and working
2. ✅ First GitHub repository created with your first commit
3. ✅ Completed Python for Everybody Chapters 1-2 (variables, expressions)
4. ✅ Completed CS50 Week 0 (Scratch — understanding computational thinking)
5. ✅ Completed 5+ SQLZoo exercises (SELECT basics)
6. ✅ Completed DataCamp "Introduction to Python" course
7. ✅ Watched DeepLearning.AI "ChatGPT Prompt Engineering for Developers" (AI awareness)
8. ✅ Written your first Python script that actually runs
9. ✅ Made 7+ GitHub commits (building your streak from Day 1)

### Week 1 Total Hours: ~25 hours

---

### 📌 DAY 1 — Thursday, November 20, 2025

**Theme: "First Code Day" — Your tech career starts TODAY**

#### Morning Block: 4:30 AM – 6:00 AM (1.5 hours)

**4:30 – 4:45 AM | Activate Subscriptions (15 min)**
- [ ] Open browser → Go to coursera.org → Subscribe to **Coursera Plus** ($59/month)
- [ ] Go to datacamp.com → Subscribe to **DataCamp Premium** ($25/month)
- [ ] Open Cursor IDE → Subscribe to **Cursor Pro** ($20/month) if not done yet
- [ ] Quick confirmation: you should now have access to all three platforms

**4:45 – 5:15 AM | Python for Everybody — Chapter 1: Why Program? (30 min)**
- [ ] Go to Coursera → Search "Python for Everybody" → Enroll (included in Plus)
- [ ] Start **Course 1: "Programming for Everybody (Getting Started with Python)"**
- [ ] Watch **Chapter 1 video lectures** by Dr. Chuck (Charles Severance)
  - "Why Program?" (~15 min)
  - "Hardware Architecture" (~10 min)
- [ ] **What you'll learn:** Why computers need instructions, what a program is, how hardware executes code
- [ ] **Take notes in your physical notebook:** Write down 3 things that surprised you

**5:15 – 6:00 AM | CS50 Week 0 — Scratch: Part 1 (45 min)**
- [ ] Go to edX → Search "CS50" → Enroll in "CS50's Introduction to Computer Science" (FREE)
- [ ] Start **Week 0: Scratch**
- [ ] Watch David Malan's lecture (first 45 minutes)
  - This lecture introduces computational thinking, algorithms, and abstraction
  - Malan is one of the best CS lecturers alive — enjoy this
- [ ] **Why CS50 matters for you:** It teaches you to THINK like a programmer, not just memorize syntax

#### Evening Block: 8:00 PM – 10:00 PM (2 hours)

**8:00 – 8:30 PM | Create Your First GitHub Repository (30 min)**

This is a milestone moment. Your first repository.

- [ ] Open your browser → Go to github.com → Sign in
- [ ] Click the green **"New"** button (top left) to create a new repository
- [ ] Repository name: `learning_journey`
- [ ] Description: `🚀 Career transformation: Business Ops → Senior LLM Engineer | GenAI-First from Day 1`
- [ ] Select: **Public** (this will be your public learning journal)
- [ ] Check: ✅ "Add a README file"
- [ ] Check: ✅ "Add .gitignore" → Select "Python" from dropdown
- [ ] Click **"Create repository"**

Now clone it to your computer:
- [ ] Open your terminal (Command Prompt or Terminal)
- [ ] Navigate to your coding folder:
  - Windows: `cd C:\Users\%USERNAME%\coding`
  - Mac: `cd ~/coding`
- [ ] Type: `git clone https://github.com/YOUR-USERNAME/learning_journey.git`
  - Replace YOUR-USERNAME with your actual GitHub username
- [ ] Type: `cd learning_journey`
- [ ] Open it in Cursor: `cursor .` (or open Cursor and use File → Open Folder)

**8:30 – 9:00 PM | Write Your First Python Script (30 min)**

- [ ] In Cursor, create a new file: `day_001_hello_world.py`
- [ ] Type this code (type it yourself, do NOT copy-paste — muscle memory matters):

```python
# Day 1: My first Python program
# Date: November 20, 2025
# Manuel Reyes - Learning Journey

# My first print statement
print("Hello, World!")
print("My name is Manuel Reyes")
print("Today I start my journey from Business Ops to Senior LLM Engineer")

# My first variable
days_in_journey = 1
total_days = 37 * 30  # 37 months * ~30 days
print(f"Day {days_in_journey} of {total_days}")

# My first calculation
years_experience = 15
trading_years = 6
print(f"I bring {years_experience} years of business experience")
print(f"And {trading_years} years of trading knowledge")
print(f"Combined domain expertise: {years_experience + trading_years} years")

# My first conditional
if days_in_journey == 1:
    print("🚀 The journey begins!")
```

- [ ] Save the file (Ctrl+S or Cmd+S)
- [ ] Run it: Open the terminal in Cursor (Ctrl+` or View → Terminal) and type:
  - `python day_001_hello_world.py` (Windows)
  - `python3 day_001_hello_world.py` (Mac)
- [ ] You should see your text printed in the terminal. **Congratulations — you just ran your first program!**

**If you see an error:** Don't panic. Read the error message. It usually tells you the line number. Common issues:
- Missing colon after `if` statement
- Mismatched quotes (started with `"` but ended with `'`)
- Indentation error (Python uses spaces for structure — the `print` after `if` must be indented)

**9:00 – 9:30 PM | Make Your First Git Commit (30 min)**

This saves your work to GitHub. You'll do this EVERY day.

- [ ] In the terminal (inside your `learning_journey` folder), type:
```bash
git add .
git commit -m "Day 1: First Python script - Hello World 🚀"
git push
```
- [ ] Go to github.com → your `learning_journey` repository → Refresh the page
- [ ] You should see your `day_001_hello_world.py` file there!
- [ ] **You just made your first contribution to your GitHub streak.**

**9:30 – 10:00 PM | DataCamp — Introduction to Python: Chapter 1 (30 min)**
- [ ] Go to DataCamp → Start the track **"Data Analyst with Python"**
- [ ] Begin the first course: **"Introduction to Python"**
- [ ] Complete **Chapter 1: Python Basics**
  - This covers: variables, basic arithmetic, data types (int, float, str)
  - Interactive exercises — type code directly in the browser
  - ~30 minutes to complete
- [ ] **Why DataCamp alongside Coursera?** Coursera teaches concepts with videos; DataCamp forces you to type code and get instant feedback. The combination accelerates fluency.

#### Day 1 Checklist

- [ ] Subscriptions activated (Coursera Plus, DataCamp, Cursor Pro)
- [ ] **v8.3 AI tooling ready:** Anthropic API key + Gemini API key stored securely; Claude Desktop installed; Docker Desktop running; `gh` CLI authenticated
- [ ] Python for Everybody Ch.1 watched
- [ ] CS50 Week 0 lecture started (first 45 min)
- [ ] GitHub repo created and cloned
- [ ] First Python script written and executed
- [ ] First git commit pushed
- [ ] DataCamp Intro to Python Ch.1 completed
- [ ] **Total study time: ~3.5 hours** ✅

---

### 📌 DAY 2 — Friday, November 21, 2025

**Theme: "Python Fundamentals" — Variables, Types, and Your First Real Calculations**

#### Morning Block: 4:30 AM – 6:00 AM (1.5 hours)

**4:30 – 5:15 AM | Python for Everybody — Chapter 1 continued + Chapter 2 start (45 min)**
- [ ] Continue/complete Chapter 1 videos if any remaining
- [ ] Start **Chapter 2: "Variables, Expressions and Statements"**
  - Watch: "Variables" video
  - Watch: "Expressions" video
- [ ] **Key concepts to understand:**
  - A variable is a name that stores a value (like a cell reference in Excel)
  - Python executes code line by line, top to bottom
  - `=` means "assign" (not "equals" like in math)
  - `==` means "is equal to?" (comparison)
- [ ] Write these distinctions in your notebook

**5:15 – 6:00 AM | CS50 Week 0 — Scratch: Part 2 (45 min)**
- [ ] Continue David Malan's Week 0 lecture (pick up where you left off)
- [ ] Focus on understanding:
  - **Functions:** Reusable blocks of instructions
  - **Conditionals:** If/else decision-making
  - **Loops:** Repeating actions
  - **Abstraction:** Hiding complexity behind simple names
- [ ] These concepts appear in EVERY programming language — they're universal

#### Evening Block: 8:00 PM – 10:00 PM (2 hours)

**8:00 – 8:45 PM | Practice: Python Variables & Expressions (45 min)**

- [ ] Create a new file in Cursor: `day_002_variables.py`
- [ ] Practice typing these concepts yourself (DO NOT copy-paste):

```python
# Day 2: Variables, Types, and Expressions
# Understanding how Python stores and manipulates data

# --- VARIABLES (like Excel cells, but with names) ---
first_name = "Manuel"           # str (text) — uses quotes
last_name = "Reyes"             # str
age = 35                         # int (whole number) — no quotes
years_in_finance = 15            # int
trading_balance = 25000.50       # float (decimal number)
is_learning_python = True        # bool (True or False)

# --- PRINTING VARIABLES ---
print(f"Name: {first_name} {last_name}")
print(f"Age: {age}")
print(f"Finance experience: {years_in_finance} years")
print(f"Trading balance: ${trading_balance:,.2f}")
print(f"Learning Python: {is_learning_python}")

# --- TYPE CHECKING (what type is this variable?) ---
print(f"Type of first_name: {type(first_name)}")   # <class 'str'>
print(f"Type of age: {type(age)}")                   # <class 'int'>
print(f"Type of trading_balance: {type(trading_balance)}")  # <class 'float'>

# --- ARITHMETIC (like Excel formulas) ---
monthly_savings = 500
months_to_save = 12
annual_savings = monthly_savings * months_to_save
print(f"Annual savings: ${annual_savings}")

# --- STRING OPERATIONS ---
full_name = first_name + " " + last_name  # concatenation (joining strings)
print(f"Full name: {full_name}")
print(f"Name length: {len(full_name)} characters")
print(f"Uppercase: {full_name.upper()}")

# --- USER INPUT (your program asks a question!) ---
# Uncomment the lines below to try interactive input:
# user_stock = input("Enter a stock ticker: ")
# print(f"You entered: {user_stock.upper()}")
```

- [ ] Run the script. Read each output line and make sure you understand WHY it printed that
- [ ] **Experiment:** Change values, add new variables, break things on purpose and fix them

**8:45 – 9:15 PM | DataCamp — Introduction to Python: Chapter 2 (30 min)**
- [ ] Complete **Chapter 2: "Python Lists"**
  - Lists are like a column in Excel — a collection of values in order
  - You'll learn: creating lists, accessing items, slicing, list operations
  - ~30 minutes of interactive exercises

**9:15 – 9:45 PM | SQLZoo — First SQL Exercises (30 min)**
- [ ] Go to [sqlzoo.net](https://sqlzoo.net)
- [ ] Start **Tutorial 0: "SELECT basics"**
- [ ] Complete all exercises in this section (there are about 3)
- [ ] Then start **Tutorial 1: "SELECT name"**
- [ ] Complete at least the first 5 exercises
- [ ] **What is SQL?** It's the language for asking questions about data in databases. If Python is how you *process* data, SQL is how you *retrieve* data. Both are essential.
- [ ] **SQL concepts to know after today:**
  - `SELECT` — choose which columns to show
  - `FROM` — which table to look in
  - `WHERE` — filter rows based on conditions

**9:45 – 10:00 PM | Git Commit + Day 2 Notes (15 min)**
- [ ] Save your work
- [ ] In terminal:
```bash
git add .
git commit -m "Day 2: Variables, types, expressions + SQLZoo SELECT basics"
git push
```
- [ ] In your physical notebook: Write 3 things you learned today and 1 thing that confused you

#### Day 2 Checklist

- [ ] Python for Everybody Ch.2 started (variables, expressions)
- [ ] CS50 Week 0 lecture completed
- [ ] `day_002_variables.py` written and executed
- [ ] DataCamp Intro to Python Ch.2 (Lists) completed
- [ ] SQLZoo Tutorial 0 + Tutorial 1 started (5+ exercises)
- [ ] Git commit pushed (Day 2 streak continues)
- [ ] **Total study time: ~3.5 hours** ✅

---

### 📌 DAY 3 — Saturday, November 22, 2025

**Theme: "Deep Work Saturday" — CS50 Scratch Project + Python Deep Dive**

This is your POWER DAY — 5.5 hours of uninterrupted learning.

#### Morning Block: 5:00 AM – 8:30 AM (3.5 hours)

**5:00 – 6:00 AM | CS50 Week 0 — Build Your Scratch Project (60 min)**
- [ ] Go to [scratch.mit.edu](https://scratch.mit.edu) → Create an account
- [ ] Work on the **CS50 Problem Set 0** — Create an interactive Scratch project
- [ ] Requirements from CS50:
  - Must have at least two sprites (characters)
  - Must have at least three scripts (code blocks)
  - Must use at least one conditional
  - Must use at least one loop
  - Must use at least one variable
- [ ] **Suggestion for YOUR project:** Build a simple trading game!
  - Sprite 1: A stock chart that moves up/down randomly
  - Sprite 2: A "Buy" and "Sell" button
  - Variable: Track your profit/loss
  - This connects to your trading background while learning programming concepts
- [ ] Don't aim for perfection — aim for COMPLETION

**6:00 – 7:00 AM | Python for Everybody — Chapter 2: Complete + Chapter 3 Start (60 min)**
- [ ] Finish all Chapter 2 videos: "Variables, Expressions and Statements"
- [ ] Complete the Chapter 2 quiz/exercises on Coursera
- [ ] Start **Chapter 3: "Conditional Execution" (if/else)**
  - Watch: "Conditional Execution" video
- [ ] **Key concept:** `if/elif/else` is how programs make DECISIONS
  - Think of it like Excel's `IF()` function, but much more powerful
- [ ] **In your notebook:** Draw a flowchart of an if/elif/else decision

**7:00 – 8:00 AM | DataCamp — Introduction to Python: Chapters 3-4 (60 min)**
- [ ] Complete **Chapter 3: "Functions and Packages"**
  - Functions = reusable blocks of code (like Excel macros, but better)
  - Packages = pre-built tools others have made (like Excel add-ins)
- [ ] Complete **Chapter 4: "NumPy"**
  - NumPy = the math engine of Python for data work
  - NumPy arrays are like Excel columns but can do calculations instantly on millions of rows
- [ ] **Milestone:** Completing all 4 chapters = you've finished your first DataCamp course!

**8:00 – 8:30 AM | Practice: Conditionals Script (30 min)**
- [ ] Create `day_003_conditionals.py` in your learning_journey folder
- [ ] Write a program that uses if/elif/else — connect it to something you know:

```python
# Day 3: Conditional Execution
# A simple stock analysis decision maker

stock_price = 150.00
purchase_price = 140.00
rsi_value = 28  # RSI below 30 = potentially oversold

# Calculate profit/loss
change = stock_price - purchase_price
change_percent = (change / purchase_price) * 100

print(f"Stock Price: ${stock_price}")
print(f"Purchase Price: ${purchase_price}")
print(f"Change: ${change:.2f} ({change_percent:.1f}%)")
print(f"RSI: {rsi_value}")

# Decision logic using if/elif/else
if rsi_value < 30:
    print("⚠️ RSI is oversold territory — potential buying opportunity")
elif rsi_value > 70:
    print("⚠️ RSI is overbought — consider taking profits")
else:
    print("✅ RSI is in normal range")

if change_percent > 5:
    print("📈 Strong gain — consider trailing stop")
elif change_percent > 0:
    print("📈 Modest gain — hold position")
elif change_percent > -5:
    print("📉 Small loss — review thesis")
else:
    print("🚨 Significant loss — review stop-loss")
```

- [ ] Run it. Change the values and re-run to see different paths execute.

#### Evening Block: 8:00 PM – 10:00 PM (2 hours)

**8:00 – 8:45 PM | SQLZoo — Continue SELECT Exercises (45 min)**
- [ ] Complete **Tutorial 1: "SELECT name"** (all remaining exercises)
- [ ] Start **Tutorial 2: "SELECT from World"**
- [ ] Complete at least 8 exercises in Tutorial 2
- [ ] **SQL skills building:** `WHERE`, `LIKE`, `IN`, `BETWEEN`, `ORDER BY`

**8:45 – 9:30 PM | DeepLearning.AI — ChatGPT Prompt Engineering for Developers (45 min)**
- [ ] Go to [deeplearning.ai/short-courses/chatgpt-prompt-engineering-for-developers/](https://www.deeplearning.ai/short-courses/chatgpt-prompt-engineering-for-developers/)
- [ ] Start watching (total course is ~1 hour, spread across today and tomorrow)
- [ ] Watch: Introduction + Guidelines + Iterative sections (~45 min)
- [ ] **Why this matters NOW (Week 1):** Your roadmap says "AI Awareness Week 1-2." This 1-hour course plants the seed of understanding HOW LLM APIs work. You won't build with them yet, but you'll understand the foundation.
- [ ] **Key takeaways to note:**
  - LLMs are called via APIs (like making a phone call to a smart assistant)
  - Prompts need to be specific and structured
  - Temperature controls randomness (0 = focused, 1 = creative)
  - You can build SYSTEMS with these APIs, not just chat

**9:30 – 10:00 PM | Git Commit + Weekly Planning Note (30 min)**
- [ ] Git commit:
```bash
git add .
git commit -m "Day 3: Scratch project + conditionals + DataCamp Intro complete 🎉"
git push
```
- [ ] Write in your notebook: "What was the hardest thing today? What clicked?"
- [ ] Quick review: How are you feeling about the 4:30 AM schedule? Adjust if needed.

#### Day 3 Checklist

- [ ] CS50 Scratch project built (or significantly progressed)
- [ ] Python for Everybody Ch.2 completed, Ch.3 started
- [ ] DataCamp "Introduction to Python" COMPLETE (all 4 chapters) 🎉
- [ ] `day_003_conditionals.py` written and executed
- [ ] SQLZoo Tutorial 1 complete + Tutorial 2 started
- [ ] DeepLearning.AI Prompt Engineering course — first 45 minutes
- [ ] Git commit pushed (Day 3 streak)
- [ ] **Total study time: ~5.5 hours** ✅

---

### 📌 DAY 4 — Sunday, November 23, 2025

**Theme: "Review & Plan" — Consolidate learning + LinkedIn**

#### Evening Block: 7:30 PM – 9:30 PM (2 hours)

**7:30 – 8:00 PM | DeepLearning.AI — Prompt Engineering: Complete (30 min)**
- [ ] Finish remaining sections: Summarizing, Inferring, Transforming, Expanding, Chatbot
- [ ] **After completing:** You now understand the basics of LLM APIs. This is your AI awareness foundation.
- [ ] In your notebook, write: "3 things I could build with LLM APIs in finance"

**8:00 – 8:45 PM | Week 1 Mid-Review: Practice What You've Learned (45 min)**
- [ ] Create `day_004_review.py` — Write a program that combines everything from Days 1-3:
  - Variables (strings, ints, floats)
  - Arithmetic operations
  - f-string formatting
  - if/elif/else conditionals
  - print statements with meaningful output
- [ ] **Challenge yourself:** Build a "Mini Portfolio Tracker" that:
  - Stores 3 stock names and prices as variables
  - Calculates total portfolio value
  - Determines if portfolio is up or down from a target
  - Prints a formatted summary

**8:45 – 9:15 PM | LinkedIn Profile Planning (30 min)**
- [ ] DO NOT change your LinkedIn headline yet
- [ ] Instead, research: Open LinkedIn → Search "Data Analyst" and "AI Engineer" profiles
- [ ] Save/bookmark 5 profiles of people who transitioned from non-tech to data/AI roles
- [ ] Note what skills they list, what their "About" section says
- [ ] Draft (in your notebook, NOT on LinkedIn yet) a new headline idea:
  - Example: "Data Analyst & AI Engineer | Python • SQL • GenAI | Finance Domain Expert"

**9:15 – 9:30 PM | Git Commit + Plan Monday (15 min)**
- [ ] Git commit:
```bash
git add .
git commit -m "Day 4: Week review + portfolio tracker + AI prompt engineering complete"
git push
```
- [ ] Plan Monday morning: What specific Python for Everybody video will you start?

#### Day 4 Checklist

- [ ] DeepLearning.AI Prompt Engineering course COMPLETE ✅
- [ ] Review script written combining all concepts
- [ ] LinkedIn research done (5 profiles saved)
- [ ] Draft headline written in notebook
- [ ] Git commit pushed (Day 4 streak)
- [ ] **Total study time: ~2 hours** ✅

---

### 📌 DAY 5 — Monday, November 24, 2025

**Theme: "Loops & Iteration" — The power of automation**

#### Morning Block: 4:30 AM – 6:00 AM (1.5 hours)

**4:30 – 5:30 AM | Python for Everybody — Chapter 3: Conditional + Chapter 4: Functions (60 min)**
- [ ] Complete Chapter 3 videos if any remaining
- [ ] Start **Chapter 4: "Functions"**
  - Watch: "Functions" videos
- [ ] **Functions are CRITICAL to understand well.** They are reusable blocks of code:
  - Think of a function like an Excel formula you create yourself
  - You define it once, then use it anywhere
  - Functions take inputs (parameters) and return outputs

**5:30 – 6:00 AM | Python for Everybody — Chapter 5: Loops Start (30 min)**
- [ ] Start **Chapter 5: "Loops and Iteration"**
  - `for` loops: do something for each item in a list (like dragging an Excel formula down a column)
  - `while` loops: keep doing something until a condition is met

#### Evening Block: 8:00 PM – 10:00 PM (2 hours)

**8:00 – 9:00 PM | Practice: Loops + Functions Script (60 min)**
- [ ] Create `day_005_loops_functions.py`:

```python
# Day 5: Loops and Functions
# Automating repetitive calculations

# --- FOR LOOP (iterate through a list) ---
stock_prices = [145.50, 148.20, 142.80, 151.00, 149.75]
print("Daily Stock Prices:")
for i, price in enumerate(stock_prices, 1):
    print(f"  Day {i}: ${price:.2f}")

# Calculate average (this is what loops are for!)
total = 0
for price in stock_prices:
    total = total + price
average = total / len(stock_prices)
print(f"Average price: ${average:.2f}")

# --- FUNCTIONS (reusable calculations) ---
def calculate_return(buy_price, sell_price):
    """Calculate the percentage return on a trade."""
    dollar_return = sell_price - buy_price
    percent_return = (dollar_return / buy_price) * 100
    return percent_return

# Use the function multiple times
trade1 = calculate_return(100, 115)
trade2 = calculate_return(50, 47)
trade3 = calculate_return(200, 220)

print(f"Trade 1 return: {trade1:.1f}%")
print(f"Trade 2 return: {trade2:.1f}%")
print(f"Trade 3 return: {trade3:.1f}%")

# --- WHILE LOOP ---
savings = 0
month = 0
target = 5000
monthly_deposit = 500

while savings < target:
    month = month + 1
    savings = savings + monthly_deposit
    print(f"Month {month}: ${savings:,.2f}")

print(f"Reached ${target:,} in {month} months!")
```

- [ ] Run it. Modify the stock prices list. Add more trades. Change the savings target.

**9:00 – 9:30 PM | SQLZoo — Tutorial 2: Complete (30 min)**
- [ ] Complete all remaining exercises in **Tutorial 2: "SELECT from World"**
- [ ] SQL skills you now have: `SELECT`, `FROM`, `WHERE`, `ORDER BY`, `LIKE`, `IN`, `BETWEEN`

**9:30 – 10:00 PM | DataCamp — Start "Intermediate Python" Chapter 1 (30 min)**
- [ ] Begin the next course in the track: **"Intermediate Python"**
- [ ] Complete **Chapter 1: "Matplotlib"** (data visualization basics)
  - Matplotlib is Python's main charting library
  - Like creating charts in Excel, but with code

**10:00 PM | Git Commit**
```bash
git add .
git commit -m "Day 5: Loops, functions, Matplotlib basics + SQLZoo Tutorial 2 complete"
git push
```

#### Day 5 Checklist

- [ ] Python for Everybody Ch.3 done, Ch.4 (Functions), Ch.5 (Loops) started
- [ ] `day_005_loops_functions.py` written and executed
- [ ] SQLZoo Tutorial 2 complete
- [ ] DataCamp Intermediate Python Ch.1 (Matplotlib) started
- [ ] Git commit pushed (Day 5 streak)
- [ ] **Total study time: ~3.5 hours** ✅

---

### 📌 DAY 6 — Tuesday, November 25, 2025

**Theme: "Data Structures" — Lists, dictionaries, and organizing information**

#### Morning Block: 4:30 AM – 6:00 AM (1.5 hours)

**4:30 – 5:30 AM | Python for Everybody — Chapter 5: Loops Complete + Chapter 6: Strings (60 min)**
- [ ] Complete Chapter 5 loops videos and exercises
- [ ] Start **Chapter 6: "Strings"**
  - Strings are text data — the most common data type you'll work with
  - String methods: `.upper()`, `.lower()`, `.strip()`, `.split()`, `.find()`, `.replace()`
  - Slicing: `text[0:5]` gets first 5 characters (like Excel's LEFT function)

**5:30 – 6:00 AM | HackerRank — Python Challenges (30 min)**
- [ ] Go to HackerRank → Python domain
- [ ] Complete 3 easy challenges from "Introduction" section:
  - "Say 'Hello, World!' With Python"
  - "Python If-Else"
  - "Arithmetic Operators"
- [ ] **Why HackerRank?** It forces you to solve problems WITHOUT seeing the answer first. This builds real problem-solving muscle.

#### Evening Block: 8:00 PM – 10:00 PM (2 hours)

**8:00 – 8:45 PM | Practice: Lists & Dictionaries (45 min)**
- [ ] Create `day_006_data_structures.py`:

```python
# Day 6: Lists and Dictionaries
# How Python organizes collections of data

# --- LISTS (ordered collection, like a spreadsheet column) ---
watchlist = ["AAPL", "GOOGL", "MSFT", "TSLA", "AMZN"]
print(f"My watchlist: {watchlist}")
print(f"First stock: {watchlist[0]}")      # Index starts at 0!
print(f"Last stock: {watchlist[-1]}")       # -1 = last item
print(f"Watchlist size: {len(watchlist)}")

# Add and remove
watchlist.append("NVDA")
print(f"After adding NVDA: {watchlist}")

# Loop through list
for stock in watchlist:
    print(f"  Analyzing: {stock}")

# --- DICTIONARIES (key-value pairs, like a lookup table) ---
portfolio = {
    "AAPL": {"shares": 10, "avg_cost": 150.00},
    "GOOGL": {"shares": 5, "avg_cost": 140.00},
    "MSFT": {"shares": 15, "avg_cost": 380.00},
}

# Access data
print(f"Apple shares: {portfolio['AAPL']['shares']}")
print(f"Google avg cost: ${portfolio['GOOGL']['avg_cost']}")

# Loop through dictionary
total_invested = 0
for ticker, data in portfolio.items():
    invested = data["shares"] * data["avg_cost"]
    total_invested += invested
    print(f"  {ticker}: {data['shares']} shares × ${data['avg_cost']:.2f} = ${invested:,.2f}")

print(f"Total invested: ${total_invested:,.2f}")
```

- [ ] Run it. Add more stocks. Change the share counts.
- [ ] **Key insight:** Dictionaries are EVERYWHERE in Python. APIs return dictionaries. JSON files are dictionaries. Understanding them well is critical.

**8:45 – 9:15 PM | DataCamp — Intermediate Python: Chapters 2-3 (30 min)**
- [ ] Complete **Chapter 2: "Dictionaries & Pandas"** — Introduction to Pandas DataFrames
  - Pandas is like Excel but for millions of rows
  - DataFrames are the #1 data structure in data analysis
- [ ] Start **Chapter 3: "Logic, Control Flow and Filtering"**

**9:15 – 10:00 PM | SQLZoo — Tutorial 3: SELECT from Nobel (45 min)**
- [ ] Start **Tutorial 3: "SELECT from Nobel"**
- [ ] Complete as many exercises as possible (aim for 10+)
- [ ] New SQL concepts: more complex `WHERE` conditions, `AND`, `OR`, pattern matching

**10:00 PM | Git Commit**
```bash
git add .
git commit -m "Day 6: Data structures (lists, dicts) + Pandas intro + SQL Nobel queries"
git push
```

#### Day 6 Checklist

- [ ] Python for Everybody Ch.5 done, Ch.6 (Strings) started
- [ ] HackerRank: 3 Python challenges completed
- [ ] `day_006_data_structures.py` written and executed
- [ ] DataCamp Intermediate Python Ch.2-3 progressed
- [ ] SQLZoo Tutorial 3 started (10+ exercises)
- [ ] Git commit pushed (Day 6 streak)
- [ ] **Total study time: ~3.5 hours** ✅

---

### 📌 DAY 7 — Wednesday, November 26, 2025 (Day Before Thanksgiving)

**Theme: "Week 1 Capstone" — Combine everything into one meaningful script**

#### Morning Block: 4:30 AM – 6:00 AM (1.5 hours)

**4:30 – 5:30 AM | Python for Everybody — Chapter 6 + Chapter 7 Start (60 min)**
- [ ] Complete Chapter 6: Strings
- [ ] Start **Chapter 7: "Files"** (reading data from files)
  - This is where Python gets powerful for YOUR work
  - Reading CSV files = reading Excel-like data with code
  - This skill directly connects to your data analyst work

**5:30 – 6:00 AM | DataCamp — Intermediate Python: Complete Chapters 3-4 (30 min)**
- [ ] Complete **Chapter 3: "Logic, Control Flow and Filtering"**
- [ ] Start **Chapter 4: "Loops"** (in Pandas context)

#### Evening Block: 8:00 PM – 10:00 PM (2 hours)

**8:00 – 9:30 PM | Week 1 Capstone Script (90 min)**
- [ ] Create `week_01_capstone.py` — A "Trading Journal Analyzer" that combines EVERYTHING:

```python
# Week 1 Capstone: Trading Journal Analyzer
# Combines: variables, lists, dicts, loops, functions, conditionals, f-strings
# Manuel Reyes | Week 1 | Learning Journey

def calculate_return(entry, exit_price):
    """Calculate percentage return on a trade."""
    return ((exit_price - entry) / entry) * 100

def classify_trade(return_pct):
    """Classify a trade result."""
    if return_pct > 10:
        return "🏆 Big Win"
    elif return_pct > 0:
        return "✅ Win"
    elif return_pct > -5:
        return "⚠️ Small Loss"
    else:
        return "🚨 Big Loss"

# Trade journal data (list of dictionaries)
trades = [
    {"ticker": "AAPL", "entry": 150.00, "exit": 165.00, "shares": 10},
    {"ticker": "TSLA", "entry": 200.00, "exit": 185.00, "shares": 5},
    {"ticker": "NVDA", "entry": 400.00, "exit": 480.00, "shares": 8},
    {"ticker": "MSFT", "entry": 370.00, "exit": 365.00, "shares": 12},
    {"ticker": "GOOGL", "entry": 140.00, "exit": 155.00, "shares": 15},
]

# Analyze all trades
print("=" * 60)
print("📊 TRADING JOURNAL ANALYSIS — WEEK 1 CAPSTONE")
print("=" * 60)

total_pnl = 0
wins = 0
losses = 0

for trade in trades:
    ret = calculate_return(trade["entry"], trade["exit"])
    pnl = (trade["exit"] - trade["entry"]) * trade["shares"]
    total_pnl += pnl
    classification = classify_trade(ret)

    if pnl > 0:
        wins += 1
    else:
        losses += 1

    print(f"\n{trade['ticker']}:")
    print(f"  Entry: ${trade['entry']:.2f} → Exit: ${trade['exit']:.2f}")
    print(f"  Shares: {trade['shares']} | P&L: ${pnl:,.2f} | Return: {ret:.1f}%")
    print(f"  Result: {classification}")

# Summary statistics
print("\n" + "=" * 60)
print("📈 SUMMARY")
print("=" * 60)
print(f"Total Trades: {len(trades)}")
print(f"Wins: {wins} | Losses: {losses}")
print(f"Win Rate: {(wins/len(trades))*100:.0f}%")
print(f"Total P&L: ${total_pnl:,.2f}")

if total_pnl > 0:
    print("✅ Overall: PROFITABLE")
else:
    print("🚨 Overall: NET LOSS — review strategy")
```

- [ ] Run it. This script demonstrates EVERY Python concept you learned this week.
- [ ] **This is portfolio-worthy.** Even this simple script shows: domain expertise + programming ability.

**9:30 – 10:00 PM | Git Commit + Week 1 Reflection (30 min)**
```bash
git add .
git commit -m "Week 1 Capstone: Trading Journal Analyzer - combines all Python fundamentals 🎉"
git push
```
- [ ] In your notebook, write your **Week 1 Reflection:**
  - What was the hardest concept?
  - What clicked fastest?
  - How is the 4:30 AM schedule working?
  - Rate your confidence 1-10 on: Python basics, SQL basics, Git workflow

#### Day 7 Checklist

- [ ] Python for Everybody through Ch.6, Ch.7 started
- [ ] DataCamp Intermediate Python progressing (Ch.3-4)
- [ ] `week_01_capstone.py` completed — your first "real" program!
- [ ] Week 1 reflection written
- [ ] Git commit pushed (Day 7 streak — **full week!** 🎉)
- [ ] **Total study time: ~3.5 hours** ✅

---

## 📊 WEEK 1 CUMULATIVE PROGRESS

| Metric | Target | Status |
|--------|--------|--------|
| Study hours | ~25 hrs | ~25 hrs ✅ |
| Git commits | 7+ | 7 ✅ |
| Python scripts written | 6+ | 6 ✅ |
| Python for Everybody | Ch. 1-7 started | ✅ |
| CS50 | Week 0 complete | ✅ |
| DataCamp courses | Intro complete, Intermediate started | ✅ |
| SQLZoo tutorials | Tutorials 0-3 (25+ exercises) | ✅ |
| AI awareness | Prompt Engineering course complete | ✅ |
| Concepts mastered | Variables, types, conditionals, loops, functions, lists, dicts | ✅ |

---

## 🗓 WEEK 2: BUILD MOMENTUM (Nov 27 – Dec 3, 2025)

### Week 2 Goals

By Wednesday night December 3, you will have:

1. ✅ Python for Everybody through Chapter 9 (Dictionaries)
2. ✅ CS50 Week 1 started (C language — understanding how computers really work)
3. ✅ DataCamp "Intermediate Python" completed
4. ✅ 15+ more SQLZoo exercises completed
5. ✅ HackerRank: 5+ Python challenges, 5+ SQL challenges
6. ✅ DeepLearning.AI "Building Systems with ChatGPT API" watched (AI awareness #2)
7. ✅ Your README.md file written for your learning_journey repo
8. ✅ LinkedIn headline updated + "Open to Work" activated
9. ✅ 14+ total GitHub commits (2-week streak)
10. ✅ DataCamp "Data Manipulation with pandas" started

### Special Note: Thanksgiving Week

Thursday Nov 27 is Thanksgiving. Your schedule adjusts:

- **Thursday Nov 27 (Thanksgiving):** REST DAY or light 1 hour if you feel like it
- **Friday Nov 28 (Day off work):** BONUS deep work day — treat it like a Saturday (5+ hours!)

---

### 📌 DAY 8 — Thursday, November 27, 2025 (Thanksgiving)

**Theme: "Rest or Light Review" — Recovery is part of the plan**

#### Option A: Full Rest Day (Recommended)
- [ ] Enjoy Thanksgiving with family
- [ ] Zero guilt — rest is how your brain consolidates learning
- [ ] Your brain is literally building new neural pathways this week; sleep and rest help

#### Option B: Light Study (1 hour, only if you WANT to)

**Anytime that works | 60 min max**
- [ ] DataCamp: Complete 1 chapter of Intermediate Python
- [ ] OR: Watch 1 Python for Everybody video
- [ ] Quick git commit if you did anything:
```bash
git commit -m "Day 8: Thanksgiving light study - [what you did]"
```

---

### 📌 DAY 9 — Friday, November 28, 2025 (Black Friday — Day off work!)

**Theme: "BONUS Power Day" — Deep Python + Pandas Introduction**

Since you're likely off work, this is a GOLDEN opportunity. Use Saturday's schedule.

#### Morning Block: 5:00 AM – 8:30 AM (3.5 hours)

**5:00 – 6:30 AM | Python for Everybody — Chapter 7: Files + Chapter 8: Lists (90 min)**
- [ ] Complete **Chapter 7: "Files"**
  - Opening files, reading lines, searching through data
  - `open()`, `read()`, `readline()`, `readlines()`
  - This is your gateway to processing CSV data
- [ ] Start **Chapter 8: "Lists"** (deeper than DataCamp's intro)
  - List methods: `.append()`, `.sort()`, `.reverse()`, `.pop()`
  - List comprehensions (shortcut for creating lists — very Pythonic)
  - Splitting strings into lists: `"AAPL,GOOGL,MSFT".split(",")`

**6:30 – 7:30 AM | DataCamp — Complete Intermediate Python (60 min)**
- [ ] Complete remaining chapters of **"Intermediate Python"**
- [ ] **Chapter 4: "Loops"** — focus on looping over Pandas DataFrames
- [ ] **Milestone: Second DataCamp course complete!** 🎉

**7:30 – 8:30 AM | DeepLearning.AI — Building Systems with ChatGPT API (60 min)**
- [ ] Go to [deeplearning.ai/short-courses/building-systems-with-chatgpt/](https://www.deeplearning.ai/short-courses/building-systems-with-chatgpt/)
- [ ] Watch the COMPLETE course (~1 hour)
- [ ] **Key concepts:**
  - Chaining LLM calls (output of one call → input of next)
  - Building a multi-step customer service system
  - Classification, moderation, chain of thought prompting
  - Evaluation of LLM outputs
- [ ] **In your notebook:** "How could I use chained LLM calls for financial analysis?"
- [ ] **Roadmap alignment:** This is your "AI Awareness Week 2" deliverable

#### Evening Block: 8:00 PM – 10:00 PM (2 hours)

**8:00 – 9:00 PM | Practice: File Reading + Data Processing (60 min)**
- [ ] Create `day_009_file_processing.py`:
- [ ] First, create a sample data file `sample_trades.csv` in the same folder:

```
ticker,entry_price,exit_price,shares,date
AAPL,150.00,165.00,10,2025-01-15
TSLA,200.00,185.00,5,2025-02-20
NVDA,400.00,480.00,8,2025-03-10
MSFT,370.00,365.00,12,2025-04-05
GOOGL,140.00,155.00,15,2025-05-22
```

- [ ] Then write the Python script to read and analyze it:

```python
# Day 9: Reading and Processing Files
# The bridge between "learning Python" and "using Python for data"

# Read the CSV file manually (without pandas - understand the basics first)
filename = "sample_trades.csv"

trades = []
with open(filename, "r") as file:
    header = file.readline().strip().split(",")
    print(f"Columns: {header}")

    for line in file:
        values = line.strip().split(",")
        trade = {
            "ticker": values[0],
            "entry": float(values[1]),
            "exit": float(values[2]),
            "shares": int(values[3]),
            "date": values[4],
        }
        trades.append(trade)

print(f"\nLoaded {len(trades)} trades from {filename}")
print("-" * 50)

# Process and analyze
for trade in trades:
    pnl = (trade["exit"] - trade["entry"]) * trade["shares"]
    ret = ((trade["exit"] - trade["entry"]) / trade["entry"]) * 100
    status = "WIN ✅" if pnl > 0 else "LOSS ❌"
    print(f"{trade['date']} | {trade['ticker']:5} | P&L: ${pnl:>10,.2f} | {ret:>6.1f}% | {status}")

# Summary
total_pnl = sum((t["exit"] - t["entry"]) * t["shares"] for t in trades)
print(f"\n{'='*50}")
print(f"Total P&L: ${total_pnl:,.2f}")
```

- [ ] Run it. This is a REAL data processing script — the kind of thing data analysts do daily.

**9:00 – 9:30 PM | SQLZoo — Tutorials 3-4 (30 min)**
- [ ] Complete **Tutorial 3: "SELECT from Nobel"**
- [ ] Start **Tutorial 4: "SELECT within SELECT"** (subqueries — more advanced!)

**9:30 – 10:00 PM | Git Commit**
```bash
git add .
git commit -m "Day 9: File processing, CSV reading, AI Systems course complete, Intermediate Python done 🎉"
git push
```

#### Day 9 Checklist

- [ ] Python for Everybody Ch.7 (Files) complete, Ch.8 (Lists) started
- [ ] DataCamp "Intermediate Python" COMPLETE 🎉
- [ ] DeepLearning.AI "Building Systems with ChatGPT API" COMPLETE ✅
- [ ] `day_009_file_processing.py` + `sample_trades.csv` created
- [ ] SQLZoo Tutorial 3 complete, Tutorial 4 started
- [ ] Git commit pushed
- [ ] **Total study time: ~5.5 hours** ✅

---

### 📌 DAY 10 — Saturday, November 29, 2025

**Theme: "Pandas Day" — Your Most Important Data Tool**

#### Morning Block: 5:00 AM – 8:30 AM (3.5 hours)

**5:00 – 6:30 AM | DataCamp — Start "Data Manipulation with pandas" (90 min)**
- [ ] Begin the next course: **"Data Manipulation with pandas"**
- [ ] Complete **Chapter 1: "Transforming DataFrames"**
  - DataFrames = the Excel spreadsheet of Python
  - `.head()`, `.info()`, `.describe()` — instant data summary
  - `.sort_values()`, `.loc[]`, `.iloc[]` — selecting and filtering data
- [ ] Start **Chapter 2: "Aggregating DataFrames"**
  - `.groupby()` — like Excel Pivot Tables
  - `.mean()`, `.sum()`, `.count()` — aggregate calculations

**6:30 – 7:30 AM | Python for Everybody — Chapter 8: Lists + Chapter 9: Dictionaries (60 min)**
- [ ] Complete Chapter 8 and start Chapter 9: Dictionaries
- [ ] Dictionaries are the MOST USED data structure in data analysis and API work
- [ ] **Why Chapter 9 matters:** APIs return JSON data, which is essentially Python dictionaries. Every AI API (OpenAI, Gemini, Claude) sends and receives dictionaries.

**7:30 – 8:30 AM | Practice: Your First Pandas Script (60 min)**
- [ ] Create `day_010_pandas_intro.py`:

```python
# Day 10: Introduction to Pandas
# Going from manual file reading to professional data analysis

import pandas as pd

# Read CSV with pandas (one line vs 15 lines of manual code!)
df = pd.read_csv("sample_trades.csv")

# Explore the data (first things every analyst does)
print("=== DATA OVERVIEW ===")
print(f"Shape: {df.shape[0]} rows × {df.shape[1]} columns")
print(f"\nFirst 3 rows:")
print(df.head(3))
print(f"\nColumn types:")
print(df.dtypes)
print(f"\nBasic statistics:")
print(df.describe())

# Add calculated columns (like Excel formulas for entire columns!)
df["pnl"] = (df["exit_price"] - df["entry_price"]) * df["shares"]
df["return_pct"] = ((df["exit_price"] - df["entry_price"]) / df["entry_price"]) * 100
df["result"] = df["pnl"].apply(lambda x: "WIN" if x > 0 else "LOSS")

print("\n=== ENRICHED DATA ===")
print(df.to_string(index=False))

# Summary statistics (what took 20 lines before = 3 lines with pandas)
print(f"\n=== SUMMARY ===")
print(f"Total P&L: ${df['pnl'].sum():,.2f}")
print(f"Average Return: {df['return_pct'].mean():.1f}%")
print(f"Best Trade: {df.loc[df['pnl'].idxmax(), 'ticker']} (${df['pnl'].max():,.2f})")
print(f"Worst Trade: {df.loc[df['pnl'].idxmin(), 'ticker']} (${df['pnl'].min():,.2f})")
print(f"Win Rate: {(df['result'] == 'WIN').mean()*100:.0f}%")
```

- [ ] Run it. Compare this to your Day 9 manual file reading — THAT's why pandas exists!
- [ ] **Note:** You'll need to install pandas first. In your terminal: `pip install pandas`

#### Evening Block: 8:00 PM – 10:00 PM (2 hours)

**8:00 – 8:45 PM | HackerRank Challenges (45 min)**
- [ ] Complete 3 Python challenges (Introduction or Basic Data Types)
- [ ] Complete 3 SQL challenges (start the SQL domain → "Basic Select")
- [ ] **Target:** Earn at least 1 HackerRank badge this week

**8:45 – 9:30 PM | CS50 Week 1 — Lecture Start (45 min)**
- [ ] Start **CS50 Week 1: C** (watch first 45 minutes of lecture)
- [ ] **Why learn C when you're focused on Python?** CS50 teaches C to show you HOW computers actually work — memory, pointers, compilation. This deep understanding makes you a better programmer in ANY language. Top tech interviewers value this knowledge.

**9:30 – 10:00 PM | Git Commit**
```bash
git add .
git commit -m "Day 10: Pandas intro! DataFrame operations + HackerRank challenges"
git push
```

---

### 📌 DAY 11 — Sunday, November 30, 2025

**Theme: "GitHub Polish + Week Planning"**

#### Evening Block: 7:30 PM – 9:30 PM (2 hours)

**7:30 – 8:30 PM | Create Your README.md (60 min)**
- [ ] Open your `learning_journey` repo's `README.md` file in Cursor
- [ ] Replace the default content with a professional README:

```markdown
# 🚀 Learning Journey: Business Ops → Senior LLM Engineer

**GenAI-First Career Transformation** | Production Code from Day 1

> **Current Stage:** Stage 1 — GenAI-First Data Analyst & AI Engineer
> **Study Commitment:** 25 hours/week
> **Started:** November 20, 2025

## 🎯 What This Repository Contains

Daily Python scripts, SQL practice, and course notes documenting my
systematic career transformation from 15+ years in business operations
and financial services to AI Engineering.

## 💪 What I Bring

- 15+ years of business data management experience
- 6 years of active trading (stocks, options, forex)
- Deep domain expertise in retirement plan operations
- Production mindset from managing real business systems

## 📊 Current Progress

- **Python:** Variables, types, conditionals, loops, functions, lists, dicts, file I/O
- **SQL:** SELECT, WHERE, JOINs (in progress)
- **AI Awareness:** LLM APIs, prompt engineering fundamentals
- **Tools:** VS Code, Cursor AI, Git/GitHub, Pandas

## 📚 Learning Path (Stage 1)

- CS50 (Harvard) — Computer Science fundamentals
- Python for Everybody (University of Michigan)
- DataCamp Data Analyst track
- Google Data Analytics Certificate
- IBM GenAI Engineering Certificate (upcoming)

## 🔗 Connect

- **LinkedIn:** [Your LinkedIn URL]
- **GitHub:** [@your-username](https://github.com/your-username)
```

- [ ] Save and commit:
```bash
git add .
git commit -m "Add professional README.md to learning_journey repo"
git push
```

**8:30 – 9:00 PM | LinkedIn Updates (30 min)**
- [ ] Update your LinkedIn **headline** (use what you drafted in Week 1):
  - Example: `Data Analyst in Training | Python • SQL • GenAI | 15+ Years Finance & Operations`
- [ ] Turn on **#OpenToWork** badge (Settings → Job seeking preferences)
- [ ] Add your GitHub link to your LinkedIn profile (Contact Info section)
- [ ] Post your first update (keep it simple and authentic):
  - "Starting my career transformation into data analytics and AI engineering. Week 2 of learning Python and SQL. Building in public at [GitHub link]. The journey of 1,000 miles begins with `print('Hello, World!')`"

**9:00 – 9:30 PM | Week 2 Planning (30 min)**
- [ ] Review what you accomplished in Week 1 vs targets
- [ ] Identify your weakest area (Python? SQL? Schedule consistency?)
- [ ] Write your top 3 priorities for the remaining 3 days of Week 2
- [ ] Set specific learning goals for Monday-Wednesday

---

### 📌 DAY 12 — Monday, December 1, 2025

**Theme: "Dictionaries Deep Dive + SQL JOINs Preview"**

#### Morning Block: 4:30 AM – 6:00 AM (1.5 hours)

**4:30 – 5:30 AM | Python for Everybody — Chapter 9: Dictionaries Complete (60 min)**
- [ ] Complete all Chapter 9 videos and exercises
- [ ] **Master these dictionary operations:**
  - Creating: `data = {"key": "value"}`
  - Accessing: `data["key"]`
  - Checking: `if "key" in data:`
  - Looping: `for key, value in data.items():`
  - Counting pattern: Build a frequency counter (this appears in 50% of data analysis tasks)

**5:30 – 6:00 AM | DataCamp — Pandas Manipulation Ch.2-3 (30 min)**
- [ ] Continue **"Data Manipulation with pandas"**
- [ ] Focus on `.groupby()` operations — this is the Pandas equivalent of Excel Pivot Tables

#### Evening Block: 8:00 PM – 10:00 PM (2 hours)

**8:00 – 9:00 PM | Practice: Dictionary Counting + Pandas GroupBy (60 min)**
- [ ] Create `day_012_dictionaries_groupby.py` combining both concepts
- [ ] Build a word frequency counter (classic interview question)
- [ ] Build a Pandas groupby analysis on your trade data

**9:00 – 9:30 PM | SQLZoo — Tutorial 4: Subqueries (30 min)**
- [ ] Continue **Tutorial 4: "SELECT within SELECT"**
- [ ] Subqueries are queries INSIDE queries — powerful for complex analysis

**9:30 – 10:00 PM | SQLZoo — Tutorial 5: SUM and COUNT Preview (30 min)**
- [ ] Start **Tutorial 5: "SUM and COUNT"** (aggregate functions)
- [ ] `SUM()`, `COUNT()`, `AVG()`, `GROUP BY` — the SQL equivalent of Pandas groupby

**10:00 PM | Git Commit**
```bash
git add .
git commit -m "Day 12: Dictionaries mastery + Pandas groupby + SQL aggregates"
git push
```

---

### 📌 DAY 13 — Tuesday, December 2, 2025

**Theme: "Error Handling + Data Cleaning Basics"**

#### Morning Block: 4:30 AM – 6:00 AM (1.5 hours)

**4:30 – 5:30 AM | Python for Everybody — Chapter 10: Tuples (60 min)**
- [ ] Start **Chapter 10: "Tuples"**
  - Tuples are like lists but immutable (can't change after creation)
  - Used for returning multiple values from functions
  - Sorting dictionaries by value uses tuples

**5:30 – 6:00 AM | HackerRank — 3 Challenges (30 min)**
- [ ] 2 Python challenges (Strings or Basic Data Types)
- [ ] 1 SQL challenge (Basic Select)

#### Evening Block: 8:00 PM – 10:00 PM (2 hours)

**8:00 – 9:00 PM | Practice: Error Handling Script (60 min)**
- [ ] Create `day_013_error_handling.py`:
- [ ] Learn `try/except` — how to handle things going wrong gracefully
- [ ] This is a PRODUCTION skill — real programs must handle errors

```python
# Day 13: Error Handling
# Production code NEVER crashes silently

def safe_calculate_return(entry, exit_price):
    """Calculate return with error handling."""
    try:
        if entry <= 0:
            raise ValueError(f"Entry price must be positive, got {entry}")
        return_pct = ((exit_price - entry) / entry) * 100
        return round(return_pct, 2)
    except ZeroDivisionError:
        print("Error: Entry price cannot be zero")
        return None
    except TypeError as e:
        print(f"Error: Invalid data type - {e}")
        return None

# Test with good data
print(safe_calculate_return(100, 115))    # 15.0%

# Test with bad data (these WON'T crash your program)
print(safe_calculate_return(0, 115))       # Error handled
print(safe_calculate_return("abc", 115))   # Error handled
print(safe_calculate_return(-50, 115))     # ValueError handled
```

**9:00 – 9:30 PM | DataCamp — Pandas Ch.3-4 (30 min)**
- [ ] Complete remaining chapters of **"Data Manipulation with pandas"**
- [ ] Slicing and indexing DataFrames
- [ ] Creating and transforming columns

**9:30 – 10:00 PM | SQLZoo — Tutorial 5 + HackerRank SQL (30 min)**
- [ ] Continue SQLZoo Tutorial 5: SUM and COUNT
- [ ] OR do 3 HackerRank SQL challenges

**10:00 PM | Git Commit**
```bash
git add .
git commit -m "Day 13: Error handling + Pandas data manipulation + SQL aggregates"
git push
```

---

### 📌 DAY 14 — Wednesday, December 3, 2025

**Theme: "Week 2 Capstone" — Two-Week Celebration Script**

#### Morning Block: 4:30 AM – 6:00 AM (1.5 hours)

**4:30 – 5:15 AM | Python for Everybody — Review + Chapter 10 complete (45 min)**
- [ ] Complete Chapter 10: Tuples
- [ ] Quick review of Chapters 1-10 key concepts

**5:15 – 6:00 AM | CS50 Week 1 Lecture — Continue (45 min)**
- [ ] Continue CS50 Week 1 lecture (data types in C, operators, conditionals)

#### Evening Block: 8:00 PM – 10:00 PM (2 hours)

**8:00 – 9:30 PM | 2-Week Capstone: "Portfolio Performance Reporter" (90 min)**
- [ ] Create `week_02_capstone.py` — Your most impressive script yet
- [ ] Combine: pandas, functions, error handling, dictionaries, file I/O, formatting
- [ ] Read from CSV → Process with pandas → Generate formatted report → Error handling
- [ ] This should demonstrate clear progression from Week 1 capstone

**9:30 – 10:00 PM | Final Git Commit + 2-Week Reflection (30 min)**
```bash
git add .
git commit -m "Week 2 Capstone: Portfolio Performance Reporter - 2 weeks complete! 🎉🚀"
git push
```
- [ ] Write your **2-Week Reflection** in your notebook:
  - Skills gained (list everything!)
  - Biggest challenge overcome
  - Confidence rating now vs Day 1
  - Schedule adjustments needed
  - Top 3 goals for Weeks 3-4

---

## 🏆 2-WEEK SUCCESS METRICS

### By December 3, 2025 — You Should Have:

| Category | Metric | Target |
|----------|--------|--------|
| **Study Hours** | Total hours invested | ~47-50 hours |
| **GitHub** | Total commits | 14+ |
| **GitHub** | Contribution streak | 14 days (with Thanksgiving gap OK) |
| **Python Scripts** | Files written | 10+ original scripts |
| **Python Knowledge** | Chapters completed | PY4E Ch. 1-10 |
| **DataCamp** | Courses completed | 2 complete + 1 in progress |
| **SQL** | SQLZoo exercises | 40+ exercises |
| **SQL** | Tutorials completed | Tutorials 0-5 |
| **AI Awareness** | Short courses complete | 2 (Prompt Engineering + Building Systems) |
| **HackerRank** | Challenges solved | 8+ (Python + SQL) |
| **CS50** | Progress | Week 0 complete, Week 1 started |
| **LinkedIn** | Profile updated | Headline + Open to Work + GitHub link |
| **Concepts** | Python fundamentals | Variables → Tuples (10 concepts) |

---

## 🔧 TROUBLESHOOTING GUIDE

### "My Python script won't run"
1. Check: Are you in the right folder? (`cd learning_journey`)
2. Check: Is the filename spelled exactly right?
3. Check: Did you save the file? (Ctrl+S)
4. Read the error message — it tells you the line number. Go to that line.
5. Common fixes: Missing colon `:`, wrong indentation, mismatched quotes

### "Git push failed"
1. Try: `git pull` first, then `git push` again
2. If it asks for credentials: Use your GitHub username and a Personal Access Token (not your password). Go to GitHub → Settings → Developer settings → Personal access tokens → Generate new token

### "I missed a morning session"
- Don't try to make it up by doubling evening session (that leads to burnout)
- Just hit the next scheduled block
- Consistency over intensity — missing 1 session out of 14 is a 93% attendance rate

### "I'm falling behind the plan"
- This plan is AMBITIOUS by design. If you complete 80%, you're on track.
- Prioritize in this order: (1) Python practice scripts, (2) DataCamp, (3) Python for Everybody videos, (4) SQLZoo, (5) Everything else
- The goal isn't to check every box — it's to build habits and foundational skills

### "I don't understand a concept"
1. First: Ask Cursor AI (highlight code → Ctrl+K → "explain this in simple terms")
2. Second: Ask ChatGPT "Explain [concept] like I'm someone who knows Excel but not programming"
3. Third: YouTube search "[concept] python tutorial for beginners"
4. Fourth: Move on and come back later — some things click after more exposure

---

## 🔮 WHAT COMES NEXT: WEEK 3-4 PREVIEW

**Week 3 (Dec 4-10):** Python for Everybody Ch. 11-13 (Regular Expressions, Networking, Web Services) + CS50 Week 1 Problem Set + DataCamp "Joining Data with pandas" + Start Kaggle "Intro to Python" micro-course

**Week 4 (Dec 11-17):** Begin Google Data Analytics Certificate (Course 1) + Start DataCamp SQL track + Python for Everybody finalize + First HackerRank certificates (Python + SQL)

**Month 2 target:** First portfolio project started (Financial Data Analysis Dashboard), Upwork profile created, Google Data Analytics Certificate progressing

---

## 💪 FINAL MOTIVATION

You're about to invest 50 hours over the next 2 weeks learning skills that will compound for the rest of your career. Every line of code you type, every SQL query you run, every git commit you push — it's building toward a $180-250K career as a Senior LLM Engineer.

Most people who say "I want to learn to code" never write their first line. **You're writing yours on November 20, 2025 at 4:30 AM.**

That's the difference.

---

*Document created: November 2025*  
*Aligned to: GenAI-First Career Roadmap v8.3*  
*Next activation plan: Weeks 3-4 (December 4-17, 2025)*