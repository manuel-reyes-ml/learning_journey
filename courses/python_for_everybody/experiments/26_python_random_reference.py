"""
python_random_reference.py
===========================

Personal reference: Python's ``random`` module — pseudo-random number
generation, seeding, selection functions, and production patterns.

Topics covered
--------------
1. What "random" means in Python — PRNG vs TRNG vs CSPRNG
2. The Mersenne Twister — how Python generates numbers
3. Seeding — reproducibility and determinism
4. Core functions — choice, randint, randrange, shuffle, sample
5. random.Random instances — isolated generators
6. The secrets module — when random is NOT enough
7. Common pitfalls and gotchas
8. Production patterns from your roadmap

Why this matters for your roadmap
----------------------------------
- Stage 1: Your CS50 Inheritance project uses ``random.choice()``
  for allele selection and ``random.seed()`` for CLI reproducibility.
  Your 1099 Reconciliation ETL uses ``random.Random`` instance
  isolation with ``DEFAULT_SEED = 20250214`` for deterministic
  synthetic test data generation via Faker.
- Stage 2: Simulation-based testing, Monte Carlo methods for data
  validation, and randomized train/test splits in data pipelines.
- Stage 3: ML model training relies on seeded randomness for
  reproducible experiments. Scikit-learn, PyTorch, and NumPy all
  have their own RNG systems that must be seeded consistently.
- Stage 4-5: LLM temperature sampling is controlled randomness.
  Agent exploration strategies (epsilon-greedy) use random selection.
  A/B test assignment uses deterministic hashing, not ``random``.

How to use this file
---------------------
Run it directly to see all output::

    $ python 26_python_random_reference.py

Or import individual sections to experiment in a REPL.

References
----------
.. [1] Python random module docs: https://docs.python.org/3/library/random.html
.. [2] Python secrets module docs: https://docs.python.org/3/library/secrets.html
.. [3] Real Python — Generating Random Data: https://realpython.com/python-random/
.. [4] Mersenne Twister paper: Matsumoto & Nishimura, ACM TOMACS 1998
"""

from __future__ import annotations

import random
import sys


# =============================================================================
# SECTION 1: WHAT "RANDOM" MEANS IN PYTHON
# =============================================================================
#
# Python's ``random`` module generates PSEUDO-random numbers (PRNGs).
# They LOOK random but are completely DETERMINISTIC — given the same
# starting state, they produce the exact same sequence every time.
#
# THREE LEVELS OF RANDOMNESS:
# ┌──────────────────────────────────────────────────────────────────┐
# │  Level │ Module      │ Use case              │ Predictable?      │
# │────────│─────────────│───────────────────────│───────────────────│
# │  PRNG  │ random      │ Simulations, games,   │ YES — same seed   │
# │        │             │ test data, sampling   │ = same sequence   │
# │────────│─────────────│───────────────────────│───────────────────│
# │  PRNG  │ numpy.random│ Arrays of random data │ YES — same seed   │
# │  (bulk)│             │ ML training, stats    │ = same sequence   │
# │────────│─────────────│───────────────────────│───────────────────│
# │ CSPRNG │ secrets     │ Passwords, tokens,    │ NO — uses OS      │
# │        │             │ auth, cryptography    │ entropy source    │
# └──────────────────────────────────────────────────────────────────┘
#
# THE KEY INSIGHT:
# "Random" in Python means "deterministic but hard to predict without
# knowing the seed." This is a FEATURE for reproducibility, not a bug.
# Your 1099 project and Inheritance project both exploit this:
#   - Same seed → same test data → reproducible tests
#   - No seed → system entropy → different each run
#
# =============================================================================


def section_1_what_is_random() -> None:
    """
    Demonstrate that Python's random is pseudo-random (deterministic).

    Shows that the same seed always produces the same sequence,
    proving that ``random`` is not truly random.
    """
    print("=" * 70)
    print("SECTION 1: WHAT 'RANDOM' MEANS IN PYTHON")
    print("=" * 70)

    # ── Same seed = same sequence (ALWAYS) ───────────────────────
    print("\n── Same seed = same sequence ──")
    random.seed(42)
    run_1 = [random.randint(1, 100) for _ in range(5)]

    random.seed(42)
    run_2 = [random.randint(1, 100) for _ in range(5)]

    print(f"  Seed 42, run 1: {run_1}")
    print(f"  Seed 42, run 2: {run_2}")
    print(f"  Identical? {run_1 == run_2}")  # Always True

    # ── Different seed = different sequence ───────────────────────
    print("\n── Different seed = different sequence ──")
    random.seed(99)
    run_3 = [random.randint(1, 100) for _ in range(5)]
    print(f"  Seed 99:        {run_3}")
    print(f"  Same as seed 42? {run_1 == run_3}")  # Almost certainly False

    # ── No seed = system entropy (different every run) ───────────
    print("\n── No seed = different each run ──")
    random.seed()  # Uses system time/entropy
    run_4 = [random.randint(1, 100) for _ in range(5)]
    print(f"  No seed:         {run_4}")
    print(f"  This changes every time you run the program.")


# =============================================================================
# SECTION 2: THE MERSENNE TWISTER
# =============================================================================
#
# Python uses the Mersenne Twister algorithm (MT19937) as its core
# PRNG. Key properties:
#
# ┌──────────────────────────────────────────────────────────────────┐
# │  Property          │ Value                                      │
# │────────────────────│────────────────────────────────────────────│
# │  Period            │ 2^19937 - 1 (astronomically long)          │
# │  Precision         │ 53-bit floats                              │
# │  Speed             │ Fast, implemented in C under the hood      │
# │  Thread-safe       │ Yes (CPython implementation)               │
# │  Cryptographic     │ NO — do not use for security               │
# │  State size        │ 624 × 32-bit integers (internal state)     │
# └──────────────────────────────────────────────────────────────────┘
#
# The period means: after 2^19937 - 1 numbers, the sequence repeats.
# That's a number with ~6,000 digits. You will never exhaust it.
#
# =============================================================================


def section_2_mersenne_twister() -> None:
    """
    Show properties of Python's underlying random generator.
    """
    print("\n" + "=" * 70)
    print("SECTION 2: THE MERSENNE TWISTER")
    print("=" * 70)

    # ── The state is large but inspectable ───────────────────────
    print("\n── Internal state ──")
    random.seed(42)
    state = random.getstate()
    print(f"  State type:   {type(state)}")
    print(f"  State[0]:     {state[0]} (version number)")
    print(f"  State[1] len: {len(state[1])} integers (624 + 1 index)")
    print(f"  State can be saved and restored for exact replay.")

    # ── Save and restore state ───────────────────────────────────
    print("\n── Save/restore state (advanced reproducibility) ──")
    random.seed(42)
    saved_state = random.getstate()
    first_three = [random.random() for _ in range(3)]

    # Restore and regenerate — identical results
    random.setstate(saved_state)
    replayed = [random.random() for _ in range(3)]

    print(f"  First run:  {first_three}")
    print(f"  Replayed:   {replayed}")
    print(f"  Identical?  {first_three == replayed}")


# =============================================================================
# SECTION 3: SEEDING — REPRODUCIBILITY AND DETERMINISM
# =============================================================================
#
# random.seed() sets the starting state of the generator. Everything
# after that call is deterministic.
#
# ┌──────────────────────────────────────────────────────────────────┐
# │  Call               │ Behavior                                   │
# │─────────────────────│────────────────────────────────────────────│
# │  random.seed()      │ Uses system entropy (time, OS randomness)  │
# │  random.seed(None)  │ Same as seed() — system entropy            │
# │  random.seed(42)    │ Deterministic — same sequence every time   │
# │  random.seed(0)     │ Valid! 0 is an accepted value              │
# │  random.seed(-7)    │ Valid! Negatives work                      │
# │  random.seed(3.14)  │ Valid! Floats are accepted                 │
# │  random.seed("abc") │ Valid! Strings are accepted                │
# └──────────────────────────────────────────────────────────────────┘
#
# THE RULE: seed() accepts None, int, float, str, bytes, and
# bytearray (Python 3.12+). NOT tuples, lists, dicts, or sets.
# The seed value is used to initialize the generator state.
#
# SUPPORTED SEED TYPES (Python 3.12+):
# None, int, float, str, bytes, bytearray.
# NOT supported: tuple, list, dict, set — even if hashable.
# (Older Python versions accepted any hashable value.)
#
# =============================================================================


def section_3_seeding() -> None:
    """
    Demonstrate seed behavior with various input types.

    Shows that any hashable value is valid, and that seed()
    with no argument uses system entropy.
    """
    print("\n" + "=" * 70)
    print("SECTION 3: SEEDING — REPRODUCIBILITY AND DETERMINISM")
    print("=" * 70)

    # ── All hashable types work as seeds ─────────────────────────
    print("\n── Valid seed values (all hashable types) ──")
    seed_values = [42, 0, -7, 3.14, "hello", True, None]

    for seed_val in seed_values:
        random.seed(seed_val)
        result = random.randint(1, 1000)
        print(f"  seed({str(seed_val):12s}) → randint(1,1000) = {result}")

    # ── Reproducing the same seed gives same result ──────────────
    print("\n── Proof: same seed = same output ──")
    for seed_val in [42, "hello", 3.14]:
        random.seed(seed_val)
        r1 = random.randint(1, 1000)
        random.seed(seed_val)
        r2 = random.randint(1, 1000)
        print(f"  seed({str(seed_val):8s}): {r1} == {r2}? {r1 == r2}")

    # ── Unsupported types FAIL ────────────────────────────────────
    print("\n── Invalid seeds (unsupported types in Python 3.12+) ──")
    for bad_seed, name in [((1, 2), "tuple"), ([1, 2], "list"), ({"a": 1}, "dict"), ({1, 2}, "set")]:
        try:
            random.seed(bad_seed)
        except TypeError as e:
            print(f"  seed({name:5s}) → TypeError")

    # ── Production patterns ──────────────────────────────────────
    print("\n── Production seeding patterns ──")
    print(f"  # At module level (different each run):")
    print(f"  random.seed()           # ← your inheritance.py line 76")
    print(f"")
    print(f"  # CLI flag for reproducible testing:")
    print(f"  random.seed(args.seed)  # ← your inheritance.py line 788")
    print(f"")
    print(f"  # Test data generation with explicit constant:")
    print(f"  DEFAULT_SEED = 20250214 # ← your 1099 generate_sample_data.py")
    print(f"  rng = random.Random(DEFAULT_SEED)")


# =============================================================================
# SECTION 4: CORE FUNCTIONS
# =============================================================================
#
# ┌──────────────────────────────────────────────────────────────────┐
# │  Function             │ Returns    │ Purpose                     │
# │───────────────────────│────────────│─────────────────────────────│
# │  random.choice(seq)   │ element    │ Pick ONE random element     │
# │  random.choices(seq,k)│ list       │ Pick k WITH replacement     │
# │  random.sample(seq,k) │ list       │ Pick k WITHOUT replacement  │
# │  random.randint(a,b)  │ int        │ Random int, a <= N <= b     │
# │  random.randrange(a,b)│ int        │ Random int, a <= N < b      │
# │  random.random()      │ float      │ Random float 0.0 <= N < 1.0 │
# │  random.uniform(a,b)  │ float      │ Random float a <= N <= b    │
# │  random.shuffle(seq)  │ None       │ Shuffle list IN PLACE       │
# │  random.seed(val)     │ None       │ Set generator state         │
# └──────────────────────────────────────────────────────────────────┘
#
# KEY DISTINCTION:
#   randint(a, b)  → b is INCLUSIVE  [a, b]
#   randrange(a, b) → b is EXCLUSIVE [a, b)
#   This matches range() behavior: range(1, 10) doesn't include 10.
#
# =============================================================================


def section_4_core_functions() -> None:
    """
    Demonstrate all commonly used random module functions.
    """
    print("\n" + "=" * 70)
    print("SECTION 4: CORE FUNCTIONS")
    print("=" * 70)

    random.seed(42)  # Fixed seed for reproducible demo output

    # ── random.choice() — pick ONE element ───────────────────────
    print("\n── random.choice(sequence) — pick ONE ──")
    alleles = ['A', 'B', 'O']
    picks = [random.choice(alleles) for _ in range(10)]
    print(f"  Alleles pool: {alleles}")
    print(f"  10 picks:     {picks}")
    print(f"  This is how your Inheritance project picks alleles!")

    # ── choice() vs manual indexing ──────────────────────────────
    print("\n── choice() vs manual index (style comparison) ──")
    random.seed(42)
    # ❌ C-style (works but not Pythonic)
    c_style = alleles[random.randint(0, len(alleles) - 1)]
    random.seed(42)
    # ✅ Pythonic
    pythonic = random.choice(alleles)
    print(f"  C-style:  alleles[randint(0, 2)]  → '{c_style}'")
    print(f"  Pythonic: random.choice(alleles)   → '{pythonic}'")
    print(f"  Both give same result with same seed, but choice() is")
    print(f"  cleaner, safer (no off-by-one), and self-documenting.")

    # ── random.choices() — pick k WITH replacement ───────────────
    print("\n── random.choices(seq, k=n) — pick k WITH replacement ──")
    random.seed(42)
    with_replacement = random.choices(alleles, k=6)
    print(f"  6 picks (can repeat): {with_replacement}")

    # ── random.sample() — pick k WITHOUT replacement ─────────────
    print("\n── random.sample(seq, k=n) — pick k WITHOUT replacement ──")
    deck = list(range(1, 11))
    hand = random.sample(deck, k=5)
    print(f"  Deck: {deck}")
    print(f"  Hand: {hand}  (no duplicates!)")

    # ── random.randint(a, b) — inclusive range ───────────────────
    print("\n── random.randint(a, b) — inclusive on BOTH ends ──")
    rolls = [random.randint(1, 6) for _ in range(10)]
    print(f"  10 dice rolls (1-6): {rolls}")

    # ── random.randrange(a, b) — exclusive upper bound ───────────
    print("\n── random.randrange(a, b) — exclusive upper bound ──")
    indices = [random.randrange(0, 3) for _ in range(10)]
    print(f"  10 indices (0-2): {indices}")
    print(f"  Note: 3 is NEVER produced (exclusive, like range())")

    # ── The 0-or-1 pattern (coin flip / parent allele) ───────────
    print("\n── The 0-or-1 pattern (coin flip) ──")
    print(f"  # C-style: rand() % 2")
    print(f"  # Python:  random.randint(0, 1)     → {random.randint(0, 1)}")
    print(f"  # Better:  random.choice([0, 1])     → {random.choice([0, 1])}")
    print(f"  # Best:    random.choice(parent.alleles) → direct pick!")
    print(f"  Your Inheritance project uses the 'Best' pattern.")

    # ── random.random() — float in [0.0, 1.0) ───────────────────
    print("\n── random.random() — float [0.0, 1.0) ──")
    floats = [round(random.random(), 4) for _ in range(5)]
    print(f"  5 random floats: {floats}")

    # ── random.uniform(a, b) — float in [a, b] ──────────────────
    print("\n── random.uniform(a, b) — float in [a, b] ──")
    amounts = [round(random.uniform(1000.0, 9999.99), 2) for _ in range(3)]
    print(f"  3 random amounts: {amounts}")
    print(f"  Your 1099 project uses this for synthetic transaction amounts.")

    # ── random.shuffle() — in-place reordering ───────────────────
    print("\n── random.shuffle(list) — mutates IN PLACE ──")
    items = [1, 2, 3, 4, 5]
    print(f"  Before: {items}")
    random.shuffle(items)
    print(f"  After:  {items}")
    print(f"  Returns None! The list itself is changed.")


# =============================================================================
# SECTION 5: random.Random INSTANCES — ISOLATED GENERATORS
# =============================================================================
#
# The module-level functions (random.choice, random.seed, etc.) all
# share a SINGLE hidden Random instance. This means:
#
#   random.seed(42)
#   result_a = random.choice(...)    ← advances the shared state
#   result_b = random.randint(...)   ← uses SAME shared state
#
# If two parts of your code both call random functions, they
# INTERFERE with each other's sequences.
#
# SOLUTION: Create isolated Random INSTANCES:
# ┌──────────────────────────────────────────────────────────────────┐
# │                                                                  │
# │  # Each instance has its OWN state — no interference             │
# │  rng_data = random.Random(42)    # for test data generation      │
# │  rng_game = random.Random(99)    # for game logic                │
# │                                                                  │
# │  rng_data.choice(...)  ← uses rng_data's state only              │
# │  rng_game.randint(...) ← uses rng_game's state only              │
# │                                                                  │
# │  They never affect each other, even if called interleaved.       │
# └──────────────────────────────────────────────────────────────────┘
#
# YOUR 1099 PROJECT uses this pattern:
#   rng = random.Random(DEFAULT_SEED)
#   rng.uniform(low, high)   # isolated from module-level random
#   rng.choice(options)      # same isolated instance
#
# =============================================================================


def section_5_random_instances() -> None:
    """
    Demonstrate isolated Random instances for independent streams.

    Shows how module-level random and instance-level random
    produce different sequences, and why isolation matters.
    """
    print("\n" + "=" * 70)
    print("SECTION 5: random.Random INSTANCES — ISOLATED GENERATORS")
    print("=" * 70)

    # ── Module-level vs instance-level ───────────────────────────
    print("\n── Module-level (shared state) ──")
    random.seed(42)
    shared = [random.randint(1, 100) for _ in range(5)]
    print(f"  Module-level: {shared}")

    print("\n── Instance-level (isolated state) ──")
    rng = random.Random(42)
    isolated = [rng.randint(1, 100) for _ in range(5)]
    print(f"  Instance:     {isolated}")
    print(f"  Same seed, same results: {shared == isolated}")

    # ── Two instances don't interfere ────────────────────────────
    print("\n── Two instances running independently ──")
    rng_a = random.Random(42)
    rng_b = random.Random(42)

    # Advance rng_a by 3 calls
    for _ in range(3):
        rng_a.random()

    # rng_b is still at the start — unaffected
    a_next = rng_a.randint(1, 100)
    b_next = rng_b.randint(1, 100)
    print(f"  rng_a (after 3 calls): next = {a_next}")
    print(f"  rng_b (fresh):         next = {b_next}")
    print(f"  Different! rng_a advanced, rng_b didn't.")

    # ── The 1099 project pattern ─────────────────────────────────
    print("\n── Your 1099 project pattern ──")
    DEFAULT_SEED = 20250214
    rng = random.Random(DEFAULT_SEED)
    amounts = [round(rng.uniform(4000, 9000), 2) for _ in range(3)]
    print(f"  DEFAULT_SEED = {DEFAULT_SEED}")
    print(f"  rng = random.Random(DEFAULT_SEED)")
    print(f"  3 synthetic amounts: {amounts}")
    print(f"  Deterministic test data — same every run!")

    # ── Instance has ALL the same methods ────────────────────────
    print("\n── Instance methods (same as module-level) ──")
    rng = random.Random(42)
    print(f"  rng.choice(['A','B','O']): '{rng.choice(['A', 'B', 'O'])}'")
    print(f"  rng.randint(1, 100):       {rng.randint(1, 100)}")
    print(f"  rng.random():              {rng.random():.4f}")
    print(f"  rng.uniform(10, 20):       {rng.uniform(10, 20):.2f}")
    items = [1, 2, 3, 4, 5]
    rng.shuffle(items)
    print(f"  rng.shuffle([1,2,3,4,5]):  {items}")


# =============================================================================
# SECTION 6: THE secrets MODULE — WHEN random IS NOT ENOUGH
# =============================================================================
#
# random is PREDICTABLE (by design). If an attacker knows your seed,
# they know your entire sequence. For security-sensitive operations,
# use the ``secrets`` module instead.
#
# ┌──────────────────────────────────────────────────────────────────┐
# │  Task                    │ Use random   │ Use secrets             │
# │──────────────────────────│──────────────│─────────────────────────│
# │  Blood type simulation   │ ✅           │ ❌ Overkill            │
# │  Test data generation    │ ✅           │ ❌ Need reproducibility│
# │  Shuffling a game deck   │ ✅           │ ❌ Not security        │
# │  ML train/test split     │ ✅           │ ❌ Need reproducibility│
# │  Password generation     │ ❌ INSECURE  │ ✅                     │
# │  API tokens              │ ❌ INSECURE  │ ✅                     │
# │  Session IDs             │ ❌ INSECURE  │ ✅                     │
# │  Cryptographic keys      │ ❌ INSECURE  │ ✅                     │
# └──────────────────────────────────────────────────────────────────┘
#
# =============================================================================


def section_6_secrets() -> None:
    """
    Show when to use secrets instead of random.

    Demonstrates the API similarity and the security difference.
    """
    print("\n" + "=" * 70)
    print("SECTION 6: THE secrets MODULE — WHEN random IS NOT ENOUGH")
    print("=" * 70)

    import secrets
    import string

    # ── secrets has similar functions ────────────────────────────
    print("\n── secrets API (similar to random) ──")
    print(f"  secrets.choice('ABC'):     '{secrets.choice('ABC')}'")
    print(f"  secrets.randbelow(100):    {secrets.randbelow(100)}")
    print(f"  secrets.token_hex(16):     '{secrets.token_hex(16)}'")
    print(f"  secrets.token_urlsafe(16): '{secrets.token_urlsafe(16)}'")

    # ── The critical difference ──────────────────────────────────
    print("\n── Why secrets is different ──")
    print(f"  random.seed(42) → sequence is predictable forever")
    print(f"  secrets has NO seed — uses OS entropy (e.g., /dev/urandom)")
    print(f"  Each call is independent and unpredictable")

    # ── Secure password example ──────────────────────────────────
    print("\n── Secure password (CORRECT way) ──")
    chars = string.ascii_letters + string.digits + string.punctuation
    secure_pw = ''.join(secrets.choice(chars) for _ in range(16))
    print(f"  secrets-based:  '{secure_pw}'")

    print("\n── Insecure password (WRONG way — never do this) ──")
    insecure_pw = ''.join(random.choice(chars) for _ in range(16))
    print(f"  random-based:   '{insecure_pw}'")
    print(f"  Looks the same, but an attacker could predict the sequence!")


# =============================================================================
# SECTION 7: COMMON PITFALLS AND GOTCHAS
# =============================================================================


def section_7_pitfalls() -> None:
    """
    Show the most common mistakes with the random module.
    """
    print("\n" + "=" * 70)
    print("SECTION 7: COMMON PITFALLS AND GOTCHAS")
    print("=" * 70)

    # ── Pitfall 1: Seeding inside a loop ─────────────────────────
    print("\n── Pitfall 1: Seeding inside a loop ──")
    print(f"  ❌ BAD — re-seeding resets the sequence:")
    results_bad = []
    for _ in range(5):
        random.seed(42)  # WRONG: resets every iteration!
        results_bad.append(random.randint(1, 100))
    print(f"     {results_bad}  ← same number every time!")

    print(f"  ✅ GOOD — seed once, before the loop:")
    random.seed(42)
    results_good = [random.randint(1, 100) for _ in range(5)]
    print(f"     {results_good}  ← different numbers!")

    # ── Pitfall 2: randint vs randrange boundary ─────────────────
    print("\n── Pitfall 2: randint vs randrange boundaries ──")
    random.seed(42)
    print(f"  randint(0, 2)   can return: 0, 1, or 2  (inclusive)")
    print(f"  randrange(0, 2) can return: 0 or 1 only  (exclusive)")
    print(f"  For picking index 0 or 1: randint(0, 1) works")
    print(f"  But random.choice([0, 1]) is clearer and safer.")

    # ── Pitfall 3: shuffle returns None ──────────────────────────
    print("\n── Pitfall 3: shuffle() returns None ──")
    items = [1, 2, 3, 4, 5]
    result = random.shuffle(items)
    print(f"  result = random.shuffle(items)")
    print(f"  result is None: {result is None}")
    print(f"  items (mutated): {items}")
    print(f"  ❌ Don't do: shuffled = random.shuffle(items)")
    print(f"  ✅ If you need a copy: shuffled = random.sample(items, len(items))")

    # ── Pitfall 4: Using random for security ─────────────────────
    print("\n── Pitfall 4: Using random for security ──")
    print(f"  The Python docs explicitly warn:")
    print(f"  'The pseudo-random generators of this module should")
    print(f"   not be used for security purposes.'")
    print(f"  Use secrets module instead (see Section 6).")

    # ── Pitfall 5: Shared state across modules ───────────────────
    print("\n── Pitfall 5: Shared state interference ──")
    print(f"  Module A calls random.seed(42)")
    print(f"  Module B calls random.choice() — uses A's state!")
    print(f"  Fix: Use random.Random() instances for isolation.")
    print(f"  Your 1099 project does this correctly.")

    # ── Pitfall 6: Forgetting to seed in tests ───────────────────
    print("\n── Pitfall 6: Non-deterministic tests ──")
    print(f"  If your test uses random but doesn't seed,")
    print(f"  it produces different results each run = flaky test.")
    print(f"  Always seed at the start of randomized tests:")
    print(f"    def test_allele_selection():")
    print(f"        random.seed(42)  # ← deterministic!")
    print(f"        result = random_allele()")
    print(f"        assert result in ('A', 'B', 'O')")


# =============================================================================
# SECTION 8: PRODUCTION PATTERNS FROM YOUR ROADMAP
# =============================================================================


def section_8_production_patterns() -> None:
    """
    Real-world random patterns directly applicable to your projects.
    """
    print("\n" + "=" * 70)
    print("SECTION 8: PRODUCTION PATTERNS — YOUR ROADMAP")
    print("=" * 70)

    # ── Pattern 1: Inheritance project — allele selection ────────
    print("\n── Pattern 1: Allele Selection (Stage 1 — Inheritance) ──")

    ALLELES = ('A', 'B', 'O')

    def random_allele(alleles: tuple[str, ...] = ALLELES) -> str:
        """Return a randomly chosen blood type allele."""
        return random.choice(alleles)

    random.seed(42)
    # Base case: oldest generation gets two random alleles
    grandparent_alleles = (random_allele(), random_allele())
    print(f"  Grandparent: {grandparent_alleles}")

    # Recursive case: child inherits one from each parent
    parent_alleles = ('A', 'O')
    inherited = random.choice(parent_alleles)
    print(f"  Parent alleles: {parent_alleles}")
    print(f"  Child inherits: '{inherited}'")

    # ── Pattern 2: 1099 project — seeded test data ───────────────
    print("\n── Pattern 2: Synthetic Test Data (Stage 1 — 1099 ETL) ──")

    DEFAULT_SEED = 20250214
    rng = random.Random(DEFAULT_SEED)

    def generate_amount(rng: random.Random, low: float, high: float) -> float:
        """Generate a deterministic synthetic dollar amount."""
        return round(rng.uniform(low, high), 2)

    amounts = [generate_amount(rng, 4000, 9000) for _ in range(5)]
    print(f"  Seed: {DEFAULT_SEED}")
    print(f"  5 synthetic amounts: {amounts}")
    print(f"  Same every run — perfect for test assertions!")

    # ── Pattern 3: CLI seed flag ─────────────────────────────────
    print("\n── Pattern 3: CLI --seed Flag (Stage 1 — Inheritance) ──")
    print(f"  # In argparse:")
    print(f"  parser.add_argument('-s', '--seed', type=validate_seed)")
    print(f"")
    print(f"  # In main():")
    print(f"  if args.seed:")
    print(f"      random.seed(args.seed)")
    print(f"")
    print(f"  # Usage:")
    print(f"  python inheritance.py -g 3 -s 42     # reproducible")
    print(f"  python inheritance.py -g 3            # random each run")

    # ── Pattern 4: ML reproducibility (Stage 3) ──────────────────
    print("\n── Pattern 4: ML Reproducibility (Stage 3 — future) ──")
    print(f"  # Seed ALL random sources for reproducible training:")
    print(f"  import random")
    print(f"  import numpy as np")
    print(f"  # import torch  # when you get there")
    print(f"")
    print(f"  SEED = 42")
    print(f"  random.seed(SEED)")
    print(f"  np.random.seed(SEED)")
    print(f"  # torch.manual_seed(SEED)")
    print(f"  # torch.cuda.manual_seed_all(SEED)")


# =============================================================================
# SECTION 9: QUICK REFERENCE CHEAT SHEET
# =============================================================================
#
# ┌─────────────────────────────────────────────────────────────────┐
# │                   FUNCTION RETURNS GUIDE                        │
# │─────────────────────────────────────────────────────────────────│
# │  random.seed(val)       → None (sets state)                    │
# │  random.random()        → float [0.0, 1.0)                    │
# │  random.uniform(a, b)   → float [a, b]                        │
# │  random.randint(a, b)   → int [a, b] inclusive                 │
# │  random.randrange(a, b) → int [a, b) exclusive                 │
# │  random.choice(seq)     → single element                       │
# │  random.choices(seq, k) → list of k elements (WITH replace)    │
# │  random.sample(seq, k)  → list of k elements (WITHOUT replace) │
# │  random.shuffle(seq)    → None (mutates in place!)             │
# │  random.getstate()      → tuple (internal state snapshot)      │
# │  random.setstate(state) → None (restores snapshot)             │
# └─────────────────────────────────────────────────────────────────┘
#
# ┌─────────────────────────────────────────────────────────────────┐
# │                    SEED ACCEPTS                                 │
# │─────────────────────────────────────────────────────────────────│
# │  int:        random.seed(42)        ✅                         │
# │  int(0):     random.seed(0)         ✅ (valid!)                │
# │  negative:   random.seed(-7)        ✅                         │
# │  float:      random.seed(3.14)      ✅ (floats are hashable)   │
# │  str:        random.seed("hello")   ✅                         │
# │  bool:       random.seed(True)      ✅ (bool is int subclass)  │
# │  None:       random.seed(None)      ✅ (uses system entropy)   │
# │  bytes:      random.seed(b"data")   ✅                         │
# │  bytearray:  random.seed(ba)        ✅                         │
# │  tuple:      random.seed((1,2,3))   ❌ TypeError (3.12+)       │
# │  list:       random.seed([1,2])     ❌ TypeError               │
# │  dict:       random.seed({"a":1})   ❌ TypeError               │
# │  set:        random.seed({1,2})     ❌ TypeError               │
# └─────────────────────────────────────────────────────────────────┘
#
# ┌──────────────────────────────────────────────────────────────────┐
# │                   DECISION GUIDE                                 │
# │──────────────────────────────────────────────────────────────────│
# │  Need to...                       │ Use                         │
# │───────────────────────────────────│─────────────────────────────│
# │  Pick one item from a list         │ random.choice(seq)         │
# │  Pick item from parent's alleles   │ random.choice(parent.alleles)│
# │  Pick k items (can repeat)         │ random.choices(seq, k=n)   │
# │  Pick k items (no repeats)         │ random.sample(seq, k=n)    │
# │  Random int in range               │ random.randint(a, b)       │
# │  Random float in range             │ random.uniform(a, b)       │
# │  Reorder a list                    │ random.shuffle(seq)        │
# │  Reproducible test data            │ rng = random.Random(seed)  │
# │  Isolated generator                │ rng = random.Random(seed)  │
# │  Password / token / auth           │ secrets.choice() etc.      │
# │  Seed for ML experiment            │ Seed random + numpy + torch│
# └──────────────────────────────────────────────────────────────────┘
#
# =============================================================================


# =============================================================================
# MAIN EXECUTION
# =============================================================================

if __name__ == "__main__":
    section_1_what_is_random()
    section_2_mersenne_twister()
    section_3_seeding()
    section_4_core_functions()
    section_5_random_instances()
    section_6_secrets()
    section_7_pitfalls()
    section_8_production_patterns()

    print("\n" + "=" * 70)
    print("REFERENCE COMPLETE — See Section 9 (cheat sheet) in source code")
    print("=" * 70)
