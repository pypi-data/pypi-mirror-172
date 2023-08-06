from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="CisPartnership")


@attr.s(auto_attribs=True)
class CisPartnership:
    """If an Employee is marked as a CIS Subcontractor and is registered as a Partnership then this model provides further
    details specifically related to the CIS Partnership.

        Attributes:
            name (Union[Unset, None, str]):
            utr (Union[Unset, None, str]):
    """

    name: Union[Unset, None, str] = UNSET
    utr: Union[Unset, None, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        name = self.name
        utr = self.utr

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if name is not UNSET:
            field_dict["name"] = name
        if utr is not UNSET:
            field_dict["utr"] = utr

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        name = d.pop("name", UNSET)

        utr = d.pop("utr", UNSET)

        cis_partnership = cls(
            name=name,
            utr=utr,
        )

        return cis_partnership
