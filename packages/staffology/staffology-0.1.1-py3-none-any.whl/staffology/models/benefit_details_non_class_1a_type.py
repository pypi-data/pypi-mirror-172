from enum import Enum


class BenefitDetailsNonClass1AType(str, Enum):
    OTHER = "Other"
    MULTIPLE = "Multiple"
    LOANSWRITTENORWAIVED = "LoansWrittenOrWaived"
    NURSERYPLACES = "NurseryPlaces"
    EDUCATIONALASSITANCE = "EducationalAssitance"
    SUBSCRIPTIONSANDFEES = "SubscriptionsAndFees"

    def __str__(self) -> str:
        return str(self.value)
