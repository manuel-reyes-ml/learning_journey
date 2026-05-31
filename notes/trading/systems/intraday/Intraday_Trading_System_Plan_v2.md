# INTRADAY TRADING SYSTEM — v2

*5m Execution • 15m Structure • 1H Momentum • 1D/1W Levels*

*Revised with research-backed refinements (ORB time filter, VWAP slope, extension limits, journal upgrades).*

---

## Changelog — v1 to v2

Refinements were derived from current public research on professional ORB and VWAP practice. The original system framework is preserved; the changes tighten setup quality and add fields required for meaningful post-trade review.

| Area | v1 | v2 Refinement |
| --- | --- | --- |
| ORB time window | 9:45–11:30 ET allowed | Hard cap at 10:30 ET; mandatory day-of-week tagging |
| VWAP slope | Not specified | Rising VWAP for longs, falling for shorts, flat = no-trade |
| VWAP extension | Not specified | No entry if price >2% from VWAP (large-cap) or >3% (volatile) |
| Liquidity floor | Loose mention | 1M+ average daily volume required for VWAP playbooks |
| Failed Breakout (Trap) | 3/5 confirmations | 4/5 confirmations required (counter-trend bar raised) |
| Journal fields | Basic fields | Adds time-of-day, day-of-week, VWAP slope, MAE/MFE |
| Anchored VWAP | Not included | Pilot 4th playbook (Earnings-gap AVWAP), added but not yet live |

---

## Scope and Intent

This document defines a repeatable intraday trading process (pre-market preparation, execution rules, and three core playbooks plus one pilot). It is designed to reduce discretionary noise by requiring objective confirmation (levels, VWAP behavior with slope, market alignment, relative strength, extension, and volume) before every entry.

## Disclaimer

This document is for educational purposes only and does not constitute investment advice, a recommendation, or an offer to buy or sell any security. Intraday trading involves substantial risk, including the risk of loss of capital. You are responsible for your own decisions and risk management.

---

## System Overview

### Chart Stack (fixed)

- **5-minute (5m):** execution and risk management (entries, stops, partials, exits).
- **15-minute (15m):** intraday structure and day type; defines Opening Range High/Low (ORH/ORL).
- **1-hour (1H):** momentum/sentiment filter (MACD + RSI).
- **1-day (1D) and 1-week (1W):** major structure and levels; defines higher-timeframe (HTF) bias and key zones.

### Core Philosophy

Trade only when price action shows acceptance or rejection at important levels, confirmed by VWAP behavior (including slope), aligned market/relative-strength conditions, and a non-extended entry.

### Definitions

| Term | Definition | Use in this system |
| --- | --- | --- |
| VWAP | Volume-weighted average price for the current session. | Bias line: above VWAP favors longs; below favors shorts. Look for reclaim/hold or rejection/fail with slope confirmation. |
| VWAP Slope (v2) | Direction of the VWAP line over the last 30–60 minutes. | Rising = long bias; Falling = short bias; Flat = no-trade (chop signal). |
| VWAP Extension (v2) | % distance from current price to VWAP at entry. | Hard cap: >2% (large-cap) or >3% (volatile small-cap) = no entry; wait for return. |
| ORH / ORL | Opening Range High/Low for first 15 minutes (9:30–9:45 ET). | Primary breakout/breakdown levels for the ORB playbook. |
| PMH / PML | Premarket high/low (from extended hours). | Liquidity levels; frequent trap zones at the open. |
| HOD / LOD | High/Low of Day (regular session). | Targets and invalidation points. |
| RS | Ticker performance relative to a benchmark (e.g., Ticker/QQQ ratio). | Confirms leadership/lag; improves breakout reliability. |
| RVOL | Relative volume: current vs average volume baseline. | Tradability filter; confirms participation behind moves. |
| 1R | Fixed risk unit per trade. | Sizing and daily loss limits; keeps outcomes comparable. |

### Market Proxies

- **QQQ:** Nasdaq-100 ETF (cash-session proxy for growth/tech sentiment).
- **SPY:** S&P 500 ETF (broad market risk-on/risk-off context).
- **/NQ:** Nasdaq-100 futures (overnight and premarket tone).

**Rule:** If your trade direction conflicts with QQQ's intraday structure (trend and VWAP behavior), reduce size or stand down.

---

## Risk Management Framework

### Standard Risk Settings

- Risk per trade: 0.5% of account (adjust to 0.25%–1.0% based on consistency).
- Daily max loss: 2R to 3R (stop trading when hit).
- Max trades/day: 3–5 (prevents overtrading).
- Two-loss rule: after 2 consecutive losses, stop trading or cut size by 50%.

### Position Sizing

`Shares = (Dollar risk per trade) / (Entry price − Stop price)`

Example: $100 risk, entry $11.30, stop $11.10 → risk/share $0.20 → shares = 500.

### Universal Trade Management

- Define stop and first target before entry (no exceptions).
- Time stop: if no progress within 3 × 5m candles (15 minutes) after entry, exit or reduce.
- Take partials systematically (example): 50% at +1R; move stop to breakeven only after partial is achieved.
- Do not average down intraday; re-enter only if a new playbook trigger appears with confirmation.

---

## Daily Workflow

### Pre-market (10–15 minutes)

- Identify catalyst/attention: news, earnings, guidance, sector headlines, unusual premarket volume.
- Mark levels on 1D/1W: nearest major support/resistance zones and key moving averages (1D EMA20, SMA50/200).
- On the 15m chart, mark PMH/PML and prior day H/L/C.
- Check market context: /NQ tone, SPY and QQQ direction.
- Create an A-level plan: choose which playbook is most likely based on where price is relative to VWAP and key levels.

> **v2 UPDATE:** Add a Day-of-Week assessment to pre-market notes. Tuesday and Wednesday have historically produced the strongest ORB win rates across index/sector ETFs. Friday should be reduced-size or skip for ORB specifically. Tag every trade with weekday for journal analysis.

### First 15 Minutes (9:30–9:45 ET)

- Do not chase the first move. Let the opening range form.
- Set ORH and ORL on the 15m chart (first 15 minutes).
- Classify the day type using VWAP and slope: holding above VWAP with rising slope (trend-up); holding below with falling slope (trend-down); whipping with flat slope (mean-reversion/trap or stand-down).
- Observe 1H momentum filter: RSI and MACD improving vs deteriorating.

### Trading Windows and No-Trade Conditions

> **v2 UPDATE:** ORB playbook is now HARD-CAPPED at 10:30 ET. Research indicates 15m ORB triggers from 9:45–10:00 ET historically produce materially better win rates than mid-day triggers. After 10:30 ET, only VWAP and Trap playbooks remain in play.

- Primary execution window: 9:45–11:30 ET and 13:30–15:45 ET (avoid midday chop unless a high-conviction setup forms).
- No-trade: spreads widen materially, volume collapses, market proxy breaks sharply against you, price chops through VWAP without acceptance, VWAP is flat with no directional energy, or price is already extended beyond the 2%/3% VWAP cap.

---

## Confirmation Stack

Require minimum 3 of 5 confirmations for ORB and VWAP playbooks. Require minimum 4 of 5 for the Failed Breakout (Trap) playbook — counter-trend trades need a higher bar.

| # | Confirmation | Pass criteria |
| --- | --- | --- |
| 1 | Level | Entry occurs at ORH/ORL, PMH/PML, prior day H/L, or a clearly marked HTF level. |
| 2 | VWAP behavior + slope (v2) | Clear reclaim/hold for longs (slope rising or flattening up); rejection/fail for shorts (slope falling or flattening down). 5m close confirmation. Flat slope = stand down. |
| 3 | Market alignment | QQQ (/NQ) structure supports your trade direction (not diverging sharply). |
| 4 | Relative strength | RS line flat-to-rising for longs; flat-to-falling for shorts (vs QQQ or sector ETF). |
| 5 | Volume / RVOL | Breakout/reversal candle shows increased volume; pullbacks show contracting volume; RVOL meaningfully elevated. |

### Scoring Shortcut

- **ORB / VWAP:** 3/5 = tradeable at normal size (RR ≥ 2:1); 4–5/5 = A+, may size up modestly within plan; ≤2/5 = pass.
- **Failed Breakout (Trap):** 4/5 = tradeable at normal size; 5/5 = A+; ≤3/5 = pass.

> **v2 UPDATE:** All VWAP playbook entries must additionally pass the EXTENSION CHECK: price must be within 2% of VWAP (large-cap) or 3% (volatile small-cap) at trigger. Extension beyond limit = no trade regardless of confirmation count.

---

## The Three Core Playbooks

Trade only these three playbooks (plus pilot Playbook 4 once validated) until you have a statistically meaningful sample. This prevents strategy drift and makes journaling and improvement possible.

### Playbook 1: Opening Range Breakout (ORB) with Acceptance + Retest

Purpose: Capture trend continuation after the open once price shows acceptance outside the 15-minute opening range.

> **v2 UPDATE:** ORB entries are now restricted to 9:45–10:30 ET. Day-of-week tag is required on every trade. Reduce size or skip on Mondays and Fridays until your own journal data confirms or refutes this asymmetry on your specific tickers.

**Best Conditions**

- RVOL elevated; stock is in play.
- Market proxy (QQQ) aligned in the trade direction.
- Price holding on the correct side of VWAP with supportive slope (or reclaiming with rising slope).

**Long Setup Criteria**

- 15m establishes ORH/ORL (9:30–9:45 ET).
- Price approaches ORH while above VWAP (rising slope) or after a clean VWAP reclaim that holds.
- 1H momentum supportive (RSI > 50 and rising; MACD improving).
- Time window: trigger must occur between 9:45 and 10:30 ET.

**Long Trigger (5m execution)**

- A 5m candle closes above ORH (not just a wick).
- Preferred entry: wait for retest of ORH that holds; enter on the first 5m confirmation candle after the hold.
- Confirm 3/5 stack minimum: Level + VWAP (with slope) + Market.

**Stops and Targets**

- Stop: below the retest low (or below ORH with buffer if retest is tight).
- T1: prior high / HOD / next HTF resistance.
- T2: opening range size projected above ORH (measured move) or next HTF level.
- Management: take partial at +1R; trail under 5m higher lows for the runner.

**Invalidation**

- 5m close back inside the opening range and failure to reclaim ORH.
- Market proxy (QQQ) breaks down sharply during the trade.
- VWAP slope flips against the position and is not recovered within 1–2 candles.

### Playbook 2: VWAP Reclaim / VWAP Rejection

Purpose: Trade the session fair-value control point. VWAP often acts as a pivot; reclaim suggests buyers regained control; rejection suggests sellers defended fair value.

> **v2 UPDATE:** Liquidity floor for VWAP playbooks: ticker must have 1M+ average daily volume. Below that, VWAP loses institutional defense and behaves as a random line. Extension cap applies: no entry if price is already >2% (large-cap) or >3% (volatile) from VWAP at trigger.

**A) VWAP Reclaim Long**

- Context: price traded below VWAP early (fade/flush) and then returns to VWAP. VWAP slope flattening or beginning to rise.
- Trigger: one 5m close above VWAP.
- Entry: pullback to VWAP that holds; enter on higher-low confirmation (5m).
- Confirmations: Market alignment (QQQ stable/green) + RS improving + volume not collapsing + extension within cap.

*Stop / Targets (Reclaim Long)*

- Stop: below pullback low (or below VWAP with buffer if structure is clean).
- T1: ORH or prior pivot.
- T2: PMH/HOD or next HTF resistance.

*Invalidation (Reclaim)*

- Price closes back below VWAP and rejects VWAP on retest.
- VWAP slope rolls over to falling.

**B) VWAP Rejection Short**

- Context: price is below VWAP with falling slope; attempts to reclaim fail.
- Trigger: retest VWAP from below with 5m rejection (wick into VWAP, close back below).
- Entry: on rejection close or next weak retest failure.
- Confirmations: Market alignment bearish/weak, RS deteriorating, volume expands on rejection, extension within cap.

*Stop / Targets (Rejection Short)*

- Stop: above the VWAP rejection high.
- T1: ORL / LOD / nearby round number.
- T2: next HTF support.

### Playbook 3: Failed Breakout (Bull Trap) / Liquidity Sweep Fade

Purpose: Exploit high-probability reversals when price briefly breaks a highly visible level (PMH/ORH/prior high/round number) and then fails.

> **v2 UPDATE:** Confirmation bar raised to 4/5 for this playbook. Counter-trend trades fail more often than continuation trades, so the evidentiary requirement is higher.

**Best Conditions**

- Obvious breakout level near HTF resistance (daily/weekly zone or key MA).
- Market/sector not providing strong tailwind for the breakout.
- Fast push through the level followed by immediate rejection (classic trap).

**Short Trigger (5m execution)**

- Price breaks above a key level (PMH or ORH) but fails to hold.
- Within 1–3 candles, price closes back below that level (failure confirmation).
- Best confirmation: price also loses VWAP (slope rolling down) or rejects VWAP shortly after.
- Entry: retest of the failed level from below that fails (weak bounce).
- Confirmation requirement: 4 of 5 from the stack (raised from 3).

**Stops and Targets**

- Stop: above the sweep high or above the failed retest high.
- T1: VWAP (if entry is above VWAP) or opening range midpoint.
- T2: ORL / PML / LOD.
- Management: partial at +1R; trail above lower highs (5m) for runner.

**Invalidation**

- Reclaim and acceptance above the failed level (5m closes holding above).
- Strong market reversal upward that aligns across QQQ and SPY.

### Playbook 4 (Pilot): Anchored VWAP from Earnings Gap

> **v2 UPDATE:** New pilot playbook. DO NOT trade live until you have completed 30+ paper-trade observations and validated expectancy. The setup bridges intraday execution with 1–5 day swing duration.

Purpose: After an earnings or news gap, institutions that missed the initial entry leave large limit buy orders at the gap day's volume-weighted average price. AVWAP anchored to the gap bar becomes a dynamic support level the algorithms defend for several sessions.

**Setup Criteria**

- Gap up of 5%+ on earnings or material news with strong volume.
- Stock holds above the gap day's open by end of day (i.e., the gap did not fill).
- AVWAP is anchored to the first 1-minute candle of the gap day.

**Long Trigger**

- Over the next 3–10 sessions, price pulls back to the AVWAP line.
- Pullback shows contracting volume; reversal candle prints at AVWAP.
- Entry on confirmation candle close above AVWAP.

**Stops and Targets**

- Stop: below the AVWAP line by structure (recent swing low or 1 ATR buffer).
- T1: gap day high.
- T2: measured move from base to gap day high projected upward.

**Validation Gate (must clear before going live)**

- Minimum 30 paper-tracked observations across at least 5 different tickers.
- Expectancy ≥ +0.30R per trade after a 25% performance haircut applied to paper results.
- Maximum consecutive loss streak in observation period must be psychologically tolerable at planned live size.

---

## Thinkorswim Execution

### Chart Preparation (daily)

- Open workspace grid: market proxies (QQQ/SPY and /NQ), target ticker multi-timeframe (1W/1D/1H/15m/5m), and RS panel.
- On 1D/1W: mark major support/resistance zones and key moving averages.
- On 15m: mark PMH/PML and prior day H/L/C; create ORH/ORL after 9:45 ET.
- On 5m: VWAP (with slope visible), ORH/ORL lines, and volume must be visible and uncluttered.
- For Playbook 4 setups: add Anchored VWAP study anchored to the gap day's 9:30 candle.

### Placing the Trade

1. Identify which playbook applies (ORB / VWAP / Trap / AVWAP).
2. Verify required confirmation count (3/5 for ORB and VWAP; 4/5 for Trap).
3. Confirm VWAP slope direction and extension cap (VWAP playbooks).
4. Define stop level using structure (retest low, VWAP rejection high, or sweep high).
5. Calculate shares based on 1R. Round down to reduce slippage risk.
6. Place entry using limit orders when possible; avoid market orders in the first minutes after the open if spreads are wide.
7. Place stop immediately (OCO bracket recommended) and set first target at +1R or next level.

### Trade Management

- At +1R: take partial and reduce risk. Do not move stop to breakeven before earning it unless playbook requires.
- If VWAP slope flips against your position and you cannot reclaim within 1–2 candles, tighten risk or exit.
- Use the time stop: if trade stalls for 15 minutes, reduce or exit.

---

## Journaling and Performance Review

> **v2 UPDATE:** Journal schema is materially expanded in v2. Time-of-day, day-of-week, VWAP slope, RS percentile, and MAE/MFE are now REQUIRED fields. Without them, the weekly review cannot identify your real edge or your real leak.

### Required Journal Fields (v2)

| Field | What to record |
| --- | --- |
| Date / Ticker | YYYY-MM-DD, symbol |
| Day of Week (v2) | Mon/Tue/Wed/Thu/Fri — tag every trade |
| Time of Trigger (v2) | ET time when entry triggered (HH:MM) |
| Playbook | ORB / VWAP Reclaim / VWAP Rejection / Trap / AVWAP |
| Direction | Long/Short |
| Entry / Stop / Targets | Prices and rationale tied to levels |
| Confirmations Passed | Which of 5 (bitfield or list) — minimum 3 for ORB/VWAP, 4 for Trap |
| VWAP Slope at Entry (v2) | Rising / Falling / Flat |
| VWAP Extension at Entry (v2) | % distance from VWAP at trigger |
| Market Context | QQQ/SPY VWAP status; sector/RS status |
| Result | R multiple (+1.6R, −1R, etc.) |
| MAE / MFE (v2) | Maximum Adverse Excursion and Maximum Favorable Excursion in R units |
| Mistake / Insight | One line: what to repeat or fix |

### Weekly Review Metrics

- Win rate by playbook (separately).
- Average R (winners) and average R (losers).
- Expectancy per playbook: (Win% × AvgWin) − (Loss% × AvgLoss).
- Performance by time-of-day bucket (v2): 9:45–10:30, 10:30–11:30, 13:30–14:30, 14:30–15:45.
- Performance by day-of-week (v2): expect Tue/Wed to outperform; verify or refute on your data.
- Performance by VWAP slope (v2): rising vs falling vs flat.
- Top 2 recurring mistakes (to turn into rules).

---

## Paper Testing Protocol (v2 addition)

Before any playbook goes live, it must clear this protocol. Performance haircut applied to paper results: 25%. Live expectancy is expected to come in below paper expectancy due to slippage, partial fills, and psychological pressure.

### Phase 0: Manual Chart Study

- Mark 20 historical examples per playbook: entry, stop, target, outcome.
- This is pattern recognition, not statistics. Complete before paper trading.

### Phase 1: Isolated Playbook Paper Testing

- Trade one playbook at a time for two weeks before adding the next.
- Order: ORB → VWAP Reclaim → VWAP Rejection → Failed Breakout → AVWAP.
- Apply $0.02–0.05 slippage assumption per fill.
- Target: 50–80 trades per playbook before evaluating.

### Phase 2: Decision Gate

- Expectancy must be ≥ +0.20R after the 25% haircut.
- Minimum 50 trades per playbook.
- Maximum consecutive loss streak must be psychologically tolerable at live size.

### Phase 3: Live Micro-Sizing

- Go live at 25% of normal risk (e.g., 0.125% instead of 0.5%).
- Run 30–50 live trades; compare live expectancy to paper expectancy.
- If live expectancy is still positive after the haircut, scale to full sizing tier.

### Hard Rule

Do not add a playbook to live trading just because it cleared paper. Each playbook earns live status independently.

---

## Glossary of Acronyms and Abbreviations

All shorthand used in this document, in alphabetical order. Common trading-platform terms are included for completeness.

| Acronym | Meaning | Notes / Use in this system |
| --- | --- | --- |
| ATR | Average True Range | Volatility measure; used to size stops on volatile names. |
| AVWAP | Anchored Volume-Weighted Average Price | VWAP calculated from a chosen anchor bar (e.g., gap day open) rather than session open. Used in Playbook 4 (pilot). |
| EMA | Exponential Moving Average | Faster-reacting moving average; e.g., 20 EMA used for trailing. |
| ET | Eastern Time | All session times referenced in U.S. Eastern Time (NY market hours). |
| ETF | Exchange-Traded Fund | e.g., QQQ, SPY used as market proxies. |
| HOD | High of Day | Highest price during regular session; common target. |
| HTF | Higher Time Frame | Daily/weekly structure referenced for context above intraday charts. |
| LOD | Low of Day | Lowest price during regular session; common short target. |
| MA | Moving Average | Generic term covering SMA and EMA. |
| MACD | Moving Average Convergence Divergence | Momentum indicator; histogram and signal-line cross used as confirmation only. |
| MAE | Maximum Adverse Excursion | Worst unrealized loss reached during a trade; journal field. |
| MFE | Maximum Favorable Excursion | Best unrealized gain reached during a trade; journal field. |
| NQ / /NQ | Nasdaq-100 E-mini Futures | Premarket/overnight sentiment proxy; CME futures contract. |
| NYSE | New York Stock Exchange | U.S. equities exchange referenced in source links. |
| OCO | One-Cancels-Other Order | Bracket order type pairing stop and target; one fills, the other cancels. |
| ORB | Opening Range Breakout | Playbook 1 — break above ORH (long) or below ORL (short) with confirmation. |
| ORH / ORL | Opening Range High / Low | High and low of the first 15 minutes (9:30–9:45 ET). |
| PMH / PML | Premarket High / Low | Highest and lowest prices traded during 4:00–9:30 ET premarket session. |
| QQQ | Invesco QQQ Trust (Nasdaq-100 ETF) | Primary intraday sentiment proxy for growth/tech. |
| R / 1R | Risk Unit | Dollar amount lost if stop is hit. All outcomes expressed in R multiples (e.g., +2R, −1R). |
| RR | Reward-to-Risk Ratio | Planned profit divided by planned loss. Minimum 1.5:1; prefer 2:1+. |
| RS | Relative Strength | Ticker performance relative to a benchmark (often QQQ or SPY). Distinct from RSI. |
| RSI | Relative Strength Index | Momentum oscillator (0–100), typically RSI(14). Used as confirmation only. |
| RVOL | Relative Volume | Current volume divided by average volume baseline. Tradability filter. |
| SMA | Simple Moving Average | Unweighted average of last N closes (e.g., SMA50, SMA200). |
| SPY | SPDR S&P 500 ETF Trust | Broad market risk-on/risk-off proxy. |
| T1 / T2 | Target 1 / Target 2 | First and second profit objectives, set before entry. |
| TOS | Thinkorswim | Charles Schwab trading platform used for execution. |
| VWAP | Volume-Weighted Average Price | Session fair-value benchmark used by institutions; primary bias and execution reference. |

---

## References (selected)

- Investopedia — VWAP: https://www.investopedia.com/terms/v/vwap.asp
- Charles Schwab — Volume-Weighted Indicators in Trading: https://www.schwab.com/learn/story/how-to-use-volume-weighted-indicators-trading
- Nasdaq Trader — Opening and Closing Crosses Fact Sheet: https://www.nasdaqtrader.com/content/productsservices/trading/crosses/fact_sheet.pdf
- NYSE — Opening Auction and Price Discovery: https://www.nyse.com/data-insights/nyse-introduces-the-enhanced-nyse-auction-tool-with-opening-imbalance-history
- StockCharts ChartSchool — Relative Volume (RVOL): https://chartschool.stockcharts.com/table-of-contents/technical-indicators-and-overlays/technical-indicators/relative-volume-rvol
- Flux Charts — Opening Range Breakout (ORB) Strategy: https://www.fluxcharts.com/articles/trading-strategies/common-strategies/opening-range-breakout
- ORB time-of-day research (TOS Indicators): https://tosindicators.com/research/orb-strategy-spy-sectors-thinkorswim
- ORB day-of-week research (TOS Indicators): https://tosindicators.com/research/orb-success-rate
- VWAP slope and extension practice: https://www.snappchart.app/blog/strategy-playbooks/vwap-momentum-trading-strategy
- VWAP institutional practice (Bulls on Wall Street): https://www.bullsonwallstreet.com/post/vwap-trading-strategy
- Anchored VWAP (TradingSim): https://www.tradingsim.com/blog/vwap-indicator-guide

---

*Educational use only. Not financial advice.*
