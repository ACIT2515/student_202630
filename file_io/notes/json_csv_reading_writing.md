# Reading and Writing JSON and CSV Files

These notes explain the basic file patterns to read a nested JSON structure, flatten it in Python, and then save the result to a CSV file.

## Why JSON and CSV are useful

- JSON is a good format for storing structured data such as lists of Python dictionaries.
- CSV is a good format for saving rows of data in a spreadsheet-friendly layout.
- In the task flattener exercise, the input data is stored in JSON and the final output is written to CSV.

## Reading JSON files

Python's `json` module is used to read and write JSON data.

```python
import json

with open("sample_tasks.json", "r", encoding="utf-8") as file:
    tasks = json.load(file)

print(tasks)
```

### What this does

- `open(..., "r")` opens the file for reading
- `encoding="utf-8"` makes sure text is read correctly
- `json.load(file)` converts the JSON text into Python data
- the result is usually a list of dictionaries

### Example JSON input

```json
[
  {
    "details": "Deploy app",
    "status": "In Progress",
    "assignee": "Alice",
    "sub_tasks": [
      {
        "details": "Setup database",
        "status": "Completed",
        "assignee": "Bob",
        "sub_tasks": []
      }
    ]
  }
]
```

This becomes a Python list like this:

```python
[
    {
        "details": "Deploy app",
        "status": "In Progress",
        "assignee": "Alice",
        "sub_tasks": [
            {
                "details": "Setup database",
                "status": "Completed",
                "assignee": "Bob",
                "sub_tasks": []
            }
        ]
    }
]
```

For the task flattener exercise, this is the shape of the data you will process recursively.

## Writing JSON files

You can also write Python data to a JSON file.

```python
import json

record = {
    "details": "Deploy app",
    "status": "In Progress",
    "assignee": "Alice"
}

with open("task_data.json", "w", encoding="utf-8") as file:
    json.dump(record, file, indent=2)
```

### Notes

- `"w"` means write mode
- `indent=2` makes the JSON easier to read for humans
- `json.dump(...)` writes the Python object to the file

## Reading CSV files

CSV files store values in rows separated by commas.

```python
import csv

with open("tasks.csv", "r", newline="", encoding="utf-8") as file:
    reader = csv.DictReader(file)

    for row in reader:
        print(row)
```

### What this does

- `newline=""` is recommended when using Python's CSV module
- `csv.DictReader(file)` reads each row and turns it into a dictionary
- the first row of the file is assumed to contain column names

### Example CSV file

```csv
details,status,assignee
Deploy app,In Progress,Alice
Setup database,Completed,Bob
```

This is read as:

```python
[
    {"details": "Deploy app", "status": "In Progress", "assignee": "Alice"},
    {"details": "Setup database", "status": "Completed", "assignee": "Bob"}
]
```

## Writing CSV files

```python
import csv

rows = [
    {"details": "Deploy app", "status": "In Progress", "assignee": "Alice"},
    {"details": "Setup database", "status": "Completed", "assignee": "Bob"}
]

fieldnames = ["details", "status", "assignee"]

with open("tasks.csv", "w", newline="", encoding="utf-8") as file:
    writer = csv.DictWriter(file, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(rows)
```

### What this does

- `csv.DictWriter(...)` writes dictionaries to CSV rows
- `writeheader()` writes the column names
- `writerows(rows)` writes all the row data

## Applying this to the task flattener exercise

In the task flattener lab, the program usually does the following:

1. Read a nested list of tasks from a JSON file
2. Flatten the nested structure recursively
3. Save the flattened list to a CSV file

### Example pattern

```python
import csv
import json

with open("sample_tasks.json", "r", encoding="utf-8") as file:
    tasks = json.load(file)

flat_tasks = []

for task in tasks:
    flat_tasks.append({
        "details": task.get("details", ""),
        "status": task.get("status", ""),
        "assignee": task.get("assignee", "")
    })

fieldnames = ["details", "status", "assignee"]

with open("flattened_tasks.csv", "w", newline="", encoding="utf-8") as file:
    writer = csv.DictWriter(file, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(flat_tasks)
```

This is a simplified example, but it shows the exact pattern used in the task flattener exercise.

## Common mistakes to avoid

- Forgetting to use `encoding="utf-8"` when opening files
- Using `"r"` when you meant to write
- Forgetting `newline=""` when working with CSV files
- Expecting JSON to be a simple string instead of a Python data structure
- Writing dictionaries with keys that do not match the CSV header row

## Best practice

When working with JSON and CSV:

- use `json.load()` to read JSON
- use `json.dump()` to write JSON
- use `csv.DictReader()` to read rows as dictionaries
- use `csv.DictWriter()` to write dictionaries to CSV
- keep the field names consistent across rows and output files

## Summary

The basic idea is simple:

- JSON is used for structured nested Python objects
- CSV is used for tabular data output
- Python gives us easy tools to read and write both formats

## References

1. [Python JSON module](https://docs.python.org/3/library/json.html)
2. [Python CSV module](https://docs.python.org/3/library/csv.html)
3. [Reading and writing files in Python](https://docs.python.org/3/tutorial/inputoutput.html)
