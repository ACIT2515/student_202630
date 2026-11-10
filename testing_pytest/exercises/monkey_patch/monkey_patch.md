# Exercise: Testing an HTTP Client with Monkey Patching

## Overview

Your `MusicLibraryClient` works — but so far, checking it meant starting the
server and running `main()` by hand. That is manual testing. In this exercise
you write automated pytest tests for the client that run **without any server at
all**.

Why not just test against the real server?

1. The server must be running, on the right port, with known data.
1. Tests that create, update, and delete tracks **change that data**, so tests
   interfere with each other and cannot safely re-run.
1. Some situations are hard to trigger on purpose — how do you make a healthy
   server return a `500` error?
1. Network calls are slow. A unit test suite should run in milliseconds.

The fix is **monkey patching**: temporarily replace the `httpx` methods your
client calls with simple functions that return responses you control. Your
client's logic runs for real — only the network disappears.

> **Background reading:** `pytest.md`, `pytest_fixtures.md`, and
> `monkeypatch.md` in the testing notes.

## Setup (5 minutes)

Work in your `music_library` project folder — the same one as the previous
exercises. It should contain `music_library.py` and your `oo_http_client.py`.

1. Add pytest as a development dependency:

   ```powershell
   uv add --dev pytest
   ```

1. **Stop the server if it is running** (`Ctrl+C`). The whole point of this
   exercise is that the tests pass without it.

1. Create a file called `test_oo_http_client.py`.

## Part 1 — A Fake Response (10 minutes)

### The problem

Your client calls methods like `self._http.get(...)` and expects back an
`httpx.Response` — an object with a `.status_code`, a `.json()` method, and a
`.raise_for_status()` method. If we replace `httpx.Client.get`, our replacement
must return something that _looks enough like_ a response for the client to
work.

It does not need to be a real `httpx.Response`. Python only cares that the
object has the attributes and methods the client actually uses. This is called
**duck typing**: if it walks like a response and quacks like a response, the
client cannot tell the difference.

### Step 1: Write the fake

Put this at the top of `test_oo_http_client.py`:

```python
"""Tests for MusicLibraryClient, using monkeypatch instead of a server."""

import httpx
import pytest

from oo_http_client import MusicLibraryClient


class FakeResponse:
    """A stand-in for httpx.Response with only the parts our client uses."""

    def __init__(self, status_code: int, json_data=None):
        self.status_code = status_code
        self._json_data = json_data

    def json(self):
        return self._json_data

    def raise_for_status(self):
        if self.status_code >= 400:
            raise httpx.HTTPStatusError(
                f"Error response {self.status_code}",
                request=None,
                response=None,
            )
```

### Step 2: The first test — given

This test replaces `httpx.Client.get` for the duration of one test. Note the
patch target: it is the **method on the class**, so the replacement takes `self`
as its first parameter — the same pattern as the `'module.ClassName.attribute'`
example in the monkey patching notes.

```python
def test_get_track_found(monkeypatch):
    # Arrange: any GET will return this canned track
    track = {"id": 1, "title": "So What", "artist": "Miles Davis"}
    monkeypatch.setattr(
        "httpx.Client.get", lambda self, url: FakeResponse(200, track)
    )
    client = MusicLibraryClient()

    # Act
    result = client.get_track(1)

    # Assert
    assert result == track
```

Run it:

```powershell
uv run pytest -v
```

The test passes with no server running. Pytest restores the real
`httpx.Client.get` automatically after the test.

### Q1.1

The lambda has two parameters: `self` and `url`. Why does it need `self` when
the real code calls `self._http.get(url)` with only one argument?

### Q1.2

`FakeResponse` does not inherit from `httpx.Response`, yet the client accepts
it. What property of Python makes this work?

## Part 2 — Testing the Read Methods (5 minutes)

Write these tests yourself, following the pattern from Part 1:

```python
def test_get_track_missing(monkeypatch):
    # TODO: patch httpx.Client.get to return FakeResponse(404)
    # TODO: assert that client.get_track(999) returns None


def test_get_track_server_error(monkeypatch):
    # The hard-to-trigger case: the server fails with a 500.
    # TODO: patch httpx.Client.get to return FakeResponse(500)
    # TODO: use "with pytest.raises(httpx.HTTPStatusError):" and call
    #       client.get_track(1) inside the block
```

### Q2.1

`test_get_track_server_error` checks behaviour you could not easily test against
the real server. Why is it still important for the client to be tested with a
`500` response?

## Part 3 — A Client Fixture (5 minutes)

Every test so far builds its own `MusicLibraryClient()`. That is repeated setup,
exactly what fixtures are for.

### Step 1: Add the fixture

```python
@pytest.fixture
def client():
    """Provide a MusicLibraryClient for tests."""
    return MusicLibraryClient()
```

### Step 2: Use it

Change your tests to take `client` as a parameter instead of constructing one:

```python
def test_get_track_found(monkeypatch, client):
    track = {"id": 1, "title": "So What", "artist": "Miles Davis"}
    monkeypatch.setattr(
        "httpx.Client.get", lambda self, url: FakeResponse(200, track)
    )

    assert client.get_track(1) == track
```

Update your other tests the same way, then re-run pytest.

### Q3.1

Each test gets a **fresh** client from the fixture. Why is that better than
sharing one client object between all tests?

## Part 4 — Testing the Write Methods (10 minutes)

The write methods call `post`, `put`, and `delete`, and those take more
arguments — for example the client calls `self._http.post(url, json=body)`, so
the replacement needs a `json` parameter:

```python
def test_create_track(monkeypatch, client):
    created = {"id": 5, "title": "Ping", "artist": "The Packets"}
    monkeypatch.setattr(
        "httpx.Client.post",
        lambda self, url, json: FakeResponse(201, {"track": created}),
    )

    result = client.create_track("Ping", "The Packets")

    assert result == created
```

Note the fake response body: `{"track": created}`. It must have the same
**shape** as the real server's response, because `create_track` reaches into it
with `["track"]`.

Write these yourself:

```python
def test_update_track(monkeypatch, client):
    # TODO: patch httpx.Client.put to return
    #       FakeResponse(200, {"track": {...with your changed field...}})
    # TODO: call client.update_track(1, genre="jazz")
    # TODO: assert the returned track has the new genre


def test_delete_track_missing(monkeypatch, client):
    # TODO: patch httpx.Client.delete to return FakeResponse(404)
    # TODO: assert client.delete_track(999) is False
```

Run the full suite:

```powershell
uv run pytest -v
```

All tests should pass — with the server stopped.

### Q4.1

The `put` and `delete` replacements never check which URL or body they were
given. Suppose `update_track` had a bug and sent the request to `/api/tracks`
without the ID — would these tests catch it? What does that tell you about what
these tests do and do not prove?

## Optional Tasks

### Task 1: Round out the suite

Add the mirror images of the Part 2 and Part 4 tests:

```python
def test_list_tracks(monkeypatch, client):
    # TODO: patch httpx.Client.get to return FakeResponse(200, [...])
    #       with a list of two track dicts
    # TODO: assert the result has length 2


def test_update_track_missing(monkeypatch, client):
    # TODO: patch httpx.Client.put to return FakeResponse(404)
    # TODO: assert client.update_track(999, genre="jazz") returns None


def test_delete_track(monkeypatch, client):
    # TODO: patch httpx.Client.delete to return
    #       FakeResponse(200, {"message": "deleted"})
    # TODO: assert client.delete_track(1) is True
```

### Task 2: A `spy` to track function calls

A replacement function can **record** what it was called with. Use a list and a
`def` instead of a lambda:

```python
def test_create_track_sends_correct_body(monkeypatch, client):
    sent_bodies = []

    def fake_post(self, url, json):
        sent_bodies.append(json)
        return FakeResponse(201, {"track": {"id": 5}})

    monkeypatch.setattr("httpx.Client.post", fake_post)

    client.create_track("Ping", "The Packets", duration=32)

    assert sent_bodies[0]["title"] == "Ping"
    assert sent_bodies[0]["duration"] == 32
```

This test _does_ catch request-building bugs. Recording calls like this is so
useful that Python has a standard tool for it — **mock objects**
