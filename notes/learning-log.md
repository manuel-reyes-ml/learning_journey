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
- **Takeaway:** An "agent" = REACT LLM (Reason) + tools (Act) + a loop that decides which tool to call next
  toward a goal. The failure mode is unbounded looping / bad tool choice, which is why
  eval + guardrails aren't optional add-ons but part of the architecture — directly
  relevant to why AFC needs a faithfulness gate and Crucible needs a human sign-off. Also, to
  to identify programmatic vs Agentic approach to design and create LLM control logic (systems).
  Programmatic to think Fast, the LLm is given only specific data to resolve specific queries, and Agentic
  for the complex tasks that can random (not for a specific topic).
- **Apply:** Cross-reference with AFC's ≥0.9 faithfulness threshold; note for the
  Crucible human-in-the-loop write-up.

<!--
Newest entries go ABOVE this line. Keep the two examples above as format references,
or delete them once you've added a few real ones.
-->