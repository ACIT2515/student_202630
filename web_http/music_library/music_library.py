"""
MusicLibrary — A practice API for learning http python consumption

This server manages a simple music library of tracks. It validates all
incoming requests and song and server info,
It includes a "echo" object that shows exactly what the server received.


Each track has the following attributes:
    id        — number, the track ID (assigned by the server)
    title     — string, name of the song
    artist    — string, the name of the artist
    recording — string, name of the album, EP, or single
    genre     — string, the type of music
    released  — string, the release date of the track (YYYY-MM-DD)
    duration  — number, length of the sound in seconds

Tracks are stored in memory as instances of the ``Track`` dataclass,
, and converted to plain dicts with ``dataclasses.asdict`` when sent as JSON.

The app is built with the ``create_app`` factory, which takes the
``Library`` to serve. Tests can call ``create_app(Library())`` to get a
fresh, isolated app; running this file serves a pre-seeded library.

Run with:
    uv run python music_library.py

Endpoints:
    GET    /api/status          — Server health check
    GET    /api/tracks          — List all tracks
    GET    /api/tracks/<id>     — Get one track by ID
    POST   /api/tracks          — Create a new track (requires JSON with
                                  "title" and "artist")
    PUT    /api/tracks/<id>     — Replace an existing track (full update)
    DELETE /api/tracks/<id>     — Delete a track
"""

from dataclasses import asdict, dataclass

from flask import Flask, jsonify, request


@dataclass
class Track:
    """A single track in the music library.

    Attributes:
        id: The track ID, assigned by the server.
        title: Name of the song.
        artist: The name of the artist.
        recording: Name of the album, EP, or single.
        genre: The type of music.
        released: The release date of the track (YYYY-MM-DD).
        duration: Length of the sound in seconds.
    """

    id: int
    title: str
    artist: str
    recording: str = "unknown"
    genre: str = "unknown"
    released: str = "unknown"
    duration: int = 0


# Fields a client may set on a track (id is assigned by the library).
# Must match the Track dataclass fields above.
TRACK_FIELDS = ("title", "artist", "recording", "genre", "released", "duration")


class Library:
    """An in-memory collection of tracks, keyed by track ID.

    The library owns ID assignment: ``add`` creates each ``Track`` with
    the next available ID, the way a database assigns primary keys. The
    dict keyed by ID gives O(1) lookup, update, and delete.
    """

    def __init__(self):
        self._tracks: dict[int, Track] = {}
        self._next_id = 1

    def add(self, title: str, artist: str, **extras) -> Track:
        """Create a track, assign it the next ID, and store it.

        Args:
            title: Name of the song.
            artist: The name of the artist.
            **extras: Any other Track fields (recording, genre, released,
                duration). Omitted fields use the Track defaults.

        Returns:
            Track: The newly created track, including its assigned ID.
        """
        track = Track(id=self._next_id, title=title, artist=artist, **extras)
        self._tracks[track.id] = track
        self._next_id += 1
        return track

    def get(self, track_id: int) -> Track | None:
        """Return the track with the given ID, or None if not found."""
        return self._tracks.get(track_id)

    def update(self, track_id: int, changes: dict) -> Track | None:
        """Apply changes to an existing track.

        Args:
            track_id: The ID of the track to update.
            changes: A dict of field names to new values. Only keys in
                TRACK_FIELDS are applied; anything else is ignored.

        Returns:
            Track: The updated track, or None if the ID is not found.
        """
        track = self._tracks.get(track_id)
        if track is None:
            return None
        for field in TRACK_FIELDS:
            if field in changes:
                setattr(track, field, changes[field])
        return track

    def remove(self, track_id: int) -> Track | None:
        """Remove and return the track with the given ID, or None if not found."""
        return self._tracks.pop(track_id, None)

    def all_tracks(self) -> list[Track]:
        """Return all tracks as a list, in the order they were added."""
        return list(self._tracks.values())

    def __len__(self):
        """Return the number of tracks, so len(library) works."""
        return len(self._tracks)


# ── Application factory ─────────────────────────────────────────
def create_app(library: Library) -> Flask:
    """Build and return a Flask app serving the given music library.

    The library is injected rather than created here, so tests can
    build an app around an empty or specially prepared Library. The
    route functions below reach the library through a closure.

    Args:
        library: The Library instance the app's routes will serve.

    Returns:
        Flask: The configured application.
    """
    app = Flask(__name__)

    # ── Health check ────────────────────────────────────────────
    @app.route("/api/status")
    def status():
        """Return server health check information.

        Returns:
            dict: JSON with server status, track count, and a welcome message.
        """
        return {
            "status": "online",
            "track_count": len(library),
            "message": "Echo server is running. Send requests to /api/tracks",
        }


    # ── READ ────────────────────────────────────────────────────
    @app.route("/api/tracks", methods=["GET"])
    def list_tracks():
        """Return all tracks in the music library.

        Returns:
            flask.Response: JSON array of all track objects.
        """
        # Flask's JSON provider serializes dataclasses automatically
        return jsonify(library.all_tracks())

    @app.route("/api/tracks/<int:track_id>", methods=["GET"])
    def get_track(track_id):
        """Return a single track by its ID.

        Args:
            track_id: The integer ID of the track to retrieve.

        Returns:
            dict: The track object if found (200), or an error message (404).
        """
        track = library.get(track_id)
        if track is None:
            return {"error": f"Track {track_id} not found"}, 404
        return asdict(track)


    # ── CREATE ──────────────────────────────────────────────────
    @app.route("/api/tracks", methods=["POST"])
    def create_track():
        """Create a new track in the music library.

        Expects a JSON body with at least ``title`` and ``artist`` fields.
        Optional fields are ``recording``, ``genre``, and ``released``
        (each defaults to ``"unknown"``) and ``duration`` (defaults to ``0``).

        Returns:
            tuple: A JSON object with a success message, the created track,
                and an echo of the received request (201). Returns an error
                with a hint on 400 if the body is missing or invalid.
        """
        # silent=True returns None for a missing or invalid JSON body instead
        # of letting Flask raise its own 415/400, so the hint below is sent
        data = request.get_json(silent=True)

        if data is None:
            return {
                "error": "Request body must be JSON",
                "hint": "Use httpx.post(url, json={...}) — the json= parameter "
                "sets the Content-Type header and encodes the body for you",
            }, 400

        for required in ("title", "artist"):
            if required not in data:
                return {
                    "error": f"Missing required field: {required}",
                    "hint": 'Send JSON with at least "title" and "artist" '
                    'fields, e.g. json={"title": "My Song", "artist": "My Band"}',
                }, 400

        # Pass along only the optional fields the client provided; any field
        # left out falls back to the Track dataclass default
        extras = {}
        for field in ("recording", "genre", "released", "duration"):
            if field in data:
                extras[field] = data[field]
        new_track = library.add(title=data["title"], artist=data["artist"], **extras)

        return {
            "message": f"Track '{new_track.title}' created successfully",
            "track": asdict(new_track),
            "echo": {
                "method": "POST",
                "url": "/api/tracks",
                "body_received": data,
            },
        }, 201


    # ── UPDATE ──────────────────────────────────────────────────
    @app.route("/api/tracks/<int:track_id>", methods=["PUT"])
    def update_track(track_id):
        """Replace an existing track (full update).

        Accepts a JSON body with any combination of ``title``, ``artist``,
        ``recording``, ``genre``, ``released``, and ``duration``. Only the
        provided fields are updated.

        Args:
            track_id: The integer ID of the track to update.

        Returns:
            dict: A JSON object with a success message, the updated track,
                and an echo of the received request (200). Returns 404 if
                the track does not exist, or 400 if the body is not valid
                JSON.
        """
        # silent=True returns None for a missing or invalid JSON body instead
        # of letting Flask raise its own 415/400, so the hint below is sent
        data = request.get_json(silent=True)

        if data is None:
            return {
                "error": "Request body must be JSON",
                "hint": "Use httpx.put(url, json={...}) — the json= parameter "
                "sets the Content-Type header and encodes the body for you",
            }, 400

        track = library.update(track_id, data)
        if track is None:
            return {"error": f"Track {track_id} not found"}, 404

        return {
            "message": f"Track {track_id} updated successfully",
            "track": asdict(track),
            "echo": {
                "method": "PUT",
                "url": f"/api/tracks/{track_id}",
                "body_received": data,
            },
        }


    # ── DELETE ──────────────────────────────────────────────────
    @app.route("/api/tracks/<int:track_id>", methods=["DELETE"])
    def delete_track(track_id):
        """Delete a track from the music library.

        Args:
            track_id: The integer ID of the track to delete.

        Returns:
            dict: A JSON object with a success message, the deleted track,
                and an echo of the received request (200). Returns 404 if
                the track does not exist.
        """
        deleted = library.remove(track_id)
        if deleted is None:
            return {"error": f"Track {track_id} not found"}, 404

        return {
            "message": f"Track '{deleted.title}' deleted successfully",
            "deleted_track": asdict(deleted),
            "echo": {
                "method": "DELETE",
                "url": f"/api/tracks/{track_id}",
            },
        }

    return app


# ── Seed data ───────────────────────────────────────────────────
def build_seed_library() -> Library:
    """Return a Library pre-loaded with sample tracks.

    Seeding through add() means the library assigns the IDs (1-4) and
    its internal counter is already correct for the next POST.

    Returns:
        Library: A library containing four sample tracks.
    """
    library = Library()
    library.add(
        title="Makeshift Patriot",
        artist="Sage Francis",
        recording="Sick of Raging War",
        genre="rap",
        released="2002-01-01",
        duration=710,
    )
    library.add(
        title="So What",
        artist="Miles Davis",
        recording="Kind of Blue",
        genre="jazz",
        released="1959-08-17",
        duration=545,
    )
    library.add(
        title="Bootleg Rascal",
        artist="Sticky Fingers",
        recording="Caress Your Soul",
        genre="rock",
        released="2013-04-15",
        duration=227,
    )
    library.add(
        title="Colors",
        artist="Black Pumas",
        recording="Black Pumas",
        genre="soul",
        released="2019-06-21",
        duration=246,
    )
    return library


# ── Startup ─────────────────────────────────────────────────────
def main():
    """Serve a pre-seeded music library on localhost:5000."""
    print("=" * 60)
    print("  Echo Server — Music library practice API for httpx exercises")
    print("  Endpoints:")
    print("    GET    http://localhost:5000/api/status")
    print("    GET    http://localhost:5000/api/tracks")
    print("    GET    http://localhost:5000/api/tracks/<id>")
    print("    POST   http://localhost:5000/api/tracks")
    print("    PUT    http://localhost:5000/api/tracks/<id>")
    print("    DELETE http://localhost:5000/api/tracks/<id>")
    print("=" * 60)
    app = create_app(build_seed_library())
    app.run(host="localhost", port=5000, debug=True)


if __name__ == "__main__":
    main()
