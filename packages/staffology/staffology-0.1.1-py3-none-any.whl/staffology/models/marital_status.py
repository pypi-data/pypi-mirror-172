from enum import Enum


class MaritalStatus(str, Enum):
    SINGLE = "Single"
    MARRIED = "Married"
    DIVORCED = "Divorced"
    WIDOWED = "Widowed"
    CIVILPARTNERSHIP = "CivilPartnership"
    UNKNOWN = "Unknown"

    def __str__(self) -> str:
        return str(self.value)
