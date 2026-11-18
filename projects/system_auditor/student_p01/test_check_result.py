"""Test how a check result is presented."""

from check_result import CheckResult


def test_to_dict():
    """The dictionary contains the result's fields and values."""
    result = CheckResult("Disk Space", "Check free disk space.", 40.0, 20, True)

    assert result.to_dict() == {
        "name": "Disk Space",
        "description": "Check free disk space.",
        "measured": 40.0,
        "requirement": 20,
        "passed": True,
    }


def test_to_dict_failed_result():
    """A failed result is recorded as False."""
    result = CheckResult("Disk Space", "Check free disk space.", 10.0, 20, False)

    assert result.to_dict()["passed"] is False


def test_str_passed_result():
    """The text includes the result's values and a PASS outcome."""
    result = CheckResult("Disk Space", "Check free disk space.", 40.0, 20, True)

    text = str(result)

    assert "Disk Space" in text
    assert "Description:" in text
    assert "Check free disk space." in text
    assert "Measured:" in text
    measured = text.split("Measured:", 1)[1].splitlines()[0]
    assert float(measured) == 40.0
    assert "Requirement:" in text
    requirement = text.split("Requirement:", 1)[1].splitlines()[0]
    assert float(requirement) == 20
    assert "Result:" in text
    outcome = text.split("Result:", 1)[1].splitlines()[0]
    assert outcome.strip() == "PASS"


def test_str_failed_result():
    """A failed result is presented as FAIL."""
    result = CheckResult("Disk Space", "Check free disk space.", 10.0, 20, False)

    text = str(result)

    assert "Result:" in text
    outcome = text.split("Result:", 1)[1].splitlines()[0]
    assert outcome.strip() == "FAIL"
