from enum import Enum


class RtiSenderType(str, Enum):
    ACTINGINCAPACITY = "ActingInCapacity"
    AGENT = "Agent"
    BUREAU = "Bureau"
    COMPANY = "Company"
    EMPLOYER = "Employer"
    GOVERNMENT = "Government"
    INDIVIDUAL = "Individual"
    OTHER = "Other"
    PARTNERSHIP = "Partnership"
    TRUST = "Trust"

    def __str__(self) -> str:
        return str(self.value)
