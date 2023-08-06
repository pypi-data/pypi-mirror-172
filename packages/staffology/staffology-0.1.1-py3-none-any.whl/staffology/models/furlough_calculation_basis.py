from enum import Enum


class FurloughCalculationBasis(str, Enum):
    ACTUALPAIDAMOUNT = "ActualPaidAmount"
    DAILYREFERENCEAMOUNT = "DailyReferenceAmount"
    MONTHLYREFERENCEAMOUNT = "MonthlyReferenceAmount"

    def __str__(self) -> str:
        return str(self.value)
