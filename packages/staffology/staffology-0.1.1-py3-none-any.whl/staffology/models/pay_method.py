from enum import Enum


class PayMethod(str, Enum):
    CASH = "Cash"
    CHEQUE = "Cheque"
    CREDIT = "Credit"
    DIRECTDEBIT = "DirectDebit"

    def __str__(self) -> str:
        return str(self.value)
