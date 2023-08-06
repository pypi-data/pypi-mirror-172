import datetime
from typing import Any, Dict, Type, TypeVar, Union

import attr
from dateutil.parser import isoparse

from ..types import UNSET, Unset

T = TypeVar("T", bound="LogEntry")


@attr.s(auto_attribs=True)
class LogEntry:
    """
    Attributes:
        date (Union[Unset, datetime.date]):
        message (Union[Unset, None, str]):
    """

    date: Union[Unset, datetime.date] = UNSET
    message: Union[Unset, None, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        date: Union[Unset, str] = UNSET
        if not isinstance(self.date, Unset):
            date = self.date.isoformat()

        message = self.message

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if date is not UNSET:
            field_dict["date"] = date
        if message is not UNSET:
            field_dict["message"] = message

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        _date = d.pop("date", UNSET)
        date: Union[Unset, datetime.date]
        if isinstance(_date, Unset):
            date = UNSET
        else:
            date = isoparse(_date).date()

        message = d.pop("message", UNSET)

        log_entry = cls(
            date=date,
            message=message,
        )

        return log_entry
