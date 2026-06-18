"""Cross-cutting technical concerns: config loading, logging setup, AWS clients/sessions.

Not the domain, not a use case. Adapters and composition roots use this; the
domain never imports it.
"""
