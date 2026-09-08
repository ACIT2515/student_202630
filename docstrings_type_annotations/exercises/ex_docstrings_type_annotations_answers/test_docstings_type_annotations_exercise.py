from ex_docstrings_type_annotations_exercise import (
    average_score,
    calculate_tip_amount,
    celsius_to_fahrenheit,
    count_vowels,
    find_max_score,
    is_even,
)


def test_calculate_tip_amount():
    assert calculate_tip_amount(50, 20) == 10.0


def test_is_even_true():
    assert is_even(4) is True


def test_is_even_false():
    assert is_even(7) is False


def test_average_score():
    assert average_score([80.0, 90.0, 100.0]) == 90.0


def test_find_max_score():
    assert find_max_score([55.0, 92.5, 78.0]) == 92.5


def test_find_max_score_empty_list():
    assert find_max_score([]) is None


def test_celsius_to_fahrenheit_freezing():
    assert celsius_to_fahrenheit(0) == 32


def test_celsius_to_fahrenheit_boiling():
    assert celsius_to_fahrenheit(100) == 212


def test_count_vowels():
    assert count_vowels("Hello World") == 3


def test_count_vowels_no_vowels():
    assert count_vowels("xyz") == 0
