# Testing Python with pytest

## Why Test?

You already test programs when you run them and inspect the output. This is
manual testing. Automated testing is code that checks your program's behaviour
for you.

This course focuses on unit tests: fast, repeatable tests for one function,
method, or class at a time. They let you verify a change quickly and prevent a
previously working feature from breaking.

## Iterative Development and TDD

Iterative development builds software in small cycles. Each cycle adds or
improves one behaviour, verifies it with tests, and uses the result to guide the
next cycle.

Test-Driven Development (TDD) is one way to work iteratively:

1. Red: Write a failing test for the behaviour you want.
1. Green: Write the smallest amount of code that makes the test pass.
1. Refactor: Improve the code while keeping the tests passing.

## Your First pytest Test

`pytest` is a third-party Python testing framework. It discovers test files and
test functions automatically, runs them, and reports which tests pass or fail.
Tests use Python's regular `assert` statement.

Install pytest as a project development dependency:

```bash
uv add --dev pytest
```

Create a function to test:

```python
# calculator.py
def divide(a, b):
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b
```

```python
# test_calculator.py
import pytest
from calculator import divide

def test_divide():
    assert divide(10, 2) == 5

Install pytest as a **development dependency** (not needed for production):

For course projects, add pytest once with `uv add --dev pytest`, then run it
through `uv`. The `--dev` flag identifies pytest as a development and testing
tool rather than an application dependency.

```bash
uv run pytest
uv run pytest tests/
uv run pytest tests/test_calculator.py
```

`uv run` uses the project environment for this command without changing your
terminal session.

### Useful Options

- `uv run pytest -v`: Show each test name.
- `uv run pytest -k "pattern"`: Run tests whose names match a pattern.
- `uv run pytest -x`: Stop after the first failure.
- `uv run pytest --lf`: Re-run only tests that failed last time.

### Alternatives

If pytest was installed in an activated virtual environment, run `pytest`
directly. A system-wide `pip install -U pytest` also makes `pytest` available,
but this is not recommended for project work because its version is shared by
every project on the computer.

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

## How pytest Finds Tests

`pytest` first discovers test files and test functions, then runs the tests it
finds. Use `uv run pytest --collect-only` to see the tests before running them.

- Test files are usually named `test_*.py`, such as `test_calculator.py`.
  `*_test.py` is also supported.
- Test functions start with `test_`, such as `def test_addition():`.
- Optional test classes start with `Test`, and their test methods start with
  `test_`.
- Store test files in a `tests` folder at the project root when practical.

Do not rely on test execution order. Each test should set up the state it needs
and leave no state that affects another test.

## Writing Useful Tests

Use Arrange, Act, Assert to keep each test focused:

1. Arrange: Create the input values and required objects.
1. Act: Call the function or method being tested.
1. Assert: Check the expected result with `assert`.

An assertion passes when its condition is `True`. When the condition is `False`,
pytest reports the failure and shows the actual values.

```python
assert actual == expected
assert item in collection
assert is_valid
```

Write a separate test for each important behaviour or input case. Test classes
are optional and are covered later.

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

#### Basic Coverage Report
(terminal output):

```bash
pytest --cov=.
```

#### Specify what to cover

```bash
pytest --cov=calculator         # Single module
pytest --cov=mypackage          # Package
pytest --cov=src                # Specific directory
```

#### Generate HTML report

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

1. [Get Started - pytest documentation](https://docs.pytest.org/en/stable/getting-started.html)
1. [Getting Started with Pytest: Python Testing with pytest Book](https://learning.oreilly.com/library/view/python-testing-with/9781680509427/f_0013.xhtml#ch.getting_started)]
2. [Writing Test Functions: Python Testing with pytest Book]](https://learning.oreilly.com/library/view/python-testing-with/9781680509427/f_0019.xhtml#ch.test_functions)
3. [Pytest Documentation](https://docs.pytest.org/en/stable/)
