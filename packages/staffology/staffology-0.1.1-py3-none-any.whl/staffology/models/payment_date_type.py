from enum import Enum


class PaymentDateType(str, Enum):
    SAMEDATE = "SameDate"
    LASTDAY = "LastDay"
    LASTWEEKDAY = "LastWeekday"
    LASTXXXDAY = "LastXxxday"
    SAMEDATEWORKINGDAY = "SameDateWorkingDay"

    def __str__(self) -> str:
        return str(self.value)
