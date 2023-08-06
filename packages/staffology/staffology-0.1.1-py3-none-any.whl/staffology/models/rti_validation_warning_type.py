from enum import Enum


class RtiValidationWarningType(str, Enum):
    MISSINGADDRESS = "MissingAddress"
    MISSINGNINO = "MissingNiNo"

    def __str__(self) -> str:
        return str(self.value)
