from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..models.papdis_employee_contact_postal_address import (
    PapdisEmployeeContactPostalAddress,
)
from ..types import UNSET, Unset

T = TypeVar("T", bound="PapdisEmployeeContact")


@attr.s(auto_attribs=True)
class PapdisEmployeeContact:
    """
    Attributes:
        postal_address (Union[Unset, PapdisEmployeeContactPostalAddress]):
        email_address (Union[Unset, None, str]): [readonly]
        secondary_email_address (Union[Unset, None, str]): [readonly]
    """

    postal_address: Union[Unset, PapdisEmployeeContactPostalAddress] = UNSET
    email_address: Union[Unset, None, str] = UNSET
    secondary_email_address: Union[Unset, None, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        postal_address: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.postal_address, Unset):
            postal_address = self.postal_address.to_dict()

        email_address = self.email_address
        secondary_email_address = self.secondary_email_address

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if postal_address is not UNSET:
            field_dict["postalAddress"] = postal_address
        if email_address is not UNSET:
            field_dict["emailAddress"] = email_address
        if secondary_email_address is not UNSET:
            field_dict["secondaryEmailAddress"] = secondary_email_address

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        _postal_address = d.pop("postalAddress", UNSET)
        postal_address: Union[Unset, PapdisEmployeeContactPostalAddress]
        if isinstance(_postal_address, Unset):
            postal_address = UNSET
        else:
            postal_address = PapdisEmployeeContactPostalAddress.from_dict(
                _postal_address
            )

        email_address = d.pop("emailAddress", UNSET)

        secondary_email_address = d.pop("secondaryEmailAddress", UNSET)

        papdis_employee_contact = cls(
            postal_address=postal_address,
            email_address=email_address,
            secondary_email_address=secondary_email_address,
        )

        return papdis_employee_contact
