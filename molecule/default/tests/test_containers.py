"""Verify Docker containers deployed by the role."""

from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from ._data import _CONTAINER_NAMES, _EXPECTED_PORTS

if TYPE_CHECKING:
    from testinfra.host import Host


@pytest.mark.parametrize("name", _CONTAINER_NAMES)
def test_container_running(host: Host, name: str) -> None:
    container = host.docker(name)
    assert container.is_running


@pytest.mark.parametrize("name", _CONTAINER_NAMES)
def test_container_restart_policy(host: Host, name: str) -> None:
    result = host.run("docker inspect -f '{{.HostConfig.RestartPolicy.Name}}' %s", name)
    assert result.rc == 0
    assert result.stdout.strip() == "unless-stopped"


@pytest.mark.parametrize(("port", "proto"), _EXPECTED_PORTS)
def test_unifi_app_port_exposed(host: Host, port: str, proto: str) -> None:
    result = host.run("docker inspect -f '{{json .HostConfig.PortBindings}}' unifi-network-application")
    assert result.rc == 0
    assert f"{port}/{proto}" in result.stdout


def test_mongo_port_not_exposed_by_default(host: Host) -> None:
    result = host.run("docker inspect -f '{{json .HostConfig.PortBindings}}' unifi-mongo")
    assert result.rc == 0
    assert "27017" not in result.stdout
