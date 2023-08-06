from enum import Enum


class PayCodeMultiplierType(str, Enum):
    NONE = "None"
    HOURS = "Hours"
    DAYS = "Days"

    def __str__(self) -> str:
        return str(self.value)
