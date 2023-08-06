from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="DepartmentMembership")


@attr.s(auto_attribs=True)
class DepartmentMembership:
    """Used to represent an Employees membership of a Department

    Attributes:
        code (str): The Code for the Department
        color (Union[Unset, None, str]): [readonly] The Color for the Department
        title (Union[Unset, None, str]): [readonly] The Title for the Department
        primary (Union[Unset, bool]): Set to true if this is the primary Department for the Employee.
            Only one department can be set as the primary.
        weighting (Union[Unset, float]): If there is more than one Department Membership for the Employee then this
            determines the weighting to give to this membership.
            ie, if he is in two departments you might set the primary as 0.8 and the secondary as 0.2;
    """

    code: str
    color: Union[Unset, None, str] = UNSET
    title: Union[Unset, None, str] = UNSET
    primary: Union[Unset, bool] = UNSET
    weighting: Union[Unset, float] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        code = self.code
        color = self.color
        title = self.title
        primary = self.primary
        weighting = self.weighting

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
        if weighting is not UNSET:
            field_dict["weighting"] = weighting

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        code = d.pop("code")

        color = d.pop("color", UNSET)

        title = d.pop("title", UNSET)

        primary = d.pop("primary", UNSET)

        weighting = d.pop("weighting", UNSET)

        department_membership = cls(
            code=code,
            color=color,
            title=title,
            primary=primary,
            weighting=weighting,
        )

        return department_membership
