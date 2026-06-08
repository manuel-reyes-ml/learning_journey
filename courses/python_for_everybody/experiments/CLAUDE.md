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
- **Never modify my source learning module.** Each topic is built from an existing Python
  module — the `.py` you read the material *from*. That file is strictly **read-only**: read
  it to understand what to teach and mine it for content, but never edit, rename, move, or
  delete it. Your only deliverable is the `.ipynb` notebook (plus its own build file, below).
- **Improve explanations whenever it helps me learn.** If a clearer wording, an extra
  example, an analogy, or more description would make a concept land better, add it — err
  toward more teaching, never strip detail just to be concise.

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
   summary, a `---` rule, then a **`## Table of Contents`** heading (a real heading, not bold
   text) with a numbered list linking each section, e.g. `1. [Why Type Hints?](#1-why-type-hints)`.
2. **Before each topic — markdown section header:** start the cell with a `---` horizontal
   rule, then `## N. <Section Name>`, then a conceptual note (what it is, why it exists, when
   to use it). The `---` divider between sections is part of the look — include it every time.
3. **Code cells — top-level demonstrations**, each opened with an ASCII banner comment:
   ```python
   # =============================================================================
   # SHORT TOPIC LABEL
   # =============================================================================
   ```
   The banner is a concise topic label (`PRIMITIVE TYPES`, `NESTED COLLECTIONS`) — not
   `SECTION N — ...`. Show each idea at module level so running the cell shows the result.
4. **Imports go inline**, in the code cell that first needs them (as notebook 18 does). Do
   **not** add a standalone "0. Imports" section. `from __future__ import annotations` goes
   at the top of the first code cell.
5. **Last cell — markdown "Quick Reference":** a fenced `# ====` cheat-sheet of the topic's
   syntax for fast lookup.

**File naming:** `NN_topic_name_reference.ipynb` — two-digit zero-padded, snake_case.

### Cell granularity (the #1 thing to get right)

Notebook 18 has **many small code cells** — roughly 3–5 per section, each demonstrating
**one idea** under its own ASCII banner. **Do the same. Never put a whole section in one
giant code cell.** If a section's code cell is more than ~30–40 lines, split it: one concept
per cell, each independently runnable, with a short markdown note between cells when a
sub-idea needs framing. The goal is that I can run and study one idea at a time, top to
bottom — not scroll through a 150-line block.

### Heading levels (match 18's rhythm — this is what looks like "font size")

Markdown has no font sizes; rendered size comes only from heading level. Match 18 exactly:

- **H1 (`#`)** — the notebook title only. Once per notebook. Keep the title plain text
  (avoid inline-code backticks in it, or that word renders in a different monospace size).
- **H2 (`##`)** — section headers (`## N. …`), plus `## Table of Contents` and
  `## Quick Reference`. Nothing else.
- **H3 (`###`)** — rare. Only for a genuine named sub-topic, the way 18 uses it about twice.
- **Minor lead-ins use bold, not headings.** "Mental model", "Structure", "How it works",
  "Key insight", etc. should be `**bold text**` on their own line — NOT `### headings`.
  Over-using `###` is exactly what makes a notebook's heading sizes look inconsistent
  next to 18.
- Never use a bare `#` line for emphasis outside a fenced code block — it becomes a heading.

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

## Description density — maximize the learning content (explain generously)

This is the whole point of the folder: I study these to learn **how the feature works and
why it behaves that way**, so generate as much genuine teaching content as is useful. When
in doubt, explain more — never trim a helpful explanation to keep the notebook short.

- Rich conceptual prose in markdown cells: what it is, **how it works under the hood, and
  why** — plus when to use it and the trade-offs.
- **Heavy inline comments inside code cells** — annotate the lines that teach something:
  what each call does, what to notice in the output, why it's written this way. Go beyond
  function-level docstrings; comment within the code itself.
- Show or note the expected output next to the code where it aids understanding.

## Narration → markdown, not `print()`

The source module narrates with `print()` because it runs as a script. When you build the
notebook, **don't copy that narration into code cells** — lift it into markdown:

- **Static explanatory text → markdown.** Headers, step-by-step lists, conceptual notes,
  pseudo-code, "what Python does behind the scenes," lists of real-world examples — write
  these as formatted markdown prose (use a fenced code block for pseudo-code). It reads far
  better than console output and becomes part of the document.
- **Keep `print()` only for real runtime output** — a computed value, or output that
  demonstrates actual execution order/behavior (e.g. the ①–⑩ trace fired from inside the
  generator).
- **Quick test:** *does this line need the code to run to be true?* No → it's narration →
  move it to markdown. Yes (it interpolates a real value or proves execution order) → keep
  the `print()`.

## Python code standards (apply to all code you write)

- `from __future__ import annotations` in the first code cell — IPython applies it to the
  whole session (PEP 604 unions, forward references).
- **Type hints everywhere**, PEP 604 unions (`str | None`, not `Optional[str]`).
- **NumPy-style docstrings** on every function/class (Parameters / Returns / Raises /
  Examples) — in addition to, not instead of, inline comments.
- **Naming:** `snake_case` functions/vars, `PascalCase` classes, `SCREAMING_SNAKE_CASE`
  constants.
- **`print()` only for real output** — computed values or demonstrating execution order.
  Never use it to narrate; narration goes in markdown (see "Narration → markdown").

## How to generate the notebook (clean, notebook-native)

Author as a `.py` in **jupytext percent format**, then convert — but write it as cells, not
as a script. This build file is the notebook's **own** scratch artifact
(`NN_topic_name_reference.py`); it is never my source learning module, which stays read-only.

1. Use explicit markers: `# %% [markdown]` for every prose cell (title, TOC, section
   headers, Quick Reference) and `# %%` for each code cell.
2. In `# %% [markdown]` cells, prefix each markdown line with `# ` (jupytext requirement);
   write real markdown — `#`, `##`, lists, TOC links.
3. In `# %%` code cells, write top-level runnable code with dense inline comments — no
   `def section_…()` wrappers, no `main()`.
4. Convert: `jupytext --to notebook NN_topic_name_reference.py`.
5. The deliverable is the `.ipynb`. If you revise the notebook, edit its build file and
   regenerate — but **never** edit, overwrite, or rename my source learning module.

## Definition of done

- [ ] Markdown title cell with emoji + clickable Table of Contents
- [ ] Each section: `## N.` markdown header + conceptual note + ASCII-banner code cell
- [ ] Sections split into several small code cells (~3–5), one idea each — no giant cells
- [ ] `---` divider above the TOC and above every section header; TOC is a `##` heading
- [ ] Imports inline where first used — no standalone "0. Imports" section
- [ ] Heading levels match 18: H1 = title only, H2 = sections/TOC/Quick Reference, H3 rare; minor lead-ins are **bold**, not `###`
- [ ] Code is top-level and runnable — NO `def section_…()`, `main()`, or `__main__`
- [ ] At least one ASCII diagram for any flow/lifecycle/structure concept
- [ ] Dense inline comments throughout the code cells
- [ ] Narration moved to markdown — `print()` used only for real runtime output, not static text
- [ ] As much how-it-works/why teaching content as is useful — nothing trimmed for brevity
- [ ] Real-world usage + a realistic domain example + common pitfalls covered
- [ ] Version requirements noted; functions/classes have NumPy docstrings + type hints
- [ ] Final markdown Quick Reference cheat-sheet cell
- [ ] Runs top to bottom without errors; named `NN_topic_name_reference.ipynb`
- [ ] Compared side by side against `18_python_type_system_reference.ipynb`; structure matches
- [ ] My source learning module is unchanged — only the `.ipynb` (and its build file) were created