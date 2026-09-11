# Python Project Management: Virtual Environments and External Dependencies

## Why Projects Need Isolated Environments

Managing Python applications introduces challenges around how Python locates and
shares code. Virtual environments and dependency managers attempt to solve these
challenges. Understanding Python's library search path makes the connection
between these problems and their solution clear.

### System Pollution and Operating System Integrity

When an operating system installs Python, that interpreter is often used by
system utilities, package managers, and administration daemons. Installing
third-party libraries into this global Python installation pollutes the system
environment and risks breaking critical operating system tools when packages are
overwritten or upgraded.

### Conflicting Version Requirements Across Projects

Without environment isolation, every Python script on a computer shares a single
global `site-packages` directory (or maybe one for each user). If Project A requires
`pydantic>=2.0` and Project B relies on legacy syntax from `pydantic==1.10`,
installing or upgrading the library for one project inevitably breaks the other.

### Environment Drift and Reproducibility

In team environments and automated deployments, code that works on one user's
workstation must run identically on test servers and production hosts. If
dependencies are installed without explicit tracking , version discrepancies and
missing dependencies cause failures.

### Isolation and Project Management

Two tools resolve these challenges:

1. Virtual Environments: Isolated directory trees that provide a dedicated
   Python interpreter and private `site-packages` location for each project.
1. Dependency and Project Managers: Tools that track direct dependencies,
   resolve dependency trees, lock versions, and provision consistent Python
   runtimes.

## Running a program

- Python programs are plain text files, usually ending in `.py`
- You run one by typing a command in a terminal, e.g. `python my_file.py`
- What actually happens when you do this:
  1. The `python` command starts the Python **interpreter**
  2. The interpreter opens your file and reads it
  3. It executes the statements **from top to bottom, one at a time**
  4. Defining a function or class doesn't run its code - that only happens
     later, when the function/class is actually _called_
  5. When the last statement finishes (or the program hits an error), the
     interpreter exits and control returns to the terminal
- Which `python` actually runs depends on how Python is set up on your
  computer - this is one of the reasons we use virtual environments (see below)

- `python my_file.py` runs a script
- `python -m XXX` runs the module `XXX`, e.g. `python -m pytest` (same as
  running `pytest`)
- Extra passed arguments are available in `sys.argv`
- `sys.argv` always has at least one element: the script name itself

```python
import sys

print(sys.argv)
```

```bash
$ python my_script.py arg1 arg2 arg3
['my_script.py', 'arg1', 'arg2', 'arg3']
```

## Use the interactive Python shell

- `python -i file01.py` runs a script and keeps the interpreter open afterward -
  useful for testing functions interactively

```bash
$ python -i file01.py
Hello from file01!
>>> hello()
Hello.
```

## How Python Finds Packages

- When you write `import something`, Python has to search for it - the search
  order is stored in `sys.path`:
  1. Built-in modules (compiled into the interpreter, e.g. `sys`)
  2. The folder containing the script you're running
  3. Folders listed in the `PYTHONPATH` environment variable (if you've set
     one - most people haven't)
  4. The standard library (e.g. `os`, `json`, `datetime` - included with Python)
  5. Third-party packages installed with `pip`, which live in a `site-packages`
     folder
- You can see this search order yourself:

  ```python
  import sys
  print(sys.path)
  ```

- Without a virtual environment, there's usually only **one** `site-packages`
  folder for your whole computer or user, shared by every project. This causes
  problems:
  - Two projects that need different versions of the same library conflict with
    each other
  - Installing/upgrading a package for one project can break another project
- A virtual environment gives each project its **own** `site-packages` folder
  - Activating the environment changes `sys.path` (and what `python`/`pip` point
    to) so it uses that project's folder instead of the shared, computer-wide or
    per user one
  - That's why activation matters - it's what tells Python which `site-packages`
    to use

## Project Environment Approaches

Use one project folder and one virtual environment for each project, assignment,
or exercise. The following approaches both create isolated environments, but
`uv` also manages the project's Python version and dependencies.

### `uv`: Recommended Course Workflow

[`uv`](https://docs.astral.sh/uv/) is a fast, Python package and project manager
built in Rust by Astral. Unlike traditional workflows that combine separate
tools (`py`/`python3` for runtime discovery, `venv` for virtual environments,
and `pip` + `requirements.txt` for package installation), `uv` provides a tool
for Python project management.

#### Why Use a Project Manager Instead of Raw `pip` and `venv`?

Previous Python tools require manual coordination across multiple steps:

1. Creating and updating virtual environment folders manually.
1. Remembering to activate environments in each terminal session.
1. Managing unpinned or loosely pinned `requirements.txt` files that omit
   transitive (hidden) dependencies.
1. Installing and managing system-level Python versions manually when projects
   require different interpreters.

As an integrated project manager, `uv` automates these responsibilities:

1. **Declarative Project Configuration (`pyproject.toml`):** All project
   metadata, Python version constraints, direct dependencies, and development
   tools (such as `pytest`) is defined in standard `pyproject.toml` format.
1. **Deterministic Lockfiles (`uv.lock`):** `uv` resolves the full dependency
   graph and records exact package hashes and versions into `uv.lock`. This
   guarantees that identical dependencies are included.
1. **Python Version Management:** `uv` can automatically download, install, and
   pin specific Python interpreters (such as Python 3.14)
1. **Automated Virtual Environment Synchronization (`uv sync`):** `uv` creates
   and updates the project's `.venv` automatically so the installed libraries
   match `uv.lock`.
1. **Isolated Execution (`uv run`):** Commands run through `uv run`
   automatically execute inside the managed environment, eliminating common bugs
   caused by forgotting to activate your virtual environment.

#### Installing `uv`

Install `uv` once per computer (not per project):

1. Windows (PowerShell):
   `powershell -c "irm https://astral.sh/uv/install.ps1 | iex"` or
   `winget install --astral-sh.uv -e`
1. Linux/macOS: `curl -LsSf https://astral.sh/uv/install.sh | sh` or your OS
   package manager.
1. Verify the installation: `uv --version`

#### Creating and Managing a Project with `uv`

##### Initializing a Project

Run `uv init` inside your project directory to create a standardized project
structure with a `pyproject.toml` file:

```bash
$ uv init my_project
$ cd my_project
```

##### Adding and Removing Dependencies

Use `uv add` to declare project dependencies:

- Add a runtime library: `uv add requests`
- Add a development-only testing tool: `uv add --dev pytest`
- Remove a library: `uv remove requests`

Each modification updates `pyproject.toml`, refreshes `uv.lock`, and updates the
local `.venv` automatically.

##### Synchronizing an Existing Project

When cloning a repository or setting up a project on another machine:

```bash
$ uv sync
```

This reads `uv.lock` and ensures the local `.venv` contains the exact required
dependencies.

##### Running Code and Tools with `uv run`

`uv run` executes commands inside the project's virtual environment without
requiring manual script activation:

```bash
$ uv run python main.py
$ uv run pytest
```

#### Low-Level Virtual Environments with `uv venv`

When you only need a standalone virtual environment without a full project
manifest:

- `uv venv` creates a `.venv` directory in the current folder.
- `uv venv --python 3.14` creates a virtual environment using a specific Python
  version.
- Activate the environment in PowerShell via `.\.venv\Scripts\activate.ps1` or
  in Linux/macOS via `source .venv/bin/activate`.
- Use `uv pip install <package>` for accelerated package installation.

### Standard-Library `venv`: Low-Level Alternative

- `venv` is a module included in the Python Standard Library for managing
  virtual environments
- Creates a folder containing:
  - Scripts/binaries used to run Python
  - The libraries your project needs
- The folder is usually named `venv`
- You must **activate** the environment before using it
- Once active, use only `python` and `pip` - not `py` or `python3`

#### Creating a virtual environment with `venv`

- Create a folder for the course, e.g. `C:\Users\Tom\BCIT\ACIT2515`
- Open that folder in VS Code, then open a terminal
- Create the environment:
  - `py -m venv venv` (Windows)
  - `python3 -m venv venv` (Linux)
  - This creates a `venv` folder inside your project folder
  - Use a different name if you like: `py -m venv tim`

Create the virtual environment once, then just reuse it.

#### Activating the virtual environment with `venv`

- Activate it each time you work on the project:
  - `.\venv\Scripts\activate.bat` (Windows cmd)
  - `.\venv\Scripts\activate.ps1` (Windows PowerShell)
  - `source venv/bin/activate` (Linux/macOS)
- VS Code usually detects the environment and offers to activate it
  automatically - say yes
- When active, your prompt shows `(venv)`
- When active, run programs with just `python`
- You can Install packages with `pip install <package>`, e.g.
  `pip install pytest`
- Turn it off with `deactivate` - in practice, most people just close VS Code
  instead

#### Always

_open the project folder_ in VS Code (File > Open Folder). Don't right-click a
file and "Open with VS Code" - VS Code won't find your venv that way.

# Windows issues

- Activating a virtual environment runs a script, and Windows may block this for
  "security" reasons
- Read the error message on screen - it includes a link with more information
- Fix: allow local scripts to run, in PowerShell:
  - `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser`
- See the [Python documentation](https://docs.python.org/3/library/venv.html)
  and [Windows documentation](https://go.microsoft.com/fwlink/?LinkID=135170)

# Managing environments in VS Code

VS Code automatically finds virtual environments (`venv`, `uv`, Conda, ...)
inside your workspace folder, and treats them the same way regardless of which
tool created them.

### Selecting the environment

- The Status Bar (bottom of the window) shows the active environment
- To change it: click the Status Bar entry, or open the Command Palette
  (`Ctrl+Shift+P`) and run `Python: Select Interpreter`
- Pick the environment inside your project folder (e.g.
  `.\venv\Scripts\python.exe` or `.\.venv\Scripts\python.exe`)
- This is the environment used for running, debugging, and IntelliSense

### Running a program

- Click ▶ **Run Python File** (top-right of the editor), or right-click the
  editor and choose **Run Python File in Terminal**
- This opens a terminal, activates the selected environment, and runs
  `python your_file.py`

### Using the debugger

- Click in the left margin next to a line number to set a breakpoint
- Press `F5` (choose **Python File** the first time) to start debugging
- At a breakpoint you can inspect variables, step through code (`F10` step over,
  `F11` step into), and use the Debug Console
- The debugger uses whichever environment is currently selected

For more control, add a `.vscode/launch.json`:

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
      "args": ["arg1", "arg2"]
    }
  ]
}
```

- Use `"type": "debugpy"` (`"python"` is deprecated)
- `args` supplies command line arguments, same as `sys.argv`

### Using the integrated terminal

- Opening a new terminal (`` Ctrl+` ``) automatically activates the selected
  environment - look for `(venv)` or `(.venv)` in the prompt
- After switching environments, open a **new** terminal for the change to take
  effect

# References

1. [Virtual Environments](https://docs.python.org/3/library/venv.html)
2. [The Module Search Path](https://docs.python.org/3/tutorial/modules.html#the-module-search-path)
3. [How does python find packages?](https://leemendelowitz.github.io/blog/how-does-python-find-packages.html)
4. [uv: Using Python environments](https://docs.astral.sh/uv/pip/environments/)
5. [Mastering uv in VS Code](https://dev.to/lifeportal20002010/mastering-uv-in-vs-code-the-ultra-fast-python-setup-guide-2n56)
6. [Python environments in VS Code](https://code.visualstudio.com/docs/python/environments)
