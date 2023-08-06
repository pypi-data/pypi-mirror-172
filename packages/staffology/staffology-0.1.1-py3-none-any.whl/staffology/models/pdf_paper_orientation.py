from enum import Enum


class PdfPaperOrientation(str, Enum):
    LANDSCAPE = "Landscape"
    PORTRAIT = "Portrait"

    def __str__(self) -> str:
        return str(self.value)
