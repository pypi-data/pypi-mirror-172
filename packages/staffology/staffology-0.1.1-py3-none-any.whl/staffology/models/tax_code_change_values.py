from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..models.item import Item
from ..types import UNSET, Unset

T = TypeVar("T", bound="TaxCodeChangeValues")


@attr.s(auto_attribs=True)
class TaxCodeChangeValues:
    """
    Attributes:
        employee_id (Union[Unset, int]):
        employee (Union[Unset, Item]):
        payroll_code (Union[Unset, None, str]):
        first_name (Union[Unset, None, str]):
        last_name (Union[Unset, None, str]):
        ni_number (Union[Unset, None, str]):
        period_change (Union[Unset, int]):
        previous_tax_code (Union[Unset, None, str]):
        current_tax_code (Union[Unset, None, str]):
    """

    employee_id: Union[Unset, int] = UNSET
    employee: Union[Unset, Item] = UNSET
    payroll_code: Union[Unset, None, str] = UNSET
    first_name: Union[Unset, None, str] = UNSET
    last_name: Union[Unset, None, str] = UNSET
    ni_number: Union[Unset, None, str] = UNSET
    period_change: Union[Unset, int] = UNSET
    previous_tax_code: Union[Unset, None, str] = UNSET
    current_tax_code: Union[Unset, None, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        employee_id = self.employee_id
        employee: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.employee, Unset):
            employee = self.employee.to_dict()

        payroll_code = self.payroll_code
        first_name = self.first_name
        last_name = self.last_name
        ni_number = self.ni_number
        period_change = self.period_change
        previous_tax_code = self.previous_tax_code
        current_tax_code = self.current_tax_code

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if employee_id is not UNSET:
            field_dict["employeeId"] = employee_id
        if employee is not UNSET:
            field_dict["employee"] = employee
        if payroll_code is not UNSET:
            field_dict["payrollCode"] = payroll_code
        if first_name is not UNSET:
            field_dict["firstName"] = first_name
        if last_name is not UNSET:
            field_dict["lastName"] = last_name
        if ni_number is not UNSET:
            field_dict["niNumber"] = ni_number
        if period_change is not UNSET:
            field_dict["periodChange"] = period_change
        if previous_tax_code is not UNSET:
            field_dict["previousTaxCode"] = previous_tax_code
        if current_tax_code is not UNSET:
            field_dict["currentTaxCode"] = current_tax_code

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        employee_id = d.pop("employeeId", UNSET)

        _employee = d.pop("employee", UNSET)
        employee: Union[Unset, Item]
        if isinstance(_employee, Unset):
            employee = UNSET
        else:
            employee = Item.from_dict(_employee)

        payroll_code = d.pop("payrollCode", UNSET)

        first_name = d.pop("firstName", UNSET)

        last_name = d.pop("lastName", UNSET)

        ni_number = d.pop("niNumber", UNSET)

        period_change = d.pop("periodChange", UNSET)

        previous_tax_code = d.pop("previousTaxCode", UNSET)

        current_tax_code = d.pop("currentTaxCode", UNSET)

        tax_code_change_values = cls(
            employee_id=employee_id,
            employee=employee,
            payroll_code=payroll_code,
            first_name=first_name,
            last_name=last_name,
            ni_number=ni_number,
            period_change=period_change,
            previous_tax_code=previous_tax_code,
            current_tax_code=current_tax_code,
        )

        return tax_code_change_values
