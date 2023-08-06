from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="PapdisEmployeeName")


@attr.s(auto_attribs=True)
class PapdisEmployeeName:
    """
    Attributes:
        title (Union[Unset, None, str]): [readonly]
        forename1 (Union[Unset, None, str]): [readonly]
        forename2 (Union[Unset, None, str]): [readonly]
        surname (Union[Unset, None, str]): [readonly]
    """

    title: Union[Unset, None, str] = UNSET
    forename1: Union[Unset, None, str] = UNSET
    forename2: Union[Unset, None, str] = UNSET
    surname: Union[Unset, None, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        title = self.title
        forename1 = self.forename1
        forename2 = self.forename2
        surname = self.surname

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if title is not UNSET:
            field_dict["title"] = title
        if forename1 is not UNSET:
            field_dict["forename1"] = forename1
        if forename2 is not UNSET:
            field_dict["forename2"] = forename2
        if surname is not UNSET:
            field_dict["surname"] = surname

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        title = d.pop("title", UNSET)

        forename1 = d.pop("forename1", UNSET)

        forename2 = d.pop("forename2", UNSET)

        surname = d.pop("surname", UNSET)

        papdis_employee_name = cls(
            title=title,
            forename1=forename1,
            forename2=forename2,
            surname=surname,
        )

        return papdis_employee_name
