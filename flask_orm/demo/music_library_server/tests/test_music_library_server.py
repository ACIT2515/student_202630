"""Tests for the Music Library Flask application."""

import pytest
from music_library_server import create_app
from seed_data import build_seed_library


@pytest.fixture
def seeded_library():
    """Build a fresh library with sample tracks for each test."""
    return build_seed_library()


@pytest.fixture
def new_track():
    """Return a fresh, valid track request body for a test."""
    return {
        "title": "Clair de Lune",
        "artist": "Claude Debussy",
        "recording": "Suite bergamasque",
        "genre": "classical",
        "released": "1905-01-01",
        "duration": 300,
    }


@pytest.fixture
def app(seeded_library):
    """Create a Flask app that serves the seeded library."""
    app = create_app(seeded_library)

    # TESTING makes Flask propagate exceptions so failures are easier to debug.
    # https://flask.palletsprojects.com/en/stable/config/#TESTING
    app.config["TESTING"] = True
    return app


@pytest.fixture
def client(app):
    """Create a test client that sends requests to the app."""
    # The test client sends requests without starting a live web server.
    # https://flask.palletsprojects.com/en/stable/testing/#sending-requests-with-the-test-client
    return app.test_client()


def test_status(client):
    """The status route reports that the server is online."""
    response = client.get("/api/status")

    # The status endpoint should return a successful response.
    assert response.status_code == 200
    # The response should identify the server as online.
    assert response.json["status"] == "online"
    # The seeded library should contain four tracks.
    assert response.json["track_count"] == 4


def test_list_tracks(client):
    """The tracks route returns the sample tracks as JSON."""
    response = client.get("/api/tracks")

    # Listing tracks should return a successful response.
    assert response.status_code == 200
    # The list should contain every seeded track.
    assert len(response.json) == 4
    # The first returned track should be the first seeded track.
    assert response.json[0]["title"] == "Makeshift Patriot"
    # The API should serialize the release date as ISO-formatted text.
    assert response.json[0]["released"] == "2002-01-01"


def test_get_track(client):
    """The detail route returns the track with the requested ID."""
    response = client.get("/api/tracks/1")

    # A request for an existing track should succeed.
    assert response.status_code == 200
    # The returned track should have the requested ID.
    assert response.json["id"] == 1
    # The returned track should be the seeded track with ID 1.
    assert response.json["title"] == "Makeshift Patriot"


def test_create_track(client, new_track):
    """The create route stores a track and returns its assigned ID."""
    # json= encodes the request body and sets its JSON content type.
    # response.json reads the JSON returned by the Flask test client.
    # https://flask.palletsprojects.com/en/stable/testing/#json-data
    response = client.post("/api/tracks", json=new_track)

    # Creating a track should return the Created status.
    assert response.status_code == 201
    # The response should contain the submitted fields and the next ID.
    assert response.json["track"] == {"id": 5, **new_track}


def test_create_track_reports_all_missing_fields(client):
    """An empty track body reports every missing field."""
    response = client.post("/api/tracks", json={})

    # A request missing fields should be rejected as a client error.
    assert response.status_code == 400
    # The response should identify the missing-fields error.
    assert response.json["error"] == "Missing required fields"
    # Every required field should be reported, in the defined order.
    assert response.json["missing_fields"] == [
        "title",
        "artist",
        "recording",
        "genre",
        "released",
        "duration",
    ]
    # The response should help the client construct a complete request.
    assert response.json["hint"].startswith("Send JSON with every field")
    # Rejecting an incomplete create request must not add a track.
    assert client.get("/api/status").json["track_count"] == 4


def test_create_track_reports_multiple_missing_fields(client, new_track):
    """A partial track body reports only the fields that are missing."""
    del new_track["artist"]
    del new_track["duration"]

    response = client.post("/api/tracks", json=new_track)

    # A request missing fields should be rejected as a client error.
    assert response.status_code == 400
    # The response should list only the fields omitted from this request.
    assert response.json["missing_fields"] == ["artist", "duration"]
    # Rejecting an incomplete create request must not add a track.
    assert client.get("/api/status").json["track_count"] == 4

# The following tests a list of parameters and uses parameterize
# https://docs.pytest.org/en/stable/how-to/parametrize.html#parametrize-basics
@pytest.mark.parametrize(
    "field, value, message",
    [
        ("title", "", "title must be a non-empty string"),
        ("artist", "   ", "artist must be a non-empty string"),
        ("genre", 5, "genre must be a non-empty string"),
        ("released", "2024-02-30", "released must use YYYY-MM-DD format"),
        ("released", None, "released must use YYYY-MM-DD format"),
        ("duration", 0, "duration must be a number greater than zero"),
        ("duration", "300", "duration must be a number greater than zero"),
        ("duration", True, "duration must be a number greater than zero"),
    ],
)
def test_create_track_rejects_invalid_values(
    client, new_track, field, value, message
):
    """The create route returns 400 when a value is invalid."""
    new_track[field] = value

    response = client.post("/api/tracks", json=new_track)

    # Invalid values must be rejected with a client error.
    assert response.status_code == 400
    # The message confirms which validation rule rejected the value.
    assert response.json["error"] == message
    # A rejected request must not add a track to the library.
    assert client.get("/api/status").json["track_count"] == 4


def test_update_track_replaces_every_field(client, new_track):
    """The update route replaces every field and keeps the track's ID."""
    response = client.put("/api/tracks/1", json=new_track)

    # Replacing an existing track should return a successful response.
    assert response.status_code == 200
    # The response should contain all submitted fields and preserve the ID.
    assert response.json["track"] == {"id": 1, **new_track}
    # A follow-up read should confirm the replacement was stored.
    assert client.get("/api/tracks/1").json == {"id": 1, **new_track}


def test_update_track_requires_every_field(client):
    """A partial update is rejected and the track is unchanged."""
    original_track = client.get("/api/tracks/1").json
    response = client.put("/api/tracks/1", json={"genre": "jazz"})

    # A partial PUT should be rejected as a client error.
    assert response.status_code == 400
    # The response should identify the missing-fields error.
    assert response.json["error"] == "Missing required fields"
    # The error should list all required fields omitted from the request.
    assert response.json["missing_fields"] == [
        "title",
        "artist",
        "recording",
        "released",
        "duration",
    ]
    # A rejected partial update must leave the stored track unchanged.
    assert client.get("/api/tracks/1").json == original_track


def test_update_track_with_invalid_value_changes_nothing(client, new_track):
    """A rejected update leaves every field of the track unchanged."""
    new_track["duration"] = -1

    response = client.put("/api/tracks/1", json=new_track)

    # An update with an invalid duration should be rejected.
    assert response.status_code == 400
    # The response should explain why the duration was invalid.
    assert response.json["error"] == "duration must be a number greater than zero"
    # A rejected update must leave the existing track unchanged.
    assert client.get("/api/tracks/1").json["title"] == "Makeshift Patriot"


def test_update_missing_track(client, new_track):
    """Updating a track that does not exist returns a JSON 404."""
    response = client.put("/api/tracks/99", json=new_track)

    # Updating an unknown ID should return Not Found.
    assert response.status_code == 404
    # The response should identify the requested ID as missing.
    assert response.json == {"error": "Track 99 not found"}


def test_delete_track(client):
    """The delete route removes the requested track."""
    response = client.delete("/api/tracks/1")

    # Deleting an existing track should succeed.
    assert response.status_code == 200
    # The response should identify which track was deleted.
    assert response.json["deleted_track"]["id"] == 1
    # A follow-up lookup should confirm the track was removed.
    assert client.get("/api/tracks/1").status_code == 404


def test_get_missing_track(client):
    """Requesting a track that does not exist returns a JSON 404."""
    response = client.get("/api/tracks/99")

    # Looking up an unknown ID should return Not Found.
    assert response.status_code == 404
    # The response should identify the requested ID as missing.
    assert response.json == {"error": "Track 99 not found"}


def test_create_with_malformed_json(client):
    """Sending malformed JSON to the create route returns a JSON 400."""
    response = client.post(
        "/api/tracks",
        data="{",
        content_type="application/json",
    )

    # Malformed JSON should be rejected as a client error.
    assert response.status_code == 400
    # The response should explain that a JSON body is required.
    assert response.json["error"] == "Request body must be JSON"