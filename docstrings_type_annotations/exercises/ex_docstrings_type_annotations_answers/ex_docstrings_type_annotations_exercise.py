def calculate_tip_amount(bill_total: float, tip_percent: float) -> float:
    """Calculate the tip amount for a given bill and tip percentage.

    Args:
        bill_total: The total bill amount, before tip.
        tip_percent: The tip percentage (e.g., 20 for 20%).

    Returns:
        The calculated tip amount.

    Examples:
        >>> calculate_tip_amount(50, 20)
        10.0
    """
    return bill_total * tip_percent / 100


def is_even(number: int) -> bool:
    """Return True if number is even, False otherwise.

    Args:
        number: The integer to check.

    Returns:
        True if number is even, False otherwise.

    Examples:
        >>> is_even(4)
        True
        >>> is_even(7)
        False
    """
    return number % 2 == 0


def average_score(scores: list[float]) -> float:
    """Return the arithmetic average of a non-empty list of scores.

    Args:
        scores: A non-empty list of numeric scores.

    Returns:
        The arithmetic average of scores.

    Examples:
        >>> average_score([80.0, 90.0, 100.0])
        90.0
    """
    return sum(scores) / len(scores)


def find_max_score(scores: list[float]) -> float | None:
    """Return the largest score in the list, or None if the list is empty.

    Args:
        scores: A list of numeric scores, which may be empty.

    Returns:
        The largest score in scores, or None if scores is empty.

    Examples:
        >>> find_max_score([55.0, 92.5, 78.0])
        92.5
        >>> print(find_max_score([]))
        None
    """
    if not scores:
        return None
    return max(scores)


def celsius_to_fahrenheit(celsius: float) -> float:
    """Convert a Celsius temperature to Fahrenheit.

    Args:
        celsius (float): The temperature in degrees Celsius.

    Returns:
        float: The temperature in degrees Fahrenheit.
    """
    return celsius * 9 / 5 + 32


def count_vowels(text: str) -> int:
    """Count the number of vowels (a, e, i, o, u) in a string, ignoring case.

    Args:
        text (str): The text to search.

    Returns:
        int: The number of vowels found.
    """
    count = 0
    for letter in text.lower():
        if letter in "aeiou":
            count += 1
    return count


def summarize_grades(names: list[str], grades: list[int]) -> dict[str, int]:
    """Combine parallel lists of names and grades into a dictionary.

    Args:
        names (list[str]): Student names, in order.
        grades (list[int]): Grades, in the same order as names.

    Returns:
        dict[str, int]: A mapping of each name to their grade.
    """
    return dict(zip(names, grades))


def get_student_record(student_id: str, records: dict[str, str]) -> str | None:
    """Look up a student's name using their student ID.

    Args:
        student_id (str): The ID to look up.
        records (dict[str, str]): A mapping of student ID to student name.

    Returns:
        str | None: The student's name, or None if the ID is not found.
    """
    return records.get(student_id)


def main():
    """Demonstrate every function implemented for this exercise."""
    print(f"Tip on $50 at 20%: {calculate_tip_amount(50, 20)}")
    print(f"Is 4 even? {is_even(4)}")
    print(f"Average of [80.0, 90.0, 100.0]: {average_score([80.0, 90.0, 100.0])}")
    print(f"Max of [55.0, 92.5, 78.0]: {find_max_score([55.0, 92.5, 78.0])}")
    print(f"0 Celsius in Fahrenheit: {celsius_to_fahrenheit(0)}")
    print(f"Vowels in 'Hello World': {count_vowels('Hello World')}")


if __name__ == "__main__":
    main()
