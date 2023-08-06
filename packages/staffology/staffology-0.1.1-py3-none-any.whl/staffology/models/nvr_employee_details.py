from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..models.rti_employee_address import RtiEmployeeAddress
from ..models.rti_employee_name import RtiEmployeeName
from ..types import UNSET, Unset

T = TypeVar("T", bound="NvrEmployeeDetails")


@attr.s(auto_attribs=True)
class NvrEmployeeDetails:
    """
    Attributes:
        nino (Union[Unset, None, str]):
        name (Union[Unset, RtiEmployeeName]):
        address (Union[Unset, RtiEmployeeAddress]):
        birth_date (Union[Unset, None, str]):
        gender (Union[Unset, None, str]):
    """

    nino: Union[Unset, None, str] = UNSET
    name: Union[Unset, RtiEmployeeName] = UNSET
    address: Union[Unset, RtiEmployeeAddress] = UNSET
    birth_date: Union[Unset, None, str] = UNSET
    gender: Union[Unset, None, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        nino = self.nino
        name: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.name, Unset):
            name = self.name.to_dict()

        address: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.address, Unset):
            address = self.address.to_dict()

        birth_date = self.birth_date
        gender = self.gender

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if nino is not UNSET:
            field_dict["nino"] = nino
        if name is not UNSET:
            field_dict["name"] = name
        if address is not UNSET:
            field_dict["address"] = address
        if birth_date is not UNSET:
            field_dict["birthDate"] = birth_date
        if gender is not UNSET:
            field_dict["gender"] = gender

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        nino = d.pop("nino", UNSET)

        _name = d.pop("name", UNSET)
        name: Union[Unset, RtiEmployeeName]
        if isinstance(_name, Unset):
            name = UNSET
        else:
            name = RtiEmployeeName.from_dict(_name)

        _address = d.pop("address", UNSET)
        address: Union[Unset, RtiEmployeeAddress]
        if isinstance(_address, Unset):
            address = UNSET
        else:
            address = RtiEmployeeAddress.from_dict(_address)

        birth_date = d.pop("birthDate", UNSET)

        gender = d.pop("gender", UNSET)

        nvr_employee_details = cls(
            nino=nino,
            name=name,
            address=address,
            birth_date=birth_date,
            gender=gender,
        )

        return nvr_employee_details
