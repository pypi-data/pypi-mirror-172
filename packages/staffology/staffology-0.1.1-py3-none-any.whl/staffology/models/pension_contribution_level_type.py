from enum import Enum


class PensionContributionLevelType(str, Enum):
    USERDEFINED = "UserDefined"
    STATUTORYMINIMUM = "StatutoryMinimum"
    NHS2015 = "Nhs2015"
    TP2020 = "Tp2020"

    def __str__(self) -> str:
        return str(self.value)
