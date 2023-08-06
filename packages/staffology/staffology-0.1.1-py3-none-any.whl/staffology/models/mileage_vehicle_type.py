from enum import Enum


class MileageVehicleType(str, Enum):
    CAR = "Car"
    MOTORCYCLE = "Motorcycle"
    CYCLE = "Cycle"

    def __str__(self) -> str:
        return str(self.value)
