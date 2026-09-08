"""
Simple logging setup module.

Configures logging and creates a global alias to the debug logger called 'log'.
This aids in visualizing the flow of imports and execution.
"""

# Setup Logging
import logging

logging.basicConfig(
    level=logging.DEBUG,
    format="{filename:<25} {module:<25} {funcName:<15} : {message}",
    style="{",
)  # Use new style string formatter

log = logging.getLogger(__name__).debug
