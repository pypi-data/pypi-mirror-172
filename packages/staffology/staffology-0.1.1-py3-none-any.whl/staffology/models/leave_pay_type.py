from enum import Enum


class LeavePayType(str, Enum):
    DONOTPAY = "DoNotPay"
    PAYASUSUAL = "PayAsUsual"
    STATUTORYPAY = "StatutoryPay"

    def __str__(self) -> str:
        return str(self.value)
