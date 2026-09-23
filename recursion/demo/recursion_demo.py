import sys


def parse_arguments(arguments: list[str]) -> tuple[str, int]:
    """Parse CLI input for the recursion demo.

    Usage:
        python recursion_demo.py
        python recursion_demo.py -i -c 3
        python recursion_demo.py --count 2
        python recursion_demo.py --iterative --count 3

    Args:
        arguments: The raw command-line arguments after the script name.

    Returns:
        A tuple containing the selected mode and the countdown start value.
    """
    mode = "recursive"
    count = 5
    index = 0

    while index < len(arguments):
        arg = arguments[index]

        if arg in {"-r", "--recursive"}:
            mode = "recursive"
        elif arg in {"-i", "--iterative"}:
            mode = "iterative"
        elif arg in {"-c", "--count"}:
            if index + 1 >= len(arguments):
                raise SystemExit(
                    "Usage: python 01_recursion_demo.py [-r | --recursive | -i | --iterative] [-c N]"
                )
            try:
                count = int(arguments[index + 1])
            except ValueError as exc:
                raise SystemExit(
                    f"Count must be an integer: {arguments[index + 1]}"
                ) from exc
            index += 1
        elif arg in {"-h", "--help"}:
            print(
                "Usage: python 01_recursion_demo.py [-r | --recursive | -i | --iterative] [-c N]"
            )
            raise SystemExit(0)
        else:
            raise SystemExit(f"Unknown option: {arg}")

        index += 1

    return mode, count


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


def main():
    """Demonstrate recursion and iteration with a countdown example.

    Usage:
        python recursion_demo.py
        python recursion_demo.py -i -c 3
        python recursion_demo.py --count 2

    The program reads mode and count values from sys.argv and then shows either
    a recursive countdown or an iterative countdown.

    Returns:
        None
    """
    try:
        mode, start_count = parse_arguments(sys.argv[1:])
    except SystemExit:
        raise

    print("=" * 60)

    if mode == "iterative":
        print("LOOPING DEMONSTRATION")
        print("=" * 60)
        print("\nSimple countdown using iteration (loop):\n")
        countdown_looping(start_count)
    else:
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

    main()
