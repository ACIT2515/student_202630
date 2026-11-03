"""Shared utility helpers"""


def describe(obj) -> str:
    """Return the first non-empty line of obj's docstring as a one-line summary.

    Accepts any object with a docstring: a class, an instance, or a bound method.
    Reads the ``__doc__`` dunder attribute that Python attaches to every class,
    function, and method at definition time.

    Args:
        obj: Any object whose ``__doc__`` should be summarised.

    Returns:
        str: First non-empty line of the docstring, or
            ``'No description available.'`` if none exists.

    """
    doc = obj.__doc__
    if not doc:
        raise AttributeError(
            " A Docstring is required for displaying the object's description"
        )

    for line in doc.splitlines():
        stripped = line.strip()
        if stripped:
            return stripped
    raise AttributeError(
        "A Docstring is required for displaying the object's description"
    )


def separator(char: str = "=", width: int = 60) -> None:
    """Print a repeated-character separator line."""
    print(char * width)


def prompt_int(prompt: str, low: int, high: int) -> int:
    """Prompt the user until they enter an integer in [low, high]."""
    while True:
        try:
            value = int(input(prompt))
            if low <= value <= high:
                return value
        except ValueError:
            pass
        print(f"  Please enter a number between {low} and {high}.")
