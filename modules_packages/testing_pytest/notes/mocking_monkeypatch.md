# Mocking and Monkey Patching in Python Tests

## Why Do We Need Mocking?

When writing unit tests, you want to test your code in isolation. However, your
code often depends on external systems or operations that are:

- **Slow**: Network requests, database queries, file I/O operations
- **Unpredictable**: External APIs, random number generators, timestamps
- **Expensive**: Paid API calls, resource-intensive operations
- **Difficult to set up**: Specific error conditions, edge cases

Mocking allows you to replace these dependencies with controlled, predictable
substitutes during testing.

## What is Mocking?

**Mocking** is the practice of replacing real objects or functions with fake
versions (called "mocks") that:

- Return predetermined values
- Allow you to verify they were called correctly
- Don't actually perform the real operation

## What is Monkey Patching?

**Monkey Patching** is dynamically modifying code at runtime. In testing, we use
it to temporarily replace parts of code (generally functions and methods, but
sometimes classes) with mocks or different implementations for the duration of a
test.

`monkeypatch` is a part of the `pytest-mock` library that allows you to
intercept what a function would normally do, substituting its full execution
with a return value of your own specification. Note that monkey patching a
function call does not count as actually testing that function call

## Mocking: `unittest.mock`

The `unittest.mock` module is part of Python's standard library (no installation
needed). It provides the `Mock` class and the `patch()` function.

### When to Use unittest.mock

- When you need to create mock objects with complex behavior
- When you want to verify method calls and arguments
- When you need to mock class methods or entire classes

### Basic Example: Mocking a Function

Let's say we have a module that makes API calls:

#### `weather.py`

```python
import requests

def get_temperature(city):
    """Fetch the current temperature for a city."""
    response = requests.get(f"https://api.weather.com/current/{city}")
    data = response.json()
    return data['temperature']

def should_bring_jacket(city):
    """Determine if you need a jacket based on temperature."""
    temp = get_temperature(city)
    return temp < 15
```

#### `test_weatherpy` using `unittest.mock`

```python
from unittest.mock import patch, Mock
from weather import should_bring_jacket

def test_should_bring_jacket_cold():
    # Mock get_temperature to return a cold temperature
    with patch('weather.get_temperature') as mock_get_temp:
        mock_get_temp.return_value = 10

        result = should_bring_jacket("Vancouver")

        assert result is True
        mock_get_temp.assert_called_once_with("Vancouver")

def test_should_bring_jacket_warm():
    with patch('weather.get_temperature') as mock_get_temp:
        mock_get_temp.return_value = 20

        result = should_bring_jacket("Vancouver")

        assert result is False
```

### Key Features of unittest.mock

**1. Creating Mock Objects**

```python
from unittest.mock import Mock

# Create a mock object
mock_obj = Mock()

# Set return values
mock_obj.some_method.return_value = 42

# Use it
result = mock_obj.some_method()  # Returns 42
```

**2. Verifying Calls**

```python
mock_obj.some_method("arg1", "arg2")

# Check if called
mock_obj.some_method.assert_called()
mock_obj.some_method.assert_called_once()
mock_obj.some_method.assert_called_with("arg1", "arg2")

# Check call count
assert mock_obj.some_method.call_count == 1
```

**3. Patching with Decorators**

```python
from unittest.mock import patch

@patch('weather.get_temperature')
def test_with_decorator(mock_get_temp):
    mock_get_temp.return_value = 10
    # Test code here
```

The `@patch` decorator provides an alternative way to mock functions without
using a context manager. When you place `@patch('weather.get_temperature')`
above your test function, it automatically creates a mock object for the
`get_temperature` function in the `weather` module and passes that mock as an
additional parameter to your test function (in this case, `mock_get_temp`). This
means the entire test function runs with the mock in place, and you can
configure the mock's behavior (like setting its return value to 10) at the start
of the test. The decorator approach is cleaner when you need the mock for the
entire test, as opposed to the `with patch()` context manager which is better
when you only need the mock for a specific section of code. When the test
finishes, the decorator automatically restores the original function, ensuring
no side effects carry over to other tests.

### Example: Mocking File Operations

#### `file_processor.py`

```python
def count_lines(filename):
    """Count the number of lines in a file."""
    with open(filename, 'r') as f:
        return len(f.readlines())

def is_short_file(filename):
    """Check if a file has fewer than 100 lines."""
    return count_lines(filename) < 100
```

#### `test_file_processor.py`

```python
from unittest.mock import patch, mock_open
from file_processor import is_short_file

def test_is_short_file_true():
    # Mock file content with 50 lines
    mock_file_content = "\n".join([f"line {i}" for i in range(50)])

    with patch('builtins.open', mock_open(read_data=mock_file_content)):
        result = is_short_file("test.txt")
        assert result is True

def test_is_short_file_false():
    # Mock file content with 150 lines
    mock_file_content = "\n".join([f"line {i}" for i in range(150)])

    with patch('builtins.open', mock_open(read_data=mock_file_content)):
        result = is_short_file("test.txt")
        assert result is False
```

#### Explanation

This demonstrates how to test file operations without actually creating
or reading real files. The tests use `mock_open`, a specialized helper from
`unittest.mock` designed specifically for mocking file operations.

* With `open("test.txt", 'r')`, the mock intercepts that call and returns a 
  fake file object that contains the data you specified with `read_data`

* first test, we create a string representing 50 lines of text using
    `"\n".join([f"line {i}" for i in range(50)])`, 
    which generates "line 0\nline 1\nline 2..." up to line 49.

* `patch('builtins.open', mock_open(read_data=mock_file_content))` 
    replaces Python's built-in `open()` function with our mock version. 
    The string `'builtins.open'` refers to the actual `open()` function that
    lives in Python's built-in namespace

* When `is_short_file("test.txt")` runs inside the patched context, it calls
    `count_lines("test.txt")`, which in turn calls `open(filename, 'r')`. Instead of
    trying to find an actual file named "test.txt" on your computer, the mock
    returns a fake file object containing our 50 lines. The `readlines()` method on
    this fake file object returns a list of 50 strings, so `len(f.readlines())`
    returns 50, and since 50 < 100, the function returns `True`, which we verify
    with the assertion.

The second test works identically but with 150 lines instead of 50, allowing us
to test both branches of the logic (files with fewer than 100 lines and files
with 100 or more lines) without creating any actual test files or worrying about
file cleanup. This approach makes the tests fast, reliable, and independent of
the file system.

---

## `pytest monkeypatch`

The `monkeypatch` fixture is built into pytest (no additional packages needed).
It provides a simple way to temporarily modify objects, functions, or
environment variables.

### When to Use pytest monkeypatch

- When you want automatic cleanup after tests
- When mocking is simple (replacing function/attribute values)
- When you prefer pytest's fixture-based style
- When you need to mock environment variables or dictionary values

### Basic Example: Same Weather App

**test_weather_monkeypatch.py**

```python
import pytest
from weather import should_bring_jacket

def test_should_bring_jacket_cold(monkeypatch):
    # Replace get_temperature with a simple function
    def mock_get_temp(city):
        return 10

    monkeypatch.setattr('weather.get_temperature', mock_get_temp)

    result = should_bring_jacket("Vancouver")
    assert result is True

def test_should_bring_jacket_warm(monkeypatch):
    monkeypatch.setattr('weather.get_temperature', lambda city: 20)

    result = should_bring_jacket("Vancouver")
    assert result is False
```

### Key Features of pytest monkeypatch

**1. Setting Attributes**

```python
def test_example(monkeypatch):
    # Replace a function
    monkeypatch.setattr('module.function_name', lambda: 42)

    # Replace a class attribute
    monkeypatch.setattr('module.ClassName.attribute', 'new_value')
```

**2. Setting Environment Variables**

```python
def test_with_env_var(monkeypatch):
    monkeypatch.setenv('API_KEY', 'test-key-12345')
    # Code that reads os.environ['API_KEY'] will get 'test-key-12345'
```

**3. Deleting Attributes**

```python
def test_without_optional_feature(monkeypatch):
    monkeypatch.delattr('module.optional_function')
    # Now accessing optional_function will raise AttributeError
```

**4. Modifying Dictionaries**

```python
def test_dict_modification(monkeypatch):
    my_dict = {'key': 'original'}
    monkeypatch.setitem(my_dict, 'key', 'modified')
    assert my_dict['key'] == 'modified'
```

### Example: Mocking User Input

**quiz.py**

```python
def ask_question(question, correct_answer):
    """Ask user a question and check if they got it right."""
    user_answer = input(f"{question} ")
    return user_answer.lower() == correct_answer.lower()

def run_quiz():
    """Run a simple quiz and return the score."""
    score = 0
    if ask_question("What is 2+2?", "4"):
        score += 1
    if ask_question("What is the capital of Canada?", "Ottawa"):
        score += 1
    return score
```

**test_quiz.py**

```python
import pytest
from quiz import ask_question, run_quiz

def test_ask_question_correct(monkeypatch):
    # Mock input to return "4"
    monkeypatch.setattr('builtins.input', lambda prompt: "4")

    result = ask_question("What is 2+2?", "4")
    assert result is True

def test_ask_question_incorrect(monkeypatch):
    monkeypatch.setattr('builtins.input', lambda prompt: "5")

    result = ask_question("What is 2+2?", "4")
    assert result is False

def test_run_quiz_perfect_score(monkeypatch):
    # Mock input to return correct answers
    answers = iter(["4", "Ottawa"])
    monkeypatch.setattr('builtins.input', lambda prompt: next(answers))

    score = run_quiz()
    assert score == 2
```

---

## Comparison: When to Use Which?

| Feature                   | unittest.mock                      | pytest monkeypatch                |
| ------------------------- | ---------------------------------- | --------------------------------- |
| **Installation**          | Built into Python                  | Built into pytest                 |
| **Complexity**            | Good for complex mocking           | Best for simple replacements      |
| **Verification**          | Can verify calls and arguments     | No built-in verification          |
| **Style**                 | Context managers or decorators     | Fixture-based                     |
| **Cleanup**               | Manual (or via context manager)    | Automatic after test              |
| **Mock objects**          | Creates sophisticated Mock objects | Replaces with your function/value |
| **Environment variables** | Requires additional setup          | Simple `setenv()` method          |

### Guidelines for Choosing

**Use unittest.mock when:**

- You need to verify that a function was called with specific arguments
- You need complex mock behavior (side effects, multiple return values)
- You want to mock entire classes or create complex mock object hierarchies
- You need to count how many times something was called

**Use pytest monkeypatch when:**

- You simply need to replace a function with a known return value
- You're mocking environment variables
- You prefer pytest's fixture style
- The mock is straightforward and doesn't need verification

**Example where unittest.mock is better:**

```python
@patch('requests.post')
def test_api_error_handling(mock_post):
    # Need to verify exact arguments sent to API
    mock_post.return_value.status_code = 500

    result = send_notification("Test message")

    # Verify the exact API call
    mock_post.assert_called_once_with(
        "https://api.example.com/notify",
        json={"message": "Test message"},
        headers={"Authorization": "Bearer token"}
    )
    assert result is False
```

**Example where monkeypatch is better:**

```python
def test_temperature_conversion(monkeypatch):
    # Simply need to set an environment variable
    monkeypatch.setenv('TEMP_UNIT', 'celsius')

    result = convert_temperature(100)
    assert result == 100  # No conversion needed
```

---

## Setting Up Your Test Environment

Since you're using `uv` for dependency management, pytest is likely already
installed. If you need to add it:

```bash
uv add --dev pytest
```

No additional packages are needed! `unittest.mock` is in the standard library and `pytest.monkeypatch`
is part of `pytest`.

---

## Quick Reference

### unittest.mock Cheat Sheet

```python
from unittest.mock import Mock, patch, mock_open

# Create a mock
mock = Mock(return_value=42)

# Patch a function (context manager)
with patch('module.function') as mock_func:
    mock_func.return_value = 'value'
    # test code

# Patch a function (decorator)
@patch('module.function')
def test_something(mock_func):
    mock_func.return_value = 'value'

# Verify calls
mock_func.assert_called()
mock_func.assert_called_with('arg')
mock_func.assert_called_once()

# Mock file operations
with patch('builtins.open', mock_open(read_data='content')):
    # test code
```

### pytest monkeypatch Cheat Sheet

```python
# Replace a function/attribute
monkeypatch.setattr('module.function', lambda: 42)

# Set environment variable
monkeypatch.setenv('VAR_NAME', 'value')

# Delete an attribute
monkeypatch.delattr('module.attribute')

# Modify a dictionary
monkeypatch.setitem(dict_obj, 'key', 'value')

# Change current directory
monkeypatch.chdir('/tmp')
```

---

## Practice Exercise

Try mocking the following function using both approaches:

**calculator.py**

```python
import random

def get_random_operator():
    """Return a random math operator."""
    return random.choice(['+', '-', '*', '/'])

def create_math_problem():
    """Create a random math problem as a string."""
    num1 = random.randint(1, 10)
    num2 = random.randint(1, 10)
    operator = get_random_operator()
    return f"{num1} {operator} {num2}"
```

**Challenge**: Write tests for `create_math_problem()` that ensure it generates
specific problems by controlling the random values and operator.

<details>
<summary>Solution with unittest.mock</summary>

```python
from unittest.mock import patch
from calculator import create_math_problem

@patch('calculator.random.randint')
@patch('calculator.get_random_operator')
def test_create_math_problem(mock_operator, mock_randint):
    mock_randint.side_effect = [5, 3]  # First call returns 5, second returns 3
    mock_operator.return_value = '+'

    result = create_math_problem()
    assert result == "5 + 3"
```

</details>

<details>
<summary>Solution with pytest monkeypatch</summary>

```python
import random
from calculator import create_math_problem

def test_create_math_problem(monkeypatch):
    # Mock randint to return specific values
    call_count = 0
    def mock_randint(a, b):
        nonlocal call_count
        call_count += 1
        return 5 if call_count == 1 else 3

    monkeypatch.setattr('random.randint', mock_randint)
    monkeypatch.setattr('calculator.get_random_operator', lambda: '+')

    result = create_math_problem()
    assert result == "5 + 3"
```

</details>

---

## Summary

- **Mocking** replaces dependencies with controlled substitutes for testing
- **unittest.mock** is powerful for complex mocking with verification
- **pytest monkeypatch** is simple and clean for straightforward replacements
- Choose based on complexity and what you need to verify
