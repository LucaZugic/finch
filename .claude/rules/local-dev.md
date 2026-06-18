---
description: Local stack and dev-container conventions.
paths:
  - "docker-compose*.yml"
  - ".devcontainer/**"
  - "docker/**"
---

# Local development

`docker-compose.yml` is the **source of truth** for the local stack. Services and how they
network (every service reachable by name on the compose network):

- `dev` — the dev container PyCharm attaches to; all commands run here.
- `kafka` (`apache/kafka`) — local stand-in for MSK, at `kafka:9092`.
- `flink-jobmanager` + `flink-taskmanager` — local Flink cluster (UI at `:8081`).
- `stomp-bridge` — the Darwin→Kafka bridge process.
- `localstack` — S3, SNS, EventBridge, Step Functions, Glue, Secrets Manager (`:4566`).
- `dynamodb-local` — DynamoDB (`:8000`).

Rules:

- **All tooling runs inside the dev container** (interpreter + `uv run ...`). Never assume a
  host-installed Python, uv, node, or AWS CLI.
- **New runtime/dev dependencies** go into `pyproject.toml` and `uv.lock` (`uv add ...`), and
  into the image/compose if they need system packages — never `pip install` on the host.
- **Keep devcontainer wired to compose:** `dockerComposeFile` + `service: dev` +
  `workspaceFolder`. After changing the image, compose, or `devcontainer.json`, **rebuild and
  reopen the container in PyCharm** ("Rebuild and Reopen in Container") so changes take effect.
- **Reference services by name, not localhost,** from inside the container (`kafka:9092`,
  `http://localstack:4566`).
- **Never hardcode real credentials** in compose/env; use `.env` (gitignored) and
  `.env.example` for the template.
