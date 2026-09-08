"""Module B within Package 1.

Demonstrates a module nested within a package directory.
"""

from log_setup import log

log(f"module __name__ = {__name__} : start")


def modbfunc():
    """Logs execution of function inside package 1 module B."""
    log("executing modbfunc")


log(f"module __name__ = {__name__} : end")
