# Monkey Patching in Python Tests

Before these notes, read [A Gentle Introduction to Python Lambda Functions](../../lambdas/notes/lambda.md).
We will use lambdas to create simple replacement functions.

## Why Do We Need Monkey Patching?

Unit tests should test the code under test in isolation. However, that code
often depends on external systems or operations that are slow, unreliable,
expensive, or difficult to configure for specific test conditions.

Monkey patching temporarily replaces a dependency during a test. It is useful
when the real dependency would make the test slow, unreliable, expensive, or
difficult to configure. For example, a test can replace a network request,
database connection, file operation, clock, or user input with a predictable
replacement. Pytest restores the original object after the test, so the patch
does not affect other tests.

## What is Monkey Patching?

Monkey patching is dynamically modifying code at runtime. In testing, we use
it to temporarily replace parts of code, generally functions, methods, classes,
or values, for the duration of a test.

`monkeypatch` is a fixture built into pytest that allows you to intercept what a
function would normally do, substituting its full execution with a return value
of your own specification. Note that monkey patching a function call does not
count as actually testing that function call.

## When Should Monkey Patching Be Used?

Use monkey patching when the test needs to change what the code under test
can access. Typical use cases include:

- Replacing a function with a simple test function or lambda
- Setting or deleting environment variables
- Changing dictionary values or configuration settings
- Changing the current directory or another pytest-managed test condition

## `pytest monkeypatch`

The `monkeypatch` fixture is built into pytest (no additional packages needed).
It provides a simple way to temporarily modify objects, functions, or
environment variables.

### When to Use pytest monkeypatch

- When you want automatic cleanup after tests
- When the replacement is simple (replacing function/attribute values)
- When you prefer pytest's fixture-based style
- When you need to replace environment variables or dictionary values

### Basic Example: A Weather App

Suppose we have a module that makes API calls:

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

A test of `should_bring_jacket()` should not make a real network request. The
request would be slow, could fail if the network is down, and the returned
temperature would change from run to run. Instead, the test replaces
`get_temperature()` with a simple function that returns a known value.

#### `test_weather_monkeypatch.py`

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

#### 1. Setting Attributes

```python
def test_example(monkeypatch):
    # Replace a function
    monkeypatch.setattr('module.function_name', lambda: 42)

    # Replace a class attribute
    monkeypatch.setattr('module.ClassName.attribute', 'new_value')
```

#### 2. Setting Environment Variables

```python
def test_with_env_var(monkeypatch):
    monkeypatch.setenv('API_KEY', 'test-key-12345')
    # Code that reads os.environ['API_KEY'] will get 'test-key-12345'
```

#### 3. Deleting Attributes

```python
def test_without_optional_feature(monkeypatch):
    monkeypatch.delattr('module.optional_function')
    # Now accessing optional_function will raise AttributeError
```

#### 4. Modifying Dictionaries

```python
def test_dict_modification(monkeypatch):
    my_dict = {'key': 'original'}
    monkeypatch.setitem(my_dict, 'key', 'modified')
    assert my_dict['key'] == 'modified'
```

### Example: Replacing User Input

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
    # Replace input so it returns "4"
    monkeypatch.setattr('builtins.input', lambda prompt: "4")

    result = ask_question("What is 2+2?", "4")
    assert result is True

def test_ask_question_incorrect(monkeypatch):
    monkeypatch.setattr('builtins.input', lambda prompt: "5")

    result = ask_question("What is 2+2?", "4")
    assert result is False

def test_run_quiz_perfect_score(monkeypatch):
    # Replace input so it returns correct answers
    answers = iter(["4", "Ottawa"])
    monkeypatch.setattr('builtins.input', lambda prompt: next(answers))

    score = run_quiz()
    assert score == 2
```

### Example: Replacing an Environment Variable

Suppose `convert_temperature()` reads the `TEMP_UNIT` environment variable to
decide whether a value should be converted. This test sets that variable to a
known value without changing the student's real environment. Pytest restores
the original environment after the test.

```python
def test_temperature_conversion(monkeypatch):
    # Replace the environment value read by convert_temperature().
    monkeypatch.setenv('TEMP_UNIT', 'celsius')

    result = convert_temperature(100)
    assert result == 100  # No conversion needed
```

## Quick Reference

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

## Summary

- Monkey patching temporarily replaces a dependency during a test
- The pytest `monkeypatch` fixture is simple and clean for straightforward
  replacements of functions, attributes, environment variables, and dictionary
  values
- Pytest automatically restores the original objects after each test
- Monkey patching a function call does not count as testing that function

## What's Next

Monkey patching installs a replacement, but a plain function or lambda cannot
record how it was used. When a test needs to verify calls, arguments, or call
counts, or needs a substitute with more complex behavior, use mocking. 