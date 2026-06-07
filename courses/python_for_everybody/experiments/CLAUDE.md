# CLAUDE.md — Python Learning Notebooks (`experiments/`)

<!-- Scoped to learning_journey/courses/python_for_everybody/experiments/.
     HTML comments are stripped from Claude's context, so notes here cost no tokens. -->

## What this folder is

This folder holds **reference notebooks** — numbered `.ipynb` study guides that teach one
Python feature, class, function, or library (e.g. `18_python_type_system_reference.ipynb`).
I read them later to learn the topic in depth. **You author these completely** — they are
teaching material you produce, not code I hand-write.

## Your job here (important — this folder is the exception)

In my project codebases under `src/`, I write the code myself and you guide me block by
block ("no vibe coding"). **This folder is the opposite of that rule.** Here:

- **Write the entire notebook**, start to finish, for whatever topic I name.
- Aim for a **comprehensive, study-ready reference**, not a minimal demo. Depth and clarity
  beat brevity — I use this to actually learn the feature and how it works.
- **Teach as you go.** Every section pairs a plain-language conceptual note (what it is, why
  it exists, when to use it) with runnable code that demonstrates it.

## Research & depth (what makes a good guide)

- **Use current, idiomatic practices** for the topic, and note version requirements
  (e.g. "3.10+", "3.12 `type` statement"). Prefer modern syntax: PEP 585 builtin generics
  (`list[int]`), PEP 604 unions (`X | Y`), `pathlib` over `os.path`, and so on.
- **Verify the current API.** For a library or stdlib module, check its official
  documentation so signatures, methods, and recommended patterns are up to date — don't
  rely on stale memory.
- **Show real-world usage**, not just toy snippets: how the feature is actually used in
  practice (idiomatic patterns; how the stdlib or popular libraries use it), plus a
  realistic finance/data example where it fits naturally.
- **Cover the edges:** common mistakes, gotchas, anti-patterns, and when *not* to use it.
- **Make cells runnable and self-contained** so I can execute top to bottom and see output.

## Notebook structure (match `18_python_type_system_reference.ipynb`)

1. **Title cell** (markdown): `# 🔷 <Topic> — Complete Reference Guide`, a one-line summary,
   then a numbered **Table of Contents** linking each section.
2. **Section markdown header** (`## N. <Section>`) before each topic, with a short
   conceptual note (bullets: what it provides, when to use it).
3. **Code cells** opened with an ASCII banner, one idea per cell (several small cells beat
   one large one):
   ```python
   # =============================================================================
   # SECTION NAME
   # =============================================================================
   ```
4. **Final "Quick Reference" cell** (markdown): a `# ====` cheat-sheet summarizing the
   topic's syntax for fast lookup.

**File naming:** `NN_topic_name_reference.ipynb` — two-digit zero-padded, snake_case.

## Python code standards (apply to all code you write in the notebook)

- `from __future__ import annotations` in the first code cell — IPython applies it to the
  whole session, enabling PEP 604 unions and forward references.
- **Type hints everywhere**, PEP 604 unions (`str | None`, not `Optional[str]`).
- **NumPy-style docstrings** on every function and class
  (Parameters / Returns / Raises / Examples).
- **Naming:** `snake_case` functions and variables, `PascalCase` classes,
  `SCREAMING_SNAKE_CASE` constants.
- **`print()` is expected here** to show output — this is a teaching notebook, not `src/`.
- **pandas (if used):** `.copy()` on derived frames, `.loc[]` for assignment, vectorized
  ops over `.apply()`.

## How to generate the notebook (clean output)

Don't hand-assemble `.ipynb` JSON — it produces malformed cells and noisy diffs. Instead:

1. Write the full guide as a `.py` with `# %%` markers (`# %% [markdown]` for prose cells).
2. Convert with **jupytext**: `jupytext --to notebook NN_topic_name_reference.py`.
3. Keep the `.py` as the source of truth; regenerate the `.ipynb` from it on later edits.

## Definition of done

- [ ] Title + emoji + Table of Contents
- [ ] Every section: conceptual note + ASCII banner + runnable example
- [ ] Real-world usage and a realistic domain example included
- [ ] Common mistakes / anti-patterns / "when not to use" covered
- [ ] Version requirements noted where relevant
- [ ] Functions and classes have NumPy docstrings + type hints
- [ ] Final Quick Reference cheat-sheet cell
- [ ] Runs top to bottom without errors; file named `NN_topic_name_reference.ipynb`
