from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="PapdisEmployeeContactPostalAddress")


@attr.s(auto_attribs=True)
class PapdisEmployeeContactPostalAddress:
    """
    Attributes:
        address1 (Union[Unset, None, str]): [readonly]
        address2 (Union[Unset, None, str]): [readonly]
        address3 (Union[Unset, None, str]): [readonly]
        address4 (Union[Unset, None, str]): [readonly]
        postcode (Union[Unset, None, str]): [readonly]
        country (Union[Unset, None, str]): [readonly]
    """

    address1: Union[Unset, None, str] = UNSET
    address2: Union[Unset, None, str] = UNSET
    address3: Union[Unset, None, str] = UNSET
    address4: Union[Unset, None, str] = UNSET
    postcode: Union[Unset, None, str] = UNSET
    country: Union[Unset, None, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        address1 = self.address1
        address2 = self.address2
        address3 = self.address3
        address4 = self.address4
        postcode = self.postcode
        country = self.country

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if address1 is not UNSET:
            field_dict["address1"] = address1
        if address2 is not UNSET:
            field_dict["address2"] = address2
        if address3 is not UNSET:
            field_dict["address3"] = address3
        if address4 is not UNSET:
            field_dict["address4"] = address4
        if postcode is not UNSET:
            field_dict["postcode"] = postcode
        if country is not UNSET:
            field_dict["country"] = country

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        address1 = d.pop("address1", UNSET)

        address2 = d.pop("address2", UNSET)

        address3 = d.pop("address3", UNSET)

        address4 = d.pop("address4", UNSET)

        postcode = d.pop("postcode", UNSET)

        country = d.pop("country", UNSET)

        papdis_employee_contact_postal_address = cls(
            address1=address1,
            address2=address2,
            address3=address3,
            address4=address4,
            postcode=postcode,
            country=country,
        )

        return papdis_employee_contact_postal_address
