"""Simple module 2 for demonstration.

Demonstrates a module that imports another module (mod1) to show dependency chains.
"""

from log_setup import log

log(f"module __name__ = {__name__} : start")

import mod1  # intentionally not at the top of file


def mod2func():
    """Logs execution and calls a function from the imported mod1."""
    log("executing mod2func")
    mod1.mod1func()


log(f"module __name__ = {__name__} : end")
