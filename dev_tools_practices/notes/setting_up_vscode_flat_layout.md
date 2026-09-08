# Setting Up a Flat Python Project

## Overview

A flat or adhoc project layout is a simple project structure where all Python
files are in a single directory. This approach is ideal for small scripts,
learning exercises, quick prototypes, and simple programs that don't require
complex organization.

This is the formate that we use for the first part of this course.

## When to Use a Flat Layout

Use a flat project layout when:

- Writing small scripts (< 500 lines of code)
- Creating quick prototypes or experiments
- Working on assignments or exercises

## Project Structure

A typical flat project has this structure:

```
my_project/
├── main.py              # Entry point for your program
├── helper.py            # Additional modules (optional)
├── data.txt             # Data files (optional)
└── README.md            # Project description (optional)
```

## Setting Up in VS Code

### 1. Create a Project Folder

Open a terminal (PowerShell on Windows) and create your project directory:

```powershell
mkdir my_project
cd my_project
```

### 2. Open in VS Code

Open the folder in VS Code:

```powershell
code .
```

Or use **File → Open Folder** from the VS Code menu.

### 3. Create Your Python Files

Create your main Python file:

- Click the **New File** button in the Explorer pane
- Name it `main.py`
- Start coding!

### Configuring VSCode
#### Select Python Interpreter

1. Open the Command Palette (`Ctrl+Shift+P`)
2. Type "Python: Select Interpreter"
3. Choose your Python installation (e.g., Python 3.14)

VS Code will show the selected interpreter in the status bar.

#### Configure Workspace Settings (Optional)

Create a `.vscode/settings.json` file in your project folder to configure workspace-specific settings:

1. Create a `.vscode` folder in your project root
2. Create a `settings.json` file inside it
3. Add your settings:

```json
{
    "python.defaultInterpreterPath": "python",
    "python.terminal.activateEnvironment": true,
    "files.autoSave": "afterDelay",
    "editor.formatOnSave": true,
    "python.formatting.provider": "black",
    "python.linting.enabled": true,
    "python.linting.pylintEnabled": false,
    "python.linting.flake8Enabled": true
}
```

Common settings:
- `python.defaultInterpreterPath`: Path to your Python interpreter
- `files.autoSave`: Auto-save files after delay
- `editor.formatOnSave`: Format code when saving
- `python.linting.enabled`: Enable code linting

#### Configure Debugging 

Create a `.vscode/launch.json` file to customize debugging:

1. Open the Run and Debug view (`Ctrl+Shift+D`)
2. Click "create a launch.json file"
3. Select "Python File"
4. VS Code will create `.vscode/launch.json` with default configuration:

```json
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Python: Current File",
            "type": "debugpy",
            "request": "launch",
            "program": "${file}",
            "console": "integratedTerminal"
        },
        {
            "name": "Python: Main File",
            "type": "debugpy",
            "request": "launch",
            "program": "${workspaceFolder}/main.py",
            "console": "integratedTerminal"
        }
    ]
}
```

Useful configuration options:
- `program`: File to run (use `${file}` for current file or specify a path)
- `console`: Where to show output (`integratedTerminal` or `internalConsole`)
- `args`: Command-line arguments as an array: `["arg1", "arg2"]`
- `cwd`: Working directory (defaults to `${workspaceFolder}`)

## Running Your Code

### Option 1: Using the Run Button

1. Open your Python file
2. Click the **▷ Run** button in the top-right corner
3. View output in the integrated terminal

### Option 2: Using the Terminal

Open the integrated terminal (`Ctrl+\``) and run:

```powershell
python main.py
```

### Option 3: Using the Debugger

1. Set breakpoints by clicking left of line numbers
2. Press `F5` to start debugging
3. Select "Python File" when prompted

## Best Practices

### File Naming

- Use lowercase with underscores: `my_module.py`
- Keep names descriptive: `calculator.py` not `calc.py`
- Main entry point: `main.py` or a descriptive name

### Code Organization

- Keep related functions in the same file
- Always use a main guard for executable scripts:
  ```python
  if __name__ == "__main__":
      main()
  ```

### Importing Between Files

If you have multiple Python files in the same folder:

```python
# In helper.py
def greet(name):
    return f"Hello, {name}!"

# In main.py
from helper import greet

if __name__ == "__main__":
    print(greet("World"))
```

## Adding a README

Create a `README.md` file to document your project:

```markdown
# My Project

Description of what your project does.

## How to Run

python main.py

## Depenencies

```

## When to Graduate to a Package Structure

Consider switching to a more structured layout when:

- Your project grows beyond 5-10 files
- You need to distribute your code
- You're using external dependencies
- You need automated testing
- Multiple people are collaborating

## Common Issues

### Import Errors

If you get import errors between files:

- Ensure files are in the same directory
- Check for typos in import statements
- Verify file names match import statements

### Wrong Python Version

### File Not Running

If clicking Run doesn't work:

- Ensure the Python extension is installed
- Check that a Python interpreter is selected
- Try running from the terminal instead

## Example Project

Here's a complete simple project:

**main.py:**

```python
"""A simple calculator program."""
from operations import add, subtract, multiply, divide

def main():
    """Run the calculator program.

    Prompts user for two numbers and an operation, then displays the result.
    """
    print("Simple Calculator")
    print("-" * 20)

    a = float(input("Enter first number: "))
    b = float(input("Enter second number: "))
    op = input("Operation (+, -, *, /): ")

    if op == "+":
        print(f"Result: {add(a, b)}")
    elif op == "-":
        print(f"Result: {subtract(a, b)}")
    elif op == "*":
        print(f"Result: {multiply(a, b)}")
    elif op == "/":
        print(f"Result: {divide(a, b)}")
    else:
        print("Invalid operation")

if __name__ == "__main__":
    main()
```

**operations.py:**

```python
"""Calculator operations."""

def add(a, b):
    """Return the sum of a and b.

    Args:
        a: First number.
        b: Second number.

    Returns:
        The sum of a and b.
    """
    return a + b

def subtract(a, b):
    """Return the difference of a and b.

    Args:
        a: First number.
        b: Second number.

    Returns:
        The difference of a and b.
    """
    return a - b

def multiply(a, b):
    """Return the product of a and b.

    Args:
        a: First number.
        b: Second number.

    Returns:
        The product of a and b.
    """
    return a + b

def divide(a, b):
    """Return the quotient of a and b.

    Args:
        a: First number (dividend).
        b: Second number (divisor).

    Returns:
        The quotient of a and b.

    Raises:
        ValueError: If b is zero.
    """
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b
```

## _Remember_

Open each activity or lab in its own directory and configure VSCode for the specific activity.

_Don't_ open an indiviual file in VSCode.