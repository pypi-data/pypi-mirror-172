from enum import Enum


class AeUKWorker(str, Enum):
    NO = "No"
    YES = "Yes"
    ORDINARILY = "Ordinarily"

    def __str__(self) -> str:
        return str(self.value)
