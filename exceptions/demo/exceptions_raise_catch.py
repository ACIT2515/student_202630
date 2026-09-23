#! /usr/bin/env python3
"""Introduction to exception handling in Python.

This program lets you practice handling different types of exceptions.
You choose which type of error to create, and the program shows you
how to catch and handle it properly.
"""


def raise_exc(exc_option):
    """Create and raise a specific type of exception.

    This function intentionally raises different types of errors
    based on what you ask for. This helps you practice catching
    and handling different exception types.

    Args:
        exc_option: A string telling us which exception to raise.
            Examples: "SyntaxError", "NameError", "KeyError", etc.

    Returns:
        The string "Success" if you choose an option that doesn't
        raise an exception.

    Raises:
        Different exceptions depending on the exc_option you provide.
        Each exception is raised on purpose so you can practice
        handling it.
    """
    # Intentionally raise exceptions based on user selection
    if exc_option == "SyntaxError":
        raise SyntaxError("Intentionally raised SyntaxError Exception")
    elif exc_option == "NameError":
        raise NameError("Intentionally raised NameError Exception")
    elif exc_option == "KeyError":
        raise KeyError("Intentionally raised KeyError Exception")
    elif exc_option == "IndexError":
        raise IndexError("Intentionally raised IndexError Exception")
    elif exc_option == "FileNotFoundError":
        raise FileNotFoundError("Intentionally raised FileNotFoundError Exception")
    elif exc_option == "TimeoutError":
        raise TimeoutError("Intentionally raised TimeoutError Exception")
    elif exc_option == "ValueError":
        raise ValueError("Intentionally raised ValueError Exception")
    else:
        # No exception raised - return success
        return "Success"


def main():
    """Let the user choose and practice handling an exception.

    This function shows you a menu of different exception types.
    When you pick one, the program raises that exception and shows
    you how to catch it. This is a safe way to learn about exceptions!

    Returns:
        The string "Success" if you choose option 0 (no exception).
        Nothing (None) if an exception was raised and caught.

    Important:
        Some exceptions (SyntaxError and ValueError) are NOT caught here.
        If you choose those options, the program will crash - this shows
        you what happens when you don't handle an exception!
    """
    # Dictionary mapping option numbers to exception type names
    exc_types = {
        0: "Success",
        1: "SyntaxError",
        2: "NameError",
        3: "KeyError",
        4: "IndexError",
        5: "FileNotFoundError",
        6: "TimeoutError",
        7: "ValueError",
    }

    print("""Exception Options
    0: Success - no exception
    1: SyntaxError - normally raised during import of module with syntax errors
    2: NameError - normally raised when accessing an undeclared variable
    3: KeyError - normally raised when accessing a dict using an invalid key
    4: IndexError - normally raised when accessing a list using an invalid index
    5: FileNotFoundError - normally raised when opening non-existent file
    6: TimeoutError - normally raised when an os operation takes too long
    7: ValueError - normally raised when an argument is set to an improper value
    """)

    # May raise ValueError if input is not a valid integer (not caught in this function)
    exc_option = int(input("Enter exception option: "))

    try:
        # This function call may raise various exceptions based on user's choice
        # May also raise KeyError if exc_option is not in exc_types dict
        status = raise_exc(exc_types[exc_option])
    except NameError as error:
        # Catch and handle NameError exception
        print("NameError Details: {}".format(error))
    except KeyError as error:
        # Catch and handle KeyError exception (from dict access or raised exception)
        print("KeyError Details: {}".format(error))
    except IndexError as error:
        # Catch and handle IndexError exception
        print("IndexError Details: {}".format(error))
    except FileNotFoundError as error:
        # Catch and handle FileNotFoundError exception
        print("FileNotFoundError Details: {}".format(error))
    except TimeoutError as error:
        # Catch and handle TimeoutError exception
        print("TimeoutError Details: {}".format(error))
    else:
        # This block executes only if NO exception was raised in the try block
        print("The exc_option function returned: {}".format(status))
        return status
    finally:
        # This block ALWAYS executes, whether an exception occurred or not
        print("Finished exc_processing")


if __name__ == "__main__":
    main()
