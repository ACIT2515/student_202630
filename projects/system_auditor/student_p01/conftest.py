"""Shared fixtures for the required disk, memory, and CPU checks."""

import json
from types import SimpleNamespace

import checks
import pytest

GB = 1024 ** 3
DISK_FREE = 40 * GB
MEMORY_TOTAL = 16 * GB
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

    # monkeypatch uses these fake functions during a test, then restores the
    # original psutil functions when the test ends.
    monkeypatch.setattr(checks.psutil, "disk_usage", disk_usage)
    monkeypatch.setattr(checks.psutil, "virtual_memory", virtual_memory)
    monkeypatch.setattr(checks.psutil, "cpu_count", cpu_count)


@pytest.fixture
def checks_file(tmp_path):
    """Write an audit with disk, memory, and CPU checks to a JSON file."""
    path = tmp_path / "checks.json"
    audit = {
        "audit_id": "test-audit",
        "audit_description": "Check the example host against a minimum policy.",
        "checks": [
            {
                "type": "disk",
                "requirement": 20,
                "description": "At least 20 GiB of free disk space.",
            },
            {
                "type": "memory",
                "requirement": 8,
                "description": "At least 8 GiB of installed memory.",
            },
            {
                "type": "cpu",
                "requirement": 4,
                "description": "At least 4 logical CPUs.",
            },
        ],
    }
    path.write_text(json.dumps(audit), encoding="utf-8")
    return path
