from enum import Enum


class WebhookEvent(str, Enum):
    EMPLOYEE_CREATED = "Employee_Created"
    EMPLOYEE_UPDATED = "Employee_Updated"
    EMPLOYEE_DELETED = "Employee_Deleted"
    PAYRUN_FINALISED = "Payrun_Finalised"

    def __str__(self) -> str:
        return str(self.value)
