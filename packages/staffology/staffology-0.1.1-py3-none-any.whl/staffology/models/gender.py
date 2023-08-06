from enum import Enum


class Gender(str, Enum):
    MALE = "Male"
    FEMALE = "Female"

    def __str__(self) -> str:
        return str(self.value)
