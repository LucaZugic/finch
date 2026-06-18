# Dev-container image. The PyCharm dev container and every `uv run ...` command
# execute inside this image — the host has no project tooling.
FROM python:3.12-slim

# uv: dependency + venv manager (source of truth is uv.lock).
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /usr/local/bin/

# System deps: git for tooling, default-jre for PyFlink, nodejs/npm for the CDK CLI.
RUN apt-get update && apt-get install -y --no-install-recommends \
        git default-jre-headless curl ca-certificates nodejs npm \
    && rm -rf /var/lib/apt/lists/* \
    && npm install -g aws-cdk@2

ENV UV_PROJECT_ENVIRONMENT=/opt/venv \
    PATH="/opt/venv/bin:$PATH" \
    UV_LINK_MODE=copy

WORKDIR /workspaces/finch

# Keeps the container alive for the dev-container lifecycle; PyCharm attaches a shell.
CMD ["sleep", "infinity"]
