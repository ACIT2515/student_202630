"""Tests for the Track class."""

from datetime import date

import pytest

from track import Track


@pytest.fixture
def track() -> Track:
    """Create a valid track for each test."""
    return Track(
        id=1,
        title="So What",
        artist="Miles Davis",
        recording="Kind of Blue",
        genre="jazz",
        released=date(1959, 8, 17),
        duration=545,
    )


def test_create_track(track):
    """A valid track contains all the supplied values."""
    # to_dict keeps the release date as a Python date, not JSON text.
    assert track.to_dict() == {
        "id": 1,
        "title": "So What",
        "artist": "Miles Davis",
        "recording": "Kind of Blue",
        "genre": "jazz",
        "released": date(1959, 8, 17),
        "duration": 545,
    }


def test_update_track_properties(track):
    """Valid values can be assigned after a track is created."""
    track.title = "All Blues"
    track.released = date(1959, 8, 18)
    track.duration = 12.5

    # Each property should retain its newly assigned value.
    assert track.title == "All Blues"
    # A release date remains a date after an update.
    assert track.released == date(1959, 8, 18)
    # Positive fractional durations are allowed.
    assert track.duration == 12.5


def test_text_properties_reject_blank_values(track):
    """Every text property rejects empty or whitespace-only strings."""
    original = track.to_dict()

    # pytest.raises checks that an invalid assignment raises ValueError.
    with pytest.raises(ValueError, match="title must be a non-empty string"):
        track.title = ""
    # Whitespace alone is not a valid artist.
    with pytest.raises(ValueError, match="artist must be a non-empty string"):
        track.artist = "   "
    # A recording must not be empty.
    with pytest.raises(ValueError, match="recording must be a non-empty string"):
        track.recording = ""
    # A genre must not be empty.
    with pytest.raises(ValueError, match="genre must be a non-empty string"):
        track.genre = ""

    # Rejected assignments must leave the track unchanged.
    assert track.to_dict() == original


@pytest.mark.parametrize("value", [0, -1, "545", True])
def test_duration_must_be_a_positive_number(track, value):
    """Zero, negative, text, and boolean durations are invalid."""
    # Each invalid value must be rejected by the duration setter.
    with pytest.raises(ValueError, match="duration must be a number greater than zero"):
        track.duration = value

    # A rejected duration must not replace the previous value.
    assert track.duration == 545


@pytest.mark.parametrize("value", [None, "1959-08-17"])
def test_release_date_must_be_a_date(track, value):
    """A release date cannot be None or a string."""
    # The Track class expects a date object, not API-formatted text.
    with pytest.raises(ValueError, match="released must be a date"):
        track.released = value

    # A rejected date must not replace the previous value.
    assert track.released == date(1959, 8, 17)


@pytest.mark.parametrize("invalid_id", [0, -1, "1"])
def test_id_must_be_a_positive_integer(invalid_id):
    """A track ID must be a positive integer."""
    # The constructor must reject an invalid ID.
    with pytest.raises(ValueError, match="id must be an integer greater than zero"):
        Track(
            id=invalid_id,
            title="So What",
            artist="Miles Davis",
            recording="Kind of Blue",
            genre="jazz",
            released=date(1959, 8, 17),
            duration=545,
        )


def test_id_cannot_be_changed(track):
    """The ID is read-only after construction."""
    # Assigning to the read-only ID property must fail.
    with pytest.raises(AttributeError):
        track.id = 2

    # The original ID remains unchanged.
    assert track.id == 1


def test_constructor_rejects_invalid_duration():
    """The constructor validates values as well as later assignments."""
    # An invalid duration must prevent the Track from being created.
    with pytest.raises(ValueError, match="duration must be a number greater than zero"):
        Track(
            id=1,
            title="So What",
            artist="Miles Davis",
            recording="Kind of Blue",
            genre="jazz",
            released=date(1959, 8, 17),
            duration=0,
        )

