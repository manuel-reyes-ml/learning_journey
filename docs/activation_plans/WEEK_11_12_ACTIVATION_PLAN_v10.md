# 🚀 WEEKS 11–12 MASTER ACTIVATION PLAN (v10.0)
## PolicyPulse Opens + The IBM Spine + Month-3 Retro | September 28 – October 11, 2026

**Document Version:** 1.1 (realigned to roadmap Corrections 21–43 — **materially re-scoped**)
**Covers:** Monday, September 28 – Sunday, October 11, 2026 (Stage 1 · Month 3 · Weeks 11–12)
**Aligned To:** Career Roadmap v10.0, **Corrections 1–43**
**Prerequisite:** Weeks 9–10 metrics ≥80% (non-negotiables: harness v1 + documented improve cycle)
**Weekly Hours:** 25 · ⏰ **Pro month expires ~Oct 13 — empty it and cancel it this fortnight (hard deadline).**

> 🤖 **Agent Policy:** Phase 3. PolicyPulse follows the DataVault pattern: requirements-first comment blocks, agents for scaffolding under diff review, retrieval logic + all eval gates + ADRs by hand. End-of-quarter checkpoint: Sunday Day 84's retro includes an honest agent-policy review — where did agents genuinely accelerate you, and where did you accept a line you couldn't fully explain? That answer calibrates Q2's policy.

---

---

## 🔄 REALIGNMENT PASS — ROADMAP CORRECTIONS 21–43 (applied 27 Aug 2026)

**This fortnight changed more than any other.** Corrections 22 and 32 land directly inside it.

> # 🔴 DAY 82 — Friday, 9 October 2026 — is your last day of employment.
> It sits in Week 12 of this plan. Everything below that assumed continuing employment is re-scoped:
> - The **internal 1099 retro-migration** loses *system access* after Day 82 — nine working days, then the live system is gone. 🔄 **Revised on your 27 Aug confirmation that the codebase is not company-private:** the code travels with you, so this is **one continuous project**, not an internal pass plus a public rebuild. Front-load only what is **irrecoverable**: the before-metrics measured against the live system, and the ADRs while the decisions are fresh. ⚠️ The **data** boundary is untouched by that confirmation — synthetic-only in anything public.
> - **Automation win #1 must be drafted Days 78–80** and finalized on Day 82 — not started on Day 82.
> - **Automation win #2 never happens.** There is no Month 4–6 employment to earn it in. Capture both wins now — and get the **code-ownership position in writing** before Day 82 while you can still ask.
> - The **"elevation file"** is renamed the **evidence file**. Audience: a Q1 2027 external interviewer, not a manager.
> - The **Month-6 scope-change conversation is retired** — it cannot occur. Stage 1 now exits on an **evidence gate** (DataVault S2 hardening).
> - A **Day 82 exit checklist** has been added inline (irrecoverable before-metrics, data boundary, written ownership confirmation, contacts, transition log).

**Also applied this fortnight:**
- **🛑 IBM anti-stack warning** (Correction 43): enrol in the **16-course IBM GenAI Engineering PC only**. IBM's separately-marketed *Generative AI Engineering with LLMs* programme is **contained within it** — taking it standalone double-buys the hours for one Tier-4 line, not two. Verify the course count at enrolment (Credly says 13, a 2026 review says 16 — unresolved).
- **🏆 PostCheck is Flagship #4** (Correction 33), and it depends on ERISA distribution-workflow knowledge you are about to lose daily access to. **Capture the SOP surface before Day 82** — see What Comes Next.
- **🐻‍❄️ Polars is the default engine** (Correction 35) for PolicyPulse's ingestion path; pandas only at the two named boundaries.
- **🪝 pre-commit** (Correction 21) belongs in the `policypulse` scaffold on Day 71 — it is part of "the full standard, from memory" now.
- **📖 The reading layer** is live (Correction 34).

> 🗺️ **Harness note (your ruling, 27 Aug 2026): you run a DUAL harness** — OpenCode in Cursor, Claude Code in VS Code, both under one portable `AGENTS.md`. Two Q2 items follow: (a) write `scripts/build_claude_agents.py`, because **Claude Code has no native import for subagent files** and hand-maintaining two copies guarantees drift — treat harness drift as a build failure, exactly as Correction 21 treats hooks disagreeing with CI; (b) **re-check the tool budget.** Correction 40 moved Cursor to Hobby specifically to stop paying twice for agent capacity — running OpenCode Go **and** Claude Code reopens that question, and it should be answered with a number, not a feeling.

> 📝 **ROADMAP CORRECTIONS OWED — three divergences these plans now carry that `roadmap.html` does not.** Under your own governance the file must record them, with falsifiers; otherwise the plans are ahead of the roadmap and the roadmap stops being authoritative. **Correction 42's number is reserved and unwritten** — these are candidates for it and the two following:
> 1. **Harness:** Correction 39 rules OpenCode the *sole* harness and Claude Code *evaluated and declined*. Reality is dual. Needs reversal + the `AGENTS.md` / generator-script standard recorded. *Falsifier: if maintaining two harnesses produces drift the generator cannot absorb, collapse to one.*
> 2. **AB-620:** Correction 37 lists it conditional. You have committed it. Needs a status change + the extra-time-hours ruling. *Falsifier: if AE/DE applications never surface Azure-stack requirements, it does not get re-bought at renewal.*
> 3. **Hours model:** frozen at 25/week pending the Correction 22 deferral. You have now authorised ~4 hrs/week of extra-time threads. Needs recording as an explicit exception with the cap and the pause rule, not left as an undocumented overrun. *Falsifier: actual > ~29 hrs/week or the 4:30 AM trend degrading → threads pause.*

> 🧭 **The honest reframe.** This plan's closing line called the Month-6 conversation "the deliverable every artifact this quarter was quietly building toward." That is no longer true, and the substitute is not a downgrade: the artifacts were always the point, and they now go to a market instead of a manager. Two eval-gated flagships, a CI habit with eleven weeks of commits, a cert, and a regulated-domain story is a **stronger** Q1 2027 position than an internal scope memo would have been. The work does not change. The audience does.

---

## 📊 WHERE YOU STAND
You own an eval harness with dual graders, a CI-gated DE flagship running end-to-end, an AI-901 pass, SDK fluency, and ~11 weeks of daily commits. This fortnight completes the Quarter-1 promise: **both lead flagships alive, eval-gated, and public.**

## 🧠 STRATEGIC CONTEXT

### PolicyPulse S1: what ships and what deliberately doesn't
S1 core = **retrieval that can prove itself**: synthetic policy corpus → chunk → embed → store (ChromaDB) → retrieve → answer with citations — with the RAG Triad eval gate wired from commit one (your Weeks 9–10 harness, graduated). Deliberately NOT in S1: GraphRAG/Neo4j (S3), FastMCP server (S3 — but the MCP *primer* is this fortnight, so the design leaves the seam), per-document access control (S2–S3 layer; note the seam in an ADR).

**Data rule:** the corpus is synthetic policy/handbook text YOU write (or generate with Claude and then *edit* — you must know every claim in your corpus, because your golden questions test against it). Never real plan documents, never employer text.

### The IBM spine begins
The **IBM Generative AI Engineering Professional Certificate** (16 courses, Coursera Plus, ACE-recommended) is your roadmap's Months 3–6 structured spine.

> 🛑 **Correction 43 — anti-stack warning, read before you enrol.** IBM markets a separate *Generative AI Engineering with LLMs* programme (a Specialization on Coursera, described as a Professional Certificate in IBM's promotional email). It is **superseded and contained** within the 16-course PC you are enrolling in — its component courses are flagged by Coursera as "part of multiple programs." **Taking it standalone would double-buy the same hours for zero credential gain** (one Tier-4 line, not two). Enrol in the 16-course PC only. ⚠️ Also verify the course count at enrolment: IBM's Credly badge says 13, a 2026 practitioner review says 16 — the roadmap flags this as unresolved. It starts Week 11 at a sustainable ~3 hrs/week morning-thread pace — a marathon lane next to the build lanes, not a sprint. Early courses will overlap what you've built; per the standing rule, move FAST through overlap (the marginal value early is structure + the credential; depth compounds mid-program).

### The retro-migration pass (Corrections 13/14/16's "named pass") — ⚠️ **NOW A HARD-DEADLINE ITEM**
The 1099 pipeline at work gets its production retro-migration: pip→uv (+ lockfile), structlog with ProcessorFormatter + a PII-redaction processor, first C4 Context diagram (Structurizr DSL → Mermaid), and its first ADRs. ~~**This is internal work on internal systems** — done at work or on the work machine as appropriate, with only sanitized lessons-learned becoming public content.~~ → 🔄 **REVISED (your confirmation, 27 Aug 2026): the codebase is not company-private.** The pipeline itself is portable, so the retro-migration is **one project, publishable**, not an internal exercise with a sanitized shadow. ~~Scheduled here as *started, not finished* — it continues into Q2.~~

> ✅ **What your confirmation changes.** The code can travel with you and can be portfolio evidence. Track A is no longer a salvage operation — it is the first half of one continuous project that finishes on your own machine in Q2.
>
> ⚠️ **What it does NOT change, and this is a different axis entirely.** "The code is not company-private" is a statement about **ownership**. It says nothing about the **data**. The 1099 pipeline processes ERISA-regulated participant records — SSNs, names, DOBs, distribution amounts — and none of that becomes publishable because the code did. **The synthetic-data-only rule for public repos stands unchanged**, as does the three-layer PII defence (`redact_pii` structlog processor + `SecretStr` + display-boundary masking). Take the code; leave every row of real data behind, including in test fixtures, notebook output, log samples, and screenshots. `detect-private-key`, `gitleaks` and `nbstripout` are your commit-time enforcement of exactly this.

> 🔴 **Correction 22 breaks this schedule. Your last day of employment is Friday 9 October 2026 — Day 82 of this very fortnight.** The retro-migration cannot "continue into Q2": after Day 82 you no longer have access to the work machine or the internal system. Two consequences, and they are the reason this plan is re-scoped rather than annotated:
> 1. **Whatever is going to happen on the internal 1099 pipeline must happen in Week 11 and the first four days of Week 12.** Front-load it. Treat Day 82 as a cliff, not a milestone.
> 2. **Take the code AND the record.** 🔄 Revised on your confirmation that the codebase is not company-private — the *code* travels with you, so the earlier "extract documentation only" instruction is withdrawn. What still has to happen before Day 82 is the part you **cannot reconstruct afterwards**: the before-metrics (runtime, memory, row counts, defect counts, manual-touch counts) measured against the live system, plus the ADRs while the decisions are fresh. ⚠️ **The data boundary is unchanged:** no real participant records, no exports, no screenshots containing PII — not in the repo, not in fixtures, not in a notebook cell. Figures in write-ups stay relative ("N hundred corrections caught pre-mailing"), which is good interview practice regardless of permission.
>
> ✅ **YOUR RULING (27 Aug 2026): run the WHOLE retro-migration to completion, even if it takes longer — the goal is a complete production-grade project.** Adopted. It is implemented as **two tracks**, because one hard constraint cannot be ruled away: **after Day 82 you no longer have access to the internal system.** That is a fact about access, not a scoping preference.

**🔴 TRACK A — INTERNAL (`1099` pipeline at work) · HARD STOP: Friday 9 Oct, Day 82.**
Nine working days, alongside a handover. 🔄 **Revised:** since the codebase is not company-private, this is no longer a salvage pass — it is **phase 1 of one continuous project** that you finish on your own machine. Sequence by what is **irrecoverable after Day 82**, not by what looks finished:
1. **Measure the "before" and write it down.** Runtime, memory, row counts, defect counts, manual-touch counts. These numbers become the S2 writeup headline and you cannot recover them after Day 82.
2. **ADRs** — the real decisions and their trade-offs, in your own words.
3. **C4 Context diagram** (Structurizr DSL → Mermaid), sanitized.
4. **pip→uv + structlog PII redaction** on the internal copy — valuable if it lands, **abandon without guilt if Day 82 arrives first.**
⚠️ **Data boundary (unchanged by the ownership confirmation):** no real participant data leaves with you — no client identifiers, no exports, no PII in fixtures or notebook output. Write-up figures stay relative. 📌 **One thing to close before Day 82:** get the code-ownership position **in writing** (a one-line email to your manager or HR confirming you may retain and publish the pipeline code). You are confident it is fine, and it very likely is — but a written confirmation obtained while you are still employed costs one email, and reconstructing it in Q1 2027 while an employer's counsel reads your public GitHub costs considerably more. Treat it as the same instinct as the RPF written-determination ask.

**🟢 TRACK B — PUBLIC (`1099_reconciliation_pipeline`, your repo) · NO DEADLINE · THIS IS THE COMPLETE PRODUCTION-GRADE PROJECT.**
This is the one that satisfies your ruling, because it is the only one you still control after Day 82 and the only one an interviewer can open. It **starts in Week 12 and continues into Q2 until finished** — the full standard, nothing partial:

| # | Item | Correction | Note |
|---|---|---|---|
| 1 | `requirements.txt` → `pyproject.toml` + **committed `uv.lock`**; delete pip/venv install instructions | 13 | The standing top-of-backlog item |
| 2 | Fix the **broken clone-command slug**, the **stale bio**, and the **superseded roadmap link** | 32 | A broken clone command is the first thing a reviewer hits |
| 3 | `src/` layout + `py.typed` + ruff + mypy + pytest | standard | |
| 4 | **Python 3.14** floor, single-source `requires-python` + 4 consumers | 28 | Same pattern as the Day 41 retrofit |
| 5 | **pre-commit** Tier A + `nbstripout` if notebooks; strict subset of CI | 21 | |
| 6 | **structlog** ProcessorFormatter + PII-redaction processor, with a `capture_logs` test asserting a fake SSN never appears | 16 | `cache_logger_on_first_use=False` in tests |
| 7 | **pydantic-settings** with `SecretStr`; **stamina** retries | standard | |
| 8 | **Dockerfile** (two-stage, `uv sync --frozen`) + **CI** blocking gate + badge | standard | |
| 9 | **`docs/adr/`** (Nygard) + **C4 Context** via Structurizr DSL → Mermaid | 14 | Single-source diagram pattern |
| 10 | **README** in ①Production / ②Cost / ③Architecture order, honest claims only | 18 | |
| 11 | **Conventional Commits** throughout | standard | |

> 🛑 **What Track B explicitly does NOT include — and this is a ruling, not an omission.** **Do not rewrite the pipeline in Polars.** Correction 35 §3 freezes the shipped 1099 pipeline as the **"before"**: it is live and production-evidenced, and churning working code is not evidence. The runtime/memory delta against a *future* Polars implementation is a headline metric for the S2 writeup — spend it there, not here. Retro-migration means **raising the tooling and documentation to the production standard**, not re-engineering what already works. Same shape as PostCheck's deterministic-parser-vs-flattened-baseline story.

> ⏱️ **Honest scope note.** Track B is realistically **12–20 hours**, which does not fit in Week 12 next to PolicyPulse's opening, the Month-3 retro and your last day of work. It is **scheduled to start Week 12 and finish in Q2** — that is what "even if it takes a little longer" means in practice. Do not compress it; a half-migrated public repo reads worse than an honest un-migrated one, because it looks abandoned rather than pending.

### And the evidence file gets its keystone
**Internal automation win #1, documented** — the story you identified on Day 70, written with a quantified outcome. ~~Jen-readable framing~~ → **interviewer-readable framing**: this is no longer an exhibit for an internal scope conversation (Correction 22 closed that), it is a **STAR story for the Q1 2027 AE/DE interviews** and the anchor of your FDE discovery-and-decomposition round. Reframe accordingly — lead with the problem shape and the decomposition, not with the internal politics. The 450+-corrections pattern is still the template. Deposition test applies: mechanism and relative outcomes, no client identifiers, no absolute dollar figures.

> ⏰ **Write this before Day 82, not on it.** Day 82 is your last day; you will not have access to the system to check a figure afterwards. **Move the drafting to Day 78–80 and use Day 82 only to finalize.**

### New concepts
```
RAG:    chunking strategies · embeddings at corpus scale · ChromaDB · retrieval
        with citations · RAG Triad gates on YOUR system
MCP:    protocol concepts — tools/resources/prompts, client-server (Academy primer)
Arch:   Structurizr DSL → C4 Context · ProcessorFormatter + redaction processor
        (the full Correction 16 pattern, on the retro-migration)
```

---

## 🗓 WEEK 11 (Sep 28 – Oct 4)

### Week 11 goals
```
□ policypulse repo: full production scaffold + CI (from memory — third time now)
□ Synthetic corpus (12+ docs) + chunker with tests
□ Embeddings + ChromaDB store + retrieval v0 returning cited chunks
□ IBM GenAI PC: enrolled, Course 1 started      □ MCP primer (Academy) started
□ Remaining S2 short labs done + downloaded     □ Post #11
```

### 📌 DAY 71 — Monday, September 28
**Morning:** IBM GenAI PC — enroll; Course 1 first modules (fast through overlap). Then scope PolicyPulse: `docs/SCOPE_v0.1.md` (S1 boundary above, S1→S3 arc, corpus rule) — 30-min cap.
**Evening:**
- [ ] 60 min — Scaffold `policypulse` (full standard, from memory: uv, src/ + py.typed, ruff+mypy+pytest, structlog, pydantic-settings, CI, docs/adr/, README P/C/A stubs). Target: under an hour — scaffolding speed is itself a skill metric now.
- [ ] 40 min — **Corpus v1**: draft 4 of 12+ synthetic policy docs (`data/corpus/*.md` — e.g., eligibility, vesting, loans, hardship-withdrawal policies for the invented "Meridian Manufacturing 401(k) Plan"). Make claims SPECIFIC and internally consistent ("employees become eligible after 90 days and age 21") — specific claims are what retrieval evals can verify against.
- [ ] 20 min — Journal + commit (`chore: scaffold policypulse + corpus v1 start`)

### 📌 DAY 72 — Tuesday, September 29
**Morning:** IBM PC Course 1 continue.
**Evening:**
- [ ] 70 min — **The chunker** ⭐ `src/policypulse/ingest/chunker.py`:

```python
"""Chunking — the highest-leverage, least-glamorous decision in RAG.

Why chunk at all: embeddings represent a passage as ONE vector. Too big a
passage = a blurry average of many topics (retrieval finds mush). Too
small = fragments with no context ("the waiting period" — for what?).
Chunk size is a real trade-off you will defend in interviews; that makes
it ADR 0002 material, with the eval harness as the referee.
"""

from dataclasses import dataclass

import structlog

log = structlog.get_logger()


@dataclass(frozen=True)          # frozen = immutable — chunks are facts, not state
class Chunk:
    doc_id: str                  # provenance: which document...
    chunk_index: int             # ...and where in it. Provenance is what
    text: str                    # makes CITATIONS possible — and citations
    heading: str | None          # are what make RAG auditable. Non-negotiable
                                 # in a compliance-adjacent system.


def chunk_markdown(
    doc_id: str,
    text: str,
    max_chars: int = 1200,       # starting policy — the eval harness will judge it
    overlap: int = 150,          # overlap so a fact straddling a boundary
) -> list[Chunk]:                # survives in at least one chunk whole
    """Heading-aware chunking: split on ## sections first (semantic units
    beat arbitrary character windows), then window any oversized section
    with overlap. Simple, inspectable, testable — v0 by design; fancier
    strategies must EARN their way in by beating this on the Triad evals
    (the earned-overlay principle from your roadmap, applied to chunking).
    """
    chunks: list[Chunk] = []
    current_heading: str | None = None

    for section in text.split("\n## "):
        lines = section.strip().splitlines()
        if not lines:
            continue
        current_heading = lines[0].strip("# ").strip()
        body = "\n".join(lines[1:]).strip()

        start = 0
        while start < len(body):
            piece = body[start : start + max_chars]
            chunks.append(Chunk(doc_id, len(chunks), piece, current_heading))
            if start + max_chars >= len(body):
                break
            start += max_chars - overlap        # step back by overlap

    log.info("doc_chunked", doc_id=doc_id, n_chunks=len(chunks))
    return chunks
```
Tests: chunk count on a known doc; overlap actually overlaps; a fact placed at a boundary appears intact in ≥1 chunk (write the doc to make it so — golden-dataset thinking, applied to chunking).
- [ ] 30 min — Corpus: 4 more docs
- [ ] 20 min — Journal + commit

### 📌 DAY 73 — Wednesday, September 30
**Morning:** Anthropic Academy — **Introduction to Model Context Protocol** (the roadmap's first-party primer route: free, official cert) — first half.
**Evening:**
- [ ] 70 min — **Embed + store** `src/policypulse/ingest/indexer.py`:

```python
"""Index the corpus into ChromaDB.

Install: uv add chromadb
ChromaDB = a vector database: stores each chunk's embedding and finds
nearest neighbors to a query vector. Local, file-persisted, zero infra —
right-sized for S1 (an ADR-worthy choice: consequences include single-node
limits, which is fine and stated honestly).
"""

import chromadb

from policypulse.ingest.chunker import Chunk

# PersistentClient writes to disk — the index survives restarts (an
# in-memory index rebuilt per run would hide real-world staleness issues).
client = chromadb.PersistentClient(path="data/chroma")


def index_chunks(chunks: list[Chunk]) -> None:
    collection = client.get_or_create_collection(
        name="policies",
        metadata={"hnsw:space": "cosine"},     # cosine similarity — Day 67's
    )                                          # by-hand math, now infrastructure
    collection.upsert(                          # upsert = insert-or-update:
        ids=[f"{c.doc_id}:{c.chunk_index}" for c in chunks],   # re-runs are
        documents=[c.text for c in chunks],                     # idempotent —
        metadatas=[                                             # a pipeline
            {"doc_id": c.doc_id, "heading": c.heading or ""}    # virtue you'll
            for c in chunks                                     # formalize in
        ],                                                      # Stage 2 Airflow
    )
    # Chroma embeds automatically with its default model. GOOD ENOUGH for v0;
    # embedding-model choice is a later, eval-refereed decision. Ship first.


def retrieve(query: str, k: int = 4) -> list[dict]:
    """Top-k chunks with provenance — the retrieval half of RAG."""
    collection = client.get_or_create_collection("policies")
    res = collection.query(query_texts=[query], n_results=k)
    return [
        {"text": doc, "doc_id": meta["doc_id"], "heading": meta["heading"],
         "distance": dist}
        for doc, meta, dist in zip(
            res["documents"][0], res["metadatas"][0], res["distances"][0]
        )
    ]
```
Index the corpus; run 5 hand-queries; eyeball whether the right chunks surface. Your domain brain is the v0 eval.
- [ ] 30 min — Journal + commit (`feat: chromadb indexing + retrieval v0`)

### 📌 DAY 74 — Thursday, October 1
**Morning:** IBM PC · **Evening:** 70 min — **Answer with citations**: `src/policypulse/answer.py` — retrieve top-k → build a prompt embedding the chunks with their doc_id/heading labels → system prompt commands: *answer ONLY from provided context; cite [doc_id › heading] for each claim; if the context doesn't contain the answer, say exactly that* (the say-I-don't-know clause is the anti-hallucination pressure valve — your Improving-Accuracy course, applied) → pydantic-validated `CitedAnswer {answer, citations: list[str], answerable: bool}` · 30 min MCP primer finish → **official Academy cert → Tier-5 log** · journal + commit

### 📌 DAY 75 — Friday, October 2
**Morning:** DL.AI Pro — remaining S2 short labs (*Knowledge Graphs for RAG* if deferred, *RAG Production-Ready*); download everything.
**Evening:** 60 min — corpus to 12+ docs; re-index; retrieval quality spot-check · 40 min — **golden questions v1**: 20+ Q&A cases against YOUR corpus (`evals/golden_policy.json`), including 4+ deliberately *unanswerable* questions (expected: `answerable: false` — refusing to invent is a first-class behavior to test) · journal + commit

### 📌 DAY 76 — Saturday, October 3 (5.5h)
**Morning (5:00–8:30):**
- [ ] 150 min — **The RAG Triad gate** ⭐ — the harness graduates. `src/policypulse/evals/triad.py`, adapting your Weeks 9–10 harness to the three questions that define RAG quality:

```python
"""RAG Triad evaluation — the Advanced RAG course's frame, on YOUR system.

For each golden question, three judgments:
1. CONTEXT RELEVANCE  (code-assisted): did retrieval surface the chunk(s)
   the golden case names? Measurable: expected_doc_id in retrieved set.
2. GROUNDEDNESS       (judge): is every claim in the answer supported by
   the retrieved context — no smuggled outside knowledge?
3. ANSWER RELEVANCE   (judge): does the answer actually address the
   question asked?
Grader assignment follows the Week 10 rule: code where truth is checkable
(#1), judge where it's a judgment (#2, #3) — with judge outputs pydantic-
validated, because judges are models too.

Gates (starting policy, ADR 0003, ratchet-up-only):
  context_relevance >= 0.80 · groundedness >= 0.85 · answer_relevance >= 0.85
  AND: 100% of unanswerable cases answered with answerable=false —
  a hard gate, not an average: inventing policy answers for participants
  is the one failure a compliance-adjacent assistant may never make.
"""
```
Implement it (you have every piece: retrieval call, judge pattern, thresholds, structlog reporting, exit-code gating). Wire as a `workflow_dispatch` CI job like Day 61. Run the full gate; log the first real numbers in `docs/eval-log.md`.
**Evening:** 60 min IBM PC · 45 min draft post #11 (artifact: the Triad numbers table — "my RAG system now has to pass an exam before it ships") · journal + commit

### 📌 DAY 77 — Sunday, October 4 (2h)
Week summary · publish post #11 · plan Week 12 · confirm Pro-month cancel date on calendar · journal 🎉

---

## 🗓 WEEK 12 (Oct 5–11) — QUARTER CLOSE

### Week 12 goals
```
□ PolicyPulse: one improve cycle vs the Triad (documented before/after)
□ Track A (internal): before-metrics captured + ADRs + C4 — BEFORE Day 82
□ Track B (public repo): started — uv migration + clone-slug fix (finishes in Q2)
□ Automation win #1 documented (**evidence file** keystone) — ⏰ draft Day 78–80
□ Pro month: notebooks all downloaded → CANCELLED
□ IBM PC Course 1 done or near · AB-620 ~50% · Post #12 · MONTH-3 RETRO
```

### 📌 DAY 78 — Monday, October 5
**Morning:** IBM PC. **Evening:** 70 min — Triad-driven improve cycle: worst metric → one change (chunk size? k? system prompt?) → re-run → eval-log before/after. One variable at a time — otherwise you learn nothing from the delta. · 30 min AB-620 · journal + commit

### 📌 DAY 79 — Tuesday, October 6
**Morning:** IBM PC. **Evening:** 🎪 meetup window (check calendar — monthly commitment). Else: 70 min **retro-migration pass, session 1** (work context): the 1099 pipeline gets `pyproject.toml` + `uv.lock` (pip→uv), verified running under `uv run`; notes for the build-in-public post (sanitized: mechanism only) · 30 min AB-620 · journal

### 📌 DAY 80 — Wednesday, October 7
**Morning:** CS50P Week 5 (unit tests — meta-moment: the course teaches what you've practiced for 10 weeks; collect the vocabulary).
**Evening:** 70 min — **retro-migration session 2**: structlog with the FULL Correction 16 pattern — `ProcessorFormatter` (foreign third-party logs render through your chain) + a **redaction processor** as the PII choke point:

```python
"""The redaction processor — Correction 16's highest-value line for an
ERISA-adjacent system: masking as a PROCESSOR runs on EVERY event dict,
including third-party libraries echoing payloads — not a helper you must
remember to call at each site. The choke-point pattern.
"""

import re

SSN_RE = re.compile(r"\b\d{3}-?\d{2}-?\d{4}\b")     # P4E C3's regex, deployed

REDACT_KEYS = {"ssn", "tin", "participant_name", "dob", "account_number"}


def redact_pii(logger, method_name, event_dict):
    """structlog processor signature: receives every event dict, returns it."""
    for key in list(event_dict):
        if key.lower() in REDACT_KEYS:
            event_dict[key] = "***REDACTED***"
        elif isinstance(event_dict[key], str):
            event_dict[key] = SSN_RE.sub("***SSN***", event_dict[key])
    return event_dict

# Wired into the processor chain BEFORE the renderer; ProcessorFormatter's
# foreign_pre_chain gets it too, so even httpx/SDK logs pass through.
# Write the test with structlog.testing.capture_logs: log a fake SSN,
# assert it NEVER appears in output. (Remember Correction 16's testing
# footnote: cache_logger_on_first_use must be False in tests.)
```
The full wiring (ProcessorFormatter config) comes from structlog's *Standard Library Logging* docs page — the roadmap's named source-of-truth; read it as you implement (this IS the Correction 16 learning line).
- [ ] 30 min — ADR (in the pipeline's new docs/adr/): `0001-processorformatter-over-alternatives` — the decision Correction 16 says to record, rejected alternatives included (loguru, python-json-logger — reasons are in your roadmap)
- [ ] Journal + commit

### 📌 DAY 81 — Thursday, October 8
**Morning:** IBM PC.
**Evening:** 70 min — **retro-migration session 3: first C4 Context** via the roadmap's toolchain — `architecture.dsl` (Structurizr DSL):

```
workspace "1099 Reconciliation Pipeline" {
    model {
        operator  = person "Plan Operations"          "Reviews exceptions"
        matrix    = softwareSystem "Matrix Export"    "Recordkeeper system" "external"
        relius    = softwareSystem "Relius Export"    "Plan admin system"   "external"
        pipeline  = softwareSystem "1099 Recon Pipeline" "Normalizes, reconciles, derives Box-7, reports corrections"

        matrix   -> pipeline "Distribution extracts (CSV)"
        relius   -> pipeline "Distribution extracts (CSV)"
        pipeline -> operator "Exceptions & corrections report"
    }
    views {
        systemContext pipeline "C4-L1" { include *; autolayout lr }
    }
}
```
Run **Structurizr Lite in Docker** (free, per Correction 14 — Docker's already a requirement: `docker run -it --rm -p 8080:8080 -v $(pwd):/usr/local/structurizr structurizr/lite`), view it at localhost:8080, then export to Mermaid via structurizr-cli for the README — **one model, two outputs, no drift** (the exact Correction 14 pattern). Self-score against c4model.com's diagram review checklist.
- [ ] 30 min — AB-620 · journal + commit

### 📌 DAY 82 — Friday, October 9
**Morning:** IBM PC Course 1 wrap (or near).
### 🔴 DAY 82 IS YOUR LAST DAY OF EMPLOYMENT (Correction 22)
Treat this day as a boundary, not a workday. Before you log off for the last time:
- [ ] **Final data check** — any figure you will ever cite about the internal 1099 pipeline or automation win #1 must be verified **today**. After today there is no system to check against, and a number you cannot source is a number you cannot say in an interview.
- [ ] **Data boundary check.** 🔄 Revised: the *code* travels with you (not company-private, per your confirmation). What must not: **real participant data in any form** — exports, CSV fixtures, notebook output, log samples, screenshots of internal screens. Sweep the repo you are taking: `gitleaks detect`, `nbstripout` across every notebook, and grep the fixtures for anything that looks like an SSN or a real name before it touches a public remote.
- [ ] **Written ownership confirmation on file** (see the note above) — the last day is the last day you can ask.
- [ ] **Contacts** — personal-email your working relationships (colleagues, not clients) before access closes. Referrals are a dominant 2026 hiring channel and these are your warmest ones.
- [ ] **Log the transition** in the evidence file: role, dates, and the two automation wins as STAR stories. This is résumé source-of-truth from tomorrow onward.

**Evening:** 70 min — **Automation win #1, FINALIZE** ⭐ (drafted Day 78–80): one page in the **evidence file** — situation → what you automated → mechanism (one paragraph, plain) → quantified outcome (relative/scale figures that pass the deposition test: "N hundred corrections caught pre-mailing," "X hours/cycle removed") → what it meant for the team. ~~Jen-readable: outcomes first, mechanism second~~ → **interviewer-readable**: problem shape and decomposition first, mechanism second, outcome third, zero jargon. ~~This page is the Month-6 conversation's opening exhibit.~~ → **This page is your FDE discovery-round opening story and a résumé bullet for Q1 2027.** · 30 min — **Pro-month closeout**: notebook inventory check → download stragglers → **CANCEL Pro** → log Accomplishments as Tier-5 evidence · journal + commit

### 📌 DAY 83 — Saturday, October 10 (5.5h)
**Morning:** 120 min — flagship polish pass: both repos green (CI, mypy, ruff), READMEs honest in P/C/A order (PolicyPulse ②Cost now has REAL numbers: cost-per-query from the Triad runs — the roadmap's noted "best Cost story" begins), demo GIFs if time (15–30s terminal recordings — the README standard's next item) · 60 min IBM PC · 30 min CS50P
**Evening:** 60 min — draft post #12: **the Quarter-1 story** (Day 1 setup → two eval-gated flagships + a cert + a live CI habit; artifact-dense, zero job-seeking language) · 45 min pre-write the Month-3 retro data (hours, completions, gaps) · journal + commit

### 📌 DAY 84 — Sunday, October 11 (2h) — 🏁 **MONTH-3 RETRO**
- [ ] 60 min — The retro, written in `weekly-summaries/QUARTER_1_RETRO.md`:
```
1. NUMBERS: hours/week actual vs 25 · courses done vs plan · commits ·
   posts published vs 12 · meetups attended vs 3
2. EVIDENCE INVENTORY: elevation file contents · both flagships' state vs
   the Quarter Map's Week-12 targets · Tier-5 log
3. GATE CHECK: which fortnights hit 80%? Where did the plan overreach or
   underreach? (Honest — the Q2 plans calibrate on THIS.)
4. AGENT-POLICY REVIEW: acceleration vs comprehension debt — any line you
   accepted that you still can't explain? (If yes: schedule the study.)
5. SUSTAINABILITY: 4:30 AM energy trend · family friction · what changes
6. Q2 SHAPE: IBM spine cadence · AB-620 — GO or HOLD? (now conditional,
   self-funded ~$165 — C37) · PolicyPulse S1 hardening · public
   1099_reconciliation_pipeline remediation · Google Git/GitHub course
   (row 3.5, ~8 hrs — unscheduled, needs a slot) · DataVault S2 path
   (the Stage 1 EVIDENCE GATE) · Q1 2027 application runway
7. EXTRA-TIME THREADS: AB-620 + Google Git — did they hold at ~2 hrs/wk
   each, or did they leak into the 25? (If actual > ~29 hrs/wk: PAUSE both.
   Flagships never pause first.)
8. 🔴 POST-EMPLOYMENT SHAPE: hours available now that the job has ended
   — does the 25 hrs/week model change? Income runway? This is the
   biggest single input to the Q2 plan and it did not exist when this
   document was written.
```
- [ ] 30 min — Publish post #12 · 30 min — Share the retro with Claude for the Q2 plan generation (propose→approve, as always) · journal + 🎉 **Quarter 1 complete.**

---

## 📊 2-WEEK SUCCESS METRICS
```
□ PolicyPulse S1 v0: corpus→chunk→embed→     □ Retro-migration: uv done · structlog
  retrieve→cited answers, CI green             PF + redaction done · C4-L1 exists
□ RAG Triad gate live + first improve cycle  □ Automation win #1 documented
□ Unanswerable-question hard gate at 100%    □ Pro month emptied + CANCELLED
□ MCP primer (Academy) cert — Tier-5 log     □ AB-620 ~50% · CS50P Wk 5
□ IBM PC enrolled, Course 1 ~done            □ Posts #11–12 · meetup ✓
□ Golden policy set: 20+ cases w/ rationale  □ MONTH-3 RETRO written & shared
```
**Passing bar: 80%.** Non-negotiables: PolicyPulse's Triad gate, the automation-win doc, and the retro itself.

---

## 🔭 WHAT COMES NEXT (Quarter 2 preview — plans generated AFTER your retro)
Months 4–6, per the roadmap: the IBM spine intensifies (its RAG/LangChain/watsonx middle) · PolicyPulse S1 hardening toward "shipped with eval gates" (the Stage 1 deliverable) · Streamlit enters (30 Days of AI — Correction 20's row 11.5) as the flagships' demo surface · CS50x/CS50P completion track.

**🔄 Re-anchored by Corrections 22 / 32 / 33 / 37 — four items changed:**
- ~~AB-620 exam~~ → ✅ **GO** (your ruling), **self-funded ~$165**, run as an **extra-time thread outside the 25 hrs/week**. ⭐ **Book the exam AFTER 9 Oct**, not before — post-employment is when the capacity actually exists.
- ~~retro-migration pass completed (internal)~~ → ✅ **FULL retro-migration approved** (your ruling), split into **Track A (internal, hard stop Day 82)** and **Track B (public `1099_reconciliation_pipeline`, runs to completion in Q2)**. Track B is the complete production-grade project — all 11 items in the table above, finished, not started. **This is a named Q2 deliverable now, not a backlog item.**
- ~~automation win #2~~ → there is no Month 4–6 employment in which to earn one. **Both wins must be captured before Day 82.**
- ~~the Month-6 scope-change conversation with Jen — the deliverable every artifact this quarter was quietly building toward~~ → ❌ **retired**. The deliverable everything now builds toward is the **Q1 2027 external application package**: Analytics Engineer first door, Data Engineer parallel, exiting Stage 1 on the **evidence gate** (DataVault S2 hardening), not on an employment event.

**🆕 New in Q2, from corrections that post-date this plan:**
- **PostCheck** (Correction 33) enters the portfolio as **Flagship #4** — the post-posting distribution QA agent, and the only project producing first-class evidence for **both** doors at once (agentic adjudication + eval gates for Applied AI; exactly-once ingestion, deterministic parsing, append-only event log, dbt models + contracts for AE/DE). Given the ERISA domain is your structural differentiator and you are about to lose daily access to the domain, **capture the SOP and workflow knowledge PostCheck depends on before Day 82.**
- ✅ **Google — Introduction to Git and GitHub** (Stage 1 row 3️⃣.5, ~8 hrs committed) — **approved for Stage 1 as an extra-time thread**, opened Week 9, continuing here. Finish it in Q2. ⚠️ The shareable certificate is **Tier 4/5 — never a Certifications line**.
- 💡 **Worth considering in Q2: the IBM Git secondary** (~10.5 hrs, conditional). Correction 30 records the reason, and it is the strongest one available: **its final project is peer-reviewed** — you submit work and review other learners' submissions. That makes it the *only* mechanism in the entire Stage 1 course list that puts another human's code in front of you, and a solo portfolio has no other source of team-workflow evidence. ⚠️ Anti-stack condition: it is a component of *IBM Applied Software Engineering Fundamentals* (the row-14 secondary) — taking both double-buys the hours, so it is one or the other.
- **The reading layer** (Correction 34) is live: finish *Robust Python* and *AI Engineering* in Q2; *Python Testing with pytest 2e* is the secondary. Buy at stage entry, re-verify editions.

---
*Aligned to Career Roadmap v10.0 (Corrections 1–20). No roadmap edits made; propose→approve governance applies. Q2 plans will be generated from your actual Month-3 retro, not assumptions.*