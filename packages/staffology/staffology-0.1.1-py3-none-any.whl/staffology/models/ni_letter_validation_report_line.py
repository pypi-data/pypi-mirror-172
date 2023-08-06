import datetime
from typing import Any, Dict, Type, TypeVar, Union

import attr
from dateutil.parser import isoparse

from ..models.gender import Gender
from ..models.ni_letter_error import NiLetterError
from ..types import UNSET, Unset

T = TypeVar("T", bound="NiLetterValidationReportLine")


@attr.s(auto_attribs=True)
class NiLetterValidationReportLine:
    """
    Attributes:
        employee_id (Union[Unset, str]):
        payroll_code (Union[Unset, None, str]):
        name (Union[Unset, None, str]):
        ni_number (Union[Unset, None, str]):
        gender (Union[Unset, Gender]):
        date_of_birth (Union[Unset, datetime.date]):
        ni_letter_error (Union[Unset, NiLetterError]):
        error_details (Union[Unset, None, str]):
        ni_letter (Union[Unset, None, str]):
        suggested_letter (Union[Unset, None, str]):
    """

    employee_id: Union[Unset, str] = UNSET
    payroll_code: Union[Unset, None, str] = UNSET
    name: Union[Unset, None, str] = UNSET
    ni_number: Union[Unset, None, str] = UNSET
    gender: Union[Unset, Gender] = UNSET
    date_of_birth: Union[Unset, datetime.date] = UNSET
    ni_letter_error: Union[Unset, NiLetterError] = UNSET
    error_details: Union[Unset, None, str] = UNSET
    ni_letter: Union[Unset, None, str] = UNSET
    suggested_letter: Union[Unset, None, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        employee_id = self.employee_id
        payroll_code = self.payroll_code
        name = self.name
        ni_number = self.ni_number
        gender: Union[Unset, str] = UNSET
        if not isinstance(self.gender, Unset):
            gender = self.gender.value

        date_of_birth: Union[Unset, str] = UNSET
        if not isinstance(self.date_of_birth, Unset):
            date_of_birth = self.date_of_birth.isoformat()

        ni_letter_error: Union[Unset, str] = UNSET
        if not isinstance(self.ni_letter_error, Unset):
            ni_letter_error = self.ni_letter_error.value

        error_details = self.error_details
        ni_letter = self.ni_letter
        suggested_letter = self.suggested_letter

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if employee_id is not UNSET:
            field_dict["employeeId"] = employee_id
        if payroll_code is not UNSET:
            field_dict["payrollCode"] = payroll_code
        if name is not UNSET:
            field_dict["name"] = name
        if ni_number is not UNSET:
            field_dict["niNumber"] = ni_number
        if gender is not UNSET:
            field_dict["gender"] = gender
        if date_of_birth is not UNSET:
            field_dict["dateOfBirth"] = date_of_birth
        if ni_letter_error is not UNSET:
            field_dict["niLetterError"] = ni_letter_error
        if error_details is not UNSET:
            field_dict["errorDetails"] = error_details
        if ni_letter is not UNSET:
            field_dict["niLetter"] = ni_letter
        if suggested_letter is not UNSET:
            field_dict["suggestedLetter"] = suggested_letter

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        employee_id = d.pop("employeeId", UNSET)

        payroll_code = d.pop("payrollCode", UNSET)

        name = d.pop("name", UNSET)

        ni_number = d.pop("niNumber", UNSET)

        _gender = d.pop("gender", UNSET)
        gender: Union[Unset, Gender]
        if isinstance(_gender, Unset):
            gender = UNSET
        else:
            gender = Gender(_gender)

        _date_of_birth = d.pop("dateOfBirth", UNSET)
        date_of_birth: Union[Unset, datetime.date]
        if isinstance(_date_of_birth, Unset):
            date_of_birth = UNSET
        else:
            date_of_birth = isoparse(_date_of_birth).date()

        _ni_letter_error = d.pop("niLetterError", UNSET)
        ni_letter_error: Union[Unset, NiLetterError]
        if isinstance(_ni_letter_error, Unset):
            ni_letter_error = UNSET
        else:
            ni_letter_error = NiLetterError(_ni_letter_error)

        error_details = d.pop("errorDetails", UNSET)

        ni_letter = d.pop("niLetter", UNSET)

        suggested_letter = d.pop("suggestedLetter", UNSET)

        ni_letter_validation_report_line = cls(
            employee_id=employee_id,
            payroll_code=payroll_code,
            name=name,
            ni_number=ni_number,
            gender=gender,
            date_of_birth=date_of_birth,
            ni_letter_error=ni_letter_error,
            error_details=error_details,
            ni_letter=ni_letter,
            suggested_letter=suggested_letter,
        )

        return ni_letter_validation_report_line
