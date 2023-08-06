from enum import Enum


class BenefitDeclarationType(str, Enum):
    P11D = "P11D"
    PAYE = "Paye"

    def __str__(self) -> str:
        return str(self.value)
