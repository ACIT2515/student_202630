"""Test SystemAuditor without inspecting the real computer."""

import pytest

import checks
from audit import Audit
from audit_report import AuditReport
from system_auditor import SystemAuditor


def test_auditor_runs_all_checks_and_reports_failure(fake_system):
    """Every check runs in order, even after a failure, and the report fails."""
    audit = Audit(
        [
            checks.DiskCheck(41, "At least 41 GiB of free disk space."),
            checks.MemoryCheck(8, "At least 8 GiB of installed memory."),
            checks.CPUCheck(4, "At least 4 logical CPUs."),
        ],
        "test-audit",
        "Check the example host against a minimum policy.",
    )
    auditor = SystemAuditor(audit)

    report = auditor.run()

    assert isinstance(report, AuditReport)
    assert len(report.results) == 3
    assert report.results[0].name == "Disk Space"
    assert report.results[0].passed is False
    assert report.results[1].name == "Memory"
    assert report.results[1].passed is True
    assert report.results[2].name == "CPUs"
    assert report.results[2].passed is True
    assert report.passed is False
    assert report.audit_id == "test-audit"
    assert report.audit_description == (
        "Check the example host against a minimum policy."
    )


def test_auditor_reuses_definition_with_fresh_measurements(fake_system, monkeypatch):
    """Reusing an audit produces new results without changing earlier reports."""
    audit = Audit(
        [checks.CPUCheck(4, "At least 4 logical CPUs.")],
        "cpu-audit",
        "Check the logical CPU count.",
    )
    auditor = SystemAuditor(audit)
    first_report = auditor.run()

    def cpu_count():
        """Return fewer CPUs for the second run."""
        return 2

    monkeypatch.setattr(checks.psutil, "cpu_count", cpu_count)
    second_report = auditor.run()

    assert first_report.passed is True
    assert first_report.results[0].measured == 8
    assert second_report.passed is False
    assert second_report.results[0].measured == 2
    assert first_report.audit_id == second_report.audit_id == audit.audit_id
    assert second_report.audit_description == audit.audit_description


if __name__ == "__main__":
    raise SystemExit(pytest.main([__file__]))
