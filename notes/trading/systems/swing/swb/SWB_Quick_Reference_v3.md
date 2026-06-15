# SW-B QUICK REFERENCE — v3

**Trend Continuation (VCP Pullback / Consolidation → Resumption) — Swing Trading — Stocks**

> **v3 CHANGES (from v2):** (1) **Quantitative sector gate backported from SW-A v3** — stock's SPDR sector ETF must be **top-third by RS vs SPY** (RS line rising); **bottom-third = NO TRADE**. Replaces v2's qualitative "sector strong or improving." (2) Footprint-metric journal fields added (U/D volume ratio, distribution-day count) for instrumentation — see §8. VCP (2+ contractions, each shallower, each on lower volume) and RS ≥ 80 remain mandatory and unchanged.

---

## 1. GO / NO-GO (60S)

- **Trend:** price above rising 50 SMA (preferably above 200 SMA); weekly structure intact.
- **Sector (v3 — quantitative gate):** stock's SPDR sector ETF **top-third by RS vs SPY** (≈ top 4 of 11), sector RS line rising. **Bottom-third / falling sector RS = NO TRADE.**
- **VCP structure:** pullback shows 2+ contractions, each shallower, each on lower volume.
- **RS percentile:** ≥ 80 vs SPY at entry — required.
- **Trigger:** clear pivot level with room to next resistance; ≥2R planned.
- **Event check:** no unplanned earnings/binary risk within 3–5 days.

## 2. SETUP FILTERS (EOD)

- **Structure:**
  - 3–20 day pullback/consolidation toward 20EMA/50SMA or prior breakout level.
  - Range tightens; higher low forms; volatility contracts.
- **VCP requirement (mandatory):**
  - 2 or more contractions during the base/pullback.
  - Each contraction shallower than previous (e.g., −15%, −10%, −5%).
  - Each contraction on lower volume than previous.
  - Final contraction within 5–10% of pivot.
- **Sector / Group strength (v3 — mandatory, quantitative):**
  - Map stock to its SPDR sector ETF (XLK/XLF/XLE/XLV/XLY/XLP/XLI/XLB/XLU/XLRE/XLC).
  - Rank 11 sectors by RS vs SPY (blend 3- and 6-month); re-rank **weekly** (top rank decays in ~21–47 days).
  - Top-third → A+ eligible. Middle-third → A/B reduced size. **Bottom-third or falling sector RS → NO TRADE.**
  - Measure sector RS *independently* of stock RS. Rank vs **SPY** (not QQQ).
- **RS leadership (mandatory):**
  - RS percentile vs SPY ≥ 80 at entry.
  - RS line flat-to-rising during pullback (not making new RS lows). Bonus tell: RS line printing a new high *ahead* of price.
- **Confirmation:**
  - RSI typically 40–60 during pullback; MACD stabilizing/turning up (confirmation only).
  - Breakout/reclaim shows volume expansion vs pullback volume.
  - ADX > 20 confirms trend strength.

## 3. ENTRY RULES

- **Entry type (pick ONE):**
  - Pullback entry (preferred): limit at 20/50 EMA or pivot with bullish candle confirmation after VCP completes.
  - Pivot-break entry: stop-limit above consolidation high with volume confirmation.
  - Retest entry: breakout then buy retest of pivot as support.
- **Acceptance rule:** breakout closing back inside range is a warning; repeated failures = no trade/exit.
- **No chase:** if extended beyond pivot, wait for pullback/retest or skip.

## 4. RISK, STOPS, SIZING

- **A+: 1.0%** equity risk (**A+ also requires a top-third sector**); **A: 0.75%**; **B: 0.50%** (or skip).
- **Position size** = AccountRisk$ / (Entry − Stop).
- **Stop:** below pullback low / final VCP contraction / consolidation low (structure-first).
- Avoid obvious stop pools when structure allows; never widen stops.
- **Portfolio heat:** max total open risk 3.0%; max sector risk 1.5%.

## 5. TARGETS + MANAGEMENT

- **T1:** next resistance / measured-move zone.
- **T2:** continuation to 2R–4R depending on volatility and structure.
- **Default:** no partial at +1R unless immediate resistance; consider partial at +2R into resistance/earnings window.
- **Runner:** trail by higher lows or 20EMA once resumption is clean.
- **Add-ons** allowed only after +1R and formation of a new tight continuation.
- **Time stop:** if trigger fails to break within 5–10 sessions (momentum fades), exit.

## 6. EXITS + CIRCUIT BREAKERS

- **Hard exit:** stop hit or trend structure breaks (lower low / MA failure with volume).
- **Failure:** breakout closes back into range with distribution; repeated failed pivots.
- **Distribution warning (v3):** a cluster of stock-level distribution days (down on higher volume) while you hold, or U/D volume ratio rolling under 1.0, is a caution flag even if price holds — tighten or reduce. (Instrumented, not yet a hard rule — see Master Plan footprint section.)
- **Circuit breakers:** 3 losses in a row → pause new entries 3 sessions; rule violation → stop new entries for the week.
- **Execution routine:** EOD scan + tickets; lunch = alerts/stops/partials only.

## 7. PAPER-TO-LIVE (v2/v3)

- Apply **25% performance haircut** to paper expectancy when projecting to live.
- Minimum 50 SW-B paper trades (30 minimum, 50+ preferred) before live consideration.
- Live gate: expectancy ≥ +0.20R after haircut; max consecutive loss streak tolerable at live size.
- Trade SW-B alone for 6 weeks before adding SW-A v3.

## 8. JOURNAL FIELDS (v3 additions)

- VCP description (contractions, depth sequence, volume trend); RS percentile (≥80); **sector ETF + sector RS rank (1–11)**.
- **U/D volume ratio (~50d)** and **stock distribution-day count (~25d)** at entry — footprint instrumentation; split expectancy by these in weekly review.
- MAE/MFE in R; result in R multiple.

---

## Glossary

| Acronym | Meaning / Use |
| --- | --- |
| ADX | Average Directional Index — trend-strength indicator. ADX > 20 confirms trend in SW-B. |
| ATR | Average True Range — volatility measure used to size stops on volatile names. |
| Distribution day | Stock (or index) down on higher volume than the prior day — institutional selling footprint. Cluster = caution. |
| EMA | Exponential Moving Average — 20 EMA trend trail, 50 EMA trend confirmation. |
| EOD | End of Day — scan/routine timing after 4:00 PM ET close. |
| MA | Moving Average — generic; SMA and EMA. |
| MACD | Moving Average Convergence Divergence — momentum indicator (confirmation only). |
| MAE / MFE | Maximum Adverse / Favorable Excursion — worst loss / best gain reached during trade. |
| OCO | One-Cancels-Other order — bracket pairing stop and target. |
| R / 1R | Risk Unit — dollars lost if stop hits. Outcomes in R multiples. |
| RR | Reward-to-Risk Ratio — minimum 1.5:1, prefer 2:1+. |
| RS | Relative Strength — ticker (or sector) vs benchmark. SW-B requires RS percentile ≥ 80 vs SPY. Distinct from RSI. |
| RSI | Relative Strength Index — momentum oscillator (0–100), confirmation only. |
| Sector RS | Sector ETF RS vs SPY; 11 SPDR sectors ranked weekly. Top-third required; bottom-third = NO TRADE. |
| SEPA | Specific Entry Point Analysis — Minervini methodology; basis for VCP. |
| SMA | Simple Moving Average (e.g., SMA50, SMA200). |
| SPDR sectors | XLK/XLF/XLE/XLV/XLY/XLP/XLI/XLB/XLU/XLRE/XLC — ranked for the sector gate. |
| SPY | SPDR S&P 500 ETF Trust — benchmark for RS and sector ranking. |
| SW-A / SW-B | Swing Playbook A v3 (Pullback/Base Breakout) / B (Trend Continuation, VCP). |
| T1 / T2 | Target 1 / Target 2 — set before entry. |
| U/D volume ratio | Up-day volume ÷ down-day volume over ~50 days. ≥1 healthy; ≥1.5–2 strong accumulation; <1 distribution. |
| VCP | Volatility Contraction Pattern — 2+ contractions, each shallower, each on lower volume. MANDATORY for SW-B. |
| VDU | Volume Dry-Up — a base day with volume well below average (≈≤50% of 50-day) signalling supply exhaustion before breakout. |

---

*Internal Trading SOP v3 — use strict risk sizing; educational use only (not investment advice).*
