# IT-2 QUICK REFERENCE — VWAP Reclaim / Rejection

**Intraday Playbook 2 — Trade the session fair-value control point**

> **v2 KEY RULES:** (1) Liquidity floor — 1M+ ADV minimum; below that VWAP is a random line. (2) Extension cap — no entry if price already >2% (large-cap) or >3% (volatile) from VWAP. (3) VWAP slope must confirm direction; flat slope = stand down. (4) 3/5 confirmations minimum.

---

## 1. GO / NO-GO (60S)

- **Liquidity floor (v2):** ticker has 1M+ average daily volume. Below that, VWAP is a random line.
- **Extension cap (v2):** price within 2% of VWAP (large-cap) or 3% (volatile small-cap) at trigger.
- **VWAP slope (v2):** rising for reclaim long; falling for rejection short; flat = NO trade.
- **Market alignment:** QQQ supports direction; sector not diverging sharply.
- **Plan:** structure-defined stop; ≥2R to first realistic resistance.

## 2A. VWAP RECLAIM LONG — SETUP

- Price traded below VWAP early (fade/flush) and is returning toward VWAP.
- VWAP slope flattening OR beginning to rise (not still falling).
- Volume not collapsing; RS line stabilizing vs QQQ.

### 2A. VWAP RECLAIM LONG — TRIGGER + ENTRY

- One 5m candle CLOSES above VWAP.
- **Preferred entry:** pullback to VWAP that holds; enter on higher-low confirmation (5m).
- **Extension check:** reject entry if already >2% (large-cap) or >3% (volatile) above VWAP.
- **Stop:** below pullback low (or below VWAP with buffer if structure clean).
- **T1:** ORH or prior pivot. **T2:** PMH/HOD or next HTF resistance.

## 2B. VWAP REJECTION SHORT — SETUP

- Price below VWAP with falling slope; attempts to reclaim fail.
- Volume expanding on rejection candle; RS deteriorating vs QQQ.

### 2B. VWAP REJECTION SHORT — TRIGGER + ENTRY

- Retest of VWAP from below with 5m REJECTION: wick into VWAP, close back below.
- Entry on rejection close OR next weak retest failure.
- **Extension check:** reject entry if already >2%/3% below VWAP.
- **Stop:** above the VWAP rejection high.
- **T1:** ORL / LOD / nearby round number. **T2:** next HTF support.

## 3. CONFIRMATION STACK (3 of 5 minimum)

1. **Level:** entry at VWAP confluence with another marked level (ORH/ORL, PMH/PML, prior day H/L).
2. **VWAP behavior + slope:** clean reclaim/rejection on 5m close, slope confirms direction.
3. **Market alignment:** QQQ supports.
4. **Relative strength:** RS direction matches.
5. **Volume:** expansion on reclaim/rejection; pullback contracts.

## 4. RISK, STOPS, SIZING

- **Risk per trade:** 0.25%–1.0% account (start at 0.5%).
- **Position size** = (Account Risk $) / (Entry − Stop).
- Daily max loss: 2–3R; two-loss rule applies.

## 5. INVALIDATION + EXITS

- **Reclaim long fails:** price closes back below VWAP and rejects on retest, OR slope rolls over to falling.
- **Rejection short fails:** 5m close above VWAP with rising slope.
- **Time stop:** 15 min (3 × 5m) without progress → exit/reduce.

## 6. JOURNAL FIELDS (v2 — REQUIRED)

- Time of trigger; day of week; VWAP slope at entry; VWAP extension % at entry.
- Confirmations passed; MAE/MFE in R; result in R multiple.

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
