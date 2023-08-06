from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.item import Item
from ..models.ytd_value import YtdValue
from ..types import UNSET, Unset

T = TypeVar("T", bound="EmployeeYtdValues")


@attr.s(auto_attribs=True)
class EmployeeYtdValues:
    """
    Attributes:
        employee (Union[Unset, Item]):
        payroll_code (Union[Unset, None, str]):
        first_name (Union[Unset, None, str]):
        last_name (Union[Unset, None, str]):
        values (Union[Unset, None, List[YtdValue]]):
    """

    employee: Union[Unset, Item] = UNSET
    payroll_code: Union[Unset, None, str] = UNSET
    first_name: Union[Unset, None, str] = UNSET
    last_name: Union[Unset, None, str] = UNSET
    values: Union[Unset, None, List[YtdValue]] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        employee: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.employee, Unset):
            employee = self.employee.to_dict()

        payroll_code = self.payroll_code
        first_name = self.first_name
        last_name = self.last_name
        values: Union[Unset, None, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.values, Unset):
            if self.values is None:
                values = None
            else:
                values = []
                for values_item_data in self.values:
                    values_item = values_item_data.to_dict()

                    values.append(values_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if employee is not UNSET:
            field_dict["employee"] = employee
        if payroll_code is not UNSET:
            field_dict["payrollCode"] = payroll_code
        if first_name is not UNSET:
            field_dict["firstName"] = first_name
        if last_name is not UNSET:
            field_dict["lastName"] = last_name
        if values is not UNSET:
            field_dict["values"] = values

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

        payroll_code = d.pop("payrollCode", UNSET)

        first_name = d.pop("firstName", UNSET)

        last_name = d.pop("lastName", UNSET)

        values = []
        _values = d.pop("values", UNSET)
        for values_item_data in _values or []:
            values_item = YtdValue.from_dict(values_item_data)

            values.append(values_item)

        employee_ytd_values = cls(
            employee=employee,
            payroll_code=payroll_code,
            first_name=first_name,
            last_name=last_name,
            values=values,
        )

        return employee_ytd_values
