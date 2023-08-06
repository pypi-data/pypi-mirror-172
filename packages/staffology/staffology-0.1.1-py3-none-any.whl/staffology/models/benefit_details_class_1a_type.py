from enum import Enum


class BenefitDetailsClass1AType(str, Enum):
    OTHER = "Other"
    MULTIPLE = "Multiple"
    STOPLOSSCHARGES = "StopLossCharges"
    NONQUALIFYINGRELOCATIONBENEFIT = "NonQualifyingRelocationBenefit"
    EDUCATIONALASSITANCE = "EducationalAssitance"
    SUBSCRIPTIONSANDFEES = "SubscriptionsAndFees"

    def __str__(self) -> str:
        return str(self.value)
