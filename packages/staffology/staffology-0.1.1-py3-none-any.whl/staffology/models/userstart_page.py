from enum import Enum


class UserstartPage(str, Enum):
    DASHBOARD = "Dashboard"
    EMPLOYERLIST = "EmployerList"
    EMPLOYEELIST = "EmployeeList"
    PAYROLL = "Payroll"
    RTI = "Rti"
    BUREAUDASHBOARD = "BureauDashboard"

    def __str__(self) -> str:
        return str(self.value)
