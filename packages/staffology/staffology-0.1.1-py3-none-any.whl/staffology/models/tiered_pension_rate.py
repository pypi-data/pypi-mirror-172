from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="TieredPensionRate")


@attr.s(auto_attribs=True)
class TieredPensionRate:
    """Part of the TaxYearConfig that our engine uses to calculate tiered pension contributions.
    It is used internally when our engine performs calculations.
    You do not need to do anything with this model, it's provided purely for informational purposes.

        Attributes:
            name (Union[Unset, None, str]):
            description (Union[Unset, None, str]):
            range_start (Union[Unset, float]):
            rate (Union[Unset, float]):
    """

    name: Union[Unset, None, str] = UNSET
    description: Union[Unset, None, str] = UNSET
    range_start: Union[Unset, float] = UNSET
    rate: Union[Unset, float] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        name = self.name
        description = self.description
        range_start = self.range_start
        rate = self.rate

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if name is not UNSET:
            field_dict["name"] = name
        if description is not UNSET:
            field_dict["description"] = description
        if range_start is not UNSET:
            field_dict["rangeStart"] = range_start
        if rate is not UNSET:
            field_dict["rate"] = rate

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        name = d.pop("name", UNSET)

        description = d.pop("description", UNSET)

        range_start = d.pop("rangeStart", UNSET)

        rate = d.pop("rate", UNSET)

        tiered_pension_rate = cls(
            name=name,
            description=description,
            range_start=range_start,
            rate=rate,
        )

        return tiered_pension_rate
