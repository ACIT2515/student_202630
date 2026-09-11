# Virtual Environment: In Depth Explainer

## Purpose

Virtual environments are used to:

1. Avoid system pollution interfering with the operating system Python
   installation.
1. Avoid dependency conflicts between projects that require different versions
   of the same package.
1. Provide consistent, reproducible execution environments across development
   workstations, test runners, and production servers.

Python virtual environments create isolated execution environments for Python
projects. They allow you to manage Python versions and package dependencies
separately for each project and apart from any system-wide Python installation.

## Definition

A virtual environment is a self-contained directory tree that contains a Python
interpreter configuration for a particular version of Python, along with its own
isolated third-party packages. The directory contains:

1. `Scripts` directory (Windows) or `bin` directory (Unix-like systems) that
   contains the Python interpreter binary/shim and scripts installed in the
   virtual environment.
   1. `activate<shell specific extension>`: a script that modifies your shell's
      `PATH` environment variable to point to the virtual environment's Python
      and updates your prompt to show that the environment is active.
1. `Lib` directory (Windows) or `lib` directory (Unix-like systems) that
   contains the standard library and site packages.
   1. `Lib\site-packages` directory (Windows) or `lib/site-packages` directory
      (Unix-like systems) where third-party packages are installed.
   1. `include` directory that contains C headers for compiling Python C-extensions.
1. `pyvenv.cfg` configuration file stored in the root of the virtual environment
   directory. It is read by `site.py` during Python interpreter startup to
   configure module resolution. Key keys include:
   1. `home`: the path to the Python installation directory used to create the
      virtual environment.
   1. `include-system-site-packages`: boolean indicating whether system-wide
      `site-packages` are visible. Setting this to `false` enforces complete
      isolation.
   1. `version`: the Python version used in the virtual environment.
   1. `executable`: the path of the Python executable used to create the
      environment.
   1. `command`: the CLI command that generated the virtual environment.

## What Virtual Environments Change: Interpreter Startup and Module Search

When you run a Python executable inside a virtual environment or activate it in
your shell, Python's startup routine redirects where modules and packages are
discovered.

During startup, Python automatically loads the `site.py` module and executes
`site.main()`. This invokes `site.venv()`, which configures how the running
interpreter locates modules and packages.

Together, these routines set up the interpreter environment:

1. Adding site-specific paths to the `sys.path` list, enabling package discovery.
1. Setting the `site-packages` directory to the private folder within the virtual
   environment rather than the system-wide library path.
1. Inspecting `pyvenv.cfg` in the executable's directory or parent directory.
1. Evaluating `include-system-site-packages` to decide whether global packages
   should be appended to `sys.path`.
1. Setting `sys.base_prefix` and `sys.prefix`: in a virtual environment,
   `sys.base_prefix` points to the underlying Python installation, while
   `sys.prefix` points to the virtual environment folder.

Python resolves imported modules in the following order:

1. Built-in Modules: Compiled directly into the interpreter (such as `sys`).
1. Current Directory: The directory containing the executed script or current working directory.
1. `PYTHONPATH`: Directories explicitly defined in the `PYTHONPATH` environment variable.
1. Standard Library: Core Python standard library modules.
1. Third-Party Packages: The `site-packages` directory located under `sys.prefix`.

Virtual environments control this resolution order by modifying `sys.prefix` and
populating `sys.path` with the project's private `site-packages`.

## Virtual Environment Activation: `<virtual_env>/Scripts/activate`

The `activate` script prepares a shell session to use a virtual environment:

1. Modifies the `PATH` environment variable, placing the virtual environment's
   `Scripts` (Windows) or `bin` (Unix) folder first. Any subsequent `python` or
   CLI tool call resolves to the virtual environment's copy.
1. Sets the `VIRTUAL_ENV` environment variable to the path of the virtual
   environment folder.
1. Updates the prompt string to show the active environment name (for example,
   `(.venv)`).
1. Defines the `deactivate` function, which restores the prior `PATH`, removes
   `VIRTUAL_ENV`, and resets the shell prompt.

## How `uv` Manages Virtual Environments

Traditional Python tooling uses `venv` to create environments and `pip` to install
packages into them, requiring manual activation and external script management.
`uv` manages virtual environments as part of an integrated, declarative project
workflow.

### Automatic Environment Provisioning (`.venv`)

`uv` standardizes project environments around a `.venv` directory in the project
root:

1. Project commands (`uv run`, `uv add`, `uv sync`) automatically locate or
   create the `.venv` folder without requiring manual `python -m venv` commands.
1. `uv` writes a standard `pyvenv.cfg` file, making `.venv` fully compatible with
   standard Python tools, IDEs, and VS Code interpreter auto-detection.

### Python Version Provisioning and Toolchains

Unlike standard `venv`, which can only build virtual environments using Python
interpreters already installed on the host operating system:

1. `uv` can download, install, and manage standalone, isolated Python
   toolchains (for example, Python 3.14) on demand.
1. When running `uv venv --python 3.14` or defining `requires-python = ">=3.14"`
   in `pyproject.toml`, `uv` fetches the required Python binary directly into its
   managed toolchain cache and configures the virtual environment's `pyvenv.cfg`
   to use it.

### Declarative Synchronization vs Manual Mutations

In traditional `venv` + `pip` workflows:

1. Packages are installed imperatively with `pip install`, which can leave
   untracked or orphaned packages in `site-packages`.
1. Reproducing the environment on another machine relies on manually exported
   `requirements.txt` files.

In `uv` managed workflows:

1. Dependencies are declared in `pyproject.toml` and resolved into a
   deterministic `uv.lock` file containing exact versions and cryptographic
   hashes for all direct and transitive dependencies.
1. `uv sync` performs declarative reconciliation: it installs missing packages,
   updates changed dependencies, and removes extraneous packages from
   `.venv/Lib/site-packages` so the environment matches `uv.lock` exactly.

### Execution Without Shell Mutation (`uv run`)

While `.venv` includes traditional `activate` scripts for standard shell and IDE
use, `uv` eliminates the requirement to mutate the shell's `PATH`:

1. `uv run <command>` inspects the project root, verifies that `.venv` is up to
   date with `uv.lock`, and invokes the command with environment variables
   (`PATH`, `VIRTUAL_ENV`) configured specifically for that child process.
1. This ensures automated scripts, administrative tasks, and test runners execute
   in the correct isolated environment without relying on prior manual shell
   activation.

## References

1. [venv - Creation of virtual environments](https://docs.python.org/3/library/venv.html)
1. [uv Virtual Environments Documentation](https://docs.astral.sh/uv/concepts/environments/)
1. [How Virtual Environments Work](https://snarky.ca/how-virtual-environments-work/)
1. [The Python Tutorial - Modules](https://docs.python.org/3/tutorial/modules.html)
