# Music Library API

A small Flask API and HTTP client for practicing object-oriented Python. The
server stores tracks in memory; it does not use a database.

## Project Files

| File | Purpose |
| --- | --- |
| `track.py` | Defines a track and validates its fields. |
| `music_library.py` | Stores tracks and assigns IDs. |
| `seed_data.py` | Builds a library with four sample tracks. |
| `music_library_server.py` | Creates the Flask app and handles API requests. |
| `client.py` | Provides a Python client for the API using HTTPX. |
| `tests/` | Contains unit tests and API tests. |
| `pyproject.toml` | Defines dependencies and pytest settings. |
| `uv.lock` | Records the resolved dependency versions. |

## Set Up

Use Python 3.13 or newer and install uv. Open a terminal in the project folder
and install the project dependencies:

```powershell
uv sync
```

`uv sync` creates a virtual environment and installs the dependencies listed
in the project configuration.

### References

- [uv documentation](https://docs.astral.sh/uv/)

## Run the Server

From the project folder, start Flask's development server:

```powershell
uv run flask --app music_library_server run --debug
```

Open [http://localhost:5000/api/status](http://localhost:5000/api/status) to
check that the server is running. Stop it with `Ctrl+C`.

The app starts with four sample tracks. Data is held in memory and resets when
the server restarts. Flask's development server is for local development, not
production.

To run the example client, leave the server running and open a second terminal
in the project folder:

```powershell
uv run python client.py
```

The client uses a 10-second HTTP timeout.

### References

- [Flask CLI documentation](https://flask.palletsprojects.com/en/stable/cli/)
- [HTTPX client documentation](https://www.python-httpx.org/advanced/clients/)

## API

| Method | Path | Purpose | Success response |
| --- | --- | --- | --- |
| `GET` | `/api/status` | Check server status. | `200` |
| `GET` | `/api/tracks` | List all tracks. | `200` |
| `GET` | `/api/tracks/<id>` | Get a track. | `200` |
| `POST` | `/api/tracks` | Create a track. | `201` |
| `PUT` | `/api/tracks/<id>` | Replace a track. | `200` |
| `DELETE` | `/api/tracks/<id>` | Delete a track. | `200` |

Track fields are `title`, `artist`, `recording`, `genre`, `released`, and
`duration`. The server assigns `id`. Every field is required when creating or
replacing a track.

Text fields must not be blank. `released` must use the `YYYY-MM-DD` format, and
`duration` must be a number greater than zero. Invalid requests return `400`;
incomplete requests list all missing fields. Requests for tracks that do not
exist return `404`. A `PUT` replaces all track fields; it is not a partial
update.

For example, create a track from PowerShell:

```powershell
$track = @{
    title = "So What"
    artist = "Miles Davis"
    recording = "Kind of Blue"
    genre = "jazz"
    released = "1959-08-17"
    duration = 545
}

Invoke-RestMethod `
    -Uri "http://localhost:5000/api/tracks" `
    -Method Post `
    -ContentType "application/json" `
    -Body ($track | ConvertTo-Json)
```

## How the Classes Work Together

- `Track` represents one track and validates values assigned to its fields.
- `MusicLibrary` creates, finds, updates, and removes tracks. It does not depend
  on Flask or HTTP.
- `MusicLibraryServer` translates HTTP requests and JSON into library method
  calls, then turns the results into HTTP responses.
- `create_app()` builds the Flask app. By default, it creates a library with
  the four sample tracks. Tests can pass in a different library.
- `MusicLibraryClient` wraps HTTP requests so Python code can work with tracks
  without constructing URLs or decoding JSON itself.

## Run the Tests

Run all tests from the project folder:

```powershell
uv run pytest -q
```

Run one test file by passing its path:

```powershell
uv run pytest -q tests\test_track.py
```

The tests are grouped by component:

- `test_track.py` tests `Track` directly.
- `test_library.py` tests `MusicLibrary` with a fake `Track`.
- `test_client.py` replaces the HTTPX client with a fake, so no server or
  network connection is needed.
- `test_music_library_server.py` uses Flask's test client to make requests
  without starting a live server. Its fixtures build fresh sample data, the
  app, and the test client.

### References

- [Flask testing documentation](https://flask.palletsprojects.com/en/stable/testing/)

### Pytest Settings

Pytest settings are in `[tool.pytest.ini_options]` in
[pyproject.toml](pyproject.toml):

```toml
[tool.pytest.ini_options]
testpaths = ["tests"]
pythonpath = ["."]
```

- `testpaths` tells pytest to search `tests` by default when running pytest
  from the project folder. A path given on the command line selects a specific
  file or directory.
- `pythonpath` adds the project folder to Python's import path during tests, so
  test files can import modules such as `track` and `music_library_server`.

These settings do not change the terminal's current folder. Pytest selects its
`rootdir` based on the command and configuration-file discovery; `.` in
`pythonpath` refers to that root directory. To see the selected configuration
and collected tests, run:

```powershell
uv run pytest --collect-only
```

#### References

- [Pytest configuration guide](https://docs.pytest.org/en/stable/reference/customize.html)
- [Pytest root directory explanation](https://docs.pytest.org/en/stable/reference/customize.html#finding-the-rootdir)
- [Pytest `testpaths` setting](https://docs.pytest.org/en/stable/reference/reference.html#confval-testpaths)
- [Pytest `pythonpath` setting](https://docs.pytest.org/en/stable/reference/reference.html#confval-pythonpath)

## Debug in VS Code

Open the `music_library_server` project folder in VS Code. This makes its
`.vscode` settings available. If needed, install the Python extension, then
select the project's virtual environment as the Python interpreter:

- Windows: `.venv\Scripts\python.exe`
- macOS or Linux: `.venv/bin/python`

Open the Run and Debug view and select "Python Debugger: Flask Music Library".
Press `F5` to start the server under the debugger. The launch configuration
disables Flask's debugger and reloader so VS Code can control the debug session.
Set a breakpoint in `music_library_server.py`, then send a request to the
server. For example, use
`http://127.0.0.1:5000/api/tracks/1` in a browser.

### References

- [VS Code Python debugging guide](https://code.visualstudio.com/docs/python/debugging)
