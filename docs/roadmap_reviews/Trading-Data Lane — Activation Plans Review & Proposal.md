# Trading-Data Lane — Activation Plans Review & Proposal

Oct 13, 2026 · @Manuel Reyes · Status: **PROPOSAL — no plan file changed**

## Summary

**Recommendation: run trading data as a paired second domain inside slots you already have (Option A).** It is 16 changes across the six plans, about 5 hours of trading-data practice over 12 weeks, and zero net hours. No DataVault build slot moves, so the C58/C59 guardrail is unchanged.

The changes grow your Day-41 `market_rehearsal` dbt project in `learning_journey` into a small, tested market-data model. Each piece maps to a named deliverable in the AFC v9.1 or Crucible v3.1 build sheet, so it moves into those repos later instead of being thrown away.

Why this beats adding a separate trading block:

- **Same skills, second domain.** The exercises are the AE interview staples (top-N per group, gaps-and-islands, dedupe, SCD2, incremental models) on market data. A live TradingView Analytics Engineer posting asks for master/reference data, golden-record logic and dbt tests, with market data as a plus.
- **Nothing is wasted.** Knowledge-time tests feed AFC deliverable B6; the security master feeds Crucible's S2 lakehouse; the volume functions follow `signalcore` signatures.
- **The gate stays protected.** DataVault S2 is still the only thing that opens the broad search.

If you want real trading artifacts before Q2, Option B moves the AB-620 extra-time thread to a trading block. It reverses a C42 ruling, so I rank it second.

Two findings change your scope docs, not just the plans: Alpha Vantage's daily-adjusted endpoint is now premium-only, and users reported Stooq historical downloads failing in March–April 2026. Details are under Review findings.

## Review findings

The trading lane is sound in design but thin: across 84 days it has two sessions (Day 41 and Day 83, about 4 hours). Day 41 already teaches the two mistakes practitioners say kill most backtests, look-ahead and a baseline that includes today. Eight things need attention.

| # | Where | Finding | Proposed fix | Kind |
| --- | --- | --- | --- | --- |
| 1 | Weeks 5–6, Day 41 | `asof join` is an inner join in DuckDB, so a filing with no later session open is silently dropped and the lookahead test never sees it. | Use `asof left join` and add a test that the unmatched count equals the generator's manifest. | Plan edit |
| 2 | Weeks 5–6, Day 41 | Each event has one `filed_at` time. AFC §4.2 and §5.3 need two: the filing date and the EDGAR acceptance datetime. Section 16 filings accepted 5:30–10:00 p.m. ET keep that day's filing date. | Generate both times; plant one 18:00 acceptance and one filing at exactly 09:30:00; test on acceptance time. | Plan edit |
| 3 | Crucible v3.1 §5 | Alpha Vantage `TIME_SERIES_DAILY_ADJUSTED` is listed as a free top-up. It is premium-only, and the free tier allows 25 requests a day. | Move it out of the free column; re-check on Alpha Vantage's own page at the data spike. | Scope correction |
| 4 | Crucible v3.1 §5 | Stooq bulk CSV is the backfill source. Users reported Stooq historical retrievals returning empty from late March 2026; the cause was never confirmed and reports were mixed. | Add Stooq to Crucible's data spike as "verify before relying on it". | Scope correction |
| 5 | AFC v9.1 §7B.2, Weeks 11–12 Day 83 | yfinance is AFC's Phase-2 price source. Its rate-limit errors date from April 2025 and the fixes helped only some users. Spike B1 is already planned. | Name Tiingo Starter and Alpaca Basic as B1 fallbacks. Tiingo Starter is licensed for internal use only, so public repos hold code and synthetic fixtures, never vendor rows. | Plan edit |
| 6 | Weeks 7–8 lane table | "L4 Trading: Rest (exam fortnight)" — the exam moved to Q2 (C58), so the stated reason is stale. | Keep the rest, relabel it "DataVault star fortnight", and offer the optional Labor Day block (change 9). | Plan edit |
| 7 | Weeks 5–6, Weeks 11–12, all headers | Weeks 5–6 still says OpenCode is the sole harness (C39/40), superseded by C42. Weeks 11–12 retro item 6 still calls AB-620 conditional (C37), also superseded by C42. Headers say Corrections 1–59; the roadmap is at 1–61, and C60–C61 do not touch these 12 weeks. | Text-only fixes in the same pass. | Plan edit |
| 8 | Weeks 9–12 | Your Weeks 1–2 copy has Day 1 ticked, yet the dates anchor to 20 July and your last working day was 9 October. If you are running the template from now, the Track A before-metrics (Day 68) and the work-system sessions (Days 79–82) cannot run as written. PostCheck capture (Day 81) still can, from memory. | Your call — see Decisions. | Question |

## Option A — paired-domain exercises (recommended)

Sixteen changes, all inside blocks the plans already schedule: 285 minutes of trading-data practice plus one optional hour. Pick a decision per row; I change no plan file until you do.

| # | Fortnight · Day | Slot it lives in (min) | Trading twin — what you build | Min | Lane | Feeds | Decision |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | W1–2 · Day 6 | Jupyter: redo 2–3 Week-1 exercises (60) | One redo is a Form 4 code checker, the twin of Day 5's Box-7 checker: P, S, A, M, F, G → meaning, and `is_open_market_purchase` true only for P | 15 | Foundations | AFC §4.2 (T1 = code P only) |  |
| 2 | W1–2 · Day 11 | Alpaca paper account, parked (20) | `notes/trading/data-sources.md`: one line each on limits and licence for Alpaca Basic, EDGAR, Tiingo Starter, Alpha Vantage, Stooq | 10 | Trading | Crucible §5, AFC spike B1 |  |
| 3 | W3–4 · Day 15 | Messy-text parser (60) | Three market-export lines: `$4.12` prices, `1.2M` volumes, one `N/A` bar that is quarantined with a warning | 15 | Foundations | Crucible §5 vendor quirks |  |
| 4 | W3–4 · Day 21 | Target list v0 (20) | At least three Tier-3 names (capital-markets or trading fintech); note whether each posting says "market data" or "reference data" | 0 | Job search | Tier 3 (C54) |  |
| 5 | W3–4 · Days 24, 26 | Kimball Ch. 1–2 notes | A market example: a daily bar is a fact, the security a dimension; tag SCD2 (security master), periodic snapshot (bars), accumulating snapshot (order lifecycle) | 10 | Foundations | AFC S2, Crucible S2 |  |
| 6 | W5–6 · Day 32 | LAG/LEAD + month-over-month deltas (40) | Same functions on seeded synthetic bars: daily return, overnight gap, and the RVOL leak side by side (`current row` vs `1 preceding`). Writes `gen_market_seed.py` early, so Day 41 starts ahead | 40 | Foundations | AFC T4a, `signalcore.volume.rvol` |  |
| 7 | W5–6 · Day 40 | AE reps #0 (40) | Gaps-and-islands on bars: the longest run of days with volume under 50% of its trailing 20-day average. Top-N and dedupe stay on `recon.db` | 15 | Job search | AFC T4e, Crucible SW-B dry-up, `vdu_present` |  |
| 8 | W5–6 · Day 41 | Market rehearsal (105) | Findings 1–2: `asof left join` + an unmatched-count test; `filing_date` and `accepted_at`; boundary events at 18:00 and exactly 09:30:00 | 15 | Trading | AFC B6 `test_knowledge_time`, Crucible "The Wall" |  |
| 9 | W7–8 · Day 50 | Labor Day bonus — optional, not counted | `dim_security` seed with one ticker rename and one reused ticker, keyed on CIK + share class rather than ticker; a test that one ticker maps to two securities over time | 60 opt. | Trading | Crucible S2 security master, AFC B4 |  |
| 10 | W9–10 · Day 58 | Kimball Ch. 19, part 1 (30) | One market line per subsystem: profiling → OHLC integrity; error-event schema → bad-tick quarantine; audit dimension → source, `fetched_at`, `accepted_at` | 5 | Foundations | AFC S2 contracts |  |
| 11 | W9–10 · Day 62 | Kimball Ch. 7 + 10 (90) | Two securities patterns from Ch. 10 (heterogeneous products — stock, ETF, warrant; the account periodic snapshot as a position snapshot) and a market bus-matrix row | 20 | Foundations | AFC S2, Crucible S2 |  |
| 12 | W9–10 · Day 68 | dbt Advanced: "the options you didn't use" (60) | A `timestamp`-strategy snapshot of the security master (DataVault used `check`); a `delete+insert` incremental that absorbs a restated bar; a note on why `signalcore.data` appends restatements instead | 60 | Foundations | `signalcore.data` bitemporal, Crucible S2 |  |
| 13 | W9–10 · Day 69 | dbt Advanced: packages (90) | One OHLC-integrity test on bars: high ≥ greatest(open, close), low ≤ least(open, close), volume ≥ 0 | 20 | Foundations | AFC B2 data-quality checks |  |
| 14 | W11–12 · Day 75 | AE reps #3 (45) | Timed SQL: top-3 sectors by 20-day ETF return per session. Timed dbt change: `fct_event_labels`, HIT when the 3-day max high ≥ next open × 1.115 | 45 | Job search | AFC §7B.4 label and screen, Crucible sector tier |  |
| 15 | W11–12 · Day 83 | AFC kickoff (120) | Findings 3–5 go into the dependency-spike checklist; Tiingo Starter and Alpaca Basic named as B1 fallbacks | 10 | Trading | AFC ADR-0005, ADR-0008 |  |
| 16 | W11–12 · Day 84 | Retro item 10 (trading lane) | One added question: which `market_rehearsal` pieces move to `afc.primitives`, AFC B6, or Crucible S2 | 5 | Trading | Next section |  |

Every twin uses seeded synthetic data in the public `learning_journey` repo. Real SEC filings stay in the AFC repo under its ADR-0004 public-record rule, and no vendor price rows are committed anywhere.

## How the practice pieces migrate

&#91;embedded content: practice → AFC Phase 2 → S2 shared layer · 6 pieces\]

Nothing is rebuilt: each Q1 twin is the first draft of an AFC Phase-2 deliverable, and the S2 extraction moves it once more into `signalcore` or Crucible's lakehouse, where the boundary spec's golden-value tests must pass unchanged.

## Hours and the priority guardrail

The guardrail holds unchanged in every fortnight: no change moves time into or out of a DataVault or Applied-AI build slot. Trading minutes come from Foundations, job-search and trading-lane blocks, which count on neither side (C58, C59).

| Fortnight | Trading minutes added | Blocks they sit in | AE/DE build (v3.1) | Applied AI (v3.1) | Guardrail |
| --- | --- | --- | --- | --- | --- |
| Weeks 1–2 | 25 | Foundations, Trading | 3.5 h | 0 h | Holds, unchanged |
| Weeks 3–4 | 25 | Foundations, Job search | 20.3 h | 3.2 h | Holds, unchanged |
| Weeks 5–6 | 70 | Foundations, Job search, Trading | 20.0 h | 18.8 h | Holds, unchanged |
| Weeks 7–8 | 0 (+60 optional) | Labor Day bonus only | 28.5 h | 4.0 h | Holds, unchanged |
| Weeks 9–10 | 105 | Foundations | 20.1 h | 10.6 h | Holds, unchanged |
| Weeks 11–12 | 60 | Job search, Trading | 14.4 h | 10.5 h | Holds, unchanged |

What each swap gives up, honestly:

- **Day 32** loses the month-over-month drill on retirement data; the LAG/LEAD skill is the same.
- **Days 40 and 75** move two of six AE rep sessions to market data. DataVault keeps Days 54, 61, 74 and the Day 76 take-home rehearsal.
- **Days 62 and 68** change differently: Day 62 adds about 20 minutes inside the 90-minute reading block, and Day 68 re-aims its whole 60-minute dbt Advanced practice at market data. If the Day 62 block runs long, the market note is what slips.

**Falsifier:** if a fortnight's journal shows a twin pushed a DataVault task into the next week, that twin reverts to its original exercise for the rest of the quarter.

## Option B — a dedicated trading block (alternative)

**Option B moves the AB-620 extra-time thread (\~2 h/week from Week 9, outside the 25) to a trading build thread, with the same cap and pause rule.** Over Weeks 9–12 that buys about 8 hours, on top of Option A.

What the 8 hours would build:

1. **A private daily job that snapshots the 11 SPDR sector ETF holdings** (Crucible v3.1 §5.2). Its point-in-time history only exists from the day it starts, so every week of delay is history you cannot rebuild for free. Keep the files private until the holdings' reuse terms are checked.
2. **Crucible's data spike:** Stooq, Tiingo Starter and Alpaca Basic tested for history depth, delisted coverage and install on Python 3.14, closed with an ADR.

What it costs:

- It reverses C42 §3(a), which committed AB-620 with the exam after 9 October, so it needs its own roadmap correction.
- Neither the AE nor the DE door screens on AB-620 (your Weeks 9–10 plan says so), but you chose it for Azure breadth and the AI-103 path. That reason does not go away.
- It is still extra time. The Week-12 rule stands: above \~29 h/week, extra-time threads pause before any flagship does.

**Falsifier:** if after four weeks the snapshot job has missed more than five sessions, or weekly hours pass \~29, stop the thread and restore AB-620.

**My ranking: second.** Take it only if a visible trading artifact this quarter matters more to you than the Copilot credential.

## Free trading-data sources: what the research found

SEC EDGAR is the one free source that is both reliable and point-in-time correct; every free price source carries a limit, a licence catch or a reliability report. That is why the twins stay synthetic and real data waits for the AFC and Crucible spikes.

| Source | Free limit | History | Catch | Use in your plans |
| --- | --- | --- | --- | --- |
| [SEC EDGAR APIs](https://www.sec.gov/os/accessing-edgar-data) | 10 requests/s with a declared User-Agent | Index files from 1994 Q3; [bulk ZIPs](https://www.sec.gov/edgar/sec-api-documentation) rebuilt nightly \~3 a.m. ET | Submissions JSON carries `acceptanceDateTime` ([field list](https://tldrfiling.com/blog/sec-edgar-submissions-json-structure)) | AFC T1/T5 and knowledge time |
| [SEC Insider Transactions Data Sets](https://www.sec.gov/dera/data/form-345) | Free quarterly files | Jan 2006 – Sep 2026 | [`FILING_DATE` only, no acceptance time](https://SEC.gov/files/insider_transactions_readme.pdf) — the exact trap in finding 2 | Bulk T1 history; a good knowledge-time exercise |
| [Alpaca Basic](https://docs.alpaca.markets/docs/about-market-data-api) | 200 historical calls/min | Since 2016 | Real-time is IEX only; a 15-minute recency limit on historical data | Crucible bars; AFC fallback |
| [Tiingo Starter](https://www.tiingo.com/about/pricing) | 50/hour, 1,000/day, 500 symbols/month | 30+ years of prices | Licensed for internal use only — no display or sharing | AFC spike B1 fallback, private |
| [Alpha Vantage free](https://docs.coupler.io/sources/category/finance-and-accounting/alpha-vantage/faq) | 25 requests/day, 5/min | — | Daily adjusted is premium-only (third-party docs; confirm at the spike) | Finding 3 |
| [Stooq](https://fundmanagersoftware.com/forum/viewtopic.php?p=28786) | Free CSV | Long | Historical pulls reported empty from late March 2026; cause unconfirmed | Finding 4 |
| [yfinance](https://github.com/ranaroussi/yfinance/issues/2422) | Unofficial | Long | Rate-limit errors since April 2025; fixes partial | AFC spike B1 |

**What practitioners report.** Two 2026 r/algotrading threads describe the same cycle: an edge appears, then turns out to be [look-ahead, survivorship or a split error](https://reddit.sentinel-team.org/posts/1t0ny8o/snapshots/2026-05-08T19%3A59%3A29.3336Z). Commenters' fixes match your scopes almost line for line: ask whether each field existed at decision time, treat every variant as spent [backtest budget](https://reddit.sentinel-team.org/posts/1t0twnn/snapshots/2026-05-08T19%3A59%3A29.3336Z), and use purged or embargoed splits. AFC's BH-FDR and Crucible's overfitting ledger are the engineered version of that advice.

**What hiring managers ask for.** [TradingView's Analytics Engineer posting](https://tradingview.teamtailor.com/jobs/8204636) wants expert dbt, master/reference data and golden-record logic, with market data a plus. [Polymarket's Senior AE](https://jobs.generalcatalyst.com/companies/polymarket/jobs/89762401-senior-analytics-engineer) models trading activity with dbt incremental models. Both are senior (4–7+ years), so read them as stack words, not entry bars. [QuantStart](https://www.quantstart.com/articles/Securities-Master-Databases-for-Algorithmic-Trading) names ticker management and vendor back-fills as the classic security-master failures, which is what changes 9 and 12 practise.

## Decisions needed before any file changes

Four answers unlock the edit pass; until then no plan, scope doc or `roadmap.html` is touched.

- [ ] Option A: pick a decision on each of the 16 rows.
- [ ] Option B: yes or no. A yes needs its own roadmap correction because it reverses C42 §3(a).
- [ ] Findings 3–4 (Crucible data sources): record them as a roadmap correction and patch Crucible v3.1 §5, or carry them only into the Day 83 spike checklist?
- [ ] Finding 8: are you running the template from now? If yes, I re-scope Days 68 and 79–82 in the same pass.

On approval I write v3.3 of all six plans in their own Markdown format, with a changelog block in Weeks 1–2 like v3.0–v3.2, and send the files back.

## Sources

Your files: the six v3.2 activation plans; `roadmap.html` v10.0 (Corrections 1–61); AFC v9.1 Stage-1 build sheet, Crucible v3.1 Stage-1 build sheet and the Shared SignalCore Boundary Spec v1.5 in `data-portfolio/project_scopes`; the SW-A, SW-B and IT-1 machine specs in `learning_journey/notes/trading`.

Web pages opened for this review:

- SEC — [Accessing EDGAR Data](https://www.sec.gov/os/accessing-edgar-data)
- SEC — [EDGAR application programming interfaces](https://www.sec.gov/edgar/sec-api-documentation)
- SEC — [Insider Transactions Data Sets](https://www.sec.gov/dera/data/form-345) and its [readme](https://SEC.gov/files/insider_transactions_readme.pdf)
- TLDRFiling — [EDGAR submissions JSON structure](https://tldrfiling.com/blog/sec-edgar-submissions-json-structure)
- DuckDB — [AsOf join guide](https://duckdb.org/docs/current/guides/sql_features/asof_join) and [FROM clause](https://duckdb.org/docs/current/sql/query_syntax/from)
- Alpaca — [About Market Data API](https://docs.alpaca.markets/docs/about-market-data-api)
- Tiingo — [Pricing](https://www.tiingo.com/about/pricing)
- Coupler.io — [Alpha Vantage FAQ](https://docs.coupler.io/sources/category/finance-and-accounting/alpha-vantage/faq) (third-party)
- Fund Manager forum — [Stooq historical retrieval thread](https://fundmanagersoftware.com/forum/viewtopic.php?p=28786)
- GitHub — [yfinance issue #2422](https://github.com/ranaroussi/yfinance/issues/2422)
- O'Reilly — [The Data Warehouse Toolkit, 3rd ed., contents](https://oreilly.com/library/view/the-data-warehouse/9781118530801)
- TradingView — [Analytics Engineer](https://tradingview.teamtailor.com/jobs/8204636); Polymarket — [Senior Analytics Engineer](https://jobs.generalcatalyst.com/companies/polymarket/jobs/89762401-senior-analytics-engineer)
- r/algotrading snapshots — [thread 1](https://reddit.sentinel-team.org/posts/1t0ny8o/snapshots/2026-05-08T19%3A59%3A29.3336Z), [thread 2](https://reddit.sentinel-team.org/posts/1t0twnn/snapshots/2026-05-08T19%3A59%3A29.3336Z)
- QuantStart — [Securities Master Databases for Algorithmic Trading](https://www.quantstart.com/articles/Securities-Master-Databases-for-Algorithmic-Trading)
- Data Engineer Academy — [Portfolio review checklist 2026](https://dataengineeracademy.com/blog/data-engineer-portfolio-review-checklist-2026-what-hiring-managers-actually-score/) (vendor; directional)
- Intrinio — [Modern security master architecture](https://intrinio.com/blog/modern-security-master-architecture-unifying-ticker-cusip-isin-and-figi-data-at-scale) (vendor; directional)
