from enum import Enum


class BenefitDetailsCarPowerType(str, Enum):
    DIESEL6D = "Diesel6d"
    DIESELNON6D = "DieselNon6d"
    PETROL = "Petrol"
    HYBRID = "Hybrid"
    ELECTRIC = "Electric"

    def __str__(self) -> str:
        return str(self.value)
