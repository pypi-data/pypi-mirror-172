from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..models.item import Item
from ..types import UNSET, Unset

T = TypeVar("T", bound="GrossToNetReportCisLine")


@attr.s(auto_attribs=True)
class GrossToNetReportCisLine:
    """
    Attributes:
        employee (Union[Unset, Item]):
        payroll_code (Union[Unset, None, str]):
        department (Union[Unset, None, str]):
        total_gross (Union[Unset, float]):
        labour (Union[Unset, float]):
        materials (Union[Unset, float]):
        taxable_gross (Union[Unset, float]):
        cis_deduction (Union[Unset, float]):
        umbrella_fee (Union[Unset, float]):
        vat (Union[Unset, float]):
        payment (Union[Unset, float]):
    """

    employee: Union[Unset, Item] = UNSET
    payroll_code: Union[Unset, None, str] = UNSET
    department: Union[Unset, None, str] = UNSET
    total_gross: Union[Unset, float] = UNSET
    labour: Union[Unset, float] = UNSET
    materials: Union[Unset, float] = UNSET
    taxable_gross: Union[Unset, float] = UNSET
    cis_deduction: Union[Unset, float] = UNSET
    umbrella_fee: Union[Unset, float] = UNSET
    vat: Union[Unset, float] = UNSET
    payment: Union[Unset, float] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        employee: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.employee, Unset):
            employee = self.employee.to_dict()

        payroll_code = self.payroll_code
        department = self.department
        total_gross = self.total_gross
        labour = self.labour
        materials = self.materials
        taxable_gross = self.taxable_gross
        cis_deduction = self.cis_deduction
        umbrella_fee = self.umbrella_fee
        vat = self.vat
        payment = self.payment

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if employee is not UNSET:
            field_dict["employee"] = employee
        if payroll_code is not UNSET:
            field_dict["payrollCode"] = payroll_code
        if department is not UNSET:
            field_dict["department"] = department
        if total_gross is not UNSET:
            field_dict["totalGross"] = total_gross
        if labour is not UNSET:
            field_dict["labour"] = labour
        if materials is not UNSET:
            field_dict["materials"] = materials
        if taxable_gross is not UNSET:
            field_dict["taxableGross"] = taxable_gross
        if cis_deduction is not UNSET:
            field_dict["cisDeduction"] = cis_deduction
        if umbrella_fee is not UNSET:
            field_dict["umbrellaFee"] = umbrella_fee
        if vat is not UNSET:
            field_dict["vat"] = vat
        if payment is not UNSET:
            field_dict["payment"] = payment

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

        department = d.pop("department", UNSET)

        total_gross = d.pop("totalGross", UNSET)

        labour = d.pop("labour", UNSET)

        materials = d.pop("materials", UNSET)

        taxable_gross = d.pop("taxableGross", UNSET)

        cis_deduction = d.pop("cisDeduction", UNSET)

        umbrella_fee = d.pop("umbrellaFee", UNSET)

        vat = d.pop("vat", UNSET)

        payment = d.pop("payment", UNSET)

        gross_to_net_report_cis_line = cls(
            employee=employee,
            payroll_code=payroll_code,
            department=department,
            total_gross=total_gross,
            labour=labour,
            materials=materials,
            taxable_gross=taxable_gross,
            cis_deduction=cis_deduction,
            umbrella_fee=umbrella_fee,
            vat=vat,
            payment=payment,
        )

        return gross_to_net_report_cis_line
