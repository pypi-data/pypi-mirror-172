import datetime
from typing import Any, Dict, Type, TypeVar, Union

import attr
from dateutil.parser import isoparse

from ..models.calendar_entry_type import CalendarEntryType
from ..types import UNSET, Unset

T = TypeVar("T", bound="CalendarEntry")


@attr.s(auto_attribs=True)
class CalendarEntry:
    """
    Attributes:
        title (Union[Unset, None, str]):
        start (Union[Unset, datetime.date]):
        end (Union[Unset, datetime.date]):
        type (Union[Unset, CalendarEntryType]):
    """

    title: Union[Unset, None, str] = UNSET
    start: Union[Unset, datetime.date] = UNSET
    end: Union[Unset, datetime.date] = UNSET
    type: Union[Unset, CalendarEntryType] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        title = self.title
        start: Union[Unset, str] = UNSET
        if not isinstance(self.start, Unset):
            start = self.start.isoformat()

        end: Union[Unset, str] = UNSET
        if not isinstance(self.end, Unset):
            end = self.end.isoformat()

        type: Union[Unset, str] = UNSET
        if not isinstance(self.type, Unset):
            type = self.type.value

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if title is not UNSET:
            field_dict["title"] = title
        if start is not UNSET:
            field_dict["start"] = start
        if end is not UNSET:
            field_dict["end"] = end
        if type is not UNSET:
            field_dict["type"] = type

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        title = d.pop("title", UNSET)

        _start = d.pop("start", UNSET)
        start: Union[Unset, datetime.date]
        if isinstance(_start, Unset):
            start = UNSET
        else:
            start = isoparse(_start).date()

        _end = d.pop("end", UNSET)
        end: Union[Unset, datetime.date]
        if isinstance(_end, Unset):
            end = UNSET
        else:
            end = isoparse(_end).date()

        _type = d.pop("type", UNSET)
        type: Union[Unset, CalendarEntryType]
        if isinstance(_type, Unset):
            type = UNSET
        else:
            type = CalendarEntryType(_type)

        calendar_entry = cls(
            title=title,
            start=start,
            end=end,
            type=type,
        )

        return calendar_entry
