# IT-4 QUICK REFERENCE — Anchored VWAP from Earnings Gap (PILOT)

**Intraday Playbook 4 (PILOT) — Bridges intraday and swing; institutional accumulation at gap day AVWAP**

> **PILOT STATUS — NOT LIVE.** Minimum 30 paper observations across 5+ tickers required. Live gate: expectancy ≥ +0.30R after 25% haircut. Live sizing starts at 25% of normal risk. Hold duration 1–5 sessions; this is an intraday/swing bridge play.

---

## 1. PILOT STATUS — READ FIRST

- **This playbook is NOT live.** Pilot status only.
- **Validation gate:** minimum 30 paper-tracked observations across 5+ tickers BEFORE going live.
- **Live threshold:** expectancy ≥ +0.30R after 25% performance haircut on paper results.
- **Live sizing:** start at 25% of normal risk (e.g., 0.125% instead of 0.5%).

## 2. GO / NO-GO (60S)

- **Catalyst:** earnings or material news gap up of 5%+ within last 1–10 sessions.
- **Strength:** stock held above gap day open by end of day (gap NOT filled).
- **Volume:** gap day printed strong RVOL (institutional participation).
- **AVWAP anchor:** anchored to first 1-minute candle of the gap day.
- **Plan:** stop below AVWAP by structure; ≥2R to gap day high or measured move.

## 3. SETUP CRITERIA

- Gap up ≥5% on earnings/news with strong volume on gap day.
- Stock holds above gap day open through close (not a failed gap).
- Over next 3–10 sessions, price pulls back toward the AVWAP line anchored to gap day.
- Pullback shows contracting volume (institutional accumulation, not distribution).
- RS line vs QQQ holds steady or improves during pullback.

## 4. CONFIRMATION + ENTRY

- **Trigger:** reversal candle prints at AVWAP; 5m or daily close ABOVE AVWAP after the pullback.
- **Preferred entry:** first higher low ABOVE AVWAP after the touch.
- **Volume:** confirmation candle shows volume pickup (defense of AVWAP by buyers).
- **No chase:** if price has run more than 1 ATR above AVWAP, wait for next test or skip.

## 5. RISK, STOPS, SIZING (PILOT)

- **Pilot risk per trade:** 0.125% (25% of normal 0.5%).
- **Stop:** below AVWAP by structure — recent swing low OR 1 ATR buffer below AVWAP.
- **Position size** = (Pilot Risk $) / (Entry − Stop).

## 6. TARGETS + MANAGEMENT

- **T1:** gap day high.
- **T2:** measured move (gap day range projected upward from base).
- **Partial:** 50% at +1R; move stop to breakeven after partial.
- **Trail:** under daily higher lows for the runner.
- **Hold duration:** 1–5 sessions typically (bridges intraday and swing).

## 7. INVALIDATION + EXITS

- **Hard exit:** daily close BELOW AVWAP with conviction (volume expansion on the break).
- **Failed test:** price touches AVWAP twice and the second hold is weaker than the first.
- **Gap fill:** price returns to gap day open with no defense → invalidation, exit.

## 8. PAPER-TEST JOURNAL FIELDS

- Date of gap; size of gap (%); RVOL on gap day; days from gap to AVWAP test.
- AVWAP price at test; volume on test candle; stop and target distances.
- Result in R; MAE/MFE; whether AVWAP held on subsequent tests.

---

## Glossary

| Acronym | Meaning / Use |
| --- | --- |
| ATR | Average True Range — volatility measure used to size stops on volatile names. |
| AVWAP | Anchored Volume-Weighted Average Price — VWAP anchored to a chosen bar (e.g., gap day open). |
| ET | Eastern Time — all session times referenced in U.S. Eastern Time. |
| ETF | Exchange-Traded Fund — e.g., QQQ, SPY used as market proxies. |
| HOD / LOD | High / Low of Day — extreme price during regular session; common targets. |
| HTF | Higher Time Frame — daily/weekly structure referenced above intraday charts. |
| MA | Moving Average — generic; covers SMA and EMA. |
| MACD | Moving Average Convergence Divergence — momentum indicator (confirmation only). |
| MAE / MFE | Maximum Adverse / Favorable Excursion — worst / best unrealized point during trade. |
| /NQ | Nasdaq-100 E-mini Futures — premarket/overnight sentiment proxy. |
| OCO | One-Cancels-Other order — bracket pairing stop and target. |
| ORB | Opening Range Breakout — Playbook 1. |
| ORH / ORL | Opening Range High / Low — first 15 minutes (9:30–9:45 ET). |
| PMH / PML | Premarket High / Low — extreme prices during 4:00–9:30 ET premarket. |
| QQQ | Invesco QQQ Trust (Nasdaq-100 ETF) — primary intraday sentiment proxy. |
| R / 1R | Risk Unit — dollars lost if stop hits. Outcomes expressed in R multiples. |
| RR | Reward-to-Risk Ratio — minimum 1.5:1, prefer 2:1+. |
| RS | Relative Strength — ticker performance vs benchmark. Distinct from RSI. |
| RSI | Relative Strength Index — momentum oscillator (0–100), confirmation only. |
| RVOL | Relative Volume — current vs average baseline; tradability filter. |
| SPY | SPDR S&P 500 ETF Trust — broad market risk-on/off proxy. |
| T1 / T2 | Target 1 / Target 2 — first and second profit objectives, set before entry. |
| TOS | Thinkorswim — Charles Schwab trading platform used for execution. |
| VWAP | Volume-Weighted Average Price — session fair-value benchmark. |

---

*Internal Trading SOP v2 — use strict risk sizing; educational use only (not investment advice).*
