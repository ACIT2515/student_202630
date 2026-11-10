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

### What Fixtures Give You

- No repeated setup: write the setup once, request it in any test that needs it.
- Test isolation: by default every test gets a fresh copy of the fixture, so one
  test cannot change the data another test sees.
- Guaranteed cleanup: teardown code in a fixture runs even when a test fails
  (see Fixture with Setup and Cleanup below).
- One place to change: when the setup changes, update the fixture instead of
  every test.

### Why Not Just a Helper Function?

A plain helper function can also remove duplicated setup, but you would have to
call it yourself at the start of every test. Fixtures add what helpers cannot:

- pytest injects them automatically by parameter name
- cleanup code after `yield` always runs, even when the test fails
- `scope` controls how often they are built
- `conftest.py` shares them across files with no imports

Use a helper function for small calculations inside a test. Use a fixture for
anything that sets up the environment the test runs in.

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

### Fixture Using Another Fixture

A fixture can request another fixture the same way a test requests a fixture:
list the fixture name as a parameter and pytest will build it first and pass it
in.

```python
@pytest.fixture
def hostname():
    return "webserver01"

@pytest.fixture
def server_config(hostname):  # uses the hostname fixture
    """Build a configuration dictionary for the server"""
    return {"hostname": hostname, "port": 8080, "ip": "192.168.1.10"}

def test_config_hostname(server_config):
    assert server_config["hostname"] == "webserver01"

def test_config_port(server_config):
    assert server_config["port"] == 8080
```

**How it works**: pytest sees that `server_config` needs `hostname`, so it calls
`hostname` first and passes the result into `server_config`. The Fixture
Creating Test Files pattern later in these notes uses the same idea with the
built-in `tmp_path` fixture.

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

### `scope='class'`

Runs **once per test class**, shared by all tests in that class:

```python
@pytest.fixture(scope='class')
def server_connection():
    """Created once for the whole class"""
    return connect_to_server("192.168.1.10")

class TestServerStatus:
    def test_is_online(self, server_connection):
        assert server_connection.is_online()

    def test_uptime(self, server_connection):
        # Uses the SAME connection as test_is_online
        assert server_connection.uptime() > 0
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

| Scope      | When It Runs             | Use Case                           |
| ---------- | ------------------------ | ---------------------------------- |
| `function` | Once per test (default)  | Most common, tests are isolated    |
| `class`    | Once per test class      | Group related tests                |
| `module`   | Once per file            | Expensive setup shared in one file |
| `session`  | Once for entire test run | Very expensive setup (rare)        |

---

## Built-in Pytest Fixtures

Pytest provides useful fixtures out of the box: see
[Pytest Fixtures Reference](https://docs.pytest.org/en/stable/reference/fixtures.html)

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

The teardown code after `yield` runs even when the test fails. This is why
cleanup belongs in the fixture instead of at the end of the test: connections
get closed and temporary resources get removed no matter what the test does.

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

## References

1. [pytest: About Fixtures](https://docs.pytest.org/en/stable/explanation/fixtures.html)
1. [pytest: How to use temporary directories and files in tests](https://docs.pytest.org/en/stable/how-to/tmp_path.html)
1. [pytst: How to capture stdout/stderr output](https://docs.pytest.org/en/stable/how-to/capture-stdout-stderr.html)
