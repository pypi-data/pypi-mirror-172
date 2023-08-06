from enum import Enum


class PayBasis(str, Enum):
    HOURLY = "Hourly"
    DAILY = "Daily"
    MONTHLY = "Monthly"

    def __str__(self) -> str:
        return str(self.value)
