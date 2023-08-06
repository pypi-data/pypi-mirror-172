from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="NationalMinimumWage")


@attr.s(auto_attribs=True)
class NationalMinimumWage:
    """Part of the TaxYearConfig that our engine uses to calculate National Minimum Wage.
    It is used internally when our engine performs calculations.
    You do not need to do anything with this model, it's provided purely for informational purposes.

        Attributes:
            apprentice (Union[Unset, None, bool]):
            max_age (Union[Unset, int]):
            hourly_amount (Union[Unset, float]):
    """

    apprentice: Union[Unset, None, bool] = UNSET
    max_age: Union[Unset, int] = UNSET
    hourly_amount: Union[Unset, float] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        apprentice = self.apprentice
        max_age = self.max_age
        hourly_amount = self.hourly_amount

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if apprentice is not UNSET:
            field_dict["apprentice"] = apprentice
        if max_age is not UNSET:
            field_dict["maxAge"] = max_age
        if hourly_amount is not UNSET:
            field_dict["hourlyAmount"] = hourly_amount

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        apprentice = d.pop("apprentice", UNSET)

        max_age = d.pop("maxAge", UNSET)

        hourly_amount = d.pop("hourlyAmount", UNSET)

        national_minimum_wage = cls(
            apprentice=apprentice,
            max_age=max_age,
            hourly_amount=hourly_amount,
        )

        return national_minimum_wage
