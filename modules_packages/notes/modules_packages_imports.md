# Python Program Architecture: Scripts, Modules, and Packages

## Module

A Python module is a file containing Python code, usually with a .py extension.
It can define variables, functions, and classes that other Python files can
reuse.

For example, calculator.py is a module:

```python

def add(a, b):
    return a + b
```

Another file can import and use it:

```python
import calculator

print(calculator.add(2, 3))
```

Modules also create their own namespace, so calculator.add is distinct from an
add function defined elsewhere. A script is simply a module that you run
directly with the python program.

In Python, the distinction between a **script** and a **library** is strictly
based on how the code is used. Both are simply text files containing Python
statements, and both are technically **modules**.

- **Scripts**: Modules intended to be executed directly by the Python
  interpreter to perform a task.
- **Libraries**: Modules intended to be **imported** into other programs to
  provide functionality.

Note: this reference does not elaborate on scenarios where custom classes are
defined; this is left for later.

## Scripts

Python scripts are simply a collection of Python statements stored in a text
file that get executed when the script is loaded by the Python interpreter.
Technically, they are Python modules that are executed directly.

### Running Programs: Invocation Forms

Scripts can be run by invoking the Python interpreter and passing the name of
the script file in a CLI terminal:

    python $scriptname

Where `$scriptname` is the filename of the script.

Additionally, scripts can be invoked by name:

    $scriptname

but only if the following conditions are true:

**On Windows:**

1. Python is installed
2. The script has the `.py` file extension
3. The `$scriptname` specified is in the user's `$env:Path`, or you provide the
   full path

**On \*nix operating systems (macOS, Linux, BSD, etc.):**

1. Python is installed
2. The script specifies an interpreter on the first line in a specially formed
   comment called the `shebang`
   - for our course this will take the form `#!/usr/bin/env python3`
3. The script has the executable permissions set
   - this can be accomplished for the owner of the file using
     `chmod u+x $scriptname`
4. The `$scriptname` specified is in the user's `$PATH`, or you provide the path
   (e.g., `./scriptname` if in the current directory)

## Namespaces

**Key Principle:** Code that is intended to be reused should be organized into
its own module.

A namespace is, in short, "the place where a variable is stored" (namespaces are
implemented as dictionaries). Their purpose is to prevent naming conflicts.
Without the ability to divide up the scope where variables are visible, all
variable names used in a program would have to be unique. This would severely
limit the size of programs and the ability to reuse code.

So far we have used functions as a method of scoping variables.  
Modules provide another scope for variable naming.

Any script directly invoked by the Python interpreter adds any names it declares
to the global namespace. By default, when a module is imported, its name is
added to the global namespace and all of the names defined in the module are
added with the module name as a prefix.

## Import Statement

This statement is the mechanism that pulls modules into other modules or
scripts. It performs module lookup, compilation into bytecode if necessary,
loading, and execution.

The most basic `import` form is:

```python
import some_module
```

This completes the following steps:

1. Check if `some_module` is already loaded (i.e., is it in the `sys.modules`
   table? If so, skip finding and compiling the module)
2. Find the file `some_module.py` by searching the Standard Module Search Path
3. Compile the module to bytecode if necessary. Compilation is required when the
   compiled bytecode file (`some_module.version.pyc`) doesn't exist or is older
   than the source file. The bytecode files are stored in a `__pycache__`
   subdirectory located in the same directory as the source files
4. Run the module code. Generally this creates a series of variables (and
   functions) and makes them available with the prefix `some_module`

   If `some_module.py` defines a function `some_func`, it can be executed as
   `some_module.some_func()`

**Important:** Import statements only execute a module's code **once** per
program run, even if you import it multiple times. Subsequent imports simply
retrieve the already-loaded module from `sys.modules`.

### Brief Notes on Byte-Code Compilation

To speed up program execution, Python caches the compiled version of modules in
the `__pycache__` directory under the name `module.version.pyc`, where version
is the Python implementation and version that last compiled the file.

e.g., CPython release 3.14 that compiled `mod1.py` would create a cached
`__pycache__/mod1.cpython-314.pyc`

Python compares the modification date of the source with the cached compiled
version to determine if it needs to be recompiled.

Note that this process occurs automatically.

Python always recompiles and does not cache the module that's directly executed.

Second, it does not check the cache if there is no source file. This allows
compiled binary distribution of modules where only the `.pyc` file is provided.

### Additional Import Forms

It is possible to override the default import statement to change the way that a
module's variables and functions are brought into the current module in the
following ways:

1. **Import with alias:**

   ```python
   import module_name as local_name
   ```

   This imports the module `module_name` but makes it available via the
   `local_name` alias.

   Example: `import numpy as np`

2. **Import specific members:**

   ```python
   from module_name import member
   ```

   This pulls in the variable/function `member` from `module_name` and makes it
   available directly without the `module_name` prefix.

   Example: `from math import sqrt`

3. **Import specific members with alias:**

   ```python
   from module_name import member as local_name
   ```

   This pulls in the variable/function `member` from `module_name` and makes it
   available as `local_name` without the `module_name` prefix.

4. **Import everything (discouraged):**

   ```python
   from module_name import *
   ```

   This pulls all the variables/functions defined in `module_name` (that don't
   start with `_`) and makes them available directly without the `module_name`
   prefix.

   **Note: This is discouraged and considered bad programming practice**
   because:
   - It makes it unclear where names come from
   - It can cause name conflicts
   - It makes code harder to debug

## A Worked Example: The `my_print` Module

Let's start with a very simple module: `my_print.py`

```python
# filepath: my_print.py
# Contents of my_print.py

MY_MESSAGE = "Hello!"

def my_print_func(text):
    """Print a message and the provided text."""
    print(MY_MESSAGE)
    print(text)
```

### Importing the Whole Module

We can import this file (module) using `import`. Let's write another module that
uses `my_print`:

```python
# filepath: main.py
# Contents of main.py
import my_print

def main():
    my_print.my_print_func("Example.")
    print(my_print.MY_MESSAGE)

if __name__ == '__main__':
    main()
```

### Importing Only Specific Variables / Functions

```python
# filepath: main.py
from my_print import MY_MESSAGE

print(MY_MESSAGE)
```

### Key Takeaways

- The entire module `my_print` is imported when you use `import my_print`
- You can access functions or variables using the `.` notation
- Everything in Python is an object!
- You can access "properties" of the module like you access "behaviors" for data
  types (with the `.`)
- When the module is imported, the code it contains **IS EXECUTED**!
- Make sure you use `if __name__ == "__main__"` to prevent side effects

### `__name__`

When a module is directly executed by the Python interpreter as a script, the
variable `__name__` is assigned the value `"__main__"`.

If a module is imported, the `__name__` local name variable is set to the name
of the module.

### Modules that are both Libraries and Scripts

By checking the value of `__name__`, we can tell if a module was directly
invoked by the Python interpreter or imported by another script. This allows
Python files to act as both scripts (i.e., be directly executed) and as
libraries (i.e., be imported).

This check takes the form:

```python
if __name__ == '__main__':
    # Code here only runs when script is executed directly
    main()
```

This is common boilerplate code.

Only when the module is invoked directly (i.e., not imported) is the above true,
and that is the only time code within the above `if` statement is executed.

**Example:**

```python
# Contents of calculator.py

def add(a, b):
    """Add two numbers."""
    return a + b

def subtract(a, b):
    """Subtract b from a."""
    return a - b

def main():
    """Demo the calculator functions."""
    print(f"5 + 3 = {add(5, 3)}")
    print(f"5 - 3 = {subtract(5, 3)}")

if __name__ == '__main__':
    # This only runs when you execute: python calculator.py
    main()
```

When imported (`import calculator`), only the functions are available. When run
directly (`python calculator.py`), it also runs the demo in `main()`.

### Recommended Script Structure

**Write scripts as a collection of small functions.** Keep as much code as
possible out of the module root. Module-root code should normally contain only
imports, constants, and function or class definitions. Avoid global variables
used as mutable program state.

Put the program's work in a `main()` function. Call `main()` only from the
`if __name__ == '__main__':` conditional:

```python
# Contents of report.py

DEFAULT_REPORT_NAME = "report.txt"

def collect_data():
   """Return the data for the report."""
   return ["item 1", "item 2"]

def write_report(items, filename):
   """Write report items to a file."""
   with open(filename, "w") as file:
      file.write("\n".join(items))

def main():
   """Run the report program."""
   items = collect_data()
   write_report(items, DEFAULT_REPORT_NAME)

if __name__ == '__main__':
   main()
```

This structure makes functions easier to test and reuse, and prevents program
behavior from running unexpectedly when another module imports the script.

### Practical Considerations

1. It is customary to place all imports at the top of a module
2. The list of any loaded modules is stored in `sys.modules` from the `sys`
   library
3. Module names should be all lowercase, using numbers, letters, and underscores
   only
4. Avoid circular imports (module A imports module B, which imports module A)

### Finding Modules and the Standard Module Search Path

In order to find module files, Python searches for files with the `.py`
extension in a particular list of directories. This list of directories is the
Standard Module Search Path.

The path is comprised of the following components:

1. The home directory of the program (the directory containing the script being
   run)
2. Directories in the `PYTHONPATH` environment variable (if set)
3. Standard library directories
4. The contents of any `.pth` files (if present). These are simply files with
   directory names listed one per line. They are used to add site-specific
   locations to the search path. See
   [Python Standard Library: site](https://docs.python.org/3/library/site.html)
5. The site-packages home of third-party extensions

These components are combined and stored in the `sys.path` variable.

You can inspect this path by running:

```python
import sys
print(sys.path)
```

#### Current Directory

This is added automatically to the search path. This is the directory containing
a running program's top-level script (i.e., the name of the file passed to the
Python interpreter). When running Python interactively, this is the current
working directory.

#### Module Discovery Process

1. Check for built-in module
2. Search list of directories in `sys.path`

## Standard Library Modules

Python comes with a collection of over 200 modules known as the standard
library. It contains platform-independent support for common programming tasks
including:

- operating system interfaces (`os`, `pathlib`)
- object persistence (`pickle`, `json`)
- text pattern matching (`re`)
- network and Internet scripting (`http`, `urllib`, `socket`)
- GUI construction (`tkinter`)
- mathematics (`math`, `statistics`, `random`)
- file and directory access (`shutil`, `glob`)
- data types (`datetime`, `collections`, `array`)

These are not part of the Python language itself but can be used by importing
them. You can also be relatively certain they are available and will work
portably on most platforms.

The best way to learn about them is via the online documentation:
[The Python Standard Library](https://docs.python.org/3/library/index.html)

You've probably already used some of these modules:

```python
import random
import math
import string
from collections import Counter
```

## Packages

A package is a directory containing multiple modules, i.e., a directory of
Python files. Packages allow the structuring of code into a hierarchy rather
than a flat list of modules.

After importing a package, all of the contained modules are available by
prefixing the individual module with `package_name.`.

Packages are a way of structuring Python's namespace. As such, packages can
contain nested packages, not just modules.

Just like modules, packages are searched for using the directories contained in
the `sys.path` variable.

### `__init__.py` Files

In order for a directory to be considered a regular package, it must contain an
`__init__.py` file. This file can be empty, but any statements it contains will
be executed when the package is first imported.

**Note:** Packages can work without an explicit `__init__.py` (these are called
"namespace packages"), but **you should always have one** for clarity and to
maintain compatibility. See
[What's a Python Namespace Package, and What's It For?](https://realpython.com/python-namespace-package/)

### `__all__`

In order for wildcard imports (i.e., `from package_name import *`) to work, the
package itself must explicitly specify the index of the package.

This is done by populating the `__all__` variable in the `__init__.py` file.
This variable holds a list of all the module names that will be imported when
`from package import *` is used.

Example:

```python
# Contents of my_package/__init__.py
__all__ = ['module1', 'module2']
```

### Package Imports

In general, importing packages works similarly to modules.

A file `modu.py` in the directory `pack/` is imported with the statement:

```python
import pack.modu
```

This statement will look for an `__init__.py` file in the `pack` directory,
execute all of its top-level statements. Then it will look for a file named
`pack/modu.py` and execute all of its top-level statements. After these
operations, any variable, function, or class defined in `modu.py` is available
in the `pack.modu` namespace.

For importing deeply nested packages, it is often easier to bring the name into
the local namespace directly:

```python
import very.deep.module as mod
```

### Imports within a Package

Within a package, a module can be imported using the full or absolute name as
you would from outside the package.

Within a package, it is possible to import other modules in the same package
using the `from module import name` form of the import statement.

- `from . import name1`: Imports `name1` from the package of the current module
- `from .. import name2`: Imports `name2` from the parent package of the current
  module
- `from .sibling import name3`: Imports `name3` from a sibling module

**Relative imports (those starting with `.`) only work within packages and
cannot be used in scripts run directly.**

### A Worked Example: The `my_game` Package

Python packages can contain modules and other packages:

```
my_game/
├── constants.py
├── display/             # This is the PACKAGE display
│   ├── __init__.py
│   └── show_map.py      # It contains the MODULE show_map
├── logic/               # This is the PACKAGE logic
│   ├── __init__.py
│   ├── computer/        # It contains a PACKAGE computer
│   │   ├── __init__.py
│   │   └── aimbot.py    # Which contains a MODULE aimbot
│   │                    # This module has a FUNCTION shoot() in its code
│   ├── game.py          # This module belongs to the PACKAGE logic
│   └── win.py
└── main.py
```

### Importing Modules and Packages

You can import the whole package like you did with modules:

```python
import logic
```

And then use `.` to access submodules/packages:

```python
import logic

logic.computer.aimbot.shoot()  # In the PACKAGE logic
                               # Look for the PACKAGE computer
                               # And find the MODULE aimbot
                               # Run the FUNCTION shoot

logic.game.start()             # In the PACKAGE logic
                               # Look for the MODULE game
                               # Run the FUNCTION start
```

### Importing Subpackages

```python
import logic.game

logic.game.start()              # OK
logic.computer.aimbot.shoot()   # DOES NOT WORK (we only imported logic.game)
```

### Importing and Renaming

Can be convenient for long/complicated names:

```python
import logic.computer.aimbot as bot

bot.shoot()
```

### Absolute and Relative Imports

By default, Python will look for modules and packages:

- In the current folder
- In the folders of your virtual environment/Python installation

It is sometimes desirable to tell Python to look for modules and packages in
paths **relative** to the current module's path. In that case, you must import
the module/package by adding a `.` at the beginning.

**Relative imports are tricky. Use them only if you know what you are doing, or
in `__init__.py` files.**

### Using `__init__.py` to Allow Easier Access to Subpackages

When Python encounters an `import` statement and the symbol imported is a
package, the `__init__.py` file will automatically be run. This file can import
functions/variables from submodules and packages to allow for easier imports.

```
my_game/
├── logic/
│   ├── __init__.py
│   ├── constants/
│   │   ├── __init__.py
│   │   ├── player.py       # Contains NUMBER_PLAYERS = 10
│   │   └── bot.py          # Contains AIMBOT_PRECISION = 1.0
│   └── game.py
└── main.py
```

#### `logic/__init__.py`

```python
# filepath: logic/__init__.py
from .constants.player import NUMBER_PLAYERS
from .constants.bot import AIMBOT_PRECISION
```

#### `main.py`

```python
# filepath: main.py
from logic import NUMBER_PLAYERS

# Or even
from logic import NUMBER_PLAYERS, AIMBOT_PRECISION
```

### Packages and Paths

When running a Python program, the working directory is **the directory where**
**you ran the Python command**. This can have an effect when testing/developing
your programs.

```
my_project/
├── my_package/
│   ├── __init__.py
│   └── my_module.py
├── file.txt
└── main.py
```

```python
# filepath: my_package/my_module.py
# Contents of my_package/my_module.py
with open("file.txt", "r") as f:
    print(f.read())
```

Running from different locations:

- `python main.py`: WORKS (if main.py is in my_project/)
- `python -m my_package.my_module`: WORKS (preferred way when running from
  my_project/)
- `cd my_package`, then `python my_module.py`: DOES NOT WORK (there is no
  "file.txt" file in the my_package folder)

**Best Practice:** Always run Python from your project root and use
`python -m package.module` for modules within packages.

## External Packages: `PyPI` and `pip`

While the Python standard library is very expansive, there is also a huge set of
third-party software available via the Python Package Index (PyPI). This is like
an app store for Python.

`pip` is the standard tool for installing Python packages. (`uv` is a newer,
faster alternative. We will be using `uv` for the course)

Installing packages from PyPI using `pip` is as simple as:

    pip install package_name

The following are useful `pip` commands:

1. `pip install package_name`: Install a package
2. `pip uninstall package_name`: Uninstall a package
3. `pip list`: Lists currently installed packages
4. `pip show package_name`: Shows information about the specified installed
   package
5. `pip freeze`: Outputs installed packages in requirements format (useful for
   `requirements.txt`)
6. `pip install -r requirements.txt`: Install all packages listed in a
   requirements file

**Note:** `pip search` has been disabled on PyPI due to abuse. Use the PyPI
website to search instead.

## Import Guidelines

The [Python style guide (PEP 8)](https://www.python.org/dev/peps/pep-0008/) has
recommendations about imports:

1. Keep imports at the top of the file
2. Write imports on separate lines
3. Organize imports into groups: first standard library imports, then
   third-party imports, and finally local application or library imports
4. Order imports alphabetically within each group
5. Prefer absolute imports over relative imports
6. Avoid wildcard imports like `from module import *`

**Example of well-formatted imports:**

```python
# Standard library imports
import os
import sys
from pathlib import Path

# Third-party imports
import numpy as np
import pandas as pd

# Local application imports
from my_package import my_module
from my_package.utils import helper_function
```

## Common Pitfalls for Beginners

### 1. Circular Imports

Avoid having two modules import each other. This creates a circular dependency.

### 2. Shadowing Standard Library Names

Don't name your module `random.py` or `string.py` – you'll shadow the standard
library modules.

### 3. Modifying `sys.path` Unnecessarily

Usually not needed. Organize your code properly instead.

### 4. Running Modules from Wrong Directory

If your imports fail, check that you're running Python from the correct
directory (usually the project root).

### 5. Forgetting `__init__.py`

Without it, Python won't recognize your directory as a package.

## References

1. [The Python Tutorial: CH 6 Modules](https://docs.python.org/3/tutorial/modules.html)
2. [`pip` Documentation](https://pip.pypa.io/en/stable/)
3. [PyPI - the Python Package Index](https://pypi.python.org/pypi)
