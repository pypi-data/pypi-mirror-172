from enum import Enum


class PayRunState(str, Enum):
    OPEN = "Open"
    SUBMITTEDFORPROCESSING = "SubmittedForProcessing"
    PROCESSING = "Processing"
    AWAITINGAPPROVAL = "AwaitingApproval"
    APPROVED = "Approved"
    FINALISED = "Finalised"

    def __str__(self) -> str:
        return str(self.value)
