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
# RUN:    docker run --rm recon-toy             → runs with the default args (CMD: --help)
#         docker run --rm recon-toy <args...>   → <args> replace CMD
#   --rm   deletes the stopped container afterwards (the image stays).
#         docker run --rm -v "$PWD/foundations/data:/data" recon-toy --participants 50
#
# HOW A BUILD WORKS
#   Each instruction (FROM, COPY, RUN, ...) produces one LAYER: a read-only snapshot of
#   the filesystem changes it made. The image is the stack of layers. Docker caches each
#   layer and reuses it on the next build if that instruction AND its inputs (the copied
#   files) are unchanged. Once one layer changes, every layer below it is rebuilt.
#   → So the order is: things that rarely change (Python, uv, dependencies) first,
#     things that change often (your source code) last.
#
# WHERE THE PACKAGES COME FROM
#   Nothing is copied from your machine's .venv. The `RUN uv sync` steps CREATE
#   /app/.venv inside the image, so the installed packages are part of the image layers.
#   Anyone who pulls this image gets them with it. uv is needed only to BUILD;
#   at runtime the container calls python directly (see ENTRYPOINT).
#
# Single-stage for now (roadmap: multi-stage is a Stage-2 optimisation). A second stage
# would copy only /app/.venv + source into a fresh python:3.14-slim, leaving uv behind.
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
# step with [tool.uv] required-version and the uv version CI runs.
COPY --from=ghcr.io/astral-sh/uv:0.13.6 /uv /uvx /bin/

# ENV: sets environment variables for every later build step AND for running containers.
#   UV_COMPILE_BYTECODE=1  → compile .py → .pyc during the build, so the container doesn't
#                            do it at startup (faster start; the non-root user couldn't
#                            write them anyway).
#   UV_LINK_MODE=copy      → uv normally hard-links files from its cache; the cache mount
#                            below is a separate filesystem where that fails, so copy
#                            instead and silence the warning.
#   UV_PYTHON_DOWNLOADS=0  → never download a Python; use the image's /usr/local/bin one.
#                            The venv's `python` is a symlink to it, so build and runtime
#                            must use this same base image.
ENV UV_COMPILE_BYTECODE=1 UV_LINK_MODE=copy UV_PYTHON_DOWNLOADS=0

# WORKDIR: creates /app (if missing) and makes it the current directory for every later
# instruction and for the running container. /app mirrors the repo root, so paths.py
# finds its uv.lock marker here (/app/uv.lock) and FOUNDATIONS_DIR = /app/foundations.
WORKDIR /app

# ---------------------------------------------------------------------------
# Layer 1 — third-party dependencies only (the slow, rarely-changing part)
# ---------------------------------------------------------------------------
# COPY <src...> <dest>: copy from the build context into the image. Only the dependency
# manifests are copied here, not the code, so editing your .py files does NOT invalidate
# this layer and the next RUN — dependencies are reinstalled only when these change.
COPY pyproject.toml uv.lock .python-version ./
COPY foundations/pyproject.toml foundations/

# RUN: executes a command inside the image during the build; its file changes become a layer.
# --mount=type=cache,target=/root/.cache/uv
#   BuildKit feature (the default builder since Docker Engine 23). Gives uv a download
#   cache that persists on the BUILD machine between builds, so packages aren't
#   re-downloaded. The cache is mounted only while this command runs and is NOT saved
#   into the image.
# uv sync = make .venv match uv.lock. Creates /app/.venv here.
#   --frozen                 → install from uv.lock as written WITHOUT checking it against
#                              pyproject.toml. It can't be checked yet: the other workspace
#                              members' manifests aren't in the image. (CORRECTION 65: the
#                              freshness check is the --locked sync in layer 2.)
#   --no-install-workspace   → skip the workspace members' own code (not copied yet);
#                              install only third-party packages.
#   --package lj-foundations → only this member's dependencies; the root project's
#                              notebook stack (jupyterlab, matplotlib, ...) stays out.
#   --no-dev                 → skip dependency groups like dev/test (pytest, ruff).
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-install-workspace --package lj-foundations --no-dev

# ---------------------------------------------------------------------------
# Layer 2 — every member manifest, a runtime user, then the source
# ---------------------------------------------------------------------------
# The other members' pyproject.toml files (manifests only — their code never ships).
# uv.lock describes the WHOLE workspace, so --locked below can only verify it when every
# member's manifest is present. Adding a workspace member later = add its line here;
# the build fails loudly until you do.
COPY llm-api-smoke-test/pyproject.toml llm-api-smoke-test/
COPY courses/cs50_harvard/code/05_data_structures/speller/py_src/pyproject.toml \
     courses/cs50_harvard/code/05_data_structures/speller/py_src/

# Create an unprivileged system user + group named "app" (no password, no login).
# The container will run as this user instead of root (see USER below): if the process
# is ever compromised, it cannot change the root-owned .venv or system files.
RUN groupadd --system app && useradd --system --gid app app

# Runtime state lives outside the code tree; this is the ONLY folder "app" can write to.
RUN mkdir -p /data/outputs && chown -R app:app /data
ENV LJ_DATA_DIR=/data LJ_OUTPUT_DIR=/data/outputs

# Copy the member's source. --chown=app:app makes the "app" user the owner, so the
# toy can write its SQLite file under projects/data/ at runtime. Everything else in the
# image stays root-owned (readable, not writable, by "app").
# What gets copied is filtered by foundations/Dockerfile.dockerignore.
#
# No --chown: code stays root-owned and read-only for "app" at runtime.
COPY foundations/ foundations/

# Second sync, now that every manifest and the source are present:
#   --locked → FAIL the build if uv.lock is out of date with any pyproject.toml
#              (the reproducibility guarantee — CORRECTION 65).
#   Installs lj-foundations itself (the `learning_journey` import package), as an
#   editable install: .venv links to /app/foundations/src, so the source must stay in
#   the image. Third-party packages are already there from layer 1, so this is quick.
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
# receives `docker stop`'s SIGTERM directly.
#   docker run --rm recon-toy           → python -m learning_journey.projects.recon_toy --help
#   docker run --rm recon-toy <args>    → python -m learning_journey.projects.recon_toy <args>
# (Change the program itself with: docker run --entrypoint <cmd> recon-toy ...)
ENTRYPOINT ["python", "-m", "learning_journey.projects.recon_toy"]
CMD ["--help"]
