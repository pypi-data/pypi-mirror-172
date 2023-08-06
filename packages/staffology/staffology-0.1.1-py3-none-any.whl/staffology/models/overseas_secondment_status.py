from enum import Enum


class OverseasSecondmentStatus(str, Enum):
    MORETHAN183DAYS = "MoreThan183Days"
    LESSTHAN183DAYS = "LessThan183Days"
    BOTHINANDOUTOFUK = "BothInAndOutOfUK"

    def __str__(self) -> str:
        return str(self.value)
