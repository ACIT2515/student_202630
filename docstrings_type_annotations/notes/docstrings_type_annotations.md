# Introduction to Documenting Python Docstring and Type Annotations

This document provides an overview of Docstings and Type annotations in Python, focusing on
the inputs and outputs of functions.

---

## 1. Docstrings

### What?

A **docstring** is a string literal placed as the first statement inside a
function (or module, or class) to document what it does. It is written with
triple quotes, right after the `def` line:

```python
def square(number):
    """Return the square of number."""
    return number ** 2
```

Docstrings are stored on the function itself and can be read at runtime with
`help(square)` or `square.__doc__`.

### Why?

A docstring documents _what a function does_ and _how to use it_, in plain
language. This is different from a **type annotation** (covered next), which
documents the _type_ of a value. The two work together: the annotation
describes the shape of the data, and the docstring describes its meaning and
behavior.

This course follows the **Google style** for docstrings. A Google-style
docstring starts with a one-line summary, then optional sections such as:

- `Args:` - one entry per parameter, describing what it represents
- `Returns:` - what the function returns
- `Raises:` - exceptions the function may raise
- `Examples:` - small usage examples, often written as if typed into the
  Python REPL (lines starting with `>>>`, called **doctests**)

See the
[Google Python Style Guide: Comments and Docstrings](https://google.github.io/styleguide/pyguide.html#38-comments-and-docstrings)
for the full convention.

### Use Case: A Fully Documented Function

```python
def calculate_bmi(weight_kg: float, height_m: float) -> float:
    """Calculate the Body Mass Index (BMI) for the given weight and height.

    Args:
        weight_kg: Body weight in kilograms.
        height_m: Height in meters.

    Returns:
        The calculated BMI.

    Examples:
        >>> calculate_bmi(70, 1.75)
        22.857142857142858
    """
    return weight_kg / height_m ** 2
```

Notice that `Args:` and `Returns:` describe _what each value means_, not its
type. The `: float` and `-> float` parts of the signature are type
annotations, covered next - once you add them, repeating the type in the
docstring would be redundant.

---

## 2. Introduction to Type Annotations

### What?

Python is a **dynamically typed** language: the type of a variable is determined
at runtime, and you don't have to declare it in advance.

```python
value = 5
value = "now I'm a string"
```

**Type annotations** (also called **type hints**) let you optionally write down
the type you _intend_ a variable, parameter, or return value to have. They look
like this:

```python
age: int = 20

def greet(name: str) -> str:
    return f"Hello, {name}!"
```

Annotations do not change how the program runs. Python does not check them, and
does not stop you from breaking them:

```python
def add(a: int, b: int) -> int:
    return a + b

add("2", "3")  # No error at runtime! Returns "23", not 5.
```

Annotations are read by **you**, by other developers, and by separate tools
called **static type checkers** (covered in Section 6). Python itself mostly
ignores them while your program is running.

### Why Use Type Annotations?

1. **Documentation**: The function signature tells you what to pass in and what
   you'll get back, without reading the whole function body.
2. **Catching bugs early**: A type checker (or your editor) can warn you that
   you're passing the wrong kind of value _before_ you run the program.
3. **Editor support**: Autocomplete, inline documentation, and "go to
   definition" all work better when your editor knows the expected types.
4. **Communicating intent**: Annotations make it clear what a function expects,
   which helps others (and future you) understand and safely change the code.

In short, annotations turn an implicit assumption ("this function expects a
number") into something explicit and checkable.

---

## 3. Annotating Variables

### What?

The basic syntax for a variable annotation is:

```python
variable_name: type = value
```

### Use Case: Simple Variable Annotations

```python
student_name: str = "Alice"
student_id: int = 12345
gpa: float = 3.85
is_registered: bool = True
```

The annotation (`str`, `int`, `float`, `bool`) documents the intended type of
each variable. You could still reassign `student_name` to an `int`, but doing so
would contradict the annotation and would be flagged by a type checker.

For simple, obviously-typed assignments like these, annotations are often
skipped, since the type is clear from the value itself. Annotations become more
valuable on **function signatures**, which is the main focus of this document.

---

## 4. Annotating Functions: Parameters and Return Values

### What?

Function annotations describe the expected type of each parameter and the type
of the value the function returns:

```python
def function_name(parameter: type, another_parameter: type) -> return_type:
    <block>
```

- Each parameter's annotation comes after a colon (`:`).
- The return type comes after an arrow (`->`), before the final colon.
- A function that doesn't return a meaningful value (implicitly returns `None`)
  can be annotated with `-> None`.

### Why?

A function signature is the "contract" a caller relies on. Annotating parameters
and return values makes that contract explicit: what must you provide, and what
will you get back?

### Use Case: A `calculate_area` Function

```python
def calculate_area(radius: float) -> float:
    """Calculate the area of a circle from its radius."""
    return 3.14159 * radius ** 2

area = calculate_area(2.5)
print(area)  # 19.6349375
```

Just from the signature `calculate_area(radius: float) -> float`, you know:

- You must pass one argument, `radius`, and it should be a `float`.
- You'll get a `float` back.

### Use Case: A Function That Returns Nothing

```python
def display_receipt(item: str, price: float) -> None:
    """Print a formatted receipt line. Returns nothing."""
    print(f"{item}: ${price:.2f}")

display_receipt("Coffee", 4.50)
```

`-> None` tells the caller not to expect (or use) a return value.

### Use Case: Multiple Parameters

```python
def register_student(student_id: str, name: str, gpa: float) -> bool:
    """Register a student and return True if successful."""
    print(f"Registering {name} ({student_id}), GPA: {gpa}")
    return True

success: bool = register_student("A0123456", "Sam Lee", 3.7)
```

Each parameter is annotated independently, and the annotation of `success`
documents what kind of value `register_student(...)` is expected to return.

---

## 5. Annotating Collections and Optional Values

### What?

Since Python 3.9, you can use the built-in collection types directly as
annotations, with the element type(s) inside square brackets:

```python
def average(scores: list[float]) -> float:
    return sum(scores) / len(scores)

def word_lengths(words: list[str]) -> dict[str, int]:
    return {word: len(word) for word in words}
```

| Annotation         | Meaning                                     |
| ------------------ | ------------------------------------------- |
| `list[int]`        | A list containing `int` values              |
| `dict[str, float]` | A dict mapping `str` keys to `float` values |
| `tuple[int, int]`  | A tuple of exactly two `int` values         |
| `set[str]`         | A set containing `str` values               |

### Optional and Union Types

Sometimes a parameter or return value can be one of several types, or may be
`None`. Python lets you express this with `|` (a **union**):

```python
def find_student(student_id: str) -> dict | None:
    """Return the student's record, or None if not found."""
    ...

def parse_amount(value: str) -> int | float:
    """Parse a value that could be a whole number or a decimal."""
    ...
```

`dict | None` means "a `dict`, or `None`". This is a very common pattern for
functions that might not find what they're looking for.

### Use Case: An Optional Parameter

```python
def greet(name: str, title: str | None = None) -> str:
    """Greet a person, optionally including a title."""
    if title is None:
        return f"Hello, {name}!"
    return f"Hello, {title} {name}!"

print(greet("Lee"))               # Hello, Lee!
print(greet("Lee", "Dr."))        # Hello, Dr. Lee!
```

Here, `title: str | None = None` documents that `title` is optional: callers may
omit it, pass a `str`, or explicitly pass `None`.

---

## 6. Type Checking Tools

### What?

Since Python does not enforce annotations at runtime, a separate **static type**
**checker** is used to verify that your code respects them. Two common tools are:

- **[Pylance](https://marketplace.visualstudio.com/items?itemName=ms-python.vscode-pylance)** -
  built into VS Code, checks your code live as you type.
- **[mypy](https://mypy-lang.org/)** - a command-line type checker, often run as
  part of a build or test pipeline.

### Why?

Without a type checker, annotations are just comments that Python happens to
have special syntax for. The type checker is what actually turns them into a
useful, automatic bug-catching tool.

### Use Case: Catching a Mistake Before Running the Code

```python
def calculate_area(radius: float) -> float:
    return 3.14159 * radius ** 2

calculate_area("2.5")  # Passing a string, not a float
```

Running this code doesn't raise an error immediately (string multiplication and
exponentiation can behave unexpectedly, and may fail deep inside the function,
or silently produce a nonsensical value). A type checker, however, flags the
call immediately:

```text
error: Argument of type "str" is not assignable to parameter "radius" of type "float"
```

This is the key benefit of annotations: the mistake is caught **before** you run
the program, rather than being discovered as a bug later.

---

## 7. Best Practices

1. **Always annotate function parameters and return values.** This is where
   annotations add the most value, since it documents the function's contract
   for every caller.
2. **Don't annotate every single variable.** If the type is obvious from the
   assigned value (`count = 0`), an annotation adds noise rather than clarity.
3. **Prefer built-in generics** (`list[int]`, `dict[str, float]`) over the older
   `typing.List`, `typing.Dict` forms, which are no longer needed since Python
   3.9.
4. **Use `| None` for optional values** rather than leaving it undocumented that
   a function might return or accept `None`.
5. **Run a type checker.** Annotations that nobody checks are just documentation
   that can quietly go out of date. Let Pylance or `mypy` do the checking for
   you.
6. **Keep annotations honest.** An incorrect annotation is worse than no
   annotation, since it actively misleads readers and the type checker.
