from enum import Enum


class AeStatus(str, Enum):
    ELIGIBLE = "Eligible"
    NONELIGIBLE = "NonEligible"
    ENTITLED = "Entitled"
    NODUTIES = "NoDuties"

    def __str__(self) -> str:
        return str(self.value)
