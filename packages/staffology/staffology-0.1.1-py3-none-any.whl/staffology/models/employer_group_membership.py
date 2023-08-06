from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="EmployerGroupMembership")


@attr.s(auto_attribs=True)
class EmployerGroupMembership:
    """Used to represent an Employers membership of a EmployerGroup

    Attributes:
        code (str): The Code for the EmployerGroup
        color (Union[Unset, None, str]): [readonly] The Color for the EmployerGroup
        title (Union[Unset, None, str]): [readonly] The Title for the EmployerGroup
        primary (Union[Unset, bool]): Set to true if this is the primary EmployerGroup for the Employer.
            Only one EmployerGroup can be set as the primary.
    """

    code: str
    color: Union[Unset, None, str] = UNSET
    title: Union[Unset, None, str] = UNSET
    primary: Union[Unset, bool] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        code = self.code
        color = self.color
        title = self.title
        primary = self.primary

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "code": code,
            }
        )
        if color is not UNSET:
            field_dict["color"] = color
        if title is not UNSET:
            field_dict["title"] = title
        if primary is not UNSET:
            field_dict["primary"] = primary

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        code = d.pop("code")

        color = d.pop("color", UNSET)

        title = d.pop("title", UNSET)

        primary = d.pop("primary", UNSET)

        employer_group_membership = cls(
            code=code,
            color=color,
            title=title,
            primary=primary,
        )

        return employer_group_membership
