---
name: tdd
description: Drive one red-green-refactor TDD cycle for a described behaviour. Use when implementing or changing any domain/application/adapter behaviour in Finch.
---

# tdd — one red-green-refactor cycle

Implement the behaviour described in `$ARGUMENTS` strictly test-first. Do **not** write
production code before a failing test exists.

## Steps

1. **Locate / create the test.** Mirror `finch/` under `tests/`: domain & application →
   `tests/unit/<layer>/`; adapters → `tests/integration/` with `@pytest.mark.integration`.
   Build inputs from factories in `tests/factories/` (polyfactory), not inline mocks.
2. **RED.** Write the smallest test that captures the next increment of behaviour. Run the
   fast suite and confirm it fails for the expected reason:
   `uv run pytest -m "not integration" <path> -q`
   (integration work: `uv run pytest <path> -q` with the local stack up).
   Always run via `uv run` — it tests the installed package, not the working dir (flat
   layout); `uv sync` first if you changed dependencies. Show the failure before continuing.
3. **GREEN.** Write the minimum production code to pass — respect hexagonal layering
   (pure domain; ports before adapters; no infra imports inward). Re-run; confirm green.
4. **REFACTOR.** Clean up names/duplication with tests green. Re-run to confirm.
5. **Verify the suite & gates** before reporting done:
   `uv run pytest -m "not integration" -q && uv run ruff check . && uv run mypy`

If a step would require an infra import inside the domain, stop and introduce a port instead.
Keep the cycle small — one behaviour at a time.
