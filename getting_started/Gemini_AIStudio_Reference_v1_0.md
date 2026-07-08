# Google AI Studio & Gemini API — Setup, Keys & Configuration Reference

**Focus:** Creating and using **two Gemini API keys** — a **FREE key** (Flash models, prototyping/public scaffolding) and a **PAID key** (higher limits, Pro models, data-not-trained) — via **Google AI Studio**, wired into a provider-agnostic, privacy-first Python stack (`google-genai`, Pydantic, OpenCode/OpenRouter routing).
**Compiled:** July 2026 · Aligned to a Cursor-primary, `google-genai`-SDK, "Anthropic-primary / Gemini-fallback", privacy-routed, "no vibe coding" workflow.
**Version:** 1.0 (July 8, 2026)

> 📝 **Changelog v1.0:** Initial reference. Covers the AI Studio ⇄ Gemini API ⇄ project/billing mental model, the **free-vs-paid data-training boundary** (§2 — the one that matters for your governance rule), two-project key setup (§3–§4), current free/paid model split + rate limits + pricing (§5–§7), the `google-genai` SDK (§8), stack integration incl. dual-key routing + PolicyPulse/FormSense/StreamSmart (§9), security for build-in-public (§11), and tailored tips (§13).

> 📝 **Why this exists:** Companion to the Ollama / LM Studio / OpenCode references. Those three are your **local-first, private, $0** lane. This one documents the **cloud fallback lane** — where Gemini sits in your model-routing chain (Anthropic primary → **Gemini fallback** → OpenAI alt), plus the two Gemini-native capabilities you actually reach for it: **multimodal Vision** (FormSense) and **native embeddings** (PolicyPulse). It is deliberately scoped so the **free key never touches proprietary data** (§2).

> ⚠️ **Google changes Gemini pricing, model IDs, rate limits, and billing rules frequently** (the Prepay billing system landed Mar 23, 2026; Pro models moved paid-only in Apr 2026). Treat **`ai.google.dev/gemini-api/docs`** and the **pricing page** (`ai.google.dev/gemini-api/docs/pricing`) as the source of truth, and read the **live quota panel in AI Studio for *your* project** before relying on any number below. Model tags and dollar figures here are representative snapshots (early–mid 2026).

---

> 🔴 **READ FIRST — the free/paid line is a DATA-GOVERNANCE line, not just a rate-limit line.**
> On the **free tier, Google may use your prompts and responses to improve/train its models.** On the **paid tier, your inputs/outputs are *not* used for training.** This maps directly onto your hard rule: **finance / proprietary / participant / ERISA data stays LOCAL (Ollama) — it never goes to *any* Gemini tier.** The free key is for **public build scaffolding and synthetic data only.** Details and the routing table in **§2**.

---

## 1. Mental model (AI Studio vs the API vs keys vs projects)

Four different things get called "Google AI Studio pricing," and conflating them is the #1 source of confusion:

- **Google AI Studio** (`aistudio.google.com`) — the free **browser playground**. Prompt-tuning, function-calling tests, "Get code" export. It has **no paid tier and no subscription**; it never bills you. This is a sandbox, not a runtime.
- **Gemini Developer API** — the **billable runtime** your code calls. It has a **free tier** and a **paid tier**. This is what your API key talks to.
- **Vertex AI** — Google Cloud's enterprise ML platform (separate URL, separate auth, GCP project + billing required). **You don't need this**; the Developer API is the right lane for your portfolio. Mentioned only so you don't wander into it by accident.
- **The API key** — just a **credential attached to a Google Cloud *project*.**

The critical mechanical fact, and the reason your "two APIs" request needs a small reframe:

> 🔑 **Tier lives on the *project* (via its billing account), not on the key.** A key is only a credential. **Adding extra keys to the *same* project does *not* add quota or change tier** — the free-tier limit is per-project, shared across all its keys. To get a genuinely separate **free** lane and **paid** lane, you create **two projects**: one with **no billing** (stays free tier) and one with **billing enabled** (paid tier). Then you generate **one key in each**. That's the setup this doc builds.

```
Google account
├── Project A  (no billing)      → FREE tier   → KEY_FREE   → Flash / Flash-Lite, prototyping, synthetic data
└── Project B  (billing enabled) → PAID tier   → KEY_PAID   → higher limits, Pro models, data NOT trained
```

Everything else — which model you get, whether you're trained on, your rate limits — is decided by **which project's key** you send the request with, plus **which model name** you put in the call.

---

## 2. The split that matters most: DATA governance (free vs paid)

This is the section that actually governs how you use Gemini, given your privacy-first architecture.

| | **FREE key (Project A)** | **PAID key (Project B)** |
|---|---|---|
| **Data used to train Google's models?** | **Yes — may be** (prompts + responses) | **No** — not used for product/model improvement |
| **Credit card** | Not required | Required (link billing, prepay ≥ $10) |
| **Models** | **Flash + Flash-Lite only** (Pro rejected) | Flash, Flash-Lite, **and Pro** |
| **Rate limits** | Low (see §6) | 100×–200× higher, tier-scaled |
| **Right use** | Prototyping, learning, demos, **synthetic/public data** | Public build at scale, Pro-model work, reliable throughput |

**How this plugs into your routing rule (the important part):**

- 🟢 **Local Ollama / LM Studio** — the *only* lane for **real Daybright / participant / ERISA / proprietary** data. Unchanged. Gemini (either tier) is **never** in this lane.
- 🟡 **Gemini FREE key** — **public build scaffolding + synthetic data only.** Your repos already enforce this (the 1099 pipeline README: *all data in this repo is synthetic; real participant data cannot be shared for compliance reasons*). The free key is safe there **precisely because** nothing sensitive touches it. Treat "free tier = trained on" as the reason, not just a footnote.
- 🟠 **Gemini PAID key** — reach for it when you want (a) **Pro-model** capability, (b) **higher/reliable limits** for a demo or eval batch, or (c) **data-not-trained** assurance for *public-but-not-for-training* content. It is **not** a license to send proprietary data — that still stays local. Paid just removes the training exposure for the public work you *do* route to Gemini.

> 💡 **One-line policy to put in your `.cursor/rules`:** *"Gemini FREE key → synthetic/public only (trained on). Gemini PAID key → public build at scale / Pro / no-train. Real finance/participant data → local Ollama, never Gemini."*

---

## 3. Create the FREE key (Project A — no billing)

**~2 minutes, no credit card.**

1. Go to **`aistudio.google.com`** → sign in with your Google account.
2. Sidebar → **API keys** (or the **"Get API key"** button).
3. Click **Create API key**. Let it **create a new Google Cloud project** for you (or pick one) — name it something like `gemini-free-prototyping` so it's unmistakable later.
4. **Copy the key** and store it (see §10/§11 — env var, never in code). You won't be shown it again in full.
5. Confirm the plan: on the **API keys / Projects** page, this project should show **"Free"** under the Billing Tier / Plan column.

That's the free lane. It talks to Flash/Flash-Lite, is rate-limited (§6), and **its traffic may be used for training** — so keep it to synthetic and public content.

> ⚠️ **EEA/UK/Switzerland caveat (not you, but for awareness):** users in those regions must enable billing even for free-eligible models. In the US (Greenville, SC) the no-card free key works as described.

---

## 4. Create the PAID key (Project B — billing enabled)

You want the paid lane in a **separate project** so it can't be confused with the free one and so its quota/tier is cleanly its own.

1. On the **API keys / Projects** page in AI Studio, click **Create API key** again and create/select a **second project** — name it e.g. `gemini-paid-prod`.
2. Find that project's row → under **Billing Tier**, click **Set up billing**.
3. First-time billing: confirm **country**, accept Terms, add **contact + payment method**.
4. **Prepay:** add a minimum of **$10** in credits (the new **Prepay** plan; the UI shows your region's minimum and max). New AI Studio users since **Mar 23, 2026** are generally on Prepay.
5. Copy the second key → store as a **separate env var** (`GEMINI_API_KEY_PAID`).
6. Confirm the project now shows **"Paid"** under Billing Tier.

**Two billing landmines to know before you rely on this in a demo:**

> ⚠️ **Prepay depletion stops service across *every* project on that billing account.** If a live demo (or later, an AFC/Crucible research run) depends on the paid key, treat the **prepay balance as uptime infrastructure** — set a **budget alert** and know it'll hard-stop at zero.

> ⚠️ **Mandatory monthly spend cap (since Apr 2026):** Tier 1 billing accounts have a **$250/month cap that cannot be disabled** — calls pause until the next cycle once hit. For your PAYG-discipline this is actually a *feature* (a hard ceiling against runaway bills), but plan capacity around it.

> 💡 **Alternative one-click paid path — Vertex AI Express Mode:** creates a paid-tier key without the full Cloud-project dance (rate limits 100×–200× over free, data not trained, Pro access). Handy if the project/billing UI fights you. It's a different surface, though — for consistency with `google-genai` + AI Studio, prefer the two-project setup above unless you hit friction.

---

## 5. Which models are free vs paid (current IDs)

Model availability shifted in 2026: **Pro moved to paid-only (Apr 2026)**; the free tier is **Flash + Flash-Lite**. Pick the model **by name in the call** — the *same* key can call any model its tier allows; a **free key calling a Pro model just gets rejected** until billing is enabled.

| Model ID (representative) | Tier | Good for (your stack) |
|---|---|---|
| `gemini-3.5-flash` ⭐ | Free + Paid | Default workhorse — RAG synthesis fallback, StreamSmart primary, general build |
| `gemini-3.1-flash-lite` | Free + Paid | Cheapest/fastest — **StreamSmart safety-judge**, bulk classification, high-RPM light tasks |
| `gemini-3-flash-preview` | Free + Paid | Newer Flash preview; A/B against 3.5-flash |
| `gemini-3.1-pro-preview` | **Paid only** | Hard reasoning, long-context analysis — **AFC** research, complex FormSense docs |
| `gemini-2.5-flash` / `gemini-2.5-pro` | Free (Flash) / Paid (Pro) | Prior gen; still available, useful as eval baselines |
| `gemini-embedding-001` ⭐ | Free + Paid | **PolicyPulse embeddings** (RETRIEVAL_DOCUMENT), semantic search |
| `gemini-embedding-2` *(emerging)* | Free + Paid | Newer embedding model appearing in docs — verify/benchmark before adopting |
| `gemini-2.5-flash-image` / Imagen | Paid (mostly) | Image gen — not on your roadmap; skip |

> 🔎 **Embeddings note for PolicyPulse:** your Stage-1 scope references `text-embedding-004`. That still works but is **legacy**; the current GA recommendation is **`gemini-embedding-001`** (with `gemini-embedding-2` emerging). Not a change to make now — flagging it as a one-line scope update to consider when you build PolicyPulse, so you embed on the current model from day one. (See §9 for the call.)

---

## 6. Rate limits & quotas (free vs paid)

> ⚠️ **These are starting points, not contracts.** The **live cap in AI Studio for your project** is authoritative; it varies by model, region, account age, and billing state. `429` = one limit exceeded → **exponential backoff** (most SDKs retry; you should still handle it).

| Model (free tier, representative) | RPM | TPM | RPD |
|---|---|---|---|
| `gemini-3.5-flash` / `gemini-3-flash` | ~10 | ~250K | ~1,500 |
| `gemini-3.1-flash-lite` | ~15 | higher | ~1,500 |
| Pro models | — | — | **paid only** |

- **Per-project, not per-key** — spinning up more keys in Project A won't raise the ceiling. To go higher, use the **paid** project.
- **Paid tier** scales **100×–200×** over free, and climbs through **Tier 1 → 2 → 3** based on cumulative Cloud spend + account age (tier is set at the **billing-account** level; all its projects inherit it).
- **`429` is not always quota** — it can be RPM, TPM, RPD, burst, region, or a paid-only model on a free key. Check the AI Studio quota panel before "fixing" it in code.

---

## 7. Pricing (paid tier — representative)

Per **1M tokens**, snapshot early–mid 2026. **Verify on the pricing page before anything cost-sensitive** — Flash sub-versions differ and figures move.

| Model | Input ($/1M) | Output ($/1M) |
|---|---|---|
| Flash-Lite | ~$0.10 | ~$0.40 |
| Flash (2.5 / 3.x) | ~$0.15–$0.30 | ~$0.60–$2.50 |
| Pro (2.5) | ~$1.25 | ~$10.00 |
| Gemini 3.1 Pro Preview | ~$2.00 | ~$12.00 |

**Cost levers that matter for your workloads:**
- **Batch mode ≈ 50% off** — asynchronous, non-real-time. Ideal for **PolicyPulse embedding backfills** and **StreamSmart eval-suite runs** (50–500 scenarios). Use it for any bulk job that isn't user-facing.
- **Context caching** (~$0.15–$1.00 / 1M / hour stored) — cache a large system prompt or knowledge base so repeated calls don't re-pay input. Relevant if a demo hammers the same context.
- **Google Search grounding** — 5,000 free prompts/month, then ~$14/1,000 (Gemini 3 line). Only matters if you add web grounding (e.g. an AFC trend node) — budget it separately from tokens.
- **Priority ≈ 1.8× standard** — guaranteed low latency; you almost certainly don't need it.

---

## 8. The `google-genai` Python SDK

The unified **`google-genai`** SDK is GA and is the one to use. The old `google-generativeai` package is **deprecated** — don't start anything new on it.

```bash
pip install google-genai
```

**Client — picks up your env var automatically:**
```python
from google import genai

# Reads GEMINI_API_KEY (or GOOGLE_API_KEY; if both set, GOOGLE_API_KEY wins).
client = genai.Client()

# ...or pass a specific key explicitly (e.g. to choose free vs paid, see §9):
client = genai.Client(api_key="...")
```

**Generate:**
```python
resp = client.models.generate_content(
    model="gemini-3.5-flash",
    contents="Summarize this 1099-R correction rule in one sentence.",
)
print(resp.text)
```

**Stream:**
```python
for chunk in client.models.generate_content_stream(
    model="gemini-3.5-flash", contents="Explain RAG grounding."
):
    print(chunk.text, end="")
```

**Structured output (Pydantic — matches your discipline):** all config/types are Pydantic classes in `google.genai.types`.
```python
from google import genai
from google.genai import types
from pydantic import BaseModel

class Correction(BaseModel):
    account_id: str
    old_tax_code: str
    new_tax_code: str
    reason: str

resp = client.models.generate_content(
    model="gemini-3.5-flash",
    contents="...",
    config=types.GenerateContentConfig(
        response_mime_type="application/json",
        response_schema=Correction,     # validated, typed output
    ),
)
obj: Correction = resp.parsed
```

**Embeddings (PolicyPulse):**
```python
from google.genai import types

result = client.models.embed_content(
    model="gemini-embedding-001",
    contents=[chunk1, chunk2, chunk3],
    config=types.EmbedContentConfig(
        task_type="RETRIEVAL_DOCUMENT",   # use RETRIEVAL_QUERY for the question side
        output_dimensionality=768,        # match your ChromaDB collection dim
    ),
)
vectors = [e.values for e in result.embeddings]
```

**Function calling / MCP (experimental, native):** you can hand the SDK a **local MCP server as a tool** directly — relevant to your FastMCP work.
```python
config=types.GenerateContentConfig(tools=[your_python_function])   # auto function calling
```

**Async** (for AFC's httpx-async style): `await client.aio.models.generate_content(...)`.
**Offline token counting:** `from google.genai import local_tokenizer` (no API call — good for cost pre-estimates).

---

## 9. Integrations (your stack)

**Provider-agnostic abstraction — same pattern as PolicyPulse/StreamSmart/AFC.** Gemini is the **fallback** provider (Anthropic primary). Nothing here changes that; it just makes the fallback real and lets you pick free vs paid explicitly.

```yaml
# config/ai_config.yaml  (consistent with your existing scopes)
ai:
  provider: "anthropic"                 # primary for RAG synthesis / financial reasoning
  fallback_provider: "gemini"
  generation_model: "claude-sonnet-4-6"
  gemini_model: "gemini-3.5-flash"
  embedding_model: "gemini-embedding-001"   # current GA (was text-embedding-004)
  temperature: 0.1
```

**Dual-key routing (the whole point of two projects):**
```python
import os
from google import genai

# FREE lane — synthetic/public scaffolding only (trained on)
free = genai.Client(api_key=os.environ["GEMINI_API_KEY_FREE"])
# PAID lane — public build at scale / Pro / no-train
paid = genai.Client(api_key=os.environ["GEMINI_API_KEY_PAID"])

def gemini(client, model, contents):
    return client.models.generate_content(model=model, contents=contents).text
```

**Where each Gemini capability earns its place in your portfolio:**
- **PolicyPulse (RAG)** — Gemini **embeddings** (`gemini-embedding-001`) into ChromaDB; Anthropic for synthesis. Run the initial embed as a **batch job** on the **paid** key for cost/limits, or free key if the corpus is small + synthetic.
- **FormSense (multimodal)** — **Gemini Vision** is the reason Gemini is in this project at all. Multimodal doc extraction on `gemini-3.5-flash` (or Pro for hard layouts). Synthetic/sample docs → free key fine; anything resembling real participant forms → **local**, not Gemini.
- **StreamSmart** — Gemini SDK primary; **`gemini-3.1-flash-lite` as the cheap safety-judge** in your eval pipeline. Batch the eval runs.
- **Model-routing chain** — Gemini direct (this SDK) is **not** the same as Gemini-via-OpenRouter. Use **Gemini direct** when you need **Gemini-native features** (Vision, native embeddings, structured multimodal, MCP tools); use **OpenRouter** for provider-agnostic *text* routing alongside DeepSeek/MiniMax. Don't route embeddings or Vision through OpenRouter's OpenAI-compat layer — go direct.

> 💡 **OpenCode/Cursor:** you can add Gemini as an OpenCode provider (OpenAI-compatible endpoint or native), but keep your **manual-commit gate** — Gemini is a model choice, not a change to the plan→build→review→commit discipline.

---

## 10. Environment & configuration

Never hardcode keys. Use env vars + a git-ignored `.env`.

```bash
# .env  (MUST be in .gitignore — see §11)
GEMINI_API_KEY_FREE=AIza...free
GEMINI_API_KEY_PAID=AIza...paid
```

| Variable | Picked up by SDK? | Notes |
|---|---|---|
| `GEMINI_API_KEY` | ✅ auto | Default the client reads |
| `GOOGLE_API_KEY` | ✅ auto | Also read; **wins if both set** — pick one convention to avoid surprises |
| `GEMINI_API_KEY_FREE` / `_PAID` | ❌ (explicit) | Your own names → pass via `genai.Client(api_key=...)` for dual-key routing |

- **Separate key per environment** (dev / demo / prod) is standard — and here, separate keys per **tier**.
- Load with `python-dotenv` or your existing config loader; keep the same YAML-config pattern you use across projects.

---

## 11. Security best practices (build-in-public matters here)

You publish repos and post on LinkedIn — a leaked key is a live risk, and Google is aggressive about it.

- 🔴 **Google auto-revokes keys detected in public GitHub repos.** A key that stops working right after a push probably got scanned and killed. **Prevent it:** `.env` in `.gitignore`, commit a `.env.example` with placeholder values only.
- **Never** put a key in frontend/JS or a notebook you'll push. If a demo needs client-side calls, **proxy through a backend**.
- **`.gitignore` must include:** `.env`, `.env.*`, `*.key`, any `secrets/` dir. Add a pre-commit secret scan (e.g. `gitleaks`) — a nice CI addition consistent with your ruff/mypy/pytest gates.
- If a key leaks: **revoke immediately** on the AI Studio API keys page, create a new one, replace everywhere, then audit git history + anywhere you shared it.
- **Budget alerts** on the paid project (Cloud Console) + you already have the mandatory $250 Tier-1 cap as a backstop.
- **Rotate** keys periodically (quarterly is fine for a portfolio).

---

## 12. Quick reference

**Setup checklist**
```
□ Project A (no billing)   → Create API key → confirm "Free"  → GEMINI_API_KEY_FREE
□ Project B (billing on)   → Create API key → Set up billing → prepay ≥ $10 → confirm "Paid" → GEMINI_API_KEY_PAID
□ Budget alert on Project B; note the $250/mo Tier-1 cap
□ .env (both keys) + .gitignore + .env.example committed
□ pip install google-genai
□ Smoke test: free key → gemini-3.5-flash ; paid key → gemini-3.1-pro-preview
```

**Code cheatsheet**
```python
from google import genai
from google.genai import types

client = genai.Client(api_key=KEY)                       # or genai.Client() to read env
client.models.generate_content(model=M, contents=T).text # generate
client.models.generate_content_stream(model=M, contents=T)  # stream
client.models.embed_content(model="gemini-embedding-001", contents=[...],
    config=types.EmbedContentConfig(task_type="RETRIEVAL_DOCUMENT"))  # embed
# structured: config=types.GenerateContentConfig(response_schema=MyPydanticModel,
#                        response_mime_type="application/json") -> resp.parsed
```

**Model quick-pick:** free/light → `gemini-3.1-flash-lite` · default → `gemini-3.5-flash` · hard/long → `gemini-3.1-pro-preview` (paid) · embeddings → `gemini-embedding-001`.

---

## 13. Tips (tailored)

- **Keep the free key "clean."** Its one job is synthetic/public scaffolding. The moment you're tempted to paste anything Daybright-shaped into it, that's the signal to route local instead. This is the discipline recruiters can't see but that keeps your ERISA story honest.
- **Batch the boring stuff.** PolicyPulse embedding backfills and StreamSmart eval sweeps are non-real-time → **Batch mode, paid key, ~50% off.** Real-time demo calls stay standard.
- **Gemini direct for Vision + embeddings; OpenRouter for text routing.** Don't collapse them — you lose the Gemini-native features that justify Gemini being in FormSense/PolicyPulse at all.
- **Update PolicyPulse to `gemini-embedding-001`** (from `text-embedding-004`) when you build it — embed on the current GA model, not the legacy one. (Scope edit — your call, not done here.)
- **Log provider/model/tokens/cost/latency per call** — you already specify this in scopes; the SDK's `local_tokenizer` lets you pre-estimate cost offline before a batch run.
- **The $250 cap is a friend.** It's the hard ceiling your PAYG philosophy already wants; set an alert well below it so a runaway loop pauses instead of surprising you.
- **Verify before you cite.** In a LinkedIn post or README, don't quote a Gemini price/limit from memory — link the pricing page. The numbers here are snapshots.

---

## 14. Troubleshooting

| Symptom | Cause / Fix |
|---|---|
| `429 RESOURCE_EXHAUSTED` | A limit hit (RPM/TPM/RPD/burst). Add **exponential backoff**; check the **AI Studio quota panel** for which one. More keys ≠ more quota. |
| Pro model call rejected on a working key | That key's project is **free tier**; Pro is **paid-only**. Use the paid key (Project B). |
| Key stopped working right after a `git push` | Likely **auto-revoked as leaked**. Revoke/recreate, move it to `.env`, add to `.gitignore`, force-scrub history. |
| Paid calls suddenly fail account-wide | **Prepay balance hit $0** (stops all projects on that billing account) or **monthly cap reached**. Top up / wait for cycle. |
| "Which tier am I on?" | AI Studio **Projects** page → **Billing Tier** column (Free / Paid). Tier is per **billing account**, inherited by its projects. |
| Env key not picked up | SDK reads `GEMINI_API_KEY` / `GOOGLE_API_KEY` only; your `_FREE`/`_PAID` names must be passed **explicitly** to `genai.Client(api_key=...)`. |
| `import google.generativeai` examples online don't match | That's the **deprecated** SDK. Use **`google-genai`** (`from google import genai`). |
| Embeddings dim mismatch in ChromaDB | Set `output_dimensionality` to match your collection; keep query/document `task_type` correct. |
| Region forces billing on a "free" model | EEA/UK/CH require billing even for free-eligible models (not US). |

---

## 15. Sources
ai.google.dev/gemini-api/docs — **Billing** (`/billing`: Prepay/Postpay, tier-per-billing-account, $10 upgrade min), **Pricing** (`/pricing`), **Embeddings** (`/embeddings`: `gemini-embedding-001`), **Migrate** (`/migrate`: `google-genai` GA, legacy deprecated) · github.com/googleapis/python-genai + pypi.org/project/google-genai (client, `generate_content`, `embed_content`, streaming, async, MCP, `local_tokenizer`) · how2shout / pecollective / tinkerllm / nocode.mba / comparedge / laozhang.ai — 2026 free-vs-paid, model split (Pro paid-only Apr 2026), rate limits (~10–15 RPM, 1,500 RPD free), pricing snapshots, $250 Tier-1 cap, public-GitHub auto-revocation, "keys don't add quota, projects/billing set tier." **Verify all model IDs, limits, and prices against the official pricing/docs pages before relying on them — they change often.**
