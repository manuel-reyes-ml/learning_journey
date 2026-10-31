# =============================================================================
# Dockerfile — recon-toy (lives in foundations/, built from the REPO ROOT)
# =============================================================================
#
# BUILD:  docker build -f foundations/Dockerfile -t recon-toy .
#   -f foundations/Dockerfile  → which Dockerfile to read.
#   -t recon-toy               → the image name (tag) to save the result as.
#   .                          → the BUILD CONTEXT: the folder whose files the build may
#                                COPY. Every COPY path below is relative to it — the repo
#                                root — not to this file's folder. It has to be the root
#                                because uv.lock and the workspace pyproject.toml live there.
#
# RUN:    docker run --rm recon-toy                  → default args (CMD: --help)
#         docker run --rm recon-toy <args...>        → <args> replace CMD
#   --rm  deletes the stopped container afterwards (the image stays).
#
#   Keep the results — mount something at /data, the only writable folder:
#     docker run --rm -v recon-data:/data recon-toy --participants 50
#       NAMED VOLUME: Docker-managed storage that outlives the container. On first use,
#       Docker copies the image's /data (outputs/, owned by "app") into the empty volume,
#       so "app" can write to it. List with `docker volume ls`.
#     docker run --rm -v "$PWD/data_test_recontoy:/data" recon-toy --participants 50
#       BIND MOUNT: a host folder ($PWD = the folder your terminal is in; run from the
#       repo root). Files appear on your machine. Nothing is copied in from the image.
#       Docker Desktop's file sharing handles ownership, which is why this works on a Mac;
#       on a Linux host the folder must be writable by the container user's UID
#       (e.g. add --user "$(id -u):$(id -g)").
#
# HOW A BUILD WORKS
#   RUN, COPY and ADD each produce a LAYER: a read-only snapshot of the files they
#   changed. FROM picks the starting layers; ENV, WORKDIR, USER, ENTRYPOINT and CMD only
#   record settings (metadata). The image is the stack of layers plus that metadata.
#   Docker caches every step and reuses it on the next build if the instruction AND its
#   inputs (the copied files) are unchanged. Once one step changes, every LATER step is
#   rebuilt.
#   → So the order is: things that rarely change (Python, uv, dependencies) first,
#     things that change often (your source code) last.
#
# WHERE THE PACKAGES COME FROM
#   Nothing is copied from your machine's .venv. The `RUN uv sync` steps CREATE
#   /app/.venv inside the image, so the installed packages are part of the image layers.
#   Anyone who pulls this image gets them with it. uv is needed only to BUILD;
#   at runtime the container calls python directly (see ENTRYPOINT).
#
# CODE vs STATE
#   /app  = code + venv, owned by root → read-only for the "app" user at runtime.
#   /data = runtime state (CSVs, recon.db, outputs/), owned by "app" → the only writable
#           folder. paths.py finds it through LJ_DATA_DIR / LJ_OUTPUT_DIR (set below).
#
# Single-stage for now (roadmap: multi-stage is a Stage-2 optimisation). A second stage
# would copy only /app/.venv + the source into a fresh python:3.14-slim, leaving uv
# behind (the source too, because the project is installed editable — see layer 2).
# =============================================================================

# FROM: the base image this one starts from. python:3.14-slim = Debian "slim" (minimal
# OS packages) + CPython 3.14 installed at /usr/local/bin. Every image starts with FROM.
# `AS base` names this stage so a later stage could refer to it (COPY --from=base ...).
# Nothing uses that name yet; it is ready for the multi-stage version.
FROM python:3.14-slim AS base

# COPY --from=<image>: copy files out of ANOTHER image instead of the build context.
# Docker pulls Astral's uv image and takes only the two static binaries (uv, uvx) into
# /bin/ — no installer script, no curl, no extra OS packages.
# Pinned to an exact version (never :latest) so every build uses the same uv; keep it in
# step with [tool.uv] required-version (>=0.13) and the uv version CI runs.
COPY --from=ghcr.io/astral-sh/uv:0.13.6 /uv /uvx /bin/

# ENV: sets environment variables for every later build step AND for running containers.
#   UV_COMPILE_BYTECODE=1  → compile .py → .pyc for the packages installed in .venv
#                            during the build, so containers don't recompile them on every
#                            start. Not your own code: lj-foundations is installed
#                            editable (it stays in foundations/src), so its modules are
#                            compiled in memory at each start — "app" can't write
#                            __pycache__ there, and Python silently skips it.
#   UV_LINK_MODE=copy      → uv normally hard-links files from its cache; the cache mount
#                            below is a separate filesystem where that fails, so copy
#                            instead and silence the warning.
#   UV_PYTHON_DOWNLOADS=0  → never download a Python; use the image's /usr/local/bin one.
#                            The venv's `python` is a symlink to it, so build and runtime
#                            must use this same base image.
ENV UV_COMPILE_BYTECODE=1 UV_LINK_MODE=copy UV_PYTHON_DOWNLOADS=0

# WORKDIR: creates /app (root-owned, if missing) and makes it the current directory for
# every later instruction and for the running container. /app mirrors the repo root, so
# paths.py finds its uv.lock marker here: PROJECT_ROOT = /app,
# FOUNDATIONS_DIR = /app/foundations. (DATA_DIR / OUTPUT_DIR come from the ENV below.)
WORKDIR /app

# ---------------------------------------------------------------------------
# Layer 1 — third-party dependencies only (the slow, rarely-changing part)
# ---------------------------------------------------------------------------
# COPY <src...> <dest>: copy from the build context into the image. Only the dependency
# manifests are copied here, not the code, so editing your .py files does NOT invalidate
# this layer and the next RUN — dependencies are reinstalled only when these change.
# .python-version tells uv which Python to use (3.14), found in the image because of
# UV_PYTHON_DOWNLOADS=0.
COPY pyproject.toml uv.lock .python-version ./
COPY foundations/pyproject.toml foundations/

# RUN: executes a command inside the image during the build; its file changes become a
# layer. Build steps run as root until the USER instruction below.
# --mount=type=cache,target=/root/.cache/uv
#   BuildKit feature (the default builder since Docker Engine 23). Gives uv a download
#   cache that persists on the BUILD machine between builds, so packages aren't
#   re-downloaded. The cache is mounted only while this command runs and is NOT saved
#   into the image. (/root/.cache/uv = uv's cache folder for the root user.)
# uv sync = make .venv match uv.lock. Creates /app/.venv here.
#   --frozen                 → install from uv.lock as written WITHOUT checking it against
#                              pyproject.toml. It can't be checked yet: the other workspace
#                              members' manifests aren't in the image. (CORRECTION 65: the
#                              freshness check is the --locked sync in layer 2.)
#   --no-install-workspace   → skip the workspace members' own code (not copied yet);
#                              install only third-party packages.
#   --package lj-foundations → only this member's dependencies; the root project's
#                              notebook stack (jupyterlab, matplotlib, ...) stays out.
#   --no-dev                 → skip the `dev` group, the only group uv installs by default.
#                              foundations' dev includes `test`, so pytest and ruff stay out.
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-install-workspace --package lj-foundations --no-dev

# ---------------------------------------------------------------------------
# Layer 2 — member manifests, runtime user + state folder, source, final sync
# ---------------------------------------------------------------------------
# The other members' pyproject.toml files (manifests only — their code never ships).
# uv.lock describes the WHOLE workspace, so --locked below can only verify it when every
# member's manifest is present. Adding a workspace member later = add its line here;
# the build fails loudly until you do.
COPY llm-api-smoke-test/pyproject.toml llm-api-smoke-test/
COPY courses/cs50_harvard/code/05_data_structures/speller/py_src/pyproject.toml \
     courses/cs50_harvard/code/05_data_structures/speller/py_src/

# Create an unprivileged system user + group named "app": a UID in the system range,
# a locked password, and no home directory. The container runs as this user instead of
# root (see USER below): if the process is ever compromised, it cannot change the code,
# the .venv or system files — all root-owned.
RUN groupadd --system app && useradd --system --gid app app

# Runtime state lives OUTSIDE the code tree; /data is the ONLY folder "app" can write to.
#   mkdir -p          → create /data and /data/outputs (-p: parents too, no error if present).
#   chown -R app:app  → hand the whole /data tree to "app" (this RUN still runs as root).
RUN mkdir -p /data/outputs && chown -R app:app /data

# Point paths.py at the state folder. _env_dir() reads these when the module is imported;
# they are absolute paths, so resolve() keeps them as-is (a relative value would be
# resolved against the working directory, /app). Without them, local runs keep the repo
# defaults (foundations/data, foundations/outputs).
# Override per run: docker run -e LJ_OUTPUT_DIR=/data/reports ...
ENV LJ_DATA_DIR=/data LJ_OUTPUT_DIR=/data/outputs

# Copy the member's source (src/, sql/, README.md, ...).
# No --chown: the code stays root-owned and read-only for "app" at runtime. Scanners
# flag `COPY --chown` because it leaves code writable by the runtime user.
# With -f foundations/Dockerfile, Docker filters the context through
# foundations/Dockerfile.dockerignore if that file exists (it takes precedence over a
# root .dockerignore). Without one, this COPY also brings in local-only folders such as
# foundations/data/, outputs/, tests/ and notebooks/.
COPY foundations/ foundations/

# Second sync, now that every manifest and the source are present:
#   --locked → FAIL the build if uv.lock is out of date with any pyproject.toml
#              (the reproducibility guarantee — CORRECTION 65).
#   Installs lj-foundations itself (the `learning_journey` import package), as an
#   editable install: a .pth file in .venv points to /app/foundations/src, so the source
#   must stay in the image. Third-party packages are already there from layer 1, so this
#   is quick.
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --locked --package lj-foundations --no-dev

# Put the venv first on PATH: `python` now means /app/.venv/bin/python. That interpreter
# reads /app/.venv/pyvenv.cfg and loads packages from .venv/lib/python3.14/site-packages.
# This is the "activation" — no uv needed at runtime.
ENV PATH="/app/.venv/bin:$PATH"

# Every later instruction, and every container started from this image, runs as "app".
USER app

# ENTRYPOINT = the program the container always runs. CMD = its default arguments.
# Both use exec form (a JSON list): no shell wraps the command, so python is PID 1 and
# receives signals itself.
#   docker run --rm recon-toy           → python -m learning_journey.projects.recon_toy --help
#   docker run --rm recon-toy <args>    → python -m learning_journey.projects.recon_toy <args>
# (Change the program itself with: docker run --entrypoint <cmd> recon-toy ...)
# PID 1 caveat: Linux ignores a signal sent to PID 1 unless the process installed a
# handler for it. Python handles SIGINT (Ctrl-C) but not SIGTERM, so `docker stop` waits
# 10 s and then SIGKILLs it. Harmless for a seconds-long batch job; for long runs, add
# `docker run --init` (a tiny init process becomes PID 1 and forwards signals) or a
# SIGTERM handler in the code.
ENTRYPOINT ["python", "-m", "learning_journey.projects.recon_toy"]
CMD ["--help"]
