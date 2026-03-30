# 🔍 ROADMAP v8.1 — COMPREHENSIVE REVIEW, CHANGES & PROJECT SCOPE UPDATES

## Expert Tech Career Coach Analysis — March 29, 2026
## For: Manuel Reyes | Goal: Junior AI Engineer ASAP + Production-Grade Portfolio

**Status:** 📋 DRAFT — Awaiting Manuel's Approval Before Any Changes  
**Scope:** Roadmap v8.1 changes + Course recommendations + All 7 project scope updates

---

## 📋 Table of Contents

1. [Evaluation Frameworks — Full Clarification](#1-evaluation-frameworks)
2. [Roadmap Changes Summary](#2-roadmap-changes-summary)
3. [Stage 1 Changes (Detailed)](#3-stage-1-changes)
4. [Stage 2 Changes (Detailed)](#4-stage-2-changes)
5. [Stage 3 Changes (Detailed)](#5-stage-3-changes)
6. [Course Recommendations (Researched)](#6-course-recommendations)
7. [Project Scope Additions — All 7 Projects](#7-project-scope-additions)

---

## 1. Evaluation Frameworks — Full Clarification

### 1.1 What Are LLM Evaluation Frameworks?

Yes, you're on the right track. Here's the full landscape, organized by category:

**Category A: LLM Evaluation Libraries (Code-Level Testing)**
These are Python libraries you integrate into your projects to measure AI output quality. Think of them as "pytest for AI."

| Framework | What It Does | Best For | Cost |
|-----------|-------------|----------|------|
| **DeepEval** | pytest-compatible LLM evaluation with 14+ metrics (faithfulness, answer relevancy, hallucination, etc.) | RAG evaluation, agent testing, production CI/CD | FREE (open-source) |
| **RAGAS** | Research-backed RAG evaluation metrics (context precision, recall, faithfulness) | RAG-specific evaluation | FREE (open-source) |

**Category B: Observability & Tracing Platforms**
These platforms help you trace, debug, and monitor LLM app behavior in production.

| Platform | What It Does | Best For | Cost |
|----------|-------------|----------|------|
| **LangSmith** | Tracing, debugging, dataset management for LangChain/LangGraph apps | Production monitoring, evaluation datasets | Free tier available |
| **Arize Phoenix** | Open-source LLM observability, tracing, evaluation | RAG debugging, hallucination detection | FREE (open-source) |

**Category C: LLM-as-Judge (built into DeepEval/RAGAS)**
Using an LLM to evaluate another LLM's output. This is a *technique* used inside frameworks like DeepEval, not a separate tool.

### 1.2 What You Should Use in Your Projects

For your Stage 1 projects, the practical choice is:

- **DeepEval** — Primary evaluation framework (pytest-compatible, matches your existing test strategy)
- **RAGAS metrics via DeepEval** — DeepEval can run RAGAS metrics natively, so you get both in one library
- **LangSmith** — Defer to Stage 4 (LangChain/LangGraph ecosystem)

**Why DeepEval wins for you right now:**
- It integrates with pytest (you already use pytest in every project)
- It's `pip install deepeval` — no complex setup
- It provides self-explaining metrics (tells you WHY a score is low, not just the number)
- It works with Gemini, OpenAI, and Claude (your provider-agnostic pattern)

### 1.3 Key Metrics to Add to Your Projects

| Metric | What It Measures | Use In |
|--------|-----------------|--------|
| **Answer Relevancy** | Does the AI answer actually address the question? | All AI projects |
| **Faithfulness** | Is the output grounded in the provided context (no hallucination)? | PolicyPulse, DataVault |
| **Contextual Precision** | Are the most relevant chunks ranked highest in retrieval? | PolicyPulse (RAG) |
| **Contextual Recall** | Does the retrieval context cover all aspects of the expected answer? | PolicyPulse (RAG) |
| **Hallucination** | Does the output contain fabricated information? | All AI projects |
| **Tool Correctness** | Did the agent call the right tool with the right parameters? | Stage 4 (agents) |

---

## 2. Roadmap Changes Summary

| # | Change | Stage | Priority |
|---|--------|-------|----------|
| 1 | **ADD** Docker fundamentals course (Stage 1 glance + Stage 2 deep) | 1 & 2 | HIGH |
| 2 | **ADD** DeepEval/RAGAS evaluation framework (Stage 1 intro + all projects) | 1 | HIGH |
| 3 | **REMOVE** TensorFlow Developer Certificate (discontinued May 2024) | 3 | HIGH |
| 4 | **ADD** Snowflake/BigQuery exposure | 2 | MEDIUM |
| 5 | **CLARIFY** IBM GenAI Engineering cert placement (remove Stage 2 duplicate) | 1 & 2 | MEDIUM |
| 6 | **ADD** DeepLearning.AI "Building and Evaluating Advanced RAG" (FREE) | 1 | HIGH |
| 7 | **ADD** DeepLearning.AI "Retrieval Augmented Generation (RAG)" on Coursera | 2 | MEDIUM |
| 8 | **CONSIDER** Compressing Stage 3 from 14 → 10-12 months | 3 | LOW |

---

## 3. Stage 1 Changes (Detailed)

### 3.1 ADD: Docker Fundamentals (Glance — 1 week, Month 5)

**Why in Stage 1:** You want to apply for Junior AI Engineer roles. Docker appears in 60%+ of AI/ML job postings. Even a basic understanding ("I can containerize my Streamlit apps") separates you from other DA candidates.

**Scope for Stage 1 (lightweight intro):**
- What containers are and why they matter
- `Dockerfile` basics (containerize a Python app)
- `docker-compose` for multi-service apps (e.g., Streamlit + ChromaDB)
- Add a `Dockerfile` to at least 1 portfolio project (PolicyPulse or DataVault)

**Recommended Course:**

> **Best Option: "Docker for Beginners with Hands-on Labs" (KodeKloud on Coursera)**  
> - Platform: Coursera (included in your Coursera Plus)  
> - Duration: ~6 hours (1 week at your pace)  
> - Why: Hands-on labs in-browser (no local setup needed), covers Dockerfile, Docker Compose, and basics of orchestration. KodeKloud is known for practical DevOps training.  
> - URL: https://www.coursera.org/learn/docker-for-the-absolute-beginner  
> - Certificate: Yes  

> **Alternative: "Introduction to Docker" (LearnQuest on Coursera)**  
> - Platform: Coursera (included in your Coursera Plus)  
> - Duration: ~10 hours (1 week)  
> - Why: More structured (3 modules), covers Dockerfile, volumes, networking, and Docker Compose with Python projects specifically.  
> - URL: https://www.coursera.org/learn/introduction-to-docker  
> - Certificate: Yes  

**Stage 2 Deep Dive (Month 12-13):**
The full Docker + Kubernetes mastery happens in Stage 2 alongside Airflow:

> **"Docker and Kubernetes Masterclass: From Beginner to Advanced" (Packt on Coursera)**  
> - Platform: Coursera (included in your Coursera Plus)  
> - Duration: ~40 hours (4-6 weeks)  
> - Why: Covers Docker → Kubernetes → GKE deployment. Bridges directly into your AWS deployment skills.  
> - URL: https://www.coursera.org/specializations/packt-docker-and-kubernetes-masterclass-from-beginner-to-advanced  
> - Certificate: Yes  

### 3.2 ADD: LLM Evaluation Frameworks (Intro — integrated into project work, Month 4-5)

**Why in Stage 1:** Evaluation-driven development is the #1 differentiator hiring managers scan for in 2026. Adding even basic evaluation metrics to PolicyPulse immediately signals production maturity.

**Scope for Stage 1:**
- `pip install deepeval` and write 3-5 evaluation test cases for PolicyPulse
- Measure: answer_relevancy, faithfulness, contextual_precision for RAG answers
- Add evaluation results to README (shows metrics-driven thinking)
- Basic concept: "I evaluate my AI's output quality, not just whether it runs"

**Recommended Courses:**

> **Best Option: "Building and Evaluating Advanced RAG Applications" (DeepLearning.AI — FREE)**  
> - Platform: DeepLearning.AI (free, no account needed)  
> - Duration: ~1 hour  
> - Why: Teaches the RAG Triad (Context Relevance, Groundedness, Answer Relevance) using TruLens/TruEra evaluation. Directly applicable to your PolicyPulse project. Uses LlamaIndex but concepts transfer.  
> - URL: https://www.deeplearning.ai/short-courses/building-evaluating-advanced-rag/  
> - Certificate: Yes  

> **Alternative: "Retrieval Augmented Generation (RAG)" (DeepLearning.AI on Coursera)**  
> - Platform: Coursera (included in your Coursera Plus)  
> - Duration: ~20 hours (multi-week course)  
> - Why: Comprehensive RAG course that covers evaluation, deployment, observability. Includes Weaviate vector DB and Phoenix (Arize) for tracing. More depth than the short course.  
> - URL: https://www.coursera.org/learn/retrieval-augmented-generation-rag  
> - Certificate: Yes  
> - Note: This could replace your Stage 2 "RAG - Production Ready" DeepLearning.AI short course since it's more comprehensive.  

**Self-Study Resource (no course needed):**
- DeepEval docs: https://deepeval.com/docs — excellent, example-driven documentation
- GitHub: https://github.com/confident-ai/deepeval — 14+ metrics, pytest integration
- Install: `pip install deepeval --break-system-packages`

### 3.3 ADD: Roadmap HTML Change — New Row in Stage 1 Courses Table

```html
<tr style="background-color: #e8f5e9;">
    <td><strong><a href="https://www.deeplearning.ai/short-courses/building-evaluating-advanced-rag/" target="_blank">🆕🤖 Building & Evaluating Advanced RAG (DeepLearning.AI)</a></strong></td>
    <td><strong><a href="https://www.deeplearning.ai/" target="_blank">DeepLearning.AI</a></strong></td>
    <td><span class="badge badge-free">FREE</span></td>
    <td>✅ Yes</td>
    <td>1 hour</td>
    <td><strong>EVALUATION-DRIVEN DEVELOPMENT!</strong> Learn the RAG Triad (Context Relevance, Groundedness, Answer Relevance). Apply directly to PolicyPulse. Shows recruiters you measure AI quality, not just build it. Take alongside PolicyPulse project!</td>
</tr>
<tr style="background-color: #e8f5e9;">
    <td><strong><a href="https://www.coursera.org/learn/docker-for-the-absolute-beginner" target="_blank">🆕 Docker for Beginners with Hands-on Labs (KodeKloud)</a></strong></td>
    <td><strong><a href="https://www.coursera.org/" target="_blank">Coursera</a></strong></td>
    <td><span class="badge badge-included">Included</span></td>
    <td>✅ Yes</td>
    <td>6 hours (1 week)</td>
    <td><strong>CONTAINERIZATION INTRO!</strong> Learn Dockerfile, Docker Compose, container basics. Add Dockerfile to 1 portfolio project. 60%+ of AI/ML job postings require Docker. Quick win for Junior AI Engineer applications!</td>
</tr>
```

---

## 4. Stage 2 Changes (Detailed)

### 4.1 ADD: Docker + Kubernetes Deep Dive (Month 12-13)

Insert as course **7.5** (between Airflow and dbt):

```html
<tr style="background-color: #e3f2fd;">
    <td><strong>7️⃣.5</strong></td>
    <td><strong><a href="https://www.coursera.org/specializations/packt-docker-and-kubernetes-masterclass-from-beginner-to-advanced" target="_blank">🆕 Docker & Kubernetes Masterclass (Packt)</a></strong></td>
    <td><strong><a href="https://www.coursera.org/" target="_blank">Coursera</a></strong></td>
    <td><span class="badge badge-included">Included</span></td>
    <td>✅ Yes</td>
    <td>4-6 weeks</td>
    <td><strong>PRODUCTION DEPLOYMENT!</strong> Containerize your Airflow pipelines, deploy to GKE. Docker appears in 70%+ of DE/ML job postings. Pairs perfectly with AWS + Airflow skills!</td>
</tr>
```

### 4.2 ADD: Snowflake/BigQuery Exposure (Month 14-15)

```html
<tr style="background-color: #e3f2fd;">
    <td><strong>1️⃣3️⃣.5</strong></td>
    <td><strong><a href="https://www.coursera.org/learn/google-cloud-bigquery-basics" target="_blank">🆕 BigQuery Basics for Data Analysts (Google Cloud)</a></strong></td>
    <td><strong><a href="https://www.coursera.org/" target="_blank">Coursera</a></strong></td>
    <td><span class="badge badge-included">Included</span></td>
    <td>✅ Yes</td>
    <td>2 weeks</td>
    <td><strong>CLOUD DATA WAREHOUSE!</strong> Quick exposure to BigQuery alongside your AWS Redshift skills. Shows multi-cloud awareness. Many DE jobs require Snowflake OR BigQuery experience!</td>
</tr>
```

### 4.3 CLARIFY: IBM GenAI Engineering Cert

The IBM GenAI Engineering Professional Certificate currently appears in both Stage 1 and Stage 2. 

**Recommended change:** Keep it in Stage 1 (your GenAI-First philosophy). In Stage 2 course #9, change the description to:

```
"REINFORCE & APPLY your Stage 1 GenAI skills to Data Engineering contexts. 
Focus on the RAG + LangChain courses that apply to your DE projects. 
Skip courses you already completed in Stage 1."
```

Or remove it from Stage 2 entirely and replace with the Coursera RAG course.

---

## 5. Stage 3 Changes (Detailed)

### 5.1 REMOVE: TensorFlow Developer Certificate

**Replace this row:**
```html
<!-- REMOVE THIS -->
<tr>
    <td><strong><a href="https://www.tensorflow.org/certificate" target="_blank">TensorFlow Developer Certificate</a></strong></td>
    <td><strong><a href="https://www.tensorflow.org/" target="_blank">TensorFlow</a></strong></td>
    <td><span class="badge badge-paid">$100</span></td>
    <td>✅ Yes</td>
    <td>2 months prep</td>
    <td>Industry-recognized, proves practical ML skills, opens doors</td>
</tr>
```

**With:**
```html
<!-- ADD THIS REPLACEMENT -->
<tr style="background-color: #e3f2fd;">
    <td><strong><a href="https://learn.nvidia.com/en-us/training/self-paced-courses" target="_blank">🆕 NVIDIA DLI: Building AI Applications (or Fundamentals of Deep Learning)</a></strong></td>
    <td><strong><a href="https://learn.nvidia.com/" target="_blank">NVIDIA DLI</a></strong></td>
    <td><span class="badge badge-free">FREE / $30</span></td>
    <td>✅ Yes</td>
    <td>1-2 days</td>
    <td><strong>REPLACES DISCONTINUED TF CERT!</strong> NVIDIA certifications are the new gold standard for deep learning verification in 2026. Covers GPU-accelerated deep learning, model deployment. Industry-recognized credential!</td>
</tr>
```

**Also update Stage 3 book section** — remove references to TF cert prep.

---

## 6. Course Recommendations — Full Research Summary

### Priority Order for Stage 1 Additions

| Priority | Course | Platform | Duration | Cost | Why |
|----------|--------|----------|----------|------|-----|
| **1** | Building & Evaluating Advanced RAG | DeepLearning.AI | 1 hour | FREE | Evaluation skills for PolicyPulse |
| **2** | Docker for Beginners (KodeKloud) | Coursera | 6 hours | Included | Docker for Junior AI Engineer apps |
| **3** | RAG (full course, Zain Hasan) | Coursera | 20 hours | Included | Comprehensive RAG + evaluation + deployment |

### Stage 2 Additions

| Priority | Course | Platform | Duration | Cost | Why |
|----------|--------|----------|----------|------|-----|
| **1** | Docker & Kubernetes Masterclass | Coursera | 40 hours | Included | Production deployment skills |
| **2** | BigQuery Basics for Data Analysts | Coursera | 10 hours | Included | Multi-cloud data warehouse exposure |

### Stage 3 Replacement

| Priority | Course | Platform | Duration | Cost | Why |
|----------|--------|----------|----------|------|-----|
| **1** | NVIDIA DLI Deep Learning / AI Applications | NVIDIA | 8-16 hours | Free-$30 | Replaces discontinued TF cert |

---

## 7. Project Scope Additions — All 7 Projects

### 7.1 CROSS-PROJECT ADDITIONS (Apply to ALL 7 projects)

Add the following sections to every project scope document:

#### A. Evaluation Framework Section (New)

```markdown
### AI Evaluation Layer (2026 Production Requirement)

Every AI-powered feature includes measurable quality evaluation using DeepEval.

**Framework:** DeepEval (pytest-compatible, open-source)
**Install:** `pip install deepeval`

| Metric | What It Measures | Target Score |
|--------|-----------------|-------------|
| Answer Relevancy | Does the AI response address the user's question? | > 0.8 |
| Faithfulness | Is the response grounded in provided context? | > 0.85 |
| Hallucination | Does the output contain fabricated info? | < 0.15 |

**Implementation:**
- Evaluation test cases live in `tests/test_eval.py`
- Run with: `deepeval test run tests/test_eval.py`
- Results logged to `logs/evaluation/` for README metrics
- CI pipeline includes evaluation gate (fail build if scores drop)

**Why This Matters for Portfolio:**
Hiring managers in 2026 specifically scan for evaluation-driven development.
"This project signals that you understand the difference between building 
an AI system and knowing whether it works." — AgenticCareers.co
```

#### B. Docker Support Section (New)

```markdown
### Docker Support (Containerization)

**Dockerfile** provided for reproducible local development and deployment.

```dockerfile
# Dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8501
CMD ["streamlit", "run", "app/Home.py", "--server.port=8501"]
```

**Docker Compose** (if multi-service):
```yaml
# docker-compose.yml
version: '3.8'
services:
  app:
    build: .
    ports:
      - "8501:8501"
    volumes:
      - ./data:/app/data
    env_file:
      - .env
```

**Why This Matters for Portfolio:**
Docker appears in 60%+ of AI/ML job postings. Including a Dockerfile 
shows deployment readiness — even for a Stage 1 project.
```

#### C. Updated Tech Stack (Add to existing)

Add these to each project's Tech Stack table:

```markdown
| **Evaluation** | DeepEval | AI output quality testing (answer relevancy, faithfulness, hallucination) |
| **Containerization** | Docker | Reproducible development environment, deployment-ready packaging |
```

#### D. Updated Project Structure (Add to existing)

Add to each project's file tree:

```
├── Dockerfile                    # Container definition
├── docker-compose.yml            # Multi-service orchestration (if needed)
├── tests/
│   ├── test_eval.py              # DeepEval evaluation test cases
│   └── ...existing tests...
├── logs/
│   ├── evaluation/               # Evaluation results & metrics
│   └── ...existing logs...
```

#### E. Updated Success Metrics (Add to existing)

Add to each project's success metrics:

```markdown
### AI Evaluation Metrics (NEW)

| Metric | Target |
|--------|--------|
| DeepEval test suite passing | ✅ All evaluation tests green |
| Answer Relevancy score | > 0.8 |
| Faithfulness score | > 0.85 |
| Hallucination rate | < 0.15 |
| Dockerfile builds successfully | ✅ |
| Docker Compose up & running | ✅ (if multi-service) |
```

---

### 7.2 PROJECT-SPECIFIC ADDITIONS

#### DataVault Analyst — Specific Additions

Add to **Tech Stack (Section 9):**
```markdown
| DeepEval | AI evaluation framework (answer relevancy for PandasAI queries) |
| Docker | Containerized Streamlit deployment |
```

Add to **Success Metrics (Section 12) — Phase 2:**
```markdown
| AI answer relevancy (DeepEval) | > 0.8 across 20+ test queries |
| PandasAI code correctness | > 90% valid Pandas code generated |
| Dockerfile | Builds and runs locally |
```

Add to **AI Guardrails (Section 8):**
```markdown
| **G-NEW: AI Quality Evaluation** | DeepEval answer_relevancy metric validates AI responses meet quality threshold before displaying to user. Low-scoring responses trigger "I'm not confident in this answer" disclaimer. |
```

---

#### PolicyPulse — Specific Additions (RAG-focused evaluation)

Add to **Tech Stack (Section 10):**
```markdown
| DeepEval | RAG evaluation framework (faithfulness, contextual precision/recall, answer relevancy) |
| RAGAS metrics (via DeepEval) | RAG-specific evaluation: context precision, context recall |
| Docker | Containerized deployment (Streamlit + ChromaDB) |
```

Add to **Success Metrics (Section 13) — Phase 2:**
```markdown
| RAG Faithfulness (DeepEval) | > 0.85 (answers grounded in policy docs) |
| Contextual Precision (DeepEval) | > 0.75 (relevant chunks ranked higher) |
| Contextual Recall (DeepEval) | > 0.80 (retrieval covers expected answer) |
| Answer Relevancy (DeepEval) | > 0.80 |
| Hallucination Rate | < 0.10 (critical for HR policy accuracy) |
| Dockerfile (Streamlit + ChromaDB) | Builds and runs via docker-compose |
```

Add new subsection to **Phase 2 (Section 8):**
```markdown
### 8.X Evaluation-Driven RAG Development

PolicyPulse implements evaluation-driven development — measuring retrieval 
and generation quality at every iteration.

**Evaluation Dataset:**
- 30+ question-answer pairs covering all 6 policy documents
- Each test case includes: question, expected_answer, expected_source_doc
- Stored in `tests/eval_dataset.json`

**Evaluation Pipeline:**
1. Load eval dataset
2. Run each question through RAG pipeline
3. Measure: faithfulness, contextual precision/recall, answer relevancy
4. Log results to `logs/evaluation/`
5. Compare across iterations (chunking strategy A vs B, embedding model X vs Y)

**Why This Matters:**
This is the single most differentiating aspect of the project.
Most portfolios show "I built a RAG chatbot." 
PolicyPulse shows "I built, MEASURED, and ITERATED on a RAG chatbot."
```

Update **docker-compose.yml** for PolicyPulse:
```yaml
# docker-compose.yml
version: '3.8'
services:
  app:
    build: .
    ports:
      - "8501:8501"
    volumes:
      - ./data:/app/data
      - ./chroma_db:/app/chroma_db
    env_file:
      - .env
  chromadb:
    image: chromadb/chroma:latest
    ports:
      - "8000:8000"
    volumes:
      - ./chroma_db:/chroma/chroma
```

---

#### FormSense — Specific Additions

Add to **Tech Stack:**
```markdown
| DeepEval | Extraction accuracy evaluation (custom GEval metric for form field extraction) |
| Docker | Containerized deployment |
```

Add to **Success Metrics (Section 13):**
```markdown
| Extraction Accuracy (DeepEval custom) | > 0.85 across 10+ sample forms |
| Field-level Confidence Calibration | Confidence scores correlate with actual accuracy |
| Validation Rule Coverage | 100% of rules have evaluation test cases |
| Dockerfile | Builds and runs locally |
```

**FormSense-specific DeepEval usage:**
FormSense uses a **custom GEval metric** (not standard RAG metrics) because it evaluates structured extraction accuracy, not RAG retrieval:

```python
from deepeval.metrics import GEval
from deepeval.test_case import LLMTestCaseParams

extraction_accuracy = GEval(
    name="Form Extraction Accuracy",
    evaluation_steps=[
        "Compare each extracted field value against the ground truth",
        "Check if checkbox states are correctly identified",
        "Verify numerical values (amounts, SSN last 4) match exactly",
        "Evaluate confidence scores correlate with extraction difficulty",
        "PENALIZE fabricated or hallucinated field values"
    ],
    evaluation_params=[
        LLMTestCaseParams.ACTUAL_OUTPUT,
        LLMTestCaseParams.EXPECTED_OUTPUT
    ],
    threshold=0.85
)
```

---

#### Operations-Demand-Intelligence — Specific Additions

Add to **Tech Stack:**
```markdown
| DeepEval | AI query evaluation (answer relevancy for PandasAI analytics queries) |
| Docker | Containerized deployment |
```

Add to **Success Metrics (Section 10):**
```markdown
| AI Answer Relevancy (DeepEval) | > 0.8 across 15+ analytics test queries |
| Dockerfile | Builds and runs locally |
```

---

#### StreamSmart Optimizer — Specific Additions

Add to **Tech Stack:**
```markdown
| DeepEval | AI recommendation quality evaluation (answer relevancy, structured output validation) |
| Docker | Containerized deployment |
```

Add to **Success Metrics (Section 12):**
```markdown
| AI Recommendation Relevancy (DeepEval) | > 0.8 |
| Rotation Plan Quality (custom metric) | Plans save money vs current spend |
| Dockerfile | Builds and runs locally |
```

---

#### Attention-Flow Catalyst — Specific Additions

Add to **Tech Stack (Section 12):**
```markdown
| DeepEval | AI dashboard query evaluation (answer relevancy, faithfulness for financial data) |
| Docker | Containerized deployment (app + DuckDB) |
```

Add to **Success Metrics (Section 17):**
```markdown
| AI Answer Relevancy (DeepEval) | > 0.8 |
| AI Faithfulness to Data (DeepEval) | > 0.9 (critical: financial data must be accurate) |
| Dockerfile | Builds and runs locally |
```

**AFC-specific note:** Financial data accuracy is especially critical. Set the faithfulness threshold to 0.9 (higher than other projects) because incorrect financial analysis can mislead trading decisions.

---

## ✅ Approval Checklist — For Manuel's Review

Before implementing any changes, please confirm:

- [ ] **Evaluation Framework:** DeepEval as primary, RAGAS metrics via DeepEval — agreed?
- [ ] **Docker Stage 1:** Add 1-week Docker intro (Month 5) + Dockerfile to 1 project — agreed?
- [ ] **Docker Stage 2:** Add Docker & Kubernetes Masterclass (Month 12-13) — agreed?
- [ ] **TensorFlow Cert:** Remove from Stage 3, replace with NVIDIA DLI — agreed?
- [ ] **BigQuery:** Add 2-week BigQuery Basics to Stage 2 — agreed?
- [ ] **IBM GenAI Cert:** Clarify as Stage 1 only, remove Stage 2 duplicate — agreed?
- [ ] **RAG Evaluation Course:** Add "Building & Evaluating Advanced RAG" (FREE) to Stage 1 — agreed?
- [ ] **Project Scopes:** Add evaluation + Docker sections to all 7 projects — agreed?
- [ ] **PolicyPulse Priority:** Make PolicyPulse the showcase project for evaluation-driven development — agreed?
- [ ] **Timeline:** Docker intro (1 week) fits in Month 5 without displacing other work — agreed?

---

**Document Status:** 📋 DRAFT — Awaiting Manuel's Approval  
**Date:** March 29, 2026  
**Next Steps:** Upon approval, I will modify each project scope .md file and draft the specific HTML changes for roadmap.html  

*"Build it, MEASURE it, then ship it — that's what separates production engineers from tutorial followers in 2026."* 🚀
