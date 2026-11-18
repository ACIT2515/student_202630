"""Test the check classes without inspecting the real computer.

The fake_system fixture in conftest.py uses monkeypatch to replace psutil's
disk, memory, and CPU functions, so these tests always see the same fake host
no matter which computer runs them. Each test that measures the system lists
fake_system as a parameter so the fixture it depends on is visible.
"""

import checks
import pytest
from check_result import CheckResult


def test_system_check_is_abstract():
    """SystemCheck cannot be created without implementing measure()."""
    with pytest.raises(Exception):
        checks.SystemCheck(1, "Example description.")


def test_disk_check_measure(fake_system):
    """Disk measurement converts free bytes to GiB."""
    check = checks.DiskCheck(20, "At least 20 GiB of free disk space.")

    assert check.measure() == 40.0


def test_memory_check_measure(fake_system):
    """Memory measurement converts total installed bytes to GiB."""
    check = checks.MemoryCheck(8, "At least 8 GiB of installed memory.")

    assert check.measure() == 16.0


def test_cpu_check_measure(fake_system):
    """CPU measurement returns the logical CPU count."""
    check = checks.CPUCheck(4, "At least 4 logical CPUs.")

    assert check.measure() == 8


def test_disk_check_run(fake_system):
    """Disk run returns results for met and unmet requirements silently."""
    check = checks.DiskCheck(40, "At least 40 GiB of free disk space.")

    result = check.run()

    assert isinstance(result, CheckResult)
    assert result.name == "Disk Space"
    assert result.description == "At least 40 GiB of free disk space."
    assert result.measured == 40.0
    assert result.requirement == 40
    assert result.passed is True

    failing_check = checks.DiskCheck(41, "At least 41 GiB of free disk space.")
    assert failing_check.run().passed is False


def test_memory_check_run(fake_system):
    """Memory run returns results for met and unmet requirements silently."""
    check = checks.MemoryCheck(16, "At least 16 GiB of installed memory.")

    result = check.run()

    assert isinstance(result, CheckResult)
    assert result.name == "Memory"
    assert result.description == "At least 16 GiB of installed memory."
    assert result.measured == 16.0
    assert result.requirement == 16
    assert result.passed is True

    failing_check = checks.MemoryCheck(17, "At least 17 GiB of installed memory.")
    assert failing_check.run().passed is False


def test_cpu_check_run(fake_system):
    """CPU run returns results for met and unmet requirements silently."""
    check = checks.CPUCheck(8, "At least 8 logical CPUs.")

    result = check.run()

    assert isinstance(result, CheckResult)
    assert result.name == "CPUs"
    assert result.description == "At least 8 logical CPUs."
    assert result.measured == 8
    assert result.requirement == 8
    assert result.passed is True

    failing_check = checks.CPUCheck(9, "At least 9 logical CPUs.")
    assert failing_check.run().passed is False


def test_create_check_disk(fake_system):
    """A disk specification creates a DiskCheck with its policy values."""
    specification = {
        "type": "disk",
        "requirement": 20,
        "description": "At least 20 GiB of free disk space.",
    }

    check = checks.create_check(specification)
    result = check.run()

    assert isinstance(check, checks.DiskCheck)
    assert result.name == "Disk Space"
    assert result.requirement == specification["requirement"]
    assert result.description == specification["description"]


def test_create_check_memory(fake_system):
    """A memory specification creates a MemoryCheck with its policy values."""
    specification = {
        "type": "memory",
        "requirement": 8,
        "description": "At least 8 GiB of installed memory.",
    }

    check = checks.create_check(specification)
    result = check.run()

    assert isinstance(check, checks.MemoryCheck)
    assert result.name == "Memory"
    assert result.requirement == specification["requirement"]
    assert result.description == specification["description"]


def test_create_check_unknown_type():
    """An unknown check type raises an error."""
    specification = {
        "type": "network",
        "requirement": 1,
        "description": "At least one network interface.",
    }

    with pytest.raises(Exception):
        checks.create_check(specification)


def test_create_check_missing_type():
    """A specification must identify the check type."""
    specification = {"requirement": 4, "description": "At least 4 logical CPUs."}

    with pytest.raises(Exception):
        checks.create_check(specification)


def test_create_check_missing_requirement():
    """A specification must include a requirement."""
    specification = {"type": "cpu", "description": "At least 4 logical CPUs."}

    with pytest.raises(Exception):
        checks.create_check(specification)


def test_create_check_missing_description():
    """A specification must include a description."""
    specification = {"type": "cpu", "requirement": 4}

    with pytest.raises(Exception):
        checks.create_check(specification)
