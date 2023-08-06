from enum import Enum


class StarterDeclaration(str, Enum):
    A = "A"
    B = "B"
    C = "C"
    UNKNOWN = "Unknown"

    def __str__(self) -> str:
        return str(self.value)
