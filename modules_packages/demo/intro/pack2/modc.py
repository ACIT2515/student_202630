"""Module C within Package 2.

Used to demonstrate wildcard imports from a package.
"""

from log_setup import log

log(f"module __name__ = {__name__} : start")


def modcfunc():
    """Logs execution of function inside package 2 module C."""
    log("executing modcfunc")


log(f"module __name__ = {__name__} : end")
