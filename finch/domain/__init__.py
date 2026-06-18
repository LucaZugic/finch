"""Pure domain: journeys, legs, connections, slack. No IO, no framework imports.

The slack calculation lives here and is unit-testable with zero IO. Nothing in
this package may import boto3, fastapi, pyflink, stomp, or a kafka client
(ruff enforces this via banned-api).
"""
