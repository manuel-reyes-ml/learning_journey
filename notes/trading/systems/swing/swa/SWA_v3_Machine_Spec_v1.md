# SW-A v3 — MACHINE SPECIFICATION v1

*Deterministic translation of the SW-A v3 Trend Pullback / Base Breakout playbook for backtesting. Long-only (the book is long-only by design). Every rule is a function of data available at the decision date — no look-ahead. Every free choice the source docs left open is flagged as an **[OPEN PARAMETER]** with a default; every modeling choice not dictated by the deep spec is flagged **[DECISION]**.*

> **Purpose:** make SW-A v3 reproducible by a machine. Two engineers implementing this spec should produce the same equity curve. Source of truth: `SWA_v3_Trend_Pullback_Base_Breakout.md` (deep spec) and `Master_Swing_Trading_Plan_v3.md`. Where those were discretionary ("orderly pullback", "first realistic resistance", "RS percentile"), this document makes the call explicit. Change any of these — but on purpose, on in-sample data, validated out-of-sample.
>
> **This spec defines process and execution logic only. It makes no claim of positive expectancy — that is what the backtest is for.** Footprint metrics (§14) are computed in **observe-mode**: logged, not gating, until validated per §16 of the deep spec.

---

## 0. Conventions

- **Decision cadence is daily, end-of-day (EOD).** A signal evaluated on the daily bar dated `t` uses data through `t`'s close only. Actions (entries, stops moved by rule) occur on session **`t+1`** unless a fill convention says otherwise (§8, §13).
- Session dates in **US/Eastern**. "Session" = regular trading day on the exchange calendar.
- **R** = initial dollar risk per share = `entry − stop`. All outcomes in R multiples.
- Booleans are strict unless a tolerance/buffer is named.
- `[OPEN PARAMETER]` = a tunable with a default to be set in-sample. `[DECISION]` = a choice not dictated by the deep spec.
- Two run modes (§17): **Funnel** (live/forward — sequential sector→stock→setup) and **Parallel-tag** (backtest attribution — full universe, sector tier tagged). Both are specified.

---

## 1. Data Requirements

| Series | Granularity | Window | Used for |
|---|---|---|---|
| Target ticker OHLCV | **daily** | trailing ≥ 300 sessions | SMA50/200 + slope, RS, 52-wk high, ADV, ATR, archetype detection, footprint |
| SPY OHLCV | **daily** | trailing ≥ 300 sessions | RS line, regime (rising 200-day), sector-ranking benchmark |
| 11 SPDR sector ETFs OHLCV (XLK XLF XLE XLV XLY XLP XLI XLB XLU XLRE XLC) | **daily** | trailing ≥ 200 sessions | sector RS ranking |
| Point-in-time sector membership (ticker → SPDR sector, per date) | per-date map | full backtest range | sector gate without look-ahead (2018 GICS reshuffle) |
| Earnings dates (historical *reported* + forward calendar) | event list | full range | earnings-window gate |
| SEC dilution filings (424B5 / S-3 / S-1) | filing dates | full range | dilution gate |
| Exchange trading calendar | — | full range | session bounds |

**Hard data rules (point-in-time):**
- Every feature uses **only data ≤ the decision date `t`**. SMA/ATR/RS/sector-rank/footprint are recomputed per `t`; none may reference a future bar.
- **Survivorship:** the candidate universe must include **delisted/merged tickers** as of each historical date. For a sector-ranked, RS-percentile system this is non-optional — omitting it inflates results.
- **Sector membership is point-in-time** (the sector a ticker had *on date `t`*, not today's). The 2018 GICS Communication Services reshuffle moved GOOGL/META/NFLX; today's map is look-ahead.
- Earnings "reported date" used for historical gating must be the **as-known** date, not a restated one.

---

## 2. Derived Series (exact definitions)

All on the daily series, evaluated at `t`.

**Trend.**
```
sma50(t)        = mean(close, 50)
sma200(t)       = mean(close, 200)
sma50_slope(t)  = sma50(t) - sma50(t - slope_lb)        # [OPEN PARAMETER] slope_lb = 10
sma50_rising    = sma50_slope(t) > 0
trend_ok        = close(t) > sma50(t) AND sma50_rising
stage2_pref     = sma50(t) > sma200(t)                  # preferred, not hard
extension(t)    = close(t)/sma50(t) - 1
near_high(t)    = close(t) >= near_high_frac * max(high, 252)   # [OPEN PARAMETER] near_high_frac = 0.80
```

**Relative strength.** `[DECISION]` The deep spec says "RS percentile vs SPY ≥ 70." RS percentile is a **cross-sectional** rank; "vs SPY" denotes the market context. Defined as IBD-style:
```
rs_return(t)    = 0.4*ret(63) + 0.2*ret(126) + 0.2*ret(189) + 0.2*ret(252)   # [OPEN PARAMETER] rs_blend_weights
rs_percentile(t)= cross-sectional percentile rank (0–100) of rs_return(t)
                  across the ELIGIBLE universe (§3) on date t
rs_line(t)      = close(t) / spy_close(t)
rs_line_falling = rs_line(t) < min(rs_line, rs_newlow_lb)       # "making new RS lows"
                  # [OPEN PARAMETER] rs_newlow_lb = 20
rs_ok           = rs_percentile(t) >= rs_floor AND NOT rs_line_falling
                  # [OPEN PARAMETER] rs_floor = 70   (SW-B uses 80)
rs_leads_price  = (rs_line(t) >= max(rs_line, rs_newhigh_lb)) AND
                  (close(t)   <  max(close,   rs_newhigh_lb))   # bonus tell, §14
                  # [OPEN PARAMETER] rs_newhigh_lb = 63
```

**Sector RS ranking (weekly, as-of).** Computed once per week, applied to the days that follow until re-rank.
```
for each sector ETF s:
    rs_ratio_s(lb) = (s_close(t)/s_close(t-lb)) / (spy_close(t)/spy_close(t-lb))
    rs_blend_s     = 0.5*rs_ratio_s(63) + 0.5*rs_ratio_s(126)       # [OPEN PARAMETER] 63/126
    rs_line_s_now  = s_close(t)/spy_close(t)
    rs_line_s_prior= s_close(t-21)/spy_close(t-21)
    sector_rising_s= rs_line_s_now > rs_line_s_prior
sector_rank_s      = rank of rs_blend_s, 1 = strongest
sector_top_third(s)= (sector_rank_s <= sector_top_n) AND sector_rising_s
                     # [OPEN PARAMETER] sector_top_n = 4   (top-third of 11)
sector_tier(s)     = "top" if rank<=4 else "middle" if rank<=8 else "bottom"
```
`[OPEN PARAMETER] sector_rerank_freq = "weekly"` (re-rank each weekend; carry forward intra-week). Top rank decays in ~21–47 sessions — do not re-rank daily.

**Volume / ATR.**
```
vol20(t) = mean(volume, 20) ; vol50(t) = mean(volume, 50)
adv20(t) = mean(volume, 20)               # liquidity screen
atr_d(t) = ATR(14) on daily
```

**Footprint features** — defined in §14 (observe-mode).

---

## 3. Universe / Candidate Selection (mechanical screen)

```
eligible(ticker, t) =
       adv20(t)     >= adv_min            # [OPEN PARAMETER] adv_min = 1_000_000 shares
   AND close(t)     >= price_min          # [OPEN PARAMETER] price_min = $5
   AND has_min_history(ticker, t, 252)    # enough bars for RS/52wk
```
The eligible set is the cross-section used to compute `rs_percentile` (§2). Special-situations/small-cap bucket is out of scope for v1 `[DECISION]` (separate, stricter parameters in the deep spec).

---

## 4. Regime State (Stage 0 — compute once per day)

```
index_uptrend   = spy_close(t) > sma200_spy(t) AND sma200_spy_rising(t)
index_dist_days = distribution_days(SPY, t)               # §14
regime_mult     = regime_size_multiplier(index_dist_days) # §14, OBSERVE-MODE (logged, not applied by default)
regime_ok       = index_uptrend                           # [DECISION] hard regime gate = SPY in uptrend
```
`[OPEN PARAMETER] regime_action ∈ {"gate","scale","observe"}; default "gate"` — if `"gate"`, `regime_ok==False` ⇒ no new entries that day; if `"scale"`, multiply `risk_pct` by `regime_mult`; if `"observe"`, log only.

---

## 5. Hard Gates (pre-filters — if ANY fails, NO TRADE regardless of score)

Evaluated at the daily close of the candidate bar `t`:

1. `regime_ok` per §4 (subject to `regime_action`).
2. `trend_ok`  : `close > rising sma50`.  *(Falling 50 SMA ⇒ hard skip — the 52-wk-low trap.)*
3. `rs_ok`     : `rs_percentile >= 70 AND NOT rs_line_falling`.
4. `sector_top_third(sector(ticker,t))` is True. *(Bottom-third / falling sector RS ⇒ NO TRADE.)*
5. `extension(t) <= ext_max`     # [OPEN PARAMETER] ext_max = 0.30  (not >30% above 50 SMA)
6. `near_high(t)` is True        # within ~20% of 52-wk high
7. `no_dilution(ticker, t, 60)`  # no 424B5/S-3/S-1 in trailing 60 calendar days
8. `no_earnings(ticker, t, earn_block)`  # [OPEN PARAMETER] earn_block = 5 sessions either side
9. Not blocked by portfolio limits (§12).

> Gates 2, 3, 4 are also confirmation items (C1/C4/C5 in §6) — they are *both* hard floors and scored. The deep spec marks trend (1) and sector (5) non-negotiable; this spec additionally hard-gates RS, extension, near-high, dilution, and earnings because §9 of the deep spec lists each as a do-not-trade. `[DECISION]`

---

## 6. Archetype Detection (the trigger) — pick the FIRST that fires at close of `t`

The trigger encodes "structure + volume." `ref_ma` is the moving average the setup is built around `[OPEN PARAMETER] ref_ma ∈ {sma20,sma50,sma200}; default sma50`.

**Archetype A — Trend Pullback (reclaim).**
```
# 1) a pullback into the rising ref_ma occurred in the last pb_window sessions
pulled_back   = min(low, pb_window) <= ref_ma(t) * (1 + touch_tol)   # touched the MA
              # [OPEN PARAMETER] pb_window = 10, touch_tol = 0.01
# 2) orderly: volume + range contracted into the dip, no heavy gap-down
vol_contract  = mean(volume over the dip leg) < mean(volume over the prior up-leg)   # [DECISION]
no_heavy_gapdn= NOT any(down_day AND gap_down AND volume > climax_mult*vol20 in dip) # [OPEN PARAMETER] climax_mult = 3.0
# 3) reclaim trigger bar (today): green close back above ref_ma on expanding volume
reclaim       = (close(t) > open(t)) AND (close(t) > ref_ma(t)) AND
                (volume(t) >= vol_mult * vol20(t))                  # [OPEN PARAMETER] vol_mult = 1.5
archetype_A   = pulled_back AND vol_contract AND no_heavy_gapdn AND reclaim
touch_count   = # of distinct ref_ma touches since the current advance began   # logged (1st/2nd preferred)
```
> "Never buy the down day" is enforced by `close>open` on the trigger bar. `[DECISION]` `vol_contract`/`no_heavy_gapdn` operationalize "orderly pullback."

**Archetype B — Base Breakout.**
```
pivot(t)      = max(high over [t - base_window, t-1])               # [OPEN PARAMETER] base_window = 20
base_tight    = (max(high,base_window) - min(low,base_window)) / pivot(t) <= base_max_depth
              # [OPEN PARAMETER] base_max_depth = 0.15  [DECISION] "tight base"
vdu_in_base   = vdu_present(base slice)                              # §14 — bonus quality (logged)
breakout      = (close(t) > pivot(t) * (1 + break_buf)) AND (volume(t) >= vol_mult * vol20(t))
              # [OPEN PARAMETER] break_buf = 0.0
archetype_B   = base_tight AND breakout
```

```
trigger = "A" if archetype_A else ("B" if archetype_B else None)
At most one trigger per ticker per day; A takes precedence if both fire [DECISION].
```

> **Mechanized-proxy caveat.** `archetype_A`/`archetype_B` are strict proxies of a discretionary read. Expect false positives/negatives; the forward/paper test validates the real pattern. Treat divergence as data.

---

## 7. Confirmation Score → Grade → Risk

Six booleans at close of `t` (some duplicate hard gates — that is intentional, for grading):
```
C1 = trend_ok                                   # also Hard Gate 2
C2 = (trigger is not None)                       # structure (archetype present)
C3 = (volume(t) >= vol_mult * vol20(t))          # volume expansion on trigger bar
C4 = rs_ok                                       # also Hard Gate 3
C5 = sector_top_third(sector)                    # also Hard Gate 4
C6 = momentum_ok                                 # confirmation only (below)
momentum_ok = (rsi14(t) >= rsi_floor) AND (rsi14(t) > rsi14(t-1)) AND
              (macd_hist(t) > macd_hist(t-1))     # [OPEN PARAMETER] rsi_floor = 40
score      = C1+C2+C3+C4+C5+C6
tradeable  = (all Hard Gates §5 pass) AND (trigger is not None) AND (score >= 4)
grade      = "A+" if (score >= 5 AND sector_top_third) else ("A" if score == 4 else "pass")
```
**Risk tier → risk_pct** (deep spec §5; A+ capped at 0.75% until 50+ live trades):
```
risk_pct = {"A+": 0.0075, "A": 0.0050, "B": 0.0025}[tier_of(grade)]   # [OPEN PARAMETER]
# B tier (score==4 AND sector middle-third) optional; default skip B  [DECISION] trade_B = False
```

---

## 8. Entry Model & Fill

`[OPEN PARAMETER] entry_model ∈ {"next_open","retest"}; default "next_open"`.

**next_open (default):**
```
no_chase = next_open(t+1) <= trigger_close(t) * (1 + chase_pct)     # [OPEN PARAMETER] chase_pct = 0.03
if no_chase: ENTRY at open(t+1) + slippage
else:        NO TRADE (or hand to retest model)
```
**retest (optional, tighter risk):** after the breakout/reclaim, wait up to `retest_max_days` for a pullback to the trigger level (`ref_ma` for A, `pivot` for B) that **holds** (close back above it), enter at the next open. `[OPEN PARAMETER] retest_max_days = 5`.

`[DECISION]` Entering on `t+1` open (not the signal-bar close) avoids using the signal bar's own close as the fill.

---

## 9. Stop, Risk/Share, Position Size

```
# Archetype A:
swing_low_A = min(low over the pullback leg)
raw_stop_A  = min(swing_low_A, ref_ma(t) - stop_buf_atr*atr_d(t))
# Archetype B:
base_low_B  = min(low over [t-base_window, t])
raw_stop_B  = base_low_B - stop_buf_atr*atr_d(t)        # or pivot - buffer if base_low far
stop_buf_atr = 0.10                                     # [OPEN PARAMETER]

stop            = raw_stop_A or raw_stop_B
risk_per_share  = entry - stop
if risk_per_share < min_risk_atr * atr_d(t):  NO TRADE  # [OPEN PARAMETER] min_risk_atr = 0.25  [DECISION]

dollar_risk = equity_base * risk_pct * (regime_mult if regime_action=="scale" else 1.0)
              # [DECISION] fixed equity_base (no compounding) for clean R; set compound=True to compound
shares      = floor(dollar_risk / risk_per_share)       # round DOWN (deep spec)
shares      = min(shares, floor(adv_participation * adv20(t)))   # [OPEN PARAMETER] adv_participation = 0.01
if shares == 0: NO TRADE
```
**Never widen the stop.** If structure demands a wider stop, share count already absorbs it (R held constant).

---

## 10. Targets, Partials, Trailing, Time Stop

```
R = risk_per_share
# ≥2R gate at entry (deep spec hard rule):
resistance = first prior swing high above entry within res_lookback, ELSE measured_move
             # [OPEN PARAMETER] res_lookback = 120 ; [DECISION] swing high = pivot(res_pivot_n) high
measured_move = entry + (pivot - base_low_B)            # archetype B base height; A uses prior swing high
if (resistance - entry) / R < 2.0:  NO TRADE            # fails the ≥2R gate

# Partial: none before +1.5R unless price runs into resistance first
partial_R   = 2.0 ; partial_frac = 0.0 (baseline)       # [OPEN PARAMETER] default no partial
# optional: partial_frac = 0.25–0.50 at +2R into resistance/earnings window

# Trailing (runner): under confirmed daily swing (pivot) lows OR 20 EMA, whichever named
trail_mode  = "pivot"                                   # [OPEN PARAMETER] {"pivot","ema20"}
pivot_n     = 1                                         # bar is a pivot low if low <= lows of pivot_n bars each side
                                                        # CONFIRMED only at i+pivot_n (no look-ahead)
trail_stop  = max(trail_stop, last_confirmed_pivot_low - stop_buf_atr*atr_d)   # monotonic up

# Time stop:
time_stop_days = 8                                      # [OPEN PARAMETER] deep spec: 5–10
progress_R     = 0.5                                    # [OPEN PARAMETER] [DECISION] "no favorable progress" = MFE_R < 0.5
at t_entry + time_stop_days: if MFE_R < progress_R ⇒ exit at close
```

---

## 11. Exit Rules (evaluated each daily close while in position)

1. **Stop / target fills** per §13 fill rules.
2. **Trend break:** `close < ref_ma(t)` on `volume >= vol_mult*vol20` **OR** a confirmed lower swing low ⇒ exit at close. `[OPEN PARAMETER] trend_break_on_volume = True`.
3. **Archetype-A failure:** entered via A and `close < ref_ma` the session after entry with no recovery within `fail_grace` sessions ⇒ exit. `[OPEN PARAMETER] fail_grace = 2`.
4. **Archetype-B failure:** entered via B and `close < pivot` (back inside the base) ⇒ exit.
5. **Time stop** (§10).
6. **Distribution warning (observe-mode):** `stock_dist_cluster >= stock_dist_cluster_warn` while held, or `ud_volume_ratio < 1.0` ⇒ **log a caution flag**; do **not** auto-exit until validated (§14).
7. **Circuit breakers** (§12) gate *new* entries, not open positions.

Runner exits at the **first** of: target/resistance limit, trail stop, an exit rule above.

---

## 12. Session / Portfolio Constraints

```
max_positions     = 8        # [OPEN PARAMETER] deep spec: 3–8
max_portfolio_heat= 0.030    # sum of open R at current stops <= 3.0% equity; block new entry if exceeded
max_sector_heat   = 0.015    # per SPDR sector
loss_streak_pause = 3        # 3 consecutive losers -> pause NEW entries 3 sessions
weekly_stop_R     = -3.0     # week P&L <= -3R -> stop new entries until next week
rule_violation    = "pause_week"   # stop new entries rest of week on any rule break
```
When `max_portfolio_heat` or `max_sector_heat` would be exceeded by a new entry, **skip** the entry (do not resize below grade) `[DECISION]`.

---

## 13. Costs & Fill Assumptions `[DECISION]`

- **Entries:** `open(t+1) + slippage` (adverse).
- **Stops:** if a daily `low <= stop` ⇒ filled at `min(open, stop) − slippage` (gap-through handled).
- **Targets/partials/resistance:** if `high >= level` ⇒ filled at `level` (limit).
- **Same-bar stop & target:** assume **stop first** (conservative).
- `slippage [OPEN PARAMETER] = $0.03` (deep spec $0.02–0.05). `commission [OPEN PARAMETER] = broker`.
- **25% paper-to-live haircut** is a *projection applied to aggregate expectancy* (deep spec §11), **not** a per-trade cost. Do not double-count it inside the backtest.

---

## 14. Footprint Instrumentation (OBSERVE-MODE — computed & logged, NOT gating)

Mirror of deep spec §9A. All features use data ≤ `t`. **Default action = record.** Promotion to a gate/posture requires the §17 parallel-tag validation.

```
def distribution_days(df, down_pct=0.002, window=25):       # index or stock
    chg = df.close.pct_change(); hv = df.volume > df.volume.shift(1)
    return int(((chg <= -down_pct) & hv).tail(window).sum())

def ud_volume_ratio(df, lookback=50):
    w = df.tail(lookback); up = w.close > w.close.shift(1)
    dn = w.loc[~up,"volume"].sum()
    return float("inf") if dn==0 else w.loc[up,"volume"].sum()/dn

def vdu_present(base, pct=0.50, avg_window=50):
    avg = base.volume.rolling(avg_window).mean()
    return bool((base.volume <= pct*avg).tail(len(base)).any())

def regime_size_multiplier(index_df):                       # logged, applied only if regime_action=="scale"
    d = distribution_days(index_df)
    return 1.0 if d<=3 else (0.5 if d<=5 else 0.0)
```
| Parameter | Default | Mode |
|---|---|---|
| `dist_down_pct` | 0.002 (0.20%) | regime input / observe (stock) |
| `dist_window` | 25 | — |
| `index_dist_cluster_riskoff` | 5 (test 4–6) | observe → regime posture |
| `stock_dist_cluster_warn` | 4 | observe (exit flag) |
| `ud_lookback` / `ud_strong` | 50 / 1.75 | observe |
| `vdu_pct` / `vdu_avg_window` | 0.50 / 50 | observe (Archetype-B bonus) |
| `rs_newhigh_lookback` | 63 | observe (bonus tell) |

---

## 15. Look-Ahead / Determinism Audit

| Quantity | Past/known only? | Mechanism |
|---|---|---|
| SMA50/200 + slope, ATR | yes | trailing windows to `t` |
| RS percentile | yes | cross-section of eligible set, returns to `t` |
| RS line / leads-price | yes | close & SPY to `t`; `max` over trailing window |
| Sector rank | yes | as-of weekly rank, data ≤ `t`, **point-in-time membership** |
| Archetype A/B detection | yes | completed bars ≤ `t` |
| Footprint features | yes | trailing windows to `t` |
| Entry fill | yes | `open(t+1)` |
| Stop/target intrabar | conservative | stop-before-target |
| Trailing pivot | yes | pivot confirmed at `i+pivot_n` lag |
| Earnings/dilution gate | yes | as-known dates only |

If any future-dated value enters a decision, the backtest is invalid. Re-audit after any code change.

---

## 16. Open Parameters — Master Table

> These are your degrees of freedom. Testing many combinations on the same data **is** overfitting. Set defaults, tune **in-sample only**, confirm on **untouched out-of-sample**, then **walk-forward**. Each tuned knob is a multiple-comparisons cost.

| Param | Default | Section |
|---|---|---|
| slope_lb | 10 | §2 |
| near_high_frac | 0.80 | §2 |
| rs_blend_weights | 0.4/0.2/0.2/0.2 (63/126/189/252) | §2 |
| **rs_floor** | 70 | §2/§5 (gates every trade) |
| rs_newlow_lb / rs_newhigh_lb | 20 / 63 | §2 |
| sector_top_n / sector_rerank_freq | 4 / weekly | §2 |
| adv_min / price_min | 1M / $5 | §3 |
| regime_action | gate | §4 |
| ext_max | 0.30 | §5 |
| earn_block | 5 sessions | §5 |
| ref_ma | sma50 | §6 |
| pb_window / touch_tol | 10 / 0.01 | §6 |
| climax_mult | 3.0 | §6 |
| **vol_mult** | 1.5 | §6/§7 |
| base_window / base_max_depth / break_buf | 20 / 0.15 / 0.0 | §6 |
| rsi_floor | 40 | §7 |
| trade_B | False | §7 |
| risk_pct (A+/A/B) | 0.0075 / 0.0050 / 0.0025 | §7 |
| entry_model / chase_pct / retest_max_days | next_open / 0.03 / 5 | §8 |
| stop_buf_atr / min_risk_atr | 0.10 / 0.25 | §9 |
| adv_participation | 0.01 | §9 |
| res_lookback / partial_R / partial_frac | 120 / 2.0 / 0.0 | §10 |
| trail_mode / pivot_n | pivot / 1 | §10 |
| time_stop_days / progress_R | 8 / 0.5 | §10 |
| fail_grace / trend_break_on_volume | 2 / True | §11 |
| max_positions / heat / sector_heat | 8 / 0.030 / 0.015 | §12 |
| loss_streak_pause / weekly_stop_R | 3 / −3.0 | §12 |
| slippage / commission | $0.03 / broker | §13 |
| footprint params | see §14 | §14 |

---

## 17. Evaluation Pseudocode

```python
sectors_ranked = {}   # refreshed weekly
for day in trading_days:
    if is_weekend_rerank(day):
        sectors_ranked = rank_sectors(sector_px, spy, asof=day)     # §2
    regime = regime_state(spy, day)                                  # §4
    universe = [tk for tk in all_tickers if eligible(tk, day)]       # §3
    rs_pct = cross_sectional_rs_percentile(universe, day)            # §2

    # ---- FUNNEL mode (live/forward): only stocks in strong sectors ----
    strong = [s for s in SPDR if sectors_ranked.top_third(s)]
    cands  = [tk for tk in universe if sector(tk,day) in strong]

    for tk in cands:
        df = load_daily(tk, day)
        if not all_hard_gates(tk, df, regime, rs_pct, sectors_ranked, day):  # §4,§5
            continue
        trig = detect_archetype(df, day)                             # §6
        if trig is None: continue
        score, grade = score_and_grade(df, trig, rs_pct, sectors_ranked, day) # §7
        if grade == "pass": continue
        if portfolio_blocked(day, sector(tk,day)): continue          # §12
        entry = entry_fill(tk, day, trig)                            # §8  (open of day+1)
        if entry is None: continue                                   # no-chase / retest fail
        trade = open_trade(entry, df, trig, grade)                   # §9,§10  (incl. ≥2R gate)
        if trade is None: continue                                   # min-risk / 2R / shares==0
        register(trade)

    manage_open_positions(day)                                       # §11,§13 (stops/targets/trails/time)
    update_portfolio_stats(day)                                      # §12

# ---- PARALLEL-TAG mode (backtest attribution): identical, but DO NOT pre-filter by sector;
#      run detect_archetype on the full eligible universe and TAG sector_tier on each trade
#      so realized expectancy can be split by tier (and by footprint bucket). §14 of deep spec.
```

---

## 18. Trade-Log Output Schema (maps to deep spec §13 journal)

`date, ticker, sector_etf, sector_rank, sector_tier, archetype, grade, score, C1..C6, trend_ok, rs_percentile, rs_line_falling, rs_leads_price, touch_count, ref_ma, extension, near_high, vol_mult_at_trigger, entry_model, entry_date, entry, stop, init_risk_per_share, shares, risk_pct, regime_uptrend, index_dist_days, regime_mult_logged, ud_volume_ratio, vdu_present, stock_dist_count, planned_R, target_resistance, partial_filled, exit_date, exit_price, exit_reason, R_realized, MAE_R, MFE_R, notes`

`exit_reason ∈ {target_resistance, trail_stop, stop, trend_break, archetypeA_fail, archetypeB_fail, time_stop}`

---

## Appendix A — Decisions Where the Deep Spec Was Silent/Discretionary

1. **RS percentile** defined as IBD-style cross-sectional rank of a 63/126/189/252 blended return over the eligible universe; "vs SPY" read as market context, with `rs_line=close/spy` used separately for the new-low / leads-price checks (§2).
2. **"Orderly pullback"** operationalized as volume-contraction into the dip + no heavy-volume gap-down + green reclaim bar (§6).
3. **"Tight base"** operationalized as base range ≤ `base_max_depth` of pivot; pivot = trailing base-window high (§6).
4. **RS, extension, near-high, dilution, earnings** promoted to hard gates because the deep spec §9 lists each as a do-not-trade (§5).
5. **"First realistic resistance / ≥2R"** operationalized as nearest prior swing high within `res_lookback`, else measured move; entry rejected if < 2R (§10).
6. **"No favorable progress"** time-stop defined as `MFE_R < 0.5` at `time_stop_days` (§10).
7. **Entry fill** = `open(t+1)`; `next_open` default with no-chase guard; retest optional (§8).
8. **Sizing** = fixed equity base (no compounding) for clean R; B-tier skipped by default (§7,§9).
9. **Same-bar stop/target** resolved stop-first (§13).
10. **Footprint metrics** computed but observe-mode; `regime_action="gate"` (SPY-uptrend hard gate) with `scale`/`observe` alternatives (§4,§14).

## Appendix B — Parallel-Tag Attribution Harness

To prove the **sector gate** (and any footprint metric) adds expectancy rather than just cutting trade count:
- Run §6–§10 on the **full eligible universe** (skip Hard Gate 4), tagging `sector_tier` and each footprint bucket on every resulting trade.
- `groupby(sector_tier)` and compare realized expectancy after costs + 25% haircut. If `top` does not out-expectancy `middle`/`bottom` by a margin surviving walk-forward, **drop the gate**.
- Repeat per footprint metric (distribution-day cluster, U/D ratio, VDU). Promote observe→gate only on a positive, walk-forward-stable result.

---

*Educational/operational specification only. Not investment advice. This document defines process and execution logic; it makes no claim that the strategy has positive expectancy — that is what the backtest is for.*
