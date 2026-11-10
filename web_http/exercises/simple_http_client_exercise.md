# Exercise: Building an HTTP Client with `httpx`

## Overview

|                         |                                                                                                                                   |
| ----------------------- | --------------------------------------------------------------------------------------------------------------------------------- |
| **Tools**               | VS Code, `uv` package manager                                                                                                     |
| **Learning Objectives** | Make HTTP requests with `httpx`, parse JSON responses, send JSON bodies with POST and PUT, handle HTTP errors, use `httpx.Client` |

In this exercise you write an **HTTP client** — a Python program that talks to a
server over the network. You will use the `httpx` library to send requests, read
JSON responses, and handle errors.

A practice server (`music_library.py`) is provided. It stores music tracks and
**echoes** back what it receives in every write response, so you can check that
your requests are correct.

The `music_library` server is like any web API on the internet. Later in the
course you will build servers like it with Flask. For now, your job is the
client.

> **Background reading:** Read `httpx_python_http_clients.md` before starting.

## The Practice Server

`music_library.py` serves these endpoints:

| Method   | URL                | Purpose             | Success Code     |
| -------- | ------------------ | ------------------- | ---------------- |
| `GET`    | `/api/status`      | Server health check | `200`            |
| `GET`    | `/api/tracks`      | List all tracks     | `200`            |
| `GET`    | `/api/tracks/<id>` | Get one track       | `200` (or `404`) |
| `POST`   | `/api/tracks`      | Create a new track  | `201`            |
| `PUT`    | `/api/tracks/<id>` | Update a track      | `200` (or `404`) |
| `DELETE` | `/api/tracks/<id>` | Delete a track      | `200` (or `404`) |

Each track has seven fields:

| Field       | Type   | Meaning                                |
| ----------- | ------ | -------------------------------------- |
| `id`        | number | Track ID, assigned by the server       |
| `title`     | string | Name of the song                       |
| `artist`    | string | Name of the artist                     |
| `recording` | string | Album, EP, or single the track is from |
| `genre`     | string | Type of music                          |
| `released`  | string | Release date (`YYYY-MM-DD`)            |
| `duration`  | number | Length of the track in seconds         |

The server starts with four tracks. When you create a track, only `title` and
`artist` are required — missing fields get default values.

Every write response (POST, PUT, DELETE) includes an `echo` object showing
exactly what the server received: the method, the URL, and the request body. Use
it to confirm your client sent the right data.

## Setup (2 minutes)

If you have not already, download `music_library` from the course site

Open a terminal in the `music_library` folder and install the dependencies:

```powershell
uv sync
```

Start the server:

```powershell
uv run python music_library.py
```

**Leave this terminal open.** Open a **second terminal** in VS Code — that is
where you will run your client code.

## Part 1 — Reading Data with GET (10 minutes)

### Step 1: Health check and list tracks

Create a file called `client.py`:

```python
import httpx

# Health check
response = httpx.get("http://localhost:5000/api/status")
print(f"Status code: {response.status_code}")
print(f"Response:    {response.json()}")

# List all tracks
response = httpx.get("http://localhost:5000/api/tracks")
tracks = response.json()

print(f"\nThere are {len(tracks)} tracks:")
for track in tracks:
    print(f"  [{track['id']}] {track['title']} — {track['artist']} ({track['duration']} s)")
```

Run it in your second terminal:

```powershell
uv run python client.py
```

### Step 2: Get a single track

Now write code **on your own** to fetch one track by its ID. The ID goes in the
URL path (see the endpoint table above).

```python
# Get a single track
# TODO: Send a GET request to fetch track 1
# Hint: The URL pattern is /api/tracks/<id>
#       See "GET — retrieve data" in httpx_python_http_clients.md Section 5
response = ___
track = response.json()
print(f"\nTrack 1: {track['title']} by {track['artist']}")
```

Once it works, change the URL to request **track 99** and run again.

### Q1.1

What status code does the server return for track 99? What key is in the JSON
body instead of `title`?

---

## Part 2 — Writing Data with POST, PUT, and DELETE (15 minutes)

### Step 1: Create a new track with POST

Add code that sends a JSON body. The `json=` parameter is how `httpx` sends JSON
— it serializes the data and sets the `Content-Type` header for you:

```python
# Create a new track
new_track = {
    "title": "Clair de Lune",
    "artist": "Claude Debussy",
    "genre": "classical",
    "duration": 300,
}
response = httpx.post("http://localhost:5000/api/tracks", json=new_track)

print(f"\nPOST status: {response.status_code}")
result = response.json()
print(f"Server says:   {result['message']}")
print(f"Created track: {result['track']}")
print(f"Echo:          {result['echo']}")
```

### Q2.1

What status code did the POST return, and why is it not `200`? What does
`body_received` in the `echo` object show? You did not send `recording` or
`released` — what values did the server give them?

### Step 2: Update a track with PUT

**Write your own code** to update the track you just created:

1. Get the new track's `id` from the POST response (`result["track"]["id"]`)
1. Send a PUT request with a JSON body of the fields to change
1. Print the status code and the updated track

> **Reference:** "PUT — update data" in `httpx_python_http_clients.md`
> Section 5.

```python
# Update the track
created_id = result["track"]["id"]

# TODO: Send a PUT request to /api/tracks/<created_id>
#       with a JSON body that changes the duration to 320
# Hint: httpx.put(url, json={...})
response = ___

print(f"\nPUT status: {response.status_code}")
put_result = response.json()
print(f"Updated track: {put_result['track']}")
```

### Step 3: Delete a track and confirm

**Write this step entirely on your own:**

1. Send a DELETE request for the track you created (use `created_id`)
1. Print the status code and the server's message
1. Send a GET request for the same track to confirm it is gone
1. Print that GET's status code

> **Reference:** "DELETE — remove data" in `httpx_python_http_clients.md`
> Section 5.

```python
# Delete the track
# TODO: Send a DELETE request to /api/tracks/<created_id>
# TODO: Print the status code and response message

# Confirm deletion
# TODO: Send a GET request for the same track
# TODO: Print the status code — what do you expect it to be?
```

### Q2.2

What status code does the GET return after the track has been deleted?

---

## Part 3 — `httpx.Client` and Error Handling (10 minutes)

So far every request opens a **new connection** and needs the **full URL**. The
`httpx.Client` class fixes both: it keeps one connection open and lets you set a
`base_url` so you write only relative paths.

> **Reference:** `httpx_python_http_clients.md` Section 7 for `httpx.Client`,
> Section 6 for error handling.

### Step 1: Create a client and read data

Create a new file called `client_v2.py`:

```python
import httpx

client = httpx.Client(base_url="http://localhost:5000", timeout=10.0)

# Health check — notice the relative path (no http://localhost:5000)
status = client.get("/api/status").json()
print(f"Server: {status['status']}, Tracks: {status['track_count']}")

# TODO: List all tracks using client.get() with a relative path
#       Print each track's title
```

Run it:

```powershell
uv run python client_v2.py
```

### Q3.1

Compare the URLs in `client_v2.py` with those in `client.py`. What is different?
Why is `httpx.Client` more efficient when making many requests to the same
server?

### Step 2: Handle a missing resource

Real client code cannot assume every request succeeds. The `raise_for_status()`
method helps: it does nothing on success (2xx) but raises
`httpx.HTTPStatusError` on 4xx or 5xx.

Add a `try`/`except` block that requests a track that does not exist, then catch
the error and print the status code and the server's error message.

```python
# Handle a 404
# TODO: Write a try/except block that:
#   - GETs /api/tracks/999 using the client
#   - Calls raise_for_status()
#   - Catches httpx.HTTPStatusError
#   - Prints e.response.status_code and e.response.json()["error"]
# Reference: httpx_python_http_clients.md Section 6
```

### Q3.2

What does `raise_for_status()` do when the status code is `200`? What does it do
when the status code is `404`?

### Optional challenge: Handle a connection error

If you finish early: **stop the server** (`Ctrl+C`), then add a `try`/`except`
that catches `httpx.ConnectError` when the server is unreachable. See
`httpx_python_http_clients.md` Section 6 for the pattern.

---

## Reflection

### Q4.1

Here you wrote the **client** while the server was provided. Later in the course
you will build the **server** side with Flask. In a real system, why might one
Python program need to be both a server (receiving requests) and a client
(sending requests to other servers)?
