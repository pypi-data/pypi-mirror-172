from enum import Enum


class EmployeeStatus(str, Enum):
    CURRENT = "Current"
    FORMER = "Former"
    UPCOMING = "Upcoming"

    def __str__(self) -> str:
        return str(self.value)
