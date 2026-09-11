# Introduction to Pytest and TDD

## Learning Objectives

By the end of this exercise, you will be able to:
- Write simple functions in Python
- Create test functions using pytest
- Use the `assert` statement to verify code behavior
- Practice Test-Driven Development (TDD)
- Run tests using `pytest`

---

## Setup

1. Create a new folder for this exercise: `intro_pytest`
2. Using `uv` create a virtual environment and activate it
3. Install pytest: `uv add --dev pytest`

---

## Part 1: Your First Test (Write Tests First!)

In TDD, we **write tests before writing the actual code**. This helps us think about what we want our code to do.

### Step 1: Create the Test File

Create a file called `test_calculator.py`:

```python
# test_calculator.py

def test_add():
    """Test that add function works correctly"""
    result = add(2, 3)
    assert result == 5
```

### Step 2: Run the Test (It Should Fail!)

```bash
uv run pytest
```

**Expected output**: The test fails because `add()` doesn't exist yet. This is normal in TDD!

```
NameError: name 'add' is not defined
```

### Step 3: Write Minimal Code to Pass the Test

Create a file called `calculator.py`:

```python
# calculator.py

def add(a, b):
    # TODO: Implement this function
    pass
```

Update your test file to import the function:

```python
# test_calculator.py
from calculator import add

def test_add():
    """Test that add function works correctly"""
    result = add(2, 3)
    assert result == 5
```

### Step 4: Make the Test Pass

Implement the `add` function in `calculator.py` to make the test pass.

### Step 5: Run the Test Again

```bash
uv run pytest -v
```

**Expected output**: Test passes! ✓

---

## Part 2: Test Multiple Cases

Good tests check different scenarios. Add more test functions to `test_calculator.py`:

```python
def test_add_positive_numbers():
    """Test adding two positive numbers"""
    # TODO: Write this test
    pass

def test_add_negative_numbers():
    """Test adding two negative numbers"""
    # TODO: Write this test
    pass

def test_add_zero():
    """Test adding zero to a number"""
    # TODO: Write this test
    pass
```

**Your Task**: 
1. Implement each test function with appropriate assertions
2. Run the tests - they should all pass with your existing `add` function!

---

## Part 3: Subtract Function (Full TDD Cycle)

Now practice the full TDD cycle on your own:

### Step 1: Write Failing Tests First

Add these test functions to `test_calculator.py`:

```python
def test_subtract():
    """Test basic subtraction"""
    # TODO: Write test for subtract(5, 3) -> 2
    pass

def test_subtract_negative_result():
    """Test subtraction that results in negative"""
    # TODO: Write test for subtract(3, 5) -> -2
    pass

def test_subtract_zero():
    """Test subtracting zero"""
    # TODO: Write test for subtract(5, 0) -> 5
    pass
```

### Step 2: Run Tests (They Should Fail)

```bash
uv run pytest
```

### Step 3: Implement the Function

Add the `subtract` function to `calculator.py` to make all tests pass.

---

## Part 4: Multiply Function (Your Turn!)

**Your Task**: Following TDD principles:

1. Write tests FIRST for a `multiply` function that:
   - Multiplies two positive numbers
   - Multiplies a positive and negative number
   - Multiplies by zero
   - Multiplies by one

2. Run tests and watch them fail

3. Implement the `multiply` function

4. Run tests again and watch them pass!

---

## Part 5: Challenge - Is Even Function

Create a function called `is_even(number)` that returns `True` if a number is even, `False` otherwise.

### Requirements:
- Write at least 4 test cases BEFORE implementing the function
- Test cases should include:
  - Even positive numbers
  - Odd positive numbers
  - Zero
  - Negative numbers

### Test Function Names:
```python
def test_is_even_positive_even():
    pass

def test_is_even_positive_odd():
    pass

def test_is_even_zero():
    pass

def test_is_even_negative():
    pass
```

---

## Verification Checklist

You will know you are finished when

- You have a `calculator.py` file with at least 4 functions
- You have a `test_calculator.py` file with at least 12 test functions
- All tests pass when you run `uv run pytest`
- You can run tests with verbose output: `uv run pytest -v`
- Each function has at least 3 test cases

---

## Running Your Tests

```bash
# Run all tests
uv run pytest

# Run with verbose output (shows each test)
uv run pytest -v

# Run only tests in a specific file
uv run pytest test_calculator.py

# Run a specific test function
uv run pytest test_calculator.py::test_add
```

---

## Expected Final File Structure

```
intro_pytest/
├── calculator.py          # Your implementation
├── test_calculator.py     # Your tests
└── pyproject.toml        # Created by uv
```

---

## Reflection Questions

After completing the exercise, answer these questions:

1. What is the advantage of writing tests before writing code?
2. How did pytest make it easy to verify your functions work correctly?
3. Why is it useful to test multiple scenarios for each function?
4. What happened when you ran tests before implementing the functions?

---

## Tips

- **Red-Green-Refactor**: Write a failing test (Red), make it pass (Green), improve the code (Refactor)
- **One test at a time**: Don't write all tests at once, write one, make it pass, then move to the next
- **Descriptive test names**: Test names should describe what they're testing
- **Simple assertions**: Each test should test one thing clearly

---

## Common Errors and Solutions

**Error**: `NameError: name 'add' is not defined`
- **Solution**: Make sure you import the function at the top of your test file

**Error**: `ModuleNotFoundError: No module named 'calculator'`
- **Solution**: Make sure `calculator.py` is in the same directory as `test_calculator.py`

**Error**: `AssertionError`
- **Solution**: Your function isn't returning the expected value. Check your implementation!

**Error**: `pytest: No tests ran` or `collected 0 items`
- **Solution**: Test discovery failed. Check that:
  - Your test file is named `test_*.py` or `*_test.py`
  - Your test functions start with `test_`
  - Your test file is in the directory where you're running `pytest`
  - If using a test class, the class name starts with `Test`

**Error**: `INTERNALERROR` or pytest crashes
- **Solution**: There might be a syntax error in your test file. Check for:
  - Missing colons (`:`) after function definitions
  - Incorrect indentation
  - Unclosed parentheses or quotes
  - Run `python test_calculator.py` to check for syntax errors