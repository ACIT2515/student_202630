# SysInfo Reporter

## Overview

**SysInfo Reporter** is a small, read-only script that gathers and prints a
summary of the local host: its operating system, computer name, and current
user. You will design and write your own functions to gather this
information, then combine their results in `main()`.

This is an introductory exercise. It focuses on:

- Designing simple function interfaces: choosing meaningful names,
  parameters, and return types for a well-defined task.
- Writing small, single-purpose functions with **type annotations** and
  **Google-style docstrings**.
- Using three standard library modules to inspect the local machine:
  `platform`, `socket`, and `getpass`.
- Organizing a script using the
  [Recommended Script Structure](../../subjects/modules_packages/notes/modules_packages_imports.md#recommended-script-structure).

## Learning Objectives

By completing this exercise, you will be able to:

1. Explain what each piece of reported host information means.
2. Use `platform`, `socket`, and `getpass` from the standard libary to read information about
   the local machine.
3. Design function names, parameters, and return types for a small,
   well-defined task.
4. Write functions with type annotations, and Google-style docstrings
5. Organize a script as a collection of functions with a single `main()`
   entry point.

## Background: What Identifies a Host?

A "host" is any computer connected to a network. When you inspect or manage a
host (your own machine, or one you administer), a few basic facts identify
and describe it:

- **Computer name (hostname)**: The name the machine is known by on a
  network. Two computers on the same network usually have different
  hostnames.
- **Operating system**: The system software running the machine (e.g.
  Windows, macOS, Linux), along with its version and the CPU architecture
  it's running on (e.g. `AMD64`, `arm64`).
- **Current user**: The username of the person currently logged in and
  running the script. A single machine can have several user accounts.

You will design and write functions to gather each of these facts; see
[Design Requirements](#design-requirements) for what must be retrievable.

**A note on privileges:** every module used in this exercise reads
information that is already visible to a normal, non-administrator user.
Nothing in this exercise requires "Run as Administrator" (Windows) or `sudo`
(macOS/Linux). 

## Structure

Create a solution directory `sysinfo_reporter`.

Create a file called `sysinfo_reporter.py`.

Your file must follow the
[Recommended Script Structure](../../subjects/modules_packages/notes/modules_packages_imports.md#recommended-script-structure):

- Design one or more functions to retrieve every piece of
  information listed in [Design Requirements](#design-requirements) must be
  obtainable by calling a function that returns it - not simply printed
  inside `main()`.
- Keep the module root free of anything except imports and function
  definitions.
- You choose the function names, parameters, and return types. A single
  function may return several related facts (for example, as a `dict`), or
  you may write one function per fact - either is acceptable.
- Add a `main()` function that calls the functions you designed and prints
  a combined host summary.
- Call `main()` only from an `if __name__ == "__main__":` conditional at the
  bottom of the file.
- Import `getpass` using an alias: `import getpass as gp`. Use `gp` (not
  `getpass`) everywhere you call its functions.

Document every function with a
[Google-style docstring](../../subjects/docstrings_type_annotations/notes/docstrings_type_annotations.md)
that includes `Args:` (if any), `Returns:`, and an `Examples:` section. 

## Design Requirements

The following pieces of information must each be retrievable: 
it:

| # | Information | Source module |
| - | ----------- | -------------- |
| 1 | Operating system name (e.g., `'Windows'`) | `platform` |
| 2 | Operating system release (e.g., `'11'`) | `platform` |
| 3 | Machine / CPU architecture (e.g., `'AMD64'`) | `platform` |
| 4 | Computer name (hostname) | `socket` |
| 5 | IP address for that hostname | `socket` |
| 6 | Current logged-in username | `getpass` |

## Part 1: Operating System Information - `platform`

### Background: the `platform` module

The [`platform`](https://docs.python.org/3/library/platform.html) module
reads information about the underlying platform your Python interpreter is
running on: the operating system, its version, and the machine's CPU
architecture. It does this by reading values that the operating system
already exposes (such as environment variables and system calls that return
public information), so no special permission is required.

Useful functions:

| Function | Returns | Example |
| --- | --- | --- |
| [`platform.system()`](https://docs.python.org/3/library/platform.html#platform.system) | The OS name | `'Windows'`, `'Linux'`, `'Darwin'` |
| [`platform.release()`](https://docs.python.org/3/library/platform.html#platform.release) | The OS release | `'11'`, `'6.8.0-40-generic'` |
| [`platform.version()`](https://docs.python.org/3/library/platform.html#platform.version) | The detailed OS version string | `'10.0.22631'` |
| [`platform.machine()`](https://docs.python.org/3/library/platform.html#platform.machine) | The machine's CPU architecture | `'AMD64'`, `'arm64'` |

### Usage Tutorial

```python
>>> import platform
>>> platform.system()
'Windows'
>>> platform.machine()
'AMD64'
```

Try this in a Python REPL on your own machine - the values you see will
depend on your OS and hardware.

### Your Task

Write one or more functions, using the `platform` functions above, so that
the operating system name, release, and machine architecture (items 1-3 in
[Design Requirements](#design-requirements)) can each be retrieved by
calling a function.

## Part 2: Computer Name - `socket`

### Background: the `socket` module

The [`socket`](https://docs.python.org/3/library/socket.html) module
provides low-level networking operations. For this exercise, you only need
two of its functions: one to find the local computer's name, and one to
resolve that name to an IP address. Both simply read information your
computer already knows about itself; neither requires elevated permissions
or contacts a remote server for the local hostname lookup.

| Function | Returns | Notes |
| --- | --- | --- |
| [`socket.gethostname()`](https://docs.python.org/3/library/socket.html#socket.gethostname) | The local computer's hostname | Same name you'd see in your OS's network settings |
| [`socket.gethostbyname(hostname)`](https://docs.python.org/3/library/socket.html#socket.gethostbyname) | The IP address for a given hostname | Raises `socket.gaierror` if the name can't be resolved |

### Usage Tutorial

```python
>>> import socket
>>> name = socket.gethostname()
>>> name  
'my-laptop'
>>> socket.gethostbyname(name)  
'192.168.1.42'
```

### Your Task

Write one or more functions, using `socket.gethostname()` and
`socket.gethostbyname()`, so that the computer's hostname and its IP
address (items 4-5) can each be retrieved by calling a function. If the
hostname cannot be resolved to an IP address, handle the
`socket.gaierror` exception rather than letting it crash your program.

## Part 3: Current User - `getpass`

### Background: the `getpass` module

The [`getpass`](https://docs.python.org/3/library/getpass.html) module is
best known for `getpass.getpass()`, which reads a password without echoing
it to the screen. This exercise instead uses
[`getpass.getuser()`](https://docs.python.org/3/library/getpass.html#getpass.getuser),
which simply returns the login name of the user running the script, read
from an environment variable (or the OS user database). It does not prompt
for a password and does not require any special permission.

### Usage Tutorial

```python
>>> import getpass
>>> getpass.getuser()  # doctest: +SKIP
'thomas_lane'
```

### Your Task

Import `getpass` using the alias `gp` (`import getpass as gp`), then write
a function, using `gp.getuser()`, that returns the current username
(item 6).

## Part 4: Combine Everything in `main()`

Write a `main()` function that calls the functions you designed for Parts
1-3, then prints a readable host summary that includes all six pieces of
information listed in [Design Requirements](#design-requirements). For
example:

```text
Host Summary
========================================
Computer name: my-laptop
IP address:    192.168.1.42
Operating system: Windows 11
Machine type:  AMD64
Current user:  thomas_lane
```

Your exact formatting, function names, and return types don't need to match
this example, but the printed summary must include all six pieces of
information: OS name, OS release, machine type, hostname, IP address, and
current user.

Call `main()` only from `if __name__ == "__main__":`, so importing your
module does not print anything.

## Deliverables

- A `sysinfo_reporter.py` file in your `sysinfo_reporter` solution
  directory containing:
  - Functions that get all six pieces of information in
    [Design Requirements](#design-requirements), each with type
    annotations and a Google-style docstring (including an `Examples:`
    doctest).
  - A `main()` function that prints the combined host summary.
  - An `if __name__ == "__main__":` guard that calls `main()`.

## References

1. [`platform` - Access to underlying platform's identifying data](https://docs.python.org/3/library/platform.html)
2. [`socket` - Low-level networking interface](https://docs.python.org/3/library/socket.html)
3. [`getpass` - Portable password input](https://docs.python.org/3/library/getpass.html)
4. [Recommended Script Structure](../../subjects/modules_packages/notes/modules_packages_imports.md#recommended-script-structure)
5. [Google Python Style Guide: Comments and Docstrings](https://google.github.io/styleguide/pyguide.html#38-comments-and-docstrings)
