from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="LoanCharge")


@attr.s(auto_attribs=True)
class LoanCharge:
    """Part of the TaxYearConfig that our engine uses to calculate charges for a Loan.
    It is used internally when our engine performs calculations.
    You do not need to do anything with this model, it's provided purely for informational purposes.

        Attributes:
            threshhold (Union[Unset, float]):
            official_interest_rate (Union[Unset, float]):
    """

    threshhold: Union[Unset, float] = UNSET
    official_interest_rate: Union[Unset, float] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        threshhold = self.threshhold
        official_interest_rate = self.official_interest_rate

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if threshhold is not UNSET:
            field_dict["threshhold"] = threshhold
        if official_interest_rate is not UNSET:
            field_dict["officialInterestRate"] = official_interest_rate

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        threshhold = d.pop("threshhold", UNSET)

        official_interest_rate = d.pop("officialInterestRate", UNSET)

        loan_charge = cls(
            threshhold=threshhold,
            official_interest_rate=official_interest_rate,
        )

        return loan_charge
