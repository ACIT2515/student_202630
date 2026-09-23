# Python Program Arguments and `sys.argv`

## Why Programs Need Command-Line Arguments

A script that hardcodes its input (a filename, a search string, a mode of
operation) only does one thing. Every time you need it to do something
slightly different, you have to edit the source code. Command-line
arguments let a program's behavior change from run to run, without touching
the code:

```bash
python scan_host.py --service Spooler
python scan_host.py --service WinRM
```

## Reading Raw Arguments with `sys.argv`

Python gives every running script access to the raw command-line words
through `sys.argv`, a list of strings. The first item is always the script
name itself. The remaining items are the actual arguments passed by the
user:

```python
import sys

print(sys.argv)
```

```bash
$ python my_script.py arg1 arg2
['my_script.py', 'arg1', 'arg2']
```

This means:

- `sys.argv[0]` is the script name
- `sys.argv[1]` is the first user argument
- `sys.argv[2]` is the second user argument
- `sys.argv[1:]` is the list of all user arguments after the script name

A very common pattern is:

```python
import sys

if len(sys.argv) < 2:
    print("Usage: python my_script.py <input_text>")
    sys.exit(1)

text = sys.argv[1]
print(f"You entered: {text}")
```

## Using Positional Arguments with `sys.argv`

A positional argument is a value that must appear in a particular order.
For example, when a program expects a username or a filename, that value is
usually the first argument after the script name:

```python
import sys

if len(sys.argv) != 2:
    print("Usage: python show_name.py <name>")
    sys.exit(1)

name = sys.argv[1]
print(f"Hello, {name}!")
```

Example usage:

```bash
python show_name.py Alice
Hello, Alice!
```

The key idea is that the programmer decides what order the arguments must
appear in. The code checks the required indexes manually.

## Using Optional Flags with `sys.argv`

Optional flags are values such as `-c`, `-l`, or `-g` that change how the
program behaves. These are often checked by looking for matching strings in
`sys.argv[1:]`:

```python
import sys

arguments = sys.argv[1:]
text = ""
operation = "default"

if not arguments:
    print("Usage: python process_text.py <text> [-c | -l | -g]")
    sys.exit(1)

text = arguments[0]

if len(arguments) > 1:
    flag = arguments[1]
    if flag in {"-c", "--chars"}:
        operation = "chars"
    elif flag in {"-l", "--letters"}:
        operation = "letters"
    elif flag in {"-g", "--histogram"}:
        operation = "histogram"
    else:
        print(f"Unknown option: {flag}")
        sys.exit(2)

print(f"Input: {text}")
print(f"Operation: {operation}")
```

This pattern is simple. The code is
clear: first extract the input, then inspect the remaining arguments for
flags.

## Checking for Mutually Exclusive Options

Some flags cannot be used together. For example, a program should not be
asked to uppercase and lowercase the same string in one run. With
`sys.argv`, this is handled explicitly with a small validation check:

```python
import sys

arguments = sys.argv[1:]
if len(arguments) < 1:
    print("Usage: python script.py <text> [-u | -l | -r]")
    sys.exit(1)

text = arguments[0]
flags = [arg for arg in arguments[1:] if arg.startswith("-")]

if flags.count("-u") + flags.count("-l") + flags.count("-r") > 1:
    print("Error: choose only one operation flag.")
    sys.exit(2)
```

## Overview: What `argparse` Is

`argparse` is Python's standard library tool for parsing command-line
arguments. It is designed for programs that need more than a raw list of
strings from `sys.argv`.

In simple programs, `sys.argv` is enough: you inspect the list yourself and
write the checks for missing values, wrong flags, and invalid input. That
works well for small scripts, but it becomes repetitive and easy to get
wrong as the program grows.

`argparse` solves these problems by letting you declare the arguments your
program expects and then automatically handling the details for you.

### Problems `argparse` Solves

- required arguments are checked automatically
- missing or bad values produce a clear error message
- `-h` and `--help` are generated automatically
- values can be converted to `int`, `float`, and other types
- flags can be grouped so that conflicting options are rejected
- optional arguments can be placed in any order without extra code

A good way to think about it is this:

- `sys.argv` gives you the raw text the user typed
- `argparse` turns that raw text into a cleaner, safer interface for your
  program


`argparse` is introduced here as the more structured optional method for larger command-line tools.

## Positional vs Optional Arguments

Argpase has the ability to specify some arguments as optional.

| Kind       | Example              | Required?                  | Order matters? | Use it for                                   |
| ---------- | --------------------- | --------------------------- | --------------- | --------------------------------------------- |
| Positional | `in_string`            | Yes, by default              | Yes              | The one input a program cannot run without    |
| Optional   | `-u`, `--upper`        | No, unless `required=True`   | No               | Flags that adjust or select program behavior  |

```python
parser.add_argument("input_text", help="The text string to process", type=str)
parser.add_argument("-u", "--upper", action="store_true", help="Convert text to uppercase")
```

Choose a positional argument for the value the program is fundamentally
about (the string to process, the file to scan). Choose an optional
argument for anything that changes *how* the program processes that value.

## Mutually Exclusive Groups

Some flags represent alternative choices, not combinations: a program that
converts text should not be told to uppercase *and* lowercase the same
input in one run. `add_mutually_exclusive_group()` enforces this
automatically, without an `if`/`elif` chain checking every possible
conflicting pair:

```python
operation = parser.add_mutually_exclusive_group()
operation.add_argument("-u", "--upper", action="store_true", help="Convert text to uppercase")
operation.add_argument("-l", "--lower", action="store_true", help="Convert text to lowercase")
operation.add_argument("-r", "--reverse", action="store_true", help="Reverse the text")
```

If a user passes both `-u` and `-l`, `argparse` reports the conflict and
exits before your program logic ever runs, rather than silently picking one
or producing confusing output. See the full example in
[argparse_demo.py](../demo/intro/argparse_demo.py).

## Boolean Flags with `action="store_true"`

A flag like `--verbose` usually represents "on" or "off," not a value the
user types in. `action="store_true"` gives the corresponding attribute
`False` by default, and switches it to `True` only if the flag is present:

```python
parser.add_argument("-u", "--upper", action="store_true")
```

This avoids a common trap: `type=bool` does not do what it looks like it
does, because `bool("False")` evaluates to `True` (any non-empty string is
truthy). `store_true` sidesteps that problem entirely by not expecting a
value after the flag at all.

## Exit Codes

By convention, a program's exit code tells whatever ran it (a shell script,
a scheduled task, another program) whether it succeeded: `0` means success,
and any nonzero value means some kind of failure. This matters most in
automation: a script in a pipeline or scheduled job is often not watched by
a person, so its exit code is the only signal available for "did this
work?"

`argparse` already participates in this convention: if required arguments
are missing or invalid, it prints a usage message to `stderr` and exits with
status code `2`, without your code needing to check for that case. Your own
program logic should follow the same convention deliberately, using
`sys.exit(code)` for the failure conditions specific to your program (for
example, exiting with a distinct nonzero code when a target host cannot be
reached, versus success when it can).

## Guidelines

1. Use `sys.argv` for first because it is easy to
   follow and easy to debug.
1. Use a positional argument for the one value the program cannot run
   without; use optional flags for everything that adjusts behavior.
1. Validate user input manually when working with `sys.argv` and give a
   clear usage message when the input is wrong.
1. Keep flag checks simple and explicit until the program becomes more
   complicated.
1. Move to `argparse` when the program grows and you want built-in help,
   validation, and cleaner error handling.
1. Treat exit codes as part of your program's interface: `0` for success,
   a distinct nonzero code for each meaningful failure.

## References

1. [Python sys.argv documentation](https://docs.python.org/3/library/sys.html#sys.argv)
2. [Python sys module documentation](https://docs.python.org/3/library/sys.html)
3. [Python: `arparse`](https://docs.python.org/3/library/argparse.html)
