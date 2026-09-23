# Parsing Command Line Arguments

## Structure

Create a solution directory `letter_frequency_cmd`

Create a file called `letter_frequency.py`.

## Exercise 0.1 - number of occurrences of a letter in a string

In this file, create a Python function `char_freq` that:

- takes a string as its only argument
- returns a dictionary:
  - the keys of the dictionary are the letters that appear in the string
  - for each letter, the associated value in the dictionary is the number of
    occurrences of the letter in the string

Examples:

```
>>> char_freq("aaaa")
{'a': 4}
>>> char_freq("Hello!")
{'H': 1, 'e': 1, 'l': 2, 'o': 1, '!': 1}
```

## Exercise 0.2 - number of occurrences, with filters

Create a function `letter_freq`. This function should reuse the `char_freq`
function. It takes a`str` argument (the string). It must:

- remove spaces
- remove punctuation
- count uppercase and lowercase letters together, but return lowercase letters
  in the result
- it _must_ use the `char_freq` function

_Note_: You want to import and use `string.punctuation`.

Example:

```
>>> letter_freq("Hello world!")
{'h': 1, 'e': 1, 'l': 3, 'o': 2, 'w': 1, 'r': 1, 'd': 1}
```

### Exercise 0.3 - histogram of letters

Create a function `histogram`. This function return a multi-line list of all
letters in a string, with as many "\*" characters as the number of times that
letter appears in the string. You must use the output from `letter_freq`.

```
>>> print(histogram("Haaaaah"))
h **
a *****
>>> print(histogram("Hello world!"))
h *
e *
l ***
o **
w *
r *
d *
```

### Exercise 1.0 - Create a CLI App

Create a `main()` function that uses `sys.argv` to create a command-line interface with the following functionality:

- Takes a positional argument `in_string` - the string to process
- Provides three optional flags:
  - `-c`: Use the `char_freq` function
  - `-l`: Use the `letter_freq` function  
  - `-g`: Use the `histogram` function (default if no flag specified)

The program should print the input string and the result of the selected operation.

Example usage:

```
python frequency_analysis.py "Hello world!" -c
python frequency_analysis.py "Hello world!" --letters
python frequency_analysis.py "Hello world!"
```

### Debugging the CLI in VS Code

You can run and debug the script from VS Code without typing the full command in the terminal each time.

1. Open the Python file you want to debug.
2. Open the Run and Debug panel.
3. Select a launch configuration.
4. Press F5 to start debugging.

For CLI programs that use `sys.argv`, the most useful configuration is one that passes arguments automatically.

#### Example `launch.json`

```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "Python Debugger: Current File",
      "type": "debugpy",
      "request": "launch",
      "program": "${file}",
      "console": "integratedTerminal"
    },
    {
      "name": "Python: Interactive Args",
      "type": "debugpy",
      "request": "launch",
      "program": "${file}",
      "console": "integratedTerminal",
      "args": ["${input:text}", "${input:operation}"]
    }
  ],
  "inputs": [
    {
      "id": "text",
      "type": "promptString",
      "description": "Enter text to process:",
      "default": "testing"
    },
    {
      "id": "operation",
      "type": "pickString",
      "description": "Select operation:",
      "options": ["-u", "-l", "-r"],
      "default": "-u"
    }
  ]
}
```

#### How this works

- `program`: "${file}" tells VS Code to run the file currently open in the editor.
- `console`: "integratedTerminal" displays output in the terminal so it behaves like a normal command-line program.
- `args`: ["${input:text}", "${input:operation}"] passes values into `sys.argv`.
- `inputs` defines the prompts shown when the debugger starts.
- `promptString` asks the user for text input.
- `pickString` gives a menu of valid choices for the operation flag.

This means the values entered in the debugger are passed into your script as if the user had run:

```bash
python letter_frequency.py "testing" "-u"
```

For a script using `sys.argv`, this is very helpful because you can test values quickly without rewriting the command each time.

#### Example of debugging a CLI script

If your script begins with code like this:

```python
import sys

arguments = sys.argv[1:]
print(arguments)
```

then the debugger will display the list of arguments you entered and you can inspect each value while the program runs.

This is a good way to confirm that your command-line parsing logic is working before you move on to more advanced tooling such as `argparse`.

### References
1. [Python command-line arguments](https://docs.python.org/3/library/sys.html#sys.argv)
2. [Command line and environment](https://docs.python.org/3/library/sys.html)
3. [VS Code Python debugging: launch.json](https://code.visualstudio.com/docs/python/debugging#_set-configuration-options)
4. [String Constants](https://docs.python.org/3/library/string.html#string-constants)
5. [Sets](https://docs.python.org/3/tutorial/datastructures.html#sets)