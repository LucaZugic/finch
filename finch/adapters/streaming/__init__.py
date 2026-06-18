"""PyFlink streaming adapter: the slack job and its operators.

Operators are thin shells that call into pure `domain` slack logic. Keying,
watermarks, and state belong here; calculation does not. See
.claude/rules/streaming-flink.md.
"""
