from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="StatutoryPay")


@attr.s(auto_attribs=True)
class StatutoryPay:
    """Part of the TaxYearConfig that our engine uses to calculate Statutory Pay.
    It is used internally when our engine performs calculations.
    You do not need to do anything with this model, it's provided purely for informational purposes.

        Attributes:
            weekly_parental_leave_amount (Union[Unset, float]): [readonly]
            weekly_sick_pay_amount (Union[Unset, float]): [readonly]
            awe_eligibility_threshold (Union[Unset, float]):
    """

    weekly_parental_leave_amount: Union[Unset, float] = UNSET
    weekly_sick_pay_amount: Union[Unset, float] = UNSET
    awe_eligibility_threshold: Union[Unset, float] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        weekly_parental_leave_amount = self.weekly_parental_leave_amount
        weekly_sick_pay_amount = self.weekly_sick_pay_amount
        awe_eligibility_threshold = self.awe_eligibility_threshold

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if weekly_parental_leave_amount is not UNSET:
            field_dict["weeklyParentalLeaveAmount"] = weekly_parental_leave_amount
        if weekly_sick_pay_amount is not UNSET:
            field_dict["weeklySickPayAmount"] = weekly_sick_pay_amount
        if awe_eligibility_threshold is not UNSET:
            field_dict["aweEligibilityThreshold"] = awe_eligibility_threshold

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        weekly_parental_leave_amount = d.pop("weeklyParentalLeaveAmount", UNSET)

        weekly_sick_pay_amount = d.pop("weeklySickPayAmount", UNSET)

        awe_eligibility_threshold = d.pop("aweEligibilityThreshold", UNSET)

        statutory_pay = cls(
            weekly_parental_leave_amount=weekly_parental_leave_amount,
            weekly_sick_pay_amount=weekly_sick_pay_amount,
            awe_eligibility_threshold=awe_eligibility_threshold,
        )

        return statutory_pay
