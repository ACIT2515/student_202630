"""
Demonstration of Recursion vs Iteration with Nested Lists
This example sums all numbers in a nested list of arbitrary depth.
"""


def sum_nested_recursive(data):
    """
    Recursively sum all numbers in a nested list.

    Args:
        data: A number or a list containing numbers and/or nested lists

    Returns:
        The sum of all numbers found
    """
    # Base case: if it's a number, return it
    if isinstance(data, (int, float)):
        return data

    # Recursive case: if it's a list, sum all elements
    total = 0
    for item in data:
        total += sum_nested_recursive(item)  # Recursive call
    return total


def sum_nested_iterative(data):
    """
    Iteratively sum all numbers in a nested list using a stack.

    Args:
        data: A number or a list containing numbers and/or nested lists

    Returns:
        The sum of all numbers found
    """
    total = 0
    stack = [data]  # Use a list as a stack

    while stack:
        current = stack.pop()

        if isinstance(current, (int, float)):
            total += current
        else:  # It's a list
            # Add all items to the stack
            for item in current:
                stack.append(item)

    return total


def main():
    # Example nested lists
    examples = [
        [1, 2, 3],
        [1, [2, 3], 4],
        [1, [2, [3, [4, 5]]], 6],
        [[1, 2], [3, 4], [5, 6]],
        [10, [20, [30, [40, 50]], 60], 70],
    ]

    print("Summing Nested Lists: Recursion vs Iteration\n")
    print("=" * 60)

    for i, example in enumerate(examples, 1):
        print(f"\nExample {i}: {example}")

        recursive_result = sum_nested_recursive(example)
        iterative_result = sum_nested_iterative(example)

        print(f"  Recursive sum: {recursive_result}")
        print(f"  Iterative sum: {iterative_result}")
        print(
            f"  Match: {recursive_result == iterative_result}"
            if recursive_result == iterative_result
            else "  Match: False "
        )

    print("\n" + "=" * 60)
    print("\nKey Insights:")
    print("Recursive solution is more intuitive and mirrors the problem structure")
    print("Iterative solution uses a stack to manually track what to process")
    print("Recursion uses the call stack; iteration uses an explicit stack")


if __name__ == "__main__":
    main()
