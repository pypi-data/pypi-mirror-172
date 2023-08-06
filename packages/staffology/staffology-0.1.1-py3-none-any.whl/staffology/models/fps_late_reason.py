from enum import Enum


class FpsLateReason(str, Enum):
    NONEGIVEN = "NoneGiven"
    NOTIONALEXPAT = "NotionalExpat"
    NOTIONALERS = "NotionalErs"
    NOTIONALOTHER = "NotionalOther"
    CLASS1 = "Class1"
    MICROEMPLOYER = "MicroEmployer"
    NOREQUIREMENT = "NoRequirement"
    REASONABLEEXCUSE = "ReasonableExcuse"
    CORRECTION = "Correction"

    def __str__(self) -> str:
        return str(self.value)
