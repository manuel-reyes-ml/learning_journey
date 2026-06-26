# LM Studio — Install, Use & Configuration Reference (Mac Apple Silicon)

**Focus:** Running local LLMs on an Apple-Silicon Mac (M-series) via LM Studio, with config, MLX model management, and integration into your stack (OpenCode, AnythingLLM, Python).
**Compiled:** June 2026 · Sized for a **Mac Mini M4 16GB** primary + MacBook Air M2 secondary.
**Version:** 1.0 (June 24, 2026)

> 📝 **Why this exists:** companion to the Ollama reference. LM Studio is the **GUI-first** alternative that makes the **MLX runtime** trivial to use — the main reason to run it alongside Ollama. This guide is built around an **A/B test**: does MLX beat your Ollama (GGUF/Metal) setup on *your* 16GB hardware? (Honest answer up front in §5 and §14.)

> ⚠️ LM Studio ships frequently and UI labels shift between releases. Treat **`lmstudio.ai/docs`** as the source of truth, and run **`lms --help`** (and `lms <subcommand> --help`) for your installed build. Model names below are representative — check the in-app search / Hugging Face for current ones.

---

## 1. Mental model (what LM Studio is)

LM Studio is a **local model runtime wrapped in a desktop GUI** — think "Ollama with a graphical front end and first-class MLX support." It bundles four things:
- a **desktop app** (model search, chat UI, parameter tuning, per-model presets),
- an **`lms` CLI** (`lms load`, `lms server …`, scriptable/headless),
- a **local server** at `http://localhost:1234` (OpenAI-, Anthropic-, and native-compatible endpoints),
- two swappable **inference engines**: **llama.cpp** (GGUF) and **MLX** (Apple's native framework, safetensors).

On Apple Silicon it runs **on-device** — free, offline, data never leaves the Mac. The big differentiator vs Ollama on your 16GB Mac: **LM Studio's MLX engine has no 32GB floor** (Ollama's MLX path requires 32GB+, so your Mini otherwise stays on llama.cpp/Metal). This is the free, private engine OpenCode and AnythingLLM can plug into — same role as Ollama, different backend options.

> **Two tools, no conflict:** Ollama listens on **11434**, LM Studio on **1234**. You can run both and switch between them in OpenCode by changing which provider/model you select — ideal for the A/B test.

---

## 2. Install & update

**Desktop app (recommended):** go to **lmstudio.ai** → Download for macOS (Apple Silicon) → open the `.dmg` → drag **LM Studio** into Applications → launch. The first launch installs the **`lms` CLI** onto your PATH automatically.

**Requirements:** Apple Silicon (M1+), macOS 13.6 Ventura minimum (14.x Sonoma+ recommended), **16GB+ recommended for 7–9B models**. (Intel Macs run GGUF only — MLX is hidden.)

**Bootstrap the CLI** (if `lms` isn't found after first run):
```bash
~/.lmstudio/bin/lms bootstrap     # adds lms to PATH; open a new terminal after
lms --version
```

**Update:** the app self-updates (or re-download from lmstudio.ai). Update the **inference runtimes** separately — this is how you get newer MLX/llama.cpp engine versions and day-one model support:
```bash
lms runtime          # list / manage inference runtimes (MLX, llama.cpp)
```
> Keep the **MLX runtime** current — new model architectures often need a fresh engine. App update ≠ runtime update.

---

## 3. Download & run your first model

**GUI:** click the 🔍 **Search** (Discover) tab → search `qwen3.5 9b` → in the results, pick a **format badge**: look for **MLX** (Apple-optimized) vs **GGUF** (llama.cpp). Choose a quantization (start **4-bit** for a 9B on 16GB) → **Download** → go to 💬 **Chat**, load it, and talk to it.

**CLI:**
```bash
lms get qwen3.5-9b            # search + download (interactive picker; shows MLX & GGUF)
lms get mlx-community/Qwen3.5-9B-Instruct-4bit   # grab a specific MLX repo directly
lms ls                        # list downloaded models + sizes (--json for scripts)
lms load qwen3.5-9b           # load into memory (see §9 for --context-length, --gpu, --ttl)
lms chat                      # quick terminal chat to sanity-check it
```
- Models live in **`~/.cache/lm-studio/models/`** (changeable in **My Models** tab).
- `lms get` with no argument shows staff-picked recommendations.
- To grab the MLX build specifically, filter the in-app search by **MLX**, or pull from the **`mlx-community`** Hugging Face org by name.

---

## 4. The chat UI & key settings

The GUI is where LM Studio beats a CLI for tuning. With a model loaded, the right-hand panel exposes per-session controls; the load dialog exposes memory-shaping ones (§9).

| Setting | Where | Does |
|---|---|---|
| **Tokens/sec counter** | bottom status bar | Your live speed readout — the fastest way to confirm MLX is actually active (§5) |
| **Temperature / Top-P / Top-K** | chat sidebar | Standard sampling controls |
| **System prompt** | chat sidebar / preset | Per-model persona; saved into a **preset** |
| **Context length** | model load dialog | KV-cache size — **keep ≤ 8192 on 16GB** (§10) |
| **GPU offload** | model load dialog | Layers on GPU; `max` on Apple Silicon (MLX manages this automatically) |
| **Flash Attention / KV-cache quant** | load dialog (experimental) | Frees RAM at long context — test for quality (§10) |
| **Keep model in memory / TTL** | load dialog / `--ttl` | Avoid reload lag between OpenCode calls |
| **Structured Output (JSON Schema)** | chat sidebar / API | Enforce JSON — big win for eval pipelines & agents |
| **Presets** | top of chat | Save a model + params + system prompt combo to reuse |

`lms chat` gives a terminal chat for quick checks; the GUI is better for tuning and watching tok/s.

---

## 5. MLX vs GGUF — the headline decision

This is the whole reason to run LM Studio on your Mac. Two engines, same model weights conceptually, different performance profile:

| | **MLX** (safetensors) | **GGUF** (llama.cpp/Metal) |
|---|---|---|
| Built for | Apple Silicon, unified memory, zero-copy | Cross-platform (the universal standard) |
| Speed (small/mid models that fit) | **~10–30% faster**, snappier TTFT | Solid, broadly tuned |
| Speed (large models filling RAM) | **Tie** — both hit the memory-bandwidth wall | Tie |
| Quant options | mainly 4-bit / 8-bit | granular k-quants (Q4_K_M, Q5_K_M, …) |
| Model availability | `mlx-community` (days after release) | broadest, day-one |
| In your stack | the reason to use LM Studio | what Ollama already gives you |

**Verify MLX is actually running** (it can silently fall back to GGUF):
1. Load the **MLX** build (Apple-logo / MLX badge on the model card).
2. Send a short prompt, watch the **tokens/sec** counter.
3. `lms ps` shows the loaded model's **architecture/runtime**. If speed looks like plain Metal and the badge says GGUF, you loaded the wrong build — reload the MLX variant.

**Honest take for your 16GB M4:** expect a **modest** win on Qwen3.5 9B — more on prompt-processing/TTFT than on generation — **not** dramatic. At 9B you're partway to the memory-bandwidth wall, and your real constraint is **16GB + context** (§10), which a framework swap won't fix. Worth a 30-minute benchmark; keep whichever wins. The genuine unlock is the **Stage-3 48GB** upgrade (opens the 27–35B tier *and* flips on Ollama's MLX too).

---

## 6. Model management (`lms` + GUI)

| Command | Does |
|---|---|
| `lms get <query>` | Search + download from Hugging Face (MLX or GGUF) |
| `lms ls` (`--json`) | List downloaded models + sizes |
| `lms ps` (`--json`) | List **loaded** models: identifier, architecture, size |
| `lms load <key>` | Load a model into memory (flags in §9) |
| `lms load <key> --estimate-only` | **Estimate RAM** before loading — sanity-check fit on 16GB |
| `lms unload <key>` · `lms unload --all` | Free memory |
| `lms import <file>` | Bring an existing **GGUF or MLX** file into LM Studio (`--copy` / `--hard-link` / `--symbolic-link`) |
| `lms status` | Is LM Studio/daemon running, and on which port |
| `lms log stream` | Live view of prompts/responses (debug integrations) |
| `lms runtime` | Manage/update the inference engines |

> `lms load --estimate-only` is your pre-flight check — e.g. it prints estimated GPU/total memory so you don't OOM a 16GB machine.

---

## 7. Picking MLX models for a 16GB Mac

Rough planning: keep **model weights under ~60% of RAM** (leave room for macOS + KV cache + runtime). On 16GB that's **~9–10GB of weights max**, realistically a clean fit at **~7GB**.

| Model (MLX 4-bit unless noted) | ~Size | Fit on 16GB | Best for |
|---|---|---|---|
| **Qwen3.5 9B** ⭐ | ~6–7 GB | ✅ clean | Your primary local model; A/B vs Ollama |
| **Qwen2.5-Coder 7B** | ~5 GB | ✅ | Coding / FIM with OpenCode |
| **Gemma 4 (E4B / 4B)** | ~3–5 GB | ✅ | Efficient small model; tool-calling; second opinion |
| **Llama 3.2 3B / Phi-4-mini** | ~2–3 GB | ✅ | Fast utility/classification alongside a 9B |
| **DeepSeek-R1 distill 7–8B** | ~5 GB | ✅ | Step-by-step reasoning |
| **Qwen3.5 9B 8-bit** | ~9–10 GB | ⚠️ tight | Higher quality; little context headroom on 16GB |
| **27B–35B-A3B / dense** | 16 GB+ | ❌ | Needs **48GB+** (your Stage-3 upgrade) |

> Sub-3B models lose noticeable quality at 4-bit — prefer **8-bit** for those. For 7–9B, 4-bit is the right default on 16GB.

---

## 8. The server & API (how apps connect)

Start the server, then any OpenAI-compatible tool can use it.
```bash
lms server start              # start (uses last/default port 1234); --port / --cors / --host
lms server status             # running? which port?
lms server stop
```
Or GUI: **Developer** tab → toggle **Start Server**.

**OpenAI-compatible** (what OpenCode, AnythingLLM, Continue use):
```
Base URL: http://localhost:1234/v1
Endpoints: /v1/chat/completions · /v1/models · /v1/embeddings
Model:    the loaded model's identifier (see `lms ps` or GET /v1/models)
API key:  any non-empty string (ignored locally)
```
```bash
curl http://localhost:1234/v1/models      # list servable model ids
curl http://localhost:1234/v1/chat/completions -d '{
  "model":"qwen3.5-9b","messages":[{"role":"user","content":"hi"}]
}'
```
- **Native REST:** `GET /api/v0/models`, plus `/api/v0/…` for richer LM-Studio-specific calls.
- **Anthropic-compatible** endpoint also exists (handy for SDKs that speak Anthropic's shape).
- **JIT loading:** if enabled, a request for a model id LM Studio knows about **auto-loads** it — so OpenCode can address a model without you pre-loading it in the GUI.
- **Structured output:** pass a JSON Schema in the request; LM Studio constrains decoding — kills parse/retry loops in eval/agent flows.

**Expose to LAN** (serve the Air from the Mini):
```bash
lms server start --host 0.0.0.0 --port 1234   # or set LMS_SERVER_HOST
```
> ⚠️ Any bind other than `127.0.0.1` exposes the API beyond localhost **with no auth by default**. Trusted networks only, behind a firewall rule.

---

## 9. Configuration (load-time settings)

Most knobs are set **per model at load time** (CLI flags or the GUI load dialog):
```bash
lms load qwen3.5-9b \
  --context-length 8192 \      # KV-cache size — keep ≤ 8192 on 16GB (§10)
  --gpu max \                  # GPU offload: max | off | 0.0–1.0 (MLX auto-manages)
  --ttl 3600 \                 # auto-unload after N seconds idle (0/none = keep resident)
  --identifier qwen3.5-9b      # pin the API model id (what OpenCode points at)
```
| Flag / setting | Does |
|---|---|
| `--context-length <n>` | Context window (RAM grows with it) — **8192 is the safe 16GB ceiling** |
| `--gpu max\|off\|<frac>` | GPU offload fraction; `max` on Apple Silicon |
| `--ttl <seconds>` | Idle auto-unload timer (omit to keep loaded for instant OpenCode responses) |
| `--identifier <name>` | Stable model id for API calls — set this so OpenCode's config key never drifts |
| `--estimate-only` | Print RAM estimate, don't load |
| Server `--port` / `--cors` / `--host` | Server bind/port and CORS (CORS only if a browser app needs it) |
| `LMS_SERVER_HOST` env | Default server bind address |
| Flash Attention / KV-cache quant | Experimental load options to cut long-context RAM (test quality) |

---

## 10. Mac performance tuning (16GB)

- **Context is your hard limit.** On 16GB, **keep context ≤ 8192**; pushing past it forces **swap** and tanks speed. (Long context is what eats a small-RAM Mac, not the model size alone.)
- **Confirm MLX is live** (§5): watch **tokens/sec**; suspiciously low = it loaded GGUF or you're swapping.
- **Estimate before loading:** `lms load --estimate-only <key>` to avoid OOM.
- **Keep weights ≤ ~60% of RAM** (~9–10GB on 16GB) so macOS + KV cache + runtime have room.
- **Avoid reload lag:** skip `--ttl` (or set it long) so the model stays resident between OpenCode calls — trades RAM for instant responses.
- **MLX helps memory a bit:** lazy evaluation trims peak spikes during long context — but it won't lift the 16GB ceiling.
- **Watch Activity Monitor:** yellow memory pressure = mild swap (ok); **red = active swapping = unusable** → unload or shrink context.
- **One heavy model at a time** on 16GB. Running a 9B *and* something else will swap.
- After major **macOS / LM Studio / runtime** updates, restart and re-check tok/s; update the **MLX runtime** (`lms runtime`) for new-model support.

---

## 11. Importing your own GGUF / MLX & reusing identifiers

**Import a file you already have** (e.g. an MLX build pulled manually, or a GGUF shared with your Ollama setup):
```bash
lms import ./Qwen3.5-9B-Instruct-4bit            # MLX folder or .gguf file
lms import ./Qwen3.5-9B-Q4_K_M.gguf --symbolic-link   # don't duplicate the file
```
`--copy` (duplicate), `--hard-link`, or `--symbolic-link` control whether the bytes are copied or linked — **symlink** if you want one copy shared on a tight disk.

**Stable identifiers (presets):** save a model + system prompt + params as a **preset** in the GUI, and pin its API id with `lms load <key> --identifier <name>`. This keeps OpenCode's config key constant even if you re-download or swap quant — the LM Studio analog of an Ollama Modelfile profile.

---

## 12. Integrations (your stack)

**OpenCode** — add LM Studio as a second local provider (drop into `opencode.json`, alongside your `ollama` block):
```json
"lmstudio": {
  "npm": "@ai-sdk/openai-compatible",
  "name": "LM Studio (local)",
  "options": { "baseURL": "http://localhost:1234/v1" },
  "models": {
    "qwen3.5-9b": { "name": "Qwen3.5 9B · MLX (LM Studio)" }
  }
}
```
- The model **key must match** the served identifier — check `lms ps` or `GET /v1/models`, or pin it with `lms load qwen3.5-9b --identifier qwen3.5-9b`.
- Point an agent at it with `"model": "lmstudio/qwen3.5-9b"`, or just pick it via `/models` in the TUI.
- **A/B test:** keep both providers; in OpenCode switch your Plan/learn agent between `ollama/qwen3.5-16k` and `lmstudio/qwen3.5-9b` at the **same context** and compare tok/s. Keep the winner; delete the other block.

**AnythingLLM:** LLM provider → **Generic OpenAI** (or LM Studio) → Base URL `http://localhost:1234/v1`, model = the served id, any API key.

**Python:**
```bash
pip install lmstudio        # native SDK
# or use the OpenAI SDK against base_url="http://localhost:1234/v1"
```
```python
import lmstudio as lms
model = lms.llm("qwen3.5-9b")
print(model.respond("hi"))
```

**LAN serving:** expose the Mini (§8) and point the Air's tools at `http://<mini-ip>:1234/v1`.

---

## 13. CLI quick reference (`lms`)

```bash
lms status                         # is LM Studio running + port
lms get <query>                    # search + download (MLX/GGUF)
lms ls            [--json]         # downloaded models
lms ps            [--json]         # loaded models + identifiers/runtime
lms load <key> --context-length 8192 --gpu max --ttl 3600 --identifier <name>
lms load <key> --estimate-only     # RAM estimate, no load
lms unload <key> | --all           # free memory
lms import <file> [--copy|--hard-link|--symbolic-link]
lms chat                           # terminal chat
lms server start [--port 1234] [--cors] [--host 0.0.0.0]
lms server status | stop
lms log stream                     # live prompt/response logs
lms runtime                        # manage/update inference engines
lms --help | lms <cmd> --help
```

---

## 14. Tips (tailored)

- **Privacy split holds:** LM Studio is on-device too, so finance/proprietary work stays local and free — same role as Ollama, just the MLX engine. Cloud (MiniMax M3 / GLM-5.2 via OpenRouter) stays for public/heavy tasks.
- **Treat this as an experiment, not a migration.** You already have Ollama working at 16k context. The question LM Studio answers is narrow: *does MLX beat GGUF/Metal on my 9B at my context?* Benchmark, then commit to one for OpenCode to avoid maintaining two local engines.
- **Set `--identifier`** so your OpenCode config key is stable across re-downloads.
- **Mind the context ceiling.** Your Ollama planner runs 16k; LM Studio on 16GB is happiest at **≤8192**. If MLX is only fast at 8k but you need 16k for OpenCode's big system prompt, that's a real point **for** staying on Ollama.
- **GUI tuning is the perk:** per-model presets, live tok/s, JSON-schema output, and a one-click MLX/GGUF swap make it a great **benchmarking bench** even if Ollama remains your daily driver.
- **Stage-3 relevance:** when you move to 48GB, LM Studio's MLX + the 27–35B-A3B tier is where local coding models start to feel cloud-class — worth revisiting then.

---

## 15. Troubleshooting

| Symptom | Cause / Fix |
|---|---|
| `lms: command not found` | Run `~/.lmstudio/bin/lms bootstrap`, open a new terminal (PATH refresh) |
| MLX model loads slow / like GGUF | You loaded the GGUF build — reload the **MLX** badge variant; confirm via `lms ps` |
| Very slow / stalls on long prompts | Context too big for 16GB → drop `--context-length` to 8192; check Activity Monitor for red |
| Red memory pressure | Active swapping → unload (`lms unload --all`), shrink context, or use a smaller model |
| OOM on load | `lms load --estimate-only` first; pick 4-bit; close other heavy apps |
| OpenCode can't see the model | Server not started (`lms server start`), or model id mismatch → check `GET /v1/models`, set `--identifier` |
| Port 1234 in use | Another instance/app → `lms server status`, `lms server stop`, or start with `--port` |
| Model won't load after update | Update the engine: `lms runtime`; new architectures need a fresh MLX/llama.cpp runtime |
| MLX models missing from search | You're on an Intel Mac (MLX is Apple-Silicon only) or filtering is set to GGUF |
| Browser app blocked (CORS) | Start server with `--cors` (only if a browser client needs it) |
| Other devices can't connect | Start with `--host 0.0.0.0` (+ firewall); trusted networks only |

---

## 16. Sources
lmstudio.ai/docs (CLI `lms`, `lms server start`, `lms load`, App/Server, MLX) · github.com/lmstudio-ai/lms · deepwiki.com/lmstudio-ai/docs (CLI overview, server control) · markaicode.com "Run MLX Models in LM Studio 2026" · mineraleyt.com "GGUF vs MLX" · insiderllm.com "Best Local LLMs for Mac 2026" · codersera.com "Apple Silicon LLMs 2026". Verify command names, flags, UI labels, and model availability against **lmstudio.ai/docs** and `lms <cmd> --help` for your installed build before relying on them.
