"""Pytest configuration and session-scoped fixtures."""

from __future__ import annotations

import pytest

from ._data import _CONTAINER_NAMES


@pytest.fixture(scope="session")
def container_names() -> list[str]:
    """Return the list of container names deployed by the role."""
    return _CONTAINER_NAMES
