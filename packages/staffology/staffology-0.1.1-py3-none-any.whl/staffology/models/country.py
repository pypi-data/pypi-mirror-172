from enum import Enum


class Country(str, Enum):
    ENGLAND = "England"
    NORTHERNIRELAND = "NorthernIreland"
    SCOTLAND = "Scotland"
    WALES = "Wales"
    OUTSIDEUK = "OutsideUk"
    UK = "Uk"

    def __str__(self) -> str:
        return str(self.value)
