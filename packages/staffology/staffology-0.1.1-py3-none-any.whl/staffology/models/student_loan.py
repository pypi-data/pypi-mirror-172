from enum import Enum


class StudentLoan(str, Enum):
    NONE = "None"
    PLANONE = "PlanOne"
    PLANTWO = "PlanTwo"
    PLANFOUR = "PlanFour"

    def __str__(self) -> str:
        return str(self.value)
