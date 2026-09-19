# Reading and Writing Files in Python

Programs often need information that lasts after the program stops running:
configuration files, logs, reports, CSV exports, JSON data, or text entered by
a user. File I/O is how a Python program reads that saved information from disk
or writes new information back to disk.

This introduction focuses on **text files**: files whose contents can be read
as characters, such as `.txt`, `.csv`, `.md`, and `.json` files.

## Paths: Finding the File

A file path tells Python where a file is located. Most course programs should
use **relative paths**, which start from the project folder or from the folder
where the program is running.

Avoid hardcoding absolute paths like these:

```python
"C:\\Users\\student\\Documents\\ACIT2515\\lab.txt"
"/home/student/ACIT2515/lab.txt"
```

Those paths usually work only on one person's computer. A relative path is more
portable:

```python
"data/servers.txt"
"reports/summary.txt"
```

## Using `pathlib.Path`

`pathlib` is the standard library module for working with paths. It lets you
build paths with Python objects instead of manually joining strings.

```python
from pathlib import Path

data_file = Path("data") / "servers.txt"
report_file = Path("reports") / "summary.txt"
```

The `/` operator joins path parts using the correct separator for the operating
system. On Windows, Python understands backslashes. On macOS and Linux, Python
uses forward slashes.

Useful `Path` operations:

- `path.exists()`: check whether the path exists.
- `path.is_file()`: check whether the path is a file.
- `path.is_dir()`: check whether the path is a directory.
- `path.parent`: get the folder containing the file.
- `path.name`: get the file name only.
- `path.suffix`: get the file extension.
- `path.mkdir()`: create a directory.
- `path.iterdir()`: loop through items in a directory.

Example:

```python
from pathlib import Path

data_file = Path("data") / "servers.txt"

if data_file.exists() and data_file.is_file():
    print(f"Reading from {data_file}")
else:
    print("The data file does not exist yet.")
```

Before writing to a file in a new directory, create the directory first:

```python
from pathlib import Path

report_file = Path("reports") / "summary.txt"
report_file.parent.mkdir(exist_ok=True)
```

## Opening and Closing Files

The built-in `open()` function opens a file and returns a file object. A file
object represents the connection between your program and the file on disk.

```python
file_obj = open("data/servers.txt", "r", encoding="utf-8")
contents = file_obj.read()
file_obj.close()
```

The `.close()` method tells Python that the program is finished using the file.
It releases the file handle back to the operating system. When writing, closing
also helps ensure buffered data is flushed to disk.

Manual opening and closing works, but it is easy to forget `close()`. An
unclosed file may not finish writing data to disk, and it keeps an operating
system resource open longer than necessary.

Prefer a `with` statement:

```python
with open("data/servers.txt", "r", encoding="utf-8") as file_obj:
    contents = file_obj.read()
```

The `with` statement closes the file automatically when the indented block
finishes, even if an error occurs inside the block.

## What Is a Context Manager?

A **context manager** is an object that knows how to set something up before a
block of code runs, and clean it up after the block finishes. The `with`
statement is Python's syntax for using a context manager.

The general pattern is:

```python
with setup_something() as resource:
        use(resource)
```

For files, the setup step opens the file and the cleanup step closes it. This
matters because an open file is not just a Python value; it is also an operating
system resource. If a program forgets to close a file, data may not be fully
written to disk, and the operating system may keep the file handle open longer
than necessary.

This code:

```python
with open("data/servers.txt", "r", encoding="utf-8") as file_obj:
        contents = file_obj.read()
```

means:

1. Open the file.
1. Store the opened file object in `file_obj`.
1. Run the indented block.
1. Close the file automatically when the block finishes.

The cleanup step still runs if an exception occurs while reading or writing.
That is the main affordance of a context manager: it makes cleanup reliable,
even when the normal flow of the program is interrupted.

### How Context Managers Work

Behind the scenes, a context manager implements two special methods:

- `__enter__()`: runs at the start of the `with` block. It prepares the
    resource and returns the value assigned after `as`.
- `__exit__()`: runs when the `with` block finishes. It performs cleanup, such
    as closing a file.

For a file object, `__enter__()` returns the open file object and `__exit__()`
closes it. You do not need to write these methods to use files, but knowing
they exist explains why `with` works for many other resources too: database
connections, locks, temporary files, and network connections can all use the
same setup/use/cleanup pattern.

You can also open a `Path` object directly:

```python
from pathlib import Path

data_file = Path("data") / "servers.txt"

with data_file.open("r", encoding="utf-8") as file_obj:
    contents = file_obj.read()
```

## Common File Modes

| Mode | Meaning | What happens |
| ---- | ------- | ------------ |
| `"r"` | Read | Opens an existing file for reading |
| `"w"` | Write | Creates or replaces a file |
| `"a"` | Append | Adds new content to the end of a file |
| `"x"` | Create | Creates a new file, but fails if it already exists |

Be careful with `"w"`: it overwrites the existing file. Use `"a"` when you
want to add log entries without deleting previous ones.

## Reading the Whole File at Once

Use `.read()` when the file is small enough to fit comfortably in memory and
you want one string containing the whole file.

```python
from pathlib import Path

log_file = Path("logs") / "startup.log"

with log_file.open("r", encoding="utf-8") as file_obj:
    contents = file_obj.read()

print(contents)
```

This approach is simple, but it may use too much memory for very large files.

## Reading One Line at a Time

Use a `for` loop over the file object when you want to process the file line by
line. This is better for large files because Python does not need to load the
whole file at once.

```python
from pathlib import Path

log_file = Path("logs") / "startup.log"

with log_file.open("r", encoding="utf-8") as file_obj:
    for line in file_obj:
        print(line.strip())
```

Each `line` includes its newline character at the end. Use `.strip()` to remove
leading and trailing whitespace, including `\n`.

## Reading All Lines into a List

Use `.readlines()` when you want a list where each item is one line from the
file.

```python
from pathlib import Path

config_file = Path("data") / "services.txt"

with config_file.open("r", encoding="utf-8") as file_obj:
    lines = file_obj.readlines()

print(lines[0])
```

Like `.read()`, this loads the whole file into memory. For large log files,
prefer line-by-line iteration.

## Writing the Whole File at Once

Use `.write()` when you already have the full output as one string.

```python
from pathlib import Path

report_file = Path("reports") / "summary.txt"
report_file.parent.mkdir(exist_ok=True)

summary = "Host: workstation-01\nStatus: OK\n"

with report_file.open("w", encoding="utf-8") as file_obj:
    file_obj.write(summary)
```

Opening the file with `"w"` creates it if it does not exist. If it already
exists, the previous contents are replaced.

## Writing One Line at a Time

Use a loop with `.write()` when each output line is produced separately.
Remember that `.write()` does not add a newline automatically.

```python
from pathlib import Path

services = ["Spooler", "W32Time", "WinRM"]
report_file = Path("reports") / "services.txt"
report_file.parent.mkdir(exist_ok=True)

with report_file.open("w", encoding="utf-8") as file_obj:
    for service in services:
        file_obj.write(f"{service}\n")
```

You can also use `.writelines()`, but it also does not add newline characters
for you:

```python
from pathlib import Path

lines = ["Spooler\n", "W32Time\n", "WinRM\n"]
report_file = Path("reports") / "services.txt"

with report_file.open("w", encoding="utf-8") as file_obj:
    file_obj.writelines(lines)
```

## Appending to a File

Use append mode (`"a"`) when you want to keep existing contents and add new
content to the end. This is common for simple logs.

```python
from pathlib import Path

log_file = Path("logs") / "checks.log"
log_file.parent.mkdir(exist_ok=True)

with log_file.open("a", encoding="utf-8") as file_obj:
    file_obj.write("Checked Spooler service\n")
```

## Guidelines

1. Use `pathlib.Path` to build and inspect paths instead of hardcoding long
   absolute path strings.
1. Use relative paths for course projects whenever possible.
1. Use `with path.open(...) as file_obj:` so Python closes the file for you.
1. Use `.read()` for small files when you need the whole file as one string.
1. Use a `for` loop over the file object for large files or line-by-line work.
1. Use `"w"` to replace a file, `"a"` to add to a file, and `"r"` to read a
   file.
1. Include `encoding="utf-8"` when reading and writing text files.

## References

1. [Reading and Writing Files](https://docs.python.org/3/tutorial/inputoutput.html#reading-and-writing-files)
1. [`pathlib` Object-Oriented Filesystem Paths](https://docs.python.org/3/library/pathlib.html)
1. [File Objects](https://docs.python.org/3/glossary.html#term-file-object)


