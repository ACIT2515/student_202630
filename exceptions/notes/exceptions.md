# Exception Handling in Python

Programs do not always receive valid input or have access to every resource
they need. A file may be missing, a network connection may fail, or a user may
enter text where a number is expected. Python represents these unusual events
with **exceptions**.

Exception handling lets a program respond to a problem in a controlled way.
Instead of allowing the program to stop with an error message, you can detect
the exception, report a useful message, recover when possible, or stop safely.

## What Is an Exception?

An exception is an object that describes an error or unusual event while a
program is running. When Python encounters a problem, it **raises** an
exception.

For example, dividing by zero raises `ZeroDivisionError`:

```python
result = 10 / 0
```

The exception interrupts the normal top-to-bottom flow of the program. If no
code handles it, Python prints a traceback and the program stops.

Exceptions should occur when it doesn't make sense to continue with normal program progression.

Common exceptions include:

| Exception | Typical cause |
| --------- | ------------- |
| `FileNotFoundError` | A requested file does not exist. |
| `PermissionError` | The program is not allowed to access a resource. |
| `ValueError` | A value has the right type but an invalid value. |
| `TypeError` | An operation uses an inappropriate type. |
| `IndexError` | A sequence index is outside its valid range. |
| `KeyError` | A dictionary key does not exist. |
| `ZeroDivisionError` | A number is divided by zero. |
| `OSError` | An operating system operation fails. |

## Catching an Exception

Use a `try` block for code that might raise an exception. Use an `except` block
to describe what the program should do if that exception occurs.

```python
try:
    result = 10 / 0
except ZeroDivisionError:
    print("You cannot divide by zero.")
```

The code in the `except` block runs only when the matching exception is raised.
After the exception is handled, the program continues after the complete
`try`/`except` statement.

```python
print("The program is starting.")

try:
    result = 10 / 0
except ZeroDivisionError:
    print("The calculation could not be completed.")

print("The program is still running.")
```

Exceptions should only be handled if it is possible for the program to recover from the specific error.

If it is possible to recover but not continue with program execution then another exeception should be raised or the program ended.

## Accessing Exception Details

Use `as` to store the exception object in a variable. The object often contains
details that help explain what went wrong.

```python
try:
    with open("missing_config.txt", "r", encoding="utf-8") as config_file:
        settings = config_file.read()
except FileNotFoundError as error:
    print(f"Configuration file was not found: {error}")
```

The exception message is useful for logging or debugging, but user-facing
messages should explain the problem in terms the user can act on.

## Handling User Input

`ValueError` is common when converting user input. The conversion is the risky
operation, so keep the `try` block small and handle only the expected problem.

```python
text = input("Enter a port number: ")

try:
    port = int(text)
except ValueError:
    print("Port numbers must be whole numbers.")
else:
    print(f"Monitoring port {port}.")
```

The `else` block runs only when the `try` block completes without raising an
exception. It keeps successful processing separate from error handling.

## Handling Multiple Exceptions

You can use more than one `except` block when different exceptions require
different responses. Python checks the blocks from top to bottom and runs the
first matching block.

```python
try:
    with open("servers.txt", "r", encoding="utf-8") as server_file:
        server_number = int(server_file.readline())
        address = server_file.readlines()[server_number]
except FileNotFoundError:
    print("The server list does not exist.")
except ValueError:
    print("The first line must contain a whole number.")
except IndexError:
    print("The server number is outside the list.")
```

You can also catch several exception types when they need the same response:

```python
try:
    value = int(input("Enter a number: "))
except (ValueError, TypeError):
    print("Please enter a valid number.")
```

## The `finally` Block

The optional `finally` block runs whether an exception occurs or not. Use it
for cleanup that must happen, such as closing a connection or removing a
temporary resource.

```python
log_file = None

try:
    log_file = open("startup.log", "a", encoding="utf-8")
    log_file.write("System check started\n")
except OSError as error:
    print(f"Could not write to the log: {error}")
finally:
    if log_file is not None:
        log_file.close()
```

For files, prefer a `with` statement because it closes the file automatically:

```python
with open("startup.log", "a", encoding="utf-8") as log_file:
    log_file.write("System check started\n")
```

## Raising an Exception

You can manually raise an exception when a function receives data that does
not meet its requirements. This makes the invalid state visible to the code
that called the function.

```python
def validate_port(port: int) -> int:
    """Return a valid TCP or UDP port number."""
    if not 1 <= port <= 65535:
        raise ValueError("port must be between 1 and 65535")
    return port
```

The caller can decide how to respond:

```python
try:
    monitored_port = validate_port(70000)
except ValueError as error:
    print(f"Invalid port: {error}")
```

Raising an exception is different from printing an error. A function should
usually raise an exception when it cannot complete its responsibility, allowing
the caller to choose whether to retry, use a default, log the problem, or stop.

## Custom Exceptions

Custom exceptions give a program a meaningful name for an application-specific
problem. Define them by inheriting from `Exception`.

```python
class InvalidServerStatusError(Exception):
    """Raised when a server reports an invalid status."""


def check_server_status(status: str) -> None:
    """Validate a server status value."""
    valid_statuses = {"online", "offline", "maintenance"}
    if status not in valid_statuses:
        raise InvalidServerStatusError(f"Unknown status: {status}")
```

The custom exception can be caught like any built-in exception:

```python
try:
    check_server_status("unknown")
except InvalidServerStatusError as error:
    print(f"Status check failed: {error}")
```

## Exception Hierarchies

Python exceptions are organized in an inheritance hierarchy. For example,
`FileNotFoundError` is a kind of `OSError`. Catching `OSError` can therefore
handle several related operating system errors.

```python
try:
    with open("servers.txt", "r", encoding="utf-8") as server_file:
        contents = server_file.read()
except OSError as error:
    print(f"A file operation failed: {error}")
```

Put more specific exceptions before general exceptions:

```python
try:
    number = int(input("Enter a number: "))
except ValueError:
    print("That was not a valid number.")
except Exception as error:
    print(f"An unexpected error occurred: {error}")
```

Avoid catching `Exception` unless you have a specific reason, such as handling
an error at the outer boundary of an application or recording an unexpected
failure before stopping. A broad handler can hide programming mistakes.

## Good Exception Handling Practices

1. Catch specific exceptions that you know how to handle.
1. Keep the `try` block as small as possible.
1. Give users useful recovery instructions rather than exposing a traceback.
1. Preserve exception details in logs when investigating operational failures.
1. Use `raise` when a function cannot fulfill its contract.
1. Use `with` for files and other resources that support context managers.
1. Do not use an empty `except` block or silently ignore an exception.

This is a poor pattern because it catches every exception and hides the cause:

```python
# Avoid this pattern.
try:
    result = 1 / 0
except:
    pass
```

A specific handler makes the intended response clear:

```python
try:
    result = 1 / 0
except ZeroDivisionError:
    result = 0
    print("The calculation used a safe default.")
```

## References

1. [Errors and Exceptions](https://docs.python.org/3/tutorial/errors.html)
1. [Built-in Exceptions](https://docs.python.org/3/library/exceptions.html)
1. [Exceptions in Python](https://docs.python.org/3/reference/executionmodel.html#exceptions)

