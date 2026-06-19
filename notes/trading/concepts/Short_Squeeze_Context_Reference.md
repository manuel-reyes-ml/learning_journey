# SHORT SQUEEZE — TRADING CONTEXT REFERENCE

*Conceptual note. What a short squeeze is, the mechanics that drive it, the metrics that gauge it, and why it is never a standalone signal. This is the "why" layer — the metrics here become a tested trigger (AFC T6) only after they earn it.*

> **One-line framing:** Short interest is a reservoir of **obligated future buying**. A squeeze is what happens when a catalyst forces that buying out all at once into a supply too small to absorb it. The metrics measure how much fuel is loaded; they do **not** tell you it will ignite.

---

## 1. The core mechanic — a short is forced future buying

- To short a stock you **borrow** shares, **sell** them now, and are obligated to **buy them back** later to return them. That buy-back is not optional — it is a deferred purchase that *will* happen.
- So every share of short interest is a **pending buy order that hasn't fired yet.** Unlike a bearish trader who simply doesn't own the stock (and creates no obligation), a short seller has manufactured a guaranteed future buyer: themselves.
- The buying becomes **forced** when price rises against the short: mounting losses (a short's loss is unbounded as price climbs), a broker **margin call**, or the lender **recalling** the borrowed shares (a "buy-in"). Any of these compels a buy *now, at market, at any price.*

## 2. The "fuel in the tank" model

- **Fuel** = the stockpile of obligated, latent buy orders sitting in the short interest.
- **Spark** = a catalyst (news, insider buy, attention spike, volume surge) that starts price rising and pressures shorts.
- **Combustion** = forced covering: shorts buy → price rises → more shorts forced to cover → price rises more (self-reinforcing).
- **Container size** = the **float**. A small float is a sealed container — the same combustion produces a violent pressure spike instead of a slow burn.

> Fuel does nothing on its own. It can sit for months. The squeeze is the *ignition*, not the fuel.

## 3. The metrics (three distinct quantities)

**Raw inputs:**
- **Short interest** = shares sold short and not yet covered. Reported by FINRA **twice a month**, aggregate per security, lagged (settlement + reporting — often ~1–2 weeks stale).
- **Float** = shares outstanding − closely-held/restricted (insiders, control holders, lock-ups). The *tradable* supply. The correct denominator for squeeze math, because locked-up shares can't be bought to cover.

| Metric | Formula | What it covers | Read |
|---|---|---|---|
| **`pct_float_short`** | `shares_short / float` | **Supply pressure** — how much of the tradable supply is obligated future buying (the fuel) | <5% quiet · 10–20% elevated · >20–30% squeeze-prone *(heuristic, unvalidated)* |
| **`days_to_cover`** *(= "short interest ratio")* | `shares_short / avg_daily_volume` | **Time pressure** — days of normal volume needed for all shorts to cover; a narrow exit | <1 easy · 5–10+ congested exit *(heuristic)* |
| **`float_turnover`** | `daily_volume / float` | **Velocity** — how fast the whole float changes hands; the real-time "is it igniting now" tell | 1.0 = entire float traded in a day = extreme activity |

> **Naming discipline:** "short interest ratio" and "days to cover" are the **same calculation**. Use one name (`days_to_cover`). `pct_float_short` and `float_turnover` are genuinely distinct. So there are **three** quantities, not four.
>
> **Freshness:** the two short-based metrics are only as current as the bi-monthly short-interest report (up to ~2 weeks stale). `float_turnover` uses live volume, so it is the most current of the three — which is why it earns its place beside the others.

## 4. Why the denominator decides everything

Same absolute short interest, opposite outcomes — only the float changed:

| | Float | Shares short | `pct_float_short` | Outcome on a catalyst |
|---|---|---|---|---|
| **Stock A** | 10M | 3M | **30%** | Forced buying = 30% of all tradable supply chasing a shrinking pool of sellers → violent spike |
| **Stock B** | 100M | 3M | **3%** | Same 3M shares absorbed without a flinch → no squeeze |

This is why `pct_float_short` (not raw short interest) is the gauge, and why squeezes are a **low-float / micro-cap** phenomenon.

## 5. Squeeze setup — the conditions (none sufficient alone)

A squeeze needs **all** of:
1. **Fuel** — high `pct_float_short` (large obligated buying relative to float).
2. **A small container** — low float (small denominator amplifies the move).
3. **A congested exit** — high `days_to_cover` (shorts can't cover quietly).
4. **A spark** — a catalyst that starts price rising and pressures shorts.
5. **Ignition tell** — `float_turnover` / volume spiking = it may be underway *now*.

Conditions 1–3 are *loaded* (potential). 4–5 are *live* (kinetic). The loaded state can persist indefinitely; only the spark converts it.

## 6. Critical caveats — why this fails and why it's never standalone

- **Shorts are often right.** A stock is frequently heavily shorted for a real reason (deteriorating fundamentals, dilution, fraud). The position never squeezes — it just grinds lower and the shorts win. High `pct_float_short` is *not* bullish by itself.
- **Fuel ≠ ignition.** Without a catalyst, the metrics predict nothing. The signal is the *combination*, not the short interest.
- **Data lag.** Short interest is up to ~2 weeks stale; against a short (e.g., 3-day) horizon that is a real weakness to measure, not wave away. *(Per-institution short data is not public — SEC Form SHO is delayed to 2028 and is aggregate even then; only bi-monthly aggregate short interest is available today.)*
- **Float is not static.** Offerings, lock-up expirations, and dilution change the denominator — re-derive it, don't cache it. (This is exactly where dilution tracking intersects squeeze math.)
- **Double-edged.** Low float amplifies **down** moves too; expect high volatility, wide spreads, gap risk, and pump-and-dump / manipulation exposure in this universe.
- **Squeezes mean-revert hard.** The spike is violent *and* the round-trip is violent. Chasing an extended squeeze is how you become exit liquidity for whoever lit it — the same "don't buy the news-day spike" discipline from the footprint work applies.

## 7. Where this lives in the system

- **Universe:** micro-cap / low-float — **AFC**, not Crucible. Crucible's liquid leaders (ADV ≥ 1M, price ≥ $5) don't squeeze this way.
- **Role:** a **squeeze-context** signal (candidate **AFC T6**), framed as contrarian-bullish potential tied to a catalyst — never "follow the shorts down."
- **Primitives:** `pct_float_short`, `days_to_cover`, `float_turnover` (+ float and short-interest accessors) belong in the shared `signalcore` library; AFC wires them into the trigger. Promote to a live trigger only after walk-forward testing (≥30 signals, bootstrap CI) proves it predicts the move.

---

## Glossary

| Term | Meaning |
|---|---|
| Short interest | Shares sold short and not yet bought back. FINRA, bi-monthly, aggregate, lagged. |
| Float | Tradable supply = shares outstanding − closely-held/restricted shares. |
| `pct_float_short` | Short interest ÷ float. Supply-pressure gauge (the "fuel"). |
| `days_to_cover` | Short interest ÷ avg daily volume. Time-to-exit gauge. (= "short interest ratio".) |
| `float_turnover` | Daily volume ÷ float. Trading-velocity gauge; most current of the three. |
| Buy-in / recall | Lender forcing return of borrowed shares → forced cover. |
| Margin call | Broker demand for more collateral as a short loses → can force a cover. |
| Squeeze | Self-reinforcing forced covering driving price up sharply. |
| Catalyst | The spark (news, insider buy, attention/volume surge) that ignites loaded fuel. |

---

*Educational note only. Not investment advice. Short interest gauges potential, not direction — these metrics are context for a tested signal, never a signal on their own.*
