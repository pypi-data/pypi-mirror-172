from enum import Enum


class LinkedPiwResult(str, Enum):
    SUCCESS = "Success"
    NOLINKEDLEAVE = "NoLinkedLeave"

    def __str__(self) -> str:
        return str(self.value)
