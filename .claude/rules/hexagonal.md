---
description: Hexagonal layering and the dependency rule for all source code.
paths:
  - "finch/**"
---

# Hexagonal architecture

The dependency arrow points inward only: `adapters → ports → application → domain`.

- **Keep the domain pure.** Put slack/connection logic in `domain/` as pure functions on
  immutable types. Never import `boto3`, `fastapi`, `pyflink`, `stomp`, or a kafka client
  here or in `application/` (ruff `banned-api` enforces this — don't suppress it).
- **Define a port before writing an adapter.** When the application needs something from
  the outside (persistence, publishing, an external feed), add a `Protocol`/ABC in
  `finch.ports` phrased in domain terms (`AlertPublisher`, not `SnsClient`). Then implement
  it in `adapters/outbound` (or `inbound`).
- **Adapters are thin.** Translate to/from the outside and call a use case. No branching on
  business conditions, no slack math, in a controller, consumer, or Flink operator.
- **Inject dependencies.** Use cases receive ports via constructor/params. Wiring (port →
  concrete adapter) happens only in a composition root: the FastAPI app factory, a Lambda
  handler, or the streaming job entry — never inside `domain`/`application`.
- **Translate errors at the edge.** Domain raises domain exceptions; adapters map them to
  HTTP/transport responses. Never let `botocore`/kafka exceptions propagate inward.

If a change seems to need an infra import in the domain, the design is wrong — add a port
instead.
