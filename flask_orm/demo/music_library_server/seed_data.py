"""Build a music library pre-loaded with sample tracks."""

from datetime import date

from music_library import MusicLibrary


def build_seed_library() -> MusicLibrary:
    """Return a MusicLibrary pre-loaded with sample tracks.

    Seeding through add() means the library assigns the IDs (1-4) and
    its internal counter is already correct for the next POST.

    Returns:
        MusicLibrary: A library containing four sample tracks.
    """
    library = MusicLibrary()
    library.add(
        title="Makeshift Patriot",
        artist="Sage Francis",
        recording="Sick of Raging War",
        genre="rap",
        released=date(2002, 1, 1),
        duration=710,
    )
    library.add(
        title="So What",
        artist="Miles Davis",
        recording="Kind of Blue",
        genre="jazz",
        released=date(1959, 8, 17),
        duration=545,
    )
    library.add(
        title="Bootleg Rascal",
        artist="Sticky Fingers",
        recording="Caress Your Soul",
        genre="rock",
        released=date(2013, 4, 15),
        duration=227,
    )
    library.add(
        title="Colors",
        artist="Black Pumas",
        recording="Black Pumas",
        genre="soul",
        released=date(2019, 6, 21),
        duration=246,
    )
    return library
