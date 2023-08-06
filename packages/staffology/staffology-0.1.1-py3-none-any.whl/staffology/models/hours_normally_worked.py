from enum import Enum


class HoursNormallyWorked(str, Enum):
    LESSTHAN16 = "LessThan16"
    MORETHAN16 = "MoreThan16"
    MORETHAN24 = "MoreThan24"
    MORETHAN30 = "MoreThan30"
    NOTREGULAR = "NotRegular"

    def __str__(self) -> str:
        return str(self.value)
