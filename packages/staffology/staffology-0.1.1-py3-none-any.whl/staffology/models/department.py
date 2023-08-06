from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="Department")


@attr.s(auto_attribs=True)
class Department:
    """
    Attributes:
        code (str): The unique code for this Department
        title (str): The name of this Department
        color (Union[Unset, None, str]): A color to used to represent this Department, in hex format. ie 'ff0000'
        employee_count (Union[Unset, int]): [readonly] The number of employees with this set as their primary department
        accounting_code (Union[Unset, None, str]):
    """

    code: str
    title: str
    color: Union[Unset, None, str] = UNSET
    employee_count: Union[Unset, int] = UNSET
    accounting_code: Union[Unset, None, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        code = self.code
        title = self.title
        color = self.color
        employee_count = self.employee_count
        accounting_code = self.accounting_code

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "code": code,
                "title": title,
            }
        )
        if color is not UNSET:
            field_dict["color"] = color
        if employee_count is not UNSET:
            field_dict["employeeCount"] = employee_count
        if accounting_code is not UNSET:
            field_dict["accountingCode"] = accounting_code

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        code = d.pop("code")

        title = d.pop("title")

        color = d.pop("color", UNSET)

        employee_count = d.pop("employeeCount", UNSET)

        accounting_code = d.pop("accountingCode", UNSET)

        department = cls(
            code=code,
            title=title,
            color=color,
            employee_count=employee_count,
            accounting_code=accounting_code,
        )

        return department
