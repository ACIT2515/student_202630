"""System checks that measure host resources and evaluate requirements."""

from abc import ABC, abstractmethod

import psutil
from check_result import CheckResult

# Add SystemCheck, DiskCheck, MemoryCheck, and create_check.
# Define SystemCheck before CPUCheck because CPUCheck inherits from it.


class CPUCheck(SystemCheck):
    """Check the number of logical CPUs."""

    name = "CPUs"

    def measure(self) -> int:
        """Return the logical CPU count."""
        return psutil.cpu_count()
