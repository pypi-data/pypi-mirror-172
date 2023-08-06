from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.nvr_employee import NvrEmployee
from ..types import UNSET, Unset

T = TypeVar("T", bound="NvrRequest")


@attr.s(auto_attribs=True)
class NvrRequest:
    """
    Attributes:
        employee (Union[Unset, None, List[NvrEmployee]]):
        related_tax_year (Union[Unset, None, str]):
    """

    employee: Union[Unset, None, List[NvrEmployee]] = UNSET
    related_tax_year: Union[Unset, None, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        employee: Union[Unset, None, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.employee, Unset):
            if self.employee is None:
                employee = None
            else:
                employee = []
                for employee_item_data in self.employee:
                    employee_item = employee_item_data.to_dict()

                    employee.append(employee_item)

        related_tax_year = self.related_tax_year

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if employee is not UNSET:
            field_dict["employee"] = employee
        if related_tax_year is not UNSET:
            field_dict["relatedTaxYear"] = related_tax_year

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        employee = []
        _employee = d.pop("employee", UNSET)
        for employee_item_data in _employee or []:
            employee_item = NvrEmployee.from_dict(employee_item_data)

            employee.append(employee_item)

        related_tax_year = d.pop("relatedTaxYear", UNSET)

        nvr_request = cls(
            employee=employee,
            related_tax_year=related_tax_year,
        )

        return nvr_request
