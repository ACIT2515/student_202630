from functools import wraps


def count_calls(func):
    """
    Decorator that counts how many times a function has been called.

    This creates a CLOSURE where 'wrapper' captures both 'func' and 'count'
    from the enclosing scope, allowing the count to persist across multiple calls.

    Args:
        func: The function to be decorated.

    Returns:
        function: Wrapped function that tracks call count (a CLOSURE).
    """
    count = 0  # Enclosing variable - will be captured in the CLOSURE

    def wrapper(*args, **kwargs):
        """
        Wrapper function that increments and displays call count.

        CLOSURE: This function captures 'func' and 'count' from the enclosing scope.
        The 'count' variable persists across multiple calls to this wrapper.

        Args:
            *args: Variable length argument list for wrapped function.
            **kwargs: Arbitrary keyword arguments for wrapped function.

        Returns:
            Any: Result from the wrapped function.
        """
        nonlocal count  # Access enclosing scope's count (part of closure)
        count += 1  # Modify the closure variable
        print(f"Call #{count} to {func.__name__}")  # Use both closure variables
        return func(*args, **kwargs)  # Call captured function

    return wrapper  # Return CLOSURE (captures 'func' and 'count')


@count_calls
def say_hello():
    """Print a greeting message."""
    print("Hello!")


if __name__ == "__main__":
    # Each call to say_hello() uses the SAME closure with persistent 'count'
    say_hello()  # Call #1 to say_hello
    say_hello()  # Call #2 to say_hello
    say_hello()  # Call #3 to say_hello
