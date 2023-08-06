from enum import Enum


class CISSubContractorType(str, Enum):
    SOLETRADER = "SoleTrader"
    PARTNERSHIP = "Partnership"
    COMPANY = "Company"
    TRUST = "Trust"

    def __str__(self) -> str:
        return str(self.value)
