from enum import Enum


class CalendarEntryType(str, Enum):
    EMPLOYEESTARTING = "EmployeeStarting"
    EMPLOYEELEAVING = "EmployeeLeaving"
    EMPLOYEEABSENCE = "EmployeeAbsence"
    PAYDAY = "PayDay"
    EMPLOYEEBIRTHDAY = "EmployeeBirthday"
    EMPLOYEEWORKANNIVERSARY = "EmployeeWorkAnniversary"

    def __str__(self) -> str:
        return str(self.value)
