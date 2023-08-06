from enum import Enum


class ExternalEmployeeMappingStatus(str, Enum):
    UNMAPPED = "Unmapped"
    MAPPED = "Mapped"
    IGNORED = "Ignored"
    IMPORT = "Import"

    def __str__(self) -> str:
        return str(self.value)
