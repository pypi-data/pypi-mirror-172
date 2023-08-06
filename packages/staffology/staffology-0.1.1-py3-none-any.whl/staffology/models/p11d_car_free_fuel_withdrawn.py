from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="P11DCarFreeFuelWithdrawn")


@attr.s(auto_attribs=True)
class P11DCarFreeFuelWithdrawn:
    """
    Attributes:
        reinstated (Union[Unset, None, str]):
        value (Union[Unset, None, str]):
    """

    reinstated: Union[Unset, None, str] = UNSET
    value: Union[Unset, None, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        reinstated = self.reinstated
        value = self.value

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if reinstated is not UNSET:
            field_dict["reinstated"] = reinstated
        if value is not UNSET:
            field_dict["value"] = value

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        reinstated = d.pop("reinstated", UNSET)

        value = d.pop("value", UNSET)

        p11d_car_free_fuel_withdrawn = cls(
            reinstated=reinstated,
            value=value,
        )

        return p11d_car_free_fuel_withdrawn
