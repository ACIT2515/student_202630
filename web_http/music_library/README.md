# Music Library API

A practice project for the HTTP exercises in this course. You will use this
one folder for several exercises:

1. Exploring RESTful APIs with Bruno and cURL
1. Building an HTTP Client with `httpx`
1. An Object-Oriented HTTP Client
1. Testing an HTTP Client with Monkey Patching

Download and unzip this folder **once**, then keep working in it. The files
you create in each exercise stay here and are used by the later exercises.

## Contents

| File               | Purpose                                            |
| ------------------ | -------------------------------------------------- |
| `music_library.py` | The practice server. Run it — do not edit it.      |
| `pyproject.toml`   | Project dependencies (`flask`, `httpx`)            |
| `uv.lock`          | Pinned dependency versions                         |

## Setup

Open a terminal in this folder and install the dependencies:

```powershell
uv sync
```

## Running the Server

```powershell
uv run python music_library.py
```

The server runs at `http://localhost:5000`. Press `Ctrl+C` to stop it.

Confirm it is up by opening `http://localhost:5000/api/status` in a browser —
you should see a small JSON object with `"status": "online"`.

## The API

| Method   | URL                 | Purpose             | Success Code     |
| -------- | ------------------- | ------------------- | ---------------- |
| `GET`    | `/api/status`       | Server health check | `200`            |
| `GET`    | `/api/tracks`       | List all tracks     | `200`            |
| `GET`    | `/api/tracks/<id>`  | Get one track       | `200` (or `404`) |
| `POST`   | `/api/tracks`       | Create a new track  | `201`            |
| `PUT`    | `/api/tracks/<id>`  | Update a track      | `200` (or `404`) |
| `DELETE` | `/api/tracks/<id>`  | Delete a track      | `200` (or `404`) |

Each track has `id`, `title`, `artist`, `recording`, `genre`, `released`, and
`duration` fields. The server stores data in memory — restarting it resets the
library to its four seed tracks.
