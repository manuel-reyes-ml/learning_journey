# SW-A v3 QUICK REFERENCE

**Trend Pullback & Base Breakout (Continuation-from-Strength) — Swing Trading — Stocks**

> **STATUS:** Research-grounded, NOT yet data-validated. Paper-test before live (§7). Replaces SW-A v2 (Bottoming / U&R near 52-wk lows).
>
> **v3 CORE:** (1) Buy strength, not weakness — proximity to 52-wk **high**, never lows. (2) HARD trend gate: price > **rising** 50 SMA. (3) Two entry archetypes: **A = pullback-to-MA reclaim**, **B = base breakout on volume**. (4) RSI/MACD are CONFIRMATION ONLY — never triggers. (5) RS percentile ≥ 70 (SW-B uses ≥80 — see anti-drift line). (6) **NEW — sector gate:** stock's sector ETF top-third by RS vs SPY; bottom-third sector = NO TRADE.

---

## SCAN ORDER (top-down funnel)

**0** Regime: SPY/QQQ > rising 200d (else cut size). → **1** Rank 11 SPDR sectors by RS vs SPY; keep **top-third + rising RS** (re-rank weekly). → **2** *Within those sectors only:* RS ≥ 70 · price > rising 50 SMA · near 52-wk high · ADV ≥ 1M · no dilution/earnings. → **3** Find **Archetype A** (pullback reclaim) or **B** (base breakout). → **4** Score 4/6, grade, ticket (≥2R).

> **Backtest note:** also run Stages 2–3 on the *full universe* with each setup's sector tier **tagged** (top/middle/bottom). That parallel-tag run is the only way to prove the sector gate adds expectancy rather than just cutting trade count. Live/forward testing uses the sequential funnel above.

---

## 1. GO / NO-GO (60S)

- **Regime:** SPY/QQQ above rising 200-day; breadth not collapsing. Index downtrend → size down or stand down.
- **Trend (HARD GATE):** price above a **rising 50 SMA**; 50 > 200 SMA preferred. Below a **falling** 50 SMA = NOT a v3 setup. No exceptions.
- **Relative strength:** RS percentile vs SPY **≥ 70**; RS line flat-to-rising (no new RS lows).
- **Sector strength (NEW gate):** stock's sector ETF in **top-third by RS vs SPY** (≈ top 4 of 11 SPDR sectors), sector RS line rising. Bottom-third / falling sector RS = stand down.
- **Archetype present (pick ONE):** (A) controlled pullback to a rising 20/50/200 SMA that holds, OR (B) tight base with volume expanding on green days into a defined pivot.
- **Not extended:** not >25–30% above the 50 SMA at a pullback buy.
- **Dilution check:** no 424B5 / S-3 / S-1 in last 60 days. Hard disqualifier.
- **Event check:** no unplanned earnings/binary event inside 3–5 sessions.
- **Plan:** defined trigger, structure stop, **≥ 2R** to first realistic resistance.

## 2. SETUP FILTERS (EOD)

- **Trend (mandatory):** price > rising 50 SMA; 50 > 200 preferred; weekly HH/HL intact.
- **RS (mandatory):** percentile ≥ 70 vs SPY; RS line not making new lows.
- **Sector (mandatory, quantitative):** map to SPDR sector ETF (XLK/XLF/XLE/XLV/XLY/XLP/XLI/XLB/XLU/XLRE/XLC); rank 11 sectors by RS vs SPY (3–6mo blend), **re-rank weekly**. Top-third → A+ eligible; middle → A/B reduced size; bottom-third → NO TRADE. Measure independently of stock RS.
- **Archetype A — Pullback:** 3–10 session orderly dip into rising MA / prior breakout level. Contracting range AND volume. Prefer **1st or 2nd touch** of the 50 SMA; later touches degrade. Heavy-volume gap-down into the MA = warning, not setup.
- **Archetype B — Base Breakout:** tight base (VCP nice-to-have, not required for v3). Volume dries up in the base, then expands on green days under a defined pivot. Final contraction / pivot within ~5–10% of breakout.
- **Momentum (CONFIRMATION ONLY):** RSI(14) resetting/turning up (~40–50 on a leader's pullback — a floor, not a buy signal); MACD histogram improving; ADX > 20 optional.

## 3. CONFIRMATION + ENTRY

- **Confirmation stack — 4 of 6 minimum:** (1) Trend/Level · (2) Structure · (3) Volume · (4) Stock RS ≥ 70 · (5) Sector top-third · (6) Momentum turning up. ≤3/6 = pass. Trend (1) and Sector (5) are non-negotiable floors — fail either = NO TRADE regardless of count.
- **Archetype A trigger:** green daily candle **reclaims/closes above** the reference MA (or prior day high) on expanding volume. **Never buy the down day** — wait for the reclaim bar.
- **Archetype B trigger:** daily close **above pivot** on volume **≥1.5× (min) to 2× 20-day avg**. Higher-quality variant: enter the **retest** of the breakout level holding as support.
- **No chase:** if >2–3% beyond trigger without you, wait for retest or skip.
- **Acceptance rule:** reclaim that fails back below the MA next bar, or breakout that closes back inside the base, is a warning; second failure = exit/no-trade.

## 4. RISK, STOPS, SIZING

- **Tiers:** A+ **0.75%** (capped until 50+ v3 trades show positive expectancy; **A+ also requires a top-third sector**) · A **0.50%** · B **0.25%** (or skip).
- **Position size** = AccountRisk$ / (Entry − Stop).
- **Stop (structure-first):** A → below pullback swing low or below reference MA by small ATR buffer. B → below final base contraction / consolidation low (or pivot with buffer).
- **Never widen stops.** If structure forces a wider stop, **reduce shares** to hold R constant.
- **Worked example ($50k, 0.75%):** risk$ = $375. Reclaim entry $40.00, stop $38.00 → $2.00/sh → 187 sh (round to 185). T1 ≥2R = $44.00. If nearest resistance < $44 → RR fails ≥2R gate → **NO TRADE**.
- **Portfolio heat:** max total open risk 3.0%; max sector risk 1.5%.

## 5. TARGETS + MANAGEMENT

- **T1:** first major resistance / prior swing high / measured-move zone.
- **T2:** next resistance or 2R–4R extension as trend resumes.
- **Partials:** none before +1.5R unless price runs straight into resistance; consider 25–50% at +2R into resistance/earnings window.
- **Trail:** higher lows (preferred) or 20 EMA once resumption is clean. Base breakouts: trail under 5/10-day structure early, widen to 20 EMA later.
- **Add-ons:** only after +1R AND a new tight continuation forms. Never pyramid into extension.
- **Time stop:** no favorable progress in 5–10 sessions → exit/redeploy.

## 6. EXITS + FAILURE SIGNALS

- **Hard exit:** stop hit, or trend structure breaks (lower low / decisive close below reference MA on expanding volume).
- **A-failure:** closes back below reclaimed MA next session, no recovery within 1–2 bars.
- **B-failure:** breakout closes back inside base with distribution; repeated failed pivots.
- **Do-not-trade:** falling 50 SMA · index downtrend + weak breadth · **bottom-third sector or falling sector RS** · heavy-volume gap-down + weak bounce · RS < 70 or new RS lows · active dilution · earnings in 3–5 sessions · climax volume (3–5×+) on entry bar · chasing >2–3% past trigger.
- **Circuit breakers:** 3 losses in a row → pause new entries 3 sessions; rule violation → stop new entries for the week; −3R in a week → stop until next week.

## 7. PAPER-TO-LIVE

- Apply **25% performance haircut** to paper expectancy.
- Minimum **50 v3 paper trades** before live (30 floor; 50+ preferred).
- **Live gate:** expectancy ≥ **+0.20R** after haircut; max consecutive-loss streak tolerable at live size.
- **Tag Archetype A vs B separately** — they may not carry equal edge. Each earns live status independently.
- Live micro-sizing: start at 25% of normal risk (≈0.18% for A+), 30–50 live trades, scale only if live holds post-haircut.

## ANTI-DRIFT BRIGHT LINE (vs SW-B)

> One ticker = ONE playbook per trade. If it is a **mandatory-VCP + RS ≥ 80 pivot breakout** → log as **SW-B** (1.0% tier). If it is a **pullback-to-MA reclaim** or non-VCP base breakout with **RS 70–79** → log as **SW-A v3** (0.75% cap). SW-A v3 = the *pullback* book; SW-B = the *breakout* book. Do not double-count or borrow SW-B's tier.

---

## Glossary

| Acronym | Meaning / Use |
| --- | --- |
| ADX | Average Directional Index — trend-strength read; >20 supports trend quality. |
| ATR | Average True Range — volatility measure for stop buffers / sizing on volatile names. |
| EMA | Exponential Moving Average — 20 EMA for trailing; faster-reacting MA. |
| EOD | End of Day — scan/routine timing after 4:00 PM ET close. |
| MA | Moving Average — generic; covers SMA and EMA. |
| MACD | Moving Average Convergence Divergence — momentum indicator. CONFIRMATION ONLY in v3; never a trigger. |
| MAE / MFE | Maximum Adverse / Favorable Excursion — worst loss / best gain reached during trade (R units). |
| OCO | One-Cancels-Other order — bracket pairing stop and target. |
| Pivot | Highest price of the final base contraction; breakout reference level. |
| R / 1R | Risk Unit — dollars lost if stop hits. Outcomes in R multiples. |
| RR | Reward-to-Risk Ratio — minimum 2:1 for v3 entries. |
| RS | Relative Strength — ticker performance vs benchmark (SPY). v3 requires RS percentile ≥ 70. Distinct from RSI. |
| RSI | Relative Strength Index — momentum oscillator (0–100). CONFIRMATION ONLY; "RSI > 40" is a floor, not a signal. |
| RVOL | Relative Volume — current vs average baseline; participation read. |
| Sector RS | Sector ETF's relative strength vs SPY; the 11 SPDR sectors ranked weekly. Top-third required; bottom-third = NO TRADE. |
| SPDR sectors | XLK, XLF, XLE, XLV, XLY, XLP, XLI, XLB, XLU, XLRE, XLC — the 11 sector ETFs ranked for the sector gate. |
| S-1 / S-3 / 424B5 | SEC dilution filings. Hard disqualifier if filed in last 60 days. |
| SMA | Simple Moving Average — 50/200 define the trend gate (Stage-2 alignment). |
| SPY | SPDR S&P 500 ETF Trust — benchmark for RS and regime. |
| Stage 2 | Weinstein advancing stage — price above a rising long-term MA; the only stage v3 buys. |
| SW-A / SW-B | Swing Playbook A v3 (Pullback/Base Breakout) / Swing Playbook B (Trend Continuation, VCP). |
| T1 / T2 | Target 1 / Target 2 — set before entry. |
| VCP | Volatility Contraction Pattern — 2+ shallower contractions on falling volume. Mandatory in SW-B; optional in SW-A v3. |

---

*Internal Trading SOP — SW-A v3 Quick Reference. Educational use only; not investment advice. Use strict risk sizing. Research-grounded; validate via paper-testing before live.*