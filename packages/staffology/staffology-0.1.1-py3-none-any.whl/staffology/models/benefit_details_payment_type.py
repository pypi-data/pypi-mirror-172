from enum import Enum


class BenefitDetailsPaymentType(str, Enum):
    OTHER = "Other"
    SEASONTICKETS = "SeasonTickets"
    PRIVATECAREXPENSES = "PrivateCarExpenses"
    PRIVATEEDUCATION = "PrivateEducation"
    ACCOUNTANCYFEES = "AccountancyFees"
    DOMESTICBILLS = "DomesticBills"
    MULTIPLE = "Multiple"

    def __str__(self) -> str:
        return str(self.value)
