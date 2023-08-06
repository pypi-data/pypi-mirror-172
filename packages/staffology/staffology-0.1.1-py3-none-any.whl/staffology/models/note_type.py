from enum import Enum


class NoteType(str, Enum):
    GENERAL = "General"
    NEWSTARTERSTATEMENT = "NewStarterStatement"
    RTWPROOF = "RtwProof"
    P45 = "P45"

    def __str__(self) -> str:
        return str(self.value)
