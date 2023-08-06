from enum import Enum


class BankHolidayCollection(str, Enum):
    NONE = "None"
    ENGLANDANDWALES = "EnglandAndWales"
    SCOTLAND = "Scotland"
    NORTHERNIRELAND = "NorthernIreland"

    def __str__(self) -> str:
        return str(self.value)
