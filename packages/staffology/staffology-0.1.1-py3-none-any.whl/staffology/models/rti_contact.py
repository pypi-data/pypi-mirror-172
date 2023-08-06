from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="RtiContact")


@attr.s(auto_attribs=True)
class RtiContact:
    """
    Attributes:
        first_name (Union[Unset, None, str]):
        last_name (Union[Unset, None, str]):
        email (Union[Unset, None, str]):
        telephone (Union[Unset, None, str]):
    """

    first_name: Union[Unset, None, str] = UNSET
    last_name: Union[Unset, None, str] = UNSET
    email: Union[Unset, None, str] = UNSET
    telephone: Union[Unset, None, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        first_name = self.first_name
        last_name = self.last_name
        email = self.email
        telephone = self.telephone

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if first_name is not UNSET:
            field_dict["firstName"] = first_name
        if last_name is not UNSET:
            field_dict["lastName"] = last_name
        if email is not UNSET:
            field_dict["email"] = email
        if telephone is not UNSET:
            field_dict["telephone"] = telephone

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        first_name = d.pop("firstName", UNSET)

        last_name = d.pop("lastName", UNSET)

        email = d.pop("email", UNSET)

        telephone = d.pop("telephone", UNSET)

        rti_contact = cls(
            first_name=first_name,
            last_name=last_name,
            email=email,
            telephone=telephone,
        )

        return rti_contact
