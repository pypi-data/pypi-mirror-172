from enum import Enum


class DeferalPeriodType(str, Enum):
    DAYS = "Days"
    WEEKS = "Weeks"
    MONTHS = "Months"
    PAYPERIODS = "PayPeriods"

    def __str__(self) -> str:
        return str(self.value)
