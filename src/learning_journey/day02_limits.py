# Day 2: Contribution limits & catch-up — first taste of DECISIONS in code
# New concepts: constants, comparison operators, if-statements (preview), min()

# --- CONSTANTS: values that never change while the program runs ---
# Convention: ALL_CAPS names. Production habit #2: no "magic numbers" buried
# in calculations — name them at the top, once, where they're easy to verify.
IRS_DEFERRAL_LIMIT = 23_500  # TODO: verify current-year IRS 402(g) limit
CATCH_UP_LIMIT = 7_500  # TODO: verify current-year catch-up amount
CATCH_UP_AGE = 50
# Those TODOs are deliberate: honesty over guessing. In regulated finance,
# an unverified number labeled as fact is a compliance problem. Same rule
# as your roadmap: unverified figures get flagged, not stated.

annual_salary = 120_000
deferral_rate = 0.25  # aggressive saver — will they hit the cap?
age = 45

# --- COMPARISON OPERATORS produce True/False (a "bool" type) ---
is_catch_up_eligible = age >= CATCH_UP_AGE  # >= means "greater than or equal"
print(f"Age {age} → catch-up eligible: {is_catch_up_eligible}")

# --- IF/ELSE: the program chooses a path ---
# Indentation (4 spaces) is not decoration in Python — it defines which
# lines belong to which branch. Cursor/VS Code + Ruff keep this tidy for you.
if is_catch_up_eligible:
    effective_limit = IRS_DEFERRAL_LIMIT + CATCH_UP_LIMIT
else:
    effective_limit = IRS_DEFERRAL_LIMIT

requested = annual_salary * deferral_rate

# --- min(): built-in that returns the smaller value ---
# The actual contribution is the requested amount, CAPPED at the limit.
# One line of business rule — exactly what plan administration does daily.
actual = min(requested, effective_limit)

print(f"Requested deferral:  ${requested:,.2f}")
print(f"Effective limit:     ${effective_limit:,.2f}")
print(f"Actual contribution: ${actual:,.2f}")

if requested > effective_limit:
    excess = requested - effective_limit
    print(f"⚠️  Deferral request exceeds limit by ${excess:,.2f} - capped.")
