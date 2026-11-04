# Docker for Beginners with Hands-on Labs

## Course Information

- **Platform:** Coursera (Coursera Plus) — produced by KodeKloud
- **Instructor:** Mumshad Mannambeth (KodeKloud)
- **Duration:** 10 modules (~10 hours, ~1 week at 10 hrs/week)
- **Skills:** Containers, `docker run`, Dockerfile, ENV / CMD / ENTRYPOINT, Docker Compose, volumes, networking, registries, Swarm & Kubernetes intro, YAML
- **Roadmap row:** Stage 1 Core Course 1️⃣2️⃣ — feeds the Dockerfile in every flagship and the DataVault S2 gate (Docker → ECS)

## Progress

- [x] 01: Docker Introduction
- [x] 02: Docker Commands
- [x] 03: Docker Run
- [x] 04: Docker Images (ENV, CMD vs ENTRYPOINT)
- [x] 05: Docker Compose
- [x] 06: Docker Engine and Storage
- [ ] 07: Docker Networking and Registry
- [ ] 08: Docker on Mac & Windows
- [ ] 09: Container Orchestration — Docker Swarm & Kubernetes
- [ ] 10: Course Conclusion and YAML Basics
- [ ] 11: 🚀 Beyond the Course — Production Docker for the roadmap (self-study)



## Structure

```
docker_kodekloud/
├── notes/
│   ├── 01_docker_introduction.md
│   ├── 02_docker_commands.md
│   ├── 03_docker_run.md
│   ├── 04_docker_images.md
│   ├── 05_docker_compose.md
│   ├── 06_engine_and_storage.md
│   ├── 07_networking_and_registry.md
│   ├── 08_docker_on_mac_windows.md
│   ├── 09_container_orchestration.md
│   ├── 10_yaml_and_conclusion.md
│   └── 11_beyond_the_course.md
├── commands/
│   ├── 01_practice_introduction.sh
│   ├── 02_practice_commands.sh
│   ├── 03_practice_run.sh
│   ├── 04_practice_images.sh
│   ├── 05_practice_compose.sh
│   ├── 06_practice_engine_storage.sh
│   ├── 07_practice_networking_registry.sh
│   ├── 08_practice_mac_windows.sh
│   ├── 09_practice_orchestration.sh
│   ├── 10_practice_yaml.sh
│   └── 11_practice_beyond.sh
└── lab_files/
    ├── dist_loader/      # the ONE Python project — Python ↔ Docker bridge (Modules 4, 5, 8, 11)
    ├── data/             # synthetic 1099-R CSVs (good + bad)
    ├── site/ site_alt/   # static pages for nginx (Modules 3, 11)
    ├── sleeper/          # CMD vs ENTRYPOINT + shell vs exec Dockerfiles (Module 4)
    ├── compose/          # Postgres + loader + report stack, voting app (Module 5)
    ├── orchestration/    # swarm/, kubernetes/, ecs/ (Module 9)
    ├── yaml/             # YAML lab file (Module 10)
    └── ci/               # CI workflow, hadolint config, dev-loop compose, Makefile (Module 11)
```



## Notes

Each module has a dedicated notes file in `/notes` following the format `XX_topic.md`, using the same template as CS50 and Python for Everybody, plus a **🚀 Beyond the Course** section with what the roadmap needs that the module skips.

- **01–03** — containers vs VMs, lifecycle commands, every `docker run` flag
- **04–05** — Dockerfiles (uv multi-stage, non-root), Compose with healthchecks and secrets
- **06–08** — engine internals, storage, networking, registries, multi-platform builds
- **09–10** — Swarm, Kubernetes and ECS concepts; YAML
- **11** — production checklist: lint, scan, secrets, hardened runs, SHA-pinned CI



## Command Files

One practice file per module in `/commands`, in the same style as the Mode SQL `queries/` files: header, table of contents, numbered sections with a `Signature:` line, then `1a / 1b` exercises.

- Run from `courses/docker_kodekloud/`, **one block at a time** (VS Code: select → *Terminal: Run Selected Text in Active Terminal*) — never the whole file; some commands fail on purpose and are marked `EXPECTED`
- Stock images only (alpine, nginx, postgres, python), pinned tags, synthetic data only
- `lab_files/` holds the non-command artifacts the commands need (Dockerfiles, Compose files, manifests, YAML)



## Python in this course

Only one Python project, kept because it *is* the roadmap's Python ↔ Docker skill: `lab_files/dist_loader` (validate + load a synthetic 1099-R CSV into Postgres). It's what Module 4 containerizes with the flagship Dockerfile standard (`uv sync --frozen` → `--locked`, multi-stage, non-root) and what Module 5 runs as the Compose `loader` service. Everything else is plain `docker` commands.

## Certificate

[Add certificate link when completed]