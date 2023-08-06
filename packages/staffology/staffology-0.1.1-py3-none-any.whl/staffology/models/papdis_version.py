from enum import Enum


class PapdisVersion(str, Enum):
    PAP10 = "PAP10"
    PAP11 = "PAP11"

    def __str__(self) -> str:
        return str(self.value)
