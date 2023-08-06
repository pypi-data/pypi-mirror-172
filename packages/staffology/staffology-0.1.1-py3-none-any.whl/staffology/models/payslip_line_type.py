from enum import Enum


class PayslipLineType(str, Enum):
    BASICPAY = "BasicPay"
    GROSS = "Gross"
    NET = "Net"
    NIC = "Nic"
    TAX = "Tax"
    CIS = "Cis"

    def __str__(self) -> str:
        return str(self.value)
