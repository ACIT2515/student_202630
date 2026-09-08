# Introductory Exercise: Documenting Code

## Introduction to Docstrings

A **docstring** is a string literal placed as the first statement in a
function (or module, or class) that documents what it does. It's written with
triple quotes, right after the `def` line:

```python
def square(number: int) -> int:
    """Return the square of number."""
    return number ** 2
```

Docstrings are stored on the function itself, and can be read at runtime with
`help(square)` or `square.__doc__`.

This course uses the **Google style** for docstrings. A Google-style docstring
starts with a one-line summary, then optional sections such as `Args:` (one
entry per parameter), `Returns:` (the return value), `Raises:` (exceptions the
function may raise), and `Examples:` (small usage examples, often written as if
typed into the Python REPL, with lines starting with `>>>`):

```python
def square(number: int) -> int:
    """Return the square of number.

    Args:
        number: The value to square.

    Returns:
        The square of number.

    Examples:
        >>> square(4)
        16
    """
    return number ** 2
```

REPL-style examples like `>>> square(4)` are called **doctests**, and can be
checked automatically. See the
[Google Python Style Guide: Comments and Docstrings](https://google.github.io/styleguide/pyguide.html#38-comments-and-docstrings)
for the full convention.

In this exercise, docstrings are used to specify what each function should do
(Part 1), and to describe the parameters and return value of existing,
unannotated functions (Part 2).

## Structure

Create a solution directory `docstrings_type_annotations`.

Create a file called `docstrings_type_annotations_exercise.py`.

Your file **must** follow the
[Recommended Script Structure](../../modules_packages/notes/modules_packages_imports.md#recommended-script-structure)
from the modules and packages notes:

- Write each exercise below as its own function. Keep the module root free of
  anything except imports and function definitions.
- Add a `main()` function that calls every function you implemented and
  prints its result, so running the script demonstrates all of them.
- Call `main()` only from an `if __name__ == '__main__':` conditional at the
  bottom of the file.

## Part 1: Write Functions From Their Annotations

For each function below, the signature (parameter and return type annotations)
is already given as a docstring-only stub. Copy each stub into your file and
implement the function body so that it satisfies the annotation and the
docstring.

### Exercise 1.1 - `calculate_tip_amount`

```python
def calculate_tip_amount(bill_total: float, tip_percent: float) -> float:
    """Calculate the tip amount for a given bill and tip percentage.

    Args:
        bill_total: The total bill amount, before tip.
        tip_percent: The tip percentage (e.g., 20 for 20%).

    Returns:
        The calculated tip amount.

    Examples:
        >>> calculate_tip_amount(50, 20)
        10.0
    """
```

### Exercise 1.2 - `is_even`

```python
def is_even(number: int) -> bool:
    """Return True if number is even, False otherwise.

    Args:
        number: The integer to check.

    Returns:
        True if number is even, False otherwise.

    Examples:
        >>> is_even(4)
        True
        >>> is_even(7)
        False
    """
```

### Exercise 1.3 - `average_score`

```python
def average_score(scores: list[float]) -> float:
    """Return the arithmetic average of a non-empty list of scores.

    Args:
        scores: A non-empty list of numeric scores.

    Returns:
        The arithmetic average of scores.

    Examples:
        >>> average_score([80.0, 90.0, 100.0])
        90.0
    """
```

### Exercise 1.4 - `find_max_score`

```python
def find_max_score(scores: list[float]) -> float | None:
    """Return the largest score in the list, or None if the list is empty.

    Args:
        scores: A list of numeric scores, which may be empty.

    Returns:
        The largest score in scores, or None if scores is empty.

    Examples:
        >>> find_max_score([55.0, 92.5, 78.0])
        92.5
        >>> print(find_max_score([]))
        None
    """
```

## Part 2: Annotate Existing Functions

The functions below already work correctly, but they are missing their
parameter and return type annotations. Copy each function into your file, then
add annotations based on what the docstring describes. Do not change the
function body.

### Exercise 2.1 - `celsius_to_fahrenheit`

```python
def celsius_to_fahrenheit(celsius):
    """Convert a Celsius temperature to Fahrenheit.

    Args:
        celsius (float): The temperature in degrees Celsius.

    Returns:
        float: The temperature in degrees Fahrenheit.
    """
    return celsius * 9 / 5 + 32
```

### Exercise 2.2 - `count_vowels`

```python
def count_vowels(text):
    """Count the number of vowels (a, e, i, o, u) in a string, ignoring case.

    Args:
        text (str): The text to search.

    Returns:
        int: The number of vowels found.
    """
    count = 0
    for letter in text.lower():
        if letter in "aeiou":
            count += 1
    return count
```

## Part 3: Run Everything From `main()`

### Exercise 3.1 - `main`

Write a `main()` function in your file that calls every function from Part 1
and Part 2, and prints the result of each call. `main()` must only run when
the script is run by name (i.e., executed directly), not when it is imported.

```python
def main():
    """Demonstrate every function implemented in this exercise."""
    # Call each function above, and print the result of each call.
    ...

if __name__ == "__main__":
    main()
```

Run your script directly (e.g. `python docstrings_type_annotations_exercise.py`)
and confirm you see the printed output of every function call.

## Part 4: Using the VS Code Debugger

### Exercise 4.1 - Step Through `find_max_score`

Set a breakpoint on the first line inside `find_max_score` (click in the
gutter to the left of the line number, or place your cursor on the line and
press `F9`). Start debugging with `F5` (or **Run > Start Debugging**) so that
`main()` runs and calls `find_max_score([])`.

- Step over each line with `F10` until you reach the `if not scores:` check.
- Inspect the value of `scores` in the **Variables** pane. Confirm it is an
  empty list.
- Continue stepping and confirm the function returns `None`.

### Exercise 4.2 - Step Into `average_score`

Set a breakpoint on the line that calls `average_score(...)` inside `main()`.
Start debugging, then use `F11` (**Step Into**) to move execution into the
`average_score` function body.

- Use the **Debug Console** to evaluate the expressions `sum(scores)` and
  `len(scores)` while paused inside the function.
- Confirm the displayed values match what you expect for the `scores` list
  you passed in.
- Press `F5` to continue running to completion.

### References

1. [Python Docs: typing](https://docs.python.org/3/library/typing.html)
2. [PEP 484 - Type Hints](https://peps.python.org/pep-0484/)
3. [Google Python Style Guide: Comments and Docstrings](https://google.github.io/styleguide/pyguide.html#38-comments-and-docstrings)
4. [Recommended Script Structure](../../modules_packages/notes/modules_packages_imports.md#recommended-script-structure)
