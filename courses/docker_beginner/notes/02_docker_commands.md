# 02: Docker Commands

**Course:** Docker for Beginners with Hands-on Labs
**Platform:** Coursera / KodeKloud
**Instructor:** Mumshad Mannambeth (KodeKloud)
**Module:** 2 of 10
**Started:** Oct 2026
**Status:** In Progress

---

## 📚 Overview

The everyday commands for the **container lifecycle** (run → list → exec → stop → remove) and the **image lifecycle** (pull → list → remove). The big lesson: a container only lives as long as its main process — which explains why `docker run ubuntu` "does nothing" and exits immediately.

---

## ✅ Progress

- [ ] Video: Basic Docker Commands
- [ ] Demo: Docker Commands
- [ ] Hands-on Lab: Basic Docker Commands
- [ ] Assignment: Docker Commands
- [ ] My practice: `commands/02_practice_commands.sh`

---

## 🎯 Key Concepts

### Container lifecycle

**What it is:**
The states a container moves through: **created → running → (paused) → exited → removed**.

**Why it matters:**
Debugging starts with "what state is it in and why?" — `docker ps -a` + the exit code answers most questions.

```
docker create ──▶ created ──docker start──▶ running ──process ends / docker stop──▶ exited ──docker rm──▶ gone
            docker run = create + start
```

**Key points:**
- **`docker run IMAGE`** — pull if missing, create, start, attach to output
- **`docker ps`** — running only; **`docker ps -a`** — all, including exited
- **`docker stop`** — sends **SIGTERM**, waits 10 s, then **SIGKILL** (graceful)
- **`docker kill`** — SIGKILL immediately (no cleanup)
- **`docker rm`** — delete a stopped container; **`docker rm -f`** — stop + delete
- **Exit codes:** `0` normal · `1` app error · `137` killed (SIGKILL / out of memory) · `143` SIGTERM

---

### A container lives as long as its main process

**What it is:**
Every container has exactly one main process (PID 1). When it exits, the container exits.

**Why it matters:**
`docker run ubuntu` exits instantly because Ubuntu's default command is `bash`, and with no terminal attached bash has nothing to do. It's not broken. Batch jobs (your loaders, dbt runs) are *supposed* to exit — with code 0.

**Key points:**
- Give it work: `docker run ubuntu sleep 300`
- Web servers/databases run forever by design; ETL jobs run and exit
- Orchestrators (Compose, ECS, Airflow's DockerOperator) read the **exit code** to decide what happens next

---

### Running commands inside a container

**What it is:**
**`docker exec`** starts an *extra* process in an already-running container. **`docker attach`** connects your terminal to the *main* process.

**Key points:**
- `docker exec -it NAME bash` (or `sh` on slim/alpine images) — debugging shell
- `docker exec NAME cat /etc/os-release` — one-off command
- `attach`: Ctrl-C sends SIGINT to PID 1 (can stop the container!) — detach with **Ctrl-P Ctrl-Q**
- **`docker logs`** is usually what you want instead of attach — it reads captured stdout/stderr without risk

---

### Image commands

**Key points:**
- **`docker images`** / `docker image ls` — local images, tags, sizes
- **`docker pull IMAGE:TAG`** — download without running (pre-warm CI or demos)
- **`docker rmi IMAGE`** — fails if any container (even exited) uses it → `docker rm` first
- **`docker image prune`** — remove dangling (untagged) images; **`docker system df`** — disk usage
- No tag = `:latest` — which only means "the tag nobody named", not "newest"

---

### Long form vs short form

Docker reorganized commands into management groups. Both work; docs and CI logs increasingly use the long form.

| Short (course) | Long (modern docs) |
|---|---|
| `docker ps` | `docker container ls` |
| `docker rm` | `docker container rm` |
| `docker images` | `docker image ls` |
| `docker rmi` | `docker image rm` |
| `docker inspect` | `docker container inspect` / `docker image inspect` |

---

## 💻 Code Examples

### Format output for scripts
```bash
docker ps -a --format 'table {{.Names}}\t{{.Image}}\t{{.Status}}'
docker ps -q                       # IDs only — feed into other commands
docker rm -f $(docker ps -aq --filter name=lab-)   # remove only lab containers
```

### Inventory without writing code
```bash
docker ps -a --filter status=exited --format 'table {{.Names}}\t{{.Status}}'
docker ps -a --filter ancestor=ubuntu:24.04 --format '{{.Names}}'
docker ps -a --format '{{json .}}' | head -2          # one JSON object per container
docker inspect web --format 'exit={{.State.ExitCode}}'
```

---

## 📖 Important Terms

| Term | Definition | Example |
|------|------------|---------|
| **`run`** | Create + start a container | `docker run -d nginx` |
| **`ps` / `ps -a`** | List running / all containers | `docker ps -a` |
| **`stop`** | SIGTERM, then SIGKILL after 10 s | `docker stop web` |
| **`kill`** | SIGKILL immediately | `docker kill web` |
| **`rm` / `rmi`** | Remove container / image | `docker rmi redis` |
| **`exec`** | Run an extra process in a running container | `docker exec -it web sh` |
| **`attach`** | Connect to the main process's I/O | detach: Ctrl-P Ctrl-Q |
| **`logs`** | Read captured stdout/stderr | `docker logs -f --tail 50 web` |
| **`prune`** | Bulk-delete unused objects | `docker system prune` |
| **Exit code 137** | Killed by SIGKILL (often OOM) | memory limit too low |
| **Dangling image** | Image layer with no tag | `<none>:<none>` |

---

## 🔧 Labs

**Course: Hands-on Lab — Basic Docker Commands**
- **Task:** Count running containers/images, run/stop/remove containers, pull images, find image tags
- **Concepts:** Lifecycle, `ps` vs `ps -a`, `rmi` dependencies
- **Approach:** Read the question carefully; most answers come from `docker ps -a` or `docker images`

**My practice: `commands/02_practice_commands.sh`** — 11 sections: lifecycle, exec vs attach, logs, stop vs kill with exit codes (0 / 1 / 137), create/pause/unpause, the `rmi` failure case, filters and `--format`

---

## 🚀 Beyond the Course

- **The CLI is scriptable** — `--filter` + `--format '{{json .}}'` cover most inventory and automation needs; Airflow's `DockerOperator` and other tools call the same Engine API when you need code
- **Exit codes as a contract** — design your CLIs to return `0/1/2` meaningfully (see `dist-loader` in Module 4); CI, Compose and ECS act on them
- **`docker system prune` habit** — Docker Desktop's VM disk fills up silently; run `docker system df` weekly

---

## 💡 Key Takeaways

1. **One main process per container** — when it exits, the container exits
2. **`stop` is polite, `kill` is not** — and apps must handle SIGTERM to be polite back (Module 3)
3. **`logs` over `attach`** for watching output
4. **Images can't be removed while any container uses them** — even stopped ones
5. **`--filter` + `--format` make the CLI scriptable** — no SDK needed for most tasks

---

## 🔗 Resources

- [Docker CLI reference](https://docs.docker.com/reference/cli/docker/)
- [Docker docs — Format command and log output](https://docs.docker.com/engine/cli/formatting/)
- [KDnuggets — 10 essential Docker commands for data engineering](https://www.kdnuggets.com/10-essential-docker-commands-for-data-engineering)

---

## 📝 My Notes

**What clicked:**
- A container lives exactly as long as its main process — `docker run ubuntu` exiting at once isn't a failure, bash just had nothing to do
- Exit codes are the contract: 0 ok · 1 app error · 137 = 128+9 (SIGKILL or out of memory) · 143 = 128+15 (SIGTERM)
- `exec` starts an extra process next to PID 1; `attach` connects to PID 1 itself — `logs` is the safe way to watch output
- `--filter` + `--format` (Go templates) make the CLI scriptable without any SDK

**Challenges:**
- Remembering that `docker rmi` fails while even an *exited* container still references the image
- Ctrl-C inside `docker attach` stops the container — detaching is Ctrl-P Ctrl-Q
- Go template syntax for `--format` (`{{.State.ExitCode}}`, `{{json .}}`) takes practice to read and write

**Aha moments:**
-

**To review:**
-

**Common mistakes:**
- `docker run ubuntu` and thinking it failed (it finished)
- Ctrl-C inside `docker attach` and stopping the container by accident
- Expecting `docker rmi` to work while an exited container still references the image

**Roadmap connection:**
- Exit codes → DataVault orchestration (Airflow task success/failure) and CI gates
- `--format '{{json .}}'` output is easy to parse with jq or Python in ops scripts and CI checks

---

## ➡️ Next Steps

**Next module:** 03_docker_run.md (tags, -it, ports, volumes, env vars, inspect, logs)
**To practice:**
- Run every section of `commands/02_practice_commands.sh`
- Write a one-liner that removes only the exited containers of one image (`--filter ancestor=` + `xargs docker rm`)
