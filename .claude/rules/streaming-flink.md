---
description: PyFlink slack job conventions — keying, event time, idempotency, runtime pin.
paths:
  - "finch/adapters/streaming/**"
  - "tests/integration/streaming/**"
---

# PyFlink streaming job

Pin the runtime to **Amazon MSF `FLINK-2_2` (Apache Flink 2.2, Python 3.12)**. Do not use
APIs deprecated/removed in Flink 2.x, and keep `apache-flink==2.2.0` in `pyproject.toml`.

- **Operators delegate to the domain.** A `KeyedProcessFunction` extracts state and timers,
  then calls the pure slack function from `finch.domain`. Never inline slack math, station
  lookups, or business thresholds into an operator.
- **Key by journey.** Use the journey id as the key so each journey owns its keyed state;
  slack is per-journey and must not be computed across the whole stream.
- **Event time + watermarks.** Use the Darwin event timestamp as event time with a bounded
  out-of-orderness watermark strategy. Do not compute slack on processing time — late delays
  would be missed or misordered.
- **Idempotency.** Darwin redelivers. Dedupe by message id / sequence in keyed state, and
  make alert emission idempotent (an alert for the same journey+connection+cause fires once).
  Use timers to fire/expire state rather than unbounded buffering.
- **Manage state lifecycle.** Register/clear timers and clear keyed state once a journey
  completes, so state doesn't grow without bound.
- **Test on the local cluster.** Integration tests run against the compose `flink-jobmanager`
  /`flink-taskmanager`; keep the slack logic itself covered by fast domain unit tests.
