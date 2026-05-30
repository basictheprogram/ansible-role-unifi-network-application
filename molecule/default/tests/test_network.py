"""Verify Docker network created by the role."""

from __future__ import annotations

from typing import TYPE_CHECKING

from ._data import _CONTAINER_NAMES, _DOCKER_NETWORK

if TYPE_CHECKING:
    from testinfra.host import Host


def test_docker_network_exists(host: Host) -> None:
    result = host.run("docker network inspect %s", _DOCKER_NETWORK)
    assert result.rc == 0


def test_docker_network_driver(host: Host) -> None:
    result = host.run("docker network inspect -f '{{.Driver}}' %s", _DOCKER_NETWORK)
    assert result.rc == 0
    assert result.stdout.strip() == "bridge"


def test_containers_on_network(host: Host) -> None:
    result = host.run("docker network inspect -f '{{json .Containers}}' %s", _DOCKER_NETWORK)
    assert result.rc == 0
    for name in _CONTAINER_NAMES:
        assert name in result.stdout
