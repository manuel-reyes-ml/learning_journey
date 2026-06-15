# SW-B v3 — TREND CONTINUATION (VCP)

*Continuation-from-Strength via Volatility Contraction Pattern → Pivot Breakout — Swing Trading — Stocks*

*The elite, narrowest continuation book. Buy the highest-conviction setup: a textbook VCP base in an RS-leader (≥ 80) inside a top-third sector, entered on the pivot breakout with volume expansion. Built from Minervini SEPA/VCP, O'Neil base/breakout practice, Weinstein Stage Analysis, and the 52-week-high / industry-momentum literature.*

---

> **READ FIRST — WHAT THIS DOCUMENT IS AND IS NOT**
>
> SW-B is the **breakout** book; SW-A v3 is the **pullback** book. They are both continuation-from-strength, and the single largest risk in running both is **strategy drift** — the two collapsing into one fuzzy playbook graded inconsistently. §10 defines the bright lines; read it before trading either.
>
> The second risk is **definitional erosion.** SW-B's entire edge is the integrity of the VCP: a mandatory sequence of progressively shallower contractions on declining volume. The moment you relax that into "any tight base" because you want more trades, SW-B stops being SW-B and you are just buying breakouts. The VCP is mechanized deterministically in §3 and §15 precisely so it cannot quietly soften. SW-B is supposed to produce **fewer, higher-quality** setups than SW-A v3 — that is the design, not a defect.
>
> **STATUS:** research-grounded, NOT yet data-validated on your tickers. Paper-test before live (§11). The VCP detector in §15 is a **strict mechanical proxy** of a discretionary read — treat divergence between it and your eye as data, not noise.

---

## Changelog — SW-B v2 → SW-B v3

SW-B's core (mandatory VCP + RS ≥ 80) is unchanged. v3 brings it into structural parity with SW-A v3 and the institutional-footprint work.

| Area | SW-B v2 | SW-B v3 |
| --- | --- | --- |
| Sector / group strength | Qualitative ("sector strong or improving") | **Quantitative gate (backported from SW-A v3):** stock's SPDR sector ETF top-third by RS vs SPY, RS line rising; **bottom-third = NO TRADE** |
| VCP structure | Mandatory (2+ shallower contractions, lower volume) | Mandatory — **now defined deterministically** (§3, §15) so it is backtestable and cannot erode |
| Footprint metrics | — | **Instrumented (observe-mode):** distribution-day counts, U/D volume ratio, VDU — defined in §9A. VDU is now an explicit, numeric part of the VCP. |
| RS floor | ≥ 80 | ≥ 80 (unchanged — the SW-B/SW-A v3 differentiator) |
| Risk tier A+ | 1.0% | 1.0% (unchanged — SW-B is the elite book; not capped like SW-A v3's 0.75%) |

> Canonical references: this document (SW-B mechanics) and the Master Plan v3 (system-level rules, portfolio heat, footprint section). Quick reference: `SWB_Quick_Reference_v3.md`.

---

## 1. Thesis and Evidence Base

SW-B trades the single highest-conviction continuation pattern: the **Volatility Contraction Pattern**, a base of progressively shallower pullbacks on declining volume, resolved by a **pivot breakout on expanding volume**, in a stock that is already a relative-strength leader inside a leading sector. The narrower filter is the point — you accept far fewer setups in exchange for the cleanest institutional-accumulation signature available on a price chart.

- **Minervini SEPA / VCP.** Inside a Stage-2 uptrend, the cleanest base is a series of contractions, each shallower than the last (e.g., 25% → 12% → 6%), each on **lower volume**, tightening toward a **pivot**. The contraction sequence *is* the visible footprint of supply being absorbed by institutions — sellers exhaust, float tightens, and the breakout resolves the coiled energy. Entry is the **pivot breakout on volume expansion**; the stop sits just below the final contraction. His Trend Template requires high RS rank and price above key moving averages.
- **O'Neil / CAN SLIM.** Proper bases (cup-with-handle, flat base, double-bottom) breaking out on volume **40–50%+ above average** (institutional 1.5–2×+) from a sound structure, in leaders from the top industry groups. The "L" (Leader, not Laggard) and the industry-group emphasis map directly onto the RS ≥ 80 and sector gates here.
- **Weinstein Stage Analysis.** Buy only **Stage 2** (price above a rising long-term MA with volume and RS confirmation). The highest-quality entries are the Stage-2 breakout and its retest. SW-B's pivot breakout is a Stage-2 breakout from a tight base.
- **Darvas box.** Tight consolidations ("boxes") breaking to new highs on volume in strong markets — an early, independent confirmation of the breakout-from-tightness principle.
- **52-week-high momentum (George & Hwang, 2004, *J. Finance*).** Nearness to the 52-week high forecasts forward returns better than past returns and does not reverse long-term. SW-B leaders are at/near highs by construction — the empirical tailwind.
- **Industry / sector momentum (Moskowitz & Grinblatt, 1999, *J. Finance*).** Industry momentum explains much of individual-stock momentum; buying leaders from winning groups is itself highly profitable. This is the basis of the sector gate (top-third SPDR by RS vs SPY), shared with SW-A v3.

The common thread: **trend first, then a structurally sound, volume-contracted base, then the breakout — momentum indicators confirm, never trigger.** SW-B is the strictest expression of that order. Operationally the gates run as a top-down funnel — regime → sector → stock → VCP → breakout — defined in §14 with a staged screener in §15.

---

## 2. GO / NO-GO (60s)

- **Regime (market):** SPY/QQQ above rising 200-day; breadth not collapsing; **index distribution-day count** within tolerance (§9A). Index downtrend / rising distribution days → size down or stand down.
- **Trend (stock) — HARD GATE:** price above a **rising 50 SMA**; 50 SMA above 200 SMA preferred. Higher highs / higher lows intact.
- **Relative strength:** RS percentile vs SPY **≥ 80** and RS line flat-to-rising (bonus: RS line at a new high *ahead* of price).
- **Sector strength (gate):** stock's sector ETF **top-third by RS vs SPY** (≈ top 4 of 11 SPDR sectors), sector RS line rising. Bottom-third / falling sector RS = stand down.
- **VCP present (mandatory):** ≥ 2 contractions, each shallower than the prior, each on lower volume, final contraction tight (≤ ~10%) and within 5–10% of the pivot, with volume dry-up. *No valid VCP = not an SW-B trade.*
- **Trigger:** a defined pivot with room to the next resistance; **≥ 2R** planned.
- **Event check:** no unplanned earnings/binary event inside 3–5 sessions.
- **Dilution check:** no SEC 424B5 / S-3 / S-1 in last 60 days (hard disqualifier).

---

## 3. Setup Filters (EOD)

**Trend (mandatory)**

- Daily: price > rising 50 SMA; 50 SMA > 200 SMA preferred (Stage 2). Weekly higher highs / higher lows intact.

**Relative Strength (mandatory — the SW-B differentiator)**

- RS percentile vs SPY **≥ 80** at entry (vs SW-A v3's ≥ 70 — see §10). RS line not making new lows during the base; bonus tell if the RS line prints a new high while price is still based.

**Sector / Group Strength (mandatory — quantitative, identical to SW-A v3)**

- Map the stock to its SPDR sector ETF (XLK, XLF, XLE, XLV, XLY, XLP, XLI, XLB, XLU, XLRE, XLC).
- Rank all 11 by RS vs **SPY** (blend 3- and 6-month; re-rank **weekly** — top rank decays in ~21–47 days).
- Top-third (≈ top 4) + rising RS → A+ eligible; middle-third → A/B reduced size; **bottom-third or falling sector RS → NO TRADE.** Measure independently of stock RS. Rank vs SPY (not QQQ).

**VCP Structure (mandatory — deterministic definition)**

The VCP is the heart of SW-B and is defined numerically so it is backtestable and cannot soften over time. Parameters (a-priori; §15 has the detector and the catalogue):

| Property | Rule (default) |
| --- | --- |
| Prior advance | Base follows a Stage-2 advance (price up materially off the pre-base low; above rising 50/200 SMA) |
| Base length | ~15–65 sessions (≈ 3–13 weeks) |
| Contraction count | **2–6** distinct peak-to-trough contractions within the base |
| Each shallower | depth(Cᵢ₊₁) ≤ depth(Cᵢ) — strictly contracting (e.g., 25% → 12% → 6%) |
| Each quieter | avg volume(Cᵢ₊₁) ≤ avg volume(Cᵢ) — volume declines leg over leg |
| Final contraction | tight (≤ ~10%, ideally ≤ 5–6%) and within 5–10% of the pivot |
| Volume Dry-Up (VDU) | ≥ 1 session in the final leg with volume ≤ 50% of the 50-day average (§9A) |
| Pivot | highest high of the base (buy reference) |

> A single pullback, or two contractions of similar depth, or a base where volume does **not** decline leg over leg, is **not a VCP** — it is at best an SW-A v3 base breakout. Do not force it.

**Confirmation reads (confirmation only — never the trigger)**

- RSI(14) typically 40–60 during the base (reset, not extended). MACD stabilizing / histogram turning up. ADX > 20 supports trend quality. A single MACD cross is not an entry (first crossovers frequently trap).

---

## 4. Entry Rules

SW-B's defining trigger is the **pivot breakout**; the other two are lower-risk fills of the *same* VCP setup. Classification into SW-B (vs SW-A v3) is driven by the mandatory VCP + RS ≥ 80, not by which of these fills you take (§10).

- **Trigger A — Pivot Breakout (defining):** a daily **close above the pivot** on volume **≥ 1.5× (min) to 2× the 20-day average** (the higher, the better — institutional breakouts often run 2–4×).
- **Trigger B — Pullback-to-pivot / MA after the VCP completes (lower-risk fill):** after a valid breakout, a controlled pull back to the pivot or 20/50 EMA that holds, entered on a bullish reclaim candle. Tighter stop, but only valid once the VCP is complete.
- **Trigger C — Retest (tightest risk):** breakout, then buy the retest of the pivot holding as support (Weinstein's second buy point).

**Universal entry rules**

- **Mandatory floors:** trend gate, RS ≥ 80, sector top-third, valid VCP, and breakout volume — all required. Any miss = NO TRADE. (See the confirmation table in §6.)
- **No chase:** if price is already > 3–5% beyond the pivot without you, wait for a retest or skip. Chasing an extended breakout is an explicit Execution Error in review.
- **Acceptance rule:** a breakout that closes back inside the base is a warning; repeated failed pivots = no trade / exit.

---

## 5. Risk, Stops, Sizing

- **Risk tiers:** A+ **1.0%** (A+ additionally requires a top-third sector), A **0.75%**, B **0.50%** (or skip). SW-B's A+ is **not** capped at 0.75% the way SW-A v3's is — SW-B is the elite, narrowest book and earns the full tier. *Discipline note:* the 1.0% is still earned only after SW-B clears its own paper gate (§11); it is not a license before validation.
- **Position size** = AccountRisk$ ÷ (Entry − Stop).
- **Stop placement (structure-first):** below the **final VCP contraction low** (Minervini-style), or below the pivot with a small ATR buffer if the final contraction is unusually deep. The tight final contraction is what makes SW-B's stops small and its R:R favorable — protect that by not entering loose bases.
- **Never widen a stop.** If structure forces a wider stop, **reduce share count** to hold R constant.
- **Portfolio heat:** max total open risk 3.0%; max sector risk 1.5%.

> **Worked example ($50,000, 1.0% A+ tier).**
> AccountRisk$ = 50,000 × 0.010 = **$500**.
> Pivot breakout entry $60.00; final-contraction low $57.80 → stop $57.60 → trade risk = **$2.40/share**.
> Shares = 500 ÷ 2.40 = **208** (round down to 205).
> First target ≥ 2R → +$4.80 → **$64.80**. If the nearest real resistance is below $64.80, the RR fails the ≥ 2R gate → **NO TRADE** or wait for a tighter entry. The tight VCP stop is precisely what lets a leader clear ≥ 2R cleanly.

---

## 6. Confirmation Stack (mandatory floors + confirmation)

SW-B's filters are stricter than SW-A v3's: five are **mandatory floors** (not a 4-of-6 vote), plus confirmation reads.

| # | Item | Type | Pass criteria |
| --- | --- | --- | --- |
| 1 | Trend / Level | **Mandatory** | Price > rising 50 SMA; entry at the defined pivot. |
| 2 | Relative strength (stock) | **Mandatory** | RS percentile ≥ 80 vs SPY; RS line flat-to-rising. |
| 3 | Sector / group | **Mandatory** | Sector ETF top-third by RS vs SPY, RS line rising. Bottom-third = NO TRADE. |
| 4 | VCP structure | **Mandatory** | Valid VCP per §3 (contractions shrinking, volume declining, tight final leg + VDU). |
| 5 | Breakout volume | **Mandatory** | Pivot-break bar ≥ 1.5×–2× 20-day average. Reject 3–5× climax-into-resistance. |
| 6 | Momentum | Confirmation | RSI reset/turning up; MACD histogram improving. Never sufficient alone. |

**Scoring:** all five mandatory floors must pass — there is no "4 of 6" relaxation for SW-B. Item 6 is supportive only. Failing any of 1–5 is an automatic NO TRADE.

---

## 7. Targets and Management

- **T1:** next resistance / measured-move zone (base depth projected up from the pivot).
- **T2:** 2R–4R extension as the trend resumes.
- **Partials:** default no partial before +1.5R unless price runs straight into resistance; consider 25–50% partial at +2R into resistance or an earnings window.
- **Trail:** by higher lows (preferred) or the 20 EMA once resumption is clean. Trail under 5/10-day structure early, widen to 20 EMA later.
- **Add-ons:** only after +1R **and** a new tight continuation forms. Never pyramid into extension.
- **Time stop:** if the pivot fails to make favorable progress within 5–10 sessions (momentum fades), exit and redeploy.

---

## 8. Exits and Failure Signals

- **Hard exit:** stop hit, or trend structure breaks (lower low / decisive close below the reference MA on expanding volume).
- **Breakout failure:** breakout closes back inside the base with distribution; repeated failed pivots.
- **Distribution warning (footprint, observe-mode):** a cluster of stock-level distribution days (down on higher volume) while you hold, or the U/D volume ratio rolling below 1.0, is a caution flag even if price still holds — tighten or reduce. Instrumented, not a hard exit until validated (§9A).
- **Circuit breakers (unchanged):** 3 losses in a row → pause new entries 3 sessions; rule violation → stop new entries for the week; −3R in a week → stop opening positions until next week.

---

## 9. Hard Do-Not-Trade Conditions

- No valid VCP (single pullback, equal-depth contractions, or volume not declining leg over leg). This is the most common SW-B error — wanting the trade and softening the pattern.
- Price below a falling 50 SMA, or index in a confirmed downtrend with deteriorating breadth → stand down or quarter-size.
- RS percentile < 80 or RS line making new lows.
- Sector in the bottom-third by RS vs SPY, or sector RS making new lows.
- Climactic volume (3–5×+ average) into overhead resistance on the breakout bar — exhaustion, not continuation.
- Active dilution (424B5 / S-3 / S-1 in last 60 days); earnings/binary event inside 3–5 sessions.
- Chasing: price already extended > 3–5% beyond the pivot.

---

## 9A. Institutional Footprint — Accumulation/Distribution Metrics (Instrumented)

> **Shared system spec.** The canonical copy lives in the Master Plan footprint section and SW-A v3 §9A; it is reproduced here for self-containment and must be changed in lockstep across all three. **Status: research-grounded, observe-mode — computed and logged, NOT gating trades** until parallel-tag validation (§14) proves added expectancy after costs. Premise (`Tracking_Institutional_Footprints_Reference.md`): institutions cannot accumulate or distribute size without leaving residue. SW-B's existing gates read the accumulation (buy) side hard — indeed the **VCP itself is the accumulation footprint made structural** (tightening on declining volume = supply absorbed). These metrics add the orthogonal **distribution (sell) side.**

> **VDU is not a bonus for SW-B — it is part of the pattern.** Where SW-A v3 treats volume dry-up as an optional quality mark, a valid SW-B VCP **requires** declining leg-over-leg volume and a VDU in the final contraction. The `vdu_*` parameters below are therefore load-bearing in §3/§15, not observe-only.

### 9A.1 Feature definitions (deterministic; data ≤ decision date)

- **Distribution day (index or stock):** close **down ≥ `dist_down_pct`** vs prior close **on higher volume than the prior session**; count in a rolling `dist_window`. Index cluster = institutional-selling / topping tell.
- **U/D volume ratio:** over `ud_lookback` sessions, Σ(up-day volume) ÷ Σ(down-day volume); ≥ 1 healthy, ≥ `ud_strong` strong, **< 1 = net distribution.**
- **Volume Dry-Up (VDU):** a session with volume ≤ `vdu_pct` × `vdu_avg_window`-day average (narrowest range preferred). **Required** in the SW-B final contraction.
- **RS-line-leads-price:** RS line vs SPY prints a new `rs_newhigh_lookback`-day high while price is still based.
- **OBV (optional, correlated):** rising confirms; failure to confirm a new price high warns. Correlated with U/D ratio — pick one primary; don't stack as gates.

### 9A.2 Parameter catalogue (shared system defaults; observe-mode unless noted)

| Parameter | Default | Type | Mode (SW-B) | Notes |
| --- | --- | --- | --- | --- |
| `dist_down_pct` | 0.20% | float | regime input / observe (stock) | Stock test 0.2–0.5% |
| `dist_window` | 25 sessions | int | — | Rolling count window |
| `index_dist_cluster_riskoff` | 5 | int | observe → regime posture | Test 4–6 |
| `stock_dist_cluster_warn` | 4 | int | observe (exit flag) | Cluster while holding = caution |
| `ud_lookback` | 50 sessions | int | — | — |
| `ud_strong` | 1.75 | float | observe | Range 1.5–2.0 |
| `vdu_pct` | 0.50 | float | **gate (VCP)** | Load-bearing: required in final contraction |
| `vdu_avg_window` | 50 sessions | int | — | — |
| `rs_newhigh_lookback` | 63 sessions | int | observe (bonus) | — |

Regime-posture map (observe-mode — log the multiplier it would apply, validate before activating): index distribution days **0–3 → 1.0×** · **4–5 → 0.5×** · **6+ → stand down.**

### 9A.3 Wiring

| Metric | Module | Default action |
| --- | --- | --- |
| Index distribution-day count | Stage 0 regime (§2/§14) | Observe → recommended first promotion (size posture) |
| Stock distribution-day cluster | Exits (§8) | Observe → caution flag |
| U/D volume ratio | Confirmation health (§6) + journal | Observe |
| VDU | **VCP validity (§3/§15) + journal** | **Gate (already mandatory in the VCP)** |
| RS-line-leads-price | RS confirmation (§3/§6) + journal | Observe (bonus) |

### 9A.4 Validation path

Run each observe-mode metric through parallel-tag attribution (§14); promote to a gate/posture only if its favorable bucket out-expectancies the rest after costs and the 25% haircut, surviving walk-forward. Recommended first promotion: index distribution-day count (changes size, not selection → least overfit risk).

---

## 10. Relationship to SW-A v3 and the Anti-Drift Rule

Both are continuation-from-strength. Left undefined, you grade them inconsistently and your journal is useless. The bright lines (identical table to the SW-A v3 deep spec):

| Dimension | **SW-B (Trend Continuation — VCP)** | **SW-A v3 (Trend Pullback / Base Breakout)** |
| --- | --- | --- |
| Primary entry mechanic | **Buy the breakout** — pivot break out of a textbook VCP | **Buy the dip** — pullback to rising MA support, reclaim on green bar |
| Base structure required | **Mandatory VCP**: 2+ contractions, each shallower, each on lower volume | Orderly pullback **or** clean base (VCP *nice-to-have*, not required) |
| RS percentile floor | **≥ 80** | **≥ 70** |
| Conviction tier | Narrowest, "elite" continuation | Broader, "good" continuation |
| A+ risk cap | 1.0% | 0.75% (capped until proven) |

**Anti-Drift Bright Line (mandatory):** *A given ticker/setup is logged under exactly ONE playbook per trade.* If it satisfies a **mandatory VCP + RS ≥ 80 pivot breakout**, it is **SW-B** — log it here, use SW-B sizing. If it is a **pullback-to-MA reclaim** or a non-VCP base breakout with **RS 70–79**, it is **SW-A v3**. SW-B wins the classification only if **all** its mandatory floors (§6) are met; otherwise it is SW-A v3. Do not let an SW-B idea that misses a floor "round up," and do not double-count the same chart in both journals.

> **Collapse rule:** run them as complements under one shared heat budget (3.0% total, 1.5% sector). If after 50 trades each their expectancies are statistically indistinguishable, **collapse into one continuation playbook** rather than keeping two alive out of attachment to the structure.

---

## 11. Paper-to-Live Protocol

- Apply a **25% performance haircut** to paper expectancy when projecting to live.
- Minimum **50 SW-B paper trades** before live (30 floor; 50+ preferred).
- **Live gate:** expectancy **≥ +0.20R** after haircut, with a max consecutive-loss streak tolerable at live size.
- **SW-B is traded alone for 6 weeks first** (it is the higher-base-rate book); SW-A v3 is added only after SW-B is producing a reviewable journal.
- Live micro-sizing: start at **25% of normal risk** (≈ 0.25% in place of 1.0% A+), 30–50 live trades, scale only if live expectancy holds post-haircut.
- Each playbook earns live status independently — SW-A v3 clearing paper does not authorize SW-B live, and vice versa.

---

## 12. Trade Ticket Additions (v3)

| Field | Entry |
| --- | --- |
| Playbook | SW-B |
| Entry trigger | Pivot breakout / pullback-to-pivot / retest |
| Trend gate confirmed | Price > rising 50 SMA? 50 > 200? (Yes/No) |
| RS percentile vs SPY | (must be ≥ 80) |
| Sector ETF & rank | e.g., XLK — rank __ of 11 (must be top-third for A+); RS line rising? |
| VCP structure | # contractions; depth sequence (e.g., 22%→11%→5%); volume declining? (Yes/No) |
| Final contraction / pivot | Final-leg depth %; pivot price; within 5–10% of pivot? VDU present? |
| Breakout volume | Pivot-break bar ×20-day avg (≥1.5×) |
| Footprint metrics (§9A) | U/D vol ratio (~50d); stock distribution-day count (~25d); index distribution-day count |
| Dilution check | No 424B5/S-3/S-1 in 60 days — confirmed (Yes/No) |
| Entry / Stop / Trade risk $/sh | Stop below final contraction low |
| Account risk $ / Size | Per tier; size = risk$ ÷ trade risk |
| T1 / T2 / Trail rule | ≥2R to first resistance confirmed (Yes/No) |
| Mandatory floors passed | 5 / 5 (all required) |

---

## 13. Journal Fields (v3)

Date · Ticker · Entry trigger (breakout/pullback/retest) · Setup grade (A+/A/B) · Regime (index trend + breadth + **index distribution-day count**) · Trend gate (50/200 state) · RS percentile (≥80) · **Sector ETF + sector RS rank (1–11)** · **VCP description (contraction count, depth sequence, volume trend, final-leg %, VDU Y/N)** · Breakout volume ×avg · Entry type · **Footprint (§9A): U/D vol ratio (~50d) · stock distribution-day count (~25d)** · Planned R · Realized R · **MAE / MFE (R units)** · Rule-adherence score (0/1 per floor) · Mistake/Insight (one line).

> **Instrument every soft filter so you can test it.** Log sector rank and each footprint metric on *every* trade; in the weekly review split realized expectancy by sector tier and by footprint-metric bucket. A filter that does not out-expectancy its alternative after costs is cutting trade count, not adding edge — drop it. Also log **VCP contraction count and final-leg depth**, so you can test whether tighter/deeper finals or more/fewer contractions carry the edge.

---

## 14. Scan Workflow (Top-Down Funnel)

Same gate order as §2–§6, applied top-down so you only evaluate VCPs *inside* strong groups. The §2 GO/NO-GO is the per-candidate 60-second check; this funnel is the process that surfaces candidates and is also the test architecture.

**Stage 0 — Market regime (weekly + daily).** SPY/QQQ above a rising 200-day; breadth not deteriorating; index distribution-day count within tolerance (§9A). Risk-off (downtrend or rising distribution days) → cut tiers or stand down.

**Stage 1 — Rank sectors (weekly).** Rank the 11 SPDR ETFs by RS vs SPY (blend 3- and 6-month). Keep the **top-third (≈ top 4) with a rising RS line**. Re-rank every weekend (top rank decays ~21–47 days).

**Stage 2 — Strong leaders inside strong sectors (nightly).** *Only within surviving sectors:* RS percentile **≥ 80** · price > rising 50 SMA (50 > 200 preferred) · near 52-wk high · ADV ≥ 1M · no 424B5/S-3/S-1 in 60 days · no earnings in 3–5 sessions.

**Stage 3 — VCP detection (nightly).** On that shortlist, run the deterministic VCP detector (§15): valid contraction count, monotonically shrinking depths, declining leg volume, tight final contraction + VDU, defined pivot.

**Stage 4 — Breakout trigger, score & ticket (nightly/intraday).** Pivot break on ≥1.5×–2× volume; confirm all five mandatory floors (§6); grade (A+ requires top-third sector); write the ticket with sizing and the ≥2R check.

**Cadence:** Stage 0 + 1 = weekend; Stages 2–3 = nightly EOD; Stage 4 trigger can fire intraday on the breakout.

### Two run modes — and why both matter

| Mode | What it does | Use for |
| --- | --- | --- |
| **Funnel (sequential)** | Stage 1 → 2 → 3 → 4 narrowing; you never see VCPs outside strong sectors | **Live + forward/paper testing** (mirror live execution) |
| **Parallel-tag (attribution)** | Run Stages 2–3 on the **full universe**, tag each VCP's sector tier + footprint buckets | **Backtesting** — the only way to prove the sector gate / footprint metrics add expectancy rather than cut count |

### Backtest integrity checklist (non-negotiable)

- **Point-in-time sector membership** (the 2018 GICS reshuffle moved GOOGL/META/NFLX — today's map is look-ahead).
- **Point-in-time ETF composition + survivorship** (include delisted/merged tickers).
- **As-of ranks, no leakage** — sector ranks, RS, and VCP detection use only data ≤ the decision date.
- **Report by regime** — break out 2018-Q4, 2020, 2022 separately; momentum whipsaws at regime turns.
- **A-priori thresholds** — VCP knobs (contraction count, depth-decline, volume-decline, final-leg tightness, VDU, breakout-volume multiple, ZigZag sensitivity) come from the literature; coarse sensitivity-check only, do **not** fine-optimize on the test set. Walk-forward / out-of-sample is the verdict.
- **Mechanized-proxy caveat (acute for VCP)** — the detector approximates a discretionary read. Expect false positives (mechanical "VCP" your eye rejects) and false negatives (clean VCPs the detector misses). The forward/paper test validates the real pattern; treat divergence as data.
- **Costs** — keep $0.02–0.05 slippage and the 25% paper-to-live haircut.

---

## 15. Screener Logic (staged, top-down — funnel + attribution)

Stages 0–2 and the sector ranking are shared with SW-A v3 (`SWA_v3_Trend_Pullback_Base_Breakout.md` §15 — `rank_sectors`, `strong_sectors`, `_stock_gates` with `rs_pct >= 80` for SW-B). The SW-B-specific logic is the **deterministic VCP detector** below. Pseudocode; thresholds are a-priori (§3) — sensitivity-check, do not optimize.

```python
import pandas as pd

# ----- VCP parameter catalogue (a-priori; lock-and-test) -----
VCP_P = dict(
    zigzag_pct=0.05,          # swing-reversal threshold (test 0.03-0.08)
    min_contractions=2, max_contractions=6,
    depth_decline_tol=0.0,    # 0.0 = strictly shallower; relax to allow small tolerance
    vol_decline_tol=0.0,      # each leg quieter than the last
    final_contraction_max=0.10,   # final leg <= 10% (ideally <= 0.06)
    vdu_pct=0.50, vdu_avg_window=50, final_leg_len=10,
    breakout_vol_mult=1.5,    # pivot-break volume >= 1.5x (2x+ preferred)
    pivot_buffer=0.002,       # small buffer above pivot to filter noise
    base_min_len=15, base_max_len=65,
)

# ----- Swing detection (ZigZag-style) -----
def swings(close, pct):
    piv, trend = [], 0
    hi = lo = close.iloc[0]; hi_i = lo_i = 0
    for i, px in enumerate(close):
        if px > hi: hi, hi_i = px, i
        if px < lo: lo, lo_i = px, i
        if trend >= 0 and px <= hi * (1 - pct):
            piv.append((hi_i, hi, "H")); trend, lo, lo_i = -1, px, i
        elif trend <= 0 and px >= lo * (1 + pct):
            piv.append((lo_i, lo, "L")); trend, hi, hi_i = 1, px, i
    return piv

# ----- Deterministic VCP detection on a candidate base window -----
def detect_vcp(base: pd.DataFrame, p=VCP_P) -> dict:
    """base: daily OHLCV (ascending) for the candidate base. Returns validity + features."""
    if not (p["base_min_len"] <= len(base) <= p["base_max_len"]):
        return {"valid": False, "reason": "base_length"}
    sw = swings(base["close"], p["zigzag_pct"])
    contr = []
    for a, b in zip(sw, sw[1:]):                 # high -> following low = one contraction
        if a[2] == "H" and b[2] == "L":
            depth = (a[1] - b[1]) / a[1]
            seg_vol = base["volume"].iloc[a[0]:b[0] + 1].mean()
            contr.append((depth, seg_vol))
    n = len(contr)
    if not (p["min_contractions"] <= n <= p["max_contractions"]):
        return {"valid": False, "reason": "contraction_count", "n": n}
    depths = [c[0] for c in contr]; vols = [c[1] for c in contr]
    shrinking = all(depths[i+1] <= depths[i] * (1 - p["depth_decline_tol"]) for i in range(n-1))
    quieter   = all(vols[i+1]   <= vols[i]   * (1 - p["vol_decline_tol"])   for i in range(n-1))
    tight_final = depths[-1] <= p["final_contraction_max"]
    avg50 = base["volume"].rolling(p["vdu_avg_window"]).mean().iloc[-1]
    vdu = bool((base["volume"].tail(p["final_leg_len"]) <= p["vdu_pct"] * avg50).any())
    pivot = float(base["high"].max())
    return {
        "valid": bool(shrinking and quieter and tight_final and vdu),
        "n": n, "depths": depths, "pivot": pivot, "vdu": vdu,
        "shrinking": shrinking, "quieter": quieter, "tight_final": tight_final,
    }

# ----- Breakout trigger (current bar) -----
def vcp_breakout(row, vcp, p=VCP_P) -> bool:
    return bool(vcp.get("valid")
               and row["close"] > vcp["pivot"] * (1 + p["pivot_buffer"])
               and row["volume"] >= p["breakout_vol_mult"] * row["vol20"])
```

> RSI/MACD are **not** gating here — confirmation only, in manual review (§3). Dilution and earnings-window checks run as a separate fundamental/event pass before a ticket. `detect_vcp` returns the full feature set (contraction count, depth sequence, VDU) so the §13 journal can log it and the parallel-tag mode can test which VCP shapes carry the edge.

---

## 16. References (selected)

- Minervini, M. *Trade Like a Stock Market Wizard* / *Think and Trade Like a Champion* (SEPA, VCP, Trend Template, pivot entries, stop below final contraction, VDU).
- O'Neil, W. *How to Make Money in Stocks* / IBD (CAN SLIM; sound bases; breakout volume 40–50%+ above average; leaders in top industry groups).
- Weinstein, S. (1988). *Secrets for Profiting in Bull and Bear Markets* (Stage 2 entries, 30-week MA, volume + RS confirmation).
- Darvas, N. *How I Made $2,000,000 in the Stock Market* (box theory; breakouts from tight consolidation on volume).
- George, T.J. & Hwang, C.-Y. (2004). *The 52-Week High and Momentum Investing.* **Journal of Finance**, 59(5), 2145–2176.
- Moskowitz, T.J. & Grinblatt, M. (1999). *Do Industries Explain Momentum?* **Journal of Finance**, 54(4), 1249–1290.
- TraderLion / IBD — VCP & base-breakout mechanics (pivot, breakout volume 1.5–2×+).
- Barchart / J. Rowland, CMT — *Don't fall for false buy signals* (first MACD crossover is often a trap; demand structure + volume + momentum confluence).

---

*Internal Trading SOP — SW-B v3. Educational use only; not investment advice. Use strict risk sizing. Research-grounded; the VCP detector is a strict mechanical proxy — validate via paper-testing before live. Each playbook earns live status independently and only on its own post-haircut expectancy.*
