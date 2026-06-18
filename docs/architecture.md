# Finch — Architecture

Finch (named for Darwin's finches — it re-plans the moment conditions change) is an
AWS-native, hexagonal, streaming system. The core invariant: a connection has
**slack** = (departure time of the onward leg) − (arrival time of the feeding leg) −
(minimum interchange time). Live Darwin updates continuously shift those times; when
slack goes negative for a watched journey, Finch alerts the traveller with the next
viable departure.

## Dataflow

```
Darwin Push Port (STOMP) ──► STOMP bridge (ECS Fargate, stomp.py) ──► MSK (Kafka)
KB incidents ──► Lambda (EventBridge schedule, poll) ─────────────► MSK (Kafka)
                                                                       │
MSK ──► Managed Service for Apache Flink (PyFlink, FLINK-2_2) ─────────┘
          per-journey stateful slack calc; fires on negative slack
            │
            └─► EventBridge ──► SNS ──► traveller alert

DTD fares/routeing files ──► Step Functions + AWS Glue ──► S3 (lake)
                                                        └─► DynamoDB (ticket
                                                            restrictions, station lookups)

Serving: FastAPI ──► API Gateway + Lambda (journey registration, status queries)
```

## Layers (hexagonal)

- **domain** — entities (`Journey`, `Leg`, `Connection`), value objects, and the pure
  slack calculation. No IO. The single source of truth for "is this connection at risk".
- **application** — use cases (register a journey, react to a Darwin update, publish an
  alert). Orchestrates domain logic through ports.
- **ports** — Protocols the inside owns: `JourneyRepository`, `AlertPublisher`,
  `IncidentSource`, `StationCatalogue`, etc.
- **adapters/inbound** — STOMP bridge, FastAPI routes, Lambda handlers; drive the app.
- **adapters/outbound** — Kafka producer/consumer, SNS/EventBridge publisher, DynamoDB and
  S3 repositories; implement ports.
- **adapters/streaming** — the PyFlink job: sources, keying by journey, watermarks,
  keyed state, and operators that delegate the actual slack math to `domain`.
- **infrastructure** — config, structured logging, AWS sessions/clients.
- **infra/** — the CDK app that provisions and wires all of the above.

## Why these choices

- **Hexagonal** keeps the slack logic free of AWS/Flink/transport concerns, so it is
  exhaustively unit-testable with no IO and reusable across the Flink job, the API, and
  batch backfills.
- **Streaming (Flink)** because slack is not a point-in-time query — it must be recomputed
  per journey as each delay arrives, with event-time semantics and durable per-journey
  state. Managed Service for Apache Flink runs the job; the pinned runtime is **FLINK-2_2**
  (Python 3.12).
- **AWS-native** managed services (MSK, MSF, EventBridge, SNS, Step Functions, Glue,
  DynamoDB, API Gateway + Lambda) keep operational surface low; CDK keeps it reproducible.

## Local ⇄ cloud mapping

| Cloud                         | Local (docker-compose)        |
|-------------------------------|-------------------------------|
| Amazon MSK                    | `apache/kafka`                |
| Managed Service for Flink     | `flink-jobmanager` + `flink-taskmanager` |
| S3 / SNS / EventBridge / Glue / Step Functions / Secrets Manager | `localstack` |
| DynamoDB                      | `dynamodb-local`              |
| STOMP bridge (Fargate)        | `stomp-bridge` service        |
