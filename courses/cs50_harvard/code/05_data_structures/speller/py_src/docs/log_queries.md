# Speller Log Queries — `jq` Cookbook

Practical `jq` recipes for analysing structured log output from the speller's
`--structured-logging` mode. Every query in this document has been verified
against real NDJSON log output from the speller package.

> **What this file is.** A reference of high-value `jq` one-liners for
> debugging, benchmarking, and reporting on speller runs.
>
> **What it isn't.** A `jq` language tutorial. For that, see the
> [official jq manual](https://jqlang.org/manual/) or the
> [jq Playground](https://jqplay.org) to experiment in a browser.

---

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [The Log Format](#the-log-format)
3. [Reading and Pretty-Printing](#reading-and-pretty-printing)
4. [Filtering by Severity](#filtering-by-severity)
5. [Filtering by Event Type](#filtering-by-event-type)
6. [Filtering by Fields](#filtering-by-fields)
7. [Reshaping Output](#reshaping-output)
8. [Exporting to CSV / TSV](#exporting-to-csv--tsv)
9. [Counting and Aggregation](#counting-and-aggregation)
10. [Math and Performance Analysis](#math-and-performance-analysis)
11. [Time-Range Queries](#time-range-queries)
12. [Live Tailing](#live-tailing)
13. [Using in Shell Scripts and CI](#using-in-shell-scripts-and-ci)
14. [Shell Aliases](#shell-aliases)
15. [Further Reading](#further-reading)

---

## Prerequisites

### Install `jq`

```bash
# macOS
brew install jq

# Debian / Ubuntu
sudo apt install jq

# Windows
winget install jqlang.jq
```

Verify:

```bash
jq --version
# jq-1.7  (or later)
```

### Generate a log file

Run the speller in structured-logging mode against the `texts/` directory with
multiple backends, which produces events worth querying:

```bash
speller -s --ops hash sorted --dir texts/
```

After the run, `logs/speller_structured.log` will contain one JSON object per
line (NDJSON). All subsequent examples assume that file exists.

---

## The Log Format

Each line in the log is a single JSON object emitted by the `structlog`
processor chain. Fields are rendered in this order (configured via
`_reorder_keys` in `structured_logger.py`):

```json
{
  "timestamp": "2026-04-22T18:33:01.305Z",
  "level": "info",
  "logger": "speller.speller",
  "event": "spell_check_complete",
  "file": "austen.txt",
  "backend": "HashTableDictionary",
  "operation": "hash",
  "words_misspelled": 1614,
  "words_in_text": 125203,
  "check_time_s": 0.147
}
```

**Core fields (always present):**

| Field | Type | Description |
|---|---|---|
| `timestamp` | ISO-8601 string | Event time, UTC |
| `level` | string | `debug`, `info`, `warning`, `error`, `critical` |
| `logger` | string | Emitting module, e.g. `speller.load_dictionary` |
| `event` | string | Event label or message |

**Context-bound fields** (from `bind_contextvars` in `__main__.py`, present on
every event inside the per-file loop):

| Field | Type | Description |
|---|---|---|
| `file` | string | Text file being processed |
| `backend` | string | Dictionary class name, e.g. `HashTableDictionary` |
| `operation` | string | CLI `--ops` value, e.g. `hash`, `sorted`, `list`, `dict` |

**Event-specific fields** (vary by event; see individual recipes below):

- `dictionary_load`: `word_count`, `path`, `load_time_s`
- `spell_check_complete`: `words_misspelled`, `words_in_text`, `check_time_s`
- `dictionary_load_failed`: `path`, `error`

---

## Reading and Pretty-Printing

### Pretty-print the whole file

The identity filter `.` outputs each event indented and colored.

```bash
jq '.' logs/speller_structured.log
```

```json
{
  "timestamp": "2026-04-22T18:33:01.274Z",
  "level": "info",
  "logger": "speller.load_dictionary",
  "event": "dictionary_load",
  "backend": "HashTableDictionary",
  "word_count": 143091,
  "path": "/dictionaries/large",
  "load_time_s": 0.032
}
...
```

### View just the last N events

```bash
tail -n 20 logs/speller_structured.log | jq '.'
```

### Page through a long log

```bash
jq -C '.' logs/speller_structured.log | less -R
```

`-C` forces colored output even when piping; `less -R` preserves ANSI color codes.

---

## Filtering by Severity

### Errors only

```bash
jq 'select(.level == "error")' logs/speller_structured.log
```

```json
{
  "timestamp": "2026-04-22T18:33:06.470Z",
  "level": "error",
  "logger": "speller.load_dictionary",
  "event": "dictionary_load_failed",
  "path": "/dictionaries/missing",
  "error": "FileNotFoundError"
}
```

### Warnings and errors

```bash
jq 'select(.level == "warning" or .level == "error")' logs/speller_structured.log
```

### Everything except debug

```bash
jq 'select(.level != "debug")' logs/speller_structured.log
```

---

## Filtering by Event Type

### Only spell-check completion events

```bash
jq 'select(.event == "spell_check_complete")' logs/speller_structured.log
```

### Only dictionary load events

```bash
jq 'select(.event == "dictionary_load")' logs/speller_structured.log
```

### Pattern-match events (regex)

```bash
jq 'select(.event | test("spell_check"))' logs/speller_structured.log
```

`test(regex)` returns true if the string matches; case-sensitive by default. Add
`"i"` as second arg for case-insensitive: `test("ERROR"; "i")`.

---

## Filtering by Fields

### All events for a specific file

```bash
jq 'select(.file == "austen.txt")' logs/speller_structured.log
```

### All events for a specific backend

```bash
jq 'select(.backend == "HashTableDictionary")' logs/speller_structured.log
```

### Slow operations only (check_time_s > 1 second)

```bash
jq 'select(has("check_time_s") and .check_time_s > 1)' logs/speller_structured.log
```

The `has(key)` guard prevents errors when the field is missing on events that
don't emit it (like `dictionary_load`).

### Texts with any misspellings

```bash
jq 'select(.words_misspelled > 0)' logs/speller_structured.log
```

### Combining filters with AND / OR

```bash
# HashTable backend AND took more than 100ms
jq 'select(.backend == "HashTableDictionary" and .check_time_s > 0.1)' \
  logs/speller_structured.log

# cat.txt OR constitution.txt
jq 'select(.file == "cat.txt" or .file == "constitution.txt")' \
  logs/speller_structured.log
```

---

## Reshaping Output

### Extract a subset of fields

```bash
jq 'select(.event == "spell_check_complete") | {file, backend, check_time_s}' \
  logs/speller_structured.log
```

```json
{"file": "cat.txt", "backend": "HashTableDictionary", "check_time_s": 0.0001}
{"file": "austen.txt", "backend": "HashTableDictionary", "check_time_s": 0.147}
{"file": "austen.txt", "backend": "SortedListDictionary", "check_time_s": 2.314}
```

Note the syntax `{file, backend, check_time_s}` is shorthand for
`{file: .file, backend: .backend, check_time_s: .check_time_s}`.

### Rename fields while extracting

```bash
jq 'select(.event == "spell_check_complete")
    | {when: .timestamp, backend, file, time_s: .check_time_s}' \
  logs/speller_structured.log
```

### Compact (single-line) output with `-c`

Useful for re-writing filtered logs back to a file as valid NDJSON:

```bash
jq -c 'select(.backend == "HashTableDictionary")' \
  logs/speller_structured.log \
  > logs/hash_only.log
```

---

## Exporting to CSV / TSV

### CSV with a header row

```bash
echo "backend,file,words_misspelled,words_in_text,check_time_s"
jq -r 'select(.event == "spell_check_complete")
       | [.backend, .file, .words_misspelled, .words_in_text, .check_time_s]
       | @csv' \
  logs/speller_structured.log
```

Output:

```
backend,file,words_misspelled,words_in_text,check_time_s
"HashTableDictionary","cat.txt",0,6,0.0001
"HashTableDictionary","austen.txt",1614,125203,0.147
"HashTableDictionary","constitution.txt",45,7591,0.009
"SortedListDictionary","cat.txt",0,6,0.0015
"SortedListDictionary","austen.txt",1614,125203,2.314
"SortedListDictionary","constitution.txt",45,7591,0.142
```

Redirect to a file and open in Excel / pandas / Google Sheets:

```bash
jq -r 'select(.event == "spell_check_complete")
       | [.backend, .file, .words_misspelled, .check_time_s]
       | @csv' \
  logs/speller_structured.log \
  > reports/benchmark.csv
```

### TSV (tab-separated)

Preferred when values may contain commas:

```bash
jq -r 'select(.event == "spell_check_complete")
       | [.backend, .file, .check_time_s]
       | @tsv' \
  logs/speller_structured.log
```

Flags explained:

- `-r` — **raw** output; strips JSON string quotes
- `@csv` — CSV-escapes values and quotes strings
- `@tsv` — tab-joins values (no quoting)

---

## Counting and Aggregation

### Count events by type

```bash
jq -r '.event' logs/speller_structured.log | sort | uniq -c | sort -rn
```

```
      6 spell_check_complete
      2 dictionary_load
      1 dictionary_load_failed
      1 Structured (structlog) logging mode enabled
      1 Skipping file: bad_encoding
      1 Running Speller with 'HashTableDictionary'
      1 Program completed.
```

### Count events by severity level

```bash
jq -r '.level' logs/speller_structured.log | sort | uniq -c
```

```
      1 debug
      1 error
     10 info
      1 warning
```

### Count events matching a condition

```bash
jq -s '[.[] | select(.event == "spell_check_complete" and .check_time_s > 0.1)]
       | length' \
  logs/speller_structured.log
```

The `-s` flag (**slurp**) reads all events into a single array so you can
aggregate across them. Without `-s`, `jq` processes one event at a time.

---

## Math and Performance Analysis

### Compare backends — sum, average, count per backend

This is the core benchmark query. It mirrors what your speller's
`BenchmarkResult` would show, but computed from the logs:

```bash
jq -s '[.[] | select(.event == "spell_check_complete")]
       | group_by(.backend)
       | map({
           backend: .[0].backend,
           files_processed: length,
           total_check_time_s: (map(.check_time_s) | add),
           avg_check_time_s: ((map(.check_time_s) | add) / length)
         })' \
  logs/speller_structured.log
```

```json
[
  {
    "backend": "HashTableDictionary",
    "files_processed": 3,
    "total_check_time_s": 0.1561,
    "avg_check_time_s": 0.0520
  },
  {
    "backend": "SortedListDictionary",
    "files_processed": 3,
    "total_check_time_s": 2.4575,
    "avg_check_time_s": 0.8192
  }
]
```

### Find the fastest and slowest runs

```bash
jq -s '[.[] | select(.event == "spell_check_complete")]
       | sort_by(.check_time_s)
       | {fastest: .[0], slowest: .[-1]}' \
  logs/speller_structured.log
```

### Compute misspelling rate per file

```bash
jq 'select(.event == "spell_check_complete")
    | {
        file,
        backend,
        misspell_rate_pct: ((.words_misspelled / .words_in_text * 100 * 100 | round) / 100)
      }' \
  logs/speller_structured.log
```

```json
{"file": "cat.txt", "backend": "HashTableDictionary", "misspell_rate_pct": 0}
{"file": "austen.txt", "backend": "HashTableDictionary", "misspell_rate_pct": 1.29}
{"file": "constitution.txt", "backend": "HashTableDictionary", "misspell_rate_pct": 0.59}
```

The `(x * 100 | round) / 100` trick rounds to two decimal places — `jq` has no
built-in rounding operator, so this is the idiomatic workaround.

### List dictionary load times by backend

```bash
jq -s '[.[] | select(.event == "dictionary_load")]
       | map({backend, load_time_s})' \
  logs/speller_structured.log
```

```json
[
  {"backend": "HashTableDictionary", "load_time_s": 0.032},
  {"backend": "SortedListDictionary", "load_time_s": 1.823}
]
```

---

## Time-Range Queries

ISO-8601 timestamps sort correctly as strings, so range filtering is just string
comparison:

### Events within a 5-second window

```bash
jq 'select(.timestamp >= "2026-04-22T18:33:05"
           and .timestamp <  "2026-04-22T18:33:10")' \
  logs/speller_structured.log
```

### Last hour's errors (replace with a real timestamp)

```bash
jq 'select(.level == "error" and .timestamp >= "2026-04-22T17:30:00Z")' \
  logs/speller_structured.log
```

### Events after a specific run started

```bash
# Pass a timestamp via shell variable
START="2026-04-22T18:33:05Z"
jq --arg start "$START" 'select(.timestamp >= $start)' \
  logs/speller_structured.log
```

`--arg NAME VALUE` passes a shell variable into the jq program as `$NAME`.
Always use this instead of interpolating into the filter string — it handles
escaping correctly.

---

## Live Tailing

### Pretty-print new events as they arrive

```bash
tail -f logs/speller_structured.log | jq '.'
```

### Tail only errors in real-time

```bash
tail -f logs/speller_structured.log | jq 'select(.level == "error")'
```

### Tail with colored output

```bash
tail -f logs/speller_structured.log | jq -C '.'
```

---

## Using in Shell Scripts and CI

### Exit code: error detection with `-e`

`jq -e` exits with code **0** if the filter produces any truthy value,
**1** if not. This makes `jq` usable as a test in CI pipelines:

```bash
if jq -e 'select(.level == "error")' logs/speller_structured.log > /dev/null; then
    echo "✗ Errors found in log — failing the build"
    exit 1
else
    echo "✓ No errors in log"
fi
```

### Extract a single value into a shell variable

Use `-r` so the result isn't wrapped in JSON quotes:

```bash
SLOWEST_FILE=$(jq -rs '
  [.[] | select(.event == "spell_check_complete")]
  | sort_by(.check_time_s)
  | .[-1].file
' logs/speller_structured.log)

echo "Slowest file was: $SLOWEST_FILE"
```

### Assert a benchmark doesn't regress

```bash
# Fail the build if any spell check took longer than 5 seconds
if jq -e '[.[] | select(.event == "spell_check_complete" and .check_time_s > 5)]
          | length > 0' logs/speller_structured.log > /dev/null; then
    echo "✗ Performance regression detected"
    exit 1
fi
```

This pattern is exactly how GitHub Actions workflows assert on log contents —
useful once you're wiring up CI in Stage 1+ of the roadmap.

---

## Shell Aliases

Add these to your `~/.zshrc` or `~/.bashrc` for daily productivity:

```bash
# Path to the speller log — adjust to your repo location
export SPELLER_LOG="$HOME/dev/projects/learning_journey/courses/cs50_harvard/code/05_data_structures/speller/py_src/logs/speller_structured.log"

# Pretty-print the whole log
alias speller-logs='jq "." "$SPELLER_LOG"'

# Only errors and warnings
alias speller-errors='jq "select(.level == \"error\" or .level == \"warning\")" "$SPELLER_LOG"'

# Only spell_check_complete events, as CSV
alias speller-bench='jq -r "select(.event == \"spell_check_complete\") | [.backend, .file, .check_time_s] | @csv" "$SPELLER_LOG"'

# Live tail
alias speller-tail='tail -f "$SPELLER_LOG" | jq "."'

# Backend comparison summary
alias speller-summary='jq -s "[.[] | select(.event == \"spell_check_complete\")] | group_by(.backend) | map({backend: .[0].backend, files: length, total_time_s: (map(.check_time_s) | add)})" "$SPELLER_LOG"'
```

After sourcing your shell config (`source ~/.zshrc`):

```bash
speller-summary
# → JSON summary of per-backend benchmark times
```

---

## Further Reading

- **[Official jq Manual](https://jqlang.org/manual/)** — the authoritative language reference
- **[jq Playground](https://jqplay.org)** — browser-based REPL for experimenting without installing
- **[jqlang/jq GitHub](https://github.com/jqlang/jq)** — source, binaries, release notes
- **Speller docs:**
  - `src/speller/structured_logger.py` — end-to-end processing flow of how these logs are produced
  - `STRUCTLOG_MIGRATION_NOTES.md` — how the `--structured-logging` flag was wired up

---

## Extending This Cookbook

As new events are added to the speller (at Stage 2+ when you introduce LLM
calls, RAG retrievals, etc.), add the corresponding queries here. Keep the
pattern:

1. Describe the event and its fields
2. Show the query
3. Show real output

This file is a living reference — the more recipes it gathers, the more it
compounds as a portfolio artifact showing that you treat observability as
first-class engineering work.
