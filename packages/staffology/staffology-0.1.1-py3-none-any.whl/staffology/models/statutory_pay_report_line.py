from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..models.item import Item
from ..types import UNSET, Unset

T = TypeVar("T", bound="StatutoryPayReportLine")


@attr.s(auto_attribs=True)
class StatutoryPayReportLine:
    """
    Attributes:
        employee (Union[Unset, Item]):
        payroll_code (Union[Unset, None, str]):
        department (Union[Unset, None, str]):
        smp (Union[Unset, float]):
        spp (Union[Unset, float]):
        sap (Union[Unset, float]):
        shpp (Union[Unset, float]):
        spbp (Union[Unset, float]):
        total_stat_pay (Union[Unset, float]):
    """

    employee: Union[Unset, Item] = UNSET
    payroll_code: Union[Unset, None, str] = UNSET
    department: Union[Unset, None, str] = UNSET
    smp: Union[Unset, float] = UNSET
    spp: Union[Unset, float] = UNSET
    sap: Union[Unset, float] = UNSET
    shpp: Union[Unset, float] = UNSET
    spbp: Union[Unset, float] = UNSET
    total_stat_pay: Union[Unset, float] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        employee: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.employee, Unset):
            employee = self.employee.to_dict()

        payroll_code = self.payroll_code
        department = self.department
        smp = self.smp
        spp = self.spp
        sap = self.sap
        shpp = self.shpp
        spbp = self.spbp
        total_stat_pay = self.total_stat_pay

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if employee is not UNSET:
            field_dict["employee"] = employee
        if payroll_code is not UNSET:
            field_dict["payrollCode"] = payroll_code
        if department is not UNSET:
            field_dict["department"] = department
        if smp is not UNSET:
            field_dict["smp"] = smp
        if spp is not UNSET:
            field_dict["spp"] = spp
        if sap is not UNSET:
            field_dict["sap"] = sap
        if shpp is not UNSET:
            field_dict["shpp"] = shpp
        if spbp is not UNSET:
            field_dict["spbp"] = spbp
        if total_stat_pay is not UNSET:
            field_dict["totalStatPay"] = total_stat_pay

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

        smp = d.pop("smp", UNSET)

        spp = d.pop("spp", UNSET)

        sap = d.pop("sap", UNSET)

        shpp = d.pop("shpp", UNSET)

        spbp = d.pop("spbp", UNSET)

        total_stat_pay = d.pop("totalStatPay", UNSET)

        statutory_pay_report_line = cls(
            employee=employee,
            payroll_code=payroll_code,
            department=department,
            smp=smp,
            spp=spp,
            sap=sap,
            shpp=shpp,
            spbp=spbp,
            total_stat_pay=total_stat_pay,
        )

        return statutory_pay_report_line
