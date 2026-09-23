"""
Task Flattener - Recursively flatten nested task structures.

This program demonstrates recursion by flattening a hierarchical task structure
into a simple list of all tasks (removing the parent-child relationships).

The recursive function processes nested tasks and subtasks, creating a flat list
where each task appears as a single entry regardless of its nesting level.
"""

import csv
import json
from typing import Any, Dict, List


def flatten_tasks(tasks: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Recursively flatten a nested task structure into a flat list.

    This function takes a list of tasks where each task may contain sub_tasks,
    and returns a flat list containing all tasks and subtasks without the
    hierarchical relationship information.

    Args:
        tasks: List of task dictionaries, each potentially containing 'sub_tasks'

    Returns:
        Flat list of all tasks without sub_tasks field

    Example:
        Input:
        [
            {
                "details": "Main Task",
                "status": "In Progress",
                "sub_tasks": [
                    {"details": "Subtask 1", "status": "Done", "sub_tasks": []},
                    {"details": "Subtask 2", "status": "Pending", "sub_tasks": []}
                ]
            }
        ]

        Output:
        [
            {"details": "Main Task", "status": "In Progress"},
            {"details": "Subtask 1", "status": "Done"},
            {"details": "Subtask 2", "status": "Pending"}
        ]
    """

    return flat_list


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
    """Main function to demonstrate task flattening."""
    # Input and output filenames
    input_file = "sample_tasks.json"
    output_file = "flattened_tasks.csv"

    try:
        # Read nested task structure from JSON
        print(f"Reading tasks from {input_file}...")
        nested_tasks = read_tasks_from_json(input_file)

        print(f"Loaded {len(nested_tasks)} top-level tasks")

        # Flatten the task structure recursively
        print("\nFlattening task structure (recursive)...")
        flat_tasks_recursive = flatten_tasks(nested_tasks)

        # Display summary
        print_task_summary(flat_tasks_recursive)

        # Save to CSV
        print(f"\nSaving flattened tasks to {output_file}...")
        save_tasks_to_csv(flat_tasks_recursive, output_file)

        # Show first few tasks
        print("\n Tasks in flattened list (recursive):")
        for i, task in enumerate(flat_tasks_recursive[:5], 1):
            print(
                f"{i}. {task['details']} (Status: {task['status']}, "
                f"Priority: {task['priority']}, Assignee: {task['assignee']})"
            )

        if len(flat_tasks_recursive) > 5:
            print(f"... and {len(flat_tasks_recursive) - 5} more tasks")

    except FileNotFoundError:
        print(
            f"\nPlease run 'python generate_sample_data.py' first to create {input_file}"
        )
    except Exception as e:
        print(f"An error occurred: {e}")
        raise


if __name__ == "__main__":
    main()
