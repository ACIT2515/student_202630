"""The Library class: an in-memory collection of tracks."""

from datetime import date

from track import Track


class MusicLibrary:
    """An in-memory collection of tracks, keyed by track ID.

    The library owns ID assignment: ``add`` creates each ``Track`` with
    the next available ID, the way a database assigns primary keys. The
    dict keyed by ID speeds up lookup, update, and delete.
    """

    def __init__(self):
        self._tracks: dict[int, Track] = {}
        self._next_id = 1

    def add(
        self,
        title: str,
        artist: str,
        recording: str,
        genre: str,
        released: date,
        duration: float,
    ) -> Track:
        """Create a track, assign it the next ID, and store it.

        Args:
            title: Name of the song.
            artist: The name of the artist.
            recording: Name of the album, EP, or single.
            genre: The type of music.
            released: The release date of the track.
            duration: Length of the track in seconds.

        Returns:
            Track: The newly created track, including its assigned ID.

        Raises:
            ValueError: If any value is invalid. No ID is used up.
        """
        track = Track(
            id=self._next_id,
            title=title,
            artist=artist,
            recording=recording,
            genre=genre,
            released=released,
            duration=duration,
        )
        self._tracks[track.id] = track
        self._next_id += 1
        return track

    def get(self, track_id: int) -> Track | None:
        """Return the track with the given ID, or None if not found."""
        return self._tracks.get(track_id)

    def update(
        self,
        track_id: int,
        title: str,
        artist: str,
        recording: str,
        genre: str,
        released: date,
        duration: float,
    ) -> Track | None:
        """Replace every field of an existing track, keeping its ID.

        A new Track is created first, so an invalid value raises
        ValueError and leaves the stored track unchanged.

        Args:
            track_id: The ID of the track to update.
            title: Name of the song.
            artist: The name of the artist.
            recording: Name of the album, EP, or single.
            genre: The type of music.
            released: The release date of the track.
            duration: Length of the track in seconds.

        Returns:
            Track: The updated track, or None if the ID is not found.

        Raises:
            ValueError: If any value is invalid.
        """
        if track_id not in self._tracks:
            return None

        updated = Track(
            id=track_id,
            title=title,
            artist=artist,
            recording=recording,
            genre=genre,
            released=released,
            duration=duration,
        )
        self._tracks[track_id] = updated
        return updated

    def remove(self, track_id: int) -> Track | None:
        """Remove and return track with the given ID, or None if not found."""
        return self._tracks.pop(track_id, None)

    def all_tracks(self) -> list[Track]:
        """Return all tracks as a list, in the order they were added."""
        return list(self._tracks.values())

    def __len__(self):
        """Return the number of tracks, so len(library) works."""
        return len(self._tracks)
