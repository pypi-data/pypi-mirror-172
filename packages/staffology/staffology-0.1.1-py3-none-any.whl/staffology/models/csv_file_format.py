from enum import Enum


class CsvFileFormat(str, Enum):
    MONEYSOFTEMPLOYEES = "MoneysoftEmployees"
    BRIGHTPAYEMPLOYEES = "BrightPayEmployees"
    FPS = "Fps"
    SAGEEMPLOYEEDETAILS = "SageEmployeeDetails"
    ACCESSPEOPLEPLANNER = "AccessPeoplePlanner"
    EMPLOYEECSV = "EmployeeCsv"

    def __str__(self) -> str:
        return str(self.value)
