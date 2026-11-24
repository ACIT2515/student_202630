# Minimal Flask and HTTPX Client Demonstration.

## Contents

| File                  | Purpose                                         |
| --------------------- | ----------------------------------------------- |
| `demo_server.py`      | `EchoServer` class and `create_app()` factory   |
| `demo_client.py`      | `EchoClient` class that sends requests (httpx)  |
| `test_demo_server.py` | PyTest tests using the Flask test client        |

## Running the Server

```powershell
uv run flask --app demo_server run --debug
```

Or run `uv run python demo_server.py`. The server runs at
`http://localhost:5000`.

## Sending a Request

With the server running, use the Python client in a second terminal:

```powershell
uv run python demo_client.py
```

The server replies with the same JSON plus a UTC timestamp:

```json
{
  "received": {"host": "web01", "status": "up"},
  "received_at": "2026-11-12T04:44:06.506359+00:00"
}
```

## Testing with Bruno

Use the Bruno VS Code extension to send requests from the included collection.
The `demo_flask_bruno` folder contains the `demo_01` request, which posts JSON
to `http://127.0.0.1:5000/api/echo`.

1. Install the Bruno extension from the VS Code Extensions view.
1. Start the server with `uv run flask --app demo_server run --debug`.
1. Open the `demo_flask_bruno` folder as a collection in the Bruno extension.
1. Open `demo_01` and click the send button to run the request.

The response shows status `200` and the echoed JSON with a `received_at`
timestamp. Edit the request body and send it again to see how the reply
changes. A body that is not valid JSON returns status `400`.

## Debugging in VS Code

The [launch.json](.vscode/launch.json) file has two debug configurations, one
for the server and one for the client. Both appear in the Run and Debug view.

### Debugging the Server

1. Set breakpoints in `demo_server.py`, for example inside the `echo` method.
1. In the Run and Debug view, choose "Python Debugger: Flask" and press `F5`.
1. Send a request with `uv run python demo_client.py` or `Invoke-RestMethod`.
   Execution pauses at the breakpoint when the request arrives.

The configuration passes `--no-debugger` and `--no-reload` to Flask so that
the VS Code debugger, not Flask's browser debugger, handles breakpoints.

### Debugging the Client

1. Start the server, either with the "Python Debugger: Flask" configuration or
   with `uv run flask --app demo_server run`.
1. Set breakpoints in `demo_client.py`.
1. In the Run and Debug view, choose "Python Debugger: Echo Client" and press
   `F5`.

The server has to be running first. Otherwise, the client fails with a
connection error.

### Debugging Both at Once

Start "Python Debugger: Flask" first, then start "Python Debugger: Echo
Client" while the server is still running. VS Code runs both sessions together.
Use the session dropdown in the debug toolbar to switch between them. With
breakpoints in both files, you can follow a request from the client to the
server and back.

## Running the Tests

```powershell
uv run pytest -q
```

