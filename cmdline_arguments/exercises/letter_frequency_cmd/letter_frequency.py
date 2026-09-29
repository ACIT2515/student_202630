"""Count characters and letters from a command-line input string."""

import string
import sys


def parse_arguments(arguments: list[str]) -> tuple[str, str]:
    """Parse a simplified ``sys.argv``-style command line.

    Args:
        arguments: Command-line arguments excluding the program name. The
            first argument is the input string, followed by an optional
            operation flag.

    Returns:
        A tuple containing the input string and the selected operation name.

    Raises:
        SystemExit: If the input is missing, a flag is invalid, or more than
            one operation flag is provided. ``-h`` exits successfully.
    """
    usage = 'Usage: python letter_frequency.py "input string" [-c | -l | -g]'

    if not arguments:
        raise SystemExit(usage)

    if arguments[0] == "-h":
        print(usage)
        raise SystemExit(0)

    input_text = arguments[0]
    operation = "histogram"

    if len(arguments) > 2:
        raise SystemExit("Error: provide at most one operation flag.")

    if len(arguments) == 2:
        flag = arguments[1]
        if flag == "-c":
            operation = "chars"
        elif flag == "-l":
            operation = "letters"
        elif flag == "-g":
            operation = "histogram"
        else:
            raise SystemExit(f"Error: unknown flag: {flag}")

    return input_text, operation


def char_freq(in_string: str) -> dict[str, int]:
    """Count occurrences of each character in a string.

    Args:
        in_string: String whose characters should be counted.

    Returns:
        A dictionary mapping each character to its number of occurrences.
    """
    letter_freq = {}
    in_string = "".join(sorted(in_string))
    for letter in in_string:

        if letter not in letter_freq:
            letter_freq[letter] = 1
        else:
            letter_freq[letter] += 1

    return letter_freq


def histogram(in_string: str) -> str:
    """Format a letter-frequency histogram for a string.

    Args:
        in_string: String whose letters should be included in the histogram.

    Returns:
        A newline-terminated string with one line per letter. Each line
        contains the lowercase letter followed by one asterisk per occurrence.
    """

    lt_frq = letter_freq(in_string)
    return_string = ""
    for letter, freq in lt_frq.items():
        return_string += f"{letter} {'*' * int(freq)}\n"

    return return_string


def letter_freq(in_string: str) -> dict[str, int]:
    """Count letters without spaces or punctuation, ignoring case.

    Args:
        in_string: String whose letters should be counted.

    Returns:
        A dictionary mapping each lowercase character to its number of
        occurrences. Digits and other non-punctuation characters are retained.
    """

    letters_to_remove = set(string.punctuation + " ")
    clean_string = ""

    for char in in_string:
        if char not in letters_to_remove:
            clean_string += char.lower()

    letter_freq = char_freq(clean_string)

    return letter_freq


def main() -> None:
    """Run the command-line frequency analysis application."""
    try:
        in_string, operation = parse_arguments(sys.argv[1:])
    except SystemExit as error:
        if isinstance(error, SystemExit) and error.code not in (0, 1, 2):
            print(error)
        raise

    if operation == "chars":
        out_string = char_freq(in_string)
    elif operation == "letters":
        out_string = letter_freq(in_string)
    else:
        out_string = histogram(in_string)

    print(f'Input: "{in_string}"\n\n')
    print(out_string)


if __name__ == "__main__":
    main()
