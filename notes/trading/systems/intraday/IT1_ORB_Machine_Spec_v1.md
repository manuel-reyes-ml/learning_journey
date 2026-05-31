# IT-1 ORB — MACHINE SPECIFICATION v1

*Deterministic translation of the IT-1 Opening Range Breakout playbook for backtesting. Long side specified in full; short side is a mirror (Appendix B). Every rule is a function of data available at the decision timestamp — no look-ahead. Every free choice the source docs left open is flagged as an **OPEN PARAMETER** with a default.*

> **Purpose:** make IT-1 reproducible by a machine. Two engineers implementing this spec should produce the same equity curve. Where the v2 docs were silent or discretionary, I made an explicit modeling decision and labeled it `[DECISION]`. Change any of these — but change them on purpose, on in-sample data, and validate out-of-sample.

---

## 0. Conventions

- All timestamps in **US/Eastern**. Bars are timestamped at their **open** unless stated; "a bar closes at T" means the interval `[T, T+Δ)`.
- A signal evaluated at the close of a 5m bar ending at `t` may use data through `t` only. Actions occur on the **next** bar unless a fill convention says otherwise (§14).
- "R" = initial dollar risk per share = `entry − stop`. All outcomes reported in R multiples.
- Booleans are strict unless a tolerance/buffer is named.
- `[DECISION]` = a choice not dictated by the v2 docs. `[OPEN PARAMETER]` = a tunable with a default that must be set in-sample.

---

## 1. Data Requirements

| Series | Granularity | Window | Used for |
|---|---|---|---|
| Target ticker OHLCV | **1-minute**, incl. premarket (04:00–09:30) | trade day + trailing 20 sessions | 5m/15m resample, VWAP, RVOL baseline, ORH/ORL, PMH/PML |
| Target ticker OHLCV | **daily** | trailing ≥ 60 sessions | ADV, ATR(daily), prior-day H/L/C, universe screen |
| QQQ OHLCV | **1-minute**, RTH | trade day | market-alignment, RS line |
| Trading calendar | — | full backtest range | session bounds, **half-days** (early-close days flag) |

**Hard data rules (point-in-time):**
- The trailing-20-session RVOL baseline and all indicators use **only sessions strictly before the trade day** (baseline) plus intraday bars **up to the decision timestamp**.
- Survivorship: the candidate universe must include **delisted tickers** as of each historical date, or selection bias inflates results. *(Less critical for IT-1 than for SW-A, but still required if you screen a broad universe.)*
- VWAP, ATR, RSI, MACD, RS, RVOL are all **recomputed per timestamp**; none may reference a future bar.

---

## 2. Derived Series (exact definitions)

**Resampling.** Build 5m and 15m bars from 1m by left-closed, left-labeled aggregation within RTH (09:30–16:00). 5m bars: 09:30, 09:35, … 15:55.

**Session VWAP (per bar, RTH-only reset at 09:30):**
```
tp_i      = (high_i + low_i + close_i) / 3          # 1m typical price, RTH only
vwap(t)   = Σ_{i=09:30..t} (tp_i * vol_i) / Σ_{i=09:30..t} vol_i
```
`[OPEN PARAMETER] vwap_include_premarket = False` `[DECISION]` (standard intraday VWAP resets at the open).
The 5m-bar VWAP value = `vwap` at the bar's closing minute.

**VWAP slope** (the doc's "rising/falling/flat" gate, quantified):
```
window_min      = vwap_slope_window           # [OPEN PARAMETER] default 30 (minutes)
slope_per_min   = OLS slope of vwap over last `window_min` 1m values
slope_norm      = slope_per_min * window_min / vwap(t)     # % move over the window
state = RISING  if slope_norm >=  flat_band
        FALLING if slope_norm <= -flat_band
        FLAT    otherwise
```
`[OPEN PARAMETER] flat_band = 0.0005` (i.e. 0.05% over the window) — **this single threshold gates every trade; tune it deliberately.**

**ATR.** `atr_5m = ATR(14)` on a **continuous** 5m series (no session reset); `atr_d = ATR(14)` on daily.

**Momentum filter (doc says "1H"; see §note).** `[DECISION]` Compute on a **continuous 5m** series so a valid value exists at 09:45:
```
rsi5   = RSI(rsi_len) on continuous 5m            # [OPEN PARAMETER] rsi_len = 14
macd_hist = MACD(12,26,9) histogram on continuous 5m
rsi_rising = rsi5(t) > rsi5(t - mom_lookback)     # [OPEN PARAMETER] mom_lookback = 1 bar
macd_improving = macd_hist(t) > macd_hist(t - mom_lookback)
```
*Note:* the v2 doc specifies a **1-hour** momentum filter, but the first 60m bar does not close until 10:30, inside the trigger window, so discrete 1H values are unstable at the open. Continuous-5m RSI/MACD is the deterministic substitute. `[OPEN PARAMETER] momentum_timeframe ∈ {"5m_continuous","60m_continuous"}; default "5m_continuous"`. If you switch to 60m, use the continuous (non-reset) 60m series and evaluate the partial bar.

**RVOL (time-of-day normalized, the correct intraday form):**
```
cumvol(t)        = Σ 1m volume from 09:30 to t (this session)
base_cumvol(m)   = mean over trailing `rvol_lookback` sessions of cumvol at minute-of-session m
rvol(t)          = cumvol(t) / base_cumvol(minute_of_session(t))
```
`[OPEN PARAMETER] rvol_lookback = 20` sessions. Requires building an intraday volume profile per ticker.

**RS line (vs QQQ):**
```
rs(t)      = close_ticker(t) / close_qqq(t)        # timestamp-aligned 5m closes
rs_slope   = OLS slope of rs over last `rs_window` minutes
            # [OPEN PARAMETER] rs_window = 30
rs_ok_long = rs_slope >= -rs_band                  # "flat-to-rising"
            # [OPEN PARAMETER] rs_band = 0  (>=0 means strictly flat-to-rising)
```

---

## 3. Universe / Candidate Selection (mechanical screen — run pre-market)

A backtest cannot use "stock is in play." Replace with a deterministic daily screen producing the candidate list for that day:
```
eligible(ticker, day) =
      ADV_20            >= adv_min                  # liquidity
  AND close_prev        >= price_min
  AND premkt_gap_or_rvol_rank in top N              # "in play" proxy
```
`[OPEN PARAMETER]` defaults: `adv_min = 1_000_000` shares, `price_min = $5`, `in_play_metric = "premarket_rvol"`, `top_N = 20`. `[DECISION]` "In play" is operationalized as the top-N tickers by premarket relative volume (premarket cumulative volume ÷ trailing-20 premarket average). Document and freeze this — it materially drives results.

---

## 4. Session Constants (compute once per ticker-day)

```
ORH = max(high) of 1m bars in [09:30:00, 09:45:00)     # first 15 min
ORL = min(low)  of 1m bars in [09:30:00, 09:45:00)
OR_size = ORH - ORL
PMH/PML = max high / min low of 1m bars in [04:00, 09:30)
PDH/PDL/PDC = prior regular session high/low/close
```

---

## 5. Hard Gates (pre-filters — if any fails, NO TRADE regardless of confirmation count)

Evaluated at the **trigger bar's close**:

1. `time_ok`: `09:45 <= trigger_time <= 10:30` (ET). Hard cap per v2.
2. `slope_gate (long)`: VWAP `state == RISING`. (`FLAT` or `FALLING` ⇒ stand down.)
3. `eligible(ticker, day)` is True (§3).
4. Not blocked by session/portfolio limits (§13).

> The v2 IT-1 doc lists **no** extension cap (that is an IT-2/VWAP rule). It is therefore **not** applied here. `[OPEN PARAMETER] apply_extension_cap = False` if you later want to import it.

---

## 6. The Five Confirmations (each a boolean at trigger-bar close)

| # | Name | Long formula |
|---|---|---|
| C1 | Level | `True` **by construction** — the trigger is a break of ORH, a defined level. *(Optional confluence bonus, not required.)* |
| C2 | VWAP | `close > vwap(t)` **AND** VWAP `state == RISING` |
| C3 | Market | `qqq_close(t) >= qqq_vwap(t)` **AND** qqq VWAP `state != FALLING` |
| C4 | RS | `rs_ok_long` (rs_slope ≥ −rs_band) |
| C5 | Volume | `trigger_bar.volume >= vol_mult * avg_5m_vol_same_TOD` **AND** `rvol(t) >= rvol_min` |

`[OPEN PARAMETER]` `vol_mult = 1.5`, `rvol_min = 1.5`. `avg_5m_vol_same_TOD` = trailing-`rvol_lookback`-session mean volume for that 5m slot.

**Effective requirement:** C1 is always true, so a valid long needs **≥2 of {C2, C3, C4, C5}** to reach the 3/5 minimum.

---

## 7. Confirmation Score → Grade → Risk

```
score = C1+C2+C3+C4+C5            # C1 always 1
tradeable = score >= 3
grade = "A+" if score >= 4 else "A"      # per v2 scoring shortcut
```
Sizing: the v2 doc leaves "size up modestly" discretionary. `[DECISION]` Default to a **flat risk %** for a clean baseline; an optional tier table is provided.
```
risk_pct = 0.005                          # [OPEN PARAMETER] default 0.5%
# Optional tier table (set use_tiers=True to enable):
#   score 3 -> 0.005, score 4 -> 0.0075, score 5 -> 0.010
```

---

## 8. Trigger Detection (long)

```
trigger_bar = first 5m bar b in [09:45, 10:30] such that:
      b.close > ORH * (1 + break_buf)        # [OPEN PARAMETER] break_buf = 0
  AND all Hard Gates pass at b.close (§5)
  AND score(b) >= 3 (§6,§7)
At most one trigger per ticker-day (first qualifying bar).
```

---

## 9. Entry Model & Fill

`[OPEN PARAMETER] entry_model ∈ {"retest","immediate"}; default "retest"` (matches "preferred" in v2).

**Retest (default):**
```
After trigger_bar, scan forward 5m bars until min(trigger_time + retest_max_bars*5m, entry_cutoff):
  hold_bar = first bar h with:
        h.low  <= ORH * (1 + retest_tol)     # price returns to the level
    AND h.close > ORH                          # but holds above it
  If hold_bar found:
        ENTRY at OPEN of the bar AFTER hold_bar (the "first confirmation candle")
  Else: NO TRADE (this encodes the v2 "no chase / wait for retest or skip").
```
`[OPEN PARAMETER]` `retest_max_bars = 6` (30 min), `retest_tol = 0.0005`, `entry_cutoff = 11:00 ET`.

**Immediate (optional, aggressive):**
```
Allowed only if trigger_bar.close <= ORH * (1 + chase_pct):   # no-chase guard
      ENTRY at OPEN of bar after trigger_bar.
chase_pct = 0.01   # [OPEN PARAMETER] from v2 "if >1% beyond trigger, wait or skip"
```

**Fill price** = the relevant bar **open** + slippage (§14). `[DECISION]` Entering on next-bar open (not signal-bar close) avoids using the signal bar's own close as the fill.

---

## 10. Stop, Risk/Share, Position Size

```
# Retest model:
raw_stop = min(hold_bar.low, ORH) - stop_buffer
# Immediate model:
raw_stop = min(trigger_bar.low, ORH) - stop_buffer

stop_buffer = stop_buf_atr * atr_5m              # [OPEN PARAMETER] stop_buf_atr = 0.10
stop = raw_stop
risk_per_share = entry - stop
if risk_per_share < min_risk_atr * atr_5m:       # "if retest is tight" guard
    stop = ORH - stop_buffer ; risk_per_share = entry - stop   # [DECISION]
# min_risk_atr = 0.15  [OPEN PARAMETER]

dollar_risk = equity_base * risk_pct             # [DECISION] fixed equity base (no compounding) for clean R; set compound=True to compound
shares = floor(dollar_risk / risk_per_share)     # round DOWN (v2)
# Optional realism cap: shares <= adv_participation * ADV_20   [OPEN PARAMETER] adv_participation = 0.01
if shares == 0: NO TRADE
```

---

## 11. Targets, Partial, Breakeven, Trailing, T2

```
R = risk_per_share
# Partial: 50% at +1R
partial_price = entry + partial_R * R            # [OPEN PARAMETER] partial_R = 1.0, partial_frac = 0.5
On partial fill: move stop to BREAKEVEN (= entry). (v2: only after partial earned.)

# Runner target T2 = measured move (objective; "next HTF level" dropped as discretionary)
T2 = ORH + or_mult * OR_size                     # [OPEN PARAMETER] or_mult = 1.0  [DECISION] drop discretionary HTF target

# Runner trailing: under confirmed 5m swing (pivot) lows
pivot_n = 1                                       # [OPEN PARAMETER]
A bar i is a pivot low if low_i <= lows of pivot_n bars on each side.
  -> CONFIRMED only at bar i+pivot_n (NO LOOK-AHEAD).
trail_stop = max(trail_stop, last_confirmed_pivot_low - stop_buffer)   # monotonic up only
```
Runner exits at the **first** of: T2 limit hit, trail stop hit, an exit rule in §12, or EOD flatten.

*Optional structural T1:* `[OPEN PARAMETER] use_pdh_partial = False` — if True, partial at `min(+1R level, PDH)` when PDH > entry.

---

## 12. Exit Rules (pre- and post-partial)

Evaluated each 5m close while in position:
1. **Stop / target fills** per §14 intrabar rules.
2. **OR re-entry invalidation:** `close < ORH` (long) ⇒ exit at that bar close. *(Active before breakeven is reached.)*
3. **VWAP slope flip:** VWAP `state == FALLING` for `vwap_flip_bars` consecutive 5m bars and price not back above VWAP ⇒ exit. `[OPEN PARAMETER] vwap_flip_bars = 2`.
4. **Market reversal (optional):** `qqq_close < qqq_vwap` with qqq state FALLING for `mkt_flip_bars` ⇒ exit. `[OPEN PARAMETER] enable_market_exit = True, mkt_flip_bars = 2`.
5. **Time stop:** at `entry_bar + time_stop_bars`, if `MFE_R < progress_R` ⇒ exit at close. `[OPEN PARAMETER] time_stop_bars = 3, progress_R = 0.5` *(v2 says "no progress" without a number — this is the definition you must own).*
6. **EOD flatten:** force-close any open position at `flat_time`. `[OPEN PARAMETER] flat_time = 15:55 ET`. (IT-1 is intraday — no overnight.)

---

## 13. Session / Portfolio Constraints

```
max_trades_day   = 3        # [OPEN PARAMETER] v2: 3–5
daily_max_loss_R = 2.0      # [OPEN PARAMETER] v2: 2–3R ; stop new entries when day P&L <= -this
two_loss_rule    = "stop"   # [DECISION/OPEN PARAMETER] {"stop","halve"} after 2 consecutive losers; default stop for the day
dow_policy       = "tag_only"  # [DECISION] baseline does NOT skip/resize by weekday; only tags it.
                               # Enable "skip_fri" / "half_mon" ONLY after your own data justifies it (v2's own caveat).
```

---

## 14. Costs & Fill Assumptions `[DECISION]`

- **Entries:** next-bar open ± `slippage` (adverse).
- **Stops:** if a 5m bar's `low <= stop` ⇒ filled at `min(open, stop) − slippage` (gap-through handled).
- **Targets/partials:** if `high >= target` ⇒ filled at `target` (limit). 
- **Same-bar stop & target:** assume **stop first** (conservative).
- `slippage` per share `[OPEN PARAMETER] = $0.03` (v2 cites $0.02–0.05). `commission [OPEN PARAMETER] = $0.005/share or per-trade as your broker`.

---

## 15. Look-Ahead / Determinism Audit

| Quantity | Uses only past/known data? | Mechanism |
|---|---|---|
| VWAP, VWAP slope | yes | cumulative to `t`, trailing regression |
| RVOL baseline | yes | trailing sessions **strictly before** trade day |
| RSI/MACD/RS | yes | continuous series up to `t` |
| ORH/ORL/PMH/PDH | yes | completed prior windows |
| Swing-low trail | yes | pivot **confirmed with `pivot_n`-bar lag** |
| QQQ alignment/RS | yes | timestamp-aligned, no future bars |
| Entry fill | yes | next-bar open |
| Stop/target intrabar | conservative | stop-before-target assumption |

If any future-dated value enters a decision, the backtest is invalid. Re-audit after any code change.

---

## 16. Open Parameters — Master Table

> These are your degrees of freedom. Testing many combinations on the same data **is** overfitting. Set defaults, tune on **in-sample only**, confirm on **untouched out-of-sample**, then **walk-forward**. Treat each parameter you tune as a multiple-comparisons cost.

| Param | Default | Section |
|---|---|---|
| vwap_slope_window | 30 min | §2 |
| **flat_band** | 0.0005 | §2 (gates every trade) |
| vwap_include_premarket | False | §2 |
| momentum_timeframe | 5m_continuous | §2 |
| rsi_len / mom_lookback | 14 / 1 | §2 |
| rvol_lookback | 20 | §2 |
| rs_window / rs_band | 30 / 0 | §2 |
| adv_min / price_min / top_N / in_play_metric | 1M / $5 / 20 / premarket_rvol | §3 |
| break_buf | 0 | §8 |
| entry_model | retest | §9 |
| retest_max_bars / retest_tol / entry_cutoff | 6 / 0.0005 / 11:00 | §9 |
| chase_pct | 0.01 | §9 |
| vol_mult / rvol_min | 1.5 / 1.5 | §6 |
| risk_pct / use_tiers | 0.005 / False | §7 |
| stop_buf_atr / min_risk_atr | 0.10 / 0.15 | §10 |
| adv_participation | 0.01 | §10 |
| partial_R / partial_frac / or_mult | 1.0 / 0.5 / 1.0 | §11 |
| pivot_n | 1 | §11 |
| vwap_flip_bars / mkt_flip_bars / enable_market_exit | 2 / 2 / True | §12 |
| time_stop_bars / progress_R | 3 / 0.5 | §12 |
| flat_time | 15:55 | §12 |
| max_trades_day / daily_max_loss_R / two_loss_rule / dow_policy | 3 / 2.0 / stop / tag_only | §13 |
| slippage / commission | $0.03 / broker | §14 |

---

## 17. Evaluation Pseudocode

```python
for day in trading_days:
    candidates = screen_universe(day)                 # §3
    for tk in candidates:
        bars1m, bars5m = load(tk, day)                # incl. premarket + trailing
        qqq5m = load_aligned("QQQ", day)
        ORH, ORL, OR_size, PMH, PDH = session_constants(tk, day)  # §4
        derived = build_series(bars1m, bars5m, qqq5m)             # §2

        state = "FLAT"  # ticker-day state machine: FLAT->TRIGGERED->IN_POSITION->DONE
        trade = None
        for b in bars5m where 09:45 <= b.time:
            if portfolio_blocked(day): break          # §13
            if state == "FLAT":
                if is_trigger(b, ORH, derived):       # §5,§6,§7,§8
                    state, trig = "TRIGGERED", b
            elif state == "TRIGGERED":
                ok, entry_ctx = check_entry(b, trig, ORH, derived)  # §9
                if ok:
                    trade = open_trade(entry_ctx, ORH, OR_size, derived)  # §10,§11
                    state = "IN_POSITION"
                elif past_entry_window(b, trig): state = "DONE"
            elif state == "IN_POSITION":
                trade = manage(trade, b, ORH, derived)   # §11,§12,§14
                if trade.closed: record(trade); state = "DONE"
        if state == "IN_POSITION":                      # EOD flatten §12.6
            record(flatten(trade, flat_time))
    update_portfolio_stats(day)                         # §13
```

---

## 18. Trade-Log Output Schema (maps to your v2 journal)

`date, ticker, day_of_week, trigger_time, entry_time, entry, stop, init_risk_per_share, shares, risk_pct, grade, score, C1..C5, vwap_slope_norm_at_trigger, rvol_at_trigger, rs_slope_at_trigger, qqq_aligned, entry_model, partial_filled, exit_time, exit_price, exit_reason, R_realized, MAE_R, MFE_R, notes`

`exit_reason ∈ {target_T2, trail_stop, stop, OR_invalidation, vwap_flip, market_reversal, time_stop, eod_flatten}`

---

## Appendix A — Decisions Where the v2 Docs Were Silent/Discretionary

1. VWAP slope quantified as normalized regression slope with `flat_band` dead-zone (§2).
2. Momentum on continuous 5m, not discrete 1H (availability at the open) (§2).
3. RVOL defined as time-of-day-normalized cumulative ratio (§2).
4. "In play" operationalized as premarket-RVOL top-N (§3).
5. Default sizing = flat 0.5% (tier table optional) (§7).
6. Entry fill = next-bar open; retest model is default (§9).
7. "Tight retest" fallback to ORH-based stop made explicit (§10).
8. T2 = measured move; discretionary HTF target dropped (§11).
9. Time-stop "progress" defined as MFE < 0.5R at bar 3 (§12).
10. DOW baseline = tag only, no filtering (§13).
11. Intrabar same-bar conflict resolved stop-first (§14).

## Appendix B — Short-Side Mirror

Replace, holding all parameters identical:
- ORH → ORL; "close above" → "close below"; `state RISING` → `FALLING`.
- C2: `close < vwap AND state==FALLING`. C3: `qqq_close <= qqq_vwap AND qqq state != RISING`. C4: `rs_slope <= +rs_band`.
- Stop = `max(hold_bar.high, ORL) + stop_buffer`. T2 = `ORL − or_mult*OR_size`. Trail under confirmed pivot **highs** (monotonic down).
- OR-invalidation: `close > ORL`. VWAP flip exit: state RISING for `vwap_flip_bars`.

---

*Educational/operational specification only. Not investment advice. This document defines process and execution logic; it makes no claim that the strategy has positive expectancy — that is what the backtest is for.*
