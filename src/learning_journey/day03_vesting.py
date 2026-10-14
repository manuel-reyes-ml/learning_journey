# Day 3: Vesting schedule checker — multi-branch decisions
# New concepts: elif chains, comparison chaining, why branch ORDER matters

years_of_service = 4
schedule_type = "graded"  # "cliff" (3-yr) or "graded" (2-6 yr)

# --- ELIF: check conditions top to bottom, take the FIRST true branch ---
if schedule_type == "cliff":
    # == asks "equal?" (one = assigns, two == compares — classic beginner trap)
    vested_pct = (
        1.0 if years_of_service >= 3 else 0.0
    )  # 100% — cliff means all-or-nothing at 3 years


elif schedule_type == "graded":
    # 6-year graded: 0% <2yrs, then 20% per year from year 2, 100% at 6.
    # ORDER MATTERS: we check the highest tier first, because the first
    # true condition wins. If we checked >= 2 first, a 6-year employee
    # would wrongly stop at 20%.
    if years_of_service >= 6:
        vested_pct = 1.0
    elif years_of_service >= 2:
        vested_pct = 0.20 * (years_of_service - 1)
    else:
        vested_pct = 0.0

else:
    # Defensive branch: if data is bad, SAY SO loudly instead of guessing.
    # Silent wrong answers are the cardinal sin of financial software.
    print(f"❌ Unknown schedule type: {schedule_type!r}")  # !r shows quotes → reveals typos
    vested_pct = None

if vested_pct is not None:
    print(f"{schedule_type} schedule, {years_of_service} yrs → {vested_pct:.0%} vested")
