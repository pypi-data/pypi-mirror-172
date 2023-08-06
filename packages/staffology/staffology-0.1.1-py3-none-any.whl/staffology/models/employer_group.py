from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="EmployerGroup")


@attr.s(auto_attribs=True)
class EmployerGroup:
    """
    Attributes:
        code (str): The unique code for this EmployerGroup
        name (str):
        employer_count (Union[Unset, int]):
        color (Union[Unset, None, str]): A color to used to represent this EmployerGroup, in hex format. ie 'ff0000'
    """

    code: str
    name: str
    employer_count: Union[Unset, int] = UNSET
    color: Union[Unset, None, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        code = self.code
        name = self.name
        employer_count = self.employer_count
        color = self.color

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "code": code,
                "name": name,
            }
        )
        if employer_count is not UNSET:
            field_dict["employerCount"] = employer_count
        if color is not UNSET:
            field_dict["color"] = color

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        code = d.pop("code")

        name = d.pop("name")

        employer_count = d.pop("employerCount", UNSET)

        color = d.pop("color", UNSET)

        employer_group = cls(
            code=code,
            name=name,
            employer_count=employer_count,
            color=color,
        )

        return employer_group
