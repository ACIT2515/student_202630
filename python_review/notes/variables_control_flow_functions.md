# Python Basics: Variables, Control Flow, and Functions

This reference introduces the Python foundations used to build small command-line
and system-administration tools. 

## Running Python Programs

Python programs are text files, normally with a `.py` extension. Run a program
from a terminal with:

```bash
python host_check.py
```

The Python interpreter reads and executes the file from top to bottom. It stops
when it reaches the end of the file or encounters an error.

## Variables and Types

A variable is a name that refers to a value. Create a variable with `=`:

```python
hostname = "server01"
port = 443
disk_usage = 74.5
is_online = True
```

Use meaningful `snake_case` names. Use uppercase names for values that should
not change while the program runs:

```python
DEFAULT_PORT = 443
MAX_DISK_USAGE_PERCENT = 90
```

Python is dynamically typed: Python determines a variable's type when the
program runs. You can inspect a type with `type()`.

```python
print(type(port))       # <class 'int'>
print(type(hostname))   # <class 'str'>
```

### Common Scalar Types

This course begins with these individual values:

- `int`: whole numbers, such as `42` or `-7`
- `float`: decimal numbers, such as `3.14` or `74.5`
- `str`: text, such as `"server01"`
- `bool`: `True` or `False`
- `None`: represents the absence of a value

### Type Annotations

Type annotations document the type you expect a variable, parameter, or return
value to have. They are checked by a type checker, not enforced automatically by
Python while it runs.

```python
hostname: str = "server01"
port: int = 443
is_online: bool = True
```

### Converting Types

Use conversion functions when input text must become a number:

```python
port_text = "443"
port = int(port_text)
usage_percent = float("74.5")
```

Not every conversion is valid. For example, `int("server01")` raises a
`ValueError`.

## Strings and f-Strings

Strings store text. Use single or double quotes consistently:

```python
hostname = "server01"
status = 'online'
```

An f-string creates readable output by placing expressions inside `{}`:

```python
hostname = "server01"
port = 443
usage_percent = 74.567

print(f"Checking {hostname} on port {port}")
print(f"Disk usage: {usage_percent:.1f}%")
```

The `:.1f` format specification displays one decimal place. F-strings are the
preferred way to build messages from variable values.

## Control Flow

Control flow determines which statements Python runs and how often it runs them.
Indented statements belong to the `if` or loop above them.

### Conditions with `if`

An `if` statement runs a block only when its condition is `True`. Use `elif` for
another condition and `else` for the remaining case.

```python
usage_percent = 92

if usage_percent >= 90:
    print("Disk usage is too high")
elif usage_percent >= 75:
    print("Disk usage needs attention")
else:
    print("Disk usage is acceptable")
```

Comparison operators include `==`, `!=`, `<`, `<=`, `>`, and `>=`. Remember:
`=` assigns a value, while `==` compares two values.

Combine conditions with `and`, `or`, and `not`:

```python
is_online = True
has_permission = False

if is_online and has_permission:
    print("Run the check")
```

### Repeating Work with `while`

A `while` loop repeats while its condition is `True`. Ensure that a value used
in the condition changes, or the loop will not stop.

```python
attempt = 1

while attempt <= 3:
    print(f"Connection attempt {attempt}")
    attempt += 1
```

Use `break` to leave a loop immediately and `continue` to skip to its next
iteration. `for` loops over container values are covered with container types.

## Functions

A function is a named, reusable block of code that performs one task. Functions
make programs easier to read, reuse, test, and improve.

```python
def show_host_status(hostname: str, is_online: bool) -> None:
    if is_online:
        print(f"{hostname} is online")
    else:
        print(f"{hostname} is offline")
```

Call a function by writing its name followed by parentheses:

```python
show_host_status("server01", True)
```

### Parameters and Arguments

Parameters are names in a function definition. Arguments are the values supplied
when the function is called.

```python
def calculate_free_space(total_gb: float, used_gb: float) -> float:
    return total_gb - used_gb

free_space = calculate_free_space(500.0, 125.5)
```

In this example, `total_gb` and `used_gb` are parameters. `500.0` and `125.5`
are arguments.

Use keyword arguments when they make a call easier to read:

```python
free_space = calculate_free_space(total_gb=500.0, used_gb=125.5)
```

### Return Values

Use `return` to send a result back to the code that called the function. A
function without a `return` statement returns `None`.

```python
def is_disk_usage_acceptable(usage_percent: float) -> bool:
    return usage_percent < 90

if is_disk_usage_acceptable(74.5):
    print("Disk usage is acceptable")
```

Prefer functions that accept values through parameters and return results. This
makes their behaviour clear and easy to test.

## Variable Scope

Scope is the part of a program where a variable name can be used. For now, focus
on function scope and module scope.

### Function Scope

A variable created inside a function is local to that function. It cannot be
used directly outside the function.

```python
def build_host_label(hostname: str) -> str:
    label = f"host-{hostname}"
    return label

print(build_host_label("server01"))
# print(label)  # NameError: label exists only inside build_host_label
```

### Module Scope

A variable created outside a function belongs to the module, which is the Python
file. Code later in the same file can use it. Other files can access it by
importing the module and using the module name.

```python
# network_settings.py
DEFAULT_PORT = 443

def show_default_port() -> None:
    print(DEFAULT_PORT)
```

Use module-level names mainly for constants. Pass values into functions and
return values from functions instead of changing module-level variables.

Object attributes and their scope are covered later with object-oriented
programming.

## References

1. [Python Tutorial](https://docs.python.org/3/tutorial/)
1. [Built-in Types](https://docs.python.org/3/library/stdtypes.html)
1. [Defining Functions](https://docs.python.org/3/tutorial/controlflow.html#defining-functions)
