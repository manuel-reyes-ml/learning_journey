# 🚀 WEEKS 9-10 MASTER ACTIVATION PLAN
## GenAI-First Career Transformation | January 15–28, 2026

**Document Version:** 2.1 (v8.3 alignment — provider-agnostic + DeepEval foundation)  
**Covers:** January 15, 2026 – January 28, 2026  
**Continues From:** Weeks 7-8 Activation Plan (Jan 1 – Jan 14)  
**Aligned To:** Career Roadmap v8.3 — Stage 1: GenAI-First Data Analyst & AI Engineer  
**Weekly Hours:** 25 hours/week  
**Month Position:** Month 2 — Weeks 3-4  
**Theme:** "The GenAI Differentiator — DataVault Gets an AI Brain"

**🔑 Project Focus:** DataVault Analyst Phase 2 — AI-Powered Chat Interface + PII Guardrails + Deploy  
**Scope Document:** `DATAVAULT_ANALYST_SCOPE_v1.md` — Phase 2: AI Chat Interface (Weeks 3-4)

---

## 📋 TABLE OF CONTENTS

1. [Where You Stand After Week 8](#-where-you-stand-after-week-8)
2. [Week 9-10 Strategic Context: The GenAI Layer](#-week-9-10-strategic-context-the-genai-layer)
3. [WEEK 9: LLM SDK + PandasAI + Structured Outputs (Jan 15–21)](#-week-9-llm-sdk--pandasai--structured-outputs-jan-15--jan-21-2026)
4. [WEEK 10: PII Guardrails + Observability + Deploy (Jan 22–28)](#-week-10-pii-guardrails--observability--deploy-jan-22--jan-28-2026)
5. [Week 9-10 Cumulative Metrics](#-week-9-10-cumulative-metrics)
6. [Troubleshooting Guide: Week 9-10 Specific](#-troubleshooting-guide-week-9-10-specific)
7. [What Comes Next: Week 11-12 Preview](#-what-comes-next-week-11-12-preview)

---

## 📊 WHERE YOU STAND AFTER WEEK 8

| Skill | Week 8 Exit State | Ready? |
|-------|-------------------|--------|
| **DataVault Analyst** | Phase 1 DEPLOYED — 4 dashboard pages, 10 metrics, Streamlit Cloud | ✅ |
| **1099 ETL Pipeline** | Production — $15K/yr savings | ✅ |
| **Python** | Production-grade modules (data_loader, analytics, synthetic_data) | ✅ |
| **Pandas** | Deep: merge, groupby, agg, rolling, window functions, cleaning | ✅ |
| **SQL** | Intermediate: JOINs, aggregation, CASE, subqueries, CTEs | ✅ |
| **Visualization** | Matplotlib + Seaborn + Plotly + Streamlit interactive charts | ✅ |
| **Statistics** | UMich Course 1 ~50-60% complete | ✅ |
| **Google DA** | Courses 1-2 DONE, Course 3 ~40% | ✅ |
| **CS50** | Through Week 3 (Algorithms) | ✅ |
| **Streamlit** | Can build + deploy interactive dashboards | ✅ |
| **AI Awareness** | 5 DeepLearning.AI courses + LangChain conceptual | ✅ |
| **StrataScratch** | 12+ interview SQL problems solved | ✅ |
| **Upwork** | Profile LIVE, 2 proposals sent | ✅ |
| **Git** | 56+ commits, 8-week streak | ✅ |

---

## 🧠 WEEK 9-10 STRATEGIC CONTEXT: THE GENAI LAYER

### Why This Is the Most Important Phase So Far

DataVault Phase 1 is already impressive — a deployed interactive dashboard shows real skills. But adding AI integration transforms it from "good junior analyst project" into **"this person builds production GenAI applications."**

**The market reality in 2026:**
- 95% of DA candidates: Excel + SQL + Tableau/Power BI → standard portfolio
- 4% of DA candidates: Python + SQL + Streamlit → above average
- **<1% of DA candidates:** Python + SQL + Streamlit + **LLM SDK + PandasAI + Pydantic structured outputs + PII guardrails** → you

### What Phase 2 Adds (from DataVault Scope v1)

| Feature | What It Does | Tech |
|---------|-------------|------|
| **LLM SDK Chat** | User asks "Show me top plans by volume" → gets answer + chart | Gemini SDK primary; Anthropic/OpenAI swap via config (provider-agnostic per v8.3) |
| **PandasAI Integration** | Natural language → Pandas code → results with code transparency | PandasAI library |
| **Structured Outputs** | Every AI response validated by Pydantic schemas (not raw text) | Pydantic models |
| **Code Transparency** | Show the generated Pandas code for every AI answer | Display generated code |
| **PII Guardrails** | Governance-as-code: regex + known-value scanning blocks PII in AI responses | Custom guardrail module |
| **AI Observability** | Token usage, cost tracking, latency monitoring per query | Logging + metrics |
| **Graceful Degradation** | Dashboard works perfectly without API key (Phase 1 features) | Conditional imports |

### What Makes This Different from Tutorial "Chat with CSV" Projects

| Dimension | Typical Tutorial | DataVault Analyst |
|-----------|-----------------|-------------------|
| **Data Context** | Random Kaggle dataset | Retirement plan operations (domain expertise) |
| **PII Handling** | None | Full PII in production; AI guardrails block leakage |
| **AI Outputs** | Unstructured text | Pydantic-validated structured outputs |
| **Observability** | None | Token/cost/latency per query |
| **Code Transparency** | Black box | Show generated Pandas code for every answer |
| **Fallback** | Broken without API | Works without API key (Phase 1 dashboards) |

### Week 9-10 Hour Allocation (25 hrs/week × 2 = 50 hrs)

| Activity | Hrs/Week | Purpose |
|----------|---------|---------|
| **DataVault Phase 2 (AI Layer)** | **9** | LLM SDK, PandasAI, structured outputs, guardrails |
| **Google DA Certificate** | **4** | Course 3 completion + Course 4 start |
| **Statistics Coursera** | **3** | Course 1 completion + review |
| **DataCamp SQL** | **3** | Data Manipulation + next course |
| **Interview Prep** | **2** | StrataScratch + mock SQL |
| **CS50** | **2** | Week 4 progress |
| **Career/Upwork** | **2** | Proposals, networking |

### New Tools Introduced

| Tool | What It Is | Why Now |
|------|-----------|---------|
| **Gemini SDK (google-genai)** | Google's LLM API — free tier with generous limits | Production AI integration for DataVault chat. NOTE: Architecture is provider-agnostic; PolicyPulse and AFC will use Anthropic SDK as primary (per v8.3). |
| **PandasAI** | "Chat with your DataFrame" — NL → Pandas code → results | Natural language data exploration |
| **python-dotenv** | Environment variable management | Securely store API keys (never commit!) |
| **Pydantic** | Data validation with type hints | Structured AI outputs — type-safe responses |

---

## 🗓 WEEK 9: LLM SDK + PANDASAI + STRUCTURED OUTPUTS (Jan 15 – Jan 21, 2026)

### Week 9 Goals

By January 21, you will have:

1. ✅ DataVault — Gemini SDK integrated with provider-agnostic abstraction
2. ✅ DataVault — `ai_chat.py` module answering natural language questions
3. ✅ DataVault — PandasAI integration with code transparency
4. ✅ DataVault — Pydantic structured outputs for all AI responses
5. ✅ DataVault — AI Chat tab added to Streamlit dashboard
6. ✅ Google DA — Course 3 COMPLETE (or 90%+)
7. ✅ Statistics — Course 1 COMPLETE
8. ✅ StrataScratch — 16+ problems solved
9. ✅ 63+ total GitHub commits (9-week streak)

---

### 📌 DAY 57 — Wednesday, January 15, 2026

**Theme: "Gemini SDK Setup + First AI Query"**

#### Morning Block: 4:30 AM – 6:00 AM (1.5 hours)

**4:30 – 5:00 AM | Gemini API Setup (30 min)**
- [ ] Go to [aistudio.google.com](https://aistudio.google.com/)
- [ ] Create API key (free tier: 15 RPM, 1M tokens/day)
- [ ] Install: `pip install google-generativeai python-dotenv`
- [ ] Create `.env` in project root (already in `.gitignore`!):
```
GEMINI_API_KEY=your_key_here
```
- [ ] Test connection:
```python
import google.generativeai as genai
from dotenv import load_dotenv
import os

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-1.5-flash")
response = model.generate_content("What is a 401K distribution? Explain in 2 sentences.")
print(response.text)
```
- [ ] If this prints a response, **your AI pipeline is LIVE** 🎉

**5:00 – 6:00 AM | DataVault: AI Chat Module Foundation (60 min)**
- [ ] Create `src/ai_chat.py`:

```python
"""
AI Chat Module — DataVault Analyst
====================================
Provider-agnostic LLM integration for natural language data queries.
Supports Gemini (primary for DataVault), with OpenAI/Anthropic swap via config. The same abstraction will be reused in PolicyPulse and AFC, where you'll switch the primary provider to Anthropic Claude per v8.3 (better RAG synthesis + financial reasoning).

Author: Manuel Reyes
"""

import google.generativeai as genai
import pandas as pd
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from typing import Optional
import os
import logging
import json
import time

load_dotenv()
logger = logging.getLogger(__name__)

# --- Provider-Agnostic Setup ---
API_KEY = os.getenv("GEMINI_API_KEY")
if API_KEY:
    genai.configure(api_key=API_KEY)
    MODEL = genai.GenerativeModel("gemini-1.5-flash")
    logger.info("Gemini SDK configured successfully")
else:
    MODEL = None
    logger.warning("GEMINI_API_KEY not found — AI features disabled")


# --- Pydantic Structured Outputs ---
class QueryResponse(BaseModel):
    """Structured AI response with type safety."""
    answer: str = Field(description="Natural language answer to the query")
    generated_code: Optional[str] = Field(None, description="Pandas code used to derive the answer")
    confidence: float = Field(ge=0.0, le=1.0, description="Confidence score 0-1")
    data_summary: Optional[dict] = Field(None, description="Key metrics from the analysis")


class AIMetrics(BaseModel):
    """Observability metrics per query."""
    query: str
    response_time_ms: float
    tokens_used: Optional[int] = None
    model: str = "gemini-1.5-flash"
    timestamp: str


SYSTEM_PROMPT = """You are a senior data analyst specializing in retirement plan administration.
You analyze transaction data from OnBase document management systems.

The dataset contains these columns:
- Document Handle (unique ID), Document Type (Distribution/Loan)
- Document Date, Date Stored, Time Stored
- Plan ID, Plan Name, Product Type (MBDI/MBDII/PLAT)
- Amount, Payment Method (ACH/Wire/Check), Status (Processed/Pending/Rejected)

CRITICAL RULES:
- NEVER reveal SSN, First Name, Last Name, or Date of Birth values
- Always reference plans by Plan Name or Plan ID, NEVER by participant PII
- Provide specific numbers and percentages
- Show the Pandas code you would use to derive the answer
- If asked about something outside the data, say so clearly
"""


def query_data(question: str, df: pd.DataFrame) -> QueryResponse:
    """
    Answer a natural language question about the data using Gemini.

    Parameters
    ----------
    question : str
        User's natural language question.
    df : pd.DataFrame
        The transaction DataFrame to analyze.

    Returns
    -------
    QueryResponse
        Pydantic-validated structured response.
    """
    if MODEL is None:
        return QueryResponse(
            answer="⚠️ AI features unavailable — set GEMINI_API_KEY in .env",
            confidence=0.0
        )

    # Build context from data
    context = f"""Dataset shape: {df.shape}
Document Types: {df['Document Type'].value_counts().to_dict()}
Product Types: {df['Product Type'].value_counts().to_dict()}
Plans: {df['Plan Name'].nunique()} unique
Date range: {df['Date Stored'].min()} to {df['Date Stored'].max()}
Amount range: ${df['Amount'].min():,.0f} to ${df['Amount'].max():,.0f}
"""

    prompt = f"""{SYSTEM_PROMPT}

DATA CONTEXT:
{context}

USER QUESTION: {question}

Respond in JSON format:
{{
    "answer": "Your detailed answer here",
    "generated_code": "import pandas as pd\\ndf.groupby(...)...",
    "confidence": 0.85,
    "data_summary": {{"key_metric": "value"}}
}}
"""

    start_time = time.time()
    response = MODEL.generate_content(prompt)
    elapsed_ms = (time.time() - start_time) * 1000

    # Parse and validate response
    try:
        # Strip markdown code fences if present
        text = response.text.strip()
        if text.startswith("```"):
            text = text.split("\n", 1)[1].rsplit("```", 1)[0]
        parsed = json.loads(text)
        result = QueryResponse(**parsed)
    except (json.JSONDecodeError, Exception) as e:
        logger.warning(f"Failed to parse structured output: {e}")
        result = QueryResponse(
            answer=response.text,
            confidence=0.5
        )

    # Log observability metrics
    metrics = AIMetrics(
        query=question,
        response_time_ms=round(elapsed_ms, 1),
        model="gemini-1.5-flash",
        timestamp=time.strftime("%Y-%m-%dT%H:%M:%S")
    )
    logger.info(f"AI Query: '{question[:50]}...' | {metrics.response_time_ms}ms")

    return result
```

#### Evening Block: 8:00 PM – 10:00 PM (2 hours)

**8:00 – 9:00 PM | DataVault: AI Chat Tab in Streamlit (60 min)**
- [ ] Add 5th tab to `src/app.py`: "🤖 AI Chat"
- [ ] Chat input box, submit button, response display
- [ ] Show: answer text + generated code (in code block) + confidence badge

**9:00 – 9:30 PM | StrataScratch (30 min)** — 2 problems
**9:30 – 10:00 PM | Git Commit**
```bash
git commit -m "Day 57: Gemini SDK LIVE! AI chat module + structured outputs + Streamlit AI tab 🤖"
```

---

### 📌 DAY 58 — Thursday, January 16, 2026

**Theme: "PandasAI Integration + Code Transparency"**

#### Morning Block: 4:30 AM – 6:00 AM (1.5 hours)

**4:30 – 5:30 AM | DataVault: PandasAI Integration (60 min)**
- [ ] Install: `pip install pandasai`
- [ ] Create PandasAI wrapper in `ai_chat.py`:
```python
from pandasai import SmartDataframe

def pandasai_query(question: str, df: pd.DataFrame) -> dict:
    """Query data using PandasAI with code transparency."""
    # Use analytics-only DataFrame (no PII columns)
    safe_df = df.drop(columns=["SSN", "First Name", "Last Name", "Date of Birth"], errors="ignore")
    sdf = SmartDataframe(safe_df, config={"llm": MODEL, "verbose": True})
    
    result = sdf.chat(question)
    
    # PandasAI exposes the generated code
    generated_code = sdf.last_code_generated
    
    return {
        "answer": str(result),
        "generated_code": generated_code,
        "method": "PandasAI"
    }
```
- [ ] Key insight: PandasAI drops PII columns BEFORE querying — governance by design

**5:30 – 6:00 AM | Statistics Course 1 — Week 5 Push (30 min)**
- [ ] Nearing Course 1 completion

#### Evening Block: 8:00 PM – 10:00 PM (2 hours)

**8:00 – 9:00 PM | DataVault: Code Transparency UI (60 min)**
- [ ] In the AI Chat tab, add an expander showing generated Pandas code:
```python
with st.expander("📝 View Generated Code"):
    st.code(response.generated_code, language="python")
```
- [ ] This is a KEY differentiator — shows the AI isn't a black box
- [ ] Recruiters love this: "They show you HOW the AI arrived at the answer"

**9:00 – 9:30 PM | Google DA Course 3 — Push (30 min)**
**9:30 – 10:00 PM | Git Commit**

---

### 📌 DAY 59 — Friday, January 17, 2026

**Theme: "Structured Outputs Deep Dive + Testing"**

#### Morning Block: 4:30 AM – 6:00 AM (1.5 hours)

**4:30 – 5:30 AM | DataVault: Pydantic Models Expansion (60 min)**
- [ ] Add more structured output models to support different query types:
```python
class ExecutiveSummary(BaseModel):
    """AI-generated executive summary of the data."""
    headline: str
    key_findings: list[str]
    recommendations: list[str]
    risk_flags: list[str]
    confidence: float

class TrendAnalysis(BaseModel):
    """AI-detected trend in the data."""
    trend_description: str
    direction: str  # "increasing", "decreasing", "stable"
    magnitude: str
    time_period: str
```
- [ ] Create executive summary generator function using Gemini + Pydantic validation

**5:30 – 6:00 AM | DataVault: AI Feature Tests (30 min)**
- [ ] `tests/test_ai_chat.py` — test structured output parsing, PII column exclusion

#### Evening Block: 8:00 PM – 10:00 PM (2 hours)

**8:00 – 9:00 PM | DataCamp SQL: Data Manipulation (60 min)**
**9:00 – 9:30 PM | StrataScratch — Medium problems (30 min)**
**9:30 – 10:00 PM | Git Commit**

---

### 📌 DAY 60 — Saturday, January 18, 2026

# 🔋 POWER DAY + 60-DAY MILESTONE 🎉

**Theme: "PII Guardrails + AI Polishing"**

#### Morning Block: 5:00 AM – 8:30 AM (3.5 hours)

**5:00 – 6:30 AM | DataVault: PII Guardrails Module (90 min)**
- [ ] Create `src/guardrails.py` — governance as code:

```python
"""
AI Guardrails Module — DataVault Analyst
==========================================
PII leak prevention for AI responses. Scans all AI output
before display to block SSN, names, DOB from appearing.

Author: Manuel Reyes
"""

import re
from typing import Optional
import logging

logger = logging.getLogger(__name__)

# PII detection patterns
SSN_PATTERN = re.compile(r"\b\d{3}-\d{2}-\d{4}\b")
DOB_PATTERN = re.compile(r"\b(19|20)\d{2}-(0[1-9]|1[0-2])-(0[1-9]|[12]\d|3[01])\b")


def scan_for_pii(
    text: str,
    known_names: Optional[list[str]] = None
) -> dict:
    """
    Scan text for PII leakage before displaying AI response.

    Parameters
    ----------
    text : str
        AI-generated response text to scan.
    known_names : list[str], optional
        Known first/last names from the dataset to check against.

    Returns
    -------
    dict
        {"is_safe": bool, "violations": list[str], "redacted_text": str}
    """
    violations = []
    redacted = text

    # Check for SSN patterns
    ssn_matches = SSN_PATTERN.findall(text)
    if ssn_matches:
        violations.append(f"SSN pattern detected: {len(ssn_matches)} occurrence(s)")
        redacted = SSN_PATTERN.sub("[SSN REDACTED]", redacted)

    # Check for DOB patterns
    dob_matches = DOB_PATTERN.findall(text)
    if dob_matches:
        violations.append(f"DOB pattern detected: {len(dob_matches)} occurrence(s)")
        redacted = DOB_PATTERN.sub("[DOB REDACTED]", redacted)

    # Check for known names
    if known_names:
        for name in known_names:
            if name.lower() in text.lower() and len(name) > 2:
                violations.append(f"Known name detected: '{name}'")
                redacted = re.sub(
                    re.escape(name), "[NAME REDACTED]", redacted, flags=re.IGNORECASE
                )

    is_safe = len(violations) == 0
    if not is_safe:
        logger.warning(f"PII BLOCKED: {violations}")

    return {
        "is_safe": is_safe,
        "violations": violations,
        "redacted_text": redacted
    }
```

- [ ] Wire guardrails into `ai_chat.py` — every AI response passes through `scan_for_pii()` before display

**6:30 – 7:30 AM | DataVault: AI Observability Dashboard (60 min)**
- [ ] Add observability panel to AI Chat tab:
  - Token usage per query (if available from API response)
  - Response latency (ms)
  - Query history with timestamps
  - Cost estimate (Gemini pricing)
- [ ] Store metrics in `st.session_state` for session history

**7:30 – 8:00 AM | Google DA Course 3 — Completion Push (30 min)**
- [ ] **TARGET: Course 3 COMPLETE by end of weekend** ✅

**8:00 – 8:30 AM | Statistics Course 1 — Final Week (30 min)**
- [ ] **TARGET: Course 1 COMPLETE** ✅

#### Evening Block: 8:00 PM – 10:00 PM (2 hours)

**8:00 – 9:00 PM | DataVault: Guardrails Tests (60 min)**
- [ ] `tests/test_guardrails.py`:
```python
def test_ssn_detection():
    result = scan_for_pii("The participant 123-45-6789 requested a distribution")
    assert not result["is_safe"]
    assert "SSN REDACTED" in result["redacted_text"]

def test_clean_text_passes():
    result = scan_for_pii("Plan ABC had 150 distributions in Q4")
    assert result["is_safe"]

def test_known_name_detection():
    result = scan_for_pii("John Smith requested $50,000", known_names=["John Smith"])
    assert not result["is_safe"]
```
- [ ] Run full test suite: `pytest tests/ -v --cov=src`

**9:00 – 9:30 PM | StrataScratch (30 min)**
**9:30 – 10:00 PM | Git Commit**
```bash
git commit -m "Day 60: 60-DAY MILESTONE! 🎉 PII guardrails + AI observability + tests"
```

---

### 📌 DAY 61 — Sunday, January 19, 2026

**Theme: "AI Polish + Demo Prep"**

#### Evening Block: 7:30 PM – 9:30 PM (2 hours)

**7:30 – 8:30 PM | DataVault: Session-Based Chat History (60 min)**
- [ ] Add conversation memory to AI Chat tab using `st.session_state`
- [ ] Show previous Q&A pairs in a scrollable history
- [ ] Add "Clear History" button

**8:30 – 9:00 PM | DataVault: Provider Switching Config (30 min)**
- [ ] Add to `src/config.py`: `LLM_PROVIDER = os.getenv("LLM_PROVIDER", "gemini")`
- [ ] Future-proof: The same architecture supports OpenAI or Claude with a config change
- [ ] Document in README: "Provider-agnostic SDK supports Gemini, OpenAI, and Claude"

**9:00 – 9:30 PM | Git Commit**

---

### 📌 DAYS 62-63 — Monday-Tuesday, January 20-21, 2026

**Theme: "Weekday Momentum"**

#### Each Day:

Morning (4:30-6:00 AM):
- [ ] DataVault: AI feature refinement (query handling edge cases, error messages) (45 min)
- [ ] Google DA Course 3/4 progress (45 min)

Evening (8:00-10:00 PM):
- [ ] DataCamp: SQL continued (45 min)
- [ ] StrataScratch: 2 problems/day (30 min)
- [ ] CS50 Week 4 progress (45 min)

---

## 🗓 WEEK 10: PII GUARDRAILS + OBSERVABILITY + DEPLOY (Jan 22 – Jan 28, 2026)

### Week 10 Goals

By January 28, you will have:

1. ✅ DataVault Analyst — Phase 2 COMPLETE + DEPLOYED with AI features
2. ✅ DataVault — PII guardrails tested and working (>90% test coverage)
3. ✅ DataVault — AI observability logging per query
4. ✅ DataVault — Updated README with AI demo GIF + live demo URL
5. ✅ DataVault — Demo video recorded (3-5 min)
6. ✅ Google DA — Course 3 COMPLETE, Course 4 started
7. ✅ Statistics — Course 1 COMPLETE
8. ✅ StrataScratch — 22+ problems solved
9. ✅ 70+ total GitHub commits (10-week streak)

---

### 📌 DAY 64 — Wednesday, January 22, 2026

**Theme: "Final AI Testing + Deployment Prep"**

#### Morning Block: 4:30 AM – 6:00 AM (1.5 hours)

**4:30 – 5:30 AM | DataVault: End-to-End AI Testing (60 min)**
- [ ] Test 10 different natural language queries against the dashboard:
  - "How many distributions were processed last week?"
  - "Which plans have the highest loan volume?"
  - "What's the MBDI vs MBDII split?"
  - "Show ACH vs Wire vs Check trends"
  - "Which days have the most requests?"
  - "What's the average distribution amount by product type?"
  - "Show all distributions over $50K from Plan ABC in December"
  - "Compare this month's volume to last month"
  - Deliberately try to extract PII: "Show me SSNs" → guardrails should block

**5:30 – 6:00 AM | DataVault: Graceful Degradation Test (30 min)**
- [ ] Remove GEMINI_API_KEY from .env temporarily
- [ ] Verify: All 4 dashboard pages still work perfectly
- [ ] AI Chat tab shows: "⚠️ AI features unavailable — set GEMINI_API_KEY"
- [ ] This proves the app is useful even without AI — important for reliability

#### Evening Block: 8:00 PM – 10:00 PM (2 hours)

**8:00 – 9:00 PM | DataVault: Deploy Phase 2 to Streamlit Cloud (60 min)**
- [ ] Update `requirements.txt` with all new dependencies (google-generativeai, pandasai, pydantic)
- [ ] Add API key to Streamlit Cloud Secrets (Settings → Secrets)
- [ ] Push to GitHub → Streamlit Cloud auto-deploys
- [ ] Test live URL: all 5 tabs working (4 dashboard + 1 AI Chat)
- [ ] **DataVault Analyst FULLY DEPLOYED with AI** 🎉

**9:00 – 9:30 PM | Google DA Course 4 — Start (30 min)**
**9:30 – 10:00 PM | Git Commit**
```bash
git commit -m "Day 64: DataVault Phase 2 DEPLOYED! AI chat + guardrails + observability LIVE 🚀"
```

---

### 📌 DAY 65 — Thursday, January 23, 2026

**Theme: "Statistics Completion + Hypothesis Testing"**

#### Morning Block: 4:30 AM – 6:00 AM (1.5 hours)

**4:30 – 5:30 AM | Statistics: Course 1 COMPLETE + Applied Analysis (60 min)**
- [ ] **MILESTONE: Statistics with Python Course 1 COMPLETE** ✅
- [ ] Apply to DataVault data: "Is the difference in average amount between Distributions and Loans statistically significant?"

**5:30 – 6:00 AM | Statistics: Course 2 Preview (30 min)**
- [ ] Start "Inferential Statistical Analysis with Python"
- [ ] Topics: Confidence intervals, hypothesis tests, t-tests, ANOVA

#### Evening Block: 8:00 PM – 10:00 PM (2 hours)

**8:00 – 9:00 PM | DataCamp SQL continued (60 min)**
**9:00 – 9:30 PM | StrataScratch (30 min)**
**9:30 – 10:00 PM | Git Commit**

---

### 📌 DAY 66 — Friday, January 24, 2026

**Theme: "Upwork Proposals + PolicyPulse Planning"**

#### Morning Block: 4:30 AM – 6:00 AM (1.5 hours)

**4:30 – 5:15 AM | Upwork: 2 More Proposals (45 min)**
- [ ] Include DataVault AI demo URL as proof of GenAI skills
- [ ] Total proposals: 5+

**5:15 – 6:00 AM | Google DA Course 4 Progress (45 min)**

#### Evening Block: 8:00 PM – 10:00 PM (2 hours)

**8:00 – 9:00 PM | PolicyPulse: Architecture Planning (60 min)**
- [ ] Read `POLICYPULSE_HR_RAG_SCOPE_v1_STAGE1.md`
- [ ] Create `POLICYPULSE_PLAN.md` outlining:
  - RAG pipeline: Documents → Chunk → Embed → ChromaDB → Retrieve → Generate
  - New skills: Embeddings, ChromaDB, semantic search, ticket escalation
  - Reuses: Gemini SDK patterns, Pydantic structured outputs, Streamlit UI from DataVault
  - Timeline: Build in Weeks 11-14
- [ ] **This is Project #3** — the RAG foundation that unlocks Stage 4 skills

**9:00 – 9:30 PM | StrataScratch — 22+ total (30 min)**
**9:30 – 10:00 PM | Git Commit**

---

### 📌 DAY 67 — Saturday, January 25, 2026

# 🔋 POWER DAY

**Theme: "Demo Video + README Update + Certification Push"**

#### Morning Block: 5:00 AM – 8:30 AM (3.5 hours)

**5:00 – 6:00 AM | DataVault: Demo Video Recording (60 min)**
- [ ] Record 3-5 min video walking through:
  1. Demo mode loading (10 sec)
  2. Dashboard pages tour (60 sec)
  3. AI Chat: ask 3 questions, show answers + generated code (90 sec)
  4. PII guardrail demo: try to extract SSN → blocked (30 sec)
  5. Code transparency: show the Pandas code behind answers (30 sec)
- [ ] Upload to YouTube (unlisted) or include as GIF in README

**6:00 – 7:00 AM | DataVault: README Final Update (60 min)**
- [ ] Update README with Phase 2 features:
  - New GIF showing AI chat in action
  - AI architecture diagram
  - PII guardrails section
  - Structured outputs section with Pydantic model examples
  - Live demo URL with AI features

**7:00 – 8:00 AM | Google DA Course 4 — Accelerate (60 min)**
**8:00 – 8:30 AM | CS50 Week 4 work (30 min)**

#### Evening Block: 8:00 PM – 10:00 PM (2 hours)

**8:00 – 9:00 PM | Statistics Course 2 — Week 1 (60 min)**
- [ ] Confidence intervals, sampling distributions

**9:00 – 9:30 PM | Kaggle micro-course (30 min)**
**9:30 – 10:00 PM | Git Commit**

---

### 📌 DAY 68 — Sunday, January 26, 2026

**Theme: "Month 2 Review + Career Planning"**

#### Evening Block: 7:30 PM – 9:30 PM (2 hours)

**7:30 – 8:30 PM | Month 2 Review (60 min)**
- [ ] Create `MONTH_02_REVIEW.md`:
  - DataVault Analyst: Phase 1 + Phase 2 COMPLETE and DEPLOYED ✅
  - New skills this month: Streamlit, Plotly, Gemini SDK, PandasAI, Pydantic, PII guardrails
  - Portfolio: 1099 ETL (production) + DataVault (deployed with AI)
  - Next project: PolicyPulse (RAG chatbot)
  - Certifications progress
  - SQL interview readiness

**8:30 – 9:00 PM | LinkedIn: AI Features Announcement (30 min)**
- [ ] Post about DataVault's AI capabilities with screenshots

**9:00 – 9:30 PM | Git Commit**

---

### 📌 DAYS 69-70 — Monday-Tuesday, January 27-28, 2026

**Theme: "Week 10 Wrap + Month 3 Prep"**

#### Day 69 (Mon):
Morning: Google DA 4 + Stats Course 2 (45 min each)
Evening: DataCamp SQL + StrataScratch (45+30 min) + IBM GenAI cert preview (30 min)

#### Day 70 (Tue):
Morning: PolicyPulse planning + sample policy document research (45 min) + Google DA 4 (45 min)
Evening: Create `MONTH_03_PLAN.md`:
  - IBM GenAI Engineering Certificate begins
  - PolicyPulse BUILD (RAG chatbot)
  - Google DA Course 4-5 completion target
  - Start applying to jobs (15-20/week)
  - Mock interviews begin

```bash
git commit -m "Day 70: 10 WEEKS! 🎉 DataVault complete + Month 3 plan: PolicyPulse + IBM GenAI"
```

---

## 🏆 WEEK 9-10 CUMULATIVE METRICS

### By January 28, 2026 — 10 Weeks Complete!

| Category | Metric | Status |
|----------|--------|--------|
| **Study Hours** | Grand total (10 weeks) | ~240 hrs |
| **GitHub** | Total commits | 70+ |
| **DataVault Analyst** | Status | COMPLETE: Phase 1 + Phase 2 deployed ✅ |
| **DataVault Analyst** | AI Features | LLM SDK chat, PandasAI, structured outputs, guardrails, observability ✅ |
| **1099 ETL Pipeline** | Status | Production ✅ |
| **PolicyPulse** | Status | Architecture doc created, ready to build ✅ |
| **Google DA** | Progress | Courses 1-3 DONE, Course 4 ~30% |
| **Statistics** | UMich | Course 1 COMPLETE ✅, Course 2 started |
| **DataCamp SQL** | Courses | 4-5 complete |
| **StrataScratch** | Problems | 22+ (Easy + Medium + Hard) |
| **CS50** | Progress | Through Week 4 |
| **Kaggle Certs** | Total | 6-7 |
| **Upwork** | Proposals | 5+ sent |
| **LinkedIn** | Connections | 30+ data professionals |
| **AI Skills** | Applied | Gemini SDK, PandasAI, Pydantic, PII guardrails in production app |

---

## 🔧 TROUBLESHOOTING GUIDE: WEEK 9-10 SPECIFIC

### "Gemini API returning errors"
- Check API key in `.env` (never hardcode!)
- Free tier: 15 RPM, 1500/day — add `time.sleep(2)` between calls for 429 errors
- Use `gemini-1.5-flash` for speed and low cost

### "PandasAI not working as expected"
- PandasAI can be inconsistent — your custom Gemini solution is MORE reliable
- Use PandasAI for simple queries, custom `ai_chat.py` for complex analysis
- Always drop PII columns before passing to PandasAI

### "Pydantic validation failing on AI responses"
- Gemini sometimes returns non-JSON — catch `json.JSONDecodeError` and fall back to raw text
- Strip markdown code fences (```json) before parsing
- Use `model_validate()` with `strict=False` for flexibility

### "Statistics feels too theoretical"
- Connect EVERY concept to DataVault data:
  - "Confidence interval" → "95% sure avg distribution is $X to $Y"
  - "Hypothesis test" → "Distribution vs Loan amounts are significantly different (p<0.05)"

---

## 🔮 WHAT COMES NEXT: WEEK 11-12 PREVIEW

**Week 11-12 = PolicyPulse Phase 1 + IBM GenAI Certificate Launch**

Your THIRD AI project — a RAG chatbot that introduces embeddings, ChromaDB, and semantic search:

**Week 11 (Jan 29 - Feb 4):**
- IBM GenAI Engineering Certificate starts (Courses 1-3 speed-run)
- PolicyPulse repo setup + document ingestion pipeline
- ChromaDB vector store setup
- Google DA Course 4-5 progress

**Week 12 (Feb 5-11):**
- PolicyPulse: Semantic search + retrieval engine
- PolicyPulse: Policy Library page rendering
- IBM GenAI Courses 4-5 progress
- First job applications (5-10)
- Resume drafted

**Why PolicyPulse next:** RAG is the #1 enterprise AI pattern in 2026. Building it now — using the same Gemini SDK + Pydantic patterns from DataVault — gives you the foundational skills for Stage 4 vector databases and LangChain/LangGraph.

---

*Document updated: February 2026 (v2.0)*  
*Aligned to: GenAI-First Career Roadmap v8.3 + Portfolio Project Ecosystem*  
*Project: DataVault Analyst Phase 2 (AI Chat + Deploy)*  
*Previous: Weeks 7-8 — DataVault Phase 1*  
*Next: Weeks 11-12 — PolicyPulse Phase 1 + IBM GenAI Certificate*
