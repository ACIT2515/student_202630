"""Simple module 3 for demonstration.

Exposes a function that can be aliased during import.
"""

from log_setup import log

log(f"module __name__ = {__name__} : start")


def mod3func():
    """Logs a message to trace execution."""
    log("executing mod3func")


log(f"module __name__ = {__name__} : end")
