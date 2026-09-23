from letter_frequency import char_freq, histogram, letter_freq, parse_arguments


def test_parse_arguments_supports_sys_argv_style_flags():
    assert parse_arguments(["Hello world!", "--letters"]) == ("Hello world!", "letters")
    assert parse_arguments(["Hello world!", "-c"]) == ("Hello world!", "chars")
    assert parse_arguments(["Hello world!"]) == ("Hello world!", "histogram")


def test_char_freq_single_character_repeated():
    assert char_freq("aaaa") == {"a": 4}


def test_char_freq_mixed_case_and_punctuation():
    assert char_freq("Hello!") == {"H": 1, "e": 1, "l": 2, "o": 1, "!": 1}


def test_char_freq_empty_string():
    assert char_freq("") == {}


def test_char_freq_single_character():
    assert char_freq("a") == {"a": 1}


def test_char_freq_spaces_counted():
    result = char_freq("a b c")
    assert result[" "] == 2


def test_char_freq_special_characters():
    result = char_freq("a!b@c#")
    assert result["!"] == 1
    assert result["@"] == 1
    assert result["#"] == 1


def test_letter_freq_removes_punctuation_and_spaces():
    assert letter_freq("Hello world!") == {
        "h": 1,
        "e": 1,
        "l": 3,
        "o": 2,
        "w": 1,
        "r": 1,
        "d": 1,
    }


def test_letter_freq_case_insensitive():
    assert letter_freq("AaAa") == {"a": 4}


def test_letter_freq_empty_string():
    assert letter_freq("") == {}


def test_letter_freq_only_punctuation_and_spaces():
    assert letter_freq("!!! ???") == {}


def test_letter_freq_mixed_punctuation():
    result = letter_freq("Hello, World!")
    assert "h" in result
    assert "w" in result
    assert "," not in result
    assert "!" not in result
    assert " " not in result


def test_letter_freq_numbers_included():
    result = letter_freq("abc123")
    assert result == {"a": 1, "b": 1, "c": 1, "1": 1, "2": 1, "3": 1}


def test_histogram_simple():
    result = histogram("Haaaaah")
    assert "h **\n" in result
    assert "a *****\n" in result


def test_histogram_multiple_letters():
    result = histogram("Hello world!")
    lines = result.strip().split("\n")
    assert len(lines) == 7
    assert "h *" in result
    assert "l ***" in result


def test_histogram_empty_string():
    assert histogram("") == ""


def test_histogram_single_character():
    result = histogram("a")
    assert result.strip() == "a *"


def test_histogram_output_format():
    result = histogram("aab")
    assert "a **\n" in result
    assert "b *\n" in result


def test_histogram_case_insensitive():
    result = histogram("AaA")
    assert "a ***" in result
    assert "A" not in result
