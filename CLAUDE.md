# Finch

Real-time **connection guardian** for UK rail. Finch watches a traveller's booked
journey legs on the National Rail **Darwin Push Port** (STOMP) and alerts them the
moment a connection's slack goes negative — *"you'll miss the 18:32 — take the 18:47."*
It is **hexagonal** so the slack logic stays pure and testable, and **streaming**
(Flink) because slack must be recomputed continuously as live delays arrive.

Architecture detail: @docs/architecture.md

## Project map

```
finch/               The import package (flat layout — no src/ dir).
  domain/            Pure: journeys, legs, connections, slack calc. ZERO IO.
  application/        Use cases; orchestrates the domain through ports.
  ports/              Protocols/ABCs the inside owns (repos, publishers, sources).
  adapters/
    inbound/          STOMP bridge, FastAPI routes, Lambda handlers (thin).
    outbound/         Kafka/MSK, SNS+EventBridge, DynamoDB, S3 (raw boto3 OK here).
    streaming/        PyFlink slack job + operators (operators delegate to domain).
  infrastructure/     Config, logging, AWS client/session setup.
infra/                AWS CDK app (Python). Stacks, IAM, wiring.
tests/                unit/ (fast, IO-free) · integration/ · factories/
docker-compose.yml    Source of truth for the local stack.
.devcontainer/        Dev container wired to the compose `dev` service.
```

The dependency arrow points **inward only**: adapters → ports → application → domain.
The domain depends on nothing in this list above it.

## Two rules that must not be broken

- **IMPORTANT: the domain is pure.** Code in `domain/`/`application/` MUST NOT import
  `boto3`, `fastapi`, `pyflink`, `stomp`, or a kafka client. Talk to the outside through
  a port; implement ports in `adapters/`. (ruff `banned-api` fails the build otherwise.)
- **YOU MUST write a failing test first.** Red → green → refactor, for every change.
  No production code without a test that was red first. Details in the auto-loaded rules.

## Commands

All commands run **inside the dev container** (PyCharm attaches to the compose `dev`
service). Do not run project tooling on the host. Run tests via `uv run pytest` (against the
installed package — flat layout means bare `pytest` would import the working dir instead);
`uv sync` first if deps changed.

```bash
uv run pytest -m "not integration"   # fast suite — domain/application, IO-free
uv run pytest                        # full suite (Testcontainers + moto)
uv run ruff check . && uv run ruff format --check .   # lint + format check
uv run ruff format .                 # apply formatting
uv run mypy                          # strict type check (src, tests, infra)

docker compose up -d                 # bring the local stack up
docker compose logs -f <service>     # tail a service (kafka, flink-jobmanager, ...)
docker compose down                  # tear it down

cd infra && cdk synth                # render CloudFormation
cd infra && cdk diff                 # diff against deployed
cd infra && cdk deploy               # deploy (needs AWS creds)
```

## Conventions

- **Style beyond ruff/mypy:** prefer pure functions and frozen dataclasses / immutable
  Pydantic models for domain types; pass dependencies in (constructor/params), don't reach
  for module globals or singletons.
- **FastAPI:** routes parse/validate and delegate to an application use case in one call —
  no business logic, DB access, or boto3 in a controller. Inject use cases via `Depends`.
- **Errors:** the domain raises domain exceptions (e.g. `UnknownStation`); adapters
  translate them to HTTP/transport errors. Don't leak `botocore`/`kafka` exceptions inward.
- **Logging:** structured, via `infrastructure` logging setup. No `print`. Never log
  credentials or full passenger PII.

## Guardrails

- **Generated — do not edit:** `uv.lock` (use `uv add`/`uv lock`), `infra/cdk.out/`,
  `.ruff_cache`/`.mypy_cache`/`.pytest_cache`.
- **Secrets:** never commit credentials. Local secrets go in `.env` (gitignored; see
  `.env.example`); deployed secrets come from **AWS Secrets Manager**. No ARNs/account IDs
  hardcoded in `infra/` — derive from context/env.
- **New dependencies** go into `pyproject.toml` + the image/compose and the `uv` lockfile —
  never `pip install` onto the host.
- **Stay in scope.** A narrow request gets a narrow change; don't refactor or restructure
  adjacent code unasked.

Deeper, path-scoped rules live in `.claude/rules/*.md` and auto-load when you edit the
files they cover (hexagonal, tdd-testing, streaming-flink, infra-cdk, local-dev).
