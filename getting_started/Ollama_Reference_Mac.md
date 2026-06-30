# Ollama — Install, Use & Configuration Reference (Mac Apple Silicon)

**Focus:** Running local LLMs on an Apple-Silicon Mac (M-series), with config, model management, and integration into your stack (AnythingLLM, OpenCode, Python).
**Compiled:** June 2026 · Sized for a **Mac Mini M4 16GB** primary + MacBook Air M2 secondary.
**Version:** 2.0 (June 29, 2026)

> 📝 **Changelog v2.0:** + §6.1 model cleanup / deletion workflow (`ollama rm`, multi-delete, delete-all, blob pruning, **unload ≠ delete**) · + §7.1 Qwen 3.5 → 3.6 on 16GB — the 3.6 open-weight lineup **starts at 27B/35B-A3B (no 9B)**, so **stay on 3.5 9B locally**; `qwen3.6:27b` is the **Stage-3 48GB** unlock; reach 3.6 **now via cloud** (`qwen3.6-plus` on OpenRouter). v1.1 below unchanged.

> 📝 **Changelog v1.1:** + §4 Interactive REPL commands (`/set`, `/show`, verbose stats) · + §5 Thinking / reasoning-mode control (shell flags, `/set think`, API, GUI) · + §8 structured outputs (JSON) & tool calling · + extra env vars (§9), Modelfile params & GGUF import (§11), CLI flags (§13), and thinking-related troubleshooting (§15). v1.0 = original.

> ⚠️ Ollama ships frequently and defaults shift between releases. Treat **`docs.ollama.com`** and **`ollama.com/library`** as the source of truth, and run **`ollama --help`** for your installed build. Model tags below are representative — check the library for current ones.

---

## 1. Mental model (what Ollama is)

Ollama is the **local model runtime** — "a package manager for LLMs." One command fetches a model, sets it up, and exposes a local API. It runs three things at once:
- a **menu-bar app** (GUI chat + settings),
- a **CLI** (`ollama …`),
- a **background server** at `http://localhost:11434` (REST + an OpenAI-compatible endpoint).

On Apple Silicon it uses **Metal GPU acceleration out of the box** — no CUDA, no drivers, no Docker. Unified memory means CPU and GPU share one RAM pool, so a 16GB Mac can load models that would need a dedicated GPU elsewhere. Everything runs **on-device** — no tokens billed, works offline, data never leaves your machine. This is the free, private engine that AnythingLLM and OpenCode plug into.

---

## 2. Install & update

**Option A — Desktop app (recommended):** Go to **ollama.com/download** → Download for macOS → unzip → drag **Ollama** into Applications → launch. You get the menu-bar app *and* the `ollama` CLI.

**Option B — Homebrew:**
```bash
brew install ollama          # CLI + server
brew upgrade ollama          # keep current
# pin a known-good version if an update regresses:
brew install ollama@0.15.4
```

**Apple Silicon:** Metal acceleration works automatically (M1–M5). Nothing extra to install.

**Verify:**
```bash
ollama --version
ollama list        # empty on a fresh install = daemon is up and ready
```

> **2026 engine note:** Ollama 0.30+ auto-routes by file format — **MLX** runner for safetensors, **llama.cpp Metal** for GGUF (what `ollama pull` usually lands). First launch after upgrading does a one-time storage migration to a content-addressable format.

---

## 3. Download & run your first model

```bash
ollama run qwen3.5:9b              # pulls on first use, then drops you into a chat REPL
ollama run qwen3.5:9b --verbose    # same, but prints tokens/sec stats after each reply
```
- `ollama pull <model>` downloads without chatting.
- Inside the REPL: type to chat; **`/bye`** exits; **`"""`** opens a multi-line block; paste an **image** path for multimodal models; **Ctrl+G** opens your `$OLLAMA_EDITOR` for long prompts. (Full command list in §4.)
- Models live in `~/.ollama/models` (change with `OLLAMA_MODELS`). Default quantization is **Q4_K_M** unless a tag says otherwise (e.g. `qwen3:14b-q4_K_M`, `:q8_0`).

---

## 4. Interactive REPL commands (inside `ollama run`)

Once you're in a chat session, lines starting with `/` are **REPL commands** (handled by Ollama, not sent to the model). Type `/?` to list them all.

| Command | Does |
|---|---|
| `/set verbose` | Print stats after each reply (**tokens/sec**, eval count) — fastest way to diagnose slowness |
| `/set quiet` | Turn stats back off |
| `/set think` · `/set nothink` | Enable / disable reasoning (see §5) |
| `/set parameter num_ctx 8192` | Change a parameter live (also `temperature`, `top_p`, `num_predict`, …) |
| `/set system "..."` | Set a system prompt for this session |
| `/set format json` · `/set noformat` | Force / stop JSON-only output |
| `/set history` · `/set nohistory` | Keep / drop conversation context between turns |
| `/show info` | Model details (params, context, quant) |
| `/show modelfile` · `/show parameters` · `/show template` · `/show system` · `/show license` | Inspect the model's config |
| `/load <model>` · `/save <name>` | Switch model mid-session / save the session as a new model |
| `/clear` | Clear the conversation context |
| `/bye` | Exit the session |
| `/?` (or `/help`) | List all commands |

> **Tip:** `/set verbose` shows your real tok/s. **Under ~5 tok/s usually means CPU spill** (model+context don't fit) — see §10. This is the quickest way to confirm whether "slow" is the model or your memory.

---

## 5. Thinking / reasoning-mode control

Reasoning models — **Qwen3 / Qwen3.5, DeepSeek-R1, Gemma 4, gpt-oss** — generate a hidden chain-of-thought *before* the answer. It genuinely improves multi-step logic and math, but adds latency, and it's **ON by default**. Plain models (Llama 3, Mistral, Phi-4) have no thinking mode — the setting is silently ignored.

**Controls (most → least reliable on Qwen3.5):**

| Method | How |
|---|---|
| **Launch flag** | `ollama run qwen3.5:9b --think=false` (off) · `--think` (on) · `--hidethinking` (think but hide the trace) |
| **In-session (REPL)** | `/set nothink` (off) · `/set think` (on) |
| **API** | `"think": false` in `/api/chat` or `/api/generate`. *(gpt-oss expects `"low"\|"medium"\|"high"`, not true/false.)* |
| **In-prompt soft switch** | append `/no_think` or `/think` inside your message — works on much of the Qwen3 family, but **unreliable specifically on Qwen3.5**; prefer the flag or `/set` |
| **Make off the default** | bake it into a Modelfile (§11) and run that variant — handy for GUI tools |

**Desktop GUI app:** the bundled chat has **no thinking toggle yet** (open feature request). For an on/off switch in a GUI, run the model through **AnythingLLM or LM Studio**, or just pick a **non-thinking model** for quick tests.

**When to use:** ON for math, multi-step logic, hard reasoning; **OFF for quick Q&A, summaries, extraction** — disabling can be **2–5× faster**.

> ⚠️ **Version caveat:** some builds (e.g. 0.20.6) ignored `/set nothink`. If toggles don't take effect, update — or pin a known-good version.

---

## 6. Model management commands

| Command | Does |
|---|---|
| `ollama run <model>` | Pull (if needed) + interactive chat |
| `ollama pull <model>` | Download/update a model |
| `ollama list` (`ls`) | List local models + sizes |
| `ollama ps` | Show **loaded** models: memory, processor, **GPU%**, unload timer |
| `ollama show <model>` | Model details (params, context, license, template) |
| `ollama stop <model>` | Unload from memory now |
| `ollama rm <model>` | Delete to free disk |
| `ollama cp <src> <dst>` | Copy/rename a model |
| `ollama create <name> -f Modelfile` | Build a custom model |
| `ollama serve` | Start the server manually (if not using the app) |

> `ollama ps` is your health check: **GPU% at 100%** = full Metal acceleration; below 100% = partial CPU offload (much slower), usually meaning the model + context don't fit in memory.

### 6.1 Cleaning up / deleting models (free disk)

Models stack up fast (~5–17 GB each) in `~/.ollama/models`. **Deleting ≠ unloading:** `ollama stop` and `OLLAMA_KEEP_ALIVE` only free **RAM**; only `ollama rm` frees **disk**.

```bash
ollama list                       # 1. see what you have + sizes — decide what to cut
ollama rm qwen3:14b               # 2. delete one model (frees its disk right away)
ollama rm qwen3:14b llama3.2:3b   #    …or several at once
ollama list                       # 3. confirm it's gone
du -sh ~/.ollama/models           # 4. check the space you reclaimed
```
- `rm` deletes the **named tag**. Ollama's store is content-addressable, so blobs shared with another model are **kept** — removing one variant won't break another.
- **Wipe everything (start clean):** `ollama rm $(ollama list | tail -n +2 | awk '{print $1}')` — removes every listed model. Eyeball `ollama list` first.
- **Reclaim orphaned blobs** after heavy churn: restart the Ollama app (or `ollama serve`) — it prunes unused blobs at startup unless `OLLAMA_NOPRUNE` is set (§9).
- Keep only what you actually route to: your **`qwen3.5:9b`** planner + a **`qwen2.5-coder:7b`** for FIM + maybe **`nomic-embed-text`** is a lean, 16GB-friendly set; delete experiments once benchmarked.

---

## 7. Picking models for a 16GB Mac

Rough planning: **~0.6 GB per 1B params** at Q4_K_M, plus context headroom. macOS reserves ~4GB, leaving ~12GB usable.

| Model | ~Size | Fit on 16GB | Best for |
|---|---|---|---|
| **Qwen3.5 9B** ⭐ | ~7 GB | ✅ clean | General reasoning / research; your primary local model |
| **Qwen2.5-Coder 7B** | ~5 GB | ✅ | Coding autocomplete/FIM (pair with OpenCode local) |
| **Gemma 3/4 (4B / E4B)** | ~3–5 GB | ✅ | Efficient small model; native tool-calling; second opinion |
| **Llama 3.2 3B / Phi-4-mini** | ~2–3 GB | ✅ | Fast utility/classification; run alongside a 9B; no thinking overhead |
| **DeepSeek-R1 distill 7–8B** | ~5 GB | ✅ | Step-by-step reasoning |
| **Qwen3 14B (q4_K_M)** | ~9–10 GB | ⚠️ tight | Loads but slow (~10–14 tok/s); use KV-cache tricks (§10) |
| **27B–35B+ / 70B** | 18 GB+ | ❌ | Needs 48GB+ unified memory |
| **nomic-embed-text** | ~0.3 GB | ✅ | Local embeddings (RAG) |

> 48GB-class Macs run 27B-class models; your roadmap's Stage-3 upgrade is what unlocks those. For now, 9B is the right ceiling.

### 7.1 Qwen 3.5 → 3.6 on a 16GB Mac (what to actually download)

**Is 3.6 better than 3.5?** Yes — at the *same* class it's a clean generational win: **Qwen 3.6-35B-A3B** scores **73.4 on SWE-bench Verified vs 70.0** for the 3.5 release, with double-digit gains on agentic / tool-use (Terminal-Bench, MCPMark), a **1M-token** native context, and no reasoning regression.

**But none of the 3.6 *local* models fit 16GB.** The open-weight 3.6 lineup **starts at 27B** — there is **no Qwen 3.6 9B** (the 4B/9B tier 3.5 shipped wasn't carried forward):

| Qwen 3.6 (local) | ~Size (Q4) | Min RAM | Verdict on your Mini |
|---|---|---|---|
| **27B dense** (best open coder, 77.2 SWE-bench) | ~16.8 GB | 24 GB | ❌ swaps hard on 16GB |
| **35B-A3B MoE** (3B active, best general) | ~18 GB+ | 32 GB+ | ❌ |
| **9B** | — | — | ❌ doesn't exist in 3.6 |

So on the Mac Mini M4 16GB:
- **Stay on `qwen3.5:9b`** as your local primary — still the right 16GB ceiling (Apache-2.0, ~7 GB, clean Metal fit). Don't pull a 3.6 here; the 27B's weights alone (16.8 GB) exceed your usable RAM.
- **`qwen3.6:27b` is your Stage-3 (48GB) unlock** — that hardware upgrade is exactly what makes the current best local coder runnable (≈25 tok/s on a 48GB-class Mac).
- **Want 3.6 *now*?** Use it on the **cloud lane**, not locally: `qwen3.6-plus` via OpenRouter (OpenAI-compatible → drops into OpenCode), same privacy split as MiniMax M3 / GLM-5.2 — public/heavy → cloud, finance/proprietary → local 3.5 9B.

> Bottom line for 16GB: the 3.6 jump is a **hardware** upgrade, not a download. Keep 3.5 9B local; reach 3.6 via cloud until Stage 3.

---

## 8. The server & API (how apps connect)

The server runs at `http://localhost:11434`. Two interfaces:

**Native REST:**
```bash
curl http://localhost:11434/api/generate -d '{"model":"qwen3.5:9b","prompt":"Why is the sky blue?"}'
curl http://localhost:11434/api/tags        # list models
curl http://localhost:11434/api/ps          # loaded models
```
Endpoints: `/api/generate`, `/api/chat`, `/api/embed` (current) or `/api/embeddings` (legacy), `/api/tags`, `/api/ps`.

**OpenAI-compatible** (this is what AnythingLLM, OpenCode, Continue use):
```
Base URL: http://localhost:11434/v1
Endpoint: /v1/chat/completions      Model: the exact tag, e.g. qwen3.5:9b
API key:  any non-empty string (ignored locally)
```

**Structured outputs (JSON):** pass `"format": "json"` *or* a full **JSON Schema** object in the request — Ollama enforces it during decoding, which eliminates whole classes of parse/retry loops. Big win for **eval pipelines and agents** that need predictable output.
```bash
curl http://localhost:11434/api/chat -d '{
  "model":"qwen3.5:9b",
  "messages":[{"role":"user","content":"List 3 risks as JSON"}],
  "format":"json","stream":false
}'
```

**Tool / function calling:** OpenAI-compatible `tools` / `tool_choice` are supported by **Qwen3, Llama 3.1+, Mistral, DeepSeek** — so agent frameworks (LangGraph, CrewAI, OpenCode) can call functions through your local models with the same shape they use for cloud models.

**Expose to your LAN** (e.g. serve the Air from the Mini): in the menu-bar app → **Settings → "Expose Ollama to the network"** (v0.94+). Or set `OLLAMA_HOST=0.0.0.0:11434`.
> ⚠️ Binding to `0.0.0.0` exposes the API on all interfaces with **no auth**. Only do this on a trusted network, ideally behind a firewall rule (`sudo ufw allow from 192.168.1.0/24 to any port 11434`).

---

## 9. Configuration & environment variables

Set behavior via env vars. **macOS gotcha:** the menu-bar app **ignores your shell profile** — set vars with `launchctl` and restart the app:
```bash
launchctl setenv OLLAMA_KEEP_ALIVE "-1"
launchctl setenv OLLAMA_FLASH_ATTENTION "1"
# then quit & relaunch the Ollama app
```
(If you run the CLI/`ollama serve` from your shell instead, normal `export VAR=…` works.)

| Variable | Default | What it does |
|---|---|---|
| `OLLAMA_HOST` | `127.0.0.1:11434` | Bind address (set `0.0.0.0:11434` for LAN) |
| `OLLAMA_MODELS` | `~/.ollama/models` | Where models are stored (move to a bigger drive early) |
| `OLLAMA_KEEP_ALIVE` | `5m` | How long a model stays in RAM. **`-1` = keep loaded indefinitely**, **`0` = unload immediately** |
| `OLLAMA_CONTEXT_LENGTH` | `4k` (VRAM-aware: 4k/32k/256k) | Default context window |
| `OLLAMA_FLASH_ATTENTION` | off | `1` enables Flash Attention — cuts memory as context grows |
| `OLLAMA_KV_CACHE_TYPE` | `f16` | `q8_0` ≈ half the KV-cache RAM (needs Flash Attention); `q4_0` ≈ quarter |
| `OLLAMA_NUM_PARALLEL` | auto (1–4) | Parallel requests per model (RAM scales with it) |
| `OLLAMA_MAX_LOADED_MODELS` | 3 | Concurrent models that fit in memory |
| `OLLAMA_MAX_QUEUE` | 512 | Queued requests before rejecting |
| `OLLAMA_LOAD_TIMEOUT` | `5m` | How long to wait for a slow model load before giving up |
| `OLLAMA_GPU_OVERHEAD` | 0 | Reserve VRAM headroom (bytes) to avoid OOM when other apps use the GPU |
| `OLLAMA_ORIGINS` | localhost | Allowed CORS origins for browser apps |
| `OLLAMA_NOHISTORY` | off | Disable the REPL history file |
| `OLLAMA_NOPRUNE` | off | Don't prune unused model blobs at startup |
| `OLLAMA_EDITOR` | — | Editor for the REPL's Ctrl+G prompt editing |
| `OLLAMA_DEBUG` | off | Verbose logs for troubleshooting |

---

## 10. Mac performance tuning (16GB)

- **Keep it on the GPU.** Check `ollama ps` shows ~100% GPU. If it spills to CPU, the model+context is too big — shrink one.
- **Diagnose with `/set verbose`** (or `--verbose`): if tok/s is in the low single digits, you're CPU-bound, not "thinking too hard."
- **Avoid reload lag:** `OLLAMA_KEEP_ALIVE=-1` keeps your model resident (trades RAM for instant responses). Good when you bounce between OpenCode and AnythingLLM.
- **Fit bigger contexts in less RAM:** `OLLAMA_FLASH_ATTENTION=1` + `OLLAMA_KV_CACHE_TYPE=q8_0` together can free 2–6 GB at long context with negligible quality loss. *Caveat:* a few reports note slight slowdowns from q8_0 KV cache on Apple's Metal backend specifically — if generation feels slower, revert to `f16`.
- **Shrink to fit when needed:** drop quant (`...:14b-q4_K_M`), lower context live with `/set parameter num_ctx 2048` (or `OLLAMA_CONTEXT_LENGTH`), or step down a size (14B→9B frees several GB).
- **Turn off thinking for quick tasks** (§5) — on a memory-tight Mac a runaway reasoning trace makes a slow model feel frozen.
- **Memory pressure (Activity Monitor):** yellow is fine (mild swap); **red = active swapping = unusable** — unload something.
- After major **macOS or Ollama updates**, fully restart the Mac and re-check `ollama ps`; pin a known-good version via Homebrew if a release regresses.

---

## 11. Custom models (Modelfile)

A `Modelfile` defines a reusable model profile — base model + system prompt + parameters.
```dockerfile
# Modelfile — local coding assistant, 8K context, low temperature
FROM qwen2.5-coder:7b
SYSTEM """
You are an expert software engineer. Explain what the code does and why,
write clean commented code, and never leave changes unexplained.
"""
PARAMETER temperature 0.3
PARAMETER num_ctx 8192
PARAMETER num_predict 2048
```
```bash
ollama create coder-mentor -f Modelfile
ollama run coder-mentor
```

**Directives:** `FROM`, `SYSTEM`, `PARAMETER`, `TEMPLATE`, `ADAPTER` (LoRA), `MESSAGE`.
**Common `PARAMETER`s:** `temperature`, `top_p`, `top_k`, `repeat_penalty`, `num_ctx` (context), `num_predict` (max output), `num_gpu` (layers on GPU), `num_thread`, `stop`, `seed`.

**Import a GGUF you downloaded** (e.g. an MLX/quant variant from Hugging Face):
```dockerfile
FROM ./Qwen3.5-9B-Q4_K_M.gguf
```

**A "no-think by default" variant** (handy for GUI tools that lack a toggle):
```dockerfile
FROM qwen3:8b
SYSTEM "/no_think"
```
```bash
ollama create qwen3-fast -f Modelfile   # then pick "qwen3-fast" in any GUI
```
> Reliable for the Qwen3 family; **finicky on Qwen3.5** — for 3.5 the `--think=false` flag or API `think:false` is more dependable than a Modelfile.

---

## 12. Integrations (your stack)

- **AnythingLLM:** LLM provider → Ollama → Base URL `http://localhost:11434`, model `qwen3.5:9b`. Keep its built-in local embedder, or point embeddings at Ollama's `nomic-embed-text`. → free, private research/RAG. *(Also a good place to toggle thinking via its own UI.)*
- **OpenCode:** add a local provider at `http://localhost:11434/v1` (model `qwen2.5-coder:7b` for FIM, `qwen3.5:9b` for agent/learning) for free, private agentic coding.
- **Python:**
  ```bash
  pip install ollama          # native client
  ```
  ```python
  import ollama
  print(ollama.chat(model="qwen3.5:9b",
        messages=[{"role":"user","content":"hi"}],
        think=False)["message"]["content"])   # think=False skips reasoning
  ```
  Or use the OpenAI SDK / `langchain-ollama` against `http://localhost:11434/v1`.
- **LAN serving:** expose the Mini (§8) and point the Air's tools at `http://<mini-ip>:11434`.

---

## 13. CLI quick reference

```bash
ollama run <model>                 # chat (pull if needed)
ollama run <model> --think=false   # disable reasoning for the session
ollama run <model> --think         # force reasoning on
ollama run <model> --hidethinking  # think but hide the trace
ollama run <model> --verbose       # print tokens/sec + timing stats
ollama run <model> --format json   # force JSON-only output
ollama pull <model>                # download
ollama list                        # local models
ollama ps                          # loaded models + GPU%
ollama show <model>                # model info
ollama show <model> --modelfile    # dump its Modelfile (base to edit/fork)
ollama stop <model>                # unload now
ollama rm <model>                  # delete
ollama cp <src> <dst>              # copy/rename
ollama create <name> -f Modelfile  # build custom model
ollama serve                       # start server manually
ollama --version | --help
```

---

## 14. Tips (tailored)

- **Privacy split:** keep finance/proprietary work on local Ollama (Qwen3.5 9B / Qwen2.5-Coder 7B) = $0 + on-device; reserve cloud (GLM-5.2 via OpenRouter) for public/heavy tasks.
- **Thinking on demand:** default-off for speed during quick work; flip on (`/set think`) for genuine math/logic. Bake a `*-fast` no-think variant for instant testing.
- **Move the model dir early** (`OLLAMA_MODELS`) if your system drive is tight — models stack up fast (~5GB each).
- **Two models at once:** a 4B utility + a 9B generalist both fit in 16GB and `ollama ps` lets you watch memory; raise `OLLAMA_MAX_LOADED_MODELS` only if they fit.
- **Embeddings locally:** `ollama pull nomic-embed-text` gives you a free RAG embedder.
- **MLX vs GGUF:** MLX runs safetensors models ~10–20% faster on Apple Silicon; GGUF via `ollama pull` is the broadest. Ollama auto-picks by format — worth A/B testing on Qwen for your Stage-3 inference work.
- **Stay current** for Metal/engine improvements, but pin a version if a release regresses.

---

## 15. Troubleshooting

| Symptom | Cause / Fix |
|---|---|
| `ollama: command not found` | Open a new terminal (PATH refresh) after install |
| Env vars ignored | The **app** ignores shell vars → use `launchctl setenv VAR "value"` and restart the app |
| `ollama ps` shows GPU% < 100 | Model+context too big → smaller model, lower quant, or shorter context |
| Red memory pressure / very slow | Active swapping → unload a model, shrink context, or drop a size |
| Model "thinks" forever / huge delay before output | Disable reasoning: `/set nothink` or `--think=false` — **and** confirm it's not memory spill (`/set verbose`, §10) |
| `/no_think` ignored on Qwen3.5 | Use `--think=false` or `/set nothink` instead (the in-prompt switch is unreliable on 3.5) |
| No thinking toggle in the desktop app | Expected — use AnythingLLM/LM Studio, or a non-thinking model |
| `/set nothink` does nothing | Possible version bug (e.g. 0.20.6) → update or pin a known-good build |
| Want to see real tok/s | `/set verbose` (or launch with `--verbose`) |
| Model reloads after idle (10s lag) | `OLLAMA_KEEP_ALIVE=-1` to keep it resident |
| Long context blows up RAM | Enable `OLLAMA_FLASH_ATTENTION=1` + `OLLAMA_KV_CACHE_TYPE=q8_0` |
| Port 11434 in use | A server/app is already running → `ollama ps`, or quit the app before `ollama serve` |
| Other devices can't connect | Enable "Expose to network" / `OLLAMA_HOST=0.0.0.0:11434` (+ firewall) |
| Perf dropped after macOS update | Full restart (not sleep), re-check `ollama ps`; pin a known-good Ollama version |

---

## 16. Sources
docs.ollama.com (FAQ, API, **Thinking** `/capabilities/thinking`, Modelfile) · ollama.com/blog/thinking · ollama.com/library (qwen3.5 / qwen3.6 tags) · github.com/ollama/ollama (`envconfig/config.go`, issues #15962 / #16016 / #15536 on GUI thinking toggle) · InsiderLLM "Best Qwen Models Ranked" (3.6 lineup: 27B / 35B-A3B, no 9B) · Tessera "Qwen 3.6 vs 3.5" (73.4 vs 70.0 SWE-bench) · codersera "Qwen 3.5/3.6/3.7 guide" · serverman.co.uk "Ollama Thinking Mode" · InsiderLLM "Ollama on Mac 2026" · SitePoint "Ollama Setup Guide 2026" · ModelPiper "Ollama Environment Variables 2026" · llmhardware.io Ollama cheat sheet. Verify command names, defaults, and model tags against `docs.ollama.com` and `ollama.com/library` before relying on them.