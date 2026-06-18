"""CDK app entry point. Env comes from context/env vars — no hardcoded account/region/ARNs."""

import os

import aws_cdk as cdk

app = cdk.App()

env = cdk.Environment(
    account=os.environ.get("CDK_DEFAULT_ACCOUNT"),
    region=os.environ.get("CDK_DEFAULT_REGION", "eu-west-2"),
)

# Stacks are added here, e.g.:
# from stacks.streaming_stack import StreamingStack
# StreamingStack(app, "Finch-Streaming", env=env)

app.synth()
