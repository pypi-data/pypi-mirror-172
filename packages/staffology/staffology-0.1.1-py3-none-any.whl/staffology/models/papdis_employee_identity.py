import datetime
from typing import Any, Dict, Type, TypeVar, Union

import attr
from dateutil.parser import isoparse

from ..types import UNSET, Unset

T = TypeVar("T", bound="PapdisEmployeeIdentity")


@attr.s(auto_attribs=True)
class PapdisEmployeeIdentity:
    """
    Attributes:
        employee_id (Union[Unset, None, str]): [readonly]
        birth_date (Union[Unset, datetime.date]): [readonly]
        gender (Union[Unset, None, str]): [readonly]
        national_insurance_number (Union[Unset, None, str]): [readonly]
        employment_start_date (Union[Unset, datetime.date]): [readonly]
    """

    employee_id: Union[Unset, None, str] = UNSET
    birth_date: Union[Unset, datetime.date] = UNSET
    gender: Union[Unset, None, str] = UNSET
    national_insurance_number: Union[Unset, None, str] = UNSET
    employment_start_date: Union[Unset, datetime.date] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        employee_id = self.employee_id
        birth_date: Union[Unset, str] = UNSET
        if not isinstance(self.birth_date, Unset):
            birth_date = self.birth_date.isoformat()

        gender = self.gender
        national_insurance_number = self.national_insurance_number
        employment_start_date: Union[Unset, str] = UNSET
        if not isinstance(self.employment_start_date, Unset):
            employment_start_date = self.employment_start_date.isoformat()

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if employee_id is not UNSET:
            field_dict["employeeId"] = employee_id
        if birth_date is not UNSET:
            field_dict["birthDate"] = birth_date
        if gender is not UNSET:
            field_dict["gender"] = gender
        if national_insurance_number is not UNSET:
            field_dict["nationalInsuranceNumber"] = national_insurance_number
        if employment_start_date is not UNSET:
            field_dict["employmentStartDate"] = employment_start_date

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        employee_id = d.pop("employeeId", UNSET)

        _birth_date = d.pop("birthDate", UNSET)
        birth_date: Union[Unset, datetime.date]
        if isinstance(_birth_date, Unset):
            birth_date = UNSET
        else:
            birth_date = isoparse(_birth_date).date()

        gender = d.pop("gender", UNSET)

        national_insurance_number = d.pop("nationalInsuranceNumber", UNSET)

        _employment_start_date = d.pop("employmentStartDate", UNSET)
        employment_start_date: Union[Unset, datetime.date]
        if isinstance(_employment_start_date, Unset):
            employment_start_date = UNSET
        else:
            employment_start_date = isoparse(_employment_start_date).date()

        papdis_employee_identity = cls(
            employee_id=employee_id,
            birth_date=birth_date,
            gender=gender,
            national_insurance_number=national_insurance_number,
            employment_start_date=employment_start_date,
        )

        return papdis_employee_identity
