"""Package 1 initialization.

Marks the 'pack1' directory as a Python package.
Code here runs when the package is imported.
"""

from log_setup import log

# log("init start")
log(f"init __name__ = {__name__} : start")

log(f"init __name__ = {__name__} : end")
# log("init end")
