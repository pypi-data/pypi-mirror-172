from enum import Enum


class BackgroundTaskStatus(str, Enum):
    QUEUED = "Queued"
    SENT = "Sent"
    FAILED = "Failed"
    PROCESSING = "Processing"

    def __str__(self) -> str:
        return str(self.value)
