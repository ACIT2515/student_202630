# Introduction to Pytest and TDD - Solution

## Solution Files

### calculator.py

```python
# calculator.py
"""
Simple calculator functions for introduction to pytest and TDD.
"""

def add(a, b):
    """
    Add two numbers together.
    
    Args:
        a: First number
        b: Second number
    
    Returns:
        The sum of a and b
    """
    return a + b


def subtract(a, b):
    """
    Subtract b from a.
    
    Args:
        a: First number
        b: Second number
    
    Returns:
        The difference of a and b
    """
    return a - b


def multiply(a, b):
    """
    Multiply two numbers together.
    
    Args:
        a: First number
        b: Second number
    
    Returns:
        The product of a and b
    """
    return a * b


def is_even(number):
    """
    Check if a number is even.
    
    Args:
        number: Integer to check
    
    Returns:
        True if number is even, False otherwise
    """
    return number % 2 == 0
```

---

### test_calculator.py

```python
# test_calculator.py
"""
Tests for calculator functions.
Following TDD principles: Write tests first, then implement!
"""

from calculator import add, subtract, multiply, is_even


# Part 1: Basic Add Tests
def test_add():
    """Test that add function works correctly"""
    result = add(2, 3)
    assert result == 5


# Part 2: Multiple Test Cases for Add
def test_add_positive_numbers():
    """Test adding two positive numbers"""
    assert add(10, 5) == 15
    assert add(100, 200) == 300


def test_add_negative_numbers():
    """Test adding two negative numbers"""
    assert add(-5, -3) == -8
    assert add(-10, -10) == -20


def test_add_zero():
    """Test adding zero to a number"""
    assert add(5, 0) == 5
    assert add(0, 5) == 5
    assert add(0, 0) == 0


# Part 3: Subtract Function Tests
def test_subtract():
    """Test basic subtraction"""
    result = subtract(5, 3)
    assert result == 2


def test_subtract_negative_result():
    """Test subtraction that results in negative"""
    result = subtract(3, 5)
    assert result == -2


def test_subtract_zero():
    """Test subtracting zero"""
    result = subtract(5, 0)
    assert result == 5


# Part 4: Multiply Function Tests
def test_multiply_positive_numbers():
    """Test multiplying two positive numbers"""
    assert multiply(3, 4) == 12
    assert multiply(5, 5) == 25


def test_multiply_positive_and_negative():
    """Test multiplying positive and negative number"""
    assert multiply(5, -3) == -15
    assert multiply(-4, 6) == -24


def test_multiply_by_zero():
    """Test multiplying by zero"""
    assert multiply(5, 0) == 0
    assert multiply(0, 100) == 0


def test_multiply_by_one():
    """Test multiplying by one"""
    assert multiply(5, 1) == 5
    assert multiply(1, 7) == 7


# Part 5: Is Even Function Tests (Challenge)
def test_is_even_positive_even():
    """Test that positive even numbers return True"""
    assert is_even(2) == True
    assert is_even(4) == True
    assert is_even(100) == True


def test_is_even_positive_odd():
    """Test that positive odd numbers return False"""
    assert is_even(1) == False
    assert is_even(3) == False
    assert is_even(99) == False


def test_is_even_zero():
    """Test that zero is considered even"""
    assert is_even(0) == True


def test_is_even_negative():
    """Test that negative even numbers return True"""
    assert is_even(-2) == True
    assert is_even(-4) == True
    # Negative odd numbers return False
    assert is_even(-1) == False
    assert is_even(-3) == False
```

---

## Running the Solution

```bash
# Run all tests
uv run pytest

# Run with verbose output
uv run pytest -v

# Expected output:
# test_calculator.py::test_add PASSED
# test_calculator.py::test_add_positive_numbers PASSED
# test_calculator.py::test_add_negative_numbers PASSED
# test_calculator.py::test_add_zero PASSED
# test_calculator.py::test_subtract PASSED
# test_calculator.py::test_subtract_negative_result PASSED
# test_calculator.py::test_subtract_zero PASSED
# test_calculator.py::test_multiply_positive_numbers PASSED
# test_calculator.py::test_multiply_positive_and_negative PASSED
# test_calculator.py::test_multiply_by_zero PASSED
# test_calculator.py::test_multiply_by_one PASSED
# test_calculator.py::test_is_even_positive_even PASSED
# test_calculator.py::test_is_even_positive_odd PASSED
# test_calculator.py::test_is_even_zero PASSED
# test_calculator.py::test_is_even_negative PASSED
#
# ================ 15 passed in 0.02s ================
```

---

## Key Concepts Demonstrated

### 1. Test-Driven Development (TDD)
- Tests written BEFORE implementation
- Red-Green-Refactor cycle
- Tests guide the implementation

### 2. Pytest Basics
- Test files start with `test_`
- Test functions start with `test_`
- Use `assert` for verification
- Import functions to test them

### 3. Good Testing Practices
- **Multiple test cases**: Testing edge cases (zero, negatives, etc.)
- **Descriptive names**: Test names explain what they test
- **One assertion per concept**: Each test focuses on one scenario
- **Independence**: Each test can run alone

### 4. The AAA Pattern

Each test follows **Arrange-Act-Assert**:

```python
def test_add():
    # Arrange: Set up test data
    a = 2
    b = 3
    
    # Act: Call the function
    result = add(a, b)
    
    # Assert: Verify the result
    assert result == 5
```

---

## Common Student Mistakes and Fixes

### Mistake 1: Forgetting to Import

❌ **Wrong**:
```python
def test_add():
    result = add(2, 3)  # NameError!
```

✅ **Correct**:
```python
from calculator import add

def test_add():
    result = add(2, 3)
```

### Mistake 2: Not Using `assert`

❌ **Wrong**:
```python
def test_add():
    result = add(2, 3)
    result == 5  # This doesn't test anything!
```

✅ **Correct**:
```python
def test_add():
    result = add(2, 3)
    assert result == 5
```

### Mistake 3: Testing Too Much in One Test

❌ **Wrong**:
```python
def test_everything():
    assert add(2, 3) == 5
    assert subtract(5, 2) == 3
    assert multiply(2, 3) == 6
    # Too many unrelated things!
```

✅ **Correct**:
```python
def test_add():
    assert add(2, 3) == 5

def test_subtract():
    assert subtract(5, 2) == 3

def test_multiply():
    assert multiply(2, 3) == 6
```

---

## Extension Ideas

Once students complete the basic exercise:

1. **Add a `divide` function** with tests for:
   - Normal division
   - Division by zero (should raise an exception)
   - Integer vs float division

2. **Add a `power` function** for exponentiation

3. **Add a `is_prime` function** to check if a number is prime

4. **Create a `greet` function** that takes a name and returns a greeting

5. **Test string operations**: Create functions for string manipulation

---

## Reflection Questions - Answers

**1. What is the advantage of writing tests before writing code?**
- Forces you to think about requirements first
- Tests serve as specifications
- Ensures code actually does what it's supposed to do
- Catches bugs early

**2. How did pytest make it easy to verify your functions work correctly?**
- Simple `assert` statements
- Clear pass/fail output
- Easy to run all tests at once
- Descriptive error messages

**3. Why is it useful to test multiple scenarios for each function?**
- Edge cases might break even if normal cases work
- Ensures robustness
- Finds hidden bugs
- Documents expected behavior

**4. What happened when you ran tests before implementing the functions?**
- Tests failed (as expected in TDD)
- This is called "Red" in Red-Green-Refactor
- Confirms tests are actually checking the code
