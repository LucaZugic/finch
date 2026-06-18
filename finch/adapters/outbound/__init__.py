"""Outbound adapters: driven by the application. Kafka/MSK, SNS/EventBridge, DynamoDB, S3.

Each implements a port defined in `finch.ports`. This is the only place raw
boto3 / kafka clients are allowed.
"""
