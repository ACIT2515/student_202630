import string
import sys


def parse_arguments(arguments: list[str]) -> tuple[str, str]:
    """Parse a simplified sys.argv-style command line.

    The CLI accepts a positional input string and zero or one operation flag.
    If no flag is provided, the default operation is histogram.
    """
    if not arguments:
        raise SystemExit(
            'Usage: python frequency_analysis.py "input string" [-c | --chars | -l | --letters | -g | --histogram]'
        )

    if arguments[0] in {"-h", "--help"}:
        print(
            'Usage: python frequency_analysis.py "input string" [-c | --chars | -l | --letters | -g | --histogram]'
        )
        raise SystemExit(0)

    input_text = arguments[0]
    operation = "histogram"

    if len(arguments) > 2:
        raise SystemExit("Error: provide at most one operation flag.")

    if len(arguments) == 2:
        flag = arguments[1]
        if flag in {"-c", "--chars"}:
            operation = "chars"
        elif flag in {"-l", "--letters"}:
            operation = "letters"
        elif flag in {"-g", "--histogram"}:
            operation = "histogram"
        else:
            raise SystemExit(f"Error: unknown flag: {flag}")

    return input_text, operation


def char_freq(in_string: str) -> dict[str, int]:
    """Convert input string to a dictionary of letter frequencies

    Args:
        string characters to calculate frequencies for

    Returns:
        A dict mapping the character to the number of times it appears
    """
    letter_freq = {}
    in_string = "".join(sorted(in_string))
    for letter in in_string:

        if letter not in letter_freq:
            letter_freq[letter] = 1
        else:
            letter_freq[letter] += 1

    return letter_freq


def histogram(in_string):
    """Generate a histogram of letters for each letter in the in input string

    Args:
        in_string:  input string to used to generate letter frequency histogram

    Returns:
        string with leading with the letter followed a star for each time the
        letter appears in the input string

    """

    lt_frq = letter_freq(in_string)
    return_string = ""
    for letter, freq in lt_frq.items():
        return_string += f"{letter} {'*' * int(freq)}\n"

    return return_string


def letter_freq(in_string):
    """Convert input string to a dictionary of letter frequencies,
    after removing punctuation and spaces. Counts upper and lower case
    letters together.

    Args:
        in_string: string to count the letter frequencies of

    Returns:
       dict mapping letter in string to the number of occurrences in input
    """

    letters_to_remove = set(string.punctuation + " ")
    clean_string = ""

    for char in in_string:
        if char not in letters_to_remove:
            clean_string += char.lower()

    letter_freq = char_freq(clean_string)

    return letter_freq


def main() -> None:
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
