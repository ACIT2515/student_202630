import string

import pytest

from text_processor import (
    capitalize_words,
    count_sentences,
    count_words,
    filter_short_words,
    find_longest_word,
    get_average_word_length,
    read_text_from_file,
    remove_punctuation,
    reverse_text,
    save_text_to_file,
)


@pytest.fixture
def sample_text():
    """Provide sample text for tests"""
    return "the quick brown fox"


@pytest.fixture
def word_list():
    """Provide a list of words for testing"""
    return ["cat", "elephant", "dog", "butterfly", "ant"]


@pytest.fixture
def greeting():
    """Provide a greeting"""
    return "Hello"


@pytest.fixture
def name():
    """Provide a name"""
    return "Alice"


@pytest.fixture
def full_greeting(greeting, name):
    """Combine greeting and name"""
    return f"{greeting}, {name}!"


@pytest.fixture
def essay():
    """Provide a multi-sentence essay"""
    return "The cat sat. The dog ran. The bird flew."


@pytest.fixture
def simple_sentence():
    """Provide a simple sentence with punctuation"""
    return "Hello, world! How are you?"


@pytest.fixture
def cleaned_text(simple_sentence):
    """Provide text without punctuation"""

    # make a translation table that maps punctuation characters to None
    # maketrans accepts:
    #   - list of from chars, empty in this case - will match nothing
    #   - list of to chars, empty in this case
    #   - string containing all characters that map to None - all punctuation.
    translation_dict = str.maketrans("", "", string.punctuation)

    return simple_sentence.translate(translation_dict)


def test_count_words(sample_text):
    result = count_words(sample_text)
    assert result == 4


def test_capitalize_words(sample_text):
    result = capitalize_words(sample_text)
    assert result == "The Quick Brown Fox"


def test_reverse_text(sample_text):
    result = reverse_text(sample_text)
    assert result == "xof nworb kciuq eht"


def test_find_longest_word(word_list):
    lw = find_longest_word(word_list)
    assert lw == "butterfly"


def test_filter_short_words(word_list):
    assert filter_short_words(word_list, 4) == ["elephant", "butterfly"]


def test_save_text_to_file(tmp_path):
    """Test saving text to a file"""
    # tmp_path is a built-in fixture that provides a temporary directory
    test_str = "Hello, World!"
    # TODO: Create a file path: tmp_path / "test.txt"
    test_file_path = tmp_path / "test.txt"

    # TODO: Save "Hello, World!" to that file using save_text_to_file
    save_text_to_file(test_str, test_file_path)

    # TODO: Read the file directly and assert it contains "Hello, World!"
    with open(test_file_path) as test_file:
        assert test_file.read() == test_str


def test_read_text_from_file(tmp_path):
    """Test reading text from a file"""
    # TODO: Create a file path: tmp_path / "input.txt"
    # TODO: Write "Test content" to the file (use file_path.write_text())
    input_content = "Test content"
    input_file_path = tmp_path / "input.txt"
    with open(input_file_path, "w") as input_file:
        input_file.write(input_content)

    # TODO: Use read_text_from_file to read it
    # TODO: Assert the result is "Test content"
    with open(input_file_path, "r") as input_file:
        assert read_text_from_file(input_file_path) == input_content


def test_full_greeting(full_greeting):
    assert full_greeting == "Hello, Alice!"


def test_count_sentences(essay):
    assert count_sentences(essay) == 3


def test_get_average_word_length(essay):
    # TODO: Test that average word length is approximately 3.0
    # Hint: Words are ["The", "cat", "sat", "The", "dog", "ran", "The", "bird", "flew"]
    # Average = (3+3+3+3+3+3+3+4+4) / 9 = 29/9 ≈ 3.22
    assert get_average_word_length(essay) == pytest.approx(3, abs=0.5)


def test_remove_punctuation(simple_sentence, cleaned_text):
    assert remove_punctuation(simple_sentence) == cleaned_text
