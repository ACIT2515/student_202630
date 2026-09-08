"""Package 2 initialization.

Demonstrates the use of the __all__ variable to control which modules are
exposed when using: from pack2 import *
"""

from log_setup import log

# log("init start")
log(f"init __name__ = {__name__} : start")

__all__ = ["modc", "modd"]

log(f"init __name__ = {__name__} : end")
# log("init end")
