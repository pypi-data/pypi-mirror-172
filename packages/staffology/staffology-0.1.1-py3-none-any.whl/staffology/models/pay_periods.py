from enum import Enum


class PayPeriods(str, Enum):
    CUSTOM = "Custom"
    MONTHLY = "Monthly"
    FOURWEEKLY = "FourWeekly"
    FORTNIGHTLY = "Fortnightly"
    WEEKLY = "Weekly"
    DAILY = "Daily"

    def __str__(self) -> str:
        return str(self.value)
