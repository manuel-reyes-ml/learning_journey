# 03: Docker Run

**Course:** Docker for Beginners with Hands-on Labs
**Platform:** Coursera / KodeKloud
**Instructor:** Mumshad Mannambeth (KodeKloud)
**Module:** 3 of 10
**Started:** Oct 2026
**Status:** In Progress

---

## 📚 Overview

`docker run` in depth: picking versions with **tags**, interactive programs with **`-i`/`-t`**, reaching services with **port mapping**, keeping data with **volume mapping**, and reading a container's state with **`inspect`** and **`logs`**. Also environment variables (`-e`) used for configuration — the 12-Factor idea your roadmap's logging/config rules build on.

---

## ✅ Progress

- [ ] Video: Docker Run
- [ ] Demo: Advanced Docker Run Features
- [ ] Hands-on Lab: Docker Run Commands
- [ ] Assignment: Docker Run
- [ ] My practice: `commands/03_practice_run.sh`

---

## 🎯 Key Concepts

### Tags

**What it is:**
The part after `:` in `python:3.14-slim` — a human label pointing at one image version.

**Why it matters:**
`python` with no tag means `python:latest`, which moves whenever the maintainers push. Your build silently changes. Your roadmap pins Python 3.14 in one place (`requires-python`) and the Dockerfile base image must agree.

**Key points:**
- `3.14` vs `3.14-slim` vs `3.14-alpine`: full (~1 GB, has compilers) · slim (Debian minimal, best default for Python) · alpine (musl libc — many Python wheels don't fit, slower builds)
- Tags are **mutable**; digests (`@sha256:...`) are **immutable** — production pins can use both: `python:3.14-slim@sha256:...`

---

### STDIN and TTY: `-i` and `-t`

**What it is:**
`-i` keeps STDIN open (you can send input). `-t` allocates a pseudo-terminal (prompts, colors, line editing). Interactive programs need both: `-it`.

**Key points:**
- No `-i` → a program reading stdin (`read`, Python's `input()`) gets EOF immediately
- `-i` only → piping works: `echo AAPL | docker run -i ...`
- `-it` → behaves like your local terminal
- Never use `-t` in CI/cron (no terminal) — use `-i` for pipes or nothing

---

### Port mapping: `-p HOST:CONTAINER`

**What it is:**
Publishes a container port on the host. `-p 8080:8000` = host port 8080 → container port 8000.

**Why it matters:**
Every container has its own network namespace; without `-p`, the host can't reach it.

**Key points:**
- Many containers can listen on 8000 **inside**; each needs a **different host port**
- The app must bind **`0.0.0.0`** inside the container — `127.0.0.1` means "only from inside this container"
- `-p 127.0.0.1:8080:8000` publishes only to your machine, not your whole Wi-Fi network (safer default for databases)

---

### Volume mapping: `-v HOST_PATH:CONTAINER_PATH`

**What it is:**
Mounts a host directory (or a Docker volume) into the container.

**Why it matters:**
A container's own filesystem disappears with the container. Databases, input files and outputs must live on a mount (Module 6 goes deep).

**Key points:**
- `-v "$PWD/data":/data:ro` — `:ro` = read-only; use it for inputs
- Swap data without rebuilding: same image, different `-v` (Exercise 4)
- `-v mysql-data:/var/lib/mysql` (course) — a named volume (Docker-managed)

---

### Environment variables: `-e`

**What it is:**
Key/value configuration passed at start: `-e PLAN_ENV=staging`.

**Why it matters:**
12-Factor app rule: config that differs between environments lives in the environment, not the code. The course example is `APP_COLOR=blue`; yours is `PLAN_ENV`, `LOG_LEVEL`, `PORT`.

**Key points:**
- `--env-file .env` loads many at once (roadmap Makefile `docker-run` target)
- Check them: `docker exec NAME env` or `docker inspect --format '{{json .Config.Env}}'`
- ⚠️ **Not for secrets in production** — env vars show up in `inspect`, crash dumps and child processes; use secret files (Module 5) or a secrets manager (ECS)

---

### Inspect and logs

**Key points:**
- **`docker inspect NAME`** — full JSON: mounts, env, network IPs, restart policy, health
- `--format '{{...}}'` (Go templates) pulls one field; pipe JSON to `python3 -m json.tool`
- **`docker logs NAME`** — stdout/stderr of the main process; `-f` follow, `--tail N`, `--since 5m`
- Logs only exist if the app writes to **stdout/stderr** — writing to `logs/app.log` inside the container hides them (and your roadmap's CORRECTION 16 says: stdout only)

---

### Graceful shutdown (not in the course, but every service needs it)

`docker stop` sends the image's **StopSignal** (default SIGTERM) to PID 1, waits 10 s, then sends SIGKILL — open DB transactions get cut.

**Key points:**
- **PID 1 ignores signals it has no handler for** — `docker run alpine sleep 600` → `docker stop` always takes the full 10 s and exits **137**
- **`--init`** puts a tiny init (tini) at PID 1 that forwards signals → the same command stops at once (exit **143**)
- Well-behaved images declare and handle their signal: `docker inspect nginx:1.29-alpine --format '{{.Config.StopSignal}}'` → `SIGQUIT`
- Your own Python services must install a SIGTERM handler (`signal.signal(signal.SIGTERM, ...)`) or run behind `--init`

---

## 💻 Code Examples

### Port + bind mount, no image build needed
```bash
docker run -d --name web1 -p 8080:80 \
  -v "$PWD/lab_files/site":/usr/share/nginx/html:ro nginx:1.29-alpine
curl -s localhost:8080 | grep '<h1>'
```

### Same image, different mount → different content
```bash
docker run -d --name web2 -p 8081:80 \
  -v "$PWD/lab_files/site_alt":/usr/share/nginx/html:ro nginx:1.29-alpine
```

### Env var config (the course's lab image)
```bash
docker run -d --name blue-app -e APP_COLOR=blue -p 38282:8080 kodekloud/simple-webapp
docker exec blue-app env | grep APP_COLOR
```

### Stop timing with and without an init
```bash
docker run -d --name sleepy alpine:3.22 sleep 600 && time docker stop sleepy             # ~10 s, exit 137
docker run -d --init --name sleepy-init alpine:3.22 sleep 600 && time docker stop sleepy-init   # <1 s, exit 143
```

### Limits and OOM
```bash
docker run --rm --memory 32m python:3.14-slim python -c "x = bytearray(200 * 1024 * 1024)"
echo $?     # 137 — OOM-killed
```

---

## 📖 Important Terms

| Term | Definition | Example |
|------|------------|---------|
| **Tag** | Mutable version label | `redis:8-alpine` |
| **Digest** | Immutable content hash | `@sha256:4f...` |
| **`-d`** | Detached (background) | `docker run -d nginx` |
| **`-it`** | Interactive + TTY | `docker run -it ubuntu bash` |
| **`-p`** | Publish port HOST:CONTAINER | `-p 8080:80` |
| **`-v`** | Mount volume/dir | `-v "$PWD/data":/data:ro` |
| **`-e` / `--env-file`** | Env vars | `-e LOG_LEVEL=DEBUG` |
| **`-w`** | Working directory inside container | `-w /app` |
| **`--name`** | Fixed container name | `--name plan-status` |
| **`--restart`** | Restart policy | `--restart on-failure:3` |
| **`inspect`** | Full JSON state | `docker inspect web` |
| **SIGTERM** | Polite stop signal | sent by `docker stop` |

---

## 🔧 Labs

**Course: Hands-on Lab — Docker Run Commands**
- **Task:** Run specific tags, interactive containers, map ports, mount volumes, read `inspect`
- **Concepts:** All flags above
- **Approach:** For port questions, remember order: **HOST first, CONTAINER second**

**My practice: `commands/03_practice_run.sh`** — 11 sections on stock images (nginx, alpine, postgres, the course's `kodekloud/simple-webapp`):
tags · `-i`/`-t` · port clash · content swap via `-v` · `:ro` · env vars + `--env-file` · inspect · logs · stop timing with and without `--init` · restart policy · memory/CPU limits and OOM

---

## 🚀 Beyond the Course

- **Bind `0.0.0.0`, publish `127.0.0.1`** — app listens on all interfaces *inside*; host publishes only locally. Postgres on `-p 5432:5432` without `127.0.0.1` is exposed to your LAN
- **`--restart` policies** — `no` · `on-failure[:N]` · `unless-stopped` · `always`. One-shot ETL jobs: `no`; long-running services: `unless-stopped` (used in Module 5)
- **Resource limits** — `--memory 512m --cpus 1` mirror ECS task CPU/memory; exit code 137 = hit the memory limit
- **Signal handling** — every long-running Python service you ship should handle SIGTERM (Airflow, ECS and Kubernetes all stop containers this way)
- **`--init`** — a one-flag fix for apps that can't handle signals as PID 1 (Compose: `init: true`; ECS: `initProcessEnabled`)
- **Inspect field changes** — current Engine API removed the old top-level `.NetworkSettings.IPAddress`; read `{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}`

---

## 💡 Key Takeaways

1. **Pin tags** — `latest` is a moving target
2. **`-p HOST:CONTAINER`**, app binds `0.0.0.0` inside
3. **Data on mounts, not in the container layer**
4. **Config via env vars, secrets via files** (Module 5)
5. **Logs go to stdout** — or `docker logs` shows nothing
6. **Handle SIGTERM** — or every stop is a 10-second hard kill

---

## 🔗 Resources

- [Docker docs — `docker container run` reference](https://docs.docker.com/reference/cli/docker/container/run/)
- [The Twelve-Factor App — Config](https://12factor.net/config) and [Logs](https://12factor.net/logs)
- [Python docs — `signal` module](https://docs.python.org/3/library/signal.html)
- [Python Docker Official Image (tags explained)](https://hub.docker.com/_/python)

---

## 📝 My Notes

**What clicked:**
- `-p HOST:CONTAINER` — host first. Many containers can all listen on port 80 inside; only the host ports must differ
- The same image with a different `-v` mount serves different content with no rebuild — that's how data and config stay out of images
- PID 1 ignores signals it has no handler for: `sleep` as PID 1 takes the full 10 s to stop, and `--init` fixes it
- Exit code 137 under a memory limit means the kernel OOM-killed the process — the same number ECS reports when a task runs out of memory

**Challenges:**
- `-it` vs `-i`: piping needs only `-i`, and `-t` breaks in CI where there is no terminal
- Reading `inspect` output with Go templates — IPs now live per network, not at the top level
- Knowing what NOT to pass with `-e`: config yes, secrets no (they show up in `docker inspect`)

**Aha moments:**
-

**To review:**
-

**Common mistakes:**
- Reversing `-p` order (`-p 8000:8080` when the app listens on 8000)
- App bound to `127.0.0.1` inside the container → "connection reset" from the host
- Logging to a file inside the container, then wondering why `docker logs` is empty

**Roadmap connection:**
- CORRECTION 16 (stdout-only logging, Docker owns rotation) — this module is where it becomes visible
- `pydantic-settings` (Stage 1 course row) reads the same env vars, typed
- ECS task definitions are `docker run` flags written as JSON (Module 9 `ecs/`)

---

## ➡️ Next Steps

**Next module:** 04_docker_images.md (Dockerfile, layers, ENV, CMD vs ENTRYPOINT)
**To practice:**
- Run all 11 sections; record `time docker stop` for `sleepy` vs `sleepy-init`
- Find the `StopSignal` of three images you use (nginx, postgres, python) with `docker inspect`
