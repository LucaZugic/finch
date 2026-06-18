"""Ports: Protocols/ABCs the application depends on, owned by the inside.

Define interfaces in terms of the domain (e.g. JourneyRepository, AlertPublisher,
IncidentSource). Adapters in `adapters/` implement these; the dependency arrow
points inward (adapter -> port), never outward.
"""
