from enum import Enum


class AeAction(str, Enum):
    NOCHANGE = "NoChange"
    ENROL = "Enrol"
    EXIT = "Exit"
    INCONCLUSIVE = "Inconclusive"
    POSTPONE = "Postpone"
    REENROL = "ReEnrol"

    def __str__(self) -> str:
        return str(self.value)
