"""Count characters and letters in strings and display their frequencies
as a histogram."""

import string


def character_count(input_string: str) -> dict[str, int]:
    """Count each character in a string.

    Args:
        input_string: The string whose characters will be counted.

    Returns:
        A dictionary mapping each character to its number of occurrences.
    """
    letter_count = {}
    for letter in input_string:
        if letter not in letter_count:
            letter_count[letter] = 1
        else:
            letter_count[letter] += 1

    return letter_count


def letter_count(input_string: str) -> dict[str, int]:
    """Count letters after normalizing a string.

    Spaces and punctuation are removed, and all remaining characters are
    converted to lowercase before they are counted.

    Args:
        input_string: The string whose letters will be counted.

    Returns:
        A dictionary mapping each lowercase character to its number of
        occurrences.
    """
    char_to_remove = set(string.punctuation + " ")

    # remove unwanted characters from input string
    clean_chars = ""
    for letter in input_string:
        if letter not in char_to_remove:
            clean_chars = clean_chars + letter.lower()
    letter_count = character_count(clean_chars)
    return letter_count


def histogram(letter_count: dict[str, int]) -> str:
    """Create a text histogram from character counts.

    Args:
        letter_count: A dictionary mapping characters to occurrence counts.

    Returns:
        A string with one histogram row per dictionary entry.
    """
    hist_str = ""
    for letter, count in letter_count.items():
        hist_str = hist_str + (f"{letter} {count * "*"}\n")
    return hist_str


def main():
    """Display character counts and a histogram for a sample string."""
    TEST_STRING = "This is a test!!"
    count_functions = [character_count, letter_count]
    for func in count_functions:
        print(f"Name: {func.__name__}")
        characters = func(TEST_STRING)
        print(characters)
        # sorted returns a list of tuples that needs to be converted back to a dictionary
        sorted_chars = dict(sorted(characters.items()))
        print(histogram(sorted_chars))
        print("\n\n")


if __name__ == "__main__":
    main()
