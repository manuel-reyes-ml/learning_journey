# 🚀 WEEKS 11–12 MASTER ACTIVATION PLAN (v10.0)
## PolicyPulse Opens + The IBM Spine + Month-3 Retro | September 28 – October 11, 2026

**Document Version:** 1.0
**Covers:** Monday, September 28 – Sunday, October 11, 2026 (Stage 1 · Month 3 · Weeks 11–12)
**Aligned To:** Career Roadmap v10.0, Corrections 1–20
**Prerequisite:** Weeks 9–10 metrics ≥80% (non-negotiables: harness v1 + documented improve cycle)
**Weekly Hours:** 25 · ⏰ **Pro month expires ~Oct 13 — empty it and cancel it this fortnight (hard deadline).**

> 🤖 **Agent Policy:** Phase 3. PolicyPulse follows the DataVault pattern: requirements-first comment blocks, agents for scaffolding under diff review, retrieval logic + all eval gates + ADRs by hand. End-of-quarter checkpoint: Sunday Day 84's retro includes an honest agent-policy review — where did agents genuinely accelerate you, and where did you accept a line you couldn't fully explain? That answer calibrates Q2's policy.

---

## 📊 WHERE YOU STAND
You own an eval harness with dual graders, a CI-gated DE flagship running end-to-end, an AI-901 pass, SDK fluency, and ~11 weeks of daily commits. This fortnight completes the Quarter-1 promise: **both lead flagships alive, eval-gated, and public.**

## 🧠 STRATEGIC CONTEXT

### PolicyPulse S1: what ships and what deliberately doesn't
S1 core = **retrieval that can prove itself**: synthetic policy corpus → chunk → embed → store (ChromaDB) → retrieve → answer with citations — with the RAG Triad eval gate wired from commit one (your Weeks 9–10 harness, graduated). Deliberately NOT in S1: GraphRAG/Neo4j (S3), FastMCP server (S3 — but the MCP *primer* is this fortnight, so the design leaves the seam), per-document access control (S2–S3 layer; note the seam in an ADR).

**Data rule:** the corpus is synthetic policy/handbook text YOU write (or generate with Claude and then *edit* — you must know every claim in your corpus, because your golden questions test against it). Never real plan documents, never employer text.

### The IBM spine begins
The **IBM Generative AI Engineering Professional Certificate** (16 courses, Coursera Plus, ACE-recommended) is your roadmap's Months 3–6 structured spine. It starts Week 11 at a sustainable ~3 hrs/week morning-thread pace — a marathon lane next to the build lanes, not a sprint. Early courses will overlap what you've built; per the standing rule, move FAST through overlap (the marginal value early is structure + the credential; depth compounds mid-program).

### The retro-migration pass (Corrections 13/14/16's "named pass") starts
The 1099 pipeline at work gets its production retro-migration: pip→uv (+ lockfile), structlog with ProcessorFormatter + a PII-redaction processor, first C4 Context diagram (Structurizr DSL → Mermaid), and its first ADRs. **This is internal work on internal systems** — done at work or on the work machine as appropriate, with only sanitized lessons-learned becoming public content (a strong build-in-public post, per the roadmap's exact intent). Scheduled here as *started, not finished* — it continues into Q2.

### And the elevation file gets its keystone
**Internal automation win #1, documented** — the story you identified on Day 70, written with a quantified outcome and Jen-readable framing (the 450+-corrections pattern is the template). Deposition test applies: mechanism and relative outcomes, no client identifiers, no absolute dollar figures.

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
□ 1099 retro-migration pass STARTED: uv migration + structlog PF + first C4
□ Automation win #1 documented (elevation file keystone)
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
**Evening:** 70 min — **Automation win #1, documented** ⭐: one page in the elevation file — situation → what you automated → mechanism (one paragraph, plain) → quantified outcome (relative/scale figures that pass the deposition test: "N hundred corrections caught pre-mailing," "X hours/cycle removed") → what it means for the team. Jen-readable: outcomes first, mechanism second, zero jargon. This page is the Month-6 conversation's opening exhibit. · 30 min — **Pro-month closeout**: notebook inventory check → download stragglers → **CANCEL Pro** → log Accomplishments as Tier-5 evidence · journal + commit

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
6. Q2 SHAPE: IBM spine cadence · AB-620 exam target · retro-migration
   completion · PolicyPulse S1 hardening · Month-6 scope-change prep
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
Months 4–6, per the roadmap: the IBM spine intensifies (its RAG/LangChain/watsonx middle) · AB-620 exam · PolicyPulse S1 hardening toward "shipped with eval gates" (the Stage 1 deliverable) · retro-migration pass completed (Docker + the pipeline's full standard) · Streamlit enters (30 Days of AI — Correction 20's row 11.5) as the flagships' demo surface · automation win #2 · CS50x/CS50P completion track · and the **Month-6 scope-change conversation with Jen, in writing** — the deliverable every artifact this quarter was quietly building toward.

---
*Aligned to Career Roadmap v10.0 (Corrections 1–20). No roadmap edits made; propose→approve governance applies. Q2 plans will be generated from your actual Month-3 retro, not assumptions.*
