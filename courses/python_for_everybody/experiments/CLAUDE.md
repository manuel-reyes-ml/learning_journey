# CLAUDE.md — Python Learning Notebooks (`experiments/`)

<!-- Scoped to learning_journey/courses/python_for_everybody/experiments/.
     HTML comments are stripped from Claude's context, so notes here cost no tokens. -->

## What this folder is

This folder holds **reference notebooks** — numbered `.ipynb` study guides that teach one
Python feature, class, function, or library (e.g. `18_python_type_system_reference.ipynb`).
I read them later to learn the topic in depth. **You author these completely** — they are
teaching material you produce, not code I hand-write.

## Canonical reference — `18_python_type_system_reference.ipynb`

`18_python_type_system_reference.ipynb` (in this folder) is the **gold standard**. Treat it
as the template for every new notebook:

- **Open and read it first** before building a new guide, so you match its cell layout,
  heading style, tone, and depth.
- **Compare the finished notebook against it side by side** before you call the work done —
  cell types, title + TOC, `## N.` section headers, ASCII-banner code cells, and the final
  Quick Reference cheat sheet should all line up. If anything diverges from 18's structure,
  fix it to match before handing it over.

## Your job here (important — this folder is the exception)

In my project codebases under `src/`, I write the code myself and you guide me block by
block ("no vibe coding"). **This folder is the opposite of that rule.** Here:

- **Write the entire notebook**, start to finish, for whatever topic I name.
- Aim for a **comprehensive, study-ready reference**, not a minimal demo. Depth and clarity
  beat brevity — I use this to actually learn the feature and how it works.
- **Teach as you go.** Every section pairs plain-language explanation with runnable code.

## Research & depth (what makes a good guide)

- **Use current, idiomatic practices** for the topic, and note version requirements
  (e.g. "3.10+", "3.12 `type` statement"). Prefer modern syntax: PEP 585 builtin generics
  (`list[int]`), PEP 604 unions (`X | Y`), `pathlib` over `os.path`.
- **Verify the current API.** For a library or stdlib module, check its official
  documentation so signatures, methods, and recommended patterns are up to date.
- **Show real-world usage**: idiomatic patterns, how the stdlib or popular libraries use the
  feature, plus a realistic finance/data example where it fits naturally.
- **Cover the edges:** common mistakes, gotchas, anti-patterns, and when *not* to use it.

## Notebook format — match `18_python_type_system_reference.ipynb` EXACTLY

This is a **notebook-native teaching document, NOT a runnable script that was converted.**
The one rule everything else follows from: **markdown cells carry the prose; code cells are
top-level, directly runnable demonstrations.**

1. **First cell — markdown title:** `# 🔷 <Topic> — Complete Reference Guide`, a one-line
   summary, then a **Table of Contents**: a numbered markdown list linking to each section,
   e.g. `1. [Why Type Hints?](#1-why-type-hints)`.
2. **Before each topic — markdown section header:** `## N. <Section Name>`, followed by a
   conceptual note (what it is, why it exists, when to use it). Real markdown headings only.
3. **Code cells — top-level demonstrations**, each opened with an ASCII banner comment:
   ```python
   # =============================================================================
   # SECTION NAME
   # =============================================================================
   ```
   Show each idea at module level so running the cell immediately shows the result.
4. **Last cell — markdown "Quick Reference":** a fenced `# ====` cheat-sheet of the topic's
   syntax for fast lookup.

**File naming:** `NN_topic_name_reference.ipynb` — two-digit zero-padded, snake_case.

### Do NOT (these are the exact mistakes from `27_…`)

- ❌ Don't wrap demonstrations in `def section_1_…()`, `def main()`, or
  `if __name__ == "__main__"`. That is a script, not a notebook. Code cells run top-level.
- ❌ Don't put the title/overview inside a code-cell `"""docstring"""`. Title and TOC are
  **markdown** cells.
- ❌ Don't paste `=====` rules into markdown cells as fake headers — they don't render as
  headings, which is why the look/"font" drifts from notebook 18. Use `#` / `##`.

## Diagrams (build them from comments)

Wherever a concept has flow, order, or structure, include an **ASCII diagram** to make it
visual — inside a code-cell comment or a markdown cell. I want more of these:

- Execution / lifecycle flow (the numbered ①②③ `@contextmanager` trace was good — do that).
- Mental-model sketches (e.g. the "bouncer" `with`-block diagram).
- Object/class relationships, state transitions, call order.

Label each step and keep the art aligned so it reads cleanly in monospace.

## Description density (explain generously — I study this later)

- Rich conceptual prose in markdown cells: what, why, when, trade-offs.
- **Heavy inline comments inside code cells** — annotate the lines that teach something:
  what each call does, what to notice in the output, why it's written this way. Go beyond
  function-level docstrings; comment within the code itself.
- Show or note the expected output next to the code where it aids understanding.

## Python code standards (apply to all code you write)

- `from __future__ import annotations` in the first code cell — IPython applies it to the
  whole session (PEP 604 unions, forward references).
- **Type hints everywhere**, PEP 604 unions (`str | None`, not `Optional[str]`).
- **NumPy-style docstrings** on every function/class (Parameters / Returns / Raises /
  Examples) — in addition to, not instead of, inline comments.
- **Naming:** `snake_case` functions/vars, `PascalCase` classes, `SCREAMING_SNAKE_CASE`
  constants.
- **`print()` is expected here** to show output — this is a teaching notebook, not `src/`.

## How to generate the notebook (clean, notebook-native)

Author as a `.py` in **jupytext percent format**, then convert — but write it as cells, not
as a script:

1. Use explicit markers: `# %% [markdown]` for every prose cell (title, TOC, section
   headers, Quick Reference) and `# %%` for each code cell.
2. In `# %% [markdown]` cells, prefix each markdown line with `# ` (jupytext requirement);
   write real markdown — `#`, `##`, lists, TOC links.
3. In `# %%` code cells, write top-level runnable code with dense inline comments — no
   `def section_…()` wrappers, no `main()`.
4. Convert: `jupytext --to notebook NN_topic_name_reference.py`.
5. Keep the `.py` as source of truth; regenerate the `.ipynb` on edits.

## Definition of done

- [ ] Markdown title cell with emoji + clickable Table of Contents
- [ ] Each section: `## N.` markdown header + conceptual note + ASCII-banner code cell
- [ ] Code is top-level and runnable — NO `def section_…()`, `main()`, or `__main__`
- [ ] At least one ASCII diagram for any flow/lifecycle/structure concept
- [ ] Dense inline comments throughout the code cells
- [ ] Real-world usage + a realistic domain example + common pitfalls covered
- [ ] Version requirements noted; functions/classes have NumPy docstrings + type hints
- [ ] Final markdown Quick Reference cheat-sheet cell
- [ ] Runs top to bottom without errors; named `NN_topic_name_reference.ipynb`
- [ ] Compared side by side against `18_python_type_system_reference.ipynb`; structure matches