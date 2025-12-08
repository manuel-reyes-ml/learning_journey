# 📊 Portfolio Projects

All my production-ready data / Python projects live in separate repositories.  
This file tracks my **capstone** and follow-up roadmap.

---

## 🚀 Active Projects

### Trading Attention Tracker (Capstone v1.0)
**Repo:** [PROJECT LINK](https://github.com/manuel-reyes-ml/trading_attention_tracker)
**Started:** December 2025 (Month 1)  
**Status:** 🚧 In Development (Capstone v1.0)  
**Type:** Data Analysis & Visualization Project  
**Tech Stack:** Python • SQLite • pandas • yfinance • Wikipedia Pageviews API • RSS (XML) • BeautifulSoup • Matplotlib

**Description**  
End-to-end Financial data analysis system that correlates **stock trading volume**, **news headlines**, and **Wikipedia pageviews** (public attention) for FAANG companies (e.g. AAPL, AMZN, MSFT).  
Built as the **capstone project** for the _Python for Everybody_ specialization and as the **first flagship repo** in my data / AI learning journey.

**Data Sources & Formats**
- 📈 **Market data:** Historical prices & volume from `yfinance` (downloaded via Python)
- 🌐 **Attention data:** Daily Wikipedia pageviews from the Wikimedia Pageviews API (JSON)
- 📰 **News data:** Finance/tech RSS feeds (XML) + optional article HTML parsing with BeautifulSoup
- 💾 **Storage:** Normalized **SQLite** database (multiple related tables)

**Database Design (SQLite)**
- `companies` – tickers, company names, Wikipedia page names  
- `trading_volumes` – daily close price & volume per company  
- `news_mentions` – news headlines, dates, sources, URLs  
- `wiki_pageviews` – daily pageviews per company  
- `sentiment_scores` – basic sentiment metrics per headline (pos/neg word counts, sentiment score)

**Core Features (v1.0)**
- ✅ Automated price & volume ingestion via `yfinance`
- ✅ Wikipedia API integration with JSON parsing for pageviews
- ✅ RSS feed ingestion (XML) and headline extraction
- ✅ Basic sentiment analysis using custom positive/negative word lists
- ✅ Aggregation by date to combine:
  - trading volume  
  - news mention count  
  - average sentiment  
  - Wikipedia pageviews
- ✅ Analytical SQL queries (joins across 3–4 tables)
- ✅ 2–3 clear visualizations with Matplotlib:
  - Time series: **news mentions vs trading volume vs pageviews**
  - Bar chart: **top headline keywords per company**
  - Optional scatter: **news count vs volume**

**Skills Demonstrated**
- 🧵 **End-to-end data pipeline:** from live APIs / RSS → Python → SQLite → pandas → analysis → plots
- 🌐 **Networked data:** working with JSON (APIs), XML (RSS), and HTML (BeautifulSoup)
- 🗄️ **Database design:** schema modeling, foreign keys, joins, aggregation queries
- 🧹 **Data cleaning & preprocessing:** dates, missing values, text normalization
- 📊 **Data analysis & visualization:** using **pandas** for tabular analysis and **Matplotlib** for charts
- 🧠 **Text processing:** tokenization, keyword frequency, handcrafted sentiment scoring
- 📑 **Reproducible project structure:** clear `src/`, `data/`, `db/`, and `docs/` layout

**Next Phase – v1.1 (Month 2)**
- Expand from 2–3 tickers to a larger tech/watchlist universe  
- Improve sentiment model (larger dictionaries, more nuanced scoring)  
- Add more visualizations (e.g., scatter plots of sentiment vs returns)  
- Export summarized daily metrics to CSV for use in Excel / BI tools  

---

## 📋 Planned Projects

### Financial Data Dashboard (Month 2–3)
**Status:** 📅 Planned  
**Type:** Interactive Dashboard (v2.0 of the Tracker)

Play the role of **v2.0** for the Trading Volume & News Sentiment Tracker:

- Interactive dashboard (Streamlit / Plotly) on top of the same SQLite/pandas data model
- Company selector (e.g. AAPL / AMZN / MSFT / others)
- Time-range filters and dynamic charts
- Ticker comparison: volume vs news attention vs pageviews
- Exportable PDF / PNG “daily report” view

---

### ML Trading Strategy Prototype (Month 3–4)
**Status:** 📅 Planned  
**Type:** Machine Learning Application

First ML-oriented project built on top of cleaned market data:

- Feature engineering: returns, volatility, simple technical indicators (e.g. SMA, RSI)
- Labeling: next-day up/down move or return buckets
- Baseline models (logistic regression / simple tree-based models)
- Train/test split and evaluation metrics (accuracy, precision/recall)
- Use of backtest-style evaluation on historical data
- Integration with the existing SQLite / pandas data pipeline

---

## 📈 Project Progression Roadmap

Month 1: Capstone v1.0 – Trading Volume & News Sentiment Tracker
Month 2: v1.1 – More tickers, richer sentiment, exportable reports
Month 2–3: Financial Data Dashboard (interactive UI on top of the tracker)
Month 3–4: ML Trading Strategy Prototype (first models on market data)
Month 5+: Hardening, documentation, and production-style deployment experiments

---

## 🎯 All Projects on GitHub

View all repositories: [github.com/manuel-reyes-ml](https://github.com/manuel-reyes-ml)

**Description:**  
Financial data analysis system that correlates Wikipedia pageviews (public attention) with stock market activity for FAANG companies.