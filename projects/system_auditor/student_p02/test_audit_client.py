"""Complete the client tests using fake responses, never network requests."""

import json
import sys

import httpx
import pytest

import audit_client


class FakeResponse:
    """A simple stand-in for an HTTPX response."""

    def __init__(self, status_code, data=None, text=""):
        """Store the status code, JSON data, and body text."""
        self.status_code = status_code
        self.data = data
        self.text = text

    def raise_for_status(self):
        """Raise the same error HTTPX raises for a 4xx or 5xx status."""
        if self.status_code >= 400:
            raise httpx.HTTPStatusError(
                "Simulated HTTP error", request=None, response=self
            )

    def json(self):
        """Return the configured JSON data."""
        return self.data


HOST = {"name": "web01", "url": "http://web01.test:5000"}
DEFINITION = {"audit_id": "a1", "audit_description": "Test audit.", "checks": []}
FAILED_CHECK = {
    "name": "CPUs",
    "description": "At least 4 logical CPUs.",
    "measured": 2.0,
    "requirement": 4,
    "passed": False,
}


def test_audit_failed_policy(monkeypatch):
    """A failed report gives FAIL and sends the URL, definition, and timeout."""
    # TODO: Arrange a fake_post(url, json, timeout) that records its arguments.
    # TODO: Return FakeResponse(200, {"checks": [FAILED_CHECK], "passed": False}).
    # TODO: Patch audit_client.httpx.post before calling the client.
    # TODO: Act by creating AuditClient(HOST) and calling audit(DEFINITION).
    # TODO: Assert the URL, definition, and 5.0-second timeout sent.
    # TODO: Assert the complete host result: name, url, result, checks, error.
    pytest.fail("Complete this test.")


def test_audit_passed_policy(monkeypatch):
    """A passing report gives PASS and preserves the report's checks."""
    # TODO: Arrange a fake response with passed True and a passing check.
    # TODO: Patch audit_client.httpx.post to return that response.
    # TODO: Act by creating an AuditClient and calling audit().
    # TODO: Assert PASS, the report's checks, and error is None.
    pytest.fail("Complete this test.")


def test_audit_connection_error(monkeypatch):
    """A connection failure gives CONNECTION ERROR, no checks, and error text."""
    # TODO: Arrange a fake_post that raises httpx.ConnectError("Connection refused").
    # TODO: Patch audit_client.httpx.post with that fake.
    # TODO: Act by creating an AuditClient and calling audit().
    # TODO: Assert CONNECTION ERROR, checks == [], and error == "Connection refused".
    pytest.fail("Complete this test.")


def test_audit_http_error(monkeypatch):
    """A 500 response gives HTTP ERROR, no checks, and the HTTP error text."""
    # TODO: Arrange FakeResponse(500, text='{"error":"Measurement failed: disk unavailable"}').
    # TODO: Patch audit_client.httpx.post to return that response.
    # TODO: Act by creating an AuditClient and calling audit().
    # TODO: Assert HTTP ERROR, checks == [], and error starting with "HTTP 500".
    pytest.fail("Complete this test.")


def test_main_displays_and_writes_results(tmp_path, monkeypatch, capsys):
    """The CLI displays and saves both hosts' results in hosts-file order."""
    # TODO: Arrange definition and two-host JSON files under tmp_path.
    # TODO: Patch sys.argv with the input paths and an output path.
    # TODO: Patch httpx.post to record requests and return a failed report.
    # TODO: Act by calling audit_client.main().
    # TODO: Assert the output includes each host line and its failed check line.
    # TODO: Read the results file and assert audit_id, host names, URLs, and order.
    # TODO: Assert each host's audit URL and the definition were sent.
    pytest.fail("Complete this test.")


def test_main_usage(monkeypatch, capsys):
    """Wrong arguments print usage without making any HTTP requests."""
    # TODO: Arrange sys.argv with only the program name.
    # TODO: Patch httpx.post with a fake that fails if called.
    # TODO: Act by calling audit_client.main().
    # TODO: Assert the output includes "Usage:" and "audit_client.py".
    pytest.fail("Complete this test.")
