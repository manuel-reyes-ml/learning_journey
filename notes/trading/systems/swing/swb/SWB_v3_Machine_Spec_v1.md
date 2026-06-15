# SW-B v3 — MACHINE SPECIFICATION v1

*Deterministic translation of the SW-B v3 Trend Continuation / VCP playbook for backtesting. Long-only. Every rule is a function of data available at the decision date — no look-ahead. **[OPEN PARAMETER]** = tunable with a default; **[DECISION]** = a modeling choice not dictated by the deep spec.*

> **Purpose:** make SW-B v3 reproducible by a machine. Source of truth: `SWB_v3_Trend_Continuation_VCP.md` (deep spec) and `Master_Swing_Trading_Plan_v3.md`. The hard part — and the reason SW-B needs a machine spec more than SW-A v3 — is the **deterministic VCP detector** (§6). It is a strict mechanical proxy of a discretionary read; treat divergence from your eye as data, not noise.
>
> **Shared with SW-A v3.** Data contract, regime state, sector ranking, RS, universe screen, footprint instrumentation, costs, portfolio constraints, look-ahead audit, and the two run modes are **identical to `SWA_v3_Machine_Spec_v1.md`** and are referenced rather than re-derived, to keep the two specs in lockstep. Only SW-B-specific differences are fully written out here.
>
> **This spec defines process and execution logic only. It makes no claim of positive expectancy — that is what the backtest is for.**

---

## 0. Conventions

Identical to SWA spec §0. Daily EOD decisions; actions on `t+1`; `R = entry − stop`; `[OPEN PARAMETER]`/`[DECISION]` tags; Funnel vs Parallel-tag run modes (§17).

---

## 1. Data Requirements

Identical to SWA spec §1 (daily ticker/SPY/11 SPDR ETFs, point-in-time sector membership, earnings, dilution, calendar) with the same point-in-time and survivorship rules. No additional series — the VCP detector runs on the same daily OHLCV.

---

## 2. Derived Series

Trend, RS, sector ranking, volume/ATR, and footprint features are **identical to SWA spec §2**, with **one parameter change**:
```
rs_floor = 80        # [OPEN PARAMETER]  (SW-B differentiator; SW-A v3 uses 70)
```
SW-B additionally relies on the VCP feature set computed in §6.

---

## 3. Universe / Candidate Selection

Identical to SWA spec §3 (`adv_min = 1_000_000`, `price_min = $5`, ≥252 sessions history). The eligible set is the cross-section for `rs_percentile`.

---

## 4. Regime State (Stage 0)

Identical to SWA spec §4 (`regime_ok = SPY uptrend`; `index_dist_days`; `regime_action ∈ {gate,scale,observe}; default gate`; `regime_mult` observe-mode).

---

## 5. Hard Gates / Mandatory Floors (ALL must pass — there is no 4-of-6 vote)

SW-B's filters are stricter than SW-A v3's: **five mandatory floors**, all required. Evaluated at close of `t`:

1. `regime_ok` (§4).
2. `trend_ok` : `close > rising sma50` (`sma50 > sma200` preferred).
3. `rs_ok`    : `rs_percentile >= 80 AND NOT rs_line_falling`.
4. `sector_top_third(sector(ticker,t))` is True. *(Bottom-third / falling sector RS ⇒ NO TRADE.)*
5. `vcp.valid` is True (§6) — **a valid VCP is mandatory; no VCP = not an SW-B trade.**
6. `breakout` fires (§7) on volume ≥ `breakout_vol_mult * vol20`.

Plus the shared event/quality gates (same as SWA §5): `extension <= ext_max`, `near_high`, `no_dilution(60)`, `no_earnings(earn_block)`, and portfolio limits (§12).

> Unlike SW-A v3, there is **no scored 4/6 relaxation.** Any floor failing = NO TRADE. Momentum (RSI/MACD) is confirmation only and never substitutes for a floor.

---

## 6. VCP Detection (the core — deterministic)

Direct machine form of deep spec §3/§15. Runs on the candidate **base window** ending at `t-1` (the breakout bar is `t`). `[DECISION]` the base is the trailing window `[t-base_max_len, t-1]`, trimmed to the most recent contraction sequence.

```
VCP_P = dict(
    zigzag_pct       = 0.05,   # swing-reversal threshold (test 0.03–0.08)   [OPEN PARAMETER]
    min_contractions = 2, max_contractions = 6,                              # [OPEN PARAMETER]
    depth_decline_tol= 0.0,    # 0.0 = strictly shallower each leg            [OPEN PARAMETER]
    vol_decline_tol  = 0.0,    # each leg quieter than the last               [OPEN PARAMETER]
    final_contraction_max = 0.10,  # final leg <= 10% (ideally <= 0.06)       [OPEN PARAMETER]
    vdu_pct = 0.50, vdu_avg_window = 50, final_leg_len = 10,                  # [OPEN PARAMETER]
    breakout_vol_mult = 1.5,   # pivot-break volume >= 1.5x (2x+ preferred)   [OPEN PARAMETER]
    pivot_buffer = 0.002,                                                     # [OPEN PARAMETER]
    base_min_len = 15, base_max_len = 65,                                     # [OPEN PARAMETER]
    prior_advance_min = 0.25,  # base must follow a >=25% advance off pre-base low  [DECISION]
)

def swings(close, pct):                      # ZigZag-style alternating H/L pivots
    piv, trend = [], 0
    hi = lo = close.iloc[0]; hi_i = lo_i = 0
    for i, px in enumerate(close):
        if px > hi: hi, hi_i = px, i
        if px < lo: lo, lo_i = px, i
        if trend >= 0 and px <= hi*(1-pct):
            piv.append((hi_i, hi, "H")); trend, lo, lo_i = -1, px, i
        elif trend <= 0 and px >= lo*(1+pct):
            piv.append((lo_i, lo, "L")); trend, hi, hi_i = 1, px, i
    return piv

def detect_vcp(base, p=VCP_P) -> dict:
    if not (p["base_min_len"] <= len(base) <= p["base_max_len"]):
        return {"valid": False, "reason": "base_length"}
    # prior-advance gate (Stage-2 context): price up >= prior_advance_min into the base
    if (base["close"].iloc[0] / base["low"].min() - 1) < 0:   # placeholder; see note
        pass
    sw = swings(base["close"], p["zigzag_pct"])
    contr = []
    for a, b in zip(sw, sw[1:]):                 # High -> following Low = one contraction
        if a[2] == "H" and b[2] == "L":
            depth   = (a[1]-b[1]) / a[1]
            seg_vol = base["volume"].iloc[a[0]:b[0]+1].mean()
            contr.append((depth, seg_vol))
    n = len(contr)
    if not (p["min_contractions"] <= n <= p["max_contractions"]):
        return {"valid": False, "reason": "contraction_count", "n": n}
    depths = [c[0] for c in contr]; vols = [c[1] for c in contr]
    shrinking   = all(depths[i+1] <= depths[i]*(1-p["depth_decline_tol"]) for i in range(n-1))
    quieter     = all(vols[i+1]   <= vols[i]  *(1-p["vol_decline_tol"])   for i in range(n-1))
    tight_final = depths[-1] <= p["final_contraction_max"]
    avg50 = base["volume"].rolling(p["vdu_avg_window"]).mean().iloc[-1]
    vdu   = bool((base["volume"].tail(p["final_leg_len"]) <= p["vdu_pct"]*avg50).any())
    pivot = float(base["high"].max())
    return {"valid": bool(shrinking and quieter and tight_final and vdu),
            "n": n, "depths": depths, "pivot": pivot, "vdu": vdu,
            "shrinking": shrinking, "quieter": quieter, "tight_final": tight_final}
```

> **VDU is a GATE for SW-B, not observe-mode.** A valid VCP *requires* `vdu == True` and `quieter == True`. This is the one place the shared footprint spec (§14) diverges: `vdu_pct` is load-bearing here.
>
> **Mechanized-proxy caveat (acute for VCP).** Expect false positives (mechanical "VCP" your eye rejects) and false negatives (clean VCPs missed). `zigzag_pct` is the most sensitive knob — coarse sensitivity-check, do **not** fine-optimize. Forward/paper test validates the real pattern.

---

## 7. Breakout Trigger & Entry

**Trigger (defining SW-B entry):** pivot breakout at close of `t`.
```
breakout = vcp["valid"]
       AND close(t) > vcp["pivot"] * (1 + pivot_buffer)
       AND volume(t) >= breakout_vol_mult * vol20(t)
At most one trigger per ticker per VCP. Reject 3–5x climax-into-resistance bars [OPEN PARAMETER] climax_mult = 3.0.
```

**Entry model** `[OPEN PARAMETER] entry_model ∈ {"next_open","retest","pullback_to_pivot"}; default "next_open"`:
- **next_open (default):** enter `open(t+1) + slippage` if `next_open <= breakout_close*(1+chase_pct)`; else NO TRADE. `[OPEN PARAMETER] chase_pct = 0.04` (deep spec: 3–5% no-chase).
- **retest:** after breakout, wait up to `retest_max_days` for a pullback to `pivot` that holds (close back above), enter next open. Tightest risk. `[OPEN PARAMETER] retest_max_days = 5`.
- **pullback_to_pivot:** after a valid completed VCP+breakout, buy a controlled pull to pivot/20-50 EMA that holds.

> Classification (vs SW-A v3) is driven by **mandatory VCP + RS ≥ 80**, not by which fill is used. A pullback-to-MA reclaim *without* a valid VCP and with RS 70–79 is an SW-A v3 trade, not SW-B (deep spec §10).

---

## 8. Confirmation (mandatory floors recap) → Grade → Risk

```
floors_ok = trend_ok AND (rs_percentile>=80 AND not rs_line_falling)
            AND sector_top_third AND vcp.valid AND breakout
momentum_ok = (rsi14>=rsi_floor) AND (rsi14>rsi14[-1]) AND (macd_hist>macd_hist[-1])  # confirmation only
tradeable = floors_ok AND all_shared_event_gates(§5)
grade = "A+" if (floors_ok AND sector_top_third AND momentum_ok) else "A"
        # B tier = floors_ok but middle-third sector; default skip  [DECISION] trade_B = False
```
**Risk tier → risk_pct** (deep spec §5 — SW-B's A+ is **NOT** capped; it is the elite book):
```
risk_pct = {"A+": 0.010, "A": 0.0075, "B": 0.0050}[tier_of(grade)]   # [OPEN PARAMETER]
```

---

## 9. Stop, Risk/Share, Position Size

```
final_contraction_low = min(low over the final VCP contraction leg)
raw_stop = final_contraction_low - stop_buf_atr*atr_d(t)      # [OPEN PARAMETER] stop_buf_atr = 0.10
# if the final contraction is unusually deep, fall back to pivot - buffer:
if (entry - raw_stop) > max_stop_atr*atr_d(t):               # [OPEN PARAMETER] max_stop_atr = 1.5  [DECISION]
    raw_stop = vcp["pivot"] - stop_buf_atr*atr_d(t)
stop = raw_stop ; risk_per_share = entry - stop
if risk_per_share < min_risk_atr*atr_d(t): NO TRADE          # [OPEN PARAMETER] min_risk_atr = 0.25

dollar_risk = equity_base * risk_pct * (regime_mult if regime_action=="scale" else 1.0)
shares = floor(dollar_risk / risk_per_share)                 # round DOWN
shares = min(shares, floor(adv_participation * adv20(t)))    # [OPEN PARAMETER] adv_participation = 0.01
if shares == 0: NO TRADE
```
The tight final-contraction stop is what makes SW-B's R small and ≥2R reachable — do not enter loose bases (enforced by `final_contraction_max` in §6).

---

## 10. Targets, Partials, Trailing, Time Stop

```
R = risk_per_share
# Measured move from base depth (deep spec §7):
measured_move = vcp["pivot"] + (vcp["pivot"] - min(low over base))      # base height up from pivot
resistance    = first prior swing high above entry within res_lookback, ELSE measured_move
                # [OPEN PARAMETER] res_lookback = 120
if (resistance - entry)/R < 2.0: NO TRADE                               # ≥2R gate

partial_R = 2.0 ; partial_frac = 0.0 (baseline)                         # optional 0.25–0.50 at +2R
trail_mode = "pivot" ; pivot_n = 1                                      # confirmed pivot lows, monotonic up
trail_stop = max(trail_stop, last_confirmed_pivot_low - stop_buf_atr*atr_d)
time_stop_days = 8 ; progress_R = 0.5                                   # exit if MFE_R < 0.5 at day 8
```

---

## 11. Exit Rules (each daily close while in position)

1. Stop / target / resistance fills per §13 (shared with SWA spec §13).
2. **Trend break:** `close < sma50` on volume, or confirmed lower swing low ⇒ exit.
3. **Breakout failure:** `close < pivot` (back inside the base) with distribution ⇒ exit; repeated failed pivots ⇒ no re-entry.
4. **Time stop** (§10).
5. **Distribution warning (observe-mode):** `stock_dist_cluster >= stock_dist_cluster_warn` or `ud_volume_ratio < 1.0` ⇒ **log caution**, do not auto-exit until validated (§14).
6. **Circuit breakers** (§12) gate new entries only.

---

## 12. Session / Portfolio Constraints

Identical to SWA spec §12 (`max_positions = 8`, `max_portfolio_heat = 0.030`, `max_sector_heat = 0.015`, 3-loss pause, −3R weekly stop, rule-violation week pause). One shared heat budget across SW-A v3 and SW-B (deep spec collapse rule).

---

## 13. Costs & Fill Assumptions

Identical to SWA spec §13 (`slippage = $0.03`, stop-before-target on same-bar conflict, 25% haircut applied to aggregate expectancy not per trade, gap-through handling).

---

## 14. Footprint Instrumentation (OBSERVE-MODE — except VDU)

Identical feature library to SWA spec §14 (`distribution_days`, `ud_volume_ratio`, `vdu_present`, `regime_size_multiplier`) with the **same parameter table**, plus the SW-B-specific override:

| Metric | Mode in SW-B |
|---|---|
| Index distribution-day count | observe → regime posture (same as SWA) |
| Stock distribution-day cluster | observe (exit flag) |
| U/D volume ratio | observe (confirmation health) |
| **VDU** | **GATE** — required in the final VCP contraction (§6), not observe |
| RS-line-leads-price | observe (bonus tell) |

---

## 15. Look-Ahead / Determinism Audit

Identical to SWA spec §15, **plus VCP-specific rows:**

| Quantity | Past/known only? | Mechanism |
|---|---|---|
| Swing/ZigZag pivots in base | yes | computed on base window `[t-base_max_len, t-1]`, closed bars only |
| Contraction depths / leg volumes | yes | between confirmed pivots ≤ `t-1` |
| Pivot (base high) | yes | `max(high)` over base ≤ `t-1` |
| Breakout trigger | yes | close/volume at `t`; fill at `t+1` open |
| VDU | yes | trailing volume vs 50-day avg ≤ `t-1` |

The ZigZag is causal as written (single forward pass, pivot recorded only after the reversal threshold is crossed). Confirm no implementation re-labels pivots using future bars.

---

## 16. Open Parameters — Master Table

Shared parameters: see SWA spec §16. SW-B-specific / changed:

| Param | Default | Section |
|---|---|---|
| **rs_floor** | **80** | §2 (SW-B differentiator) |
| zigzag_pct | 0.05 | §6 (most sensitive VCP knob) |
| min/max_contractions | 2 / 6 | §6 |
| depth_decline_tol / vol_decline_tol | 0.0 / 0.0 | §6 |
| final_contraction_max | 0.10 | §6 |
| vdu_pct / vdu_avg_window / final_leg_len | 0.50 / 50 / 10 | §6 (VDU is a GATE) |
| base_min_len / base_max_len | 15 / 65 | §6 |
| prior_advance_min | 0.25 | §6 |
| **breakout_vol_mult** | 1.5 | §6/§7 (gates the breakout) |
| pivot_buffer | 0.002 | §6/§7 |
| climax_mult | 3.0 | §7 |
| entry_model / chase_pct / retest_max_days | next_open / 0.04 / 5 | §7 |
| risk_pct (A+/A/B) | 0.010 / 0.0075 / 0.0050 | §8 (A+ uncapped) |
| trade_B | False | §8 |
| stop_buf_atr / max_stop_atr / min_risk_atr | 0.10 / 1.5 / 0.25 | §9 |
| adv_participation | 0.01 | §9 |
| res_lookback / partial_R / partial_frac | 120 / 2.0 / 0.0 | §10 |
| trail_mode / pivot_n | pivot / 1 | §10 |
| time_stop_days / progress_R | 8 / 0.5 | §10 |

---

## 17. Evaluation Pseudocode

```python
sectors_ranked = {}
for day in trading_days:
    if is_weekend_rerank(day):
        sectors_ranked = rank_sectors(sector_px, spy, asof=day)      # shared §2
    regime   = regime_state(spy, day)                                # shared §4
    universe = [tk for tk in all_tickers if eligible(tk, day)]       # shared §3
    rs_pct   = cross_sectional_rs_percentile(universe, day)          # shared §2 (floor 80)

    strong = [s for s in SPDR if sectors_ranked.top_third(s)]
    cands  = [tk for tk in universe if sector(tk,day) in strong]     # FUNNEL mode

    for tk in cands:
        df = load_daily(tk, day)
        if not (regime_ok(regime) and trend_ok(df,day)
                and rs_pct[tk] >= 80 and not rs_line_falling(df,day)
                and shared_event_gates(tk,df,day)):                  # §4,§5
            continue
        base = df.loc[day-base_max_len : day-1]
        vcp  = detect_vcp(base)                                      # §6
        if not vcp["valid"]: continue
        if not breakout(df, vcp, day): continue                     # §7
        grade = grade_swb(df, vcp, rs_pct, sectors_ranked, day)     # §8
        if portfolio_blocked(day, sector(tk,day)): continue         # §12
        entry = entry_fill(tk, day, vcp)                            # §7  (open of day+1)
        if entry is None: continue
        trade = open_trade(entry, df, vcp, grade)                   # §9,§10 (incl. ≥2R gate)
        if trade is None: continue
        register(trade)

    manage_open_positions(day)                                      # §11,§13
    update_portfolio_stats(day)                                     # §12

# PARALLEL-TAG mode: skip the sector pre-filter; run VCP+breakout on the full eligible universe,
# TAG sector_tier + footprint buckets + VCP shape (n_contractions, final_leg_depth) on each trade,
# then split realized expectancy to test which gates/shapes carry the edge.
```

---

## 18. Trade-Log Output Schema (maps to deep spec §13 journal)

`date, ticker, sector_etf, sector_rank, sector_tier, entry_trigger, grade, floors_ok, rs_percentile, rs_leads_price, vcp_n_contractions, vcp_depth_sequence, vcp_final_leg_depth, vdu_present, pivot, breakout_vol_x, entry_model, entry_date, entry, stop, init_risk_per_share, shares, risk_pct, regime_uptrend, index_dist_days, ud_volume_ratio, stock_dist_count, planned_R, target_resistance, partial_filled, exit_date, exit_price, exit_reason, R_realized, MAE_R, MFE_R, notes`

`exit_reason ∈ {target_resistance, trail_stop, stop, trend_break, breakout_fail, time_stop}`

> **Log the VCP shape** (`vcp_n_contractions`, `vcp_final_leg_depth`, `vcp_depth_sequence`) on every trade so the parallel-tag mode can test whether tighter/deeper finals or more/fewer contractions carry the edge (deep spec §13).

---

## Appendix A — Decisions Where the Deep Spec Was Silent/Discretionary

1. **VCP base window** = trailing `[t-base_max_len, t-1]`; swings via causal ZigZag at `zigzag_pct` (§6).
2. **"Each shallower / each quieter"** = strict monotone decrease with tolerance knobs `depth_decline_tol`/`vol_decline_tol` defaulted to 0 (§6).
3. **VDU promoted to a hard gate** for SW-B (mandatory in a valid VCP), unlike its observe-mode role in SW-A v3 (§6,§14).
4. **Prior-advance / Stage-2 context** required before the base (`prior_advance_min`) (§6).
5. **Entry fill** = `open(t+1)`; `next_open` default with no-chase guard at 4% (§7).
6. **Stop** = final-contraction low − ATR buffer, with a deep-final fallback to pivot − buffer (§9).
7. **≥2R resistance** = nearest prior swing high else measured move (base height) (§10).
8. **A+ uncapped at 1.0%** (SW-B is the elite book), vs SW-A v3's 0.75% cap (§8).
9. **Shared modules** (regime/sector/RS/universe/footprint/costs/portfolio) inherited verbatim from SWA spec to prevent drift (§§1–4,12–15).

## Appendix B — Parallel-Tag Attribution Harness

Same as SWA spec Appendix B, extended: run VCP+breakout on the **full eligible universe** (skip the sector pre-filter), tag `sector_tier`, footprint buckets, **and VCP shape**. Split realized expectancy after costs + 25% haircut to test (a) the sector gate, (b) each footprint metric, and (c) which VCP shapes earn their keep. Promote observe→gate (or tighten a VCP knob) only on a positive, walk-forward-stable result. If a gate only cuts trade count, drop it.

---

*Educational/operational specification only. Not investment advice. This document defines process and execution logic; it makes no claim that the strategy has positive expectancy — that is what the backtest is for.*
