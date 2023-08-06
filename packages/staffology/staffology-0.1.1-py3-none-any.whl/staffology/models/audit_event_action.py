from enum import Enum


class AuditEventAction(str, Enum):
    ADDED = "Added"
    EDITED = "Edited"
    DELETED = "Deleted"

    def __str__(self) -> str:
        return str(self.value)
