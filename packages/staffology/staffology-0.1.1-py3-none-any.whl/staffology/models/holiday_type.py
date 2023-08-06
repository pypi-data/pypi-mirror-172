from enum import Enum


class HolidayType(str, Enum):
    DAYS = "Days"
    ACCRUAL_MONEY = "Accrual_Money"
    ACCRUAL_DAYS = "Accrual_Days"

    def __str__(self) -> str:
        return str(self.value)
