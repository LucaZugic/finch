"""Inbound adapters: drive the application. STOMP bridge, FastAPI routes, Lambda handlers.

Keep these thin: translate the outside world into domain calls and back. No
business logic — that belongs in `domain`/`application`.
"""
