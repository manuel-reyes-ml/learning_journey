# MASTER SWING TRADING PLAN — v2

*Two-Playbook System (SW-A Bottoming + SW-B Trend Continuation)*

*Revised with U&R structural requirement, VCP refinement, RS percentile filter, and dilution disqualifier.*

---

## Changelog — v1 to v2

Refinements address two structural concerns: (1) SW-A as written buys names with poor statistical base rates; the U&R requirement and dilution disqualifier raise the evidentiary bar. (2) SW-B as written lacks the volume-and-volatility-contraction filter that separates institutional accumulation from random pullbacks. The VCP and RS percentile additions tighten setup quality.

| Area | v1 | v2 Refinement |
| --- | --- | --- |
| SW-A trigger | Proximity to 52-week low + RSI + accumulation | REQUIRES confirmed Undercut & Reclaim (U&R). Proximity alone disqualified. |
| SW-A risk tier | A+ up to 1.0% | A+ capped at 0.75% until 50+ SW-A trades show positive expectancy |
| SW-A disqualifier | Loose mention of dilution | Hard disqualify: SEC form 424B5 (ATM offering) or S-3 in last 60 days |
| SW-B setup filter | Pullback to 20/50 EMA + lower volume | Adds VCP requirement: 2+ contractions, each shallower, each on lower volume |
| SW-B RS filter | Qualitative | RS percentile ≥ 80 vs SPY required at entry |
| Paper-to-live projection | Not specified | Apply 25% performance haircut to paper expectancy |
| Journal fields | Basic | Adds RS percentile, MAE/MFE, sector context, rule-adherence score |

---

## 1. Mission, Objectives, and Guardrails

Mission: Extract repeatable swing gains from (A) early reversals near lows with confirmed Undercut & Reclaim structure, and (B) continuation in strong trends with confirmed VCP and RS leadership, using rules-based execution and risk containment.

### Primary Objectives

- Build a process with positive expectancy (not home runs).
- Limit drawdowns through predefined risk per trade and portfolio heat.

### Non-Negotiables

- Every trade has: Setup ID, entry trigger, invalidation level, stop, target(s), position size, and management rules.
- Your system must respect risk math (position sizing = account risk ÷ trade risk).

Educational use only; not financial advice.

---

## 2. Instruments, Universe, and Liquidity Standards

Instrument: U.S. listed stocks first. Options optional later (mainly for hedging/event risk).

### Universe Buckets

- Primary Swing Universe (default): price ≥ $5, average volume ≥ 1M shares/day, tight spreads.
- Special Situations / Small Caps (restricted): smaller size, fewer concurrent positions, stricter exits.

### Sector and Market Context

Align with industry/sector trend as a buy trigger. Avoid trading stocks fighting their sector.

---

## 3. Timeframes and Market Structure

- Weekly defines primary structure and major supply/demand (key highs/lows).
- Daily defines setup quality, base/pullback shape, and confirms trend.
- 30-min or 1-hr optional for timing precision.

Key structure rule: trade at or near levels, not in the middle of noise.

---

## 4. Risk Management

### 4.1 Risk per Trade (R)

Define R = the dollars you lose if the stop is hit.

- Primary Swing Universe: 0.5%–1.0% account risk per trade.
- Special Situations / Small Caps: 0.25%–0.6% risk per trade.
- Raise risk only after ≥ 50–100 trades show stability.

### 4.2 Portfolio Heat

- Max open risk (sum of all R at current stops): 3.0%.
- Max sector exposure: 1.5%.
- Max positions: 3–8 swing positions.

### 4.3 Position Sizing

`Position size = Account Risk ($) ÷ Trade Risk ($/share)`

Example: Account $50,000; risk/trade 0.75% = $375. Entry $25.00, Stop $23.50 = $1.50/share. Shares = 375/1.50 = 250.

### 4.4 Stop Placement

- Stops belong beyond structure, not at obvious crowded levels.
- Below the most recent swing low (trend continuation).
- Below base support or below consolidation (breakout/basing play).

---

## 5. Trade Management

### 5.1 Minimum Reward:Risk

- Minimum planned RR: 1.5R (absolute minimum), prefer 2R+ when structure supports it.
- Avoid momentum buys without an exit (explicit rule).

### 5.2 Scaling Out

- 0% partials until +1.5R (let the trade work).
- Optional 25%–50% partial at +2R if major resistance or earnings window.
- Trail remainder by structure (higher lows) or 20 EMA.

### 5.3 Time Stops

- Basing/Bottoming: if no upside follow-through within ~5–10 trading days, reduce/exit.
- Trend Continuation: if it loses trend structure (breaks swing low / closes below key MA), exit.

---

## Playbook A — Bottoming / Pre-Breakout (v2)

Buy stabilization + accumulation + structural reclaim near 52-week lows. THIS IS A CONTRARIAN PLAYBOOK with a worse statistical base rate than SW-B. v2 raises the evidentiary bar to compensate.

> **v2 UPDATE:** Hard structural requirement: Undercut & Reclaim (U&R) confirmation. A stock near its 52-week low is NOT a setup. The setup is when the stock makes a marginal new low AND reclaims a prior support level on the same or following session. Proximity-only setups are now disqualified.

> **v2 UPDATE:** Hard disqualifier: any active dilution catalyst. Check SEC filings for form 424B5 (ATM offering prospectus), S-3 shelf, or S-1 filed in the last 60 days. If found, SW-A is OFF for that ticker regardless of chart quality.

### A1) Setup Filter (must-have)

**Structural (mandatory U&R)**

- Price made a marginal new 52-week low (or is within 5–10% of one).
- Price subsequently RECLAIMED a prior swing low or key support level.
- Reclaim is confirmed by a daily close above the reclaimed level, not just an intraday wick.

**Technical Exhaustion + Early Turn**

- RSI(14) ~30–40 and rising (confirmation only, not trigger).
- MACD histogram turning positive (confirmation only, not trigger).

**Accumulation Evidence**

- Volume today > 1.5× 10-day average on up days.
- OBV / accumulation line trending up.
- Pullbacks during the base on lighter volume than rallies.

**Breakout Potential**

- Price beginning to cross above 20/50 EMA after reclaim.

### A2) Fundamental/Context Filter

- Revenue growth or improving margins trend (quarterly).
- Balance sheet runway (cash vs burn) for small caps.
- No active dilution (424B5/S-3 in last 60 days) — hard disqualifier.
- No going-concern auditor language or delisting risk.

### A3) Entry Triggers (choose one)

- **Trigger A (Preferred — Retest/Reclaim):** enter on confirmed U&R, ideally on retest of the reclaimed level holding as support.
- **Trigger B (Conservative — Breakout + acceptance):** enter on break above base resistance with volume confirmation.
- **Trigger C (Aggressive — Reclaim of MA):** reclaim of 20/50 EMA plus bullish candle confirmation. Reduced size.

### A4) Stop Placement

- Default: below the U&R spring low (the marginal new low that was reclaimed).
- For volatile small caps: widen stop only if you reduce share size to keep R constant.

### A5) Risk Tier (v2)

- A+ setup: up to 0.75% risk (capped — REDUCED from 1.0% in v1).
- A setup: 0.50% risk.
- B setup: 0.25% risk (or skip).
- Cap remains in place until 50+ SW-A trades show positive expectancy.

### A6) Profit Taking

- T1: next major daily resistance / prior breakdown area.
- T2: 2R–3R if trend emerges.
- Trail with higher lows or 20 EMA once trend transitions.

### A7) Hard Do-Not-Trade Conditions

- Extremely wide spreads / thin order book.
- Spike top / squeeze behavior.
- Earnings within 3–5 trading days.
- Active dilution filings (424B5/S-3 in last 60 days).
- No confirmed U&R structure — proximity to lows alone is not a setup.

---

## Playbook B — Trend Continuation (v2)

Buy strong stocks in strong sectors during pauses, then sell into continuation. v2 adds the VCP refinement and quantitative RS filter.

> **v2 UPDATE:** New filter: Volatility Contraction Pattern (VCP) — pullback must show 2 or more contractions, each one shallower than the previous, each on lower volume than the previous. A single pullback to the 20 EMA without contraction structure does NOT qualify as a VCP. The contraction structure is the institutional accumulation signature.

> **v2 UPDATE:** New filter: RS percentile ≥ 80 vs SPY at entry. The stock must be in the top 20% of relative strength performers. This single filter eliminates a large fraction of failed continuation trades.

### B1) Setup Filter (must-have)

**Trend Confirmation**

- Price above 50 EMA AND 200 EMA (uptrend).
- 50 EMA rising; 200 EMA rising or flattening up.
- Sector/industry strong or improving.

**VCP Structure (mandatory in v2)**

- 2 or more contractions on the daily chart during the pullback/base.
- Each contraction shallower than the previous (e.g., −15%, −10%, −5%).
- Each contraction on lower volume than the previous.
- Final contraction within 5–10% of the pivot.

**Relative Strength (mandatory in v2)**

- RS percentile ≥ 80 vs SPY at the time of entry.
- RS line flat-to-rising during the pullback (not making new RS lows).

**Momentum Alignment**

- RSI(14) 40–60 during pullback (not extended).
- MACD line close to signal (about to cross).
- ADX > 20 to confirm trend strength.

### B2) Entry Triggers

- **Trigger A (Breakout):** buy break above consolidation high with volume expansion.
- **Trigger B (Pullback Entry — preferred):** buy pullback to 20/50 EMA or pivot with confirmation candle + rising volume, after VCP completes.
- **Trigger C (Retest):** buy retest of breakout level as support.

### B3) Stop Placement

- Below the pullback swing low (daily) or below the final VCP contraction.
- Avoid obvious crowd stops.

### B4) Risk Tier

- A+ setup: up to 1.0% risk.
- A setup: 0.75% risk.
- B setup: 0.50% risk (or skip).

### B5) Profit Taking

- Initial target at next major resistance (daily/weekly).
- Secondary: trail using 20 EMA or structure-based trailing stop.
- Runner: hold through structure until breakdown.

---

## 6. Shared Business Rules

### A) Portfolio Heat and Exposure

- Max total open risk: 3.0% of equity.
- Max sector risk: 1.5% of equity.
- Reduce risk tiers in choppy markets or after drawdown triggers.

### B) Circuit Breakers

- 3 consecutive losses → pause new entries for 3 trading days.
- Rule violation → pause new entries for the rest of the week and review.
- Hit −3R in a week → stop opening new positions until next week.
- Two consecutive max-loss weeks → reduce risk/trade by 25–50% for the next month.

### C) Earnings / Binary Events

- Default: no new entries within 3–5 trading days of earnings.
- Holding through earnings only with prewritten plan + reduced size.

### D) Behavioral Rules

- No trades without a completed trade ticket.
- Avoid trading the open for new entries.
- No third-party tips trades.

---

## 7. Operational Routine (8–5 Job)

### Daily (Weekdays)

**Evening (30–60 min)**

- Run both scanners (Bottoming/Pre-Breakout + Trend Continuation).
- Chart review: weekly → daily → key levels.
- Validate v2 filters: SW-A U&R structure confirmed? SW-B VCP and RS percentile?
- Build shortlist (5–15 tickers) and write a trade ticket for each A+ setup.
- Set alerts at trigger levels; pre-stage limit/stop orders if broker supports OCO.

**Lunch Hour (15–30 min)**

- Check alerts triggered / price near levels.
- Place/adjust orders (prefer limit entries; avoid chasing).
- Update stops if rules require.

**After Close (15–25 min)**

- Journal and grade execution; capture screenshots.

### Weekly (Sunday evening, 60–90 min)

- Review prior week trades, sizing, and goals.
- Update weekly trend/levels and rebalance sizing.

### Monthly (60–120 min)

- Full process and analytics review; adjust only after enough sample size.

---

## 8. Trade Ticket Template (v2)

| Field | Entry |
| --- | --- |
| Trade ID | YYYY-MM-DD-TICKER-A or -B |
| Playbook | SW-A (Bottoming) or SW-B (Trend Continuation) |
| Market Regime | Index trend (weekly/daily) + sector trend |
| Catalyst/Context | Earnings date, sector rotation, offering resolved, etc. |
| Levels | Weekly S/R, Daily S/R, MA levels (20/50/200) |
| v2 — U&R Confirmed (SW-A) | Yes/No + level reclaimed + reclaim date |
| v2 — Dilution Check (SW-A) | No 424B5/S-3/S-1 in last 60 days — Confirmed Yes/No |
| v2 — VCP Structure (SW-B) | Number of contractions, depth sequence, volume trend |
| v2 — RS Percentile (SW-B) | RS percentile vs SPY (must be ≥80) |
| Entry Trigger | Breakout + volume / pullback confirmation / MA reclaim |
| Entry Price | |
| Stop Price (invalidation) | |
| Trade Risk $/share | Entry − Stop |
| Account Risk ($) | Per setup grade and v2 risk tier |
| Position Size (shares) | Account risk ÷ trade risk |
| Targets | T1 (structure), T2 (R-multiple), Trail rule |
| Management Rules | Move stop? Partials? Time stop? |
| Exit Triggers | Violation of structure, thesis broken, event risk window |
| Post-Trade Grade | A/B/C (process), notes, screenshots |

---

## 9. Journal Fields (v2 — Expanded)

| Field | Notes |
| --- | --- |
| Setup type (A/B) | SW-A or SW-B |
| Setup Grade | A+/A/B + rationale |
| Regime alignment | Market + sector + stock |
| Entry type | Breakout / retest / pullback / reclaim |
| v2 — RS percentile at entry | Required for SW-B (must be ≥80) |
| v2 — U&R confirmation | Required for SW-A |
| v2 — VCP description | Required for SW-B (contractions, volume) |
| Planned R | Initial RR |
| Realized R | Final outcome |
| v2 — MAE/MFE | Max Adverse and Max Favorable Excursion in R units |
| Rule adherence score | 0/1 per rule; execution grade |
| Sector context | Sector trend at entry |
| Mistake / Insight | One line lesson |

---

## 10. Paper Testing Protocol (v2 addition)

Apply 25% performance haircut to paper expectancy when projecting to live trading. Live results consistently underperform paper results due to slippage, partial fills, and psychological pressure.

### Phase 0: Manual Chart Study

- Mark 20 historical examples per playbook: entry, stop, target, outcome.
- Complete before paper trading begins.

### Phase 1: Paper Test Sequence

- SW-B first (6 weeks alone). Higher base rate playbook.
- Add SW-A only after SW-B is producing a reviewable journal.
- Minimum sample before judgment: 30 SW-B trades + 20 SW-A trades. Floor only; 50+ each preferred.

### Phase 2: Decision Gate

- Compute per playbook: win rate, average winner R, average loser R, expectancy, profit factor, max consecutive losses.
- Live gate: expectancy ≥ +0.20R after 25% haircut, with at least 50 trades in that playbook.
- Max consecutive loss streak must be tolerable at live size.

### Phase 3: Live Micro-Sizing

- Go live at 25% of normal risk (e.g., 0.18% instead of 0.75% A+ for SW-A).
- 30–50 live trades; compare live to paper expectancy.
- Scale to full sizing only if live expectancy remains positive post-haircut.

### Hard Rule

Each playbook earns live status independently. SW-B clearing paper does NOT permit SW-A live trading.

### SW-A Retirement Condition (v2)

If SW-A expectancy after 50 paper trades is materially worse than SW-B (e.g., SW-A < +0.10R and SW-B > +0.30R after haircut), retire SW-A. Do not force a contrarian playbook to work because it is in the plan.

---

## 11. AI Agent Use

### High-Value Automations

- Daily scanning + shortlist generation (apply v2 filters: U&R for SW-A, VCP + RS percentile for SW-B).
- Chart briefing pack (1-page brief per ticker).
- Trade ticket auto-fill with position sizing and RR; check portfolio heat.
- Journaling + grading assistant (R-multiples, MFE/MAE, win rate, profit factor).
- Process compliance monitor (rule break detection).

### Do Not Delegate

- AI deciding trades without your confirmation.
- Using AI sentiment outputs as primary signals.

### Implementation Path

- Phase 1 (manual + assisted): AI produces watchlist + trade tickets; you approve execution.
- Phase 2 (semi-automated): AI generates orders (OCO brackets) but you click approve.
- Phase 3 (research only): automated backtests + walk-forward testing.

---

## 12. Glossary of Acronyms and Abbreviations

All shorthand used in this document, in alphabetical order. Includes both system-specific terms and general swing-trading terminology.

| Acronym | Meaning | Notes / Use in this system |
| --- | --- | --- |
| ADL | Accumulation/Distribution Line | Volume-based indicator showing whether a stock is being accumulated or distributed. |
| ADX | Average Directional Index | Trend-strength indicator. ADX > 20 used to confirm trend in SW-B. |
| ATM offering | At-The-Market Offering | Continuous share offering filed via SEC form 424B5; signals dilution risk. Hard disqualifier for SW-A in v2. |
| ATR | Average True Range | Volatility measure; used to size stops on volatile names. |
| EMA | Exponential Moving Average | Faster-reacting moving average; 20 EMA used for trend trail, 50 EMA for trend confirmation. |
| EOD | End of Day | Routine and scan timing — typically after 4:00 PM ET close. |
| HTF | Higher Time Frame | Weekly/monthly structure referenced above daily charts. |
| MA | Moving Average | Generic term covering SMA and EMA. |
| MACD | Moving Average Convergence Divergence | Momentum indicator; histogram cross used as confirmation only, not trigger. |
| MAE | Maximum Adverse Excursion | Worst unrealized loss reached during a trade; journal field. |
| MFE | Maximum Favorable Excursion | Best unrealized gain reached during a trade; journal field. |
| OBV | On-Balance Volume | Running total of volume on up days vs down days. Trend = accumulation signal. |
| OCO | One-Cancels-Other Order | Bracket order pairing stop and target; one fills, the other cancels automatically. |
| R / 1R | Risk Unit | Dollar amount lost if stop is hit. All outcomes expressed in R multiples (e.g., +2R, −1R). |
| RR | Reward-to-Risk Ratio | Planned profit divided by planned loss. Minimum 1.5:1; prefer 2:1+. |
| RS | Relative Strength | Ticker performance vs benchmark. SW-B v2 requires RS percentile ≥ 80 vs SPY. Distinct from RSI. |
| RSI | Relative Strength Index | Momentum oscillator (0–100), typically RSI(14). Confirmation only, not trigger. |
| S/R | Support / Resistance | Price levels where buying/selling pressure historically clustered. |
| S-1 | SEC Form S-1 (Registration) | New share registration filing; signals primary offering. Dilution disqualifier for SW-A. |
| S-3 | SEC Form S-3 (Shelf Registration) | Shelf registration allowing future share issuance; dilution risk signal. Hard disqualifier for SW-A in v2. |
| 424B5 | SEC Form 424B5 (Prospectus Supplement) | ATM offering prospectus supplement; active dilution catalyst. Hard disqualifier for SW-A in v2. |
| SEPA | Specific Entry Point Analysis | Mark Minervini's swing methodology; VCP refinement in SW-B v2 is derived from SEPA principles. |
| SMA | Simple Moving Average | Unweighted average of last N closes (e.g., SMA50, SMA200). |
| SPY | SPDR S&P 500 ETF Trust | Broad market benchmark; SW-B RS percentile measured vs SPY. |
| SW-A | Swing Playbook A — Bottoming / Pre-Breakout | Contrarian playbook; v2 requires confirmed U&R structure. |
| SW-B | Swing Playbook B — Trend Continuation | Continuation playbook; v2 requires VCP structure and RS percentile ≥ 80. |
| T1 / T2 | Target 1 / Target 2 | First and second profit objectives, set before entry. |
| U&R | Undercut & Reclaim | Structural pattern: marginal new low followed by daily close reclaiming a prior swing low/support. Mandatory for SW-A in v2. |
| VCP | Volatility Contraction Pattern | Base/pullback with 2+ contractions, each shallower and on lower volume. Mandatory for SW-B in v2. |
| VWAP | Volume-Weighted Average Price | Session fair-value benchmark. Used in swing system for intraday entry timing. |

---

*Educational use only. Not financial advice.*
