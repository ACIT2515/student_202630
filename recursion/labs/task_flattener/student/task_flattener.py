"""
Task Flattener - Recursively flatten nested task structures.

This program demonstrates recursion by flattening a hierarchical task structure
into a simple list of all tasks (removing the parent-child relationships).

The recursive function processes nested tasks and subtasks, creating a flat list
where each task appears as a single entry regardless of its nesting level.
"""

import csv
import json
import sys
from typing import Any, Dict, List


def parse_arguments(arguments: list[str]) -> tuple[str, str]:
    """Parse the JSON input file and CSV output file from sys.argv."""
    if not arguments:
        raise SystemExit(
            "Usage: python task_flattener.py <input_file.json> [output_file.csv]"
        )

    input_file = arguments[0]
    output_file = "flattened_tasks.csv"

    if len(arguments) > 2:
        raise SystemExit(
            "Usage: python task_flattener.py <input_file.json> [output_file.csv]"
        )

    if len(arguments) == 2:
        output_file = arguments[1]

    return input_file, output_file


def flatten_tasks(tasks: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Recursively flatten a nested task structure into a flat list.

    Implement the recursive logic that:
    - processes each task in the list
    - removes the nested ``sub_tasks`` structure from each task
    - recursively visits every subtask
    - returns a single flat list of task dictionaries

    Example:
        Input:
        [
            {
                "details": "Parent",
                "status": "In Progress",
                "sub_tasks": [
                    {"details": "Child", "status": "Done", "sub_tasks": []}
                ]
            }
        ]

        Output:
        [
            {"details": "Parent", "status": "In Progress"},
            {"details": "Child", "status": "Done"}
        ]
    """
    # TODO: implement the recursive flattening logic.
    return []


def read_tasks_from_json(filename: str) -> List[Dict[str, Any]]:
    """
    Read tasks from a JSON file.

    Args:
        filename: Path to JSON file containing task data

    Returns:
        List of task dictionaries

    Raises:
        FileNotFoundError: If the file doesn't exist
        json.JSONDecodeError: If the file contains invalid JSON
    """
    try:
        with open(filename, "r", encoding="utf-8") as f:
            tasks = json.load(f)
        return tasks
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
        raise
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON in file '{filename}': {e}")
        raise


def save_tasks_to_csv(tasks: List[Dict[str, Any]], filename: str) -> None:
    """
    Save a flat list of tasks to a CSV file.

    Args:
        tasks: Flat list of task dictionaries
        filename: Output CSV filename

    Raises:
        ValueError: If tasks list is empty
    """
    if not tasks:
        raise ValueError("Cannot save empty task list to CSV")

    # Define CSV columns based on task structure
    fieldnames = ["due_date", "start_date", "status", "priority", "details", "assignee"]

    with open(filename, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        # Write header row
        writer.writeheader()

        # Write each task as a row
        for task in tasks:
            writer.writerow(task)

    print(f"Saved {len(tasks)} tasks to {filename}")


def print_task_summary(tasks: List[Dict[str, Any]]) -> None:
    """
    Print a summary of tasks by status.

    Args:
        tasks: List of task dictionaries
    """
    status_counts = {}

    for task in tasks:
        status = task.get("status", "Unknown")
        status_counts[status] = status_counts.get(status, 0) + 1

    print("\nTask Summary:")
    print(f"Total tasks: {len(tasks)}")
    print("\nBy Status:")
    for status, count in sorted(status_counts.items()):
        print(f"  {status}: {count}")


def main():
    """Run the task flattener application."""
    # TODO: use sys.argv to read the input file and optional output file
    # TODO: call parse_arguments(sys.argv[1:])
    # TODO: open and read the JSON file using read_tasks_from_json()
    # TODO: call flatten_tasks() to flatten the nested structure
    # TODO: print a summary of the tasks using print_task_summary()
    # TODO: save the flattened tasks to CSV using save_tasks_to_csv()
    # TODO: handle missing files and invalid input gracefully
    pass


if __name__ == "__main__":
    main()
