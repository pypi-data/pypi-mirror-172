from enum import Enum


class ExternalDataProviderType(str, Enum):
    PENSIONSCHEMES = "PensionSchemes"
    ACCOUNTING = "Accounting"
    PAYMENTS = "Payments"
    HR = "Hr"
    TIMEANDATTENDANCE = "TimeAndAttendance"
    EMPLOYEEPORTAL = "EmployeePortal"

    def __str__(self) -> str:
        return str(self.value)
