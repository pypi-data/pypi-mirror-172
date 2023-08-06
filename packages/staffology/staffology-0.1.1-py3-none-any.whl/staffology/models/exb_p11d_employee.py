from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..models.rti_employee_name import RtiEmployeeName
from ..types import UNSET, Unset

T = TypeVar("T", bound="ExbP11DEmployee")


@attr.s(auto_attribs=True)
class ExbP11DEmployee:
    """
    Attributes:
        employee_unique_id (Union[Unset, str]):
        dir_ind (Union[Unset, None, str]):
        name (Union[Unset, RtiEmployeeName]):
        wks_no (Union[Unset, None, str]):
        nino (Union[Unset, None, str]):
        birth_date (Union[Unset, None, str]):
        gender (Union[Unset, None, str]):
    """

    employee_unique_id: Union[Unset, str] = UNSET
    dir_ind: Union[Unset, None, str] = UNSET
    name: Union[Unset, RtiEmployeeName] = UNSET
    wks_no: Union[Unset, None, str] = UNSET
    nino: Union[Unset, None, str] = UNSET
    birth_date: Union[Unset, None, str] = UNSET
    gender: Union[Unset, None, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        employee_unique_id = self.employee_unique_id
        dir_ind = self.dir_ind
        name: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.name, Unset):
            name = self.name.to_dict()

        wks_no = self.wks_no
        nino = self.nino
        birth_date = self.birth_date
        gender = self.gender

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if employee_unique_id is not UNSET:
            field_dict["employeeUniqueId"] = employee_unique_id
        if dir_ind is not UNSET:
            field_dict["dirInd"] = dir_ind
        if name is not UNSET:
            field_dict["name"] = name
        if wks_no is not UNSET:
            field_dict["wksNo"] = wks_no
        if nino is not UNSET:
            field_dict["nino"] = nino
        if birth_date is not UNSET:
            field_dict["birthDate"] = birth_date
        if gender is not UNSET:
            field_dict["gender"] = gender

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        employee_unique_id = d.pop("employeeUniqueId", UNSET)

        dir_ind = d.pop("dirInd", UNSET)

        _name = d.pop("name", UNSET)
        name: Union[Unset, RtiEmployeeName]
        if isinstance(_name, Unset):
            name = UNSET
        else:
            name = RtiEmployeeName.from_dict(_name)

        wks_no = d.pop("wksNo", UNSET)

        nino = d.pop("nino", UNSET)

        birth_date = d.pop("birthDate", UNSET)

        gender = d.pop("gender", UNSET)

        exb_p11d_employee = cls(
            employee_unique_id=employee_unique_id,
            dir_ind=dir_ind,
            name=name,
            wks_no=wks_no,
            nino=nino,
            birth_date=birth_date,
            gender=gender,
        )

        return exb_p11d_employee
