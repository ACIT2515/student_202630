# Exercise: An Object-Oriented HTTP Client

## Overview

|                         |                                                                                                              |
| ----------------------- | ------------------------------------------------------------------------------------------------------------- |
| **Duration**            | 45 minutes                                                                                                   |
| **Tools**               | VS Code, `uv` package manager                                                                                |
| **Prerequisites**       | Completed "Building an HTTP Client with `httpx`"                                                             |
| **Learning Objectives** | Wrap an API in a class, encapsulation, composition, keyword arguments (`**kwargs`), context managers         |

In the previous exercise your client code repeated the same plumbing for every
request: build a URL, send it, check the status, call `.json()`. Real programs
hide that plumbing inside a **wrapper class** so the rest of the code can speak
the domain language instead of HTTP. This is how real API libraries work — for
example `boto3` for AWS: you call `s3.list_buckets()`, not
`httpx.get("https://s3.amazonaws.com/...")`.

You will build a `MusicLibraryClient` class in a file called
`oo_http_client.py`. When you are done, code that uses your class will read
like this:

```python
with MusicLibraryClient() as library:
    track = library.create_track("Clair de Lune", "Claude Debussy", duration=300)
    print(library.get_track(track["id"]))
    library.delete_track(track["id"])
```

No URLs, no status codes, no `.json()` — the class handles all of it.

---

## Setup (2 minutes)

In your `music_library` folder, start the practice server (same one as the
previous exercise) and leave it
running:

```powershell
uv run python music_library.py
```

Work in a second terminal, in the same folder.

---

## Part 1 — The Skeleton (10 minutes)

### Step 1: Create the class

Create `oo_http_client.py`:

```python
"""An object-oriented client for the Music Library API."""

import httpx


class MusicLibraryClient:
    """A client for the Music Library API.

    Wraps an httpx.Client so callers can work with tracks instead of
    URLs, status codes, and JSON.
    """

    def __init__(self, base_url: str = "http://localhost:5000"):
        self._http = httpx.Client(base_url=base_url, timeout=10.0)

    def status(self) -> dict:
        """Return the server's health check information."""
        response = self._http.get("/api/status")
        response.raise_for_status()
        return response.json()

    def close(self) -> None:
        """Close the underlying HTTP connection."""
        self._http.close()


def main():
    client = MusicLibraryClient()
    print(client.status())
    client.close()


if __name__ == "__main__":
    main()
```

Run it:

```powershell
uv run python oo_http_client.py
```

You should see the server's status dictionary.

### Q1.1

The attribute is named `_http`, with a leading underscore. What does that
convention tell other programmers?

### Q1.2

`MusicLibraryClient` does not inherit from `httpx.Client` — it **has** one as
an attribute. What is this design technique called, and where have you seen it
before in this course?

---

## Part 2 — Read Methods (10 minutes)

### Step 1: List and get

Add two methods to the class. Write the bodies yourself:

```python
    def list_tracks(self) -> list[dict]:
        """Return all tracks in the library."""
        # TODO: GET /api/tracks
        # TODO: call raise_for_status()
        # TODO: return the JSON list

    def get_track(self, track_id: int) -> dict | None:
        """Return one track, or None if it does not exist."""
        # TODO: GET /api/tracks/<track_id>
        # TODO: if the status code is 404, return None
        # TODO: otherwise call raise_for_status() and return the JSON
```

Update `main()` to try them:

```python
def main():
    client = MusicLibraryClient()
    print(client.status())

    for track in client.list_tracks():
        print(f"  [{track['id']}] {track['title']} — {track['artist']}")

    print(client.get_track(1))
    print(client.get_track(999))  # should print None

    client.close()
```

### Q2.1

`get_track` returns `None` for a missing track instead of raising an error.
Python's `dict.get()` makes the same choice. When is returning `None` more
convenient for the caller than an exception? When might an exception be
better?

---

## Part 3 — Write Methods (15 minutes)

### Step 1: Create

Add this method. Note the `**extras` parameter — it collects any extra keyword
arguments into a dict, so callers can pass as many or as few of the optional
fields as they like:

```python
    def create_track(self, title: str, artist: str, **extras) -> dict:
        """Create a track and return it (including its server-assigned ID).

        Args:
            title: Name of the song.
            artist: Name of the artist.
            **extras: Optional fields: recording, genre, released, duration.
        """
        body = {"title": title, "artist": artist, **extras}
        response = self._http.post("/api/tracks", json=body)
        response.raise_for_status()
        return response.json()["track"]
```

Try it in `main()`:

```python
    new_track = client.create_track("Clair de Lune", "Claude Debussy", duration=300)
    print(new_track)
```

### Q3.1

The server's response to a POST contains `message`, `track`, and `echo`, but
`create_track` returns only the `track` part. Why is hiding the rest of the
response a good idea? (Hint: what happens to callers if the server's response
format changes?)

### Step 2: Update and delete

Write these two yourself, following the same patterns:

```python
    def update_track(self, track_id: int, **changes) -> dict | None:
        """Update a track's fields. Return the updated track, or None if not found."""
        # TODO: PUT /api/tracks/<track_id> with json=changes
        # TODO: if 404, return None
        # TODO: otherwise raise_for_status() and return the "track" part of the JSON

    def delete_track(self, track_id: int) -> bool:
        """Delete a track. Return True if deleted, False if it did not exist."""
        # TODO: DELETE /api/tracks/<track_id>
        # TODO: if 404, return False
        # TODO: otherwise raise_for_status() and return True
```

Extend `main()` into a full lifecycle:

```python
    updated = client.update_track(new_track["id"], genre="impressionist")
    print(updated)

    print(client.delete_track(new_track["id"]))  # True
    print(client.delete_track(new_track["id"]))  # False — already gone
```

### Q3.2

In the previous exercise, deleting a track took three lines (request, status
check, JSON). What does the equivalent call look like now? Who benefits when
this logic lives in one place?

---

## Part 4 — Context Manager (10 minutes)

Right now, callers must remember to call `close()`. Python's `with` statement
can do it for them — any class with `__enter__` and `__exit__` methods works
with `with`.

### Step 1: Add the dunder methods

```python
    def __enter__(self):
        """Return this client when entering a with-block."""
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        """Close the connection when leaving a with-block."""
        self.close()
```

### Step 2: Use it

Rewrite `main()` to use a `with` block — no `close()` call needed:

```python
def main():
    with MusicLibraryClient() as library:
        print(library.status())
        new_track = library.create_track("Clair de Lune", "Claude Debussy", duration=300)
        library.update_track(new_track["id"], genre="impressionist")
        print(library.get_track(new_track["id"]))
        library.delete_track(new_track["id"])
```

### Q4.1

Where have you used `with` before? What does `__exit__` guarantee, even if the
code inside the block raises an exception?

### Optional challenge

Add a `__len__` method that returns the number of tracks on the server, so
`len(library)` works. (Hint: the status endpoint already reports a count.)

---

## Reflection

### Q5.1

The server stores its tracks in a `Library` class with methods like `get`,
`add`, and `remove`. Your `MusicLibraryClient` has nearly the same interface —
but its methods travel over the network instead of touching a dict. What does
this symmetry suggest about how large systems are designed?

### Q5.2

Suppose the API team renames the endpoint from `/api/tracks` to `/api/songs`.
How many files change in a program built on `MusicLibraryClient`? How many
would change if every part of the program called `httpx` directly?
