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

### 1. Set up the project with uv

This lab uses `uv` for dependency management. Before running the tests, add
`pytest` as a development dependency:

```bash
uv add --dev pytest
```

You can then run the test suite with:

```bash
uv run pytest 
```

### 2. Generate Sample Data (Optional)

If you want to regenerate the sample data file:

```bash
python generate_sample_data.py
```

This creates `sample_tasks.json` with hierarchical task data.

### 3. Run the Task Flattener

The program should accept the input and output filenames from the command line.

```bash
python task_flattener.py sample_tasks.json flattened_tasks.csv
```

You may also omit the output file name and allow the program to use the default:

```bash
python task_flattener.py sample_tasks.json
```

This will:

1. Read the nested task structure from the input JSON file
2. Flatten it recursively using the `flatten_tasks()` function
3. Display a summary of all tasks
4. Save the flattened tasks to the output CSV file

The script should use `sys.argv` to read both file names from the command line.

## Handling Missing Files and Exceptions

Your program should also handle file-related problems gracefully.

### Missing input file

If the user runs the program with a file that does not exist, your program should
catch the `FileNotFoundError` exception and print a helpful message instead of
crashing.

Example:

```bash
python task_flattener.py does_not_exist.json
```

Expected behavior:

```text
Error: File 'does_not_exist.json' not found.
Please run 'python generate_sample_data.py' first to create the input file
```

### Invalid JSON

If the JSON file exists but contains invalid JSON, you should catch
`json.JSONDecodeError` and display a message that the file is not valid JSON.

### Empty task list

If the input file loads successfully but produces no tasks, the CSV writing step
should raise a clear exception such as `ValueError` instead of creating a broken
output file.

This means your implementation should use `try` and `except` blocks around file
I/O and JSON loading code.

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

This starter intentionally leaves most of the real programming for you to complete.
The helper functions for parsing arguments, reading JSON, saving CSV, and
printing the summary are already provided, but the recursive algorithm and the
overall program flow are your responsibility.

Your job is to:

1. Implement the recursive `flatten_tasks()` function
2. Use `sys.argv` and `parse_arguments()` to read the input and output filenames
3. Open and read the JSON file
4. Call `flatten_tasks()` to recursively flatten the nested structure
5. Print a summary of the results
6. Save the flattened output to CSV
7. Handle file errors and invalid input gracefully

This lab is intentionally structured so students must parse the command line and
complete most of the actual programming themselves.

## Running the Tests

After you have implemented the recursive function and the CLI flow, run the
project tests from the lab folder:

```bash
uv add --dev pytest
uv run pytest 
```

The tests check that:

- `parse_arguments()` handles the required command-line inputs correctly
- `flatten_tasks()` returns the correct flattened list for empty, single, nested,
and multi-task structures
