#! /usr/bin/env python3
"""Simple module to demonstrate module include processing.

Attributes:
    mod1_global (str): Example of a module level variable.
"""
from log_setup import log

# Log module load start
log(f"module __name__ = {__name__} : start")

mod1_global = "mod1 global variable"


def mod1func():
    """Basic demonstration module level function.

    Logs invocations to trace execution flow.
    """
    log("executing mod1func")


if __name__ == "__main__":
    # If executed as script simply invoke mod1func
    mod1func()


# Log module load end
log(f"module __name__ = {__name__} : end")
