from enum import Enum


class PdfPaperSize(str, Enum):
    LETTER = "Letter"
    LETTERSMALL = "LetterSmall"
    A4 = "A4"
    A4SMALL = "A4Small"
    A5 = "A5"

    def __str__(self) -> str:
        return str(self.value)
