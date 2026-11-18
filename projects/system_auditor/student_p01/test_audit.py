"""Test Audit without inspecting the real computer."""

from types import SimpleNamespace

import audit as audit_module
import pytest
from audit import Audit


class FakeCheck:
    """Return a configured result without running a system check."""

    def __init__(self, specification: dict, result: object) -> None:
        """Store the specification and predetermined result."""
        self.specification = specification
        self.result = result

    def run(self) -> object:
        """Return the configured result."""
        return self.result


class FakeAuditReport:
    """Stand in for AuditReport and retain the values passed by Audit."""

    def __init__(self, results, audit_id, audit_description) -> None:
        """Store the values supplied by Audit."""
        self.results = results
        self.audit_id = audit_id
        self.audit_description = audit_description


@pytest.fixture
def created_fake_checks(monkeypatch) -> list[FakeCheck]:
    """Replace create_check() and collect the fake checks it creates."""
    fake_checks: list[FakeCheck] = []
    fake_results = {
        "disk": SimpleNamespace(name="Disk Space", passed=False),
        "memory": SimpleNamespace(name="Memory", passed=True),
        "cpu": SimpleNamespace(name="CPUs", passed=True),
    }

    def create_fake_check(specification: dict) -> FakeCheck:
        """Create a fake check with a predetermined result."""
        check = FakeCheck(specification, fake_results[specification["type"]])
        fake_checks.append(check)
        return check

    monkeypatch.setattr(audit_module, "create_check", create_fake_check)
    return fake_checks


@pytest.fixture
def fake_audit_report(monkeypatch) -> None:
    """Replace AuditReport in audit.py with FakeAuditReport."""
    monkeypatch.setattr(audit_module, "AuditReport", FakeAuditReport)


def make_definition() -> dict:
    """Return an audit dictionary matching a parsed JSON definition."""
    return {
        "audit_id": "test-audit",
        "audit_description": "Check the example host against a minimum policy.",
        "checks": [
            {
                "type": "disk",
                "requirement": 20,
                "description": "At least 20 GiB of free disk space.",
            },
            {
                "type": "cpu",
                "requirement": 4,
                "description": "At least 4 logical CPUs.",
            },
        ],
    }


def test_audit_runs_checks_and_builds_report(
    created_fake_checks, fake_audit_report
):
    """Pass all check results and audit identity to the report."""
    audit = Audit(make_definition())

    report = audit.run()

    assert isinstance(report, FakeAuditReport)
    assert report.results == [
        created_fake_checks[0].result,
        created_fake_checks[1].result,
    ]
    assert report.results[0].passed is False
    assert report.results[1].passed is True
    assert report.audit_id == "test-audit"
    assert report.audit_description == (
        "Check the example host against a minimum policy."
    )


def test_audit_builds_checks_from_definition(created_fake_checks):
    """Create one fake check for each specification."""
    definition = make_definition()
    audit = Audit(definition)

    assert audit.audit_id == "test-audit"
    assert audit.audit_description == (
        "Check the example host against a minimum policy."
    )
    assert len(created_fake_checks) == 2
    assert created_fake_checks[0].specification == definition["checks"][0]
    assert created_fake_checks[1].specification == definition["checks"][1]
    assert audit.checks == created_fake_checks


def test_audit_requires_audit_id():
    """An audit without an ID cannot be created."""
    definition = make_definition()
    del definition["audit_id"]

    with pytest.raises(Exception):
        Audit(definition)


def test_audit_rejects_blank_audit_description():
    """An audit must have a non-empty description."""
    definition = make_definition()
    definition["audit_description"] = "   "

    with pytest.raises(Exception):
        Audit(definition)


def test_audit_requires_populated_checks_list():
    """An invalid checks value must not produce an audit."""
    definition = make_definition()
    definition["checks"] = ""

    with pytest.raises(Exception):
        Audit(definition)
