# Debugging Python Scripts with Command-Line Arguments in VS Code

## Overview

When developing command-line applications, you need to test your code with
different arguments. This guide shows how to configure VS Code's debugger to
pass arguments to your Python scripts.

## Why This Matters

Without proper configuration, clicking the debug button (F5) runs your script
without arguments, which will cause errors for programs that expect command-line
arguments.

## Using launch.json

### Step 1: Create launch.json

1. Open your project folder in VS Code
2. Open the Run and Debug view (`Ctrl+Shift+D`)
3. Click "create a launch.json file"
4. Select "Python File"

VS Code creates `.vscode/launch.json` in your project folder.

### Step 2: Configure Arguments

Edit `.vscode/launch.json` to add the `args` parameter:

```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "Python: Current File",
      "type": "debugpy",
      "request": "launch",
      "program": "${file}",
      "console": "integratedTerminal",
      "args": []
    }
  ]
}
```

### Step 3: Add Your Arguments

The `args` parameter takes an array of strings, where each element is one
argument:

```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "Python: Current File",
      "type": "debugpy",
      "request": "launch",
      "program": "${file}",
      "console": "integratedTerminal",
      "args": ["input.txt", "--verbose"]
    }
  ]
}
```

This is equivalent to running:

```bash
python your_script.py input.txt --verbose
```

## Using Input Variables for Interactive Arguments

VS Code supports the `${input:variableName}` syntax to prompt for arguments when
you start debugging. This is useful when you want to test different inputs
without editing launch.json each time.

### Step 1: Add Input Variables

At the end of your launch.json, add an `inputs` section:

```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "Python: Interactive Args",
      "type": "debugpy",
      "request": "launch",
      "program": "${file}",
      "console": "integratedTerminal",
      "args": ["${input:filename}", "${input:operation}"]
    }
  ],
  "inputs": [
    {
      "id": "filename",
      "type": "promptString",
      "description": "Enter filename to process:",
      "default": "people_1.txt"
    },
    {
      "id": "operation",
      "type": "pickString",
      "description": "Select operation:",
      "options": ["-a", "-c", "-u", "-s"],
      "default": "-s"
    }
  ]
}
```

When you press F5, VS Code will:

1. Prompt you to enter a filename (with "people_1.txt" as default)
2. Show a dropdown to select an operation flag

### Input Types

VS Code supports several input types:

#### promptString

Asks for text input:

```json
{
  "id": "inputText",
  "type": "promptString",
  "description": "Enter text to process:",
  "default": "Hello world!"
}
```

#### pickString

Shows a dropdown menu:

```json
{
  "id": "operation",
  "type": "pickString",
  "description": "Select operation:",
  "options": ["add", "subtract", "multiply", "divide"],
  "default": "add"
}
```

#### promptFile

Opens a file picker dialog:

```json
{
  "id": "dataFile",
  "type": "promptFile",
  "description": "Select data file:"
}
```

## Examples for Common Scenarios

### Example 1: Debugging frequency_analysis.py with Interactive Input

```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "Frequency Analysis: Interactive",
      "type": "debugpy",
      "request": "launch",
      "program": "${workspaceFolder}/frequency_analysis.py",
      "console": "integratedTerminal",
      "args": ["${input:textString}", "${input:operation}"]
    },
    {
      "name": "Frequency Analysis: Chars",
      "type": "debugpy",
      "request": "launch",
      "program": "${workspaceFolder}/frequency_analysis.py",
      "console": "integratedTerminal",
      "args": ["Hello world!", "-c"]
    },
    {
      "name": "Frequency Analysis: Letters",
      "type": "debugpy",
      "request": "launch",
      "program": "${workspaceFolder}/frequency_analysis.py",
      "console": "integratedTerminal",
      "args": ["Hello world!", "--letters"]
    },
    {
      "name": "Frequency Analysis: Histogram (default)",
      "type": "debugpy",
      "request": "launch",
      "program": "${workspaceFolder}/frequency_analysis.py",
      "console": "integratedTerminal",
      "args": ["Hello world!"]
    }
  ],
  "inputs": [
    {
      "id": "textString",
      "type": "promptString",
      "description": "Enter text to analyze:",
      "default": "Hello world!"
    },
    {
      "id": "operation",
      "type": "pickString",
      "description": "Select operation:",
      "options": ["-c", "-l", "-g"],
      "default": "-g"
    }
  ]
}
```

### Example 3: Arguments with Spaces

If your arguments contain spaces, keep them as a single string:

```json
"args": ["This is one argument", "this_is_another"]
```

This is equivalent to:

```bash
python script.py "This is one argument" "this_is_another"
```

## Using Multiple Configurations

You can create multiple debug configurations for different test cases:

```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "Test Case 1: Basic",
      "type": "debugpy",
      "request": "launch",
      "program": "${workspaceFolder}/main.py",
      "console": "integratedTerminal",
      "args": ["input.txt"]
    },
    {
      "name": "Test Case 2: With Flags",
      "type": "debugpy",
      "request": "launch",
      "program": "${workspaceFolder}/main.py",
      "console": "integratedTerminal",
      "args": ["input.txt", "--verbose", "--debug"]
    },
    {
      "name": "Test Case 3: Different File",
      "type": "debugpy",
      "request": "launch",
      "program": "${workspaceFolder}/main.py",
      "console": "integratedTerminal",
      "args": ["other.txt", "-o", "output.txt"]
    }
  ]
}
```

To select which configuration to run:

1. Open the Run and Debug view (`Ctrl+Shift+D`)
2. Use the dropdown at the top to select your configuration
3. Press `F5` or click the green play button

## Important Notes

### Argument Format

- Each argument is a separate string in the array
- Flags and their values are separate: `["-o", "output.txt"]`
- Arguments with spaces stay as one string: `["Hello world!"]`
- Empty array means no arguments: `[]`

### File Paths

- Use forward slashes `/` or escaped backslashes `\\`
- Relative paths are relative to `cwd` (current working directory)
- Use `${workspaceFolder}` for project-relative paths:

```json
"args": ["${workspaceFolder}/data/input.txt"]
```

### Variable Substitution

VS Code supports several variables:

- `${workspaceFolder}` - your project root directory
- `${file}` - currently open file
- `${fileBasename}` - filename without directory
- `${fileDirname}` - directory of current file

Example:

```json
"args": ["${fileDirname}/test_data.txt", "--output", "${fileDirname}/results"]
```

## Debugging Workflow

1. **Set breakpoints** in your code where you want to pause
2. **Select your debug configuration** from the dropdown
3. **Press F5** to start debugging
4. **Step through code** using:
   - `F10` - Step over (execute current line)
   - `F11` - Step into (enter function)
   - `Shift+F11` - Step out (exit function)
   - `F5` - Continue (run to next breakpoint)

## Verifying Arguments

To verify your arguments are being passed correctly, set a breakpoint right
after `parse_args()`:

```python
def main():
    parser = argparse.ArgumentParser(description="My program")
    parser.add_argument("filename", help="File to process")
    parser.add_argument("-v", "--verbose", action="store_true")

    args = parser.parse_args()
    # Set breakpoint here and inspect args in Variables panel
    print(args)
```

## Common Issues

### Issue: Arguments Not Working

**Problem:** Your script runs but doesn't receive the arguments.

**Solution:**

- Check the `args` array in launch.json is properly formatted
- Ensure you selected the correct configuration from dropdown
- Verify the `program` path points to your script

### Issue: "No module named X"

**Problem:** Import errors when debugging.

**Solution:**

- Set `"cwd": "${workspaceFolder}"` in launch.json
- Ensure your working directory is correct

### Issue: File Not Found

**Problem:** Script can't find data files.

**Solution:**

- Use absolute paths or `${workspaceFolder}` for file arguments
- Or set `"cwd"` to the directory containing your data:

```json
"cwd": "${workspaceFolder}/data"
```

## References

- [VS Code Debugging](https://code.visualstudio.com/docs/editor/debugging)
- [Python Debugging in VS Code](https://code.visualstudio.com/docs/python/debugging)
- [Launch.json Attributes](https://code.visualstudio.com/docs/python/debugging#_set-configuration-options)
- [Variables Reference](https://code.visualstudio.com/docs/editor/variables-reference)
- [Input Variables](https://code.visualstudio.com/docs/editor/variables-reference#_input-variables)
- [Argparse Documentation](https://docs.python.org/3/library/argparse.html)
