# SW-A v3 — TREND PULLBACK & BASE BREAKOUT

*Continuation-from-Strength (Buy-the-Dip-in-an-Uptrend + Base Breakout on Expanding Volume) — Swing Trading — Stocks*

*Replaces SW-A v2 (Bottoming / Undercut & Reclaim near 52-week lows). Built from researched professional practice (Weinstein Stage Analysis, Minervini SEPA/VCP, the 52-week-high momentum literature, and published pullback systems).*

---

> **READ FIRST — WHAT THIS DOCUMENT IS AND IS NOT**
>
> This is a **candidate replacement for SW-A**, not a brand-new system. The setup you described — *price touching a rising 20/50/200 SMA on a pullback, or basing and expanding volume on green days, with RSI > 40 and MACD turning up* — is **continuation-from-strength**. It occupies the same family as your existing **SW-B (Trend Continuation)**. The single largest risk in adopting it is **strategy drift**: SW-A v3 and SW-B collapsing into one fuzzy playbook you grade inconsistently. Section 11 defines the bright lines that keep them distinct. Read it before you trade either.

---

## Changelog — SW-A v2 → SW-A v3

The v2 bottoming playbook bought stabilization near 52-week lows with a mandatory Undercut & Reclaim. Your stated concern is correct and is supported by the evidence: stocks are usually near 52-week lows for a *reason* (deteriorating fundamentals, not just rotation), and the contrarian base rate is poor. The academic momentum literature points the other direction — nearness to the **52-week high** has stronger forecasting power for forward returns than past returns alone, and those forecasted returns **do not reverse** in the long run (George & Hwang, 2004). v3 abandons bottom-fishing entirely and reallocates SW-A's risk budget to continuation-from-strength.

| Area | SW-A v2 (Bottoming) | SW-A v3 (Trend Pullback / Base Breakout) |
| --- | --- | --- |
| Core thesis | Buy marginal new low + reclaim near 52-wk low | Buy controlled pullback to rising MA support, or base breakout on expanding volume, in a confirmed uptrend |
| Location | Within 5–10% of **52-week low** | Above rising **50 SMA**, ideally above 200 SMA (Weinstein Stage 2); within reach of 52-week **high** |
| Mandatory structure | Undercut & Reclaim (U&R) | Stage-2 uptrend + one of two entry archetypes (Pullback-to-MA **or** Base Breakout) |
| Trend filter | None (contrarian by design) | **Hard gate:** price > rising 50 SMA; 50 SMA > 200 SMA preferred. A pullback in a downtrend is disqualified. |
| Relative strength | RS line flat-to-rising | **RS floor ≥ 70 percentile vs SPY** (below SW-B's ≥80; see §11) |
| Sector / group strength | Qualitative ("sector strong or improving") | **NEW — quantitative gate:** stock's sector ETF must be in the top-third by RS vs SPY (and RS line rising). Weak/bottom-third sector = NO TRADE. |
| Dilution disqualifier | 424B5 / S-3 / S-1 in last 60 days | Retained — same hard disqualifier |
| RSI / MACD role | Confirmation only | Confirmation only (unchanged) — **never a trigger.** Your raw "RSI>40 + MACD cross" is graded and tightened in §3 and §4. |
| Volume | >1.5× avg on up days | Pullback volume must **contract**; breakout/reclaim bar **≥1.5× (min) to 2× 20-day avg**; avoid 3–5× climax bars |
| Risk tier A+ | 0.75% (capped) | 0.75% (capped until 50+ v3 trades show positive expectancy — see §5) |

---

## 1. Thesis and Evidence Base

You are moving capital from a low-base-rate contrarian setup to a higher-base-rate continuation setup. The professional and academic record supports the direction of that move:

- **52-week-high momentum (George & Hwang, 2004, *Journal of Finance*).** Nearness to the 52-week high dominated and improved on past-return momentum for forecasting forward returns, and those returns did not reverse long-term. The effect has since replicated out-of-sample across most international markets. Practical read: *proximity to highs is a tailwind; proximity to lows is a headwind.* This is the empirical core of the switch.
- **Weinstein Stage Analysis.** Only buy in **Stage 2** (price breaking out and holding above a **rising** 30-week / ~150-day MA, with volume confirmation and strong relative strength). The two highest-quality entries are the **initial Stage-2 breakout** and the **retest of that breakout**. The classic errors are buying Stage 1 (premature) or Stage 3/4 (late, or into a falling MA). "Big base = big move."
- **Minervini SEPA / VCP.** Inside a Stage-2 uptrend, the cleanest base is a **Volatility Contraction Pattern** — progressively shallower pullbacks on declining volume — with entry at the **pivot breakout on expanding volume** and the stop just below the final contraction. His Trend Template requires RS rank and price above key moving averages.
- **Sector / industry momentum (Moskowitz & Grinblatt, 1999, *Journal of Finance*).** Industry momentum accounts for *much* of the individual-stock momentum anomaly — once industry returns are controlled for, individual-stock momentum largely disappears, and buying stocks from winning industries is itself highly profitable. Practitioner work concurs: roughly half of a stock's move is attributable to its sector/industry group (O'Neil's "L"; Weinstein: *"two equally bullish charts will perform far differently if one is from a bullish sector and the other from a bearish group"*). Bulkowski's test: holding stocks from the #1-ranked industry returned ~28% vs ~2% for the S&P over matched holds (1995–2007). **Caveats baked into §3/§9:** sector rank is perishable (top rank persists only ~21–47 days → re-rank weekly), it correlates with stock RS (measure it independently), and it whipsaws at sharp regime turns (tie to the regime gate).
- **Published pullback systems (e.g., Livingston's 50-day pullback method; the 9/20-EMA "pullback to support" framework).** Consistent rules across practitioners: trade pullbacks **only in confirmed uptrends**; the **first one or two touches** of the 50-day are more reliable than later touches; **never buy a down day** — wait for the green reclaim candle; require volume expansion on the reclaim and contraction into the dip.

The common thread across all four: **trend first, structure second, momentum indicators last (confirmation only).** v3 is built in that order. Operationally, the gates run as a **top-down funnel** — regime → sector → stock → setup — defined in §14, with a matching staged screener in §15.

---

## 2. GO / NO-GO (60s)

- **Regime (market):** SPY/QQQ above rising 200-day; broad participation not collapsing. In a clear index downtrend, **size down or stand down** (continuation setups fail far more often when the index is below its long-term average).
- **Trend (stock) — HARD GATE:** price above a **rising 50 SMA**; 50 SMA above 200 SMA preferred. Higher highs / higher lows intact on the daily. *If price is below a falling 50 SMA, this is not a v3 setup — skip.*
- **Relative strength:** RS percentile vs SPY **≥ 70** and RS line flat-to-rising (not making new RS lows).
- **Sector strength (NEW gate):** the stock's sector ETF is in the **top-third by RS vs SPY** (≈ top 4 of the 11 SPDR sectors) and its RS line vs SPY is rising. Bottom-third sector, or sector RS making new lows, = stand down — do not fight a weak group.
- **Entry archetype present (pick ONE):** (A) controlled **pullback** to a rising 20/50/200 SMA that is holding, **or** (B) tight **base** with volume expanding on green days into a defined pivot.
- **Volume signature:** pullback/base volume **contracting**; the reclaim or breakout bar shows **≥1.5× 20-day average** participation.
- **Dilution check:** no SEC 424B5 / S-3 / S-1 in last 60 days (hard disqualifier, retained from v2).
- **Event check:** no unplanned earnings/binary event inside 3–5 sessions.
- **Plan:** defined trigger, structure-based stop, and **≥ 2R** to first realistic resistance.

---

## 3. Setup Filters (EOD)

**Trend (mandatory — the gate that keeps you out of the 52-week-low trap)**

- Daily: price > rising 50 SMA; 50 SMA > 200 SMA preferred (Stage 2).
- Weekly structure intact (higher highs / higher lows); not extended >25–30% above the 50 SMA at the moment you're buying a pullback (over-extension = wait).

**Relative Strength (mandatory)**

- RS percentile vs SPY ≥ 70 at entry. (Deliberately below SW-B's ≥80 — see §11 for why this is the differentiator, not an accident.)
- RS line not making new lows while price pulls back.

**Sector / Group Strength (mandatory — quantitative)**

- Map the stock to its SPDR sector ETF (XLK, XLF, XLE, XLV, XLY, XLP, XLI, XLB, XLU, XLRE, XLC).
- Rank all 11 sectors by RS vs **SPY** over a consistent lookback (blend 3- and 6-month; re-rank **weekly** — top rank decays in ~21–47 days).
- **Tiered rule:**
  - Sector **top-third** (≈ top 4) AND its RS line vs SPY rising → A+ eligible ("double-RS": strong stock in a strong group).
  - Sector **middle-third** → A/B grade only, trade at reduced size.
  - Sector **bottom-third**, or sector RS line making new lows → **NO TRADE.**
- Measure sector strength *independently* of the stock's own RS — a leader inside a lagging group is a yellow flag, not a green light.
- Benchmark note: rank sectors against **SPY** (common yardstick). QQQ stays the intraday tech-sentiment proxy; it is not used for cross-sector ranking because it is itself tech-weighted.

**Structure — Entry Archetype A: Trend Pullback**

- 3–10 session controlled pullback into a rising 20/50/200 SMA (or prior breakout level acting as support).
- Pullback is **orderly**: contracting range, contracting volume, no large gap-down on heavy volume. A heavy-volume gap-down into the MA is a *warning*, not a setup.
- Prefer the **first or second touch** of the 50 SMA after a fresh advance; later touches degrade.

**Structure — Entry Archetype B: Base Breakout**

- Tight consolidation/base (ideally 2+ contractions, each shallower — i.e., a VCP, but a clean rectangle/flag also qualifies for v3).
- Volume **dries up** into the base, then **expands on green days** as price coils under a defined pivot.
- Final contraction / pivot within ~5–10% of the breakout level.

**Momentum (CONFIRMATION ONLY — not a trigger)**

- RSI(14) resetting and turning up (typically ~40–50 on a leader's pullback; do not treat "RSI > 40" as a buy signal — see grading note below).
- MACD stabilizing / histogram improving. A single MACD cross is **not** an entry.
- ADX > 20 supports trend quality (optional read).

> **GRADING YOUR RAW CRITERIA (blunt).** You proposed: *"RSI > 40 and MACD turning positive from negative."* As stated, both are weak as **triggers** and fine as **confirmation**:
> - **"RSI > 40"** describes the majority of all trading conditions. It is a floor, not an edge. Keep it as a *gate* (don't buy a leader whose RSI is collapsing through 40), but the *trigger* is price reclaiming the MA on a green bar with volume — not the RSI value.
> - **"MACD turning positive from negative"** lags and whipsaws. Published technical work is explicit that the **first crossover is frequently a trap** — a single MACD cross, a quick RSI bounce, or one green candle after a selloff is usually *not* enough to confirm a trend transition. Demand confluence: structure (reclaim/breakout) **+** volume expansion **+** momentum turning up — in that priority order. MACD confirms; it does not lead.
>
> Net: your instincts are sound, but in your own system's language these are **confirmation-stack items, not entry triggers.** v3 enforces that.

---

## 4. Entry Rules

**Entry Archetype A — Trend Pullback (preferred when trending)**

- Trigger: after the pullback into the rising MA, a **green daily candle reclaims/closes back above the reference MA (or the prior day's high)** on expanding volume.
- Do **not** buy the down day. Wait for the reclaim bar. (This single rule removes most knife-catching.)
- Preferred fill: on the reclaim close, or on a tight next-day continuation; stop below the pullback swing low.

**Entry Archetype B — Base Breakout (preferred when basing)**

- Trigger: a daily close **above the pivot** on volume **≥1.5× (min) to 2× the 20-day average**.
- Optional higher-quality variant: enter on the **retest** of the breakout level holding as support (Weinstein's second buy point), which tightens risk.

**Universal entry rules**

- **Confirmation stack — minimum 4 of 6** (see §6). Below 4, it is a NO TRADE.
- **No chase:** if price is already >2–3% beyond the trigger without you, wait for a retest or skip. (Chasing is an explicit Execution Error in post-trade review.)
- **Acceptance rule:** a breakout that closes back inside the base, or a reclaim that fails back below the MA on the next bar, is a warning; a second failure is an exit/no-trade.

---

## 5. Risk, Stops, Sizing

- **Risk tiers:** A+ **0.75%** (capped), A **0.50%**, B **0.25%** (or skip). The A+ cap stays until **50+ SW-A v3 trades** show positive expectancy. **A+ additionally requires a top-third sector** (a strong stock in a middle-tier group is capped at the A tier). *Note for discipline:* "safer in theory" is not "proven" — do not restore a 1.0% tier on the basis of this document. Earn it with data.
- **Position size** = AccountRisk$ ÷ (Entry − Stop).
- **Stop placement (structure-first):**
  - Archetype A: below the **pullback swing low**, or below the reference MA by a small ATR buffer (whichever is structurally cleaner).
  - Archetype B: below the **final base contraction / consolidation low** (Minervini-style), or below the breakout pivot with buffer.
- **Never widen a stop.** If structure forces a wider stop, **reduce share count** (ATR-adjust) to hold R constant.
- **Portfolio heat:** max total open risk 3.0%; max sector risk 1.5% (unchanged from system standard).

> **Worked example (your $50,000 convention, 0.75% A+ tier).**
> AccountRisk$ = 50,000 × 0.0075 = **$375**.
> Entry on 50-SMA reclaim at $40.00; pullback swing low at $38.20 → stop $38.00 → trade risk = **$2.00/share**.
> Shares = 375 ÷ 2.00 = **187** (round down to 185).
> First target ≥ 2R → +$4.00 → **$44.00**. If the nearest real resistance is below $44, the RR fails the ≥2R gate → **NO TRADE** or wait for a better entry. This is the math check you asked me to enforce on every sizing decision.

---

## 6. Confirmation Stack (4 of 6 minimum)

| # | Confirmation | Pass criteria |
| --- | --- | --- |
| 1 | **Trend / Level** | Price > rising 50 SMA; entry at a defined level (rising MA support for pullback, or pivot for breakout). |
| 2 | **Structure** | Orderly pullback into MA (A) **or** tight base with contracting volume (B). No heavy-volume gap-down into the level. |
| 3 | **Volume** | Pullback/base volume contracts; reclaim/breakout bar ≥1.5×–2× 20-day average. Reject 3–5× climax bars (exhaustion, not continuation). |
| 4 | **Relative strength (stock)** | RS percentile ≥ 70 vs SPY; RS line flat-to-rising. |
| 5 | **Sector / group strength** | Stock's sector ETF top-third by RS vs SPY, RS line rising. (Hard floor: bottom-third sector = NO TRADE regardless of score — see §9.) |
| 6 | **Momentum (confirmation only)** | RSI resetting and turning up; MACD histogram improving. Never sufficient alone. |

**Scoring:** 4/6 = tradeable at normal size for grade; 5–6/6 = A+, may size to tier cap; ≤3/6 = pass. Items 1 (trend) and 5 (sector floor) are non-negotiable — failing either is an automatic NO TRADE even if the count is met.

---

## 7. Targets and Management

- **T1:** first major resistance / prior swing high / measured-move zone.
- **T2:** next resistance or 2R–4R extension as the trend resumes.
- **Partials:** default no partial before +1.5R unless price runs straight into resistance; consider 25–50% partial at +2R into resistance or an earnings window.
- **Trail:** by higher lows (preferred) or the 20 EMA once resumption is clean. For base breakouts, trail under the 5/10-day structure early, then widen to 20 EMA.
- **Add-ons:** only after +1R **and** the formation of a new tight continuation (do not pyramid into extension).
- **Time stop:** if the trigger fails to make favorable progress within 5–10 sessions (momentum fades), exit and redeploy.

---

## 8. Exits and Failure Signals

- **Hard exit:** stop hit, or trend structure breaks (lower low / decisive close below the reference MA on expanding volume).
- **Pullback-entry failure:** price closes back below the reclaimed MA the next session and does not recover within 1–2 bars.
- **Breakout-entry failure:** breakout closes back inside the base with distribution; repeated failed pivots.
- **Circuit breakers (unchanged):** 3 losses in a row → pause new entries 3 sessions; rule violation → stop new entries for the week; −3R in a week → stop opening positions until next week.

---

## 9. Hard Do-Not-Trade Conditions

- Price below a **falling** 50 SMA (this is the 52-week-low trap re-entering through the back door — the exact risk you're trying to eliminate). **No exceptions.**
- Index (SPY/QQQ) in a confirmed downtrend and breadth deteriorating → stand down or quarter-size.
- Heavy-volume gap-down into the MA followed by a weak, low-conviction bounce.
- RS percentile < 70 or RS line making new lows while you're trying to buy "strength."
- **Sector in the bottom-third by RS vs SPY, or sector RS line making new lows** — do not fight a weak group, even if the individual chart looks clean.
- Active dilution (424B5 / S-3 / S-1 in last 60 days).
- Earnings/binary event inside 3–5 sessions.
- Climactic volume (3–5×+ average) on the entry bar — that is exhaustion behavior, not continuation.
- You are chasing: price already extended >2–3% beyond trigger.

---

## 10. Relationship to SW-B and the Anti-Drift Rule

SW-A v3 and SW-B are both continuation-from-strength. Left undefined, you will grade them inconsistently and your journal will be useless. The bright lines:

| Dimension | **SW-A v3 (Trend Pullback / Base Breakout)** | **SW-B (Trend Continuation — VCP)** |
| --- | --- | --- |
| Primary entry mechanic | **Buy the dip** — pullback to rising MA support, reclaim on green bar | **Buy the breakout** — pivot break out of a textbook VCP |
| Base structure required | Orderly pullback **or** clean base (VCP *nice-to-have*, not required) | **Mandatory VCP**: 2+ contractions, each shallower, each on lower volume |
| RS percentile floor | **≥ 70** | **≥ 80** |
| Conviction tier | Broader, "good" continuation | Narrowest, "elite" continuation |
| A+ risk cap | 0.75% (capped until proven) | 1.0% |

**Anti-Drift Bright Line (mandatory):** *A given ticker/setup is logged under exactly ONE playbook per trade.* If it satisfies a **mandatory VCP + RS ≥ 80 pivot breakout**, it is **SW-B** — log it there and use SW-B sizing. If it is a **pullback-to-MA reclaim** or a non-VCP base breakout with **RS 70–79**, it is **SW-A v3**. Do not let an SW-A v3 idea borrow SW-B's 1.0% tier, and do not double-count the same chart in both journals. When in doubt, the stricter book (SW-B) wins the classification only if *all* of its mandatory filters are met; otherwise it is SW-A v3.

> **Analyst recommendation:** Run them as complements — SW-B is your **breakout** book, SW-A v3 is your **pullback** book — under one shared portfolio-heat budget (3.0% total, 1.5% sector). If after 50 trades each their expectancies are statistically indistinguishable, **collapse them into one continuation playbook** rather than maintaining two. Do not keep two books alive out of attachment to the structure.

> **Consistency note:** SW-B currently treats sector strength *qualitatively* ("sector strong or improving"). The quantitative sector gate added here (top-third by RS vs SPY) is equally applicable to SW-B and arguably belongs there too. I left SW-B untouched for now since you scoped this to SW-A v3 — say the word and I'll backport the same gate to the SW-B docs so both continuation books measure sector strength identically.

---

## 11. Paper-to-Live Protocol

Consistent with the rest of the system:

- Apply a **25% performance haircut** to paper expectancy when projecting to live.
- Minimum **50 SW-A v3 paper trades** before live consideration (30 floor; 50+ preferred).
- **Live gate:** expectancy **≥ +0.20R** after haircut, with a max consecutive-loss streak tolerable at live size.
- **Phase the entry archetypes separately** for the first sample: paper-test **Archetype A (pullback)** and **Archetype B (base breakout)** as tagged sub-strategies so you can tell which one carries the edge. They may not be equally good on your tickers.
- Live micro-sizing: start at **25% of normal risk** (≈0.18% in place of 0.75% A+), 30–50 live trades, scale only if live expectancy holds post-haircut.
- **Each archetype earns live status independently.** A passing pullback book does not authorize live base-breakout trading, and vice versa.

---

## 12. Trade Ticket Additions (v3)

| Field | Entry |
| --- | --- |
| Playbook | SW-A v3 |
| Entry Archetype | A (Pullback-to-MA) / B (Base Breakout) |
| Trend gate confirmed | Price > rising 50 SMA? 50>200? (Yes/No) |
| Reference MA | 20 / 50 / 200 SMA touched & reclaimed |
| Touch count | 1st / 2nd / later touch of 50 SMA since advance began |
| RS percentile vs SPY | (must be ≥ 70) |
| Sector ETF & rank | e.g., XLK — rank __ of 11 (must be top-third for A+); RS line rising? |
| Volume signature | Pullback/base volume contracting? Reclaim/breakout bar ×avg? |
| Dilution check | No 424B5/S-3/S-1 in 60 days — confirmed (Yes/No) |
| Entry / Stop / Trade risk $/sh | |
| Account risk $ / Size | Per tier; size = risk$ ÷ trade risk |
| T1 / T2 / Trail rule | ≥2R to first resistance confirmed (Yes/No) |
| Confirmations passed | x / 6 |

---

## 13. Journal Fields (v3)

Date · Ticker · Archetype (A/B) · Setup grade (A+/A/B) · Regime (index trend + breadth) · Trend gate (50/200 state) · RS percentile · **Sector ETF + sector RS rank (1–11) at entry** · Touch count · Volume signature · Entry type (reclaim / pivot / retest) · Planned R · Realized R · **MAE / MFE (R units)** · Rule-adherence score (0/1 per rule) · Sector context · Mistake/Insight (one line).

> **Instrument the sector filter so you can test it.** Log the sector rank on *every* trade and, in the weekly review, split realized expectancy by sector tier (top / middle / bottom-third). If top-third does not out-expectancy the rest after a meaningful sample, the gate is only cutting trade count, not adding edge — and you drop it. That is the data-validation step this filter has not yet passed.

---

## 14. Scan Workflow (Top-Down Funnel)

This is the **order the scan runs in** — the same gates as §2–§6, applied top-down so you only ever evaluate setups *inside* strong groups. The §2 GO/NO-GO is the per-*candidate* 60-second check; this funnel is the *process* that surfaces those candidates. It is also the backtest/forward-test architecture (run modes below).

**Stage 0 — Market regime (weekly + daily).** SPY/QQQ above a rising 200-day; breadth not deteriorating. Risk-off → cut tiers or stand down. This gates the whole funnel; in a confirmed downtrend the lower stages do not run at full size.

**Stage 1 — Rank sectors (weekly).** Rank the 11 SPDR sector ETFs by RS vs **SPY** (blend 3- and 6-month). Keep the **top-third (≈ top 4) with a rising RS line**. Re-rank every weekend — top rank decays in ~21–47 days. This is the universe-narrowing step and the core of the top-down edge.

**Stage 2 — Strong stocks inside strong sectors (nightly).** *Only within the surviving sectors*, filter to: RS percentile ≥ 70 · price > rising 50 SMA (50 > 200 preferred) · within ~20% of the 52-wk high · not >30% extended above the 50 SMA · ADV ≥ 1M shares · no 424B5/S-3/S-1 in 60 days · no earnings in 3–5 sessions.

**Stage 3 — Setup detection (nightly).** On that shortlist only, look for the two archetypes: **(A)** pullback to a rising 20/50/200 SMA with a green reclaim bar on ≥1.5× volume, or **(B)** tight base with contracting volume, expanding on green days into a defined pivot.

**Stage 4 — Score & ticket (nightly).** Run the 4-of-6 confirmation stack (§6); grade A+/A/B (A+ requires a top-third sector); write the ticket with sizing and the ≥2R check (§5, §12).

**Cadence:** Stage 0 + Stage 1 = weekend review; Stages 2–4 = nightly EOD. Matches your existing operational routine.

### Two run modes — and why both matter for testing

| Mode | What it does | Use for |
| --- | --- | --- |
| **Funnel (sequential)** | Stage 1 → 2 → 3 narrowing exactly as above; you never see setups outside strong sectors | **Live + forward/paper testing** — the test must mirror live execution |
| **Parallel-tag (attribution)** | Run Stages 2–3 on the **full universe**, then *tag* each setup's sector tier (top/middle/bottom-third) | **Backtesting** — the only way to prove the sector gate adds expectancy rather than just cutting trade count |

> **Why both:** if you only ever run the funnel, the sector gate is unfalsifiable — you've conditioned away every trade that would have tested it. Parallel-tag runs the stock+setup logic *without* the sector filter, records which tier each trade would have fallen in, and lets you compare realized expectancy across tiers. If top-third doesn't beat middle/bottom by a margin that survives costs, **drop the gate.**

### Backtest integrity checklist (non-negotiable for a sector-first test)

- **Point-in-time sector membership** — use the GICS sector a stock had *on each historical date*, not today's. (The 2018 GICS Communication Services reshuffle moved GOOGL/META/NFLX — today's map injects look-ahead bias.)
- **Point-in-time ETF composition + survivorship** — include delisted/merged tickers; don't test on current membership only.
- **As-of ranks, no leakage** — sector ranks and RS computed only from data ≤ the decision date.
- **Report by regime** — break out 2018-Q4, 2020, 2022 separately; industry momentum whipsaws at regime turns and an aggregate number hides it.
- **A-priori thresholds** — the knobs (top-4, RS ≥ 70, 1.5× vol, 0.80×52-wk-high, 30% extension, 63/126-day lookbacks) come from the literature; sensitivity-check coarsely, do **not** fine-optimize on the test set. Walk-forward / out-of-sample is the real verdict.
- **Mechanized-proxy caveat** — the backtest tests a strict proxy of discretionary rules ("orderly pullback," "tight base"); the forward/paper test validates the actual read. Treat divergence between them as data, not noise.
- **Costs** — keep your existing $0.02–0.05 slippage and 25% paper-to-live haircut.

---

## 15. Screener Logic (staged, top-down — funnel + attribution)

Refactored to mirror the funnel: rank sectors → stocks in strong sectors → detect setups, with a parallel-tag entry point for backtest attribution. Pseudocode-level; wire to your data source (Schwab/TOS export or your provider). Thresholds are a-priori from §14 — sensitivity-check, don't optimize.

```python
import pandas as pd

SPDR_SECTORS = ["XLK","XLF","XLE","XLV","XLY","XLP","XLI","XLB","XLU","XLRE","XLC"]

# ---------- Stage 1: rank the 11 SPDR sectors by RS vs SPY (weekly, as-of) ----------
def rank_sectors(sector_px: pd.DataFrame, spy: pd.Series, asof) -> pd.DataFrame:
    """
    sector_px: daily closes for the 11 sector ETFs (cols = tickers), indexed by date.
    spy:       daily closes for SPY, same index.
    asof:      date to rank as of — uses ONLY data <= asof (no leakage).
    """
    px, bench = sector_px.loc[:asof], spy.loc[:asof]
    def rs_ratio(lb):                       # ratio of sector return to SPY return
        return (px.iloc[-1] / px.iloc[-lb]) / (bench.iloc[-1] / bench.iloc[-lb])
    blend = 0.5 * rs_ratio(63) + 0.5 * rs_ratio(126)        # ~3m and ~6m
    rs_line_now   = px.iloc[-1]  / bench.iloc[-1]
    rs_line_prior = px.iloc[-21] / bench.iloc[-21]          # ~1 month ago
    out = pd.DataFrame({"rs_blend": blend, "rs_rising": rs_line_now > rs_line_prior})
    out["sector_rank"] = out["rs_blend"].rank(ascending=False).astype(int)
    return out.sort_values("sector_rank")

def strong_sectors(ranked: pd.DataFrame, top_n: int = 4) -> list:
    """Top-third (~4 of 11) sectors WITH a rising RS line."""
    return ranked[(ranked["sector_rank"] <= top_n) & ranked["rs_rising"]].index.tolist()

# ---------- Stage 2: strong stocks within strong sectors (nightly, as-of) ----------
def _stock_gates(g: pd.DataFrame) -> pd.Series:
    """Stock-level gates WITHOUT the sector filter (reused by funnel + attribution)."""
    return (
        (g["close"] > g["sma50"]) & (g["sma50_slope"] > 0) & (g["sma50"] > g["sma200"]) &
        (g["rs_pct"] >= 70) &
        (g["close"] >= 0.80 * g["high_252"]) &                  # within ~20% of 52-wk high
        ((g["close"] / g["sma50"] - 1) <= 0.30) &               # not over-extended
        (g["adv"] >= 1_000_000)                                 # liquidity floor
    )

def stocks_in_strong_sectors(df: pd.DataFrame, strong: list) -> pd.DataFrame:
    """df: per-ticker as-of row incl. sector, close, sma20/50/200, sma50_slope,
       rs_pct, high_252, adv, plus OHLCV + vol20 + pivot for Stage 3."""
    g = df[df["sector"].isin(strong)].copy()
    return g[_stock_gates(g)]

# ---------- Stage 3: setup detection on the shortlist (nightly) ----------
def detect_setups(shortlist: pd.DataFrame) -> pd.DataFrame:
    s = shortlist.copy()
    s["archetype_A"] = (                       # pullback-to-MA reclaim
        (s["low"] <= s["sma50"] * 1.01) &
        (s["close"] > s["open"]) & (s["close"] > s["sma50"]) &
        (s["volume"] >= 1.5 * s["vol20"])
    )
    s["archetype_B"] = (                       # base breakout on volume
        (s["close"] > s["pivot"]) & (s["volume"] >= 1.5 * s["vol20"])
    )
    return s[s["archetype_A"] | s["archetype_B"]]

# ---------- LIVE FUNNEL: Stage 1 -> 2 -> 3 (forward/paper testing) ----------
def funnel(df_today: pd.DataFrame, ranked_sectors: pd.DataFrame) -> pd.DataFrame:
    strong = strong_sectors(ranked_sectors)
    return detect_setups(stocks_in_strong_sectors(df_today, strong))

# ---------- BACKTEST ATTRIBUTION: run stock+setup on FULL universe, TAG tier ----------
def parallel_tag(df_asof: pd.DataFrame, ranked_sectors: pd.DataFrame) -> pd.DataFrame:
    """Do NOT pre-filter by sector. Tag each setup's sector tier so you can compare
    realized expectancy across tiers and prove (or disprove) the sector gate."""
    cand = detect_setups(df_asof[_stock_gates(df_asof)].copy())
    cand["sector_rank"] = cand["sector"].map(ranked_sectors["sector_rank"].to_dict())
    cand["sector_tier"] = pd.cut(cand["sector_rank"], bins=[0, 4, 8, 11],
                                 labels=["top", "middle", "bottom"])
    return cand   # later: groupby("sector_tier") and compare expectancy after costs
```

> RSI(14) and MACD are intentionally **not** gating conditions here — they enter only as confirmation in the manual review, consistent with §3. Dilution (424B5/S-3/S-1) and the earnings-window check are handled in a separate fundamental/event pass before a ticket is written.

---

## 16. References (selected)

- George, T.J. & Hwang, C.-Y. (2004). *The 52-Week High and Momentum Investing.* **Journal of Finance**, 59(5), 2145–2176. (Nearness to 52-wk high dominates past-return momentum; forecasted returns do not reverse.)
- International replication: *The 52-week high momentum strategy in international stock markets* (ScienceDirect) — effect robust in 18 of 20 markets tested.
- Weinstein, S. (1988). *Secrets for Profiting in Bull and Bear Markets* (Stage Analysis; Stage-2 entries, 30-week MA, volume confirmation, RS).
- Minervini, M. *Trade Like a Stock Market Wizard* / *Think and Trade Like a Champion* (SEPA, VCP, Trend Template, pivot entries, stop below final contraction).
- Moskowitz, T.J. & Grinblatt, M. (1999). *Do Industries Explain Momentum?* **Journal of Finance**, 54(4), 1249–1290. (Industry momentum accounts for much of individual-stock momentum; controlling for it weakens individual momentum to insignificance.)
- O'Neil, W. — *How to Make Money in Stocks* / IBD (CAN SLIM "L"; ~half of a stock's move tied to its industry group; trade leaders in top industry groups).
- Bulkowski, T. — *Industry Relative Strength* study (top-ranked industry stocks materially outperformed the S&P; top rank persists ~21–47 days).
- TraderLion — Stage Analysis & VCP explainers (breakout volume 2–3× average; pivot mechanics).
- T. Livingston — *Swing Into It: Trading Pullbacks to the 50-Day Moving Average* (first-touch reliability; "never buy a down day"; RS reset on pullbacks).
- Bulls on Wall Street — pullback ("Bone Zone" 9/20 EMA) framework; green-zone vs red-zone trend filter; wait-for-the-50-SMA when extended.
- IBD CAN SLIM — breakout requires ~40–50%+ above-average volume; institutional moves 1.5–2×.
- Barchart / J. Rowland, CMT — *Don't fall for false buy signals* (first MACD crossover is often a trap; demand structure + volume + momentum confluence).

---

*Internal Trading SOP — SW-A v3. Educational use only; not investment advice. Use strict risk sizing. Each playbook earns live status independently and only on its own post-haircut expectancy.*