"""Module A within Package 1.

Demonstrates a module nested within a package directory.
"""

from log_setup import log

log(f"module __name__ = {__name__} : start")


def modafunc():
    """Logs execution of function inside package 1 module A."""
    log("executing modafunc")


log(f"module __name__ = {__name__} : end")
