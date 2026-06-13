# MASTER SWING TRADING PLAN — v3

*Two-Playbook System — both continuation-from-strength:*
*SW-A v3 (Trend Pullback / Base Breakout) + SW-B (Trend Continuation / VCP)*

*v3 retires the SW-A v2 Bottoming / Undercut & Reclaim playbook and replaces it with a continuation-from-strength book; backports the quantitative sector gate to SW-B; and makes the institutional-footprint rationale explicit, with a coverage audit and proposed accumulation/distribution metrics.*

---

## Changelog — v2 → v3

| # | Change | Detail |
| --- | --- | --- |
| 1 | **SW-A replaced** | v2 Bottoming / U&R near 52-wk lows → v3 Trend Pullback / Base Breakout (continuation-from-strength). The system no longer bottom-fishes. |
| 2 | **SW-A v3 trend gate** | Hard gate: price > rising 50 SMA; 50 > 200 preferred (Weinstein Stage 2). |
| 3 | **Quantitative sector gate** | SW-A v3 *and* (backported) **SW-B**: stock's SPDR sector ETF must be top-third by RS vs SPY, RS line rising; bottom-third = NO TRADE. Replaces qualitative sector language. |
| 4 | **RS floors formalized** | SW-A v3 ≥ 70; SW-B ≥ 80 (the deliberate differentiator — see Anti-Drift). |
| 5 | **Retirement → Collapse rule** | Old "retire SW-A if contrarian book underperforms" is obsolete; replaced by "merge SW-A v3 and SW-B if statistically indistinguishable after 50 trades each." |
| 6 | **Conceptual Foundation added** | The institutional-footprint rationale is made explicit and mapped to the gates that implement it. |
| 7 | **Footprint coverage audit + A/D metrics** | New section: audits footprint coverage, identifies the distribution-detection gap, and proposes research-grounded metrics (distribution-day count, U/D volume ratio, VDU) to instrument and test. |

> The v1→v2 history is preserved in the archived v2 plan. **This document is the current source of truth.** Canonical standalone specs: `SWA_v3_Trend_Pullback_Base_Breakout.md` (SW-A v3) and `SWB_Quick_Reference_v3.md` (SW-B). Archive `SWA_Quick_Reference_v2.md` (`_RETIRED`) to prevent a second, conflicting "SW-A" definition.

---

## 1. Mission, Objectives, and Guardrails

Mission: Extract repeatable swing gains from two continuation-from-strength setups — (A) controlled pullbacks to rising moving-average support and base breakouts in confirmed uptrends (**SW-A v3**), and (B) Volatility-Contraction-Pattern breakouts in leading stocks (**SW-B**) — using rules-based execution and risk containment. The system buys strength; it does not bottom-fish.

### Primary Objectives

- Build a process with positive expectancy (not home runs).
- Limit drawdowns through predefined risk per trade and portfolio heat.

### Non-Negotiables

- Every trade has: Setup ID, entry trigger, invalidation level, stop, target(s), position size, and management rules.
- Position sizing = account risk ÷ trade risk. Always.
- Trend first, structure second, momentum indicators last (confirmation only). RSI/MACD are never triggers.

Educational use only; not financial advice.

---

## Conceptual Foundation — Following the Institutional Footprint

The system's premise (full rationale in `Tracking_Institutional_Footprints_Reference.md`): **you cannot get the rumor, but you can read its footprint.** Institutions position weeks ahead of catalysts using information retail will never access — and they cannot accumulate size without leaving residue on price and volume. The edge is not beating them to information; it is recognizing the accumulation footprint and trading the confirmed continuation they started, while avoiding the distribution they exit into.

**Both playbooks are this philosophy made mechanical.** Every gate traces to a footprint principle:

| Footprint principle (the *why*) | Implemented by (the *how*) | Coverage |
| --- | --- | --- |
| Accumulation = quiet drift up on sustained volume in an uptrend | Stage-2 trend gate (price > rising 50 SMA; 50 > 200) | ✅ Covered |
| Leadership: outperforms the index while the tape is flat/down | RS percentile gate — ≥ 70 (SW-A v3) / ≥ 80 (SW-B); RS line not making new lows | ✅ Covered |
| Strong stock inside a strong group | Quantitative sector gate (top-third SPDR by RS vs SPY) — now both books | ✅ Covered |
| Pullbacks on *contracting* volume; supply absorbed | SW-A v3 pullback volume contraction; SW-B mandatory VCP | ✅ Covered |
| Tight, orderly bases (contraction signature) | SW-B VCP (2+ shallower contractions); SW-A v3 Archetype B base | ✅ Covered |
| Breakout/reclaim on real participation | Reclaim/breakout bar ≥ 1.5×–2× 20-day average volume | ✅ Covered |
| Avoid being exit liquidity (news-day spike / climax) | No-chase rule; reject 3–5× climax bars; never buy the down day | ✅ Covered |
| News as a defensive filter, not a trigger | Earnings/binary-event check (no entry within 3–5 sessions) | ✅ Covered |
| Distinguish accumulation from **distribution** (institutional selling) | *Indirect only — no dedicated metric* | ⚠️ **GAP** — see Footprint Coverage Audit |
| Supply dry-up before the move | *Qualitative in VCP; no numeric VDU* | 🟡 Partial |

The buy-side footprint is well covered. The two open items — distribution detection and a numeric volume-dry-up — are addressed in the Footprint Coverage Audit section below.

---

## 2. Instruments, Universe, and Liquidity Standards

Instrument: U.S. listed stocks first. Options optional later (mainly for hedging/event risk).

### Universe Buckets

- Primary Swing Universe (default): price ≥ $5, average volume ≥ 1M shares/day, tight spreads.
- Special Situations / Small Caps (restricted): smaller size, fewer concurrent positions, stricter exits.

### Sector and Market Context

Sector strength is now a **quantitative hard gate in both playbooks**: the stock's SPDR sector ETF must be top-third by RS vs SPY (RS line rising); bottom-third = NO TRADE. Do not trade stocks fighting their sector.

---

## 3. Timeframes and Market Structure

- Weekly defines primary structure and major supply/demand (key highs/lows).
- Daily defines setup quality, base/pullback shape, and confirms trend.
- 30-min or 1-hr optional for timing precision.

Key structure rule: trade at or near levels, not in the middle of noise.

---

## 4. Risk Management

### 4.1 Risk per Trade (R)

R = the dollars lost if the stop is hit.

- Primary Swing Universe: 0.5%–1.0% account risk per trade.
- Special Situations / Small Caps: 0.25%–0.6% risk per trade.
- Raise risk only after ≥ 50–100 trades show stability.

### 4.2 Portfolio Heat

- Max open risk (sum of all R at current stops): 3.0%.
- Max sector exposure: 1.5%.
- Max positions: 3–8 swing positions.

### 4.3 Position Sizing

`Position size = Account Risk ($) ÷ Trade Risk ($/share)`

Example: Account $50,000; 0.75% = $375. Entry $40.00, Stop $38.00 = $2.00/share. Shares = 375 / 2.00 = 187 (round down to 185).

### 4.4 Stop Placement

- Stops belong beyond structure, not at obvious crowded levels.
- SW-A v3 Pullback: below the pullback swing low or reference MA by a small ATR buffer.
- SW-A v3 Base Breakout / SW-B: below the final base contraction / consolidation low (or pivot with buffer).
- Never widen a stop. If structure forces a wider stop, reduce share count to hold R constant.

---

## 5. Trade Management

### 5.1 Minimum Reward:Risk

- Floor 1.5R; v3 entries require **≥ 2R** to first realistic resistance.
- Avoid momentum buys without an exit.

### 5.2 Scaling Out

- No partials until +1.5R unless price runs straight into resistance.
- Optional 25%–50% partial at +2R if major resistance or earnings window.
- Trail remainder by structure (higher lows) or 20 EMA.

### 5.3 Time Stops

- SW-A v3 / SW-B: no favorable progress within ~5–10 trading days → reduce/exit.
- Loss of trend structure (breaks swing low / decisive close below key MA on volume) → exit.

---

## Playbook A — SW-A v3: Trend Pullback & Base Breakout (CURRENT)

> **Canonical spec:** `SWA_v3_Trend_Pullback_Base_Breakout.md`. This is the Master-Plan summary; the full document governs in any conflict.

Buy continuation-from-strength: a controlled pullback to rising MA support that reclaims, **or** a tight base that breaks out on expanding volume — only inside a confirmed Stage-2 uptrend, only in a strong sector. Grounded in Weinstein Stage Analysis, Minervini SEPA/VCP, the 52-week-high momentum literature (George & Hwang, 2004), and industry-momentum research (Moskowitz & Grinblatt, 1999).

> **v3 thesis:** Proximity to highs is a tailwind; proximity to lows is a headwind.

### A1) Setup Filter (must-have)

**Trend (HARD GATE)** — price > rising 50 SMA; 50 > 200 preferred (Stage 2). Below a falling 50 SMA = NOT a v3 setup, no exceptions. Weekly HH/HL intact; not extended >25–30% above the 50 SMA at a pullback buy.

**Relative Strength (mandatory)** — RS percentile vs SPY ≥ 70; RS line not making new lows. Bonus tell: RS line printing a new high *ahead* of price (leadership leading price).

**Sector / Group Strength (mandatory, quantitative)** — map to SPDR sector ETF; rank 11 sectors by RS vs SPY (3+6-month blend), re-rank weekly. Top-third + rising → A+ eligible; middle → A/B reduced size; **bottom-third or falling sector RS → NO TRADE.** Measure independently of stock RS.

**Structure — pick ONE archetype**
- **A (Pullback):** 3–10 session orderly pullback into a rising 20/50/200 SMA; contracting range AND volume; prefer 1st/2nd touch of the 50 SMA. Heavy-volume gap-down = warning, not setup.
- **B (Base Breakout):** tight base (VCP nice-to-have); volume dries up, then expands on green days into a pivot within ~5–10% of breakout.

**Momentum (CONFIRMATION ONLY)** — RSI(14) resetting/turning up (~40–50 floor, not a buy signal); MACD histogram improving; ADX > 20 optional. A single MACD cross is not an entry.

### A2) Fundamental / Event Gate
- No active dilution: no 424B5 / S-3 / S-1 in last 60 days (hard disqualifier).
- No unplanned earnings/binary event inside 3–5 sessions.

### A3) Entry Triggers
- **A:** green daily candle reclaims/closes above the reference MA (or prior day high) on expanding volume. Never buy the down day.
- **B:** daily close above pivot on volume ≥1.5×–2× 20-day average. Higher-quality variant: enter the retest of the breakout holding as support.
- **No chase:** >2–3% beyond trigger without you → wait for retest or skip.

### A4) Confirmation Stack (4 of 6 minimum)
(1) Trend/Level · (2) Structure · (3) Volume · (4) Stock RS ≥ 70 · (5) Sector top-third · (6) Momentum turning up. 4/6 = tradeable; 5–6/6 = A+; ≤3/6 = pass. **Items 1 and 5 are non-negotiable — fail either = NO TRADE.**

### A5) Risk Tier
- A+ **0.75%** (capped until 50+ SW-A v3 trades show positive expectancy; A+ also requires a top-third sector) · A **0.50%** · B **0.25%** (or skip). Do not restore a 1.0% tier on theory. Earn it with data.

### A6) Stops, Targets, Management
- Stop: structure-first (pullback swing low / MA buffer for A; final base contraction / pivot for B).
- T1: first resistance / prior swing high / measured move. T2: 2R–4R. Trail by higher lows or 20 EMA. Add-ons only after +1R and a new tight continuation.

### A7) Hard Do-Not-Trade Conditions
Price below a falling 50 SMA · index downtrend + weak breadth · bottom-third/falling sector RS · RS < 70 or new RS lows · heavy-volume gap-down + weak bounce · active dilution · earnings in 3–5 sessions · climax volume (3–5×+) on entry bar · chasing >2–3% past trigger.

---

## Playbook B — SW-B v3: Trend Continuation / VCP (CURRENT)

> **Canonical spec:** `SWB_Quick_Reference_v3.md`.

Buy strong stocks in strong sectors during pauses, then sell into continuation. SW-B is the **breakout** book (elite, narrowest tier); SW-A v3 is the **pullback** book (broader). VCP is mandatory and RS ≥ 80.

### B1) Setup Filter (must-have)
- **Trend:** price above rising 50 SMA (preferably above 200 SMA); weekly structure intact.
- **Sector (v3 — quantitative gate, backported):** stock's SPDR sector ETF top-third by RS vs SPY, RS line rising. **Bottom-third / falling sector RS = NO TRADE.** Measured identically to SW-A v3.
- **VCP (mandatory):** 2+ contractions, each shallower, each on lower volume; final contraction within 5–10% of pivot. A single pullback does NOT qualify.
- **RS (mandatory):** RS percentile ≥ 80 vs SPY at entry; RS line flat-to-rising (bonus: RS new high ahead of price).
- **Confirmation:** RSI 40–60 during pullback; MACD stabilizing/turning up; ADX > 20; breakout shows volume expansion vs pullback.

### B2) Entry / Stops / Targets / Risk
- Entry: pullback to 20/50 EMA or pivot with confirmation (preferred); pivot-break with volume; or retest of breakout as support.
- Stop: below pullback low / final VCP contraction / consolidation low.
- Risk tiers: A+ **1.0%** (A+ also requires a top-third sector) · A **0.75%** · B **0.50%** (or skip).
- T1: next resistance / measured-move. T2: 2R–4R. Trail by higher lows or 20 EMA.

---

## Playbook A vs B — Anti-Drift Bright Line (mandatory)

Both books are continuation-from-strength. Left undefined, you will grade them inconsistently and your journal will be useless.

| Dimension | **SW-A v3 (Pullback / Base Breakout)** | **SW-B (Trend Continuation — VCP)** |
| --- | --- | --- |
| Primary entry mechanic | **Buy the dip** — pullback to rising MA, reclaim on green bar | **Buy the breakout** — pivot break out of a textbook VCP |
| Base structure required | Orderly pullback **or** clean base (VCP optional) | **Mandatory VCP** (2+ shallower contractions, falling volume) |
| RS percentile floor | **≥ 70** | **≥ 80** |
| Sector gate | Top-third SPDR by RS vs SPY | Top-third SPDR by RS vs SPY (identical) |
| Conviction tier | Broader "good" continuation | Narrowest "elite" continuation |
| A+ risk cap | 0.75% (capped until proven) | 1.0% |

**Rule:** one ticker = ONE playbook per trade. Mandatory-VCP + RS ≥ 80 pivot breakout → **SW-B** (1.0% tier). Pullback-to-MA reclaim or non-VCP base breakout with RS 70–79 → **SW-A v3** (0.75% cap). Never double-count or let SW-A v3 borrow SW-B's tier. SW-B wins classification only if *all* its mandatory filters are met.

> **Collapse rule:** Run them as complements under one shared heat budget. If after 50 trades each their expectancies are statistically indistinguishable, **merge into one continuation playbook** rather than maintaining two out of attachment.

---

## Institutional Footprint — Coverage Audit & Proposed A/D Metrics

> **Status: RESEARCH-GROUNDED, NOT YET DATA-VALIDATED.** Identical discipline to the sector gate: instrument first, test for *added expectancy* (not just trade-count reduction), promote to a hard gate only on evidence. Sources: O'Neil / IBD (CAN SLIM), Minervini (SEPA/VCP/VDU), Morales & Kacher (pocket pivot), Granville (OBV), Chaikin (ADL).

### The gap: the system is accumulation-rich and distribution-blind

The buy-side accumulation footprint is well covered (see Conceptual Foundation). But "following the footprint" is two-sided — read accumulation to enter, **read distribution to avoid or exit.** Today the system detects institutional *selling* only when a hard stop is hit. That is the real hole, and it is **orthogonal** to the existing gates (which are all variants of "is volume confirming the up-move"). Most pure accumulation indicators (OBV, ADL, A/D line) are *correlated* with what you already gate on — adding them as new buy-gates would mostly cut trade count without adding information. The distribution side is where new, non-redundant signal lives.

### Proposed metrics (priority order)

| Metric | What it measures | Definition (a-priori) | Wire into |
| --- | --- | --- | --- |
| **Index distribution-day count** ⭐ | Broad institutional selling / topping risk | Index closes down ≥0.2% on higher volume than prior day; **4–6 in 4–5 weeks = risk-off** (IBD heuristic) | **Stage-0 regime gate** — cut tiers / stand down |
| **Stock distribution-day cluster** ⭐ | Institutions exiting *your* name in an uptrend | Same rule on the stock; cluster (≈4–5 in ~25 sessions) while you hold = caution | **Exit/management warning** + journal |
| **U/D volume ratio (~50d)** | Net accumulation health | Σ up-day volume ÷ Σ down-day volume; ≥1 healthy, ≥1.5–2 strong, **<1 = distribution** | **Confirmation health check** + journal |
| **Volume Dry-Up (VDU)** | Supply exhaustion before the move | A base day with volume ≈ ≤50% of 50-day avg (ideally narrowest range) before reclaim/breakout | **Confirmation refinement** (base quality) + journal |
| **OBV trend / divergence** | Accumulation confirm; distribution warning | OBV rising with price = confirm; OBV failing to confirm new price high = warning | Optional confirm (⚠️ correlated with U/D — pick one primary) |
| **RS line new high ahead of price** | Leadership leading price | RS line vs SPY prints a new high while price still based | Bonus confirmation (already noted in both books) |

⭐ = recommended first live additions (orthogonal, regime/exit-level, low risk to trade count).

### Flagged for later (not adopted — scope/validation)

- **Pocket pivot (Morales & Kacher):** an up day whose volume exceeds the highest down-day volume of the prior 10 days, occurring inside a base / along the 10- or 50-day MA — an *earlier* accumulation entry than the standard breakout. Candidate future **Archetype C** for SW-A v3; do not trade until specified and paper-validated as its own tagged sub-strategy.

### Discipline guardrails (non-negotiable)

- None of these are validated on your data. They enter as **instrumentation and regime/exit signals**, not new hard buy-gates.
- **Do not stack correlated filters.** U/D ratio, OBV, ADL, accumulation-day counts all measure the same thing; choose **one** net-accumulation metric (recommended: U/D ratio) and the orthogonal **distribution-day count**.
- Log every proposed metric on every trade; in the weekly/monthly review, split realized expectancy by metric bucket. Promote to a hard gate **only** if it out-expectancies the alternative after costs — same parallel-tag test as the sector gate. If it only cuts count, drop it.
- The **index distribution-day count is the recommended first wire-in** (Stage-0 regime), because it is orthogonal, market-level, and changes position *size/posture* rather than adding another single-name entry hurdle.

---

## 6. Shared Business Rules

### A) Portfolio Heat and Exposure
- Max total open risk 3.0%; max sector risk 1.5%. Reduce tiers in choppy markets, after drawdown triggers, or on a rising index distribution-day count.

### B) Circuit Breakers
- 3 consecutive losses → pause new entries 3 trading days.
- Rule violation → pause new entries rest of week and review.
- −3R in a week → stop opening new positions until next week.
- Two consecutive max-loss weeks → reduce risk/trade 25–50% for the next month.

### C) Earnings / Binary Events
- Default: no new entries within 3–5 trading days of earnings.
- Hold through earnings only with prewritten plan + reduced size.

### D) Behavioral Rules
- No trades without a completed trade ticket.
- Avoid trading the open for new entries.
- No third-party tips trades.

---

## 7. Operational Routine (8–5 Job)

### Daily (Weekdays)

**Evening (30–60 min)**
- Run both scanners. SW-A v3: top-down funnel (Stage 0 regime → Stage 1 sector rank → Stage 2 strong stocks in strong sectors → Stage 3 archetype). SW-B: VCP + RS ≥ 80 within top-third sectors.
- Update index distribution-day count (regime posture).
- Chart review weekly → daily → key levels.
- Validate gates: SW-A v3 (trend, RS ≥ 70, sector top-third, archetype, ≥2R); SW-B (VCP, RS ≥ 80, sector top-third).
- Shortlist (5–15); write a ticket per A+ setup; set alerts; pre-stage OCO.

**Lunch Hour (15–30 min)** — check alerts/levels; place/adjust orders (limit, no chasing); update stops if rules require.

**After Close (15–25 min)** — journal and grade execution; capture screenshots; log footprint metrics.

### Weekly (Sunday evening, 60–90 min)
- **Re-rank the 11 SPDR sectors by RS vs SPY** (top rank is perishable). Review prior week trades, sizing, goals. Update weekly trend/levels.

### Monthly (60–120 min)
- Full process and analytics review; split realized expectancy by sector tier and by footprint-metric bucket (test the gates). Adjust only after enough sample size.

---

## 8. Trade Ticket Template (v3)

| Field | Entry |
| --- | --- |
| Trade ID | YYYY-MM-DD-TICKER-A or -B |
| Playbook | SW-A v3 or SW-B |
| Market Regime | Index trend (weekly/daily) + breadth + **index distribution-day count** |
| Levels | Weekly S/R, Daily S/R, MA levels (20/50/200) |
| Trend Gate (SW-A v3) | Price > rising 50 SMA? 50 > 200? (Yes/No) |
| Entry Archetype (SW-A v3) | A (Pullback-to-MA) / B (Base Breakout) |
| Reference MA & Touch Count (SW-A v3) | 20/50/200 reclaimed; 1st/2nd/later touch |
| RS Percentile | SW-A v3 ≥ 70 / SW-B ≥ 80 |
| Sector ETF & Rank | e.g., XLK — rank _ of 11 (top-third for A+); RS line rising? |
| VCP Structure (SW-B) | Contraction count, depth sequence, volume trend |
| Footprint metrics | U/D volume ratio (~50d); VDU present (Y/N); stock distribution-day count (~25d) |
| Dilution Check | No 424B5/S-3/S-1 in 60 days — Confirmed (Yes/No) |
| Volume Signature | Pullback/base contracting? Reclaim/breakout bar ×avg? |
| Entry Trigger / Price | Reclaim / pivot-break / retest |
| Stop Price (invalidation) | |
| Trade Risk $/share | Entry − Stop |
| Account Risk ($) / Size | Per grade/tier; size = risk$ ÷ trade risk |
| Targets | T1 (structure), T2 (R-multiple), Trail rule; ≥2R confirmed (Yes/No) |
| Confirmations Passed | x / 6 (SW-A v3) |
| Exit Triggers | Structure violation, distribution cluster, thesis broken, event window |
| Post-Trade Grade | A/B/C (process), notes, screenshots |

---

## 9. Journal Fields (v3 — Expanded)

Setup type (SW-A v3 / SW-B) · Entry Archetype (A/B — tag separately) · Setup grade (A+/A/B) · Regime (index trend + breadth + **index distribution-day count**) · Trend gate (50/200 state) · Entry type (reclaim/pivot/retest) · RS percentile · **Sector ETF + sector RS rank (1–11)** · Touch count (SW-A v3) · VCP description (SW-B) · Volume signature · **U/D volume ratio (~50d)** · **VDU present (Y/N)** · **Stock distribution-day count (~25d)** · Planned R / Realized R · **MAE / MFE (R units)** · Rule-adherence score (0/1 per rule) · Mistake/Insight.

> **Instrument the new filters so they can be tested.** Split realized expectancy by sector tier AND by footprint-metric bucket. A filter that does not out-expectancy its alternative after costs is cutting trade count, not adding edge — drop it.

---

## 10. Paper Testing Protocol (v3)

Apply a 25% performance haircut to paper expectancy when projecting to live.

### Phase 0: Manual Chart Study
- Mark 20 historical examples per playbook (and per SW-A v3 archetype): entry, stop, target, outcome. Complete before paper trading.

### Phase 1: Paper Test Sequence
- SW-B first (6 weeks alone), then add SW-A v3.
- **Tag SW-A v3 Archetype A and B separately.** Apply $0.02–0.05 slippage.
- Minimum 50 trades per playbook (30 floor; 50+ preferred).

### Phase 2: Decision Gate
- Per playbook/archetype: win rate, avg winner R, avg loser R, expectancy, profit factor, max consecutive losses.
- Live gate: expectancy ≥ +0.20R after 25% haircut, ≥ 50 trades, tolerable max-loss streak at live size.

### Phase 3: Live Micro-Sizing
- Go live at 25% of normal risk (≈ 0.18% for SW-A v3 A+). 30–50 live trades; compare to paper. Scale only if live holds post-haircut.

### Hard Rule
Each playbook — and each SW-A v3 archetype — earns live status independently.

### Collapse Condition (replaces v2 SW-A retirement condition)
If, after 50 trades each, SW-A v3 and SW-B expectancies are statistically indistinguishable, **collapse into a single continuation playbook.** (The old v2 rule — "retire SW-A if the contrarian book underperforms SW-B" — is obsolete: SW-A is no longer contrarian.)

---

## 11. AI Agent Use

### High-Value Automations
- Daily scanning + shortlist. SW-A v3: staged top-down funnel. SW-B: VCP + RS ≥ 80 in top-third sectors.
- **Backtest attribution (parallel-tag mode):** run stock+setup logic on the full universe with sector tier AND each footprint metric tagged — the only way to prove a gate adds expectancy rather than cutting count. Enforce point-in-time GICS/ETF membership and as-of ranks (no look-ahead).
- Index + stock distribution-day counters as a daily regime/health report.
- Chart briefing pack; trade-ticket auto-fill with sizing, RR, portfolio-heat check.
- Journaling + grading assistant (R-multiples, MFE/MAE, expectancy-by-tier and by-footprint-metric).
- Process compliance monitor (rule-break detection).

### Do Not Delegate
- AI deciding trades without your confirmation.
- Using AI sentiment outputs as primary signals.

### Implementation Path
- Phase 1 (manual + assisted): AI produces watchlist + tickets; you approve execution.
- Phase 2 (semi-automated): AI generates OCO brackets; you click approve.
- Phase 3 (research only): automated backtests + walk-forward / out-of-sample testing.

---

## 12. Glossary of Acronyms and Abbreviations

| Acronym | Meaning | Notes / Use in this system |
| --- | --- | --- |
| ADL | Accumulation/Distribution Line | Close-location × volume accumulation read (Chaikin). Correlated with U/D ratio — use one. |
| ADX | Average Directional Index | Trend-strength read; >20 supports trend quality. |
| Accumulation day | Up day on higher volume than prior day | Institutional buying footprint. |
| Archetype A / B | SW-A v3 entry types | A = pullback-to-MA reclaim; B = base breakout. Tagged separately. |
| ATM offering | At-The-Market Offering | SEC 424B5; dilution signal. Hard disqualifier. |
| ATR | Average True Range | Sizes stop buffers on volatile names. |
| Distribution day | Down day (≥0.2%) on higher volume than prior day | Institutional selling footprint. Index: 4–6 in 4–5 weeks = risk-off. Stock: cluster = exit caution. |
| EMA | Exponential Moving Average | 20 EMA trailing; faster-reacting MA. |
| GICS | Global Industry Classification Standard | Backtests must use point-in-time membership (2018 reshuffle moved GOOGL/META/NFLX). |
| MA / MACD | Moving Average / Moving Average Convergence Divergence | MACD = CONFIRMATION ONLY; first cross often a trap. |
| MAE / MFE | Max Adverse / Favorable Excursion | R units; journal fields. |
| OBV | On-Balance Volume | Up/down-volume running total (Granville). Divergence = distribution warning. |
| OCO | One-Cancels-Other Order | Bracket pairing stop and target. |
| Pivot | Final base-contraction high | Breakout reference for Archetype B / SW-B. |
| Pocket pivot | Morales & Kacher accumulation entry | Up day vol > highest down-day vol of prior 10 days, at the MA/in-base. Flagged future Archetype C. |
| R / 1R / RR | Risk Unit / Reward-to-Risk | Outcomes in R multiples; v3 entries require ≥2R. |
| RS / RSI | Relative Strength / RS Index | RS (vs SPY): SW-A v3 ≥70, SW-B ≥80. RSI = confirmation only. Distinct. |
| Sector RS | Sector ETF RS vs SPY | 11 SPDRs ranked weekly; top-third required, bottom-third = NO TRADE (both books). |
| SPDR sectors | XLK/XLF/XLE/XLV/XLY/XLP/XLI/XLB/XLU/XLRE/XLC | Ranked for the sector gate. |
| S-1 / S-3 / 424B5 | SEC dilution filings | Hard disqualifier if filed in last 60 days. |
| Stage 2 | Weinstein advancing stage | Price above a rising long-term MA; the only stage v3 buys. |
| SW-A / SW-B | Playbook A v3 (Pullback/Base Breakout) / B (Trend Continuation, VCP) | Both continuation-from-strength. |
| U/D volume ratio | Up-volume ÷ down-volume (~50d) | ≥1 healthy; ≥1.5–2 strong accumulation; <1 distribution. |
| U&R | Undercut & Reclaim | **Retired with SW-A v2.** Kept only to flag the change. |
| VCP | Volatility Contraction Pattern | 2+ shallower contractions on falling volume. Mandatory SW-B; optional SW-A v3. |
| VDU | Volume Dry-Up | Base day with volume ≈ ≤50% of 50-day avg before breakout — supply exhaustion (Minervini). |

### Key References
- George & Hwang (2004), *The 52-Week High and Momentum Investing*, Journal of Finance.
- Moskowitz & Grinblatt (1999), *Do Industries Explain Momentum?*, Journal of Finance.
- Weinstein (1988), *Secrets for Profiting in Bull and Bear Markets* (Stage Analysis).
- Minervini, *Trade Like a Stock Market Wizard* / *Think and Trade Like a Champion* (SEPA / VCP / VDU).
- O'Neil, *How to Make Money in Stocks* / IBD (CAN SLIM; distribution days; Accumulation/Distribution Rating).
- Morales & Kacher, *Trade Like an O'Neil Disciple* (pocket pivots).

---

*Educational use only. Not financial advice. v3 source of truth — standalone SW-A v3 and SW-B documents govern in any conflict. Footprint A/D metrics are research-grounded and unvalidated; instrument and test before promoting to hard gates.*