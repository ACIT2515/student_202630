# Testing Flask Applications with pytest

An automated test describes what code should do and checks that it does it.
Pytest finds and runs the tests and reports any failures. Flask provides a
test client that sends requests to an application without starting a server.

These notes explain the main techniques using the test suites from the
minimal echo server and the music library server. Imports and fixtures are not
repeated in every excerpt.

## What the Tests Cover

A unit test checks one part of a program, such as a class, on its own. An
integration test checks several parts working together. The `Track` tests are
unit tests. A request to the music API is an integration test: it runs the
routing, validation, library, and JSON conversion together.

Neither kind needs a running server or a network. Flask's test client calls
the application directly, and a fake HTTPX client records outgoing requests
instead of sending them. A real network connection is not part of these tests.

| Test suite                                                                            | What it tests                                     | Concepts it uses                                                          |
| ------------------------------------------------------------------------------------- | ------------------------------------------------- | ------------------------------------------------------------------------- |
| [Echo server tests](../demo/flask_minimal_demo/test_demo_server.py)                   | The echo route and the `main()` startup function. | Fixtures, the Flask test client, assertions, `monkeypatch`.               |
| [Track tests](../demo/music_library_server/tests/test_track.py)                       | `Track` values and validation.                    | Unit tests, fixtures, `pytest.raises`, parametrized tests.                |
| [Library tests](../demo/music_library_server/tests/test_library.py)                   | Storing tracks and assigning IDs.                 | Unit tests, a fake class, `monkeypatch`, identity checks with `is`.       |
| [Music server tests](../demo/music_library_server/tests/test_music_library_server.py) | Every HTTP route, with a real in-memory library.  | Integration tests, fixtures that use fixtures, `TESTING`, checking state. |
| [Music client tests](../demo/music_library_server/tests/test_client.py)               | The HTTPX-based `MusicLibraryClient`.             | Fakes that record calls, `monkeypatch`, error handling, cleanup.          |

### References

- [pytest: Get started](https://docs.pytest.org/en/stable/getting-started.html)
- [Flask: Testing Flask applications](https://flask.palletsprojects.com/en/stable/testing/)

## Running Tests

Pytest finds tests by name: files named `test_*.py` that contain functions
named `test_*`. This command, run from either project folder, runs the suite:

```powershell
uv run python -m pytest -q
```

`uv run` uses the project's environment, and `-q` gives a shorter report. A
test fails when an assertion is false or an unexpected exception is raised.
Pytest then exits with a nonzero status, so scripts and automated build tools
can detect the failure.

A run can be narrowed to a file or a single test. These commands run from the
[music library folder](../demo/music_library_server/):

```powershell
# List the tests without running them
uv run python -m pytest --collect-only -q
# Run one file
uv run python -m pytest -q tests\test_music_library_server.py
# Run one test
uv run python -m pytest -q tests\test_track.py::test_duration_must_be_a_positive_number
```

### Pytest Configuration

The music project's [settings: `pyproject.toml`](../demo/music_library_server/pyproject.toml)
tell pytest where to look. `testpaths = ["tests"]` makes pytest search the
`tests` folder when no path is given. `pythonpath = ["."]` adds the project
folder to Python's import path, so test files can import modules such as
`track`. The echo project needs neither setting because its test file sits
beside the code it tests.

### References

- [pytest: Invoking pytest](https://docs.pytest.org/en/stable/how-to/usage.html)
- [pytest: Test discovery](https://docs.pytest.org/en/stable/explanation/goodpractices.html#conventions-for-python-test-discovery)
- [pytest: Configuration](https://docs.pytest.org/en/stable/reference/customize.html)
- [Flask: Identifying tests](https://flask.palletsprojects.com/en/stable/testing/#identifying-tests)

## Fixtures and the Flask Test Client

A fixture is a function marked with `@pytest.fixture` that prepares something
a test needs. A test requests a fixture by using its name as a parameter.
Pytest calls the fixture and passes the result in. Fixtures can request other
fixtures in the same way.

The [echo tests](../demo/flask_minimal_demo/test_demo_server.py) need only a
test client:

```python
import pytest

from demo_server import create_app


@pytest.fixture
def client():
    """Return a Flask test client for a new echo server."""
    return create_app().test_client()
```

`create_app()` is the application factory, and `test_client()` returns an
object with `get`, `post`, `put`, and `delete` methods. Each method passes a
request to the application and returns its response. No server starts and no
port opens.

The [music server tests](../demo/music_library_server/tests/test_music_library_server.py)
build the client from a chain of fixtures:

```python
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
    app.config["TESTING"] = True
    return app


@pytest.fixture
def client(app):
    """Create a test client that sends requests to the app."""
    return app.test_client()
```

A test that requests `client` causes pytest to build `seeded_library`, then
`app`, then `client`. The library starts with four tracks, with IDs 1 to 4.
`new_track` supplies a valid request body.

Pytest creates fixtures again for every test, including every parametrized
case. This keeps tests isolated: a track deleted in one test is still present
in the next, and the tests pass in any order. Within one test, each fixture is
created only once, so the test and its fixtures share the same objects. The
application factory makes this possible, because each test gets its own app
around its own library.

`app.config["TESTING"] = True` makes unexpected errors easier to find. An
unhandled exception in a view reaches pytest with its traceback instead of
becoming a generic 500 response.

### References

- [pytest: Fixtures](https://docs.pytest.org/en/stable/how-to/fixtures.html)
- [Flask: Test fixtures](https://flask.palletsprojects.com/en/stable/testing/#fixtures)
- [Flask: Sending requests with the test client](https://flask.palletsprojects.com/en/stable/testing/#sending-requests-with-the-test-client)
- [Flask: `TESTING` configuration](https://flask.palletsprojects.com/en/stable/config/#TESTING)

## Testing Routes

Most tests follow three steps:

1. Arrange: prepare the objects and input data.
1. Act: perform the operation being tested.
1. Assert: check the result.

For a Flask route, the action is a request sent through the test client. A
route test checks:

- the status code
- the response body
- any change to stored data

These echo tests check a successful request and a rejected one:

```python
from datetime import datetime


def test_echo_adds_timestamp(client):
    """The server echoes the JSON body and adds a timestamp."""
    data = {"host": "web01", "status": "up"}
    response = client.post("/api/echo", json=data)

    assert response.status_code == 200
    assert response.json["received"] == data
    datetime.fromisoformat(response.json["received_at"])


def test_echo_rejects_non_json(client):
    """A body that is not JSON returns a 400 error."""
    response = client.post("/api/echo", data="hello")

    assert response.status_code == 400
    assert response.json == {"error": "Request body must be JSON"}
```

`assert` checks a condition. When the condition is false, the test fails and
pytest shows the values involved. `response.status_code` is the HTTP status as
an integer, and `response.json` is the decoded JSON body.

The request arguments matter. `json=data` encodes the dictionary as JSON and
sets the JSON content type. `data="hello"` sends plain text, which the route
rejects. The timestamp changes on every run, so the first test only checks
that it can be parsed. `datetime.fromisoformat()` raises an exception, and
the test fails, if it cannot.

Some GET routes read query parameters from the URL instead of reading a
request body. Pass a dictionary to the test client's `query_string=` argument
to send those parameters. Flask adds them to the URL, just as HTTPX's
`params=` argument does for a real client request. The test below assumes
`definition` is a fixture that returns a valid audit definition:

```python
import json


def test_audit_uses_query_definition(client, definition):
    """The audit route accepts its definition in the query string."""
    response = client.get(
        "/api/audit",
        query_string={"definition": json.dumps(definition)},
    )

    assert response.status_code == 200
    assert response.json["audit_id"] == definition["audit_id"]
```

The test client encodes the dictionary as URL query parameters; it does not
send a JSON body. No server starts and no network request is made.

The music API has more routes. Its tests check these results:

| Request                | Expected result in the music tests                          |
| ---------------------- | ----------------------------------------------------------- |
| `GET /api/status`      | `200`, with a count of four seeded tracks.                  |
| `GET /api/tracks`      | `200`, with a list of the seeded tracks.                    |
| `GET /api/tracks/1`    | `200`, with track 1 as a dictionary.                        |
| `GET /api/tracks/99`   | `404`, with a JSON error for the missing track.             |
| `POST /api/tracks`     | `201` for a valid new track; `400` for invalid input.       |
| `PUT /api/tracks/1`    | `200` for a valid replacement; `400` for an incomplete one. |
| `DELETE /api/tracks/1` | `200` when the track is removed.                            |

A creation test compares the returned track with the data it sent:

```python
def test_create_track(client, new_track):
    """The create route stores a track and returns its assigned ID."""
    response = client.post("/api/tracks", json=new_track)

    assert response.status_code == 201
    assert response.json["track"] == {"id": 5, **new_track}
```

`{"id": 5, **new_track}` builds a dictionary with the new ID and every field
from `new_track`. The ID is 5 because the fresh seed holds IDs 1 to 4.

A request that changes data can be checked with a second request that reads
it back. That read shows whether the change happened, or that a rejected
request left the data alone:

```python
def test_update_track_requires_every_field(client):
    """A partial update is rejected and the track is unchanged."""
    original_track = client.get("/api/tracks/1").json
    response = client.put("/api/tracks/1", json={"genre": "jazz"})

    assert response.status_code == 400
    assert response.json["error"] == "Missing required fields"
    assert client.get("/api/tracks/1").json == original_track


def test_delete_track(client):
    """The delete route removes the requested track."""
    response = client.delete("/api/tracks/1")

    assert response.status_code == 200
    assert response.json["deleted_track"]["id"] == 1
    assert client.get("/api/tracks/1").status_code == 404
```

Bad input takes several forms: a body that is not JSON, broken JSON, missing
fields, or invalid values. Each one is a separate case. The `json` argument
always produces valid JSON, so this test uses `data` and `content_type` to
send broken JSON on purpose:

```python
def test_create_with_malformed_json(client):
    """Sending malformed JSON to the create route returns a JSON 400."""
    response = client.post(
        "/api/tracks",
        data="{",
        content_type="application/json",
    )

    assert response.status_code == 400
    assert response.json["error"] == "Request body must be JSON"
```

The music views return JSON errors. Flask's own errors, for a URL that matches
no route or a method the route does not allow, are HTML 404 and 405 pages.

### References

- [pytest: Assertions](https://docs.pytest.org/en/stable/how-to/assert.html)
- [Flask: Sending requests with the test client](https://flask.palletsprojects.com/en/stable/testing/#sending-requests-with-the-test-client)
- [Flask: JSON data](https://flask.palletsprojects.com/en/stable/testing/#json-data)
- [Python: `datetime.fromisoformat()`](https://docs.python.org/3/library/datetime.html#datetime.datetime.fromisoformat)

## Expected Exceptions and Parametrized Tests

Sometimes raising an exception is the correct result. `pytest.raises` runs
the code in its `with` block and passes only if that block raises the named
exception. Its `match` argument also checks the exception message, using a
regular expression.

`pytest.mark.parametrize` runs one test function once for each set of
values. Each run is reported as a separate test.

The [track tests](../demo/music_library_server/tests/test_track.py) use both:

```python
@pytest.mark.parametrize("value", [0, -1, "545", True])
def test_duration_must_be_a_positive_number(track, value):
    """Zero, negative, text, and boolean durations are invalid."""
    with pytest.raises(ValueError, match="duration must be a number greater than zero"):
        track.duration = value

    assert track.duration == 545
```

Each value gets a fresh `track` fixture. The `with` block checks the error,
and the assertion after it checks that the bad value was not stored.

With several parameter names, each case can carry its input and its expected
result. This shortened test from the music server suite gives each invalid
value its expected error message:

```python
@pytest.mark.parametrize(
    "field, value, message",
    [
        ("title", "", "title must be a non-empty string"),
        ("released", "2024-02-30", "released must use YYYY-MM-DD format"),
        ("duration", True, "duration must be a number greater than zero"),
    ],
)
def test_create_track_rejects_invalid_values(
    client, new_track, field, value, message
):
    """The create route returns 400 when a value is invalid."""
    new_track[field] = value
    response = client.post("/api/tracks", json=new_track)

    assert response.status_code == 400
    assert response.json["error"] == message
    assert client.get("/api/status").json["track_count"] == 4
```

The same rule is checked differently at each level. Setting a bad duration
on a `Track` raises `ValueError`, so the class test expects an exception. The
Flask view catches that error and returns a 400 response, so the API test
expects a response.

### References

- [pytest: Parametrizing tests](https://docs.pytest.org/en/stable/how-to/parametrize.html)
- [pytest: Assertions about exceptions](https://docs.pytest.org/en/stable/how-to/assert.html#assertions-about-expected-exceptions)
- [Flask: Handling application errors](https://flask.palletsprojects.com/en/stable/errorhandling/)

## Fakes and monkeypatch

A fake is a small stand-in for a real dependency. It provides only the
attributes and methods the code under test uses. This lets a unit test check
one class without depending on another.

`monkeypatch` is a built-in pytest fixture for temporary changes.
`monkeypatch.setattr(target, name, replacement)` replaces an attribute, and
pytest puts the original back after the test, even when the test fails.

The [track tests](../demo/music_library_server/tests/test_track.py) already
check `Track` validation. The
[library tests](../demo/music_library_server/tests/test_library.py) replace
`Track` with a `FakeTrack` that stores values without checking them:

```python
import pytest

import music_library


class FakeTrack:
    """Store track fields without validating them."""

    def __init__(self, id, title, artist, recording, genre, released, duration):
        """Store the values supplied by the library."""
        self.id = id
        self.title = title
        self.artist = artist
        self.recording = recording
        self.genre = genre
        self.released = released
        self.duration = duration


@pytest.fixture
def library(monkeypatch):
    """Create an empty library that uses FakeTrack."""
    monkeypatch.setattr(music_library, "Track", FakeTrack)
    return music_library.MusicLibrary()
```

A patch must replace the name the code actually looks up. `music_library.py`
runs `from track import Track`, so the library uses `music_library.Track`.
Patching `track.Track` would not affect it.

With the fake in place, this test checks only the library's own work:

```python
def test_add_tracks(library, track_data):
    """Adding tracks assigns IDs and stores the supplied values."""
    first = library.add(**track_data)
    second = library.add(**track_data)

    assert first.id == 1
    assert second.id == 2
    assert library.get(first.id) is first
    assert library.all_tracks() == [first, second]
    assert len(library) == 2
```

`**track_data` passes the dictionary entries as named arguments. In this file,
the `track_data` fixture uses a Python `date`, because the library works with
`date` objects. `is` checks that `get()` returns the same object that was
added, not just an equal one.

A replacement can also force an error that is hard to cause otherwise. Here,
the constructor is replaced with a function that always raises:

```python
def reject_track(*_arguments, **_keyword_arguments):
    """Simulate a Track constructor rejecting its input."""
    raise ValueError("Simulated invalid track")


def test_failed_update_leaves_track_unchanged(library, track_data, monkeypatch):
    """A failed replacement leaves the original track in the library."""
    original = library.add(**track_data)
    replacement_data = track_data.copy()
    replacement_data["title"] = "All Blues"
    monkeypatch.setattr(music_library, "Track", reject_track)

    with pytest.raises(ValueError, match="Simulated invalid track"):
        library.update(original.id, **replacement_data)

    assert library.get(original.id) is original
    assert original.title == track_data["title"]
    assert len(library) == 1
```

`*_arguments` and `**_keyword_arguments` accept any arguments, so the
function can stand in for the constructor. Checking the error alone would
miss a half-finished update. The assertions after the `with` block check
that the library is unchanged.

### References

- [pytest: Monkeypatching](https://docs.pytest.org/en/stable/how-to/monkeypatch.html)
- [pytest: Assertions about exceptions](https://docs.pytest.org/en/stable/how-to/assert.html#assertions-about-expected-exceptions)
- [Flask: Identifying tests](https://flask.palletsprojects.com/en/stable/testing/#identifying-tests)

## Testing an HTTPX Client

`MusicLibraryClient` sends requests to the music server with HTTPX. A client
test checks:

- the request the client sends: method, path, and body
- the value it returns from a successful response
- how it handles errors, such as a 404 for a missing track
- that it closes its connection when finished

The [music client tests](../demo/music_library_server/tests/test_client.py)
check these points without a running server. They replace `httpx.Client` with
two fakes:

- `FakeHTTPClient` records the last request and returns a preset response. It
  also records whether it was closed.
- `FakeResponse` provides the parts of an HTTPX response that the music client
  uses: `status_code`, `raise_for_status()`, and `json()`. In HTTPX, `json()`
  is a method; in a Flask test response, `json` is a property.

This shortened version supports the tests below. The full file adds `put` and
`delete` methods that follow the same pattern:

```python
class FakeResponse:
    """A simple stand-in for an HTTPX response."""

    def __init__(self, status_code, data=None):
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
        self.response = None
        self.last_request = None
        self.closed = False

    def _request(self, method, path, body=None):
        """Record a request and return the configured response."""
        if self.response is None:
            raise AssertionError("Set a fake response before making a request")
        self.last_request = (method, path, body)
        return self.response

    def get(self, path):
        """Record a GET request."""
        return self._request("GET", path)

    def post(self, path, json):
        """Record a POST request and its JSON body."""
        return self._request("POST", path, json)

    def close(self):
        """Record that the fake client was closed."""
        self.closed = True
```

`MusicLibraryClient` creates its `httpx.Client` in `__init__`, so the patch
must be in place before the music client is created. The `music_client`
fixture patches first and then creates the client:

```python
import pytest

import client as client_module


@pytest.fixture
def fake_http():
    """Create a fresh fake HTTP client for each test."""
    return FakeHTTPClient()


@pytest.fixture
def music_client(monkeypatch, fake_http):
    """Create a MusicLibraryClient that uses the fake HTTP client."""
    def make_fake_client(base_url, timeout):
        """Record the settings and return the fake HTTP client."""
        fake_http.base_url = base_url
        fake_http.timeout = timeout
        return fake_http

    monkeypatch.setattr(client_module.httpx, "Client", make_fake_client)
    return client_module.MusicLibraryClient(server_url="http://music.test")
```

`client_module` is the application's `client.py` module, renamed so it is not
confused with a Flask test client. A test that requests both `music_client`
and `fake_http` gets the same fake that the music client uses, so it can set
responses and read recorded requests.

Each test sets a fake response, calls a client method, and checks both the
return value and the recorded request:

```python
def test_status_and_length(music_client, fake_http):
    """Status and length use the server's status response."""
    status = {"status": "online", "track_count": 2}
    fake_http.response = FakeResponse(200, status)

    assert fake_http.base_url == "http://music.test"
    assert music_client.status() == status
    assert fake_http.last_request == ("GET", "/api/status", None)
    fake_http.last_request = None
    assert len(music_client) == 2
    assert fake_http.last_request == ("GET", "/api/status", None)


def test_get_missing_track(music_client, fake_http):
    """Getting a missing track returns None."""
    fake_http.response = FakeResponse(404)

    assert music_client.get_track(99) is None
    assert fake_http.last_request == ("GET", "/api/tracks/99", None)


def test_create_track(music_client, fake_http, track_data):
    """Creating a track sends every field and returns the created track."""
    track = {"id": 5, **track_data}
    fake_http.response = FakeResponse(201, {"track": track, "message": "created"})

    created = music_client.create_track(**track_data)

    assert fake_http.last_request == ("POST", "/api/tracks", track_data)
    assert created == track


def test_other_http_errors_are_raised(music_client, fake_http):
    """Unexpected HTTP errors are passed to the caller."""
    fake_http.response = FakeResponse(500)

    with pytest.raises(RuntimeError, match="Simulated HTTP error"):
        music_client.status()
```

`len(music_client)` calls `__len__`, which makes a status request. Clearing
`last_request` first shows that a new request was made. This file's
`track_data` fixture uses a date string, because the client sends JSON.

The client treats errors in two ways. A 404 means the track does not exist,
so `get_track()` returns `None`. The full suite also checks that
`update_track()` returns `None` and `delete_track()` returns `False`. Any
other error status is passed to the caller by `raise_for_status()`. The fake
raises `RuntimeError` where real HTTPX raises `httpx.HTTPStatusError`. The
test checks the client's error handling, not HTTPX itself.

The client also works as a context manager: `__exit__` closes the HTTP
connection when a `with` block ends, even when the block raises:

```python
def test_context_manager_closes_after_error(music_client, fake_http):
    """A with-block closes the client and does not suppress exceptions."""
    with pytest.raises(ValueError, match="Error in with-block"):
        with music_client:
            raise ValueError("Error in with-block")

    assert fake_http.closed is True
```

`pytest.raises` checks that the error still reaches the caller, and the last
assertion checks that the connection was closed anyway.

### References

- [pytest: Monkeypatching](https://docs.pytest.org/en/stable/how-to/monkeypatch.html)
- [pytest: Assertions about exceptions](https://docs.pytest.org/en/stable/how-to/assert.html#assertions-about-expected-exceptions)
- [Flask: Sending requests with the test client](https://flask.palletsprojects.com/en/stable/testing/#sending-requests-with-the-test-client)
- [HTTPX: Exceptions](https://www.python-httpx.org/exceptions/)
- [Python: Context managers](https://docs.python.org/3/reference/datamodel.html#with-statement-context-managers)

## Testing Startup Without Starting a Server

`main()` calls `create_app().run(debug=True)`, which starts a server and waits for requests
until it is stopped. A test can check what `main()` does without starting
that server, by replacing the method that starts it.

The [echo startup test](../demo/flask_minimal_demo/test_demo_server.py) runs
the real `main()` and application factory, but replaces `Flask.run` with a
function that records its arguments:

```python
from flask import Flask

from demo_server import main


def test_main_starts_configured_app_in_debug_mode(monkeypatch):
    """Direct startup runs the configured app with debug mode enabled."""
    calls = []

    def fake_run(app, *, debug):
        """Record the app and its debug setting."""
        calls.append((app, debug))

    monkeypatch.setattr(Flask, "run", fake_run)
    main()

    assert len(calls) == 1
    app, debug = calls[0]
    assert debug is True
    assert app.test_client().post(
        "/api/echo", json={"host": "web01"}
    ).status_code == 200
```

Because `fake_run` replaces a method on the class, Python passes the Flask
app as its first argument. `debug` receives the `debug=True` keyword
argument. The test checks that `run` was called once with debug
mode on, then uses the recorded app's test client to check that its route
works. No port is opened.

### References

- [pytest: Monkeypatching](https://docs.pytest.org/en/stable/how-to/monkeypatch.html)
- [Flask: `Flask.run()`](https://flask.palletsprojects.com/en/stable/api/#flask.Flask.run)
- [Flask: Testing Flask applications](https://flask.palletsprojects.com/en/stable/testing/)
