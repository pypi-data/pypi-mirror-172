from enum import Enum


class ReportCustomCssOption(str, Enum):
    USEDEFAULT = "UseDefault"
    APPENDTODEFAULT = "AppendToDefault"
    REPLACEDEFAULT = "ReplaceDefault"

    def __str__(self) -> str:
        return str(self.value)
