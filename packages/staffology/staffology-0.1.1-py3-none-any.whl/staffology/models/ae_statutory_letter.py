from enum import Enum


class AeStatutoryLetter(str, Enum):
    B1 = "B1"
    B2 = "B2"
    B3 = "B3"
    B4 = "B4"

    def __str__(self) -> str:
        return str(self.value)
