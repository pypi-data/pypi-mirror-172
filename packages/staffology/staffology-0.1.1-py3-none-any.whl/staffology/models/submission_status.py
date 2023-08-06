from enum import Enum


class SubmissionStatus(str, Enum):
    NOTSUBMITTED = "NotSubmitted"
    SUBMITTED = "Submitted"
    ERRORRESPONSE = "ErrorResponse"
    ACCEPTED = "Accepted"

    def __str__(self) -> str:
        return str(self.value)
