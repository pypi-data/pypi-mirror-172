from enum import Enum


class UserJobType(str, Enum):
    BUSINESSOWNER = "BusinessOwner"
    PAYROLLMANAGER = "PayrollManager"
    ACCOUNTANT = "Accountant"
    DEVELOPER = "Developer"
    SOFTWAREVENDOR = "SoftwareVendor"
    OTHER = "Other"

    def __str__(self) -> str:
        return str(self.value)
