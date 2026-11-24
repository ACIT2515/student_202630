"""An object-oriented client for the Music Library API."""

import httpx


class MusicLibraryClient:
    """A client for the Music Library API.

    Wraps an httpx.Client so callers can work with tracks instead of
    URLs, status codes, and JSON.
    """

    def __init__(self, server_url: str = "http://localhost:5000"):
        self._http = httpx.Client(base_url=server_url, timeout=10.0)

    def status(self) -> dict:
        """Return the server's health check information."""
        response = self._http.get("/api/status")
        response.raise_for_status()
        return response.json()

    def list_tracks(self) -> list[dict]:
        """Return all tracks in the library."""
        response = self._http.get("/api/tracks")
        response.raise_for_status()
        return response.json()

    def get_track(self, track_id: int) -> dict | None:
        """Return one track, or None if it does not exist."""
        response = self._http.get(f"/api/tracks/{track_id}")
        if response.status_code == 404:
            return None
        response.raise_for_status()
        return response.json()

    def create_track(
        self,
        title: str,
        artist: str,
        recording: str,
        genre: str,
        released: str,
        duration: float,
    ) -> dict:
        """Create a track and return it (including its server-assigned ID).

        Args:
            title: Name of the song.
            artist: Name of the artist.
            recording: Name of the album, EP, or single.
            genre: The type of music.
            released: The release date, as text in YYYY-MM-DD format.
            duration: Length of the track in seconds.
        """
        body = {
            "title": title,
            "artist": artist,
            "recording": recording,
            "genre": genre,
            "released": released,
            "duration": duration,
        }
        response = self._http.post("/api/tracks", json=body)
        response.raise_for_status()
        return response.json()["track"]

    def update_track(
        self,
        track_id: int,
        title: str,
        artist: str,
        recording: str,
        genre: str,
        released: str,
        duration: float,
    ) -> dict | None:
        """Replace every field of a track.

        Args:
            track_id: The ID of the track to update.
            title: Name of the song.
            artist: Name of the artist.
            recording: Name of the album, EP, or single.
            genre: The type of music.
            released: The release date, as text in YYYY-MM-DD format.
            duration: Length of the track in seconds.

        Returns:
            dict: The updated track, or None if it does not exist.
        """
        body = {
            "title": title,
            "artist": artist,
            "recording": recording,
            "genre": genre,
            "released": released,
            "duration": duration,
        }
        response = self._http.put(f"/api/tracks/{track_id}", json=body)
        if response.status_code == 404:
            return None
        response.raise_for_status()
        return response.json()["track"]

    def delete_track(self, track_id: int) -> bool:
        """Delete a track. Return True if deleted, False if it did not exist."""
        response = self._http.delete(f"/api/tracks/{track_id}")
        if response.status_code == 404:
            return False
        response.raise_for_status()
        return True

    def close(self) -> None:
        """Close the underlying HTTP connection."""
        self._http.close()

    def __enter__(self):
        """Return this client as the ``with`` statement's ``as`` target.

        A Python with statement calls ``__enter__`` when execution enters the with-block.
        See https://docs.python.org/3/reference/datamodel.html#with-statement-context-managers.
        """
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        """Close the connection when execution leaves the with-block.

        A Python with statement calls ``__exit__`` on normal exit and when an exception occurs. 
        Returning ``None`` means an exception is not suppressed. See
        https://docs.python.org/3/reference/datamodel.html#with-statement-context-managers.
        """
        self.close()

    def __len__(self):
        """Return the number of tracks on the server (optional challenge)."""
        return self.status()["track_count"]


def main():
    """Demonstrate the client with a full track lifecycle."""

    # The with statement calls __enter__ before this block and __exit__ when
    # the block ends, so the HTTP connection is closed even if an error occurs.
    with MusicLibraryClient() as music_library_client:
        print(music_library_client.status())

        for track in music_library_client.list_tracks():
            print(f"  [{track['id']}] {track['title']} — {track['artist']}")

        print(music_library_client.get_track(1))
        print(music_library_client.get_track(999))  # None

        new_track = music_library_client.create_track(
            title="Walkin' Blues",
            artist="Robert Johnson",
            recording="King of the Delta Blues Singers",
            genre="blues",
            released="1936-11-27",
            duration=230,
        )

        # PUT replaces the whole track, so every field is sent again.
        music_library_client.update_track(
            new_track["id"],
            title="Walkin' Blues",
            artist="Robert Johnson",
            recording="The Complete Recordings",
            genre="blues",
            released="1936-11-27",
            duration=233,
        )
        print(music_library_client.get_track(new_track["id"]))

        print(f"Tracks on server: {len(music_library_client)}")

        print(music_library_client.delete_track(new_track["id"]))  # True
        print(music_library_client.delete_track(new_track["id"]))  # False — already gone


if __name__ == "__main__":
    main()
