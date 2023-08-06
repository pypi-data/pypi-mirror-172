from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="PartnerDetails")


@attr.s(auto_attribs=True)
class PartnerDetails:
    """
    Attributes:
        first_name (Union[Unset, None, str]):
        initials (Union[Unset, None, str]):
        last_name (Union[Unset, None, str]):
        ni_number (Union[Unset, None, str]):
    """

    first_name: Union[Unset, None, str] = UNSET
    initials: Union[Unset, None, str] = UNSET
    last_name: Union[Unset, None, str] = UNSET
    ni_number: Union[Unset, None, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        first_name = self.first_name
        initials = self.initials
        last_name = self.last_name
        ni_number = self.ni_number

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if first_name is not UNSET:
            field_dict["firstName"] = first_name
        if initials is not UNSET:
            field_dict["initials"] = initials
        if last_name is not UNSET:
            field_dict["lastName"] = last_name
        if ni_number is not UNSET:
            field_dict["niNumber"] = ni_number

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        first_name = d.pop("firstName", UNSET)

        initials = d.pop("initials", UNSET)

        last_name = d.pop("lastName", UNSET)

        ni_number = d.pop("niNumber", UNSET)

        partner_details = cls(
            first_name=first_name,
            initials=initials,
            last_name=last_name,
            ni_number=ni_number,
        )

        return partner_details
