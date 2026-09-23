# Task Flattener - Recursion Lab

## Overview

This lab demonstrates recursion by flattening a hierarchical task structure
(tasks with subtasks) into a simple flat list. It's a practical example of how
recursion can process nested data structures.

## Files

- **`sample_tasks.json`** - Sample hierarchical task data
- **`generate_sample_data.py`** - Script to regenerate sample data
- **`task_flattener.py`** - Main program with recursive flattening function
- **`README.md`** - This file
- **`flattened_tasks.csv`** example output.

## Task Structure

Each task has the following attributes:

- `due_date` - When the task is due
- `start_date` - When the task starts
- `status` - Current status (e.g., "In Progress", "Completed", "Not Started")
- `priority` - Priority level (e.g., "High", "Medium", "Low")
- `details` - Task description
- `assignee` - Person assigned to the task
- `sub_tasks` - List of subtasks (each with the same structure)

## Usage

### 1. Generate Sample Data (Optional)

If you want to regenerate the sample data file:

```bash
python generate_sample_data.py
```

This creates `sample_tasks.json` with hierarchical task data.

### 2. Run the Task Flattener

```bash
python task_flattener.py
```

This will:

1. Read the nested task structure from `sample_tasks.json`
2. Flatten it recursively using the `flatten_tasks()` function
3. Display a summary of all tasks
4. Save the flattened tasks to `flattened_tasks.csv`

## Example

### Input (Nested Structure)

```json
[
  {
    "details": "Deploy New Web Application",
    "status": "In Progress",
    "assignee": "Alice Johnson",
    "sub_tasks": [
      {
        "details": "Setup Database Infrastructure",
        "status": "Completed",
        "assignee": "Bob Smith",
        "sub_tasks": [
          {
            "details": "Provision Database Server",
            "status": "Completed",
            "assignee": "Bob Smith",
            "sub_tasks": []
          }
        ]
      }
    ]
  }
]
```

### Output (Flattened List)

```
Deploy New Web Application, In Progress, Alice Johnson
Setup Database Infrastructure, Completed, Bob Smith
Provision Database Server, Completed, Bob Smith
```

## Understanding the Recursion

For a task structure like:

```
Task A
  ├── Task B
  │   └── Task C
  └── Task D
```

The recursion proceeds as:

1. Process Task A, add to list
2. Recursively process A's subtasks [B, D]
3. Process Task B, add to list
4. Recursively process B's subtasks [C]
5. Process Task C, add to list
6. Process Task D, add to list

Final result: [A, B, C, D]

## Questions

Answer the following questions as part of the README.md.

1. **Identify Base Cases**: What are the base cases in the `flatten_tasks()`
   function? I.E. What would end the recursion?

1. **Identify Recursive Case**: What is the recursive case in the `flatten_tasks()`
   function? I.E. When would the function call itself.

## Programming Activity

Implement `flatten_tasks` as described in here using the starter code 
provided in `task_flattener.py`
