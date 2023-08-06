from enum import Enum


class AverageWeeklyEarningsResult(str, Enum):
    SUCCESS = "Success"
    EARNINGSBELOWTHRESHOLD = "EarningsBelowThreshold"
    NOTENOUGHPAYROLLDATA = "NotEnoughPayrollData"
    TAXYEARNOTSUPPORTED = "TaxYearNotSupported"

    def __str__(self) -> str:
        return str(self.value)
