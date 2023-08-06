from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..models.item import Item
from ..types import UNSET, Unset

T = TypeVar("T", bound="CostOfEmploymentReportLine")


@attr.s(auto_attribs=True)
class CostOfEmploymentReportLine:
    """
    Attributes:
        pay (Union[Unset, float]):
        employer_nic (Union[Unset, float]):
        pension (Union[Unset, float]):
        aeo_fees (Union[Unset, float]):
        stat_pay_reclaim (Union[Unset, float]):
        total_cost (Union[Unset, float]):
        employee (Union[Unset, Item]):
        payroll_code (Union[Unset, None, str]):
        department (Union[Unset, None, str]):
    """

    pay: Union[Unset, float] = UNSET
    employer_nic: Union[Unset, float] = UNSET
    pension: Union[Unset, float] = UNSET
    aeo_fees: Union[Unset, float] = UNSET
    stat_pay_reclaim: Union[Unset, float] = UNSET
    total_cost: Union[Unset, float] = UNSET
    employee: Union[Unset, Item] = UNSET
    payroll_code: Union[Unset, None, str] = UNSET
    department: Union[Unset, None, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        pay = self.pay
        employer_nic = self.employer_nic
        pension = self.pension
        aeo_fees = self.aeo_fees
        stat_pay_reclaim = self.stat_pay_reclaim
        total_cost = self.total_cost
        employee: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.employee, Unset):
            employee = self.employee.to_dict()

        payroll_code = self.payroll_code
        department = self.department

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if pay is not UNSET:
            field_dict["pay"] = pay
        if employer_nic is not UNSET:
            field_dict["employerNic"] = employer_nic
        if pension is not UNSET:
            field_dict["pension"] = pension
        if aeo_fees is not UNSET:
            field_dict["aeoFees"] = aeo_fees
        if stat_pay_reclaim is not UNSET:
            field_dict["statPayReclaim"] = stat_pay_reclaim
        if total_cost is not UNSET:
            field_dict["totalCost"] = total_cost
        if employee is not UNSET:
            field_dict["employee"] = employee
        if payroll_code is not UNSET:
            field_dict["payrollCode"] = payroll_code
        if department is not UNSET:
            field_dict["department"] = department

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        pay = d.pop("pay", UNSET)

        employer_nic = d.pop("employerNic", UNSET)

        pension = d.pop("pension", UNSET)

        aeo_fees = d.pop("aeoFees", UNSET)

        stat_pay_reclaim = d.pop("statPayReclaim", UNSET)

        total_cost = d.pop("totalCost", UNSET)

        _employee = d.pop("employee", UNSET)
        employee: Union[Unset, Item]
        if isinstance(_employee, Unset):
            employee = UNSET
        else:
            employee = Item.from_dict(_employee)

        payroll_code = d.pop("payrollCode", UNSET)

        department = d.pop("department", UNSET)

        cost_of_employment_report_line = cls(
            pay=pay,
            employer_nic=employer_nic,
            pension=pension,
            aeo_fees=aeo_fees,
            stat_pay_reclaim=stat_pay_reclaim,
            total_cost=total_cost,
            employee=employee,
            payroll_code=payroll_code,
            department=department,
        )

        return cost_of_employment_report_line
