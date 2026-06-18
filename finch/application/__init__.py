"""Use cases / orchestration. Coordinates domain logic through ports.

Depends on `domain` and `ports` only — never on concrete adapters. Wiring of
ports to adapters happens in a composition root (adapters/streaming job entry,
the FastAPI app factory, a Lambda handler), not here.
"""
