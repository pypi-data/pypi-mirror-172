from enum import Enum


class Role(str, Enum):
    ADMIN = "Admin"
    EDITOR = "Editor"
    REVIEWER = "Reviewer"
    PAYROLLCLIENT = "PayrollClient"

    def __str__(self) -> str:
        return str(self.value)
