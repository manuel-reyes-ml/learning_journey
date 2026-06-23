# Ollama — Install, Use & Configuration Reference (Mac Apple Silicon)

**Focus:** Running local LLMs on an Apple-Silicon Mac (M-series), with config, model management, and integration into your stack (AnythingLLM, OpenCode, Python).
**Compiled:** June 2026 · Sized for a **Mac Mini M4 16GB** primary + MacBook Air M2 secondary.

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
ollama run qwen3.5:9b     # pulls on first use, then drops you into a chat REPL
```
- `ollama pull <model>` downloads without chatting.
- Inside the REPL: type to chat; **`/bye`** exits; **`"""`** opens a multi-line block; paste an **image** path for multimodal models; **Ctrl+G** opens your `$OLLAMA_EDITOR` for long prompts.
- Models live in `~/.ollama/models` (change with `OLLAMA_MODELS`). Default quantization is **Q4_K_M** unless a tag says otherwise (e.g. `qwen3:14b-q4_K_M`, `:q8_0`).

---

## 4. Model management commands

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

---

## 5. Picking models for a 16GB Mac

Rough planning: **~0.6 GB per 1B params** at Q4_K_M, plus context headroom. macOS reserves ~4GB, leaving ~12GB usable.

| Model | ~Size | Fit on 16GB | Best for |
|---|---|---|---|
| **Qwen3.5 9B** ⭐ | ~7 GB | ✅ clean | General reasoning / research; your primary local model |
| **Qwen2.5-Coder 7B** | ~5 GB | ✅ | Coding (pair with OpenCode local) |
| **Gemma 3/4 (4B / E4B)** | ~3–5 GB | ✅ | Efficient small model; second opinion |
| **Llama 3.2 3B / Phi-4-mini** | ~2–3 GB | ✅ | Fast utility/classification; run alongside a 9B |
| **DeepSeek-R1 distill 7–8B** | ~5 GB | ✅ | Step-by-step reasoning |
| **Qwen3 14B (q4_K_M)** | ~9–10 GB | ⚠️ tight | Loads but slow (~10–14 tok/s); use KV-cache tricks (§7) |
| **27B–35B+ / 70B** | 18 GB+ | ❌ | Needs 48GB+ unified memory |
| **nomic-embed-text** | ~0.3 GB | ✅ | Local embeddings (RAG) |

> 48GB-class Macs run 27B-class models; your roadmap's Stage-3 upgrade is what unlocks those. For now, 9B is the right ceiling.

---

## 6. The server & API (how apps connect)

The server runs at `http://localhost:11434`. Two interfaces:

**Native REST:**
```bash
curl http://localhost:11434/api/generate -d '{"model":"qwen3.5:9b","prompt":"Why is the sky blue?"}'
curl http://localhost:11434/api/tags        # list models
curl http://localhost:11434/api/ps          # loaded models
```
Endpoints: `/api/generate`, `/api/chat`, `/api/embeddings`, `/api/tags`, `/api/ps`.

**OpenAI-compatible** (this is what AnythingLLM, OpenCode, Continue use):
```
Base URL: http://localhost:11434/v1
Endpoint: /v1/chat/completions      Model: the exact tag, e.g. qwen3.5:9b
API key:  any non-empty string (ignored locally)
```

**Expose to your LAN** (e.g. serve the Air from the Mini): in the menu-bar app → **Settings → "Expose Ollama to the network"** (v0.94+). Or set `OLLAMA_HOST=0.0.0.0:11434`.
> ⚠️ Binding to `0.0.0.0` exposes the API on all interfaces with **no auth**. Only do this on a trusted network, ideally behind a firewall rule (`sudo ufw allow from 192.168.1.0/24 to any port 11434`).

---

## 7. Configuration & environment variables

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
| `OLLAMA_ORIGINS` | localhost | Allowed CORS origins for browser apps |
| `OLLAMA_EDITOR` | — | Editor for the REPL's Ctrl+G prompt editing |
| `OLLAMA_DEBUG` | off | Verbose logs for troubleshooting |

---

## 8. Mac performance tuning (16GB)

- **Keep it on the GPU.** Check `ollama ps` shows ~100% GPU. If it spills to CPU, the model+context is too big — shrink one.
- **Avoid reload lag:** `OLLAMA_KEEP_ALIVE=-1` keeps your model resident (trades RAM for instant responses). Good when you bounce between OpenCode and AnythingLLM.
- **Fit bigger contexts in less RAM:** `OLLAMA_FLASH_ATTENTION=1` + `OLLAMA_KV_CACHE_TYPE=q8_0` together can free 2–6 GB at long context with negligible quality loss. *Caveat:* a few reports note slight slowdowns from q8_0 KV cache on Apple's Metal backend specifically — if generation feels slower, revert to `f16`.
- **Shrink to fit when needed:** drop quant (`...:14b-q4_K_M`), lower `OLLAMA_CONTEXT_LENGTH` (e.g. 2048), or step down a size (14B→9B frees several GB).
- **Memory pressure (Activity Monitor):** yellow is fine (mild swap); **red = active swapping = unusable** — unload something.
- After major **macOS or Ollama updates**, fully restart the Mac and re-check `ollama ps`; pin a known-good version via Homebrew if a release regresses.

---

## 9. Custom models (Modelfile)

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
Directives: `FROM`, `SYSTEM`, `PARAMETER` (temperature, num_ctx, num_predict, top_p, …), `TEMPLATE`, `ADAPTER` (LoRA), `MESSAGE`.

---

## 10. Integrations (your stack)

- **AnythingLLM:** LLM provider → Ollama → Base URL `http://localhost:11434`, model `qwen3.5:9b`. Keep its built-in local embedder, or point embeddings at Ollama's `nomic-embed-text`. → free, private research/RAG.
- **OpenCode:** add a local provider at `http://localhost:11434/v1` (model `qwen2.5-coder:7b`) for free, private agentic coding.
- **Python:**
  ```bash
  pip install ollama          # native client
  ```
  ```python
  import ollama
  print(ollama.chat(model="qwen3.5:9b",
        messages=[{"role":"user","content":"hi"}])["message"]["content"])
  ```
  Or use the OpenAI SDK / `langchain-ollama` against `http://localhost:11434/v1`.
- **LAN serving:** expose the Mini (§6) and point the Air's tools at `http://<mini-ip>:11434`.

---

## 11. CLI quick reference

```bash
ollama run <model>            # chat (pull if needed)
ollama pull <model>           # download
ollama list                   # local models
ollama ps                     # loaded models + GPU%
ollama show <model>           # model info
ollama stop <model>           # unload now
ollama rm <model>             # delete
ollama cp <src> <dst>         # copy/rename
ollama create <name> -f Modelfile   # build custom model
ollama serve                  # start server manually
ollama --version | --help
```

---

## 12. Tips (tailored)

- **Privacy split:** keep finance/proprietary work on local Ollama (Qwen3.5 9B / Qwen2.5-Coder 7B) = $0 + on-device; reserve cloud (GLM-5.2 via OpenRouter) for public/heavy tasks.
- **Move the model dir early** (`OLLAMA_MODELS`) if your system drive is tight — models stack up fast (~5GB each).
- **Two models at once:** a 4B utility + a 9B generalist both fit in 16GB and `ollama ps` lets you watch memory; raise `OLLAMA_MAX_LOADED_MODELS` only if they fit.
- **Embeddings locally:** `ollama pull nomic-embed-text` gives you a free RAG embedder.
- **MLX vs GGUF:** MLX runs safetensors models ~10–20% faster on Apple Silicon; GGUF via `ollama pull` is the broadest. Ollama auto-picks by format — worth A/B testing on Qwen for your Stage-3 inference work.
- **Stay current** for Metal/engine improvements, but pin a version if a release regresses.

---

## 13. Troubleshooting

| Symptom | Cause / Fix |
|---|---|
| `ollama: command not found` | Open a new terminal (PATH refresh) after install |
| Env vars ignored | The **app** ignores shell vars → use `launchctl setenv VAR "value"` and restart the app |
| `ollama ps` shows GPU% < 100 | Model+context too big → smaller model, lower quant, or shorter context |
| Red memory pressure / very slow | Active swapping → unload a model, shrink context, or drop a size |
| Model reloads after idle (10s lag) | `OLLAMA_KEEP_ALIVE=-1` to keep it resident |
| Long context blows up RAM | Enable `OLLAMA_FLASH_ATTENTION=1` + `OLLAMA_KV_CACHE_TYPE=q8_0` |
| Port 11434 in use | A server/app is already running → `ollama ps`, or quit the app before `ollama serve` |
| Other devices can't connect | Enable "Expose to network" / `OLLAMA_HOST=0.0.0.0:11434` (+ firewall) |
| Perf dropped after macOS update | Full restart (not sleep), re-check `ollama ps`; pin a known-good Ollama version |

---

## 14. Sources
docs.ollama.com (FAQ, API, Modelfile) · ollama.com/library · github.com/ollama/ollama (`envconfig/config.go`) · InsiderLLM "Ollama on Mac 2026" · SitePoint "Ollama Setup Guide 2026" · ModelPiper "Ollama Environment Variables 2026" · llmhardware.io Ollama cheat sheet · LMSA install guide. Verify command names, defaults, and model tags against `docs.ollama.com` and `ollama.com/library` before relying on them.
