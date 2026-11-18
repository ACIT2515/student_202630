"""Test audit report presentation and overall outcomes."""

import pytest

from audit_report import AuditReport


class FakeCheckResult:
    """Provide the result behavior needed by AuditReport."""

    def __init__(self, name: str, passed: bool) -> None:
        """Store a name and a predetermined outcome."""
        self.name = name
        self.passed = passed

    def to_dict(self) -> dict:
        """Return predictable result data."""
        return {"check": self.name, "passed": self.passed}

    def __str__(self) -> str:
        """Return predictable result text."""
        return f"Result for {self.name}"


@pytest.fixture
def fake_results() -> list[FakeCheckResult]:
    """Return a failure between two passing results."""
    return [
        FakeCheckResult("Disk Space", True),
        FakeCheckResult("Memory", False),
        FakeCheckResult("CPUs", True),
    ]


def test_passed_when_all_results_pass(fake_results):
    """The report passes when every check passed."""
    results = [fake_results[0], fake_results[2]]
    report = AuditReport(results, "host-baseline", "Check host resources.")

    assert report.passed is True


def test_passed_when_a_result_fails(fake_results):
    """A failure between passing results makes the report fail."""
    report = AuditReport(
        fake_results, "host-baseline", "Check host resources."
    )

    assert report.passed is False


def test_passed_with_no_results():
    """An empty report passes because no checks failed."""
    report = AuditReport([], "host-baseline", "Check host resources.")

    assert report.passed is True


def test_to_dict(fake_results):
    """The dictionary includes audit identity, ordered results, and outcome."""
    results = fake_results[:2]
    report = AuditReport(results, "host-baseline", "Check host resources.")

    assert report.to_dict() == {
        "audit_id": "host-baseline",
        "audit_description": "Check host resources.",
        "checks": [
            {"check": "Disk Space", "passed": True},
            {"check": "Memory", "passed": False},
        ],
        "passed": False,
    }


def test_str_passed_report(fake_results):
    """The text includes the heading, ordered results, and overall PASS."""
    disk_result = fake_results[0]
    cpu_result = fake_results[2]
    report = AuditReport(
        [disk_result, cpu_result], "host-baseline", "Check host resources."
    )

    text = str(report)

    assert "System Auditor" in text
    assert str(disk_result) in text
    assert str(cpu_result) in text
    assert text.index("Disk Space") < text.index("CPUs")
    assert "OVERALL: PASS" in text
    assert "OVERALL: FAIL" not in text


def test_str_failed_report(fake_results):
    """The text includes every result and an overall FAIL."""
    memory_result = fake_results[1]
    cpu_result = fake_results[2]
    report = AuditReport(
        [memory_result, cpu_result], "host-baseline", "Check host resources."
    )

    text = str(report)

    assert "System Auditor" in text
    assert str(memory_result) in text
    assert str(cpu_result) in text
    assert "OVERALL: FAIL" in text
    assert "OVERALL: PASS" not in text


def main() -> None:
    """Run this module's tests."""
    raise SystemExit(pytest.main([__file__]))


if __name__ == "__main__":
    main()
