"""Test the command-line interface without inspecting the real computer.

The checks_file fixture writes a three-check policy to a JSON file in pytest's
temporary directory, and fake_system supplies a host with 40 GiB free disk,
16 GiB memory, and 8 logical CPUs.

main() reads its arguments from sys.argv, so each test uses monkeypatch to
replace sys.argv with the command line it wants to simulate.
"""

import json
import sys

import pytest
import system_auditor_cli


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


def test_main_rejects_invalid_definition(checks_file, capsys, monkeypatch):
    """An invalid audit definition raises an error before any report prints.

    The individual validation rules are tested against Audit in
    test_audit.py; this test confirms that main() uses that validation.
    """
    audit = json.loads(checks_file.read_text(encoding="utf-8"))
    audit["checks"] = ""
    checks_file.write_text(json.dumps(audit), encoding="utf-8")
    monkeypatch.setattr(sys, "argv", ["system_auditor_cli.py", str(checks_file)])

    with pytest.raises(Exception):
        system_auditor_cli.main()
    assert "OVERALL:" not in capsys.readouterr().out
