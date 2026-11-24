"""Tests for the minimal echo server."""

from datetime import datetime

import pytest

from flask import Flask

from demo_server import create_app, main


@pytest.fixture
def client():
    """Return a Flask test client for a new echo server."""
    return create_app().test_client()


def test_echo_adds_timestamp(client):
    """The server echoes the JSON body and adds a timestamp."""
    data = {"host": "web01", "status": "up"}
    response = client.post("/api/echo", json=data)
    assert response.status_code == 200
    assert response.json["received"] == data

    # verify that the response `received_at` is a valid datetime
    # datetime.fromisoformat() will raise an exception if incorrect format 
    datetime.fromisoformat(response.json["received_at"])


def test_echo_rejects_non_json(client):
    """A body that is not JSON returns a 400 error."""
    response = client.post("/api/echo", data="hello")
    assert response.status_code == 400
    assert response.json == {"error": "Request body must be JSON"}


def test_main_starts_configured_app_in_debug_mode(monkeypatch):
    """Direct startup runs the configured app with debug mode enabled."""
    calls = []

    def fake_run(app, *, debug):
        calls.append((app, debug))

    monkeypatch.setattr(Flask, "run", fake_run)
    main()

    assert len(calls) == 1
    app, debug = calls[0]
    assert debug is True
    assert app.test_client().post("/api/echo", json={"host": "web01"}).status_code == 200
