from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="CarChargeRate")


@attr.s(auto_attribs=True)
class CarChargeRate:
    """Part of the TaxYearConfig that our engine uses to calculate charges for a Company Car.
    It is used internally when our engine performs calculations.
    You do not need to do anything with this model, it's provided purely for informational purposes.

        Attributes:
            range_start (Union[Unset, int]):
            range_stop (Union[Unset, int]):
            rate (Union[Unset, float]):
    """

    range_start: Union[Unset, int] = UNSET
    range_stop: Union[Unset, int] = UNSET
    rate: Union[Unset, float] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        range_start = self.range_start
        range_stop = self.range_stop
        rate = self.rate

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if range_start is not UNSET:
            field_dict["rangeStart"] = range_start
        if range_stop is not UNSET:
            field_dict["rangeStop"] = range_stop
        if rate is not UNSET:
            field_dict["rate"] = rate

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        range_start = d.pop("rangeStart", UNSET)

        range_stop = d.pop("rangeStop", UNSET)

        rate = d.pop("rate", UNSET)

        car_charge_rate = cls(
            range_start=range_start,
            range_stop=range_stop,
            rate=rate,
        )

        return car_charge_rate
