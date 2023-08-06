from enum import Enum


class ProRataRule(str, Enum):
    WORKINGDAYSINPERIOD = "WorkingDaysInPeriod"
    TWOSIXTYRULE = "TwoSixtyRule"
    THREESIXFIVERULE = "ThreeSixFiveRule"

    def __str__(self) -> str:
        return str(self.value)
