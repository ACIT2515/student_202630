# Introduction to Pytest Fixtures - Solution

## Common Mistakes and Fixes

### Mistake 1: Forgetting `@pytest.fixture` Decorator

**Wrong**:
```python
def sample_text():  # Missing decorator!
    return "test"
```

**Correct**:
```python
@pytest.fixture
def sample_text():
    return "test"
```

### Mistake 2: Not Returning a Value

**Wrong**:
```python
@pytest.fixture
def sample_text():
    "test"  # No return statement!
```

**Correct**:
```python
@pytest.fixture
def sample_text():
    return "test"
```

### Mistake 3: Calling Fixture Like a Function

**Wrong**:
```python
def test_something():
    text = sample_text()  # Don't call it!
```

**Correct**:
```python
def test_something(sample_text):  # Use as parameter
    assert len(sample_text) > 0
```

---

## Reflection Questions - Answers

**1. How do fixtures reduce code duplication in tests?**
- Setup code is written once in the fixture
- Multiple tests can use the same fixture
- Changes to test data only need to be made in one place

**2. What happens when you use a fixture name as a parameter in a test function?**
- Pytest automatically calls the fixture function
- The fixture's return value is passed to your test
- This happens before your test runs

**3. Why is `tmp_path` useful for testing file operations?**
- Provides a clean temporary directory for each test
- Automatically cleaned up after test completes
- Prevents tests from interfering with each other
- No need to manually create/delete test files

**4. How can fixtures use other fixtures?**
- Add other fixture names as parameters to your fixture function
- Pytest resolves the dependency chain automatically
- Enables building complex test data from simple components

---
