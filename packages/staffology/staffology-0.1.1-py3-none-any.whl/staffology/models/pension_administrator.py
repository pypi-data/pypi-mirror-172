from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..models.address import Address
from ..types import UNSET, Unset

T = TypeVar("T", bound="PensionAdministrator")


@attr.s(auto_attribs=True)
class PensionAdministrator:
    """
    Attributes:
        name (Union[Unset, None, str]):
        email (Union[Unset, None, str]):
        address (Union[Unset, Address]):
        telephone (Union[Unset, None, str]):
        id (Union[Unset, str]): [readonly] The unique id of the object
    """

    name: Union[Unset, None, str] = UNSET
    email: Union[Unset, None, str] = UNSET
    address: Union[Unset, Address] = UNSET
    telephone: Union[Unset, None, str] = UNSET
    id: Union[Unset, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        name = self.name
        email = self.email
        address: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.address, Unset):
            address = self.address.to_dict()

        telephone = self.telephone
        id = self.id

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if name is not UNSET:
            field_dict["name"] = name
        if email is not UNSET:
            field_dict["email"] = email
        if address is not UNSET:
            field_dict["address"] = address
        if telephone is not UNSET:
            field_dict["telephone"] = telephone
        if id is not UNSET:
            field_dict["id"] = id

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        name = d.pop("name", UNSET)

        email = d.pop("email", UNSET)

        _address = d.pop("address", UNSET)
        address: Union[Unset, Address]
        if isinstance(_address, Unset):
            address = UNSET
        else:
            address = Address.from_dict(_address)

        telephone = d.pop("telephone", UNSET)

        id = d.pop("id", UNSET)

        pension_administrator = cls(
            name=name,
            email=email,
            address=address,
            telephone=telephone,
            id=id,
        )

        return pension_administrator
