# Directed Reading Answers: Introduction to Unit Testing and pytest

## Question 1: Iterative Development and TDD

### Question

In your own words, describe the difference between manual testing and automated
unit testing. Then, explain why practicing Test driven development helps
developers design better software before writing implementation code.

### Answer

Manual testing is running a program yourself and checking, by eye, whether the
output looks correct. It depends on a person remembering to test, and to test
every case, each time the code changes. Automated unit testing replaces that
manual check with code: a test function calls one small piece of the program
and asserts what its result should be. The computer then re-runs every test in
seconds, so a regression in previously working code is caught immediately
instead of being noticed later, or not at all.

Test-Driven Development (TDD) writes the failing test before the
implementation (Red), then writes the smallest amount of code to pass it
(Green), then improves the code (Refactor). Writing the test first forces a
developer to decide what a function's inputs, outputs, and behaviour should be
before worrying about how to implement it. This produces a clearer, more
testable design, and it means every behaviour in the program is verified by a
test as soon as it exists, rather than tests being added afterward.

## Question 2: Test Discovery Conventions in pytest

### Question

State the naming pattern `pytest` looks for in test files and test functions.
Give one example of a valid test file name and one example of a valid test
function name.

### Answer

`pytest` discovers test files named `test_*.py` (or `*_test.py`), and within
those files it discovers test functions whose names start with `test_`.

- Valid test file name: `test_calculator.py`
- Valid test function name: `def test_divide():`

## Question 3: Testing Exceptions with `pytest.raises`

### Question

When testing that a function raises an error (such as a `ValueError`), what
`pytest` construct do you use instead of a standard `assert` statement? Write a
two-line code snippet showing its basic syntax.

### Answer

Use `with pytest.raises(<NAME>)` instead of a standard `assert` statement,
where `<NAME>` is the exception class you expect to be raised.

```python
def test_add_values_invalid():
    with pytest.raises(TypeError):
        add_values([1], [2])
```
