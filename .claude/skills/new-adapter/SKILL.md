---
name: new-adapter
description: Scaffold a new adapter port-first (define the Protocol before any concrete implementation). Use when adding an integration with Kafka/MSK, SNS/EventBridge, DynamoDB, S3, STOMP, or a new inbound entry point in Finch.
---

# new-adapter — port-first scaffold

Add the adapter described in `$ARGUMENTS` (e.g. "outbound DynamoDB JourneyRepository").
Enforce the dependency rule: **the port comes first; the adapter implements it.**

## Steps

1. **Define the port.** In `finch.ports`, add a `Protocol` (or ABC) phrased in domain terms
   — `AlertPublisher`, `JourneyRepository`, `IncidentSource` — typed with domain types, not
   vendor types. No `boto3`/kafka/framework names in the signature.
2. **Use it from the application.** Make the relevant use case depend on the port (constructor
   param). The application must not know which adapter implements it.
3. **RED — contract test.** Write a failing test for the concrete adapter under
   `tests/integration/adapters/<inbound|outbound>/`, `@pytest.mark.integration`, using
   Testcontainers (Kafka) or moto/localstack (AWS) and factories for data.
4. **GREEN — implement the adapter** in
   `finch/adapters/{inbound,outbound,streaming}/...`. This is the only layer allowed to
   import `boto3`/kafka/stomp/pyflink. Translate vendor errors to domain exceptions.
5. **Wire it in the composition root** (FastAPI app factory, Lambda handler, or streaming job
   entry) — never inside `domain`/`application`. Provision it in `infra/` (CDK) with
   least-privilege IAM and no hardcoded ARNs if it needs cloud resources.
6. **Verify:** `uv run pytest -q` (stack up) `&& uv run ruff check . && uv run mypy`.

Negative checks: no business logic in the adapter; no infra import leaking inward; the port —
not the concrete class — is what the application references.
