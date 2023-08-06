import datetime
from typing import Any, Dict, Type, TypeVar, Union

import attr
from dateutil.parser import isoparse

from ..types import UNSET, Unset

T = TypeVar("T", bound="DirectorshipDetails")


@attr.s(auto_attribs=True)
class DirectorshipDetails:
    """
    Attributes:
        is_director (Union[Unset, bool]):
        start_date (Union[Unset, None, datetime.date]):
        leave_date (Union[Unset, None, datetime.date]):
        ni_alternative_method (Union[Unset, bool]):
    """

    is_director: Union[Unset, bool] = UNSET
    start_date: Union[Unset, None, datetime.date] = UNSET
    leave_date: Union[Unset, None, datetime.date] = UNSET
    ni_alternative_method: Union[Unset, bool] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        is_director = self.is_director
        start_date: Union[Unset, None, str] = UNSET
        if not isinstance(self.start_date, Unset):
            start_date = self.start_date.isoformat() if self.start_date else None

        leave_date: Union[Unset, None, str] = UNSET
        if not isinstance(self.leave_date, Unset):
            leave_date = self.leave_date.isoformat() if self.leave_date else None

        ni_alternative_method = self.ni_alternative_method

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if is_director is not UNSET:
            field_dict["isDirector"] = is_director
        if start_date is not UNSET:
            field_dict["startDate"] = start_date
        if leave_date is not UNSET:
            field_dict["leaveDate"] = leave_date
        if ni_alternative_method is not UNSET:
            field_dict["niAlternativeMethod"] = ni_alternative_method

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        is_director = d.pop("isDirector", UNSET)

        _start_date = d.pop("startDate", UNSET)
        start_date: Union[Unset, None, datetime.date]
        if _start_date is None:
            start_date = None
        elif isinstance(_start_date, Unset):
            start_date = UNSET
        else:
            start_date = isoparse(_start_date).date()

        _leave_date = d.pop("leaveDate", UNSET)
        leave_date: Union[Unset, None, datetime.date]
        if _leave_date is None:
            leave_date = None
        elif isinstance(_leave_date, Unset):
            leave_date = UNSET
        else:
            leave_date = isoparse(_leave_date).date()

        ni_alternative_method = d.pop("niAlternativeMethod", UNSET)

        directorship_details = cls(
            is_director=is_director,
            start_date=start_date,
            leave_date=leave_date,
            ni_alternative_method=ni_alternative_method,
        )

        return directorship_details
