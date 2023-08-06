from enum import Enum


class PayPeriodEventType(str, Enum):
    SUBMITFORPROCESSING = "SubmitForProcessing"
    SENDFORAPPROVAL = "SendForApproval"
    APPROVAL = "Approval"
    FINALISE = "Finalise"
    SENDPAYSLIP = "SendPaySlip"
    SUBMITRTI = "SubmitRti"

    def __str__(self) -> str:
        return str(self.value)
