# Day 5: 1099-R Box 7 sanity checker — Week 1 consolidation
# Uses: constants, input loop, try/except, if/elif, f-strings.
# (Box 7 = the distribution code on Form 1099-R. You explain these codes
# at work; today your program does.)

print("=" * 50)  # strings can be multiplied — instant divider
print("1099-R BOX 7 SANITY CHECKER - v0.1")

while True:
    code = input("\nEnter a Box 7 code (or q to quit): ").strip().upper()
    # .strip() removes accidental spaces; .upper() normalizes '7 ' → '7'.
    # Cleaning input BEFORE using it: boundary habit, every time.

    if code == "Q":
        break

    # elif chain today; next week a dictionary makes this elegant —
    # feeling the clunky version FIRST is how you'll appreciate the fix.
    if code == "1":
        meaning = "Early distribution, no known exception (under 59½)"
        watch = "10% early-withdrawal penalty likely applies"
    elif code == "2":
        meaning = "Early distribution, exception applies"
        watch = "Verify the exception is documented"
    elif code == "7":
        meaning = "Normal distribution"
        watch = "Confirm participant is 59½+"
    elif code == "G":
        meaning = "Direct rollover"
        watch = "Should be non-taxable — gross vs taxable amounts must differ"
    else:
        print(f"  ❓ Code {code!r} not in this checker yet - add it! (That's the exercise.)")
        continue

    print(f"  Code {code}: {meaning}")
    print(f"  ⚠️  Check: {watch}")
