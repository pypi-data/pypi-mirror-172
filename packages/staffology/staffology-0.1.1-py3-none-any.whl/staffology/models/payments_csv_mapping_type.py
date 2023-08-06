from enum import Enum


class PaymentsCsvMappingType(str, Enum):
    ROWBASED = "RowBased"
    COLUMNBASED = "ColumnBased"

    def __str__(self) -> str:
        return str(self.value)
