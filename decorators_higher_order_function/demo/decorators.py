#!/usr/bin/env python3
"""
Demonstrates use of decorators.

This script utilizes the inspect library to access the calling function and
the named of functions that are passed as variables

"""


def decorator(func):
    """
    This is the function that takes a function creates wrapper function
    that is called every time the the passed function is called.

    Args:
        func: function to be decorated

    Returns:
        func: wrapper function
    """

    def wrapper(*args, **kwargs):
        """
        The wrapper function.  Calls the decorated function and prints
        messages before and after.

        Returns:
            Any results of the decorated function
        """
        print("*** Running decorator")
        result = func(*args, **kwargs)
        print(f"*** Finished running decorator: Result = {result}")
        return result

    return wrapper


@decorator
def some_func(arg1):
    """
    A simple function to demonstrate use of a decorator.
    """

    print(f"Running some_func: {arg1}")
    return f"some_func result: {arg1}"


def main():
    """Demonstrates use of decorators"""
    print("Start of main func")
    result = some_func("Olympics")
    print(f"End of main func: {result}")


if __name__ == "__main__":
    main()
