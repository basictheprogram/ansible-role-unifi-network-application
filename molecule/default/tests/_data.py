"""Shared constants for the unifi_network_application test suite."""

from __future__ import annotations

_BASE_PATH = "/opt/unifi"
_APP_PATH = _BASE_PATH + "/app"
_DB_PATH = _BASE_PATH + "/db"
_MONGO_INIT_PATH = _DB_PATH + "/mongo-init.sh"

_DOCKER_NETWORK = "unifi"

# Containers deployed by the role (default configuration, mongo-express disabled)
_CONTAINER_NAMES: list[str] = [
    "unifi-mongo",
    "unifi-network-application",
]

# (host_port, protocol) pairs exposed by default
_EXPECTED_PORTS: list[tuple[str, str]] = [
    ("8443", "tcp"),
    ("8080", "tcp"),
    ("3478", "udp"),
    ("10001", "udp"),
]
