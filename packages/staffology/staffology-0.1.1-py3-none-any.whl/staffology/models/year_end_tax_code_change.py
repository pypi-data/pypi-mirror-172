from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..models.item import Item
from ..types import UNSET, Unset

T = TypeVar("T", bound="YearEndTaxCodeChange")


@attr.s(auto_attribs=True)
class YearEndTaxCodeChange:
    """Forms part of the YearEnd model to list changes to Tax Codes

    Attributes:
        employee (Union[Unset, Item]):
        current_code (Union[Unset, None, str]): [readonly] The Employees current tax code
        new_code (Union[Unset, None, str]): [readonly] The new TaxCode for the employee
    """

    employee: Union[Unset, Item] = UNSET
    current_code: Union[Unset, None, str] = UNSET
    new_code: Union[Unset, None, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        employee: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.employee, Unset):
            employee = self.employee.to_dict()

        current_code = self.current_code
        new_code = self.new_code

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if employee is not UNSET:
            field_dict["employee"] = employee
        if current_code is not UNSET:
            field_dict["currentCode"] = current_code
        if new_code is not UNSET:
            field_dict["newCode"] = new_code

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        _employee = d.pop("employee", UNSET)
        employee: Union[Unset, Item]
        if isinstance(_employee, Unset):
            employee = UNSET
        else:
            employee = Item.from_dict(_employee)

        current_code = d.pop("currentCode", UNSET)

        new_code = d.pop("newCode", UNSET)

        year_end_tax_code_change = cls(
            employee=employee,
            current_code=current_code,
            new_code=new_code,
        )

        return year_end_tax_code_change
