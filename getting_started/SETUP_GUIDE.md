# 🛠️ COMPLETE SETUP GUIDE - Week 1 Infrastructure

## 📋 SETUP OVERVIEW

This guide will walk you through setting up EVERY tool, platform, and account you need for your data analyst journey. Each section includes:
- What it is and why you need it
- Step-by-step installation instructions
- Configuration for your specific needs
- Verification steps to ensure it's working
- Common troubleshooting tips

**Time Required:** 3-4 hours total (spread across Thursday-Saturday)  
**Difficulty:** Beginner-friendly with screenshots  
**Support:** If stuck, see troubleshooting section at bottom

---

## 🖥️ PART 1: DEVELOPMENT ENVIRONMENT (Thursday Morning)
**Time:** 45 minutes

### 1.1 Python Installation

**What:** Python programming language  
**Why:** Core language for data analysis  
**When to do:** Thursday 5:00-5:15 AM

#### For Windows:

**Step-by-Step:**

1. **Download Python:**
   - Go to: [python.org/downloads](https://python.org/downloads)
   - Click: "Download Python 3.11.7" (or latest 3.11.x)
   - File downloads: `python-3.11.7-amd64.exe`

2. **Install Python:**
   ```
   ✅ Run the downloaded .exe file
   ✅ ⚠️ CRITICAL: Check "Add Python to PATH" (bottom of installer)
   ✅ Click "Install Now"
   ✅ Wait for installation to complete (~2 min)
   ✅ Click "Close"
   ```

3. **Verify Installation:**
   ```bash
   # Open Command Prompt (Windows key + R, type "cmd")
   python --version
   # Should show: Python 3.11.7
   
   pip --version
   # Should show: pip 23.x.x from [location]
   ```

4. **Install Essential Packages:**
   ```bash
   # In Command Prompt:
   pip install jupyter pandas numpy matplotlib seaborn
   
   # You should see:
   # "Successfully installed jupyter-X.X.X pandas-X.X.X ..."
   ```

#### For Mac:

**Step-by-Step:**

1. **Download Python:**
   - Go to: [python.org/downloads](https://python.org/downloads)
   - Click: "Download Python 3.11.7"
   - File downloads: `python-3.11.7-macos11.pkg`

2. **Install Python:**
   ```
   ✅ Open the downloaded .pkg file
   ✅ Click "Continue" through installer
   ✅ Agree to license
   ✅ Click "Install"
   ✅ Enter password if prompted
   ✅ Installation takes ~3 min
   ```

3. **Verify Installation:**
   ```bash
   # Open Terminal (Cmd + Space, type "Terminal")
   python3 --version
   # Should show: Python 3.11.7
   
   pip3 --version
   # Should show: pip 23.x.x
   ```

4. **Install Essential Packages:**
   ```bash
   pip3 install jupyter pandas numpy matplotlib seaborn
   ```

**Troubleshooting:**
- "Python not recognized" → You didn't check "Add to PATH", reinstall
- "Permission denied" on Mac → Use `sudo pip3 install ...`
- Can't open Terminal → Search "Terminal" in Spotlight

---

### 1.2 VS Code Installation & Setup

**What:** Professional code editor (like Microsoft Word for code)  
**Why:** Industry-standard tool, free, powerful  
**When to do:** Thursday 5:15-5:30 AM

#### Installation:

1. **Download VS Code:**
   - Go to: [code.visualstudio.com](https://code.visualstudio.com)
   - Click: "Download for [Your OS]"
   - File downloads: `VSCodeSetup.exe` (Windows) or `VSCode.dmg` (Mac)

2. **Install VS Code:**
   
   **Windows:**
   ```
   ✅ Run VSCodeSetup.exe
   ✅ Accept license
   ✅ Choose install location (default is fine)
   ✅ CHECK: "Add to PATH"
   ✅ CHECK: "Create desktop icon"
   ✅ CHECK: "Add 'Open with Code' to context menu"
   ✅ Click "Install"
   ✅ Launch VS Code
   ```
   
   **Mac:**
   ```
   ✅ Open VSCode.dmg
   ✅ Drag VS Code to Applications folder
   ✅ Open Applications → Visual Studio Code
   ✅ If "can't open" warning → Right-click → Open
   ```

3. **Essential Extensions:**

   In VS Code:
   ```
   Click Extensions icon (left sidebar, 4 squares)
   Search and install these:
   
   ✅ Python (by Microsoft) - ESSENTIAL
   ✅ Jupyter (by Microsoft) - ESSENTIAL
   ✅ Python Indent (by Kevin Rose)
   ✅ GitLens (by GitKraken)
   ✅ Markdown All in One (by Yu Zhang)
   ```

4. **Configure Python in VS Code:**

   ```
   1. Create new file: test.py
   2. Write: print("Hello from VS Code!")
   3. Click Python version in bottom-right
   4. Select Python 3.11.7 interpreter
   5. Right-click in file → "Run Python File in Terminal"
   6. Should see: "Hello from VS Code!"
   ```

**VS Code Settings (Optional but Recommended):**

```
File → Preferences → Settings

Search for each setting and change:

✅ "Auto Save" → Set to "afterDelay"
✅ "Tab Size" → Set to 4 (for Python)
✅ "Format On Save" → Enable
✅ "Word Wrap" → Enable
```

**First Python File:**

```python
# Create file: first_script.py

# Week 1 - Day 1: My First Python Script
# Date: November 20, 2025
# Purpose: Verify my Python environment works

def greet(name):
    """Print a personalized greeting."""
    print(f"Hello, {name}! Welcome to data analytics.")

# Test the function
greet("Future Data Analyst")

# Basic calculations
expenses = 1250.50
revenue = 3420.00
profit = revenue - expenses

print(f"This month's profit: ${profit:.2f}")
```

---

### 1.3 Git & GitHub Setup

**What:** Version control system (tracks code changes)  
**Why:** Industry requirement, backs up your work, showcases projects  
**When to do:** Thursday 8:00-8:30 PM

#### Install Git:

**Windows:**
1. Download: [git-scm.com/download/win](https://git-scm.com/download/win)
2. Run installer with these settings:
   ```
   ✅ Default editor: Use Visual Studio Code
   ✅ Path environment: Git from command line and 3rd-party software
   ✅ HTTPS transport: Use OpenSSL library
   ✅ Line endings: Checkout Windows-style, commit Unix-style
   ✅ Terminal emulator: Use Windows' default console
   ✅ Everything else: Default
   ```

**Mac:**
1. Open Terminal
2. Type: `git --version`
3. If not installed, follow prompts to install Xcode Command Line Tools
4. Or download: [git-scm.com/download/mac](https://git-scm.com/download/mac)

**Verify:**
```bash
git --version
# Should show: git version 2.40.x or newer
```

#### Configure Git:

```bash
# In Terminal/Command Prompt:

# Set your name (will appear on commits)
git config --global user.name "Your Full Name"

# Set your email (use same as GitHub)
git config --global user.email "your.email@gmail.com"

# Set VS Code as default editor
git config --global core.editor "code --wait"

# Verify configuration
git config --list
```

#### Create GitHub Account:

1. **Go to:** [github.com](https://github.com)

2. **Sign Up:**
   ```
   Username: Choose professional (e.g., yourname-data or firstname-lastname)
   Email: Use professional email
   Password: Strong, unique password
   ```

3. **Complete Profile:**
   ```
   Profile Photo: Professional headshot or clear selfie
   Bio: "Aspiring Data Analyst | Python | SQL | Learning in Public"
   Location: Your city (helps with job searches)
   Website: LinkedIn URL
   ```

4. **Verify Email:**
   - Check email, click verification link

#### Create Your First Repository:

**On GitHub:**
```
1. Click green "New" button (top left)
2. Repository name: data-analyst-journey
3. Description: "My learning journey from zero to Data Analyst. Daily code, projects, and progress tracking."
4. ✅ Public (so recruiters can see!)
5. ✅ Initialize with README
6. Add .gitignore: Python
7. License: MIT License
8. Click "Create repository"
```

**Clone to Your Computer:**

```bash
# In Terminal/Command Prompt:

# Navigate to where you want projects
cd Documents  # or wherever you prefer

# Clone your repository
git clone https://github.com/YOUR-USERNAME/data-analyst-journey

# Navigate into it
cd data-analyst-journey

# Open in VS Code
code .
```

**Edit README:**

```markdown
# 🚀 My Data Analyst Journey

## About Me
I'm transitioning from bookkeeping to data analytics. This repository tracks my daily learning, projects, and growth over the next 5 months.

## 🎯 Goals
- Master Python for data analysis
- Become proficient in SQL
- Build 4 portfolio projects
- Land my first Data Analyst role by April 2026 (Month 5)

## 📚 Learning Path
- **Month 1:** Python & SQL fundamentals
- **Month 2:** Pandas, data visualization, first project
- **Month 3:** Advanced SQL, statistics, second project
- **Month 4-5:** Interview prep, portfolio polish, applications

## 🗂️ Repository Structure
```
data-analyst-journey/
├── week-01-learnings/     # Week 1 practice code
├── week-02-learnings/     # Week 2 practice code
├── projects/              # Portfolio projects
├── hackerrank-solutions/  # Coding challenges
├── notes/                 # Learning notes
└── learning-journal.md    # Daily progress log
```

## 📊 Progress Tracker
- [ ] Week 1 complete
- [ ] Python for Everybody Certificate
- [ ] Google Data Analytics Certificate
- [ ] First portfolio project
- [ ] 100 LinkedIn connections
- [ ] First job application

## 🔗 Connect With Me
- LinkedIn: [Your LinkedIn URL]
- Email: your.email@gmail.com

---
*Last Updated: November 20, 2025*
```

**First Commit:**

```bash
# Save README in VS Code

# In Terminal (from data-analyst-journey folder):
git add README.md
git commit -m "Initial commit: Updated README with my journey details"
git push origin main

# You'll be prompted for GitHub credentials first time
# Username: your-github-username
# Password: (use Personal Access Token, see GitHub docs if needed)
```

---

### 1.4 Jupyter Notebook Setup

**What:** Interactive coding environment (mix of code, results, notes)  
**Why:** Perfect for data analysis, experimentation, sharing work  
**When to do:** Monday 5:30-6:00 AM (Week 1)

**Installation:**

```bash
# Already installed if you ran: pip install jupyter

# Verify:
jupyter --version
# Should show: jupyter core version X.X.X
```

**Launch Jupyter:**

```bash
# In Terminal, navigate to your project folder:
cd Documents/data-analyst-journey

# Launch Jupyter:
jupyter notebook

# Browser opens automatically to: http://localhost:8888
```

**Create First Notebook:**

```
1. In Jupyter browser interface:
2. Click "New" → "Python 3"
3. Notebook opens (Untitled.ipynb)
4. Rename: Click "Untitled" → "week_01_python_notes"
```

**First Notebook Content:**

```python
# Cell 1 (Markdown):
Click dropdown "Code" → Change to "Markdown"
Type:
# Week 1 Python Learning Notes
**Date:** November 24, 2025  
**Topic:** Variables, Data Types, and Basic Operations

Press Shift+Enter to render

# Cell 2 (Code):
# Variables and Data Types
name = "Data Analyst"
age = 35
salary_goal = 75000
is_learning = True

print(f"Goal: Become a {name}")
print(f"Target salary: ${salary_goal:,}")

# Cell 3 (Code):
# Simple calculation
monthly_goal = salary_goal / 12
print(f"Monthly target: ${monthly_goal:,.2f}")

# Cell 4 (Markdown):
## Key Learnings
- Python variables don't need type declaration
- F-strings are great for formatting
- Shift+Enter runs a cell
```

**Save Notebook:**
```
File → Save and Checkpoint
Or: Cmd+S / Ctrl+S
```

**Close Jupyter:**
```
In browser: Close tabs
In Terminal: Ctrl+C (twice)
```

---

## 📊 PART 2: DATA & SQL TOOLS (Friday Evening)
**Time:** 30 minutes

### 2.1 SQLite & DB Browser

**What:** Lightweight database + visual database tool  
**Why:** Practice SQL without complex setup  
**When to do:** Friday 8:30-9:00 PM

#### Install SQLite:

**Windows:**
1. Download: [sqlite.org/download.html](https://sqlite.org/download.html)
2. Get "sqlite-tools-win32-x86-XXXXXXX.zip"
3. Extract to `C:\sqlite`
4. Add to PATH:
   ```
   Search "Environment Variables"
   Edit "Path"
   Add: C:\sqlite
   ```

**Mac:**
```bash
# SQLite comes pre-installed!
# Verify:
sqlite3 --version
```

#### Install DB Browser for SQLite:

1. **Download:** [sqlitebrowser.org](https://sqlitebrowser.org)
2. **Install:**
   - Windows: Run .msi installer
   - Mac: Drag to Applications

**Create First Database:**

```sql
1. Open DB Browser
2. New Database → Save as: practice.db (in your project folder)
3. Create Table:
   - Name: students
   - Fields:
     * id (INTEGER, Primary Key, Auto Increment)
     * name (TEXT)
     * age (INTEGER)
     * gpa (REAL)
4. Click OK

5. Insert data:
   - Browse Data tab
   - Insert Record button
   - Add 5 sample students

6. Execute SQL tab:
   - Write queries:
     SELECT * FROM students;
     SELECT name, gpa FROM students WHERE gpa > 3.5;
     SELECT AVG(gpa) as average_gpa FROM students;
```

---

## 🎓 PART 3: LEARNING PLATFORMS (Throughout Week 1)

### 3.1 Coursera Plus

**When:** Thursday 5:45 AM

1. **Sign Up:** [coursera.org/courseraplus](https://coursera.org/courseraplus)
2. **Subscription:** $59/month or $399/year (choose monthly for now)
3. **Enroll in:**
   - Python for Everybody Specialization
   - Google Data Analytics Professional Certificate
   - IBM Data Analyst Professional Certificate

**Pro Tips:**
```
✅ Set learning goals (Coursera tracks them)
✅ Download mobile app for commute learning
✅ Enable email reminders (but not too many!)
```

---

### 3.2 DataCamp

**When:** Friday morning

1. **Sign Up:** [datacamp.com](https://datacamp.com)
2. **Subscribe:** $25/month (essential for Week 1-5)
3. **Start Track:** "Data Analyst with Python"

**Setup:**
```
✅ Complete skills assessment (shows your level)
✅ Set daily goal: 30 min minimum
✅ Download mobile app
✅ Join DataCamp community
```

---

### 3.3 Practice Platforms

**HackerRank** (Friday evening):
```
1. Sign up: hackerrank.com
2. Complete profile (use same email as GitHub)
3. Start: Python track
4. Bookmark: SQL track
```

**SQLZoo** (Friday evening):
```
1. Go to: sqlzoo.net
2. No account needed!
3. Bookmark for daily practice
```

**Kaggle** (Saturday evening):
```
1. Sign up: kaggle.com
2. Complete profile
3. Verify phone (required for some features)
4. Start: Learn section → Intro to Python
```

**StrataScratch** (Saturday):
```
1. Sign up: stratascratch.com
2. Browse free questions
3. Filter by: Data Analyst, Easy difficulty
```

---

## 💼 PART 4: PROFESSIONAL PLATFORMS (Thursday Evening)

### 4.1 LinkedIn Optimization

**When:** Thursday 8:30 PM

**Profile Photo:**
```
✅ Professional headshot or clear selfie
✅ Good lighting, neutral background
✅ Smiling, approachable
✅ Business casual attire
❌ No group photos
❌ No sunglasses or hats
```

**Headline** (220 characters max):
```
Example:
"Aspiring Data Analyst | Learning Python, SQL & Data Visualization | Transitioning from Finance/Bookkeeping | Open to Remote Opportunities"
```

**About Section:**
```markdown
🔍 Who I Am:
Detail-oriented professional transitioning from 10 years of bookkeeping 
to data analytics. Currently completing comprehensive training in Python, 
SQL, and data visualization.

📊 What I'm Learning:
• Python for data analysis (Pandas, NumPy)
• SQL for data extraction and manipulation  
• Data visualization (Matplotlib, Tableau)
• Statistical analysis and business insights

🎯 What I Bring:
• Strong analytical mindset from finance background
• Attention to detail and accuracy
• Experience translating complex data into actionable insights
• Self-motivated learner committed to daily growth

💻 Current Projects:
Building portfolio of data analysis projects. Check out my GitHub: 
[Your GitHub URL]

📫 Let's Connect:
Always happy to connect with data professionals, mentors, and fellow 
learners. Feel free to reach out!

#DataAnalytics #Python #SQL #CareerTransition
```

**Experience Section:**
```
Current Role:
Title: Data Analyst (In Training) - Self-Taught
Company: Independent Learning
Dates: Jan 2026 - Present
Description:
• Completing Python for Everybody and Google Data Analytics certifications
• Building portfolio of data analysis projects using Python and SQL
• Daily coding practice: HackerRank, DataCamp, real-world datasets
• Creating data visualizations and dashboards

Previous Role:
[Your bookkeeping role - emphasize data-relevant skills]
• Maintained financial databases with 99.9% accuracy
• Generated monthly reports analyzing trends and variances
• Used Excel extensively for data analysis and forecasting
• Managed large datasets and ensured data integrity
```

**Skills:**
```
Add these skills (endorse yourself first, then ask connections):

Technical Skills:
• Python
• SQL
• Data Analysis
• Microsoft Excel
• Data Visualization
• Pandas
• NumPy
• Git/GitHub

Transferable Skills:
• Analytical Thinking
• Problem Solving
• Attention to Detail
• Time Management
```

**Creator Mode:**
```
Turn ON Creator Mode:
Settings → Creator Mode → Toggle On
Choose topics: Data Analytics, Python, SQL, Data Science
```

---

## 📱 PART 5: COMMUNICATION & PRODUCTIVITY TOOLS

### 5.1 Note-Taking Setup (Optional but Recommended)

**Notion** (Free):
```
1. Sign up: notion.so
2. Create workspace: "Data Analyst Journey"
3. Create databases:
   - Learning Log
   - Job Tracker
   - Code Snippets
   - Resources
```

**Or Obsidian** (Free, works offline):
```
1. Download: obsidian.md
2. Create vault in your project folder
3. Use markdown for everything
4. Great for linking concepts together
```

---

### 5.2 Browser Setup

**Essential Bookmarks Bar:**
```
Learning:
├── Coursera
├── DataCamp
├── Python for Everybody
├── Google Data Analytics
├── HackerRank
├── SQLZoo
└── Kaggle

Resources:
├── Python Docs
├── Pandas Docs
├── SQL Tutorial
├── Stack Overflow
└── GitHub

Career:
├── LinkedIn
├── Job Tracker Spreadsheet
├── Resume
└── Portfolio Site

Tools:
├── VS Code Web
├── Jupyter (local)
└── Your GitHub Repo
```

**Chrome Extensions:**
```
Productivity:
• StayFocusd (block distracting sites during study)
• Momentum (inspirational new tab page)
• Grammarly (for LinkedIn posts, READMEs)

Development:
• JSON Formatter
• GitHub File Icons
• Octotree (better GitHub navigation)
```

---

## 📋 SETUP VERIFICATION CHECKLIST

### Core Development (Must Have):
```
□ Python 3.11+ installed and verified
□ pip working, packages installed
□ VS Code installed with Python extension
□ Git installed and configured
□ GitHub account created
□ First repository created and cloned
□ Can run: python hello.py successfully
□ Can push to GitHub successfully
□ Jupyter Notebook working
```

### Database & SQL:
```
□ SQLite installed (or verified on Mac)
□ DB Browser for SQLite installed
□ Created first practice database
□ Can execute SQL queries
```

### Learning Platforms:
```
□ Coursera Plus subscription active
□ Enrolled in Python for Everybody
□ Enrolled in Google Data Analytics
□ DataCamp subscription active
□ Started Data Analyst with Python track
□ HackerRank account created
□ Kaggle account created
□ SQLZoo bookmarked
```

### Professional Presence:
```
□ LinkedIn profile updated
□ Professional headline set
□ About section complete
□ Creator mode enabled
□ GitHub profile complete
□ GitHub bio and photo added
```

### Optional but Helpful:
```
□ Note-taking system chosen (Notion/Obsidian)
□ Browser bookmarks organized
□ Productivity extensions installed
□ Learning journal template created
```

---

## 🆘 TROUBLESHOOTING

### Python Issues:

**"Python not recognized":**
```
Solution: Add to PATH
Windows:
1. Search "Environment Variables"
2. System Variables → Path → Edit
3. Add: C:\Users\[YourName]\AppData\Local\Programs\Python\Python311

Mac:
1. Open ~/.zshrc or ~/.bash_profile
2. Add: export PATH="/usr/local/bin/python3:$PATH"
3. Save, run: source ~/.zshrc
```

**"pip install fails":**
```
Solution: Upgrade pip
python -m pip install --upgrade pip

Or use:
python -m pip install [package]
```

---

### Git/GitHub Issues:

**"Permission denied (publickey)":**
```
Solution: Set up SSH key
1. Generate key: ssh-keygen -t ed25519 -C "your.email@gmail.com"
2. Press Enter 3 times (default location, no passphrase)
3. Copy public key: cat ~/.ssh/id_ed25519.pub
4. GitHub → Settings → SSH Keys → New SSH Key
5. Paste key, save
```

**"Can't push to GitHub":**
```
Solution: Use Personal Access Token
1. GitHub → Settings → Developer Settings
2. Personal Access Tokens → Tokens (classic)
3. Generate new token
4. Select scopes: repo, workflow
5. Generate, copy token
6. Use token as password when pushing
```

---

### VS Code Issues:

**"Python interpreter not found":**
```
Solution:
1. Cmd/Ctrl + Shift + P
2. Type: "Python: Select Interpreter"
3. Choose Python 3.11 from list
4. If not in list, browse to Python installation
```

**"Jupyter not working in VS Code":**
```
Solution:
1. Install Jupyter extension again
2. Reload VS Code
3. Create .ipynb file
4. Select kernel: Python 3.11
```

---

### Learning Platform Issues:

**"Can't access Coursera course":**
```
Solution: Verify subscription
1. Settings → My Purchases
2. Ensure Coursera Plus active
3. Try different browser
4. Clear cache/cookies
```

**"DataCamp exercises won't load":**
```
Solution:
1. Disable browser extensions
2. Try incognito/private mode
3. Clear cache
4. Try different browser
```

---

## 🎯 SETUP COMPLETION CERTIFICATE

Once everything above is complete, create this file:

**File:** `setup-complete.md`

```markdown
# ✅ SETUP COMPLETION - November 20, 2025

I, [Your Name], have successfully completed my development environment setup!

## Verified Working:
- [x] Python 3.11.7
- [x] VS Code with Python extension
- [x] Git & GitHub (first commit made!)
- [x] Jupyter Notebook
- [x] SQLite & DB Browser
- [x] All learning platform accounts
- [x] LinkedIn profile optimized
- [x] Ready to CODE!

## First Script Output:
```python
print("Environment ready! Let's build a Data Analyst career!")
```

Output: Environment ready! Let's build a Data Analyst career!

## Screenshot Evidence:
[Include screenshot of your GitHub repo]
[Include screenshot of Python --version]
[Include screenshot of first Jupyter notebook]

**Status:** READY TO LEARN 🚀

Next step: Week 1 Day 1 learning activities!
```