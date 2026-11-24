"""Unit tests for MusicLibrary, isolated from Track validation."""

from datetime import date

import pytest

import music_library


class FakeTrack:
    """A stand-in that stores track values without validating them."""

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
        """Store the values supplied by the library."""
        self.id = id
        self.title = title
        self.artist = artist
        self.recording = recording
        self.genre = genre
        self.released = released
        self.duration = duration


def reject_track(*_arguments, **_keyword_arguments):
    """Simulate a Track constructor rejecting its input."""
    # Accept any constructor arguments so the test focuses on the failure.
    raise ValueError("Simulated invalid track")


@pytest.fixture
def library(monkeypatch):
    """Create an empty library that uses FakeTrack."""
    # Replace Track where MusicLibrary looks it up; pytest restores it afterward.
    # https://docs.pytest.org/en/stable/how-to/monkeypatch.html
    monkeypatch.setattr(music_library, "Track", FakeTrack)
    return music_library.MusicLibrary()


@pytest.fixture
def track_data():
    """Provide fresh values for a track."""
    return {
        "title": "So What",
        "artist": "Miles Davis",
        "recording": "Kind of Blue",
        "genre": "jazz",
        "released": date(1959, 8, 17),
        "duration": 545,
    }


def test_new_library_is_empty(library):
    """A new library contains no tracks."""
    # The library starts with no stored tracks.
    assert len(library) == 0
    # Listing an empty library returns an empty list.
    assert library.all_tracks() == []


def test_add_tracks(library, track_data):
    """Adding tracks assigns IDs and stores the supplied values."""
    # **track_data passes the dictionary entries as named arguments.
    first = library.add(**track_data)
    second = library.add(**track_data)

    # Each new track receives the next available ID.
    assert first.id == 1
    # The second track receives a different, consecutive ID.
    assert second.id == 2
    # The library passes every supplied field to the track constructor.
    assert {
        "title": first.title,
        "artist": first.artist,
        "recording": first.recording,
        "genre": first.genre,
        "released": first.released,
        "duration": first.duration,
    } == track_data
    # A lookup returns the same track that was added.
    assert library.get(first.id) is first
    # Tracks are listed in the order they were added.
    assert library.all_tracks() == [first, second]
    # Both tracks count toward the library's length.
    assert len(library) == 2


def test_update_track(library, track_data):
    """Updating a track replaces its fields while keeping its ID."""
    original = library.add(**track_data)
    replacement_data = {
        "title": "All Blues",
        "artist": "Miles Davis Quintet",
        "recording": "Live Recording",
        "genre": "blues",
        "released": date(1960, 1, 1),
        "duration": 600,
    }

    updated = library.update(original.id, **replacement_data)

    # Updating an existing track returns the replacement.
    assert updated is not None
    # The replacement is a new object, not the original.
    assert updated is not original
    # Updating a track must not assign it a new ID.
    assert updated.id == original.id
    # Every field is taken from the replacement data.
    assert {
        "title": updated.title,
        "artist": updated.artist,
        "recording": updated.recording,
        "genre": updated.genre,
        "released": updated.released,
        "duration": updated.duration,
    } == replacement_data
    # Future lookups return the replacement, not the original object.
    assert library.get(original.id) is updated
    # Replacing a track does not change the number of tracks.
    assert len(library) == 1


def test_missing_track_operations(library, track_data):
    """Looking up, updating, or removing an unknown ID returns None."""
    original = library.add(**track_data)

    # An unknown ID cannot be found.
    assert library.get(99) is None
    # An update does not create a track for an unknown ID.
    assert library.update(99, **track_data) is None
    # Removing an unknown ID returns None.
    assert library.remove(99) is None
    # Operations on a missing ID leave existing tracks unchanged.
    assert library.all_tracks() == [original]


def test_remove_track(library, track_data):
    """Removing a track returns it and does not reuse its ID."""
    first = library.add(**track_data)
    second = library.add(**track_data)

    # Removing an existing track returns that track.
    assert library.remove(first.id) is first
    # The removed track is no longer available.
    assert library.get(first.id) is None
    # Other tracks remain in the library.
    assert library.all_tracks() == [second]
    # Removing a track reduces the library's length.
    assert len(library) == 1

    later = library.add(**track_data)
    # A later track receives a new ID instead of the removed track's ID.
    assert later.id == 3


def test_failed_add_does_not_use_an_id(library, track_data, monkeypatch):
    """A failed track creation leaves the library and next ID unchanged."""
    original = library.add(**track_data)
    # Simulate the track constructor raising an error.
    monkeypatch.setattr(music_library, "Track", reject_track)

    # The library passes the constructor's error to the caller.
    with pytest.raises(ValueError, match="Simulated invalid track"):
        library.add(**track_data)

    # The failed add leaves the existing library unchanged.
    assert library.all_tracks() == [original]

    monkeypatch.setattr(music_library, "Track", FakeTrack)
    next_track = library.add(**track_data)
    # The failed add did not consume the next available ID.
    assert next_track.id == 2


def test_failed_update_leaves_track_unchanged(library, track_data, monkeypatch):
    """A failed replacement leaves the original track in the library."""
    original = library.add(**track_data)
    replacement_data = track_data.copy()
    replacement_data["title"] = "All Blues"
    # Simulate the track constructor raising an error during an update.
    monkeypatch.setattr(music_library, "Track", reject_track)

    # The library passes the constructor's error to the caller.
    with pytest.raises(ValueError, match="Simulated invalid track"):
        library.update(original.id, **replacement_data)

    # A failed update keeps the original object in the library.
    assert library.get(original.id) is original
    # A failed update does not change the original track's title.
    assert original.title == track_data["title"]
    # A failed update does not change the number of tracks.
    assert len(library) == 1
