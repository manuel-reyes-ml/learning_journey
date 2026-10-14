# Day 1: My first Python program
# Manuel Reyes — Learning Journey (Roadmap v10.0, Stage 1)
#
# Theme: a 401(k) contribution calculator — because every exercise in this
# journey runs on retirement-plan data. Domain + code = the moat.

# --- PRINT: making the program talk ---
# print() sends text to the screen. Text in quotes is called a "string".
print("Day 1 - Manuel's 401(k) contribution calculator")

# --- VARIABLES: named boxes that hold values ---
# A variable is created the moment you assign to it with =
# Naming rule (production habit #1): full descriptive words, lowercase_with_underscores.
# BAD:  s = 85000        (what is s?)
# GOOD:
annual_salary = 85_000  # Python lets you write 85_000 for readability — same as 85000
deferral_rate = 0.06  # 6% — rates are stored as decimals, not percents

# --- TYPES: every value has a kind ---
# 85_000 is an int (whole number). 0.06 is a float (decimal).
# "Day 1..." is a str (text). Python tracks this for you, but YOU should know it too.
print(type(annual_salary))  # <class 'int'>   — try it, then delete this line
print(type(deferral_rate))  # <class 'float'>

# --- CALCULATION ---
annual_contribution = annual_salary * deferral_rate

# --- F-STRINGS: putting values inside text ---
# f"..." lets you embed variables with {curly_braces}.
# :,.2f  is a format spec: thousands separator, 2 decimal places.
# This is THE way to print money in Python.
print(f"Salary: ${annual_salary:,.2f}")
print(f"Deferral rate: {deferral_rate:.1%}")  # .1% formats 0.06 as 6.0%
print(f"Annual contribution: ${annual_contribution:,.2f}")

# --- INPUT: making it interactive ---
# input() pauses and waits for the user to type. It ALWAYS returns a string,
# so we convert ("cast") it to float before doing math. This str→number
# conversion is the #1 beginner stumble — meet it on purpose today.
user_salary_text = input("\nEnter a salary to try: ").strip()
user_salary = float(user_salary_text)
user_contribution = user_salary * deferral_rate
print(f"At {deferral_rate:.0%}, that salary contributions ${user_contribution:,.2f}/year")
