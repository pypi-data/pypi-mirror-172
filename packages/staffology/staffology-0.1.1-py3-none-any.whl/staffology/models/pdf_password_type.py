from enum import Enum


class PdfPasswordType(str, Enum):
    INITIALSANDDOB = "InitialsAndDob"
    NINUMBER = "NiNumber"
    CUSTOM = "Custom"

    def __str__(self) -> str:
        return str(self.value)
