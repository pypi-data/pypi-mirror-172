import datetime
from typing import Any, Dict, Type, TypeVar, Union

import attr
from dateutil.parser import isoparse

from ..types import UNSET, Unset

T = TypeVar("T", bound="VeteranDetails")


@attr.s(auto_attribs=True)
class VeteranDetails:
    """Employment details for veterans

    Attributes:
        is_veteran (Union[Unset, bool]): Set to true if the employee is a veteran
        first_civilian_employment_date (Union[Unset, None, datetime.date]): Date of Veteran's first civilian employment
    """

    is_veteran: Union[Unset, bool] = UNSET
    first_civilian_employment_date: Union[Unset, None, datetime.date] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        is_veteran = self.is_veteran
        first_civilian_employment_date: Union[Unset, None, str] = UNSET
        if not isinstance(self.first_civilian_employment_date, Unset):
            first_civilian_employment_date = (
                self.first_civilian_employment_date.isoformat()
                if self.first_civilian_employment_date
                else None
            )

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if is_veteran is not UNSET:
            field_dict["isVeteran"] = is_veteran
        if first_civilian_employment_date is not UNSET:
            field_dict["firstCivilianEmploymentDate"] = first_civilian_employment_date

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        is_veteran = d.pop("isVeteran", UNSET)

        _first_civilian_employment_date = d.pop("firstCivilianEmploymentDate", UNSET)
        first_civilian_employment_date: Union[Unset, None, datetime.date]
        if _first_civilian_employment_date is None:
            first_civilian_employment_date = None
        elif isinstance(_first_civilian_employment_date, Unset):
            first_civilian_employment_date = UNSET
        else:
            first_civilian_employment_date = isoparse(
                _first_civilian_employment_date
            ).date()

        veteran_details = cls(
            is_veteran=is_veteran,
            first_civilian_employment_date=first_civilian_employment_date,
        )

        return veteran_details
