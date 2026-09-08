#! /usr/bin/env python3
"""Demonstration of Python modules, packages, and import syntax.

This script serves as a practical example for students to understand how
Python code is structured across multiple files (modules) and directories
(packages), and the various ways to import functionality.
"""
# used to demonstrate reloading of a module
import importlib

# Setup Logging
from log_setup import log

# this is intentionally before imports so logging of imports is noted
log(f"module __name__ = {__name__} : start")

# --- Import Examples ---

# 1. Basic Import: Imports the entire module. Access via 'mod1.func()'
import mod1

# 5. Package Import: Imports a module nested inside a package.
#    Must access via full path: 'pack1.moda.modafunc()'
import pack1.moda

# 2. From Import: Imports a specific variable directly into local namespace.
from mod1 import mod1_global

# 3. From Import: Imports a specific function.
from mod2 import mod2func

# 4. Aliasing: Imports a function but gives it a new local name.
#    Useful for resolving naming conflicts or shortening long names.
from mod3 import mod3func as myfunc

# 6. From Package Import: Imports a specific function from a submodule.
from pack1.modb import modbfunc

# 7. Wildcard Import: Imports everything defined in pack2's __init__.py.
#    Generally discouraged in production code as it clouds the namespace.
from pack2 import *


def main():
    """Executes the demonstration of module and package usage.

    Calls functions from various imported modules to show they are accessible.
    Also demonstrates module reloading.
    """
    log("function start")

    # Call function accessing via module name prefix
    mod1.mod1func()

    # Call function imported directly into namespace
    mod2func()

    # Call function access via alias
    myfunc()

    # Call function accessing via package hierarchy
    pack1.moda.modafunc()

    # Call function imported directly from submodule
    modbfunc()

    # Call functions imported via wildcard (*) from pack2
    modc.modcfunc()
    modd.moddfunc()

    # Reload the module (useful during development if code changes)
    importlib.reload(mod1)

    log(f"Imported global = {mod1_global}")
    log("function end")


if __name__ == "__main__":
    main()

log(f"module __name__ = {__name__} : end")
