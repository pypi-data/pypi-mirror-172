from enum import Enum


class TaxYear(str, Enum):
    YEAR2017 = "Year2017"
    YEAR2018 = "Year2018"
    YEAR2019 = "Year2019"
    YEAR2020 = "Year2020"
    YEAR2021 = "Year2021"
    YEAR2022 = "Year2022"

    def __str__(self) -> str:
        return str(self.value)
