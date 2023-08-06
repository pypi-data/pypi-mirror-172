from enum import Enum


class LeaveType(str, Enum):
    UNAUTHORISED = "Unauthorised"
    HOLIDAY = "Holiday"
    SICK = "Sick"
    MATERNITY = "Maternity"
    PATERNITY = "Paternity"
    ADOPTION = "Adoption"
    SHAREDPARENTAL = "SharedParental"
    BEREAVEMENT = "Bereavement"
    SHAREDPARENTALADOPTION = "SharedParentalAdoption"
    PATERNITYADOPTION = "PaternityAdoption"

    def __str__(self) -> str:
        return str(self.value)
