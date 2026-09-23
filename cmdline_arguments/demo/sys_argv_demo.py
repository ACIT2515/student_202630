"""sys.argv demonstration showing common CLI patterns.

This module mirrors uses Python's built-in sys.argv
list to show how to access command line prompts.

It demonstrates:
- positional arguments
- mutually exclusive CLI flags
- validation of user input
- help output using simple command-line checking
"""

import sys


def print_usage() -> None:
    """Display a short usage message for the CLI demo."""
    print("Usage: python sys_argv_demo.py <input_text> [options]")
    print()
    print("Options:")
    print("  -u, --upper      Convert text to uppercase")
    print("  -l, --lower      Convert text to lowercase")
    print("  -r, --reverse    Reverse the text")
    print("  -h, --help       Show this help message")


def process_uppercase(text: str) -> str:
    """Convert text to uppercase."""
    return text.upper()


def process_lowercase(text: str) -> str:
    """Convert text to lowercase."""
    return text.lower()


def process_reverse(text: str) -> str:
    """Reverse the input text."""
    return text[::-1]


def parse_arguments(arguments: list[str]) -> tuple[str, str]:
    """Parse the CLI arguments.

    Args:
        arguments: The command-line arguments excluding the script name.

    Returns:
        A tuple containing the input text and the selected operation name.

    Raises:
        SystemExit: If the command line is invalid or the help flag is used.
    """
    if not arguments or any(arg in {"-h", "--help"} for arg in arguments):
        print_usage()
        raise SystemExit(0)

    positional_values: list[str] = []
    selected_operations: list[str] = []

    for argument in arguments:
        if argument in {"-u", "--upper"}:
            selected_operations.append("upper")
        elif argument in {"-l", "--lower"}:
            selected_operations.append("lower")
        elif argument in {"-r", "--reverse"}:
            selected_operations.append("reverse")
        elif argument.startswith("-"):
            print(f"Error: unknown option: {argument}")
            print_usage()
            raise SystemExit(2)
        else:
            positional_values.append(argument)

    if len(positional_values) != 1:
        print("Error: you must provide exactly one input_text value.")
        print_usage()
        raise SystemExit(2)

    if len(selected_operations) > 1:
        print("Error: choose only one operation flag.")
        print_usage()
        raise SystemExit(2)

    operation = selected_operations[0] if selected_operations else "no operation"
    return positional_values[0], operation


def main() -> None:
    """Run the sys.argv demonstration."""
    try:
        input_text, operation = parse_arguments(sys.argv[1:])
    except SystemExit:
        raise

    if operation == "upper":
        result = process_uppercase(input_text)
    elif operation == "lower":
        result = process_lowercase(input_text)
    elif operation == "reverse":
        result = process_reverse(input_text)
    else:
        result = input_text

    print(f"Input: '{input_text}'")
    print(f"Operation: {operation}")
    print(f"Result: '{result}'")


if __name__ == "__main__":
    main()
