from enum import Enum


class DpsDataType(str, Enum):
    P6 = "P6"
    P9 = "P9"
    SL1 = "SL1"
    SL2 = "SL2"
    PGL1 = "PGL1"
    PGL2 = "PGL2"
    AR = "AR"
    NOT = "NOT"
    RTI = "RTI"
    CIS = "CIS"

    def __str__(self) -> str:
        return str(self.value)
