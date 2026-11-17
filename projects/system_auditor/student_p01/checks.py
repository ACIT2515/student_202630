"""System checks that measure host resources and evaluate requirements."""

from abc import ABC, abstractmethod

import psutil

# Add create_check(), CheckResult, SystemCheck, DiskCheck, and MemoryCheck.
# SystemCheck must be defined above CPUCheck because CPUCheck inherits from it.


class CPUCheck(SystemCheck):
    """Check the number of logical CPUs."""

    def __init__(self, minimum_cpus: int, description: str) -> None:
        """Set the minimum logical CPU count and this check's description."""
        super().__init__("CPUs", minimum_cpus, description)

    def measure(self) -> int:
        """Return the logical CPU count."""
        return psutil.cpu_count()
