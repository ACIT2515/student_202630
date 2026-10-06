# Call Count Decorator

Try creating a decorator that counts how many times a function has been called.

Complete the code below

```python
def count_calls(func):
    """
    Decorator that counts how many times a function has been called.

    Args:
        func: The function to be decorated.

    Nonlocal Variables:
        count: the number of times the wrapped function has been called.
               Updated by the inner call_count_wrapper function

    Returns:
        function: Wrapped function that tracks call count.
    """
    # Solution Code Here
    pass

@count_calls
def say_hello():
    """Print a greeting message."""
    print("Hello!")

if __name__ == "__main__":
    say_hello()  # Call #1 to say_hello
    say_hello()  # Call #2 to say_hello
    say_hello()  # Call #3 to say_hello
    say_hello()  # Call #4 to say_hello
    say_hello()  # Call #5 to say_hello

```

## Concepts to Review

1. [`nonlocal`](https://realpython.com/ref/keywords/nonlocal/)
2. [Closures](https://realpython.com/python-closure/)