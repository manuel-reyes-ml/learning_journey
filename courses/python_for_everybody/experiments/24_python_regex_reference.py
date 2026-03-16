"""
python_regex_reference.py
==========================

Personal reference: Python's ``re`` module — regular expressions for
pattern matching, validation, extraction, and text transformation.

Topics covered
--------------
1. What are regular expressions — pattern matching fundamentals
2. re module core functions — search, match, findall, sub, split, compile
3. Pattern syntax — character classes, quantifiers, anchors, groups
4. Match objects — extracting data from matches
5. Greedy vs lazy quantifiers — controlling match length
6. Grouping and capturing — parentheses, named groups, backreferences
7. Flags — case-insensitive, multiline, dotall, verbose
8. re.compile() — pre-compiled patterns for production performance
9. Common pitfalls and gotchas
10. Production patterns from your roadmap

Why this matters for your roadmap
----------------------------------
- Stage 1: Your CS50 Inheritance project uses regex for CLI seed
  validation (NumberPattern class with INT_PATTERN/FLOAT_PATTERN).
  Your 1099 Reconciliation ETL pipeline needs regex for name
  normalization, SSN format validation, and plan ID extraction.
  Data cleaning with pandas uses regex in str.replace(),
  str.extract(), and str.contains() constantly.
- Stage 2: ETL pipelines parse log files, extract timestamps, validate
  email formats, and clean unstructured text. Airflow DAG configs use
  regex for schedule expressions and path patterns.
- Stage 3: ML feature engineering extracts structured features from
  raw text using regex before feeding to models. NLP preprocessing
  (tokenization, stopword patterns) relies heavily on regex.
- Stage 4-5: LLM output parsing, prompt template validation,
  structured output extraction from model responses, and log
  monitoring in production systems all use regex patterns.

How to use this file
---------------------
Run it directly to see all output::

    $ python 24_python_regex_reference.py

Or import individual sections to experiment in a REPL.

References
----------
.. [1] Python re module docs: https://docs.python.org/3/library/re.html
.. [2] Python HOWTO — Regular Expressions: https://docs.python.org/3/howto/regex.html
.. [3] Real Python — Regex in Python: https://realpython.com/regex-python/
.. [4] regex101.com — Interactive regex tester (use Python flavor)
"""

from __future__ import annotations

import re


# =============================================================================
# SECTION 1: WHAT ARE REGULAR EXPRESSIONS
# =============================================================================
#
# A regular expression (regex) is a PATTERN that describes a set of
# strings. Think of it as a search template with wildcards on steroids.
#
# PLAIN STRING SEARCH vs REGEX SEARCH:
# ┌──────────────────────────────────────────────────────────────────┐
# │  Task: Find phone numbers in text                               │
# │                                                                  │
# │  Plain string:                                                   │
# │    "555-1234" in text    → finds ONE exact match                 │
# │                                                                  │
# │  Regex pattern:                                                  │
# │    r"\d{3}-\d{4}"       → finds ANY phone number                │
# │    Matches: "555-1234", "800-9999", "123-4567"                  │
# │                                                                  │
# │  The pattern says: "3 digits, a dash, 4 digits"                 │
# │  It doesn't care WHICH digits — just the SHAPE.                 │
# └──────────────────────────────────────────────────────────────────┘
#
# WHY RAW STRINGS (r"..."):
# ┌──────────────────────────────────────────────────────────────────┐
# │  Python interprets backslashes in normal strings:                │
# │    "\n" = newline,  "\t" = tab,  "\d" = ???                     │
# │                                                                  │
# │  Raw strings (r"...") tell Python: "don't interpret backslashes" │
# │    r"\n" = literal backslash + n (what regex needs)              │
# │    r"\d" = literal backslash + d (regex digit pattern)           │
# │                                                                  │
# │  RULE: Always use raw strings for regex patterns.                │
# │    ❌  re.search("\d+", text)    → may break                    │
# │    ✅  re.search(r"\d+", text)   → always correct               │
# └──────────────────────────────────────────────────────────────────┘
#
# =============================================================================


def section_1_what_are_regex() -> None:
    """
    Demonstrate the difference between plain string search and regex.

    Shows why regex is more powerful than simple string methods
    for pattern-based searching.
    """
    print("=" * 70)
    print("SECTION 1: WHAT ARE REGULAR EXPRESSIONS")
    print("=" * 70)

    text = "Call 555-1234 or 800-9999 for support. Ref #A123."

    # ── Plain string — finds only exact matches ──────────────────
    print("\n── Plain string search ──")
    print(f"  '555-1234' in text: {'555-1234' in text}")   # True
    print(f"  '800-9999' in text: {'800-9999' in text}")   # True
    print(f"  Can't search for 'any phone number' pattern!")

    # ── Regex — finds ANY string matching the pattern ────────────
    print("\n── Regex search ──")
    phones = re.findall(r"\d{3}-\d{4}", text)
    print(f"  Pattern: r'\\d{{3}}-\\d{{4}}'")
    print(f"  Found: {phones}")  # ['555-1234', '800-9999']

    refs = re.findall(r"#[A-Z]\d+", text)
    print(f"  Pattern: r'#[A-Z]\\d+'")
    print(f"  Found: {refs}")    # ['#A123']

    # ── Raw strings vs normal strings ────────────────────────────
    print("\n── Raw strings (why r'...' matters) ──")
    print(f"  Normal: '\\n' = {repr(chr(10))} (newline character)")
    print(f"  Raw:    r'\\n' = {repr(r'\n')} (literal backslash + n)")
    print(f"  Regex needs the literal backslash, so ALWAYS use r'...'")


# =============================================================================
# SECTION 2: re MODULE CORE FUNCTIONS
# =============================================================================
#
# The 're' module provides 7 core functions. Each returns a different
# type and serves a different purpose:
#
# ┌─────────────────────────────────────────────────────────────────┐
# │  FUNCTION           │ RETURNS        │ PURPOSE                  │
# │─────────────────────│────────────────│──────────────────────────│
# │  re.search()        │ Match | None   │ First match ANYWHERE     │
# │  re.match()         │ Match | None   │ Match at START only      │
# │  re.fullmatch()     │ Match | None   │ ENTIRE string must match │
# │  re.findall()       │ list[str]      │ ALL matches as strings   │
# │  re.finditer()      │ Iterator[Match]│ ALL matches as objects   │
# │  re.sub()           │ str            │ Replace matches          │
# │  re.split()         │ list[str]      │ Split at matches         │
# └─────────────────────────────────────────────────────────────────┘
#
# MENTAL MODEL — search vs match vs fullmatch:
# ┌──────────────────────────────────────────────────────────────────┐
# │  Text: "abc 123 def"    Pattern: r"\d+"                         │
# │                                                                  │
# │  re.search()    → Match '123'  (found SOMEWHERE in string)      │
# │  re.match()     → None         (string doesn't START with \d+)  │
# │  re.fullmatch() → None         (entire string isn't ONLY \d+)   │
# │                                                                  │
# │  Text: "123"            Pattern: r"\d+"                         │
# │                                                                  │
# │  re.search()    → Match '123'  ✅                               │
# │  re.match()     → Match '123'  ✅                               │
# │  re.fullmatch() → Match '123'  ✅ (entire string IS digits)     │
# └──────────────────────────────────────────────────────────────────┘
#
# =============================================================================


def section_2_core_functions() -> None:
    """
    Demonstrate all core re module functions with clear examples.

    Each function is shown with both matching and non-matching input
    so you can see exactly what it returns in each case.
    """
    print("\n" + "=" * 70)
    print("SECTION 2: re MODULE CORE FUNCTIONS")
    print("=" * 70)

    text = "Order 1234 shipped. Order 5678 pending. Ref #A99."

    # ── re.search() — first match anywhere ───────────────────────
    print("\n── re.search() — first match ANYWHERE ──")
    result = re.search(r"\d+", text)
    print(f"  Pattern: r'\\d+'  Text: '{text}'")
    print(f"  Result:  {result}")
    # .group() extracts the matched string from the Match object
    print(f"  .group(): '{result.group()}'" if result else "  No match")

    no_match = re.search(r"\d+", "no numbers here")
    print(f"  No match example: {no_match}")  # None

    # ── re.match() — match at the BEGINNING only ────────────────
    print("\n── re.match() — match at START only ──")
    starts_with = re.match(r"\d+", "123 abc")
    doesnt_start = re.match(r"\d+", "abc 123")
    print(f"  '123 abc': {starts_with.group() if starts_with else None}")
    print(f"  'abc 123': {doesnt_start}")  # None — digits aren't at start

    # ── re.fullmatch() — entire string must match ────────────────
    print("\n── re.fullmatch() — ENTIRE string must match ──")
    full_yes = re.fullmatch(r"\d+", "12345")
    full_no = re.fullmatch(r"\d+", "123 abc")
    print(f"  '12345':   {full_yes.group() if full_yes else None}")
    print(f"  '123 abc': {full_no}")  # None — has non-digit chars

    # YOUR INHERITANCE PROJECT uses this pattern:
    # re.compile(r"^\d+$").match(seed) is equivalent to re.fullmatch(r"\d+", seed)
    # fullmatch is cleaner when you don't need a compiled pattern.

    # ── re.findall() — ALL matches as list of strings ────────────
    print("\n── re.findall() — ALL matches as strings ──")
    all_numbers = re.findall(r"\d+", text)
    print(f"  Pattern: r'\\d+'")
    print(f"  Result:  {all_numbers}")  # ['1234', '5678', '99']

    no_matches = re.findall(r"\d+", "no numbers")
    print(f"  No matches: {no_matches}")  # [] (empty list, not None)

    # ── re.finditer() — ALL matches as Match objects ─────────────
    # Use when you need position info, not just the matched text
    print("\n── re.finditer() — ALL matches as Match objects ──")
    for m in re.finditer(r"\d+", text):
        print(f"  '{m.group()}' at position {m.start()}-{m.end()}")

    # ── re.sub() — replace matches ──────────────────────────────
    print("\n── re.sub() — REPLACE matches ──")
    redacted = re.sub(r"\d+", "XXXX", text)
    print(f"  Original: '{text}'")
    print(f"  Redacted: '{redacted}'")

    # sub() with a count limit (replace only first N matches)
    first_only = re.sub(r"\d+", "XXXX", text, count=1)
    print(f"  First only: '{first_only}'")

    # ── re.split() — split at matches ────────────────────────────
    print("\n── re.split() — SPLIT at matches ──")
    parts = re.split(r"\s+", "hello   world  foo")
    print(f"  Split on whitespace: {parts}")

    csv_parts = re.split(r",\s*", "a, b,c,  d")
    print(f"  Split on comma+space: {csv_parts}")


# =============================================================================
# SECTION 3: PATTERN SYNTAX — THE REGEX LANGUAGE
# =============================================================================
#
# Regex has its own mini-language. Here's every symbol you'll need:
#
# CHARACTER CLASSES (what to match):
# ┌──────────────────────────────────────────────────────────────────┐
# │  Pattern │ Matches                  │ Example                   │
# │──────────│──────────────────────────│───────────────────────────│
# │  \d      │ Any digit [0-9]          │ "abc123" → 1, 2, 3       │
# │  \D      │ Any NON-digit            │ "abc123" → a, b, c       │
# │  \w      │ Word char [a-zA-Z0-9_]   │ "hi_2!" → h, i, _, 2    │
# │  \W      │ Any NON-word char        │ "hi_2!" → !              │
# │  \s      │ Whitespace (space/tab/\n)│ "a b\tc" → ' ', '\t'     │
# │  \S      │ Any NON-whitespace       │ "a b"   → a, b           │
# │  .       │ Any char EXCEPT newline  │ "a.b"   → a, ., b        │
# │  [abc]   │ Any one of a, b, c       │ "cat"   → c, a           │
# │  [^abc]  │ Any char EXCEPT a, b, c  │ "cat"   → t              │
# │  [a-z]   │ Range: a through z       │ "Cat1"  → a, t           │
# │  [0-9]   │ Same as \d               │ "ab12"  → 1, 2           │
# └──────────────────────────────────────────────────────────────────┘
#
# QUANTIFIERS (how many to match):
# ┌──────────────────────────────────────────────────────────────────┐
# │  Pattern │ Meaning                  │ Example on "aabbb"        │
# │──────────│──────────────────────────│───────────────────────────│
# │  +       │ One or more              │ r"b+"   → "bbb"          │
# │  *       │ Zero or more             │ r"c*"   → "" (empty)     │
# │  ?       │ Zero or one (optional)   │ r"b?"   → "b" (first)    │
# │  {n}     │ Exactly n times          │ r"b{2}" → "bb"           │
# │  {n,}    │ n or more times          │ r"b{2,}" → "bbb"         │
# │  {n,m}   │ Between n and m times    │ r"b{1,2}" → "bb"         │
# └──────────────────────────────────────────────────────────────────┘
#
# ANCHORS (where to match):
# ┌──────────────────────────────────────────────────────────────────┐
# │  Pattern │ Meaning                  │ Example                   │
# │──────────│──────────────────────────│───────────────────────────│
# │  ^       │ Start of string          │ r"^Hello" → at start     │
# │  $       │ End of string            │ r"world$" → at end       │
# │  \b      │ Word boundary            │ r"\bcat\b" → whole word  │
# └──────────────────────────────────────────────────────────────────┘
#
# SPECIAL CHARACTERS (need escaping with \):
# ┌──────────────────────────────────────────────────────────────────┐
# │  These have special meaning in regex and need \ to match        │
# │  literally:  .  ^  $  *  +  ?  {  }  [  ]  \  |  (  )          │
# │                                                                  │
# │  To match a literal dot:    r"\."   (not r".")                  │
# │  To match a literal dollar: r"\$"   (not r"$")                  │
# │  To match a literal star:   r"\*"   (not r"*")                  │
# └──────────────────────────────────────────────────────────────────┘
#
# =============================================================================


def section_3_pattern_syntax() -> None:
    """
    Demonstrate regex pattern syntax with practical examples.

    Covers character classes, quantifiers, anchors, and escaping.
    """
    print("\n" + "=" * 70)
    print("SECTION 3: PATTERN SYNTAX — THE REGEX LANGUAGE")
    print("=" * 70)

    sample = "Order #A-123 costs $45.99 on 2025-03-15. Email: user@test.com"

    # ── Character classes ────────────────────────────────────────
    print("\n── Character classes ──")
    print(f"  Text: '{sample}'")
    print(f"  \\d+ (digits):      {re.findall(r'\d+', sample)}")
    print(f"  \\w+ (word chars):  {re.findall(r'\w+', sample)}")
    print(f"  [A-Z] (uppercase): {re.findall(r'[A-Z]', sample)}")
    print(f"  [a-z]+ (lowercase words): {re.findall(r'[a-z]+', sample)}")

    # ── Quantifiers ──────────────────────────────────────────────
    print("\n── Quantifiers ──")
    print(f"  \\d{{4}} (exactly 4 digits): {re.findall(r'\d{4}', sample)}")
    print(f"  \\d{{1,2}} (1-2 digits):     {re.findall(r'\d{1,2}', sample)}")
    print(f"  \\d+ (one or more):          {re.findall(r'\d+', sample)}")

    # ── Anchors ──────────────────────────────────────────────────
    print("\n── Anchors ──")
    print(f"  ^Order (starts with): {bool(re.match(r'Order', sample))}")
    print(f"  com$ (ends with):     {bool(re.search(r'com$', sample))}")

    # ── Word boundaries (\b) ─────────────────────────────────────
    # \b matches the edge between a word char and a non-word char
    print("\n── Word boundaries (\\b) ──")
    text = "cat catfish concatenate scat"
    no_boundary = re.findall(r"cat", text)
    with_boundary = re.findall(r"\bcat\b", text)
    print(f"  Text: '{text}'")
    print(f"  r'cat' (no boundary):   {no_boundary}")   # 4 matches
    print(f"  r'\\bcat\\b' (whole word): {with_boundary}")  # 1 match

    # ── Escaping special characters ──────────────────────────────
    print("\n── Escaping special characters ──")
    price = re.search(r"\$\d+\.\d{2}", sample)
    print(f"  \\$\\d+\\.\\d{{2}} (price): '{price.group()}'" if price else "")
    # \$ matches literal $, \. matches literal dot


# =============================================================================
# SECTION 4: MATCH OBJECTS — EXTRACTING DATA
# =============================================================================
#
# When re.search() or re.match() finds something, it returns a
# Match object (not a string). You extract data using methods:
#
# ┌──────────────────────────────────────────────────────────────────┐
# │  Method      │ Returns              │ Example                   │
# │──────────────│──────────────────────│───────────────────────────│
# │  .group()    │ The matched string   │ '123'                     │
# │  .group(0)   │ Same as .group()     │ '123'                     │
# │  .group(1)   │ First capture group  │ (see Section 6)           │
# │  .start()    │ Start index          │ 4                         │
# │  .end()      │ End index            │ 7                         │
# │  .span()     │ (start, end) tuple   │ (4, 7)                   │
# │  .groups()   │ All captured groups  │ ('123', 'abc')            │
# │  .groupdict()│ Named groups as dict │ {'id': '123'}             │
# └──────────────────────────────────────────────────────────────────┘
#
# IMPORTANT: Always check for None before calling .group()!
#
#   result = re.search(pattern, text)
#   if result:                        ← Check first!
#       print(result.group())
#
# =============================================================================


def section_4_match_objects() -> None:
    """
    Show how to extract information from Match objects.

    Demonstrates group(), start(), end(), span(), and the
    critical None-check pattern.
    """
    print("\n" + "=" * 70)
    print("SECTION 4: MATCH OBJECTS — EXTRACTING DATA")
    print("=" * 70)

    text = "Transaction ID: TXN-98765 on 2025-03-15"

    # ── Basic extraction ─────────────────────────────────────────
    print("\n── Basic Match object methods ──")
    m = re.search(r"TXN-\d+", text)
    if m:
        print(f"  .group():  '{m.group()}'")     # 'TXN-98765'
        print(f"  .start():  {m.start()}")         # 17
        print(f"  .end():    {m.end()}")           # 26
        print(f"  .span():   {m.span()}")          # (17, 26)

    # ── The None-check pattern (CRITICAL) ────────────────────────
    print("\n── None-check pattern (ALWAYS do this) ──")

    # ✅ Safe — check before accessing
    result = re.search(r"MISSING", text)
    if result:
        print(f"  Found: {result.group()}")
    else:
        print(f"  re.search returned None — no match found")

    # ❌ Dangerous — crashes if no match
    # result = re.search(r"MISSING", text)
    # print(result.group())  # AttributeError: 'NoneType' has no attribute 'group'

    # ── Walrus operator pattern (Python 3.8+) ────────────────────
    # Combines the search and the None-check in one line
    print("\n── Walrus operator pattern ──")
    if m := re.search(r"\d{4}-\d{2}-\d{2}", text):
        print(f"  Date found: '{m.group()}'")


# =============================================================================
# SECTION 5: GREEDY VS LAZY QUANTIFIERS
# =============================================================================
#
# By default, quantifiers are GREEDY — they match as much as possible.
# Adding ? makes them LAZY — they match as little as possible.
#
# ┌──────────────────────────────────────────────────────────────────┐
# │  Text: "<b>hello</b> and <b>world</b>"                         │
# │                                                                  │
# │  Greedy:  r"<b>.*</b>"   → "<b>hello</b> and <b>world</b>"    │
# │           (grabs EVERYTHING between first <b> and LAST </b>)    │
# │                                                                  │
# │  Lazy:    r"<b>.*?</b>"  → "<b>hello</b>"                      │
# │           (stops at the FIRST </b> it finds)                    │
# │                                                                  │
# │  The ? after * makes it lazy (minimal matching).                │
# └──────────────────────────────────────────────────────────────────┘
#
# =============================================================================


def section_5_greedy_vs_lazy() -> None:
    """
    Demonstrate the difference between greedy and lazy quantifiers.

    This is one of the most common sources of regex bugs —
    especially when parsing structured text like HTML or logs.
    """
    print("\n" + "=" * 70)
    print("SECTION 5: GREEDY VS LAZY QUANTIFIERS")
    print("=" * 70)

    text = "<b>hello</b> and <b>world</b>"

    # ── Greedy (default) — matches as MUCH as possible ───────────
    greedy = re.findall(r"<b>.*</b>", text)
    print(f"\n── Greedy: r'<b>.*</b>' ──")
    print(f"  Text:   '{text}'")
    print(f"  Result: {greedy}")
    # ['<b>hello</b> and <b>world</b>'] — one big match

    # ── Lazy (add ?) — matches as LITTLE as possible ─────────────
    lazy = re.findall(r"<b>.*?</b>", text)
    print(f"\n── Lazy: r'<b>.*?</b>' ──")
    print(f"  Result: {lazy}")
    # ['<b>hello</b>', '<b>world</b>'] — two separate matches

    # ── Greedy vs lazy summary ───────────────────────────────────
    print("\n── Quantifier variants ──")
    print(f"  *  (greedy) → *?  (lazy)  — zero or more")
    print(f"  +  (greedy) → +?  (lazy)  — one or more")
    print(f"  ?  (greedy) → ??  (lazy)  — zero or one")
    print(f"  {{n,m}} (greedy) → {{n,m}}? (lazy)")


# =============================================================================
# SECTION 6: GROUPING AND CAPTURING
# =============================================================================
#
# Parentheses () create CAPTURE GROUPS — they extract parts of a match.
#
# ┌──────────────────────────────────────────────────────────────────┐
# │  Pattern: r"(\d{4})-(\d{2})-(\d{2})"                           │
# │  Text:    "Date: 2025-03-15"                                    │
# │                                                                  │
# │  Full match  = group(0) = "2025-03-15"                          │
# │  First group = group(1) = "2025"       (year)                   │
# │  Second group= group(2) = "03"         (month)                  │
# │  Third group = group(3) = "15"         (day)                    │
# │                                                                  │
# │  Named groups make this clearer:                                 │
# │  r"(?P<year>\d{4})-(?P<month>\d{2})-(?P<day>\d{2})"            │
# │  group("year") = "2025"                                         │
# └──────────────────────────────────────────────────────────────────┘
#
# KEY DISTINCTION with findall():
#   - WITHOUT groups: findall returns full matches
#     re.findall(r"\d+-\d+", text) → ['2025-03', '03-15']
#   - WITH groups: findall returns ONLY the captured groups
#     re.findall(r"(\d+)-(\d+)", text) → [('2025', '03'), ('03', '15')]
#
# =============================================================================


def section_6_grouping() -> None:
    """
    Demonstrate capture groups, named groups, and how they
    interact with findall() and search().
    """
    print("\n" + "=" * 70)
    print("SECTION 6: GROUPING AND CAPTURING")
    print("=" * 70)

    # ── Basic capture groups ─────────────────────────────────────
    print("\n── Basic capture groups ──")
    text = "Born: 2025-03-15, Hired: 2024-06-01"
    m = re.search(r"(\d{4})-(\d{2})-(\d{2})", text)
    if m:
        print(f"  Full match: '{m.group(0)}'")     # '2025-03-15'
        print(f"  Group 1:    '{m.group(1)}'")      # '2025'
        print(f"  Group 2:    '{m.group(2)}'")      # '03'
        print(f"  Group 3:    '{m.group(3)}'")      # '15'
        print(f"  .groups():  {m.groups()}")         # ('2025', '03', '15')

    # ── Named groups (?P<name>...) ───────────────────────────────
    print("\n── Named capture groups ──")
    pattern = r"(?P<year>\d{4})-(?P<month>\d{2})-(?P<day>\d{2})"
    m = re.search(pattern, text)
    if m:
        print(f"  group('year'):  '{m.group('year')}'")
        print(f"  group('month'): '{m.group('month')}'")
        print(f"  .groupdict():   {m.groupdict()}")
        # {'year': '2025', 'month': '03', 'day': '15'}

    # ── findall() WITH groups (returns ONLY group contents) ──────
    print("\n── findall() with groups ──")
    no_groups = re.findall(r"\d{4}-\d{2}-\d{2}", text)
    with_groups = re.findall(r"(\d{4})-(\d{2})-(\d{2})", text)
    print(f"  Without groups: {no_groups}")
    # ['2025-03-15', '2024-06-01']
    print(f"  With groups:    {with_groups}")
    # [('2025', '03', '15'), ('2024', '06', '01')]

    # ── Non-capturing groups (?:...) ─────────────────────────────
    # Use when you need grouping for alternation but don't want capture
    print("\n── Non-capturing groups (?:...) ──")
    text2 = "cat dog catfish"
    captured = re.findall(r"(cat|dog)", text2)
    non_captured = re.findall(r"(?:cat|dog)", text2)
    print(f"  (cat|dog):   {captured}")       # groups captured
    print(f"  (?:cat|dog): {non_captured}")   # same result, but faster

    # ── OR operator (|) ──────────────────────────────────────────
    print("\n── OR operator (|) ──")
    alleles = "Possible: AA, AB, AO, BB, BO, OO"
    blood = re.findall(r"[ABO]{2}", alleles)
    print(f"  Blood types found: {blood}")


# =============================================================================
# SECTION 7: FLAGS — MODIFYING REGEX BEHAVIOR
# =============================================================================
#
# Flags change HOW the regex engine interprets patterns:
#
# ┌──────────────────────────────────────────────────────────────────┐
# │  Flag                │ Short │ Effect                            │
# │──────────────────────│───────│───────────────────────────────────│
# │  re.IGNORECASE       │ re.I  │ Case-insensitive matching         │
# │  re.MULTILINE        │ re.M  │ ^ and $ match line start/end      │
# │  re.DOTALL           │ re.S  │ . matches newlines too             │
# │  re.VERBOSE          │ re.X  │ Allow comments & whitespace       │
# └──────────────────────────────────────────────────────────────────┘
#
# =============================================================================


def section_7_flags() -> None:
    """
    Show how regex flags modify pattern matching behavior.

    re.VERBOSE is especially important for production code —
    it makes complex patterns readable.
    """
    print("\n" + "=" * 70)
    print("SECTION 7: FLAGS — MODIFYING REGEX BEHAVIOR")
    print("=" * 70)

    # ── re.IGNORECASE ────────────────────────────────────────────
    print("\n── re.IGNORECASE (re.I) ──")
    text = "Python PYTHON python PyThOn"
    case_sensitive = re.findall(r"python", text)
    case_insensitive = re.findall(r"python", text, re.IGNORECASE)
    print(f"  Without flag: {case_sensitive}")    # ['python']
    print(f"  With re.I:    {case_insensitive}")  # All 4 matches

    # ── re.MULTILINE ─────────────────────────────────────────────
    print("\n── re.MULTILINE (re.M) ──")
    multiline_text = "Line 1: Hello\nLine 2: World\nLine 3: Done"
    default = re.findall(r"^Line \d", multiline_text)
    with_multi = re.findall(r"^Line \d", multiline_text, re.MULTILINE)
    print(f"  Without flag: {default}")     # ['Line 1'] — only absolute start
    print(f"  With re.M:    {with_multi}")  # ['Line 1', 'Line 2', 'Line 3']

    # ── re.VERBOSE — readable complex patterns ───────────────────
    # THIS IS THE PRODUCTION STANDARD for complex regex
    print("\n── re.VERBOSE (re.X) — production-grade readable regex ──")

    # ❌ Without VERBOSE — impossible to maintain
    ugly = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"

    # ✅ With VERBOSE — self-documenting
    email_pattern = re.compile(r"""
        ^                       # Start of string
        [a-zA-Z0-9_.+-]+        # Username (letters, digits, special chars)
        @                       # Literal @ sign
        [a-zA-Z0-9-]+           # Domain name
        \.                      # Literal dot
        [a-zA-Z0-9-.]+          # Top-level domain
        $                       # End of string
    """, re.VERBOSE)

    test_emails = ["user@test.com", "bad@", "@missing.com", "valid.name+tag@domain.org"]
    for email in test_emails:
        result = "✅" if email_pattern.match(email) else "❌"
        print(f"  {result} '{email}'")

    # ── Combining flags with | ───────────────────────────────────
    print("\n── Combining flags with | (bitwise OR) ──")
    combined = re.findall(
        r"^hello",
        "Hello\nhello\nHELLO",
        re.IGNORECASE | re.MULTILINE,
    )
    print(f"  re.I | re.M: {combined}")  # ['Hello', 'hello', 'HELLO']


# =============================================================================
# SECTION 8: re.compile() — PRODUCTION PERFORMANCE
# =============================================================================
#
# re.compile() pre-compiles a pattern into a reusable Pattern object.
# This is faster when you use the same pattern multiple times (loops).
#
# ┌──────────────────────────────────────────────────────────────────┐
# │  WITHOUT compile (recompiles every iteration):                   │
# │                                                                  │
# │  for row in million_rows:                                        │
# │      re.search(r"\d{3}-\d{4}", row)  ← compiles EACH time      │
# │                                                                  │
# │  WITH compile (compile once, use many times):                    │
# │                                                                  │
# │  phone_pattern = re.compile(r"\d{3}-\d{4}")  ← compile ONCE    │
# │  for row in million_rows:                                        │
# │      phone_pattern.search(row)  ← uses cached pattern           │
# └──────────────────────────────────────────────────────────────────┘
#
# YOUR INHERITANCE PROJECT already uses this pattern:
#   INT_PATTERN: re.Pattern = re.compile(r"^-?\d+$")
#   FLOAT_PATTERN: re.Pattern = re.compile(r"^-?\d+\.?\d*$")
#
# =============================================================================


def section_8_compile() -> None:
    """
    Show when and why to use re.compile() for performance.

    Demonstrates the compiled Pattern object and its methods.
    """
    print("\n" + "=" * 70)
    print("SECTION 8: re.compile() — PRODUCTION PERFORMANCE")
    print("=" * 70)

    # ── Creating a compiled pattern ──────────────────────────────
    print("\n── Compiled pattern object ──")
    int_pattern = re.compile(r"^-?\d+$")
    float_pattern = re.compile(r"^-?\d+\.\d+$")

    test_values = ["42", "-7", "3.14", "hello", "12.0", ""]
    print(f"  INT pattern:   {int_pattern.pattern}")
    print(f"  FLOAT pattern: {float_pattern.pattern}")

    for val in test_values:
        is_int = bool(int_pattern.match(val))
        is_float = bool(float_pattern.match(val))
        print(f"  '{val:6s}' → int: {is_int}, float: {is_float}")

    # ── Pattern object has ALL the same methods ──────────────────
    print("\n── Pattern object methods (same as re module) ──")
    p = re.compile(r"\d+")
    text = "Order 123 and 456"
    print(f"  p.search(text):  {p.search(text).group()}")
    print(f"  p.findall(text): {p.findall(text)}")
    print(f"  p.sub('X', text): '{p.sub('X', text)}'")
    print(f"  p.split('a1b2c3'): {p.split('a1b2c3')}")

    # ── When to compile (and when not to) ────────────────────────
    print("\n── When to use re.compile() ──")
    print(f"  ✅ Pattern reused in a loop (ETL pipelines)")
    print(f"  ✅ Pattern stored as a class/module constant")
    print(f"  ✅ Pattern is complex and benefits from a name")
    print(f"  ❌ One-off search (re.search is fine)")
    print(f"  ❌ Simple pattern used once (no performance gain)")


# =============================================================================
# SECTION 9: COMMON PITFALLS AND GOTCHAS
# =============================================================================


def section_9_pitfalls() -> None:
    """
    Show the most common regex bugs and how to avoid them.
    """
    print("\n" + "=" * 70)
    print("SECTION 9: COMMON PITFALLS AND GOTCHAS")
    print("=" * 70)

    # ── Pitfall 1: Forgetting raw strings ────────────────────────
    print("\n── Pitfall 1: Forgetting raw strings ──")
    # \b in a normal string is a backspace character!
    # \b in a raw string is a regex word boundary
    text = "cat catfish"
    bad = re.findall("\bcat\b", text)      # \b = backspace, WRONG
    good = re.findall(r"\bcat\b", text)    # \b = word boundary, RIGHT
    print(f"  Without r'': {bad}   (broken — \\b = backspace)")
    print(f"  With r'':    {good}  (correct — \\b = boundary)")

    # ── Pitfall 2: match() vs search() confusion ────────────────
    print("\n── Pitfall 2: match() only checks the START ──")
    text = "Hello World 123"
    print(f"  re.match(r'\\d+', '{text}'): {re.match(r'\d+', text)}")
    print(f"  re.search(r'\\d+', '{text}'): {re.search(r'\d+', text).group()}")
    print(f"  Use search() unless you specifically need start-of-string!")

    # ── Pitfall 3: findall() with groups ─────────────────────────
    print("\n── Pitfall 3: findall() changes behavior with groups ──")
    text = "2025-03 and 2024-06"
    no_group = re.findall(r"\d{4}-\d{2}", text)
    with_group = re.findall(r"(\d{4})-(\d{2})", text)
    print(f"  Without groups: {no_group}")    # ['2025-03', '2024-06']
    print(f"  With groups:    {with_group}")  # [('2025', '03'), ...]
    print(f"  Surprise! Groups change what findall returns.")
    print(f"  Use (?:...) for non-capturing if you want full matches.")

    # ── Pitfall 4: Greedy matching in data extraction ────────────
    print("\n── Pitfall 4: Greedy matching grabs too much ──")
    log = '[ERROR] Bad input [WARNING] Check config'
    greedy = re.findall(r"\[.*\]", log)
    lazy = re.findall(r"\[.*?\]", log)
    print(f"  Greedy \\[.*\\]:  {greedy}")   # One big match
    print(f"  Lazy \\[.*?\\]:   {lazy}")      # Two separate matches

    # ── Pitfall 5: Not anchoring validation patterns ─────────────
    print("\n── Pitfall 5: Not anchoring validation patterns ──")
    # When validating input, ALWAYS use ^ and $ (or fullmatch)
    bad_validate = bool(re.search(r"\d{3}", "abc123def"))
    good_validate = bool(re.fullmatch(r"\d{3}", "abc123def"))
    print(f"  search(r'\\d{{3}}', 'abc123def'): {bad_validate}  (finds 123 inside!)")
    print(f"  fullmatch(r'\\d{{3}}', 'abc123def'): {good_validate}  (entire string must be 3 digits)")

    # ── Pitfall 6: Catastrophic backtracking ─────────────────────
    print("\n── Pitfall 6: Catastrophic backtracking (performance) ──")
    print(f"  Patterns like r'(a+)+b' can take EXPONENTIAL time")
    print(f"  on inputs like 'aaaaaaaaaaaaaac' (no match, but slow)")
    print(f"  Fix: Avoid nested quantifiers. Use atomic groups or")
    print(f"  possessive quantifiers if available.")


# =============================================================================
# SECTION 10: PRODUCTION PATTERNS FROM YOUR ROADMAP
# =============================================================================


def section_10_production_patterns() -> None:
    """
    Real-world regex patterns directly applicable to your projects.

    Maps regex to specific roadmap stages and project needs.
    """
    print("\n" + "=" * 70)
    print("SECTION 10: PRODUCTION PATTERNS — YOUR ROADMAP")
    print("=" * 70)

    # ── Pattern 1: CLI Input Validation (Inheritance project) ────
    print("\n── Pattern 1: CLI Input Validation (Stage 1 — Inheritance) ──")

    # These are the exact patterns from your NumberPattern class
    int_pattern = re.compile(r"^-?\d+$")
    float_pattern = re.compile(r"^-?\d+\.\d+$")

    test_inputs = ["42", "-7", "3.14", "hello", "0", ""]
    for val in test_inputs:
        if int_pattern.match(val):
            print(f"  '{val}' → integer ({int(val)})")
        elif float_pattern.match(val):
            print(f"  '{val}' → float ({float(val)})")
        elif val:
            print(f"  '{val}' → string seed (hashable, valid)")
        else:
            print(f"  '' → empty (use default)")

    # ── Pattern 2: SSN Validation (1099 Reconciliation) ──────────
    print("\n── Pattern 2: SSN Format Validation (Stage 1 — 1099 ETL) ──")

    ssn_pattern = re.compile(r"^\d{3}-?\d{2}-?\d{4}$")
    test_ssns = ["123-45-6789", "123456789", "12-345-6789", "abc"]
    for ssn in test_ssns:
        result = "✅" if ssn_pattern.match(ssn) else "❌"
        print(f"  {result} '{ssn}'")

    # ── Pattern 3: Name Normalization (ETL cleaning) ─────────────
    print("\n── Pattern 3: Name Normalization (Stage 1-2 — ETL) ──")

    def normalize_name(name: str) -> str:
        """Clean a name for matching: strip, collapse spaces, title case."""
        cleaned = re.sub(r"\s+", " ", name.strip())
        cleaned = re.sub(r"[^\w\s'-]", "", cleaned)
        return cleaned.title()

    messy_names = ["  john   doe ", "JANE  M.  SMITH", "bob o'brien  "]
    for name in messy_names:
        print(f"  '{name}' → '{normalize_name(name)}'")

    # ── Pattern 4: Log Parsing (Stage 2 — Data Engineering) ─────
    print("\n── Pattern 4: Log Parsing (Stage 2 — Airflow/pipelines) ──")

    log_pattern = re.compile(r"""
        (?P<timestamp>\d{4}-\d{2}-\d{2}\s\d{2}:\d{2}:\d{2})  # datetime
        \s:\s
        (?P<level>\w+)                                          # log level
        \s:\s
        (?P<message>.+)                                         # message
    """, re.VERBOSE)

    log_line = "2025-03-15 14:30:45 : INFO : create_family took 0.000089s"
    m = log_pattern.search(log_line)
    if m:
        print(f"  Timestamp: {m.group('timestamp')}")
        print(f"  Level:     {m.group('level')}")
        print(f"  Message:   {m.group('message')}")

    # ── Pattern 5: Pandas str methods with regex ─────────────────
    print("\n── Pattern 5: Pandas str methods with regex (Stage 1-2) ──")
    print(f"  df['col'].str.contains(r'\\d+')      → boolean mask")
    print(f"  df['col'].str.extract(r'(\\d+)')     → captured group")
    print(f"  df['col'].str.replace(r'\\s+', ' ')  → regex replace")
    print(f"  df['col'].str.findall(r'\\w+')       → list of matches")
    print(f"  These accept regex=True (default in newer pandas)")


# =============================================================================
# SECTION 11: QUICK REFERENCE CHEAT SHEET
# =============================================================================
#
# ┌─────────────────────────────────────────────────────────────────┐
# │                    FUNCTION RETURNS GUIDE                       │
# │─────────────────────────────────────────────────────────────────│
# │  re.search()    → Match object | None                          │
# │  re.match()     → Match object | None                          │
# │  re.fullmatch() → Match object | None                          │
# │  re.findall()   → list[str] | list[tuple] | []                 │
# │  re.finditer()  → Iterator[Match]                              │
# │  re.sub()       → str (new string)                             │
# │  re.split()     → list[str]                                    │
# │  re.compile()   → re.Pattern (reusable object)                 │
# └─────────────────────────────────────────────────────────────────┘
#
# ┌─────────────────────────────────────────────────────────────────┐
# │                     COMMON PATTERNS                             │
# │─────────────────────────────────────────────────────────────────│
# │  Integer:     r"^-?\d+$"                                       │
# │  Float:       r"^-?\d+\.\d+$"                                  │
# │  Email:       r"^[\w.+-]+@[\w-]+\.[\w.-]+$"                    │
# │  Phone:       r"\d{3}[-.]?\d{3}[-.]?\d{4}"                     │
# │  Date:        r"\d{4}-\d{2}-\d{2}"                             │
# │  SSN:         r"\d{3}-?\d{2}-?\d{4}"                           │
# │  URL:         r"https?://[\w./\-?=&#]+"                        │
# │  Whitespace:  r"\s+"                                            │
# │  Words:       r"\b\w+\b"                                        │
# │  Price:       r"\$\d+\.?\d{0,2}"                                │
# └─────────────────────────────────────────────────────────────────┘
#
# ┌──────────────────────────────────────────────────────────────────┐
# │                   DECISION GUIDE                                 │
# │──────────────────────────────────────────────────────────────────│
# │  Need to...                       │ Use                         │
# │───────────────────────────────────│─────────────────────────────│
# │  Check if pattern exists          │ re.search() + if check      │
# │  Validate entire input string     │ re.fullmatch()              │
# │  Get all matches as strings       │ re.findall()                │
# │  Get all matches with positions   │ re.finditer()               │
# │  Replace all occurrences          │ re.sub()                    │
# │  Split on complex delimiter       │ re.split()                  │
# │  Reuse pattern in loop            │ re.compile() + method       │
# │  Make pattern readable            │ re.VERBOSE flag             │
# │  Case-insensitive search          │ re.IGNORECASE flag          │
# │  Just check start of string       │ str.startswith() (no regex) │
# │  Simple substring check           │ "x" in string (no regex)    │
# └──────────────────────────────────────────────────────────────────┘
#
# =============================================================================


# =============================================================================
# MAIN EXECUTION
# =============================================================================

if __name__ == "__main__":
    section_1_what_are_regex()
    section_2_core_functions()
    section_3_pattern_syntax()
    section_4_match_objects()
    section_5_greedy_vs_lazy()
    section_6_grouping()
    section_7_flags()
    section_8_compile()
    section_9_pitfalls()
    section_10_production_patterns()

    print("\n" + "=" * 70)
    print("REFERENCE COMPLETE — See Section 11 (cheat sheet) in source code")
    print("=" * 70)
