from enum import Enum


class PayCodeCalculationType(str, Enum):
    FIXEDAMOUNT = "FixedAmount"
    PERCENTAGEOFGROSS = "PercentageOfGross"
    PERCENTAGEOFNET = "PercentageOfNet"
    MULTIPLEOFHOURLYRATE = "MultipleOfHourlyRate"
    MULTIPLEOFDAILYRATE = "MultipleOfDailyRate"

    def __str__(self) -> str:
        return str(self.value)
