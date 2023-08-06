from enum import Enum


class PensionRule(str, Enum):
    RELIEFATSOURCE = "ReliefAtSource"
    SALARYSACRIFICE = "SalarySacrifice"
    NETPAYARRANGEMENT = "NetPayArrangement"

    def __str__(self) -> str:
        return str(self.value)
