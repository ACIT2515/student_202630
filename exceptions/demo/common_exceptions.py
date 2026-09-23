#! /usr/bin/env python3
"""Common exception handling demonstration

This module demonstrates fundamental exception handling concepts including:
- Handling different types of exceptions
- Accessing and displaying exception details
- Continuing program execution after handling exceptions
"""


def demonstrate_file_exception():
    """Demonstrate FileNotFoundError exception handling.

    Attempts to open a non-existent file and handles the exception gracefully,
    displaying error details and continuing execution.
    """
    print("=== FileNotFoundError Example ===")
    try:
        # This line will raise FileNotFoundError - file doesn't exist
        with open("non_existent_file.txt", "r") as source:
            data = source.readlines()
            print(data)
    except FileNotFoundError as error:
        # Handle the exception - program doesn't crash, continues execution
        print(f"Error: {error.strerror}")
        print(f"Filename: {error.filename}")
        print("Program continues despite the error!\n")


def demonstrate_zero_division():
    """Demonstrate ZeroDivisionError exception handling.

    Attempts to divide by zero and handles the exception, showing how
    the program can recover and continue.
    """
    print("=== ZeroDivisionError Example ===")
    try:
        # This line will raise ZeroDivisionError - cannot divide by zero
        result = 10 / 0
        print(f"Result: {result}")
    except ZeroDivisionError as error:
        # Catch the exception and provide a fallback value
        print(f"Error: {error}")
        print("Cannot divide by zero! Using default value instead.")
        result = 0  # Recovery: set a safe default value
        print(f"Result set to: {result}\n")


def demonstrate_value_error():
    """Demonstrate ValueError exception handling.

    Attempts to convert invalid input to an integer and handles the exception,
    showing how to validate and recover from invalid data.
    """
    print("=== ValueError Example ===")
    invalid_input = "abc"
    try:
        # This line will raise ValueError - "abc" cannot be converted to int
        number = int(invalid_input)
        print(f"Number: {number}")
    except ValueError as error:
        # Handle invalid conversion gracefully
        print(f"Error: {error}")
        print(f"'{invalid_input}' is not a valid number!")
        print("Using default value instead.")
        number = 0  # Recovery: provide a default value
        print(f"Number set to: {number}\n")


def demonstrate_index_error():
    """Demonstrate IndexError exception handling.

    Attempts to access an invalid list index and handles the exception,
    showing safe list access patterns.
    """
    print("=== IndexError Example ===")
    my_list = [1, 2, 3]
    try:
        # This line will raise IndexError
        # index 10 is out of range (list has only 3 items)
        value = my_list[10]
        print(f"Value: {value}")
    except IndexError as error:
        # Handle the out-of-range index error
        print(f"Error: {error}")
        print(f"List only has {len(my_list)} elements!")
        print("Accessing last element instead.")
        value = my_list[-1]  # Recovery: use last valid element
        print(f"Value: {value}\n")


def demonstrate_key_error():
    """Demonstrate KeyError exception handling.

    Attempts to access a non-existent dictionary key and handles the exception,
    showing safe dictionary access patterns.
    """
    print("=== KeyError Example ===")
    my_dict = {"name": "Alice", "age": 25}
    try:
        # This line will raise KeyError - "city" key doesn't exist in dictionary
        city = my_dict["city"]
        print(f"City: {city}")
    except KeyError as error:
        # Handle missing key gracefully
        print(f"Error: Key {error} not found in dictionary")
        print(f"Available keys: {list(my_dict.keys())}")
        print("Setting default value.")
        city = "Unknown"  # Recovery: provide a default value
        print(f"City: {city}\n")


def demonstrate_multiple_exceptions():
    """Demonstrate handling multiple exception types in one try block.

    Shows how to handle different exceptions that might occur from
    user input and perform appropriate recovery actions.
    """
    print("=== Multiple Exception Handling Example ===")
    data = ["10", "20", "abc", "30"]
    total = 0

    for item in data:
        try:
            # May raise ValueError if item isn't a valid number
            number = int(item)
            # May raise ZeroDivisionError if number is 0
            result = 100 / number
            total += result
            print(f"Processed {item}: {result:.2f}")
        except ValueError as error:
            # Handle non-numeric values - skip and continue
            print(f"Skipping invalid value '{item}': {error}")
        except ZeroDivisionError as error:
            # Handle division by zero - skip and continue
            print(f"Cannot divide by {item}: {error}")
        except Exception as error:
            # Catch-all for any other unexpected exceptions
            print(f"Unexpected error with '{item}': {error}")

    # Execution continues after all exceptions were handled
    print(f"Total: {total:.2f}\n")


def main():
    """Run all exception handling demonstrations.

    Executes each demonstration function to show various exception
    handling scenarios and how programs continue after exceptions.
    """
    print("*** Basic Exception Handling Demonstrations ***\n")

    demonstrate_file_exception()
    demonstrate_zero_division()
    demonstrate_value_error()
    demonstrate_index_error()
    demonstrate_key_error()
    demonstrate_multiple_exceptions()

    print("*** All demonstrations completed successfully! ***")
    print("Notice how the program continued running after each exception was handled.")


if __name__ == "__main__":
    main()
