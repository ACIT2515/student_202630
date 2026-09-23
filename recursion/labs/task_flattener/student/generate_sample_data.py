"""
Generate sample task data with nested subtasks.

This script creates a JSON file with hierarchical task structure
demonstrating nested tasks up to 3-4 levels deep.
"""

import json
from datetime import datetime, timedelta


def generate_sample_tasks():
    """
    Generate sample task data with nested subtasks.

    Returns:
        List of task dictionaries with nested sub_tasks
    """
    tasks = [
        {
            "due_date": "2026-02-15",
            "start_date": "2026-01-10",
            "status": "In Progress",
            "priority": "High",
            "details": "Deploy New Web Application",
            "assignee": "Alice Johnson",
            "sub_tasks": [
                {
                    "due_date": "2026-01-20",
                    "start_date": "2026-01-10",
                    "status": "Completed",
                    "priority": "High",
                    "details": "Setup Database Infrastructure",
                    "assignee": "Bob Smith",
                    "sub_tasks": [
                        {
                            "due_date": "2026-01-12",
                            "start_date": "2026-01-10",
                            "status": "Completed",
                            "priority": "High",
                            "details": "Provision Database Server",
                            "assignee": "Bob Smith",
                            "sub_tasks": [],
                        },
                        {
                            "due_date": "2026-01-15",
                            "start_date": "2026-01-13",
                            "status": "Completed",
                            "priority": "Medium",
                            "details": "Configure Security Groups",
                            "assignee": "Charlie Davis",
                            "sub_tasks": [],
                        },
                        {
                            "due_date": "2026-01-18",
                            "start_date": "2026-01-16",
                            "status": "Completed",
                            "priority": "High",
                            "details": "Import Initial Data",
                            "assignee": "Bob Smith",
                            "sub_tasks": [],
                        },
                    ],
                },
                {
                    "due_date": "2026-02-01",
                    "start_date": "2026-01-21",
                    "status": "In Progress",
                    "priority": "High",
                    "details": "Develop Application Features",
                    "assignee": "Diana Martinez",
                    "sub_tasks": [
                        {
                            "due_date": "2026-01-25",
                            "start_date": "2026-01-21",
                            "status": "Completed",
                            "priority": "High",
                            "details": "User Authentication Module",
                            "assignee": "Diana Martinez",
                            "sub_tasks": [],
                        },
                        {
                            "due_date": "2026-01-30",
                            "start_date": "2026-01-26",
                            "status": "In Progress",
                            "priority": "Medium",
                            "details": "Dashboard Interface",
                            "assignee": "Ethan Wilson",
                            "sub_tasks": [
                                {
                                    "due_date": "2026-01-27",
                                    "start_date": "2026-01-26",
                                    "status": "Completed",
                                    "priority": "Medium",
                                    "details": "Design Dashboard Mockups",
                                    "assignee": "Ethan Wilson",
                                    "sub_tasks": [],
                                },
                                {
                                    "due_date": "2026-01-30",
                                    "start_date": "2026-01-28",
                                    "status": "In Progress",
                                    "priority": "Medium",
                                    "details": "Implement Dashboard Components",
                                    "assignee": "Fiona Lee",
                                    "sub_tasks": [],
                                },
                            ],
                        },
                    ],
                },
                {
                    "due_date": "2026-02-10",
                    "start_date": "2026-02-02",
                    "status": "Not Started",
                    "priority": "High",
                    "details": "Testing and QA",
                    "assignee": "George Taylor",
                    "sub_tasks": [
                        {
                            "due_date": "2026-02-05",
                            "start_date": "2026-02-02",
                            "status": "Not Started",
                            "priority": "High",
                            "details": "Unit Testing",
                            "assignee": "George Taylor",
                            "sub_tasks": [],
                        },
                        {
                            "due_date": "2026-02-08",
                            "start_date": "2026-02-06",
                            "status": "Not Started",
                            "priority": "High",
                            "details": "Integration Testing",
                            "assignee": "Hannah Brown",
                            "sub_tasks": [],
                        },
                        {
                            "due_date": "2026-02-10",
                            "start_date": "2026-02-09",
                            "status": "Not Started",
                            "priority": "Medium",
                            "details": "User Acceptance Testing",
                            "assignee": "Ian Clark",
                            "sub_tasks": [],
                        },
                    ],
                },
                {
                    "due_date": "2026-02-15",
                    "start_date": "2026-02-11",
                    "status": "Not Started",
                    "priority": "High",
                    "details": "Production Deployment",
                    "assignee": "Alice Johnson",
                    "sub_tasks": [],
                },
            ],
        },
        {
            "due_date": "2026-03-01",
            "start_date": "2026-02-01",
            "status": "Not Started",
            "priority": "Medium",
            "details": "Security Audit",
            "assignee": "Jack Anderson",
            "sub_tasks": [
                {
                    "due_date": "2026-02-15",
                    "start_date": "2026-02-01",
                    "status": "Not Started",
                    "priority": "Medium",
                    "details": "Vulnerability Scanning",
                    "assignee": "Jack Anderson",
                    "sub_tasks": [],
                },
                {
                    "due_date": "2026-02-25",
                    "start_date": "2026-02-16",
                    "status": "Not Started",
                    "priority": "High",
                    "details": "Penetration Testing",
                    "assignee": "Karen White",
                    "sub_tasks": [],
                },
            ],
        },
    ]

    return tasks


def save_tasks_to_json(tasks, filename="sample_tasks.json"):
    """
    Save tasks to a JSON file.

    Args:
        tasks: List of task dictionaries
        filename: Output filename
    """
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(tasks, f, indent=2, ensure_ascii=False)

    print(f"Sample data saved to {filename}")


def main():
    """Generate and save sample task data."""
    tasks = generate_sample_tasks()
    save_tasks_to_json(tasks)

    # Print summary
    def count_tasks(task_list):
        """Recursively count all tasks including subtasks."""
        count = 0
        for task in task_list:
            count += 1  # Count this task
            count += count_tasks(task.get("sub_tasks", []))  # Count subtasks
        return count

    total_tasks = count_tasks(tasks)
    print(f"Generated {total_tasks} total tasks (including subtasks)")
    print(f"Top-level tasks: {len(tasks)}")


if __name__ == "__main__":
    main()
