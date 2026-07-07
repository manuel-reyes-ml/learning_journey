# Learning Log

A lightweight, append-only record of things I learn from short videos, podcasts, and
articles while working — captured in my own words so my future self can retrieve and
reuse them. Inspired by the "Today I Learned" (TIL) pattern
([jbranchaud/til](https://github.com/jbranchaud/til),
[simonw/til](https://github.com/simonw/til)).

**How I use this**
- One entry per source, newest at the top.
- The **Takeaway** is the point: 2–3 lines *in my own words*, never copy-paste. If I
  can't restate it, I didn't learn it yet.
- Tags come from the **fixed taxonomy** below — don't invent new ones ad hoc; add to
  the taxonomy deliberately so search stays clean.
- Keep it public-safe: no Daybright/proprietary or finance-client detail in this repo
  (it's public). Concepts only.

---

## Tag taxonomy

Use lowercase, hyphenated tags. Every entry gets **one stage tag**, **zero or one
project tag**, and **1–3 topic tags**.

### Stage (pick one)
- `s1-genai` — GenAI-First Data Analyst & AI Engineer
- `s2-data-eng` — Data Engineer
- `s3-ml-eng` — ML Engineer
- `s4-agentic` — Agentic AI Engineer
- `s5-llm-eng` — Senior LLM Engineer
- `s0-foundation` — cross-cutting fundamentals (math, CS, Python, git)

### Project (zero or one)
`policypulse` · `formsense` · `afc` · `crucible` · `streamsmart` · `datavault` ·
`odi` · `1099-recon` · `cadence`

### Topic (1–3, grouped by stage for reference)
- **S1:** `rag` · `graphrag` · `vector-db` · `embeddings` · `prompting` · `mcp` ·
  `llm-api` · `evals` · `chunking`
- **S2:** `sql` · `postgres` · `pyspark` · `airflow` · `aws` · `bigquery` · `docker` ·
  `k8s` · `typescript`
- **S3:** `math-ml` · `xgboost` · `deep-learning` · `mlflow` · `fine-tuning` · `lora` ·
  `vllm` · `mlops`
- **S4:** `langgraph` · `multi-agent` · `a2a` · `agent-eval` · `guardrails` ·
  `human-in-the-loop`
- **S5:** `serving` · `llmops` · `latency` · `cost` · `distributed` · `observability`
- **Cross-cutting:** `python` · `git` · `testing` · `architecture` · `security` ·
  `career`

### Format
`video` · `podcast` · `article` · `docs`

---

## Entry template (copy this)

```md
### YYYY-MM-DD — <Title>
- **Source:** <Channel/Podcast> · [link](<url>)
- **Format:** <video|podcast|article|docs> · **Time:** <mm:ss or est. min>
- **Stage:** <s1-genai> · **Project:** <policypulse|—> · **Topics:** <rag>, <evals>
- **Takeaway:** <2–3 lines, my own words — what I now understand that I didn't before.>
- **Apply:** <Optional: the specific roadmap task or project file this informs, or a
  next action. Leave blank if none.>
```

---

## Entries

2026-07-07 - RAG vs Fine-Tuning vs Prompt Engineering: Optimizing AI Models
Takeaway: Use RAG to add new documents or sources to LLM scope, so it can provide more
accurate responses. Use Fine-tuning to change model's parameters or add/update new information
into the model, however requires higher resources and it is risky. 
Use prompt engineering, so the model know your style and type of information you are looking for, 
however it would not change the fact that the model has outdated information. 

2926-07-07 - MCP vs API: Simplifying AI Agent Integration with External Data
Takeaway: MCP = Model Context Protocol -> standardize how external app/system adds context to Model (LLM)
MCP server has a Dynamic Self-discovery to client (shows its capability and data to a client - LLM)
API calls are manual and needs a developer to update calls and get newer capabilities.
A lot of MCP servers are wrapper of Rest API, using API inside them to do the work.

### 2026-07-07 — 7 AI Terms You Need to Know: Agents, RAG, ASI & More
- **Source:** IBM Technology (YouTube, Martin Keen) · [link](https://www.youtube.com/watch?v=VSFuqMh4hus)
- **Format:** video · **Time:** ~11 min
- **Stage:** s1-genai · **Project:** — · **Topics:** rag, mcp, reasoning-models
- **Takeaway:** Fast glossary pass; two anchors stuck. (1) **Agentic AI / agents** build on top of
  large *reasoning* models — the "thinking…" I see is the model generating an internal chain of
  thought before it answers, which is the raw material an agent reasons with before acting. (2) **MCP**
  standardizes how external apps/systems add context to a model (same point as the MCP-vs-API video).
  Also covered: RAG, vector DBs, ASI, MoE, explainable AI.
- **Apply:** Vocabulary reinforcement, no single project. The reasoning-model → agent link is a clean
  build-in-public framing line. Cross-references the workflow-vs-agent distinction already logged for
  FormSense/AFC.

### 2026-07-07 — RAG vs Agentic AI: How LLMs Connect Data for Smarter AI
- **Source:** IBM Technology (YouTube) · [link](https://www.youtube.com/watch?v=fB2JQXEH_94)
- **Format:** video · **Time:** ~10 min (est.)
- **Stage:** s4-agentic · **Project:** afc · **Topics:** rag, graphrag, agent-eval
- **Takeaway:** RAG and agentic AI are complementary, not rivals. An agent (or workflow) needs RAG as
  its grounding layer — a store the LLM reads from — to avoid hallucinating and to produce the accurate
  result the user actually wants. RAG = Retrieval Augmented Generation: it holds the info the model
  retrieves at answer time. The agent supplies autonomy/decisions; RAG supplies the facts.
- **Apply:** AFC's exact shape — an agentic research loop grounded on a GraphRAG store (Neo4j +
  ChromaDB). Reinforces why AFC's ≥0.9 faithfulness gate matters: "avoid hallucination" is precisely
  what that threshold enforces on the RAG grounding.

### 2026-07-06 — LLMs and AI Agents: Transforming Unstructured Data
- **Source:** IBM Technology (YouTube, w/ Terzo) · [link](https://www.youtube.com/watch?v=_pEEJu-2KKM)
- **Format:** video · **Time:** ~15 min (est.)
- **Stage:** s4-agentic · **Project:** formsense · **Topics:** multi-agent, architecture, chunking
- **Takeaway:** Agentic workflows can be **linear** — one agent's output feeds the next
  (e.g., a doc-analysis agent hands off to an extraction agent). The whole pipeline is
  **event-triggered**: it fires when something happens — like a file landing in a watched
  location that sits inside the agents' configured scope. So the "trigger + scoped hand-off
  chain" is the design, not a single do-everything agent.
- **Apply:** This is basically FormSense's shape — a file-drop event kicking off a sequential
  extract pipeline. Note it's the *workflow* end of the workflow-vs-agent spectrum (predefined
  hand-offs = predictable + cheap), which is the right call for scoped document extraction.
  **Workflow, not an agent**. The test isn't "does it have loops, tools, and self-correction" — it's who
  owns the control flow.  **Workflows** orchestrate LLM and tool calls through predefined code—you own
  the control flow. **Agents** let the model choose its next tool call from environment feedback—you
  own the goal and guardrails, not every branch.
  **In your design you own the path:** if confidence < 0.8 → review, if incomplete → email, if complete → 
  ticket are branches you wrote in code. The LLM reasons inside each step (reading the form, judging
  validation) but never decides what to do next. That is the literal workflow definition. An agent
  would be the model deciding, turn by turn, "I'll look up this participant's history, then maybe
  re-read the form, then perhaps email the rep" — dynamic routing from environment feedback.

### 2026-07-06 — 10 Use Cases for AI Agents: IoT, RAG, & Disaster Response Explained
- **Source:** IBM Technology (YouTube, Martin Keen) · [link](https://www.youtube.com/watch?v=Ts42JTye-AI)
- **Format:** video · **Time:** ~12 min (est.)
- **Stage:** s4-agentic · **Project:** afc · **Topics:** rag, vector-db, architecture
- **Takeaway:** The agent loop that drives toward a user goal:
  **Goal → Planner** (can call tools, e.g. web search) **→ Memory** (a vector DB / RAG store it
  both **reads from and writes to**) **→ Executor → Action**. Key detail: memory is
  *bidirectional* — the agent persists new state back, it doesn't just retrieve.
- **Apply:** This is AFC's research loop exactly; the read/write memory maps to AFC's GraphRAG
  store (Neo4j + ChromaDB). Worth mirroring the Planner→Executor split in AFC's orchestration
  design so planning and acting stay separable (easier to gate/eval).

### 2026-07-06 — Generative vs Agentic AI: Shaping the Future of AI Collaboration
- **Source:** IBM Technology (YouTube) · [link](https://www.youtube.com/watch?v=EDb37y_MhRw)
- **Format:** video · **Time:** ~9 min (est.)
- **Stage:** s4-agentic · **Project:** — · **Topics:** prompting, architecture
- **Takeaway:** Generative vs. agentic AI run on the **same underlying LLM** — the difference is
  behavior: **generative is reactive** (answers a prompt), **agentic is proactive** (pursues a
  goal). Agentic adds a **chain-of-thought** loop the model uses to work a problem step by step,
  deciding which tool to call next and judging whether a result is good enough — i.e., it drives
  its own loop instead of stopping at one response.
- **Apply:** This is the conceptual root of the workflow-vs-agent decision across my portfolio:
  the reactive/generative path = assistant/workflow work (PolicyPulse Q&A), the proactive/agentic
  path = AFC and Crucible. Good framing line for a build-in-public post.

### 2026-07-06 — AI Agents and AI Assistants: A Contrast in Function
- **Source:** IBM Technology (YouTube) · [link](https://www.youtube.com/watch?v=IivxYYkJ2DI&list=PLOspHqNVtKAB6AzNie7BrFhbg4dv4Gfz8&index=2)
- **Format:** video · **Time:** ~5 min
- **Stage:** s4-agentic · **Project:** crucible · **Topics:** human-in-the-loop, guardrails, architecture
- **Takeaway:** Same split as a celebrity's staff: an
  *assistant* does tasks on request (reactive, no external tools -> reliable), an *agent*
  pursues a goal proactively and doesn't need a prompt to keep working (plans, calls tools,
  adapts). The autonomy is the whole tradeoff: it buys capability but adds failure modes
  assistants don't have — infinite planning/reflection loops, brittleness when external
  tools change underneath it, and higher cost/latency. IBM's honest caveat: today's
  foundation models aren't fully reliable as agents yet, so autonomy should be *scoped*,
  not assumed.
- **Apply:** Reinforces the programmatic-vs-agentic call from the entry below — default to
  the reliable assistant/workflow path unless the task truly needs open-ended autonomy. The
  infinite-loop + tool-drift risks are the direct rationale for Crucible's kill-switch and
  mandatory human sign-off; AFC (read-only) can tolerate more autonomy.

### 2026-07-06 — What are AI Agents?
- **Source:** IBM Technology (YouTube) · [link](https://www.youtube.com/watch?v=F8NKVhkZZWI)
- **Format:** video · **Time:** ~12 min
- **Stage:** s4-agentic · **Project:** afc · **Topics:** multi-agent, agent-eval, guardrails
- **Takeaway:** An "agent" = an LLM running the **ReAct** loop (Reason + Act; Yao et al., 2022) —
  it interleaves reasoning steps with tool calls, choosing the next action toward a goal instead of
  answering in one shot. Failure mode is unbounded looping / bad tool choice, which is why eval +
  guardrails aren't optional add-ons but part of the architecture — directly why AFC needs a
  faithfulness gate and Crucible needs a human sign-off. The bigger design lever is **workflow vs.
  agent** (Anthropic, *Building Effective Agents*, 2024): a **workflow** orchestrates the LLM through
  *predefined code paths* — predictable, cheaper, best when I can script the steps (my "programmatic /
  think fast" case: specific data for specific queries); an **agent** lets the LLM *dynamically direct
  its own process and tools* — for open-ended tasks whose path I can't predict. The dividing line is
  *degree of autonomy*; the rule is start simple and add agency only when the flexibility is worth the
  latency, cost, and compounding errors.
- **Apply:** Cross-reference with AFC's ≥0.9 faithfulness threshold; note for the
  Crucible human-in-the-loop write-up.

<!--
Newest entries go ABOVE this line.
-->