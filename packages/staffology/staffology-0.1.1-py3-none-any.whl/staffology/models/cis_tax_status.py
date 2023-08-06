from enum import Enum


class CISTaxStatus(str, Enum):
    GROSS = "Gross"
    NETOFSTANDARDDEDUCTION = "NetOfStandardDeduction"
    NETOFHIGHERDEDUCTION = "NetOfHigherDeduction"

    def __str__(self) -> str:
        return str(self.value)
