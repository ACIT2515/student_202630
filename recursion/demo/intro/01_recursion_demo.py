import argparse


def countdown_recursive(count):
    """Recursive countdown function.

    Recursively counts down from a given number to zero, printing each number
    along the way. When zero is reached, prints "Liftoff!".

    Args:
        count: The current number in the countdown.

    Returns:
        None
    """
    if count <= 0:  # Base case
        print("Liftoff!")
        return
    print(f"  {count}...")
    countdown_recursive(count - 1)  # Recursive case


def countdown_looping(count):
    """Recursive countdown function.

    Counts down from a given number to zero, printing each number
    along the way. When zero is reached, prints "Liftoff!".

    Args:
        count: The current number in the countdown.

    Returns:
        None
    """

    while count > 0:
        print(f"  {count}...")
        count -= 1
    print(f"  {count}...")
    return


def demonstrate_recursion():
    """Demonstrate how recursion works with a simple countdown example.

    Parses command-line arguments and runs a recursive countdown demonstration.
    Displays the countdown and explains how the recursion works.

    Returns:
        None
    """
    parser = argparse.ArgumentParser(
        description="Demonstrate recursion with a countdown example."
    )

    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        "-r", "--recursive", action="store_true", help="Use recursive method (default)"
    )
    group.add_argument(
        "-i", "--iterative", action="store_true", help="Use iterative method"
    )

    parser.add_argument(
        "-c",
        "--count",
        type=int,
        default=5,
        help="Number to countdown from (default: 5)",
    )

    args = parser.parse_args()
    start_count = args.count
    print("=" * 60)

    if args.iterative:
        print("LOOPING DEMONSTRATION")
        print("=" * 60)
        print("\nSimple countdown using iteration (loop):\n")
        countdown_looping(start_count)
    else:
        # Default to recursive if neither or recursive is specified
        print("RECURSION DEMONSTRATION")
        print("=" * 60)
        print("\nSimple countdown using recursion:\n")
        countdown_recursive(start_count)
        print("  - Base case: Countdown final condition reached - ends recursion")
        print("  - Recursive case: Decrement Count and countdown again")

    print("\nNotice how each call waits for the next one to complete.")
    print("=" * 60)
    print()


if __name__ == "__main__":

    demonstrate_recursion()
