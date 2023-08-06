from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="GovTalkError")


@attr.s(auto_attribs=True)
class GovTalkError:
    """
    Attributes:
        raised_by (Union[Unset, None, str]):
        number (Union[Unset, None, str]):
        type (Union[Unset, None, str]):
        text (Union[Unset, None, str]):
        location (Union[Unset, None, str]):
    """

    raised_by: Union[Unset, None, str] = UNSET
    number: Union[Unset, None, str] = UNSET
    type: Union[Unset, None, str] = UNSET
    text: Union[Unset, None, str] = UNSET
    location: Union[Unset, None, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        raised_by = self.raised_by
        number = self.number
        type = self.type
        text = self.text
        location = self.location

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if raised_by is not UNSET:
            field_dict["raisedBy"] = raised_by
        if number is not UNSET:
            field_dict["number"] = number
        if type is not UNSET:
            field_dict["type"] = type
        if text is not UNSET:
            field_dict["text"] = text
        if location is not UNSET:
            field_dict["location"] = location

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        raised_by = d.pop("raisedBy", UNSET)

        number = d.pop("number", UNSET)

        type = d.pop("type", UNSET)

        text = d.pop("text", UNSET)

        location = d.pop("location", UNSET)

        gov_talk_error = cls(
            raised_by=raised_by,
            number=number,
            type=type,
            text=text,
            location=location,
        )

        return gov_talk_error
