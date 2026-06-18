---
description: AWS CDK conventions — least privilege, no hardcoded ARNs, env-driven config.
paths:
  - "infra/**"
---

# Infrastructure (AWS CDK, Python)

- **No hardcoded account IDs, regions, or ARNs.** Derive account/region from
  `CDK_DEFAULT_*` env (see `infra/app.py`); reference resources via construct objects
  (`bucket.bucket_arn`, `topic.topic_arn`), never literal strings.
- **Least-privilege IAM.** Grant with resource methods (`table.grant_read_data(fn)`,
  `topic.grant_publish(fn)`). No `"Action": "*"`, no wildcard `Resource: "*"`, no
  `AdministratorAccess`. Scope every policy to the specific resource and action.
- **Secrets via Secrets Manager.** Inject with `Secret.from_secret_name_v2` / secret
  references. Never put credentials in env defaults, context, or code.
- **Config per environment** comes from context/env, not branches in code. Keep stacks
  composable (one concern per stack: streaming, serving, batch, data).
- **Tag and name from context**, not hardcoded literals, so multiple environments coexist.
- **Validate with `cdk synth` / `cdk diff`** before proposing a deploy; review the diff.
