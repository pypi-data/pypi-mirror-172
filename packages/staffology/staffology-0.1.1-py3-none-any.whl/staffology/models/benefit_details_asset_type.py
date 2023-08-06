from enum import Enum


class BenefitDetailsAssetType(str, Enum):
    OTHER = "Other"
    MULTIPLE = "Multiple"
    PROPERTY = "Property"
    CARS = "Cars"
    PRECIOUSMETALS = "PreciousMetals"

    def __str__(self) -> str:
        return str(self.value)
