# 01: Docker Introduction

**Course:** Docker for Beginners with Hands-on Labs
**Platform:** Coursera / KodeKloud
**Instructor:** Mumshad Mannambeth (KodeKloud)
**Module:** 1 of 10
**Started:** Oct 2026
**Status:** In Progress

---

## 📚 Overview

Why containers exist, what Docker actually is, and how a container differs from a virtual machine. Installs Docker and runs the first container. The key idea of the whole course starts here: **a container is a normal Linux process that the kernel isolates** — it is not a small VM. Everything later (images, volumes, networks, orchestration) is built on that one fact.

---

## ✅ Progress

- [ ] Video: Introduction
- [ ] Video: Docker Overview
- [ ] Video: Getting started with Docker
- [ ] Demo: Setup and Install Docker
- [ ] Reading: About the Course / Community
- [ ] Assignment: Docker Introduction
- [ ] My practice: `commands/01_practice_introduction.sh`

---

## 🎯 Key Concepts

### The problem Docker solves

**What it is:**
The "works on my machine" problem: an app needs a specific OS libraries, Python version, and dependency versions. Every machine (your Mac, a teammate's laptop, CI, the cloud server) has slightly different ones.

**Why it matters:**
A data pipeline that passes on your Mac and fails in production because of a different `libpq` or Python patch version is a classic incident. Docker ships the app **with** its environment.

**Key points:**
- **Compatibility matrix:** the course's example (web server × database × messaging × OS versions) — each component needs compatible libraries; containers isolate each one
- **Onboarding:** a new developer runs `docker compose up` instead of a 2-day setup doc
- **Same artifact everywhere:** the image you test in CI is byte-for-byte the image you deploy
- **Not magic:** the image must still be built for the right CPU architecture (Module 8)

---

### Containers vs. Virtual Machines

**What it is:**
A **VM** virtualizes hardware and runs a full guest OS with its own kernel on a hypervisor. A **container** shares the host's kernel and isolates only the process, its filesystem view, network, and resources.

**Why it matters:**
Explains why containers start in milliseconds, use MBs instead of GBs, and why you can run dozens on a laptop — and also why a Linux container can't run natively on macOS (no Linux kernel → Docker Desktop runs a small Linux VM).

| | Virtual Machine | Container |
|---|---|---|
| Isolation unit | Whole OS | Process |
| Kernel | Own guest kernel | Shares host kernel |
| Size | GBs | MBs |
| Start time | Minutes | Milliseconds–seconds |
| Isolation strength | Stronger (hardware boundary) | Weaker (shared kernel) |
| Typical use | Different OSes, strong multi-tenant isolation | Packaging and running apps |

**Key points:**
- In the cloud you usually run **containers inside VMs** (ECS on EC2, Fargate micro-VMs) — they complement each other
- **Namespaces** give the process its own view: PID (own PID 1), NET (own network stack), MNT (own filesystem), UTS (own hostname), IPC, USER
- **cgroups** limit what it can use: CPU, memory, I/O (`--memory`, `--cpus` in Module 3)
- Shared kernel = a kernel exploit can escape a container → why we run as non-root (Module 4/11)

---

### Docker vocabulary: image, container, registry

**What it is:**
- **Image** — a read-only template: filesystem layers + metadata (default command, env vars, user)
- **Container** — a running (or stopped) instance of an image, plus a thin writable layer
- **Registry** — where images are stored and shared (Docker Hub, GHCR, AWS ECR)

**Why it matters:**
The same relationship as **class → object** in Python: one image, many containers. Mixing the two words up is the most common beginner error in interviews.

**Key points:**
- `docker run nginx` = pull image (if missing) → create container → start it
- Deleting a container never deletes its image; deleting an image needs all its containers removed first
- Images are identified by **tag** (moveable label, `python:3.14-slim`) and **digest** (immutable hash, `sha256:...`)

---

### Docker architecture (preview of Module 6)

**What it is:**
`docker` (the CLI) is only a client. It sends REST API calls to the **Docker daemon** (`dockerd`), which uses **containerd** to manage containers and **runc** to actually create the isolated process.

**Why it matters:**
When `docker ps` says "Cannot connect to the Docker daemon", the CLI is fine — the engine isn't running. It also explains how CI, Airflow or any script can drive Docker: they call the same API the CLI does.

```
docker CLI ──REST──▶ dockerd ──▶ containerd ──▶ runc ──▶ your process (namespaces + cgroups)
```

---

### Docker editions and installing

**What it is:**
**Docker Engine** (Linux, free, open source) vs **Docker Desktop** (Mac/Windows/Linux GUI app that bundles a Linux VM, Engine, Compose, Buildx, Scout).

**Key points:**
- On a Mac, Docker Desktop runs a lightweight Linux VM — `docker info` shows `aarch64` on Apple Silicon
- Docker Desktop is free for personal use, education, and small businesses; larger companies need a paid plan (check your future employer's policy)
- Alternatives on a Mac: **OrbStack**, **Colima**, Rancher Desktop, Podman Desktop — same `docker` CLI
- `docker version` must show both **Client** and **Server** blocks

---

## 💻 Code Examples

### Client ↔ daemon
```bash
docker version                     # Client AND Server blocks
docker info --format 'arch={{.Architecture}} driver={{.Driver}} cgroup=v{{.CgroupVersion}}'
```

### A container is a process on the host's kernel
```bash
docker run --rm alpine:3.22 sh -c 'echo "PID 1 is: $(cat /proc/1/comm)"'   # PID 1 is: sh
docker run --rm alpine:3.22 uname -r
uname -r   # Linux host: same kernel. Mac: different — the container sees Docker Desktop's VM kernel
```

### Evidence you're inside a container
```bash
docker run --rm alpine:3.22 sh -c 'ls -la /.dockerenv; cat /proc/1/cgroup'
docker run --rm alpine:3.22 ps          # only the container's own processes
```

### A cgroup limit is just a file
```bash
docker run --rm --memory 64m alpine:3.22 cat /sys/fs/cgroup/memory.max   # 67108864
```

All of these (8 sections) are in `commands/01_practice_introduction.sh`.

---

## 📖 Important Terms

| Term | Definition | Example |
|------|------------|---------|
| **Container** | Isolated process with its own filesystem/network view | `docker run nginx` |
| **Image** | Read-only template a container starts from | `python:3.14-slim` |
| **Registry** | Server that stores images | Docker Hub, `ghcr.io` |
| **Docker Engine** | Daemon + API + runtime | `dockerd` |
| **Docker Desktop** | Mac/Windows app bundling a Linux VM + Engine | — |
| **Namespace** | Kernel feature that isolates what a process can *see* | PID, NET, MNT |
| **cgroup** | Kernel feature that limits what a process can *use* | `--memory 512m` |
| **Hypervisor** | Software running VMs | VirtualBox, Apple Virtualization |
| **OCI** | Open Container Initiative — standard image/runtime format | Docker images run on Kubernetes, ECS, Podman |
| **Tag vs digest** | Moveable name vs immutable content hash | `:3.14-slim` vs `@sha256:...` |

---

## 🔧 Labs

**Course: Assignment — Docker Introduction**
- **Task:** Concept quiz on containers vs VMs and Docker basics
- **Tip (from learner reviews):** answers can be strict on exact wording/spaces — read each question twice

**My practice: `commands/01_practice_introduction.sh`**
- **Task:** Prove client ↔ daemon, run hello-world, look at a container from the inside
- **Concepts:** Client/server, namespaces, shared kernel, cgroups preview, image vs container
- **Approach:** 8 sections, one block at a time

---

## 🚀 Beyond the Course (what my roadmap needs that this module skips)

- **OCI standard** — the reason a Docker-built image runs unchanged on ECS Fargate, Kubernetes and Podman. Kubernetes removed "dockershim" in 1.24 (2022); Docker *images* still work everywhere because they are OCI images
- **Containers inside VMs** — in production you'll almost always see both (ECS on EC2, Fargate). Interview line: "VMs isolate machines, containers package apps"
- **Security posture starts here** — shared kernel ⇒ least privilege matters: non-root user, read-only filesystem, no secrets in images (Modules 4, 6, 11)

---

## 💡 Key Takeaways

1. **A container is a process, not a mini-VM** — namespaces isolate it, cgroups limit it, the kernel is shared
2. **Image : container = class : object** — one template, many instances
3. **The CLI is just a client** — "can't connect to daemon" means the engine isn't running
4. **On a Mac, there's always a Linux VM underneath** — that's why architecture (arm64 vs amd64) matters later
5. **Same image from CI to production** is the whole point — reproducibility over convenience

---

## 🔗 Resources

- [Coursera — Docker for Beginners with Hands-on Labs](https://www.coursera.org/learn/docker-for-the-absolute-beginner)
- [Docker docs — Get started](https://docs.docker.com/get-started/)
- [Docker docs — Docker Desktop](https://docs.docker.com/desktop/)
- [Open Container Initiative](https://opencontainers.org/)
- [Vu Trinh — Docker for data engineers (reproducibility + isolation as the core value)](https://vutr.substack.com/p/docker-for-data-engineer)

---

## 📝 My Notes

**What clicked:**
- A container is just a Linux process with a restricted view — `ps` inside shows only PID 1, so "lightweight VM" is the wrong mental model
- On my Mac there is always a Linux VM underneath: `uname -r` in a container shows the VM's kernel, not Darwin
- `docker` is only a REST client — "Cannot connect to the Docker daemon" means the engine is off, not that the CLI is broken
- Image : container = class : object — one read-only template, many instances, each with its own writable layer

**Challenges:**
- Unlearning the VM picture: isolation comes from kernel features (namespaces, cgroups), not a hypervisor — which is also why it's weaker isolation
- Keeping the vocabulary exact under quiz pressure: image vs container vs registry, tag vs digest
- Seeing that CPU architecture already matters here (an aarch64 VM on Apple Silicon) before Module 8 explains why

**Aha moments:**
-

**To review:**
-

**Common mistakes:**
- Calling a container a "lightweight VM" (it isn't — no own kernel)
- Thinking `docker` CLI errors mean Docker is broken (usually the daemon isn't started)

**Roadmap connection:**
- Every flagship ships a Dockerfile (README production standard) — this module is the "why"
- DataVault S2 gate: "deploy (Docker/ECS)" — ECS runs OCI images, which is what Docker builds
- Python's `os.getpid()` / `/proc` connect back to CS50 Week 4 (memory, processes)

---

## ➡️ Next Steps

**Next module:** 02_docker_commands.md (container and image lifecycle)
**To practice:**
- Run `commands/01_practice_introduction.sh` block by block
- Write in your own words: 3 differences between a VM and a container
- Run `docker info` and record your Architecture, Storage Driver, and Cgroup Version
