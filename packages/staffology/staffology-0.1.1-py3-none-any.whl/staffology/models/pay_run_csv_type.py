from enum import Enum


class PayRunCsvType(str, Enum):
    SUMMARY = "Summary"
    LINES = "Lines"
    PAYROLLCODEANDNAMEONLY = "PayrollCodeAndNameOnly"
    COLUMNCSVMAPPING = "ColumnCsvMapping"

    def __str__(self) -> str:
        return str(self.value)
