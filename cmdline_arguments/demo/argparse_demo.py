"""Argparse demonstration showing common CLI patterns.

This module demonstrates:
- Positional arguments
- Mutually exclusive argument groups
- Different action types (store_true, store_false)
- Help text and descriptions

References:
    - Argparse Tutorial: https://docs.python.org/3/howto/argparse.html
    - Argparse Documentation: https://docs.python.org/3/library/argparse.html
"""

import argparse


def process_uppercase(text: str) -> str:
    """Convert text to uppercase.

    Args:
        text: The input string to convert.

    Returns:
        The input string converted to uppercase.
    """
    return text.upper()


def process_lowercase(text: str) -> str:
    """Convert text to lowercase.

    Args:
        text: The input string to convert.

    Returns:
        The input string converted to lowercase.
    """
    return text.lower()


def process_reverse(text: str) -> str:
    """Reverse the input text.

    Args:
        text: The input string to reverse.

    Returns:
        The input string reversed.
    """
    return text[::-1]


def main() -> None:
    """Run the argparse demonstration.

    Demonstrates:
    - Creating an ArgumentParser with a description
    - Adding a required positional argument
    - Creating a mutually exclusive group
    - Using store_true action for boolean flags
    - Parsing and using arguments
    """
    # Create the argument parser with a description
    # The description appears in the help message
    parser = argparse.ArgumentParser(description="Process text with various operations")

    # Add a required positional argument
    # Positional arguments don't have a -- or - prefix
    # They are required by default and must be provided in order
    parser.add_argument("input_text", help="The text string to process", type=str)

    # Create a mutually exclusive group
    # Only one argument from this group can be used at a time
    # This prevents conflicting operations
    operation = parser.add_mutually_exclusive_group()

    # Add arguments to the mutually exclusive group
    # -u and --upper are short and long versions of the same flag
    # action="store_true" means the value is True if flag is present,
    # False otherwise (no value needs to be provided after the flag)
    operation.add_argument(
        "-u", "--upper", action="store_true", help="Convert text to uppercase"
    )

    operation.add_argument(
        "-l", "--lower", action="store_true", help="Convert text to lowercase"
    )

    operation.add_argument(
        "-r", "--reverse", action="store_true", help="Reverse the text"
    )

    # Parse the command-line arguments
    # This converts the command-line strings into Python objects
    args = parser.parse_args()

    # Process based on which flag was provided
    # Check args.upper, args.lower, args.reverse (boolean values)
    # Access the positional argument with args.input_text
    result = None

    if args.upper:
        result = process_uppercase(args.input_text)
        operation_name = "uppercase"
    elif args.lower:
        result = process_lowercase(args.input_text)
        operation_name = "lowercase"
    elif args.reverse:
        result = process_reverse(args.input_text)
        operation_name = "reverse"
    else:
        # No operation selected - just return the input
        result = args.input_text
        operation_name = "no operation"

    # Display the results
    print(f"Input: '{args.input_text}'")
    print(f"Operation: {operation_name}")
    print(f"Result: '{result}'")


if __name__ == "__main__":
    main()
