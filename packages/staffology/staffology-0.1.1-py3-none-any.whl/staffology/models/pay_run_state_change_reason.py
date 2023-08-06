from enum import Enum


class PayRunStateChangeReason(str, Enum):
    OTHER = "Other"
    ADDITIONALDATANOTSUBMITTED = "AdditionalDataNotSubmitted"
    CHANGETOORIGINALDATA = "ChangeToOriginalData"
    PAYBUREAUERROR = "PayBureauError"

    def __str__(self) -> str:
        return str(self.value)
