"""Unit tests for MusicLibraryClient without a running server."""

import pytest

# Note the renaming of the import
import client as client_module


class FakeResponse:
    """A simple stand-in for an HTTPX response."""

    def __init__(self, status_code: int, data=None):
        """Store the status code and optional JSON data."""
        self.status_code = status_code
        self.data = data

    def raise_for_status(self):
        """Simulate an HTTP error for a non-success status."""
        if self.status_code < 200 or self.status_code >= 300:
            raise RuntimeError("Simulated HTTP error")

    def json(self):
        """Return the configured JSON data."""
        if self.data is None:
            raise AssertionError("No fake JSON data was provided")
        return self.data


class FakeHTTPClient:
    """Record requests and return fake responses without network access."""

    def __init__(self):
        """Start with no response or recorded request."""
        self.base_url = None
        self.timeout = None
        self.response: FakeResponse | None = None
        self.last_request = None
        self.closed = False

    def _request(self, method: str, path: str, body=None) -> FakeResponse:
        """Record a request and return the configured response."""
        if self.response is None:
            raise AssertionError("Set a fake response before making a request")
        self.last_request = (method, path, body)
        return self.response

    def get(self, path: str) -> FakeResponse:
        """Record a GET request."""
        return self._request("GET", path)

    def post(self, path: str, json) -> FakeResponse:
        """Record a POST request and its JSON body."""
        return self._request("POST", path, json)

    def put(self, path: str, json) -> FakeResponse:
        """Record a PUT request and its JSON body."""
        return self._request("PUT", path, json)

    def delete(self, path: str) -> FakeResponse:
        """Record a DELETE request."""
        return self._request("DELETE", path)

    def close(self):
        """Record that the fake client was closed."""
        self.closed = True


@pytest.fixture
def fake_http():
    """Create a fresh fake HTTP client for each test."""
    return FakeHTTPClient()


@pytest.fixture
def music_client(monkeypatch, fake_http):
    """Create a MusicLibraryClient that uses the fake HTTP client."""
    def make_fake_client(base_url, timeout):
        fake_http.base_url = base_url
        fake_http.timeout = timeout
        return fake_http

    # Replace the HTTPX constructor before creating the music client.
    # Pytest restores the original constructor after the test.
    # https://docs.pytest.org/en/stable/how-to/monkeypatch.html
    monkeypatch.setattr(client_module.httpx, "Client", make_fake_client)
    return client_module.MusicLibraryClient(server_url="http://music.test")


@pytest.fixture
def track_data():
    """Provide fresh track fields in the API's JSON format."""
    return {
        "title": "So What",
        "artist": "Miles Davis",
        "recording": "Kind of Blue",
        "genre": "jazz",
        "released": "1959-08-17",
        "duration": 545,
    }


def test_status_and_length(music_client, fake_http):
    """Status and length use the server's status response."""
    status = {"status": "online", "track_count": 2}
    fake_http.response = FakeResponse(200, status)

    # The supplied server URL is passed to the HTTP client.
    assert fake_http.base_url == "http://music.test"
    # Status returns the JSON response.
    assert music_client.status() == status
    # Status sends a GET request to the status endpoint.
    assert fake_http.last_request == ("GET", "/api/status", None)
    fake_http.last_request = None
    # len(client) returns the track count from the status response.
    assert len(music_client) == 2
    # len(client) makes its own request for the current status.
    assert fake_http.last_request == ("GET", "/api/status", None)


def test_list_tracks(music_client, fake_http, track_data):
    """Listing tracks returns the server's JSON list."""
    # Unpack the track fields into the dictionary and add the track ID.
    tracks = [{"id": 1, **track_data}]
    fake_http.response = FakeResponse(200, tracks)

    # The client returns the list received from the server.
    assert music_client.list_tracks() == tracks
    # The list request uses the tracks endpoint.
    assert fake_http.last_request == ("GET", "/api/tracks", None)


def test_get_track(music_client, fake_http, track_data):
    """Getting an existing track returns its JSON data."""
    # Unpack the track fields into the dictionary and add the track ID.
    track = {"id": 5, **track_data}
    fake_http.response = FakeResponse(200, track)

    # The client returns the requested track.
    assert music_client.get_track(5) == track
    # The track ID is included in the requested URL.
    assert fake_http.last_request == ("GET", "/api/tracks/5", None)


def test_get_missing_track(music_client, fake_http):
    """Getting a missing track returns None."""
    fake_http.response = FakeResponse(404)

    # A 404 is represented as None instead of an exception.
    assert music_client.get_track(99) is None

    # The client still requests the specified ID.
    assert fake_http.last_request == ("GET", "/api/tracks/99", None)


def test_create_track(music_client, fake_http, track_data):
    """Creating a track sends every field and returns the created track."""

    # Unpack the track fields into the dictionary and add the track ID.
    track = {"id": 5, **track_data}
    fake_http.response = FakeResponse(201, {"track": track, "message": "created"})

    # Unpack the track fields in the create_track function call.
    created = music_client.create_track(**track_data)

    # POST sends the complete track data as JSON.
    assert fake_http.last_request == ("POST", "/api/tracks", track_data)
    # The client returns the track inside the response, including its ID.
    assert created == track


def test_update_track(music_client, fake_http, track_data):
    """Updating a track sends every field and returns the replacement."""

    # Unpack the track fields into the dictionary and add the track ID.
    track = {"id": 5, **track_data}
    fake_http.response = FakeResponse(200, {"track": track, "message": "updated"})

    updated = music_client.update_track(5, **track_data)

    # PUT sends all fields to the URL for the selected track.
    assert fake_http.last_request == ("PUT", "/api/tracks/5", track_data)
    # The client returns the updated track from the response.
    assert updated == track


def test_update_missing_track(music_client, fake_http, track_data):
    """Updating a missing track returns None."""
    fake_http.response = FakeResponse(404)

    # A 404 is represented as None.
    # Unpack the track fields into a dictionary and use them as the data for an update
    assert music_client.update_track(99, **track_data) is None
    # The request still includes the ID and complete track data.
    assert fake_http.last_request == ("PUT", "/api/tracks/99", track_data)


def test_delete_track(music_client, fake_http):
    """Deleting an existing track returns True."""
    fake_http.response = FakeResponse(200)

    # A successful deletion returns True.
    assert music_client.delete_track(5) is True
    # DELETE targets the selected track.
    assert fake_http.last_request == ("DELETE", "/api/tracks/5", None)


def test_delete_missing_track(music_client, fake_http):
    """Deleting a missing track returns False."""
    fake_http.response = FakeResponse(404)

    # A 404 returns False rather than raising an exception.
    assert music_client.delete_track(99) is False
    # The request targets the missing track's ID.
    assert fake_http.last_request == ("DELETE", "/api/tracks/99", None)


def test_other_http_errors_are_raised(music_client, fake_http, track_data):
    """Unexpected HTTP errors are passed to the caller."""
    fake_http.response = FakeResponse(500)

    # The fake uses RuntimeError; HTTPX uses httpx.HTTPStatusError.
    with pytest.raises(RuntimeError, match="Simulated HTTP error"):
        music_client.status()
    # Listing tracks must not hide a server error.
    with pytest.raises(RuntimeError, match="Simulated HTTP error"):
        music_client.list_tracks()
    # Getting a track must not treat a server error as a 404.
    with pytest.raises(RuntimeError, match="Simulated HTTP error"):
        music_client.get_track(5)
    # Creating a track must pass a server error to the caller.
    with pytest.raises(RuntimeError, match="Simulated HTTP error"):
        music_client.create_track(**track_data)
    # Updating a track must not treat a server error as a 404.
    with pytest.raises(RuntimeError, match="Simulated HTTP error"):
        music_client.update_track(5, **track_data)
    # Deleting a track must not report success after a server error.
    with pytest.raises(RuntimeError, match="Simulated HTTP error"):
        music_client.delete_track(5)


def test_close(music_client, fake_http):
    """Closing the music client closes its HTTP client."""
    music_client.close()

    # The close call reaches the underlying HTTP client.
    assert fake_http.closed is True


def test_context_manager_closes_client(music_client, fake_http):
    """A with-block returns the client and closes it afterward."""
    with music_client as opened_client:
        # __enter__ returns the same client for use inside the block.
        assert opened_client is music_client
        # The HTTP client stays open while the block is running.
        assert fake_http.closed is False

    # __exit__ closes the HTTP client when the block finishes.
    assert fake_http.closed is True


def test_context_manager_closes_after_error(music_client, fake_http):
    """A with-block closes the client and does not suppress exceptions."""
    # The error raised inside the block must reach the caller.
    with pytest.raises(ValueError, match="Error in with-block"):
        with music_client:
            raise ValueError("Error in with-block")

    # The HTTP client is closed even when the block raises an error.
    assert fake_http.closed is True

