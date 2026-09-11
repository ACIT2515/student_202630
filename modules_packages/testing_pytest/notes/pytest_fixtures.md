# Pytest Fixtures

## What are Fixtures?

**Fixtures** are a way to provide **reusable setup code** for your tests.

### The Problem Fixtures Solve

Without fixtures, you often repeat the same setup code:

```python
def test_addition():
    calculator = Calculator()  # Setup repeated
    result = calculator.add(2, 3)
    assert result == 5

def test_subtraction():
    calculator = Calculator()  # Same setup repeated
    result = calculator.subtract(5, 3)
    assert result == 2

def test_multiplication():
    calculator = Calculator()  # Same setup again!
    result = calculator.multiply(4, 3)
    assert result == 12
```

### The Fixture Solution

Fixtures eliminate this repetition:

```python
import pytest

@pytest.fixture
def calculator():
    """Provide a Calculator instance for tests"""
    return Calculator()

def test_addition(calculator):  # Fixture automatically provided
    result = calculator.add(2, 3)
    assert result == 5

def test_subtraction(calculator):  # Same fixture reused
    result = calculator.subtract(5, 3)
    assert result == 2

def test_multiplication(calculator):  # No repeated setup!
    result = calculator.multiply(4, 3)
    assert result == 12
```

---

## Creating Your First Fixture

### Basic Fixture Syntax

```python
import pytest

@pytest.fixture
def sample_data():
    """Fixture that returns test data"""
    return [1, 2, 3, 4, 5]

def test_list_length(sample_data):
    assert len(sample_data) == 5

def test_list_sum(sample_data):
    assert sum(sample_data) == 15
```

**How it works**:
1. Decorate a function with `@pytest.fixture`
2. The function name becomes the fixture name
3. Use the fixture name as a parameter in test functions
4. Pytest automatically calls the fixture and passes the result to your test

---

## Common Fixture Patterns

### Fixture Returning Simple Values

```python
@pytest.fixture
def username():
    return "test_user"

@pytest.fixture
def age():
    return 25

def test_user_info(username, age):
    assert username == "test_user"
    assert age == 25
```

### Fixture Creating Test Files

```python
import pytest

@pytest.fixture
def test_file(tmp_path):  # tmp_path is a built-in fixture
    """Create a temporary test file"""
    file_path = tmp_path / "test.txt"
    file_path.write_text("Hello, World!")
    return file_path

def test_file_content(test_file):
    content = test_file.read_text()
    assert content == "Hello, World!"

def test_file_exists(test_file):
    assert test_file.exists()
```

### Fixture with Setup and Cleanup

```python
@pytest.fixture
def database_connection():
    """Setup: Create connection, Teardown: Close it"""
    # Setup
    connection = create_db_connection()
    
    yield connection  # Provide to test
    
    # Teardown (runs after test completes)
    connection.close()

def test_database_query(database_connection):
    result = database_connection.query("SELECT * FROM users")
    assert len(result) > 0
```

---

## Fixture Scope

By default, fixtures run **once per test**. You can change this with `scope`:

### `scope='function'` (default)

Runs before/after each test function:

```python
@pytest.fixture(scope='function')
def counter():
    return {"count": 0}

def test_increment(counter):
    counter["count"] += 1
    assert counter["count"] == 1

def test_increment_again(counter):
    counter["count"] += 1
    assert counter["count"] == 1  # Fresh counter each time!
```

### `scope='module'`

Runs **once per file**, shared by all tests in that file:

```python
@pytest.fixture(scope='module')
def expensive_setup():
    """Only runs once for all tests in this file"""
    print("Setting up expensive resource...")
    return ExpensiveResource()

def test_one(expensive_setup):
    # Uses the shared resource
    pass

def test_two(expensive_setup):
    # Uses the SAME resource (not recreated)
    pass
```

### Scope Options Summary

| Scope | When It Runs | Use Case |
|-------|-------------|----------|
| `function` | Once per test (default) | Most common, tests are isolated |
| `class` | Once per test class | Group related tests |
| `module` | Once per file | Expensive setup shared in one file |
| `session` | Once for entire test run | Very expensive setup (rare) |

---

## Using Multiple Fixtures

Tests can use multiple fixtures:

```python
@pytest.fixture
def username():
    return "alice"

@pytest.fixture
def email():
    return "alice@example.com"

@pytest.fixture
def age():
    return 30

def test_user_profile(username, email, age):
    profile = create_profile(username, email, age)
    assert profile.username == "alice"
    assert profile.email == "alice@example.com"
    assert profile.age == 30
```

### Fixtures Can Use Other Fixtures

```python
@pytest.fixture
def base_url():
    return "https://api.example.com"

@pytest.fixture
def api_endpoint(base_url):  # Uses base_url fixture
    return f"{base_url}/users"

def test_api_call(api_endpoint):
    assert api_endpoint == "https://api.example.com/users"
```

---

## Built-in Pytest Fixtures

Pytest provides useful fixtures out of the box:

### `tmp_path` - Temporary Directory

Creates a unique temporary folder for each test:

```python
def test_create_file(tmp_path):
    # tmp_path is a pathlib.Path to a temporary directory
    test_file = tmp_path / "output.txt"
    test_file.write_text("Test data")
    
    assert test_file.exists()
    assert test_file.read_text() == "Test data"
    # Automatically cleaned up after test!
```

### `capsys` - Capture Print Output

Captures what your code prints:

```python
def greet(name):
    print(f"Hello, {name}!")

def test_greeting(capsys):
    greet("Alice")
    
    captured = capsys.readouterr()
    assert captured.out == "Hello, Alice!\n"
```

### See All Built-in Fixtures

```bash
pytest --fixtures
```

---

## Sharing Fixtures: `conftest.py`

Put fixtures in `conftest.py` to share them across multiple test files:

```
project/
├── conftest.py          # Shared fixtures here
├── test_math.py
└── test_strings.py
```

**conftest.py**:
```python
import pytest

@pytest.fixture
def sample_list():
    """Available to all test files"""
    return [1, 2, 3, 4, 5]
```

**test_math.py**:
```python
def test_sum(sample_list):  # No import needed!
    assert sum(sample_list) == 15
```

**test_strings.py**:
```python
def test_length(sample_list):  # Same fixture available here
    assert len(sample_list) == 5
```

---

## Debugging Fixtures

See the order fixtures run:

```bash
pytest --setup-show
```

Example output:
```
test_example.py::test_addition
  SETUP    F username
  SETUP    F calculator
    test_example.py::test_addition (fixtures used: calculator, username)
  TEARDOWN F calculator
  TEARDOWN F username
```

---

## Best Practices

**Do**:
- Use fixtures to eliminate duplicate setup code
- Give fixtures descriptive names (`user_data`, not `data`)
- Use `tmp_path` for file operations in tests
- Put shared fixtures in `conftest.py`

**Don't**:
- Make fixtures too complex (keep them simple)
- Use fixtures when simple variables would suffice
- Forget that the default `function` scope creates fresh fixtures per test

---

## Quick Reference

```python
# Basic fixture
@pytest.fixture
def my_fixture():
    return "some value"

# Fixture with cleanup
@pytest.fixture
def resource():
    r = setup_resource()
    yield r
    cleanup_resource(r)

# Fixture with scope
@pytest.fixture(scope='module')
def shared_resource():
    return expensive_setup()

# Using fixtures in tests
def test_something(my_fixture, resource):
    assert my_fixture == "some value"
    assert resource is not None
```

---

## Summary

- **Fixtures** = reusable test setup
- Decorate with `@pytest.fixture`
- Use as test function parameters
- Control when they run with `scope`
- Share across files with `conftest.py`
- Built-in fixtures like `tmp_path` and `capsys` are powerful tools