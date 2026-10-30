# Dockerfile — recon-toy
# Two-stage pattern: tiny, reproducible, exactly what uv.lock says.

# Build from the REPO ROOT:  docker build -f foundations/Dockerfile -t recon-toy .
FROM python:3.14-slim AS base

# Install uv inside the image by copying its binary from Astral's image —
# faster and more reproducible than curl-piping an installer at build time.
# pin; never :latest (uv docs)
COPY --from=ghcr.io/astral-sh/uv:0.13.6 /uv /uvx /bin/
ENV UV_COMPILE_BYTECODE=1 UV_LINK_MODE=copy UV_PYTHON_DOWNLOADS=0

WORKDIR /app

# Layer 1: third-party deps only. --frozen, because the other members' manifests aren't here yet.
COPY pyproject.toml uv.lock .python-version ./
COPY foundations/pyproject.toml foundations/

# THE ROADMAP IDIOM: --frozen = install EXACTLY uv.lock, refuse to resolve
# anything new.
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-install-workspace --package lj-foundations --no-dev
#            └ --no-dev: pytest/ruff don't ship to production images.

# Layer 2: every member manifest, then the source. --locked asserts uv.lock is fresh (C65).
COPY llm-api-smoke-test/pyproject.toml llm-api-smoke-test/
COPY courses/cs50_harvard/code/05_data_structures/speller/py_src/pyproject.toml \
     courses/cs50_harvard/code/05_data_structures/speller/py_src/

RUN groupadd --system app && useradd --system --gid app app

COPY --chown=app:app foundations/ foundations/

RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --locked --package lj-foundations --no-dev

ENV PATH="/app/.venv/bin:$PATH"

USER app

ENTRYPOINT ["python", "-m", "learning_journey.projects.recon_toy"]
CMD ["--help"]
