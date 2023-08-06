from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="Tag")


@attr.s(auto_attribs=True)
class Tag:
    """
    Attributes:
        code (str): The unique code for this Tag
        title (str): The title for this Tag
        color (Union[Unset, None, str]): A color to used to represent this Tag, in hex format. ie 'ff0000'
    """

    code: str
    title: str
    color: Union[Unset, None, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        code = self.code
        title = self.title
        color = self.color

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "code": code,
                "title": title,
            }
        )
        if color is not UNSET:
            field_dict["color"] = color

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        code = d.pop("code")

        title = d.pop("title")

        color = d.pop("color", UNSET)

        tag = cls(
            code=code,
            title=title,
            color=color,
        )

        return tag
