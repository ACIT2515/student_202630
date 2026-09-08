"""Module D within Package 2.

Demonstrates that modules inside packages behave like regular modules.
"""

from log_setup import log

log(f"module __name__ = {__name__} : start")


def moddfunc():
    """Logs execution of function inside package 2 module D."""
    log("executing moddfunc")


log(f"module __name__ = {__name__} : end")
