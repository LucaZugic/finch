---
description: TDD discipline and test layout for source and tests.
paths:
  - "finch/**"
  - "tests/**"
---

# TDD & testing

**Write a failing test first, every time.** Red → green → refactor:

1. Write the smallest test that expresses the next behaviour; run it; watch it fail.
2. Write the minimum production code to pass.
3. Refactor with the test green. Then repeat.

Running the suite:

- **Always run via `uv run pytest` against the *installed* package** — `uv sync` first if
  deps changed. We use a flat layout (`finch/` at the repo root), so bare `pytest` from the
  root imports the working-directory folder and can mask packaging mistakes; `uv run` tests
  the package as it ships.

Layout & coverage:

- **Mirror `finch/` under `tests/`.** `tests/unit/<layer>/...` for fast, IO-free tests of
  `domain`/`application`. `tests/integration/...` for adapters.
- **Keep the pyramid bottom-heavy.** Most tests are unit tests of the slack/domain logic —
  they need no Kafka, no AWS, no Flink. The fast suite (`uv run pytest -m "not integration"`)
  must stay fast.
- **Mark integration tests** with `@pytest.mark.integration`. Use **Testcontainers** for
  Kafka and **moto** (or the localstack endpoint) for AWS. Test real adapter behaviour
  against these, not mocks of the client.
- **Build test data with factories** in `tests/factories/` (polyfactory). Do not scatter
  inline literal fixtures or hand-rolled mocks across tests.
- **Test behaviour, not implementation.** Assert on outcomes (slack went negative, an alert
  was published), not on internal calls. Don't mock the type under test.
- **Don't test what ruff/mypy already guarantee** (types, formatting, import bans).
