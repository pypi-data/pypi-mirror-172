from enum import Enum


class PayeeType(str, Enum):
    EMPLOYEE = "Employee"
    HMRC = "Hmrc"
    PENSIONPROVIDER = "PensionProvider"
    AEO = "Aeo"
    DEDUCTION = "Deduction"

    def __str__(self) -> str:
        return str(self.value)
