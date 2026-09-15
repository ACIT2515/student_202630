# Directed Reading Answers: Virtual Environments and Dependencies

## Question 1: Global Python Packages

### Question

Why can installing a third-party package into the system-wide Python
installation cause problems for other projects or operating system tools?

### Answer

A system-wide Python installation is often shared by operating system
utilities, package managers, and administration daemons, and by every Python
project on the computer. Installing or upgrading a third-party package there
changes the one shared `site-packages` folder that all of them use. If a
system tool depends on a specific package version, overwriting it can break
that tool. Likewise, if one project needs `pydantic>=2.0` and another needs
`pydantic==1.10`, they cannot both be satisfied by a single shared
installation, so installing or upgrading the package for one project breaks
the other.

## Question 2: Virtual Environment Isolation

### Question

What does a virtual environment give each Python project its own copy of?

### Answer

A virtual environment gives each project its own `site-packages` folder (and
its own Python interpreter reference). Activating the environment changes
`sys.path` so that `python` and `pip` use that project's private folder
instead of the shared, computer-wide or per-user one, which is what keeps each
project's installed packages isolated from every other project.

## Question 3: Managing a Project with `uv`

### Question

Which `uv` command installs the dependencies recorded in `pyproject.toml` and
`uv.lock` when you clone a project?

### Answer

`uv sync`. It reads `uv.lock` and ensures the local `.venv` contains exactly
the dependencies and versions recorded there.
