# Day 4: try/except — programs that survive bad input
# Monday, typing "abc" as a salary crashed the program with ValueError.
# Production code NEVER crashes on user input. It anticipates, catches, recovers.

# --- WHILE LOOP + TRY/EXCEPT: ask until we get a valid answer ---

while True:  # loop forever... until `break` exits it
    salary_text = input("Enter annual salary (or q to quit): ").strip().lower()

    if salary_text == "q":  # .lower() → accepts q or Q
        print("Goobye!")
        break  # break = leave the loop immediately

    try:
        # The RISKY line goes inside try:
        salary = float(salary_text)
    except ValueError:
        # If float() fails, Python "raises" ValueError. Instead of crashing,
        # control jumps HERE. We explain, then the loop asks again.
        print(f"  '{salary_text}' is not a number - try again (e.g., 85000).")
        continue  # continue = skip to the next loop round

    # Catching the error is not enough — VALIDATE the business rule too.
    # -50000 is a valid float and an invalid salary.
    if salary <= 0:
        print("  Salary must be positive.")
        continue

    print(f"  ✅ ${salary:,.2f} accepted.")
    break

# Rule of thumb you now own: try/except for things that can FAIL,
# if-checks for things that can be WRONG. Both, always, at every boundary
# where data enters a system. (DataVault will live and die by this rule.)
