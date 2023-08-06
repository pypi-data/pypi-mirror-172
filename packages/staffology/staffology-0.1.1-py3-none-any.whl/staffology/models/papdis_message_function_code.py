from enum import Enum


class PapdisMessageFunctionCode(str, Enum):
    ENROL = "Enrol"
    INFOONLY = "InfoOnly"
    ASSESSMENTREQUEST = "AssessmentRequest"
    ASSESSMENTRESPONSE = "AssessmentResponse"
    WOKERINSTRUCTION = "WokerInstruction"

    def __str__(self) -> str:
        return str(self.value)
