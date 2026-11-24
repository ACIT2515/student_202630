"""The Track class: a single track in the music library."""

from datetime import date


class Track:
    """A single track in the music library.

    Each editable attribute is a property. Its setter checks the new value,
    so a Track can never hold invalid data, whether the value is set in
    __init__ or assigned later.

    Attributes:
        id: The track ID, assigned by the library. Read-only.
        title: Name of the song.
        artist: The name of the artist.
        recording: Name of the album, EP, or single.
        genre: The type of music.
        released: The release date of the track.
        duration: Length of the track in seconds.
    """

    # Fields a client must send to create or update a track.
    REQUIRED_FIELDS = ("title", "artist", "recording", "genre", "released", "duration")

    def __init__(
        self,
        id: int,
        title: str,
        artist: str,
        recording: str,
        genre: str,
        released: date,
        duration: float,
    ):
        """Create a track, validating every value.

        Every field is required; there are no default values.

        Raises:
            ValueError: If any value is invalid.
        """
        if not isinstance(id, int) or id <= 0:
            raise ValueError("id must be an integer greater than zero")
        self._id = id

        # Each assignment below calls the matching property setter.
        self.title = title
        self.artist = artist
        self.recording = recording
        self.genre = genre
        self.released = released
        self.duration = duration

    @property
    def id(self) -> int:
        """The track ID. It has no setter, so it cannot be changed."""
        return self._id

    @property
    def title(self) -> str:
        """Name of the song."""
        return self._title

    @title.setter
    def title(self, value: str):
        self._title = _check_text("title", value)

    @property
    def artist(self) -> str:
        """The name of the artist."""
        return self._artist

    @artist.setter
    def artist(self, value: str):
        self._artist = _check_text("artist", value)

    @property
    def recording(self) -> str:
        """Name of the album, EP, or single."""
        return self._recording

    @recording.setter
    def recording(self, value: str):
        self._recording = _check_text("recording", value)

    @property
    def genre(self) -> str:
        """The type of music."""
        return self._genre

    @genre.setter
    def genre(self, value: str):
        self._genre = _check_text("genre", value)

    @property
    def released(self) -> date:
        """The release date."""
        return self._released

    @released.setter
    def released(self, value: date):
        if not isinstance(value, date):
            raise ValueError("released must be a date")
        self._released = value

    @property
    def duration(self) -> float:
        """Length of the track in seconds."""
        return self._duration

    @duration.setter
    def duration(self, value: float):
        # bool is excluded because True and False are also ints in Python.
        is_number = isinstance(value, (int, float)) and not isinstance(value, bool)
        if not is_number or value <= 0:
            raise ValueError("duration must be a number greater than zero")
        self._duration = value

    def to_dict(self) -> dict:
        """Return the track's values as a plain dict."""
        return {
            "id": self.id,
            "title": self.title,
            "artist": self.artist,
            "recording": self.recording,
            "genre": self.genre,
            "released": self.released,
            "duration": self.duration,
        }

    def __repr__(self) -> str:
        """Return a readable description for printing and debugging."""
        return f"Track(id={self.id}, title={self.title!r}, artist={self.artist!r})"


def _check_text(field: str, value: str) -> str:
    """Return value if it is a non-blank string, otherwise raise ValueError."""
    if not isinstance(value, str) or value.strip() == "":
        raise ValueError(f"{field} must be a non-empty string")
    return value
