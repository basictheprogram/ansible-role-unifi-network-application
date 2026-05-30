"""Verify host directories and files created by the role."""

from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from ._data import _APP_PATH, _DB_PATH, _MONGO_INIT_PATH

if TYPE_CHECKING:
    from testinfra.host import Host

_EXPECTED_DIRS: list[str] = [_APP_PATH, _DB_PATH]


@pytest.mark.parametrize("path", _EXPECTED_DIRS)
def test_appdata_directory_exists(host: Host, path: str) -> None:
    d = host.file(path)
    assert d.exists
    assert d.is_directory


@pytest.mark.parametrize("path", _EXPECTED_DIRS)
def test_appdata_directory_mode(host: Host, path: str) -> None:
    d = host.file(path)
    assert oct(d.mode) == "0o775"


def test_mongo_init_script_exists(host: Host) -> None:
    f = host.file(_MONGO_INIT_PATH)
    assert f.exists
    assert f.is_file


def test_mongo_init_script_executable(host: Host) -> None:
    f = host.file(_MONGO_INIT_PATH)
    assert oct(f.mode) == "0o755"


def test_mongo_init_script_content(host: Host) -> None:
    f = host.file(_MONGO_INIT_PATH)
    assert "createUser" in f.content_string
    assert "dbOwner" in f.content_string
