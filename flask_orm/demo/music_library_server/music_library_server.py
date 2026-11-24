"""
MusicLibrary 

This server manages a simple music library of tracks. It validates all
incoming requests and song and server info,

It includes a "echo" object that shows exactly what the server received.


Each track has the following attributes. All are required when creating
or updating a track, except id, which the server assigns:
    id        — number, the track ID (assigned by the server)
    title     — string, name of the song
    artist    — string, the name of the artist
    recording — string, name of the album, EP, or single
    genre     — string, the type of music
    released  — string, the release date of the track (YYYY-MM-DD)
    duration  — number greater than zero, length in seconds

Tracks are stored in memory as instances of the ``Track`` class
(``track.py``) inside a ``MusicLibrary`` (``music_library.py``), and
converted to plain dicts with ``Track.to_dict`` when sent as JSON.
``Track`` validates its own values and raises ``ValueError``; this server
turns that error into a 400 response.

``MusicLibraryApp`` owns the Flask app and handles requests using its
``Library``. The ``create_app`` factory serves a pre-seeded library by
default. Tests can call ``create_app(Library())`` for an empty library.

Run with:
    uv run flask --app music_library run --debug

Endpoints:
    GET    /api/status          — Server health check
    GET    /api/tracks          — List all tracks
    GET    /api/tracks/<id>     — Get one track by ID
    POST   /api/tracks          — Create a new track (requires JSON with
                                  every field except id)
    PUT    /api/tracks/<id>     — Replace every field of a track (requires
                                  JSON with every field except id)
    DELETE /api/tracks/<id>     — Delete a track
"""

from datetime import date

from flask import Flask, jsonify, request

from music_library import MusicLibrary
from seed_data import build_seed_library
from track import Track


class MusicLibraryServer:
    """Handle HTTP requests for an in-memory music library.

    Attributes:
        library: The collection of tracks served by the API.
        app: The Flask application with routes bound to this object's methods.
    """

    def __init__(self, library: MusicLibrary):
        """Create the Flask app and register its routes.

        Args:
            library: The collection of tracks to serve.
        """
        # The Music Library Server has a Music Library
        self.library = library

        # The Music Library Server has a Flask App that it uses
        # to hold the application's routes and configuration.
        # __name__ identifies this module so Flask can locate app resources.
        # https://flask.palletsprojects.com/en/stable/quickstart/#a-minimal-application
        self.app = Flask(__name__)

        # add_url_rule connects a URL and HTTP method to a view function.
        # Here, the views are bound methods, bound to this specific instance of this
        # MusicLibraryApp object.

        # Without a methods argument, Flask registers GET. It also handles
        # HEAD for GET routes and OPTIONS automatically by default.
        # https://flask.palletsprojects.com/en/stable/api/#flask.Flask.add_url_rule
        # https://flask.palletsprojects.com/en/stable/quickstart/#http-methods
        self.app.add_url_rule("/api/status", view_func=self.status)

        self.app.add_url_rule(
            "/api/tracks", view_func=self.list_tracks, methods=["GET"]
        )

        # <int:track_id> matches an integer in the URL and passes it to
        # the selected view as the track_id keyword argument.
        # https://flask.palletsprojects.com/en/stable/quickstart/#variable-rules
        self.app.add_url_rule(
            "/api/tracks/<int:track_id>", view_func=self.get_track, methods=["GET"]
        )

        # The same URL can have different views for different HTTP methods.
        self.app.add_url_rule(
            "/api/tracks", view_func=self.create_track, methods=["POST"]
        )

        self.app.add_url_rule(
            "/api/tracks/<int:track_id>", view_func=self.update_track, methods=["PUT"]
        )

        self.app.add_url_rule(
            "/api/tracks/<int:track_id>",
            view_func=self.delete_track,
            methods=["DELETE"],
        )

    @staticmethod
    def _track_to_dict(track: Track) -> dict[str, object]:
        """Convert a Track to an API dict, formatting its date as ISO text."""
        data = track.to_dict()
        data["released"] = track.released.isoformat()
        return data

    @staticmethod
    def _find_missing_fields(data: dict) -> list[str]:
        """Return all required fields missing from data."""
        missing_fields = []
        for field in Track.REQUIRED_FIELDS:
            if field not in data:
                missing_fields.append(field)
        return missing_fields

    @staticmethod
    def _missing_fields_error(fields: list[str]) -> dict[str, str | list[str]]:
        """Build the JSON error body for missing required fields."""
        return {
            "error": "Missing required fields",
            "missing_fields": fields,
            "hint": "Send JSON with every field, e.g. json={"
            '"title": "So What", "artist": "Miles Davis", '
            '"recording": "Kind of Blue", "genre": "jazz", '
            '"released": "1959-08-17", "duration": 545}',
        }

    @staticmethod
    def _parse_release_date(value: object) -> date:
        """Convert an API date string from http request in YYYY-MM-DD format to a date.

        Raises:
            ValueError: If value is not a valid date in YYYY-MM-DD format.
        """
        if not isinstance(value, str):
            raise ValueError("released must use YYYY-MM-DD format")
        try:
            release_date = date.fromisoformat(value)
        except ValueError as error:
            raise ValueError("released must use YYYY-MM-DD format") from error
        # fromisoformat also accepts forms such as "20240229"; require the
        # dashed form so the API has one date format.
        if release_date.isoformat() != value:
            raise ValueError("released must use YYYY-MM-DD format")
        return release_date

    def status(self):
        """Return server health check information.

        Returns:
            dict: JSON with server status, track count, and a welcome message.
        """
        # Flask converts a returned dict into a JSON response with status 200.
        # A (body, status) tuple can override that status, as shown below.
        # https://flask.palletsprojects.com/en/stable/quickstart/#about-responses
        return {
            "status": "online",
            "track_count": len(self.library),
            "message": "Echo server is running. Send requests to /api/tracks",
        }

    def list_tracks(self):
        """Return all tracks in the music library.

        Returns:
            flask.Response: JSON array of all track objects.
        """
        # jsonify creates a Response with the application/json content type.
        # Flask cannot serialize Track objects directly, so each one is
        # converted to a dict first.
        # https://flask.palletsprojects.com/en/stable/api/#flask.json.jsonify
        tracks = []
        for track in self.library.all_tracks():
            tracks.append(MusicLibraryServer._track_to_dict(track))
        return jsonify(tracks)

    def get_track(self, track_id: int):
        """Return a single track by its ID.

        Args:
            track_id: The integer ID of the track to retrieve.

        Returns:
            dict: The track object if found (200), or an error message (404).
        """
        track = self.library.get(track_id)
        if track is None:
            # Flask uses the second value in the tuple as the HTTP status.
            return {"error": f"Track {track_id} not found"}, 404

        # Flask converts the returned dict to JSON.
        return MusicLibraryServer._track_to_dict(track)

    def create_track(self):
        """Create a new track in the music library.

        Expects a JSON body with every field in ``Track.REQUIRED_FIELDS``: ``title``,
        ``artist``, ``recording``, ``genre``, ``released`` (YYYY-MM-DD),
        and ``duration``.

        Returns:
            tuple: A JSON object with a success message, the created track,
                and an echo of the received request (201). Returns an error
                on 400 if the body is missing, incomplete, or invalid.
        """
        # request refers to the current HTTP request. get_json parses its body.
        # With silent=True, invalid JSON or a non-JSON Content-Type returns
        # None instead of raising an error. JSON null also becomes None.
        # This lets the handler return its own 400 response and hint.
        # https://flask.palletsprojects.com/en/stable/api/#flask.request
        # https://flask.palletsprojects.com/en/stable/api/#flask.Request.get_json
        data = request.get_json(silent=True)

        if data is None:
            return {
                "error": "Request body must be JSON",
                "hint": "Use httpx.post(url, json={...}) — the json= parameter"
                "sets the Content-Type header and encodes the body for you",
            }, 400

        missing_fields = MusicLibraryServer._find_missing_fields(data)
        if missing_fields:
            return MusicLibraryServer._missing_fields_error(missing_fields), 400

        # Track raises ValueError for any invalid value, such as an empty
        # title or a negative duration. Report it to the client as a 400.
        try:
            new_track = self.library.add(
                title=data["title"],
                artist=data["artist"],
                recording=data["recording"],
                genre=data["genre"],
                released=MusicLibraryServer._parse_release_date(data["released"]),
                duration=data["duration"],
            )
        except ValueError as error:
            return {"error": str(error)}, 400

        # Flask converts the dict to JSON and uses 201 as the response status.
        # https://flask.palletsprojects.com/en/stable/quickstart/#about-responses
        return {
            "message": f"Track '{new_track.title}' created successfully",
            "track": MusicLibraryServer._track_to_dict(new_track),
            "echo": {
                "method": "POST",
                "url": "/api/tracks",
                "body_received": data,
            },
        }, 201

    def update_track(self, track_id: int):
        """Replace every field of an existing track, keeping its ID.

        As with ``create_track``, the JSON body must contain every field in
        ``Track.REQUIRED_FIELDS``. In REST, PUT replaces the whole resource.

        Args:
            track_id: The integer ID of the track to update.

        Returns:
            dict: A JSON object with a success message, the updated track,
                and an echo of the received request (200). Returns 404 if
                the track does not exist, or 400 if the body is not valid
                JSON, is missing a field, or contains an invalid value.
        """
        # As in create_track, silent=True lets this view return its own 400
        # response for invalid JSON or a non-JSON Content-Type.
        # https://flask.palletsprojects.com/en/stable/api/#flask.Request.get_json
        data = request.get_json(silent=True)

        if data is None:
            return {
                "error": "Request body must be JSON",
                "hint": "Use httpx.put(url, json={...}) — the json= parameter "
                "sets the Content-Type header and encodes the body for you",
            }, 400

        if self.library.get(track_id) is None:
            return {"error": f"Track {track_id} not found"}, 404

        missing_fields = MusicLibraryServer._find_missing_fields(data)
        if missing_fields:
            return MusicLibraryServer._missing_fields_error(missing_fields), 400

        try:
            track = self.library.update(
                track_id,
                title=data["title"],
                artist=data["artist"],
                recording=data["recording"],
                genre=data["genre"],
                released=MusicLibraryServer._parse_release_date(data["released"]),
                duration=data["duration"],
            )
        except ValueError as error:
            return {"error": str(error)}, 400

        if track is None:
            return {"error": f"Track {track_id} not found"}, 404

        # A returned dict becomes a JSON response with the default status 200.
        return {
            "message": f"Track {track_id} updated successfully",
            "track": MusicLibraryServer._track_to_dict(track),
            "echo": {
                "method": "PUT",
                "url": f"/api/tracks/{track_id}",
                "body_received": data,
            },
        }

    def delete_track(self, track_id: int):
        """Delete a track from the music library.

        Args:
            track_id: The integer ID of the track to delete.

        Returns:
            dict: A JSON object with a success message, the deleted track,
                and an echo of the received request (200). Returns 404 if
                the track does not exist.
        """
        deleted = self.library.remove(track_id)
        if deleted is None:
            return {"error": f"Track {track_id} not found"}, 404

        # Flask converts this dict to JSON, as it does for the other views.
        return {
            "message": f"Track '{deleted.title}' deleted successfully",
            "deleted_track": MusicLibraryServer._track_to_dict(deleted),
            "echo": {
                "method": "DELETE",
                "url": f"/api/tracks/{track_id}",
            },
        }


def create_app(library: MusicLibrary | None = None) -> Flask:
    """Build an application for the Flask CLI, production servers, or tests.

    Notes:
        `create_app` is an application factory: a function that builds and
        returns a configured Flask app.

        Each tool or application that uses it, imports the module, calls create_app,
        and then uses the returned application to process requests.

        Flask CLI (development):
            uv run flask --app music_library_server run --debug

            The --app option imports music_library_server, finds the
            function named create_app, calls it, and starts the development
            server with the returned app.

        Example Production WSGI servers:
            waitress-serve --call music_library_server:create_app

            The text before the colon is the module to import, and the text
            after it is the factory to call. The production server, not
            Flask, handles the network connections and runs several workers
            so it can serve many clients at once.

            Waitress is a production-quality WSGI server,
            it listens for and translates incoming HTTP requests from a web
            server into a standardized format that Python web applications can understand.

    Args:
        library: The library to serve. If None, use four sample tracks.

    Returns:
        Flask: The configured application.
    """
    # https://flask.palletsprojects.com/en/stable/patterns/appfactories/
    # https://flask.palletsprojects.com/en/stable/cli/#application-discovery
    # https://flask.palletsprojects.com/en/stable/deploying/waitress/
    if library is None:
        # Use the sample data if no music library is given
        library = build_seed_library()
    return MusicLibraryServer(library).app


def main():
    """Launch the development server with app.run."""
    # app.run starts Flask's development server. debug=True enables the
    # interactive debugger and reloads the server when code changes.
    # The development server is not for production.
    # https://flask.palletsprojects.com/en/stable/api/#flask.Flask.run
    create_app().run(debug=True)

    # Alternative: start the same server from a terminal with the Flask CLI.
    # --app finds the create_app factory in this module and run --debug
    # starts the development server with debugging. That command imports
    # this module but does not call main.
    #     uv run flask --app music_library_server run --debug
    # https://flask.palletsprojects.com/en/stable/cli/#run-the-development-server


# The Flask command  imports module to find create_app. This guard prevents the
# server from starting during that import and runs main only when executed.
# https://docs.python.org/3/library/__main__.html#idiomatic-usage
if __name__ == "__main__":
    main()
