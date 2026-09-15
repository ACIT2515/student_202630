# Lab: System Information Reporter with `uv` and `psutil`

## Overview

This lab introduces working with a third-party library using `uv`
You will create a small `uv` project, add the `psutil`
library as a dependency, and write functions that report live system
information: logged-in users, network adapters, and basic CPU/memory usage.

## Background: Why `psutil` Needs `uv add`

`platform`, `socket`, and `getpass` are part of the Python standard library:
they are always available, with no installation step. `psutil` is a
**third-party** library: it is not built into Python, so it must be added to
your project's dependencies and installed into your project's virtual
environment before you can import it.


## Structure

Create a solution directory `system_report` containing one module **per
function**, one smoke test file per module, plus a main script that imports
and combines them:

- `users.py` and `test_users.py`: the logged-in users function and its tests.
- `network.py` and `test_network.py`: the network adapters function and its
  tests.
- `resources.py` and `test_resources.py`: the CPU and memory usage function
  and its tests.
- `main.py`: imports the three functions above and combines their results.

Each of `users.py`, `network.py`, and `resources.py` must follow the
[Recommended Script Structure]():

- Keep the module root free of anything except imports and one function
  definition. Each fact must be obtainable by calling that function - not
  simply printed inline.
- These modules are libraries, not scripts: do not add a `main()` or an
  `if __name__ == "__main__":` guard to them.

`main.py` imports each function using the
[`from module_name import member`](../../../modules_packages/notes/modules_packages_imports.md#additional-import-forms)
form, for example:

```python
from users import get_logged_in_users
```

- Add a `main()` function to `main.py` that calls the imported functions and
  prints a combined system report.
- Call `main()` only from an `if __name__ == "__main__":` conditional at the
  bottom of `main.py`.

Document every function with a
[Google-style docstring]()
that includes `Args:` (if any) and `Returns:`.

## Design Requirements

The following pieces of information must each be retrievable by calling a
function:

| # | Information                                   | `psutil` function(s)    | Module file    |
| - | ---------------------------------------------- | ------------------------ | -------------- |
| 1 | Usernames currently logged in (no duplicates)   | `psutil.users()`         | `users.py`      |
| 2 | Network adapter names and their IPv4 addresses  | `psutil.net_if_addrs()`  | `network.py`    |
| 3 | Number of logical CPUs                          | `psutil.cpu_count()`     | `resources.py`  |
| 4 | Current memory usage as a percentage            | `psutil.virtual_memory()`| `resources.py`  |

## Part 0: Project Setup and Installing `psutil`

1. Create and enter a new project folder: `uv init system_report` then
   `cd system_report`.
2. Add `psutil` as a dependency: `uv add psutil`.
3. Add `pytest` as a development dependency: `uv add --dev pytest`.
4. Confirm the install worked by importing `psutil` in a quick REPL check:

   ```bash
   uv run python -c "import psutil; print(psutil.cpu_count())"
   ```

5. Look at `pyproject.toml`. Confirm `psutil` and `pytest` are listed as
   dependencies.

## Part 1: Logged-in Users

### Background

[`psutil.users()`](https://psutil.readthedocs.io/en/latest/#psutil.users)
returns a list of named tuples, one per logged-in session. Each tuple has a
`name` field with the username. The same user can appear more than once if
they have multiple sessions open.

### Usage Tutorial

```python
>>> import psutil
>>> psutil.users()
[suser(name='thomas_lane', terminal=None, host='0.0.0.0', started=..., pid=...)]
```

### Your Task

In `users.py`, write a function that returns the list of **unique** usernames
currently logged in (item 1). Use a `set` to remove duplicate names, then
convert the result to a `list` before returning it.

**Checkpoint:** Call your function directly (for example, in a REPL with
`uv run python -c "from users import get_logged_in_users; print(get_logged_in_users())"`)
and confirm it prints your own username before moving on.

### Write a Smoke Test

A smoke test calls the real function and checks only what is guaranteed true
on any machine (the return type and shape), not exact values. It needs no
mocking. In `test_users.py`:

```python
from users import get_logged_in_users


def test_get_logged_in_users_returns_list():
    result = get_logged_in_users()
    assert isinstance(result, list)


def test_get_logged_in_users_contains_only_strings():
    result = get_logged_in_users()
    assert all(isinstance(name, str) for name in result)


def test_get_logged_in_users_has_no_duplicates():
    result = get_logged_in_users()
    assert len(result) == len(set(result))
```

Run it with `uv run pytest test_users.py` and confirm all tests pass before
moving on.

## Part 2: Network Adapters

### Background

[`psutil.net_if_addrs()`](https://psutil.readthedocs.io/en/latest/#psutil.net_if_addrs)
returns a dictionary mapping each network adapter's name to a list of
address entries. Each address entry has a `family` field (use
`socket.AF_INET` for IPv4) and an `address` field.

### Usage Tutorial

```python
>>> import psutil
>>> import socket
>>> adapters = psutil.net_if_addrs()
>>> list(adapters.keys())
['Loopback Pseudo-Interface 1', 'Ethernet', 'Wi-Fi']
>>> for entry in adapters["Wi-Fi"]:
...     if entry.family == socket.AF_INET:
...         print(entry.address)
192.168.1.42
```

### Your Task

In `network.py`, write a function that returns a dictionary mapping each
adapter name to a list of its IPv4 addresses (item 2). Skip addresses whose
`family` is not `socket.AF_INET`. An adapter with no IPv4 address should map
to an empty list, not be skipped entirely.

**Checkpoint:** Print your function's result and confirm it lists at least
one adapter with your machine's IP address.

### Write a Smoke Test

In `test_network.py`:

```python
from network import get_network_adapters


def test_get_network_adapters_returns_dict():
    result = get_network_adapters()
    assert isinstance(result, dict)


def test_get_network_adapters_values_are_lists_of_strings():
    result = get_network_adapters()
    for addresses in result.values():
        assert isinstance(addresses, list)
        assert all(isinstance(address, str) for address in addresses)
```

Run it with `uv run pytest test_network.py` and confirm all tests pass before
moving on.

## Part 3: CPU and Memory Usage

### Background

[`psutil.cpu_count()`](https://psutil.readthedocs.io/en/latest/#psutil.cpu_count)
returns the number of logical CPUs.
[`psutil.virtual_memory()`](https://psutil.readthedocs.io/en/latest/#psutil.virtual_memory)
returns a named tuple that includes a `percent` field: the percentage of
memory currently in use.

### Usage Tutorial

```python
>>> import psutil
>>> psutil.cpu_count()
8
>>> psutil.virtual_memory().percent
54.3
```

### Your Task

In `resources.py`, write a function that returns a dictionary with two keys,
`"cpu_count"` and `"memory_percent"`, holding the values described above
(items 3-4).

**Checkpoint:** Print your function's result and confirm both values look
reasonable for your machine.

### Write a Smoke Test

In `test_resources.py`:

```python
from resources import get_system_resources


def test_get_system_resources_has_expected_keys():
    result = get_system_resources()
    assert set(result.keys()) == {"cpu_count", "memory_percent"}


def test_get_system_resources_cpu_count_is_positive_int():
    result = get_system_resources()
    assert isinstance(result["cpu_count"], int)
    assert result["cpu_count"] > 0


def test_get_system_resources_memory_percent_in_valid_range():
    result = get_system_resources()
    assert isinstance(result["memory_percent"], float)
    assert 0.0 <= result["memory_percent"] <= 100.0
```

Run it with `uv run pytest test_resources.py` and confirm all tests pass
before moving on.

## Part 4: Combine Everything in `main.py`

In `main.py`, import the three functions from `users`, `network`, and
`resources`, then write a `main()` function that calls each of them and
prints a readable report including all four pieces of information. For
example:

```text
System Report
========================================
Logged-in users: thomas_lane
Network adapters:
  Wi-Fi: 192.168.1.42
  Ethernet: (no IPv4 address)
Logical CPUs: 8
Memory used: 54.3%
```

Your exact formatting doesn't need to match this example, but the printed
report must include all four pieces of information.

Call `main()` only from `if __name__ == "__main__":` in `main.py`.

## Stretch Goal (Optional)

If you finish early, add a `disk.py` module with a fifth function that
reports disk usage for your main drive using
[`psutil.disk_usage()`](https://psutil.readthedocs.io/en/latest/#psutil.disk_usage),
import it into `main.py`, and include it in the report.

## Deliverables

- A `system_report` project containing:
  - `users.py`, `network.py`, and `resources.py`, each with one function
    covering the items in [Design Requirements](#design-requirements), with
    type annotations and a Google-style docstring.
  - `test_users.py`, `test_network.py`, and `test_resources.py`, each with
    passing smoke tests for its matching module.
  - A `main.py` file that imports each function and prints the combined
    system report.
  - An `if __name__ == "__main__":` guard in `main.py` that calls `main()`.
- A `pyproject.toml` listing `psutil` and `pytest` as dependencies.

## References

1. [psutil documentation](https://psutil.readthedocs.io/en/latest/)
4. [Google Python Style Guide: Comments and Docstrings](https://google.github.io/styleguide/pyguide.html#38-comments-and-docstrings)
