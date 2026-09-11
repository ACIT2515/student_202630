# Introduction to Pytest Fixtures

## Learning Objectives

By the end of this exercise, you will be able to:
- Understand what fixtures are and why they're useful
- Create basic fixtures using `@pytest.fixture`
- Use fixtures in test functions
- Eliminate duplicate setup code in tests
- Use built-in fixtures like `tmp_path`

---

## Setup

1. Create a new folder for this exercise: `intro_fixtures`
2. Using `uv` create a virtual environment
3. Install pytest: `uv add --dev pytest`

---

## The Problem: Repetitive Setup Code

### Step 1: See the Problem

Create a file called `text_processor.py`:

```python
# text_processor.py

def count_words(text):
    """Count the number of words in text"""
    return len(text.split())

def capitalize_words(text):
    """Capitalize the first letter of each word"""
    return text.title()

def reverse_text(text):
    """Reverse the text"""
    return text[::-1]
```

Now create `test_text_processor.py` with repetitive setup:

```python
# test_text_processor.py
from text_processor import count_words, capitalize_words, reverse_text

def test_count_words():
    # Setup - repeated in every test!
    sample_text = "the quick brown fox"
    
    result = count_words(sample_text)
    assert result == 4

def test_capitalize_words():
    # Same setup repeated!
    sample_text = "the quick brown fox"
    
    result = capitalize_words(sample_text)
    assert result == "The Quick Brown Fox"

def test_reverse_text():
    # Same setup again!
    sample_text = "the quick brown fox"
    
    result = reverse_text(sample_text)
    assert result == "xof nworb kciuq eht"
```

**Run the tests**: `uv run pytest -v`

Notice how we repeat `sample_text = "the quick brown fox"` in every test? **Fixtures solve this!**

---

## Part 1: Your First Fixture

### Step 2: Create a Fixture

Update `test_text_processor.py` to use a fixture:

```python
# test_text_processor.py
import pytest
from text_processor import count_words, capitalize_words, reverse_text

@pytest.fixture
def sample_text():
    """Provide sample text for tests"""
    # TODO: Return the text "the quick brown fox"
    pass

def test_count_words(sample_text):
    # TODO: Use the sample_text fixture parameter
    # Assert that count_words returns 4
    pass

def test_capitalize_words(sample_text):
    # TODO: Use the sample_text fixture parameter
    # Assert that capitalize_words returns "The Quick Brown Fox"
    pass

def test_reverse_text(sample_text):
    # TODO: Use the sample_text fixture parameter
    # Assert that reverse_text returns "xof nworb kciuq eht"
    pass
```

**Your Task**:
1. Implement the `sample_text` fixture to return `"the quick brown fox"`
2. Complete each test function to use the `sample_text` parameter
3. Run tests and verify they all pass

---

## Part 2: Multiple Fixtures

### Step 3: Add More Fixtures

Add these new functions to `text_processor.py`:

```python
def get_word_count(text):
    """Get a dictionary with word frequency counts"""
    words = text.lower().split()
    word_count = {}
    for word in words:
        word_count[word] = word_count.get(word, 0) + 1
    return word_count

def contains_word(text, word):
    """Check if text contains a specific word (case-insensitive)"""
    return word.lower() in text.lower()
```

Now add fixtures for test data in `test_text_processor.py`:

```python
@pytest.fixture
def paragraph():
    """Provide a longer paragraph for testing"""
    # TODO: Return "Python is great. Python is powerful. Python is fun."
    pass

@pytest.fixture
def search_word():
    """Provide a word to search for"""
    # TODO: Return "python"
    pass

def test_get_word_count(paragraph):
    # TODO: Test that get_word_count returns {'python': 3, 'is': 3, 'great.': 1, 'powerful.': 1, 'fun.': 1}
    pass

def test_contains_word(paragraph, search_word):
    # TODO: Test that contains_word(paragraph, search_word) returns True
    pass
```

**Your Task**: Complete the fixtures and tests

---

## Part 3: Fixtures Returning Collections

### Step 4: List Fixture

Add this function to `text_processor.py`:

```python
def find_longest_word(words):
    """Find the longest word in a list"""
    return max(words, key=len)

def filter_short_words(words, min_length):
    """Filter out words shorter than min_length"""
    result = []
    for word in words:
        if len(word) >= min_length:
            result.append(word)
    return result
```

Create a fixture that returns a list:

```python
@pytest.fixture
def word_list():
    """Provide a list of words for testing"""
    # TODO: Return a list: ["cat", "elephant", "dog", "butterfly", "ant"]
    pass

def test_find_longest_word(word_list):
    # TODO: Test that find_longest_word returns "butterfly"
    pass

def test_filter_short_words(word_list):
    # TODO: Test that filter_short_words(word_list, 4) returns ["elephant", "butterfly"]
    pass
```

**Your Task**: Implement the fixture and tests

---

## Part 4: Built-in Fixture - `tmp_path`

Pytest provides useful built-in fixtures. Let's use `tmp_path` for file operations.

### Step 5: Using `tmp_path`

Add this function to `text_processor.py`:

```python
def save_text_to_file(text, filepath):
    """Save text to a file"""
    with open(filepath, 'w') as f:
        f.write(text)

def read_text_from_file(filepath):
    """Read text from a file"""
    with open(filepath, 'r') as f:
        return f.read()
```

Now write tests using `tmp_path`:

```python
def test_save_text_to_file(tmp_path):
    """Test saving text to a file"""
    # tmp_path is a built-in fixture that provides a temporary directory
    
    # TODO: Create a file path: tmp_path / "test.txt"
    # TODO: Save "Hello, World!" to that file using save_text_to_file
    # TODO: Read the file directly and assert it contains "Hello, World!"
    pass

def test_read_text_from_file(tmp_path):
    """Test reading text from a file"""
    # TODO: Create a file path: tmp_path / "input.txt"
    # TODO: Write "Test content" to the file (use file_path.write_text())
    # TODO: Use read_text_from_file to read it
    # TODO: Assert the result is "Test content"
    pass
```

**Your Task**: Complete both tests using the `tmp_path` fixture

**Hint**: 
```python
file_path = tmp_path / "filename.txt"  # Create a path
file_path.write_text("content")         # Write to file
content = file_path.read_text()         # Read from file
```

---

## Part 5: Fixture Using Another Fixture

Fixtures can use other fixtures!

### Step 6: Composed Fixtures

```python
@pytest.fixture
def greeting():
    """Provide a greeting"""
    # TODO: Return "Hello"
    pass

@pytest.fixture
def name():
    """Provide a name"""
    # TODO: Return "Alice"
    pass

@pytest.fixture
def full_greeting(greeting, name):
    """Combine greeting and name"""
    # TODO: Return f"{greeting}, {name}!"
    # Example: "Hello, Alice!"
    pass

def test_full_greeting(full_greeting):
    # TODO: Assert full_greeting equals "Hello, Alice!"
    pass
```

**Your Task**: Implement all three fixtures and the test

---

## Part 6: Challenge - Text Analysis

Create fixtures to test a text analysis system.

### Step 7: Text Analysis Functions

Add to `text_processor.py`:

```python
def count_sentences(text):
    """Count the number of sentences (separated by periods)"""
    sentences = text.split('.')
    count = 0
    for sentence in sentences:
        if sentence.strip():
            count += 1
    return count

def get_average_word_length(text):
    """Calculate average word length in text"""
    words = text.split()
    if not words:
        return 0
    total_length = 0
    for word in words:
        total_length += len(word)
    return total_length / len(words)

def remove_punctuation(text):
    """Remove common punctuation from text"""
    punctuation = '.,!?;:'
    for char in punctuation:
        text = text.replace(char, '')
    return text
```

Create fixtures and tests:

```python
@pytest.fixture
def essay():
    """Provide a multi-sentence essay"""
    # TODO: Return "The cat sat. The dog ran. The bird flew."
    pass

@pytest.fixture
def simple_sentence():
    """Provide a simple sentence with punctuation"""
    # TODO: Return "Hello, world! How are you?"
    pass

@pytest.fixture
def cleaned_text():
    """Provide text without punctuation"""
    # TODO: Return "Hello world How are you"
    pass

def test_count_sentences(essay):
    # TODO: Test that count_sentences returns 3
    pass

def test_get_average_word_length(essay):
    # TODO: Test that average word length is approximately 3.0
    # Hint: Words are ["The", "cat", "sat", "The", "dog", "ran", "The", "bird", "flew"]
    # Average = (3+3+3+3+3+3+3+4+4) / 9 = 29/9 ≈ 3.22
    pass

def test_remove_punctuation(simple_sentence, cleaned_text):
    # TODO: Test that remove_punctuation(simple_sentence) returns cleaned_text
    pass
```

**Your Task**: Implement all fixtures and tests

---

## Verification Checklist

You will know you are finished when:

- You have at least 7 fixtures defined
- You have at least 11 test functions
- All tests use fixtures (no hardcoded setup in test functions)
- You've used the `tmp_path` built-in fixture
- You've created a fixture that uses other fixtures
- All tests pass: `uv run pytest -v`

---

## Running Your Tests

```bash
# Run all tests
uv run pytest

# Run with verbose output
uv run pytest -v

# See fixture setup/teardown
uv run pytest --setup-show

# Run specific test file
uv run pytest test_text_processor.py
```

---

## Expected File Structure

```
intro_fixtures/
├── text_processor.py      # Your functions
├── test_text_processor.py # Your tests with fixtures
└── pyproject.toml        # Created by uv
```

---

## Reflection Questions

After completing the exercise, answer these questions:

1. How do fixtures reduce code duplication in tests?
2. What happens when you use a fixture name as a parameter in a test function?
3. Why is `tmp_path` useful for testing file operations?
4. How can fixtures use other fixtures?

---

## Tips

- **Fixture names**: Use descriptive names that explain what data they provide
- **Return values**: Fixtures must return the data you want to use in tests
- **Parameters**: Use the fixture name as a parameter in test functions
- **Built-in fixtures**: Explore `tmp_path`, `capsys`, and others with `pytest --fixtures`

---

## Common Errors and Solutions

**Error**: `fixture 'sample_text' not found`
- **Solution**: Make sure you decorated the fixture function with `@pytest.fixture`

**Error**: Fixture returns `None`
- **Solution**: Make sure your fixture has a `return` statement

**Error**: `TypeError: ... takes 0 positional arguments but 1 was given`
- **Solution**: You're using a fixture name as a parameter but haven't defined the fixture

**Error**: Tests pass but you still see repeated setup code
- **Solution**: You might not be using the fixture! Make sure to add it as a parameter to your test functions

---

## Submission

Clone the wk04lab01 github classroom repository.

Place your `text_processor.py` and `test_text_processor.py` files into the repository, commit, and push your changes to `origin`.
You can run the `pytest_scorer.py` to check if you solution is complete.