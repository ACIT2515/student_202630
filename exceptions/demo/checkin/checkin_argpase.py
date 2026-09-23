#! /usr/bin/env python3
"""Simple mood check-in application for tracking your location and mood.

This program helps you keep track of where you are and how you're feeling
throughout the day. It saves your check-ins to a CSV file so you can look
back at them later.

How to use:
    python checkin.py work happy
    python checkin.py home relaxed
    python checkin.py --location "coffee shop" --mood productive

The program will tell you how long it's been since your last check-in
and how your location and mood have changed.
"""

import argparse
import csv
import datetime
import sys

CHECKIN_FILE = "checkins.csv"


def parse_arguments():
    """Parse and validate command-line arguments.

    This function uses argparse to handle the location and mood inputs
    from the command line. It provides helpful error messages if the
    user forgets to include required information.

    Returns:
        argparse.Namespace: An object containing the parsed arguments
            with 'location' and 'mood' attributes.

    Demo Usage:
        >>> # Command: python checkin.py office focused
        >>> args = parse_arguments()
        >>> print(args.location, args.mood)
        office focused

        >>> # Command: python checkin.py home relaxed
        >>> args = parse_arguments()
        >>> print(args.location, args.mood)
        home relaxed
    """
    # Create the argument parser with a helpful description
    parser = argparse.ArgumentParser(
        description="Check in with your current location and mood.",
        epilog="Example: python checkin.py work happy",
    )

    # Add the location argument (required)
    parser.add_argument(
        "location", type=str, help="Your current location (e.g., home, work, gym)"
    )

    # Add the mood argument (required)
    parser.add_argument(
        "mood", type=str, help="Your current mood (e.g., happy, tired, excited)"
    )

    # Parse and return the arguments
    return parser.parse_args()


def last_checkin() -> tuple[datetime.datetime, str, str]:
    """Get the most recent check-in from the file.

    This function reads the checkins.csv file and finds your last
    check-in entry. If the file doesn't exist yet, it creates a
    first entry for you automatically.

    Returns:
        A tuple with three pieces of information:
        - datetime: When you last checked in
        - str: Where you were (location)
        - str: How you felt (mood)

    Demo Usage:
        >>> # After running: python checkin.py office focused
        >>> prev_time, prev_loc, prev_mood = last_checkin()
        >>> print(f"Last at {prev_loc} feeling {prev_mood}")
        Last at office feeling focused

        >>> # If checkins.csv doesn't exist, creates initial entry
        >>> last_checkin()  # Returns initial values automatically
        (datetime(...), 'initial location', 'initial mood')
    """
    try:
        with open(CHECKIN_FILE, "r") as checkins:
            checkin_reader = csv.DictReader(checkins)
            last_checkin_row = None
            for row in checkin_reader:
                last_checkin_row = row

            if last_checkin_row is None:
                raise IndexError("checkin file contains no entries")

            return (
                datetime.datetime.fromisoformat(last_checkin_row["date_time"]),
                last_checkin_row["location"],
                last_checkin_row["mood"],
            )

    except IndexError as error:
        print(f"Corrupt checkin file:{CHECKIN_FILE}  {error}")
        sys.exit(1)

    except FileNotFoundError:
        now = datetime.datetime.now()
        checkin("initial location", "initial mood", dtime=now)
        return now, "initial location", "initial mood"


def checkin(
    location: str, mood: str, dtime: datetime.datetime | None = None
) -> datetime.datetime:
    """Save a new check-in with your current location and mood.

    This function adds a new row to the checkins.csv file with your
    information. If the file doesn't exist yet, it creates it and
    adds column headers first.

    Args:
        location: Where you are right now (e.g., "home", "work", "gym")
        mood: How you're feeling (e.g., "happy", "tired", "excited")
        dtime: The time of check-in. If you don't provide this,
            it will use the current time automatically.

    Returns:
        The datetime when the check-in was recorded.

    Demo Usage:
        >>> # Simple check-in (uses current time)
        >>> checkin("coffee shop", "productive")
        datetime.datetime(2026, 2, 10, 14, 30, 15)

        >>> # Check-in with specific time
        >>> specific_time = datetime.datetime(2026, 2, 10, 9, 0, 0)
        >>> checkin("office", "energized", dtime=specific_time)
        datetime.datetime(2026, 2, 10, 9, 0, 0)

        >>> # Creates checkins.csv if it doesn't exist
        >>> checkin("home", "relaxed")  # First run creates file with headers

    Note:
        The function uses exception handling to check if the file exists.
        If the file is missing, it creates a new one with headers.
    """
    if dtime is None:
        dtime = datetime.datetime.now()

    try:
        # Try to open and read the file to check if it exists and has content
        with open(CHECKIN_FILE, "r") as chk_file:
            # File exists, append to it
            pass

        with open(CHECKIN_FILE, "a", newline="") as chk_file:
            writer = csv.writer(chk_file)
            writer.writerow([dtime.isoformat(timespec="seconds"), location, mood])

    except FileNotFoundError:
        # File doesn't exist - create it with headers
        with open(CHECKIN_FILE, "w", newline="") as chk_file:
            writer = csv.writer(chk_file)
            writer.writerow(["date_time", "location", "mood"])
            writer.writerow([dtime.isoformat(timespec="seconds"), location, mood])

    except OSError as error:
        # Handle other file-related errors
        print("File writing error: {}".format(error))
        sys.exit(1)

    return dtime


def timedelta_to_words(time_diff: datetime.timedelta) -> str:
    """Convert a time difference into easy-to-read words.

    Python's timedelta objects are hard to read (like "0:14:32.5").
    This function converts them into friendly text like "14 minutes 32 seconds".

    Args:
        time_diff: A timedelta object representing the time between
            two check-ins.

    Returns:
        A human-readable string describing the time difference.

    Demo Usage:
        >>> # Convert 2 hours and 30 minutes
        >>> delta = datetime.timedelta(hours=2, minutes=30)
        >>> timedelta_to_words(delta)
        '2 hours 30 minutes '

        >>> # Convert 3 days, 5 hours, 15 minutes, 42 seconds
        >>> delta = datetime.timedelta(days=3, hours=5, minutes=15, seconds=42)
        >>> timedelta_to_words(delta)
        '3 days 5 hours 15 minutes 42 seconds'

        >>> # Just minutes and seconds
        >>> delta = datetime.timedelta(minutes=14, seconds=32)
        >>> timedelta_to_words(delta)
        '14 minutes 32 seconds'
    """
    time_diff_words = ""

    if time_diff.days > 0:
        time_diff_words += "{} days ".format(time_diff.days)

    hours = time_diff.seconds // 36000
    if hours > 0:
        time_diff_words += "{} hours ".format(hours)

    minutes = time_diff.seconds // 60 % 60
    if minutes > 0:
        time_diff_words += "{} minutes ".format(minutes)

    seconds = time_diff.seconds % 60
    if seconds > 0:
        time_diff_words += "{} seconds".format(seconds)

    return time_diff_words


def main():
    """Run the mood check-in application.

    This is the main function that runs when you start the program.
    It does the following:
    1. Gets your location and mood from the command line using argparse
    2. Reads your previous check-in
    3. Saves your new check-in
    4. Tells you how much time passed and what changed

    The function uses argparse for better argument handling with
    automatic help messages and error checking.

    Demo Usage:
        Command: python checkin.py office focused
        Output:
            It has been 2 hours 15 minutes since your last checkin
            You have moved from home to office
            Your mood has gone from sleepy to focused

        Command: uv run checkin.py home relaxed
        Output:
            It has been 8 hours 30 minutes since your last checkin
            You have moved from office to home
            Your mood has gone from focused to relaxed

        Command: python checkin.py gym energized
        Output:
            It has been 45 minutes since your last checkin
            You have moved from home to gym
            Your mood has gone from relaxed to energized
    """
    # Parse command-line arguments
    args = parse_arguments()
    location = args.location
    mood = args.mood

    # Get previous check-in data
    prev_chkin, prev_location, prev_mood = last_checkin()

    # Save current check-in
    cur_chkin = checkin(location, mood)

    # Calculate and display the time difference
    checkin_gap = cur_chkin - prev_chkin
    gap_string = timedelta_to_words(checkin_gap)

    print(f"It has been {gap_string} since your last checkin")
    print("You have moved from {prev_location} to {location}")
    print("Your mood has gone from {prev_mood} to {mood}")


if __name__ == "__main__":
    main()
