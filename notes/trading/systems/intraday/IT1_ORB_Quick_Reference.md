# IT-1 QUICK REFERENCE — Opening Range Breakout (ORB)

**Intraday Playbook 1 — Trend continuation after the open with acceptance + retest**

> **v2 KEY RULES:** (1) Trigger ONLY between 9:45–10:30 ET — hard cap. (2) Day-of-week tag required (Tue/Wed strongest; reduce or skip Mon/Fri). (3) 3/5 confirmations minimum including VWAP slope. (4) Flat VWAP slope = stand down.

---

## 1. GO / NO-GO (60S)

- **Time window (v2):** trigger MUST occur between 9:45–10:30 ET. Hard cap.
- **Day-of-week (v2):** tag every trade; Tue/Wed strongest, reduce size or skip Mon/Fri.
- **Day type:** price holding correct side of VWAP with supportive slope.
- **RVOL:** elevated; stock is in play with real participation.
- **Market alignment:** QQQ (/NQ) supports trade direction (not diverging sharply).
- **Plan:** clear trigger (5m close beyond ORH/ORL), stop, and ≥2R to first realistic resistance.

## 2. SETUP CRITERIA (LONG — mirror for SHORT)

- 15m chart establishes ORH/ORL during 9:30–9:45 ET.
- Price approaches ORH while above VWAP (rising slope) OR after clean VWAP reclaim that holds.
- 1H momentum supportive: RSI > 50 and rising; MACD improving.
- RS line flat-to-rising vs QQQ or sector ETF.
- Volume on the breakout candle clearly elevated.

## 3. CONFIRMATION STACK (3 of 5 minimum)

1. **Level:** entry at ORH/ORL, PMH/PML, prior day H/L, or HTF level.
2. **VWAP + slope (v2):** reclaim/hold for longs (rising/flattening up); rejection/fail for shorts. Flat slope = stand down.
3. **Market alignment:** QQQ structure supports direction.
4. **Relative strength:** RS line flat-to-rising (longs) / flat-to-falling (shorts).
5. **Volume/RVOL:** breakout candle has volume; pullbacks contract; RVOL elevated.

## 4. ENTRY EXECUTION

- **Trigger:** 5m candle CLOSES above ORH (long) or below ORL (short) — not just a wick.
- **Preferred entry:** retest of ORH/ORL that holds; enter on first 5m confirmation candle after the hold.
- **No chase:** if >1% beyond trigger without you, wait for retest or skip.
- **Orders:** use stop-limit for breakouts; OCO bracket (stop + T1) attached immediately.

## 5. RISK, STOPS, SIZING

- **Risk per trade:** 0.25%–1.0% account (start at 0.5%).
- **Position size** = (Account Risk $) / (Entry − Stop).
- **Stop:** below the retest low (or below ORH/ORL with buffer if retest is tight).
- **Daily max loss:** 2–3R; two-loss rule: cut size 50% or stop after 2 consecutive losers.

## 6. TARGETS + MANAGEMENT

- **T1:** prior high / HOD / next HTF resistance.
- **T2:** opening range size projected (measured move) or next HTF level.
- **Partial:** 50% at +1R; move stop to breakeven only after partial.
- **Trail:** under 5m higher lows for the runner.
- **Time stop:** if no progress within 3 × 5m candles (15 min), exit/reduce.

## 7. INVALIDATION + EXITS

- **Hard exit:** 5m close back inside the opening range and failure to reclaim ORH/ORL.
- **VWAP slope flip:** against position and not recovered within 1–2 candles → tighten or exit.
- **Market reversal:** QQQ breaks down sharply during long (or up sharply during short).

## 8. JOURNAL FIELDS (v2 — REQUIRED)

- Time of trigger (HH:MM ET); day of week; VWAP slope at entry; VWAP extension %.
- Confirmations passed (which of 5); MAE/MFE in R units.
- Result in R multiple; one-line mistake/insight.

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
