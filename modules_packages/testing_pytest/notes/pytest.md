# Iterative Development: Unit testing and TDD (Test Driven Development)

## What is Iterative Development?

- An approach where software is built in small, repeated cycles rather than all
  at once
- Each cycle adds or refines a feature, and is verified (e.g. with tests) before
  moving to the next
- Feedback from one cycle informs the next, allowing the design to evolve as
  understanding improves

## Why test?

### You're Already Testing

- You've been testing your code since day 1 - running it to see if it works
- The difference: **manual testing** vs. **automated testing**
- Manual testing: run the program, check the output, repeat
- Automated testing: write code that checks if your code works

### Benefits of Automated Testing

#### Confidence and Speed

- **One command** tells you if everything works: `pytest`
- Run hundreds of tests in seconds
- No need to manually check every feature after each change

#### Catching Bugs Early

- Find problems immediately when you write code
- Prevent bugs from reaching users
- Ensure changes don't break existing functionality (regression testing)

#### Types of Automated Tests

**Unit Tests** (what we focus on):

- Test individual functions, methods, or classes in isolation
- Fast to run (seconds, not minutes)
- Easy to write alongside your code

**Integration Tests** (not covered here):

- Test how different parts of your program work together
- Test interactions between objects, databases, APIs, etc.

## The Testing Mindset

- Tests serve as **documentation**: they show how your code is meant to be used
- Tests provide **safety**: refactor and improve code without fear of breaking
  things
- Tests enforce **discipline**: write code that actually meets requirements

---

![50% center](https://www.commitstrip.com/wp-content/uploads/2017/02/Strip-Ou-sont-les-tests-unitaires-english650-final.jpg)

---

## Unit tests

### Characteristics of Good Unit Tests

- **Fast**: Run in seconds, not minutes
- **Isolated**: Test one thing at a time (functions, methods, classes)
- **Repeatable**: Same results every time
- **Self-checking**: Pass or fail automatically (no manual verification)

## Automation Benefits

- **Continuous Integration**: Run tests automatically on every commit
- **Scheduled Testing**: Run test suites nightly or on-demand
- **Living Documentation**: Tests show how your code should be used
- **Quick Feedback**: Know immediately if changes break existing functionality

## Test-Driven Development (TDD)

A development approach where you **write tests before writing code**: (or mabe
at the same time)

1. **Red**: Write a failing test for the feature you want
2. **Green**: Write minimal code to make the test pass
3. **Refactor**: Improve the code while keeping tests passing

### Benefits of TDD

- Ensures requirements are met from the start
- Forces you to think about design before implementation
- You become the first user of your own code
- Catches misunderstandings early in development

## Untested code is broken code

![50% center](https://assets.amuniversal.com/4b9def60e14e0137cc29005056a9545d)

# Testing in Python

- The testing framework provided by Python is called `unittest`
- It is derived from `jUnit` and has a very Java-oriented syntax
- It is good to know about `unittest`, but `pytest` is a more pythonic framework
  and what we will be using

## Installing `pytest`

### System Installation

```bash
pip install -U pytest
```

### Using UV and Installing `pytest` as a Project Dependency

Install pytest as a **development dependency** (not needed for production):

```bash
uv add --dev pytest
```

The `--dev` flag ensures pytest is:

- Available during development and testing
- **Not** included when distributing your application

> **Note**: install pytest in your virtual environment this will ensure others
> that clone your code are using the correct test framework

## Running `pytest`

There are three main ways to run `pytest` depending on your project setup:

### Method 0: Using System `pytest`

- If you installed pytest system-wide with `pip install -U pytest`, you can run
  it directly:
  - `pytest`: Runs all tests in the current directory and subdirectories
  - `pytest <filename>`: Runs tests in a specific file (e.g.,
    `pytest test_math.py`)
  - `pytest <filename> <filename>`: Runs tests in multiple files
  - `pytest <dirname>`: Runs all tests in a specific directory (e.g.,
    `pytest tests/`)
- No virtual environment activation is needed since pytest is installed
  system-wide
- **Not recommended** for project work: system installs are not isolated per
  project, so different projects can conflict over pytest (or dependency)
  versions

### Method 1: Using `uv` (Recommended for `uv` projects)

- If you installed pytest with `uv add --dev pytest`, you can run it directly
  with `uv`:
  - `uv run pytest`: Runs all tests in the current directory and subdirectories
  - `uv run pytest <filename>`: Runs tests in a specific file (e.g.,
    `uv run pytest test_math.py`)
  - `uv run pytest <filename> <filename>`: Runs tests in multiple files
  - `uv run pytest <dirname>`: Runs all tests in a specific directory (e.g.,
    `uv run pytest tests/`)
- `uv run` automatically activates the virtual environment and executes the
  command
- This is the simplest method as you don't need to manually activate the virtual
  environment

### Method 2: Activating the Virtual Environment

- First, activate your virtual environment:
  - **Windows**: `.venv\Scripts\activate`
  - **macOS/Linux**: `source .venv/bin/activate`
- Once activated, you can run pytest directly:
  - `pytest`: Runs all tests in the current directory and subdirectories
  - `pytest <filename>`: Runs tests in a specific file
  - `pytest <filename> <filename>`: Runs tests in multiple files
  - `pytest <dirname>`: Runs all tests in a specific directory
- Remember to deactivate the virtual environment when done: `deactivate`

### Common pytest Options

- `pytest -v`: Verbose output (shows each test name)
- `pytest -k "pattern"`: Run only tests matching the pattern (e.g.,
  `pytest -k "addition"`)
- `pytest --collect-only`: Show which tests would be run without executing them
- `pytest -x`: Stop after the first failure
- `pytest --lf`: Run only the tests that failed in the last run

### Configuring VSCode to run pytest

VSCode has built-in support for running and debugging pytest tests with a
graphical interface.

#### Configure the Test Framework

1. Open the Command Palette (`Ctrl+Shift+P` or `Cmd+Shift+P` on macOS)
2. Type and select: **Python: Configure Tests**
3. Select **pytest** as your test framework
4. Select the root directory where your tests are located (usually `tests` or
   `.` for root)

#### Configure Python Interpreter (for `uv` projects)

1. Open the Command Palette (`Ctrl+Shift+P` or `Cmd+Shift+P`)
2. Type and select: **Python: Select Interpreter**
3. Choose the interpreter from your `.venv` folder (e.g.,
   `./.venv/Scripts/python.exe` on Windows or `./.venv/bin/python` on
   macOS/Linux)
4. This ensures VSCode uses the virtual environment where pytest is installed

#### Running Tests in VSCode

Once configured, you have multiple ways to run tests:

##### Using the Test Explorer

- Click the **Testing** icon in the Activity Bar (left sidebar - looks like a
  beaker/flask)
- VSCode will discover all your tests and display them in a tree view
- Click the **play button** next to any test to run it
- Click the **play button** at the top to run all tests
- Right-click on any test for additional options (run, debug, etc.)

##### Using the Command Palette

- `Python: Run All Tests`: Runs all discovered tests
- `Python: Run Current Test File`: Runs tests in the currently open file
- `Python: Debug All Tests`: Runs all tests in debug mode

#### Viewing Test Results

- Test results appear in the Test Explorer with ✓ (pass) or ✗ (fail) icons
- Click on any failed test to see the error message and stack trace
- The **Output** panel shows detailed pytest output

#### Tips for `uv` Projects

- VSCode automatically detects the virtual environment in `.venv`
- No need to manually activate the environment - VSCode handles this
- If tests aren't discovered, ensure the Python interpreter is set to your
  `.venv` Python
- You can verify the interpreter in the bottom-right corner of VSCode (should
  show `.venv`)

## `pytest`Actions

- `pytest` operates in two distinct stages: **test discovery** and **test
  execution**

### Stage 1: Test Discovery

- `pytest` automatically scans your project to find all test files and test
  functions
- Discovery starts from the current directory by default, or you can specify a
  path: `pytest tests/`
- You can see what tests were discovered with: `pytest --collect-only`

#### What pytest looks for:

**Test files** must match these naming patterns:

- `test_*.py` (e.g., `test_calculator.py`)
- `*_test.py` (e.g., `calculator_test.py`)
- These files can be in subdirectories / folders

**Test functions** must:

- Start with `test_` (e.g., `def test_addition():`)
- Be at module level (not inside a class) OR inside a class starting with `Test`

**Test classes** (optional grouping):

- Must start with `Test` (e.g., `class TestCalculator:`)
- Must contain methods starting with `test_`

**What is NOT discovered** by pytest:

- Functions that don't start with `test_`
- Methods in classes that don't start with `Test`
- Files that don't match the naming pattern
- Any function named just `test` (too short, needs descriptive name)

### Stage 2: Test Execution

- After discovery, `pytest` runs each collected test function/method
- Tests are executed in the order they were discovered
- Each test runs independently in isolation
- `pytest` reports:
  - `.` for each passing test
  - `F` for each failing test
  - `E` for tests with errors
- Final summary shows total tests run, passed, failed, and execution time

> Very often, tests are located in the `tests` folder, at the root of the
> folder.

---

## What are Tests?

Tests in pytest are Python functions that verify your code behaves correctly.
They follow specific naming conventions so pytest can automatically discover
them.

### Anatomy of a Test

A test consists of several parts:

1. **Arrange**: Set up the data and conditions
2. **Act**: Execute the code being tested
3. **Assert**: Verify the result is what you expect
4. **Cleanup**: test clears any created artifacts / state so that other tests
   aren't influenced

### The Simplest Test

- The most basic test is a function that starts with `test_` and uses `assert`.
- The code being tested must always be imported.

```python
# test_simple.py

def test_always_passes():
    assert True  # This test always passes

def test_basic_math():
    assert 2 + 2 == 4  # Tests that Python can add
```

### Testing a Simple Function

Let's test a real function step by step:

```python
# calculator.py (the code we want to test)

def add(a, b):
    return a + b
```

```python
# test_calculator.py (our test file)

from calculator import add # get code to be tested

def test_add_positive_numbers():
    # Arrange: prepare the input
    num1 = 5
    num2 = 3

    # Act: call the function
    result = add(num1, num2)

    # Assert: check the result
    assert result == 8

    # no cleanup is necessary
```

### Multiple Assertions in One Test

You can have multiple assertions to test different scenarios:

```python
def test_add_various_numbers():
    assert add(2, 3) == 5
    assert add(0, 0) == 0
    assert add(-1, 1) == 0
    assert add(100, 200) == 300
```

### Testing with Classes (Covered Later)

Tests can also be organized in classes (class name must start with `Test`):

```python
# test_something.py
class TestCalculator:
  def test_addition(self):    # This IS run by pytest
    assert add(2, 2) == 4

  def test_subtraction(self): # This too
    assert 5 - 3 == 2
```

## Assert Aside

### What is `assert`?

- `assert` is a Python keyword used to test if a condition is true
  - Reference:
    [`assert` statement](https://docs.python.org/3/reference/simple_stmts.html#grammar-token-python-grammar-assert_stmt)
- Syntax: `assert <condition>, <optional_message>`

## How `assert` Works

When Python encounters an `assert` statement:

1. It evaluates the condition (expression after `assert`)
2. **If the condition is `True`**: Nothing happens, execution continues
3. **If the condition is `False`**: An `AssertionError` is raised

### Basic Examples

```python
# This passes - no error
assert True
assert 5 > 3
assert "hello" == "hello"

# These fail - raise AssertionError
assert False
assert 5 < 3
assert "hello" == "goodbye"
```

## Assert in `pytest` Unit Tests

In pytest, `assert` is the primary way to verify test expectations:

```python
def test_addition():
    result = 2 + 2
    assert result == 4  # Test passes if True, fails if False

def test_string_operations():
    name = "Alice"
    assert len(name) == 5
    assert name.startswith("A")
    assert "li" in name
```

## Common Assert Uses

### Testing Equality

```python
assert actual == expected
assert result != wrong_value
```

### Testing Comparisons

```python
assert score > 0
assert age >= 18
assert temperature < 100
assert count <= max_count
```

### Testing Boolean Values

```python
assert is_valid
assert not is_empty
assert user.is_active()
```

### Testing Membership

```python
assert item in collection
assert key in dictionary
assert "error" not in response
```

### Testing Types

```python
assert isinstance(value, int)
assert type(result) == str
```

## Pytest's Enhanced Assert

Pytest provides **introspection** - when an assertion fails, it shows detailed
information:

```python
def test_calculation():
    expected = 10
    actual = 2 * 4
    assert actual == expected
```

**Output when it fails:**

```
AssertionError: assert 8 == 10
  where 8 = (2 * 4)
```

Pytest automatically shows:

- The actual values
- The expected values
- The expression that was evaluated

## How to test for exceptions?

- It is sometimes _expected_ that your code raises exceptions - i.e. fails

```python
def add_values(a, b):
    if type(a) is not int or type(b) is not int:
        raise TypeError("Invalid value")
    return a+b
```

### The test

- Use the `with pytest.raises(<NAME>)` to catch the expected Exception `<NAME>`

```python
import pytest

def test_add_values_invalid():
  with pytest.raises(TypeError):
    result = add_values([1], [2])
```

## Code Coverage

### What is Code Coverage?

**Code coverage** measures what percentage of your code is executed by your
tests.

- **Goal**: Ensure all critical code paths are tested
- **Industry standard**: 80-90% coverage for production code
- **Not a guarantee**: 100% coverage doesn't mean bug-free code, but low
  coverage means untested code

### Why Measure Coverage?

- Identifies **untested code** that could harbor bugs
- Provides **confidence** that changes won't break functionality
- Helps find **dead code** that's never executed
- Guides where to write **additional tests**

### Installing Coverage Tools

```bash
uv add --dev pytest-cov
```

### Running Tests with Coverage

**Basic coverage report** (terminal output):

```bash
pytest --cov=.
```

**Specify what to cover**:

```bash
pytest --cov=calculator         # Single module
pytest --cov=mypackage          # Package
pytest --cov=src                # Specific directory
```

**Generate HTML report** (recommended):

```bash
pytest --cov=. --cov-report=html
```

This creates an `htmlcov/` folder. Open `htmlcov/index.html` in your browser to
see:

- Overall coverage percentage
- Line-by-line coverage for each file
- Highlighted lines showing what's tested (green) and what's not (red)

### Common Coverage Options

```bash
# Show which lines are missing coverage
pytest --cov=. --cov-report=term-missing

# Stop on first failure, still show coverage
pytest -x --cov=.

# Only test specific files, show coverage
pytest tests/test_math.py --cov=calculator
```

### Best Practices

#### **Do**:

- Aim for 80%+ coverage on core business logic
- Focus on testing critical paths first
- Use coverage to find gaps in your test suite

#### **Don't**:

- Obsess over 100% coverage (diminishing returns)
- Write meaningless tests just to increase coverage
- Test trivial code (simple getters/setters)

> **Reference**:
> [5 questions every unit test must answer](https://medium.com/javascript-scene/what-every-unit-test-needs-f6cd34d9836d)

---

## Developing with an Iterative Test-Oriented Mindset

### Goals

- Make sure that tests are actually written
- Validate the requirements and design
- You become the 'user' of the code you are about to write
- You can work with stakeholders to resolve the anomalies/gaps

### Issues

- Requires discipline
- "I am a developer, I want to code and not test"

## Unit testing: best practices

- Be reasonable
- No more test code than application code
- Code coverage of 80% is a good objective
- One minor change in the tests = one minor change in the application
- True for software development in general

## References

1. [Getting Started with Pytest](https://learning.oreilly.com/library/view/python-testing-with/9781680509427/f_0013.xhtml#ch.getting_started)]
2. [Writing Test Functions](https://learning.oreilly.com/library/view/python-testing-with/9781680509427/f_0019.xhtml#ch.test_functions)
3. [Pytest Documentation](https://docs.pytest.org/en/stable/)
