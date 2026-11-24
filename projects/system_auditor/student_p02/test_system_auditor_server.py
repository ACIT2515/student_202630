"""Complete the server fixtures and tests without starting a live server."""

import pytest

import checks
from system_auditor_server import create_app


# TODO: Create app(fake_system), client(app), and definition fixtures here.
# Use the music library server tests as a model.


def test_status(client):
    """GET /api/status returns 200 and {"status": "online"}."""
    # TODO: Arrange the status request.
    # TODO: Act by sending the request with the Flask test client.
    # TODO: Assert the status code and complete JSON response.
    pytest.fail("Complete this test.")


def test_audit_passed(client, definition):
    """A passing audit returns 200 and the complete expected report."""
    # TODO: Arrange a definition whose three checks pass the fake measurements.
    # TODO: Act by posting the definition as JSON to /api/audit.
    # TODO: Assert 200 and the complete report, including every check field.
    pytest.fail("Complete this test.")


def test_audit_failed_is_200(client, definition):
    """A policy failure returns 200, passed false, and all three checks."""
    # TODO: Arrange one requirement above its fake measurement.
    # TODO: Act by posting the definition.
    # TODO: Assert 200, overall and individual failure, and all three checks.
    pytest.fail("Complete this test.")


def test_audit_requires_json(client):
    """A non-JSON body returns 400 and the required error message."""
    # TODO: Arrange a body containing "not json".
    # TODO: Act by posting it with data= rather than json=.
    # TODO: Assert 400 and {"error": "Request body must be JSON"}.
    pytest.fail("Complete this test.")


@pytest.mark.parametrize("missing_key", ["audit_id", "checks"])
def test_audit_invalid_definition(client, definition, missing_key):
    """A missing required key returns 400 and an invalid-definition error."""
    # TODO: Arrange by removing missing_key from the definition.
    # TODO: Act by posting the definition.
    # TODO: Assert 400 and an error starting with "Invalid audit definition".
    pytest.fail("Complete this test.")


def test_audit_unknown_check_type(client, definition):
    """An unknown check type returns 400."""
    # TODO: Arrange a check with type "gpu".
    # TODO: Act by posting the definition.
    # TODO: Assert 400 and an invalid-definition error.
    pytest.fail("Complete this test.")


def test_audit_measurement_error(client, definition, monkeypatch):
    """A failed measurement returns 500 and the measurement error text."""
    # TODO: Arrange a fake disk_usage that raises OSError("disk unavailable").
    # TODO: Patch checks.psutil.disk_usage with that fake.
    # TODO: Act by posting the definition.
    # TODO: Assert 500 and {"error": "Measurement failed: disk unavailable"}.
    pytest.fail("Complete this test.")
