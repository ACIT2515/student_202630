"""Test the command-line interface without inspecting the real computer.

The checks_file fixture in conftest.py writes a three-check policy to a JSON
file in pytest's temporary directory, and fake_system supplies a host with
40 GiB free disk, 16 GiB memory, and 8 logical CPUs.

main() reads its arguments from sys.argv, so each test uses monkeypatch to
replace sys.argv with the command line it wants to simulate.
"""

import json
import sys

import system_auditor_cli
import pytest


def test_main_reads_checks_and_writes_json_report(
    fake_system, checks_file, tmp_path, capsys, monkeypatch
):
    """The program reads the policy, prints a report, and writes JSON."""
    report_file = tmp_path / "report.json"
    monkeypatch.setattr(
        sys, "argv", ["system_auditor_cli.py", str(checks_file), str(report_file)]
    )

    system_auditor_cli.main()

    output = capsys.readouterr().out
    assert "System Auditor" in output
    assert "Description:" in output
    assert "OVERALL: PASS" in output

    report = json.loads(report_file.read_text(encoding="utf-8"))
    assert report == {
        "audit_id": "test-audit",
        "audit_description": "Check the example host against a minimum policy.",
        "checks": [
            {
                "name": "Disk Space",
                "description": "At least 20 GiB of free disk space.",
                "measured": 40.0,
                "requirement": 20,
                "passed": True,
            },
            {
                "name": "Memory",
                "description": "At least 8 GiB of installed memory.",
                "measured": 16.0,
                "requirement": 8,
                "passed": True,
            },
            {
                "name": "CPUs",
                "description": "At least 4 logical CPUs.",
                "measured": 8,
                "requirement": 4,
                "passed": True,
            },
        ],
        "passed": True,
    }


def test_main_handles_invalid_arguments(capsys, monkeypatch):
    """A missing checks file argument prints usage without a report."""
    monkeypatch.setattr(sys, "argv", ["system_auditor_cli.py"])

    system_auditor_cli.main()

    output = capsys.readouterr().out
    assert "Usage:" in output
    assert "system_auditor_cli.py" in output
    assert "OVERALL:" not in output


def test_main_requires_audit_id(checks_file, monkeypatch):
    """An audit without an ID cannot be run."""
    audit = json.loads(checks_file.read_text(encoding="utf-8"))
    del audit["audit_id"]
    checks_file.write_text(json.dumps(audit), encoding="utf-8")
    monkeypatch.setattr(sys, "argv", ["system_auditor_cli.py", str(checks_file)])

    with pytest.raises(KeyError, match="audit_id"):
        system_auditor_cli.main()


def test_main_rejects_invalid_audit_id(checks_file, monkeypatch):
    """An audit ID must be a non-empty string."""
    audit = json.loads(checks_file.read_text(encoding="utf-8"))
    audit["audit_id"] = None
    checks_file.write_text(json.dumps(audit), encoding="utf-8")
    monkeypatch.setattr(sys, "argv", ["system_auditor_cli.py", str(checks_file)])

    with pytest.raises(ValueError, match="audit_id"):
        system_auditor_cli.main()


def test_main_rejects_blank_audit_description(checks_file, monkeypatch):
    """An audit must have a non-empty description."""
    audit = json.loads(checks_file.read_text(encoding="utf-8"))
    audit["audit_description"] = "   "
    checks_file.write_text(json.dumps(audit), encoding="utf-8")
    monkeypatch.setattr(sys, "argv", ["system_auditor_cli.py", str(checks_file)])

    with pytest.raises(ValueError, match="audit_description"):
        system_auditor_cli.main()


def test_main_rejects_a_list_without_audit_metadata(
    fake_system, checks_file, monkeypatch
):
    """A bare checks list is not an audit definition."""
    audit = json.loads(checks_file.read_text(encoding="utf-8"))
    checks_file.write_text(json.dumps(audit["checks"]), encoding="utf-8")
    monkeypatch.setattr(sys, "argv", ["system_auditor_cli.py", str(checks_file)])

    with pytest.raises(ValueError, match="audit object"):
        system_auditor_cli.main()


def test_main_requires_a_checks_list(checks_file, monkeypatch):
    """An invalid checks value must not produce a passing report."""
    audit = json.loads(checks_file.read_text(encoding="utf-8"))
    audit["checks"] = ""
    checks_file.write_text(json.dumps(audit), encoding="utf-8")
    monkeypatch.setattr(sys, "argv", ["system_auditor_cli.py", str(checks_file)])

    with pytest.raises(ValueError, match="checks must be a list"):
        system_auditor_cli.main()


if __name__ == "__main__":
    raise SystemExit(pytest.main([__file__]))
