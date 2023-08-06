from enum import Enum


class HtmlInsertionPoint(str, Enum):
    CREATEEMPLOYER = "CreateEmployer"
    EMPLOYEEDETAILS = "EmployeeDetails"

    def __str__(self) -> str:
        return str(self.value)
