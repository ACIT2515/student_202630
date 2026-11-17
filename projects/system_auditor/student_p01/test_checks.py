"""Test the check classes without inspecting the real computer.

The fake_system fixture in conftest.py uses monkeypatch to replace psutil's
disk, memory, and CPU functions, so these tests always see the same fake host
no matter which computer runs them. Each test that measures the system lists
fake_system as a parameter so the fixture it depends on is visible.
"""

import checks
import pytest

# These tests sometimes read protected attributes such as check._requirement.
# That is acceptable in a test when it makes the test clearer or more precise,
# for example to confirm what create_check() built before anything is measured.
# Where possible, prefer testing through the object's public interface, such
# as run() and the CheckResult properties, because that is what other code uses


def test_system_check_is_abstract():
    """SystemCheck cannot be created because it does not know how to measure"""
    with pytest.raises(TypeError):
        checks.SystemCheck("Example", 1, "Example description.")


def test_disk_check(fake_system):
    """Disk space is free bytes converted to GiB."""
    check = checks.create_check(
        {
            "type": "disk",
            "requirement": 20,
            "description": "At least 20 GiB of free disk space.",
        }
    )

    assert isinstance(check, checks.DiskCheck)
    assert check._requirement == 20
    assert check._description == "At least 20 GiB of free disk space."
    assert check.measure() == 40.0


def test_memory_check(fake_system):
    """Memory is total installed bytes converted to GiB."""
    check = checks.create_check(
        {
            "type": "memory",
            "requirement": 8,
            "description": "At least 8 GiB of installed memory.",
        }
    )

    assert isinstance(check, checks.MemoryCheck)
    assert check._requirement == 8
    assert check._description == "At least 8 GiB of installed memory."
    assert check.measure() == 16.0


def test_check_run_returns_result(fake_system, capsys):
    """run() returns a CheckResult without printing."""
    check = checks.CPUCheck(4, "At least 4 logical CPUs.")

    result = check.run()

    assert isinstance(result, checks.CheckResult)
    assert result.name == "CPUs"
    assert result.description == "At least 4 logical CPUs."
    assert result.measured == 8
    assert result.requirement == 4
    assert result.passed is True
    assert capsys.readouterr().out == ""  # Verify nothing printed


if __name__ == "__main__":
    raise SystemExit(pytest.main([__file__]))
