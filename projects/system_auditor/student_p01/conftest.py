"""Shared fixtures for required system checks."""

from types import SimpleNamespace

import checks
import pytest

GIB = 1024 ** 3
DISK_FREE = 40 * GIB
MEMORY_TOTAL = 16 * GIB
CPU_COUNT = 8


# SimpleNamespace makes lightweight objects with attributes without defining a
# class. Here, those attributes mimic the values returned by psutil functions.


@pytest.fixture
def fake_system(monkeypatch):
    """Replace required disk, memory, and CPU measurements with fake data.

    Tests that measure the system must request this fixture by name.
    """

    def disk_usage(path):
        """Return fake free space for the root filesystem."""
        assert path == "/"
        return SimpleNamespace(free=DISK_FREE)

    def virtual_memory():
        """Return fake total memory."""
        return SimpleNamespace(total=MEMORY_TOTAL)

    def cpu_count():
        """Return a fake logical CPU count."""
        return CPU_COUNT

    # monkeypatch restores the original psutil functions when the test ends.
    monkeypatch.setattr(checks.psutil, "disk_usage", disk_usage)
    monkeypatch.setattr(checks.psutil, "virtual_memory", virtual_memory)
    monkeypatch.setattr(checks.psutil, "cpu_count", cpu_count)
