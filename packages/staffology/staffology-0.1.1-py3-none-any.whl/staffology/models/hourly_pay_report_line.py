from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..models.item import Item
from ..types import UNSET, Unset

T = TypeVar("T", bound="HourlyPayReportLine")


@attr.s(auto_attribs=True)
class HourlyPayReportLine:
    """
    Attributes:
        employee (Union[Unset, Item]):
        payroll_code (Union[Unset, None, str]):
        pay_code (Union[Unset, None, str]):
        period (Union[Unset, int]):
        hours (Union[Unset, float]):
        rate (Union[Unset, float]):
        total (Union[Unset, float]):
    """

    employee: Union[Unset, Item] = UNSET
    payroll_code: Union[Unset, None, str] = UNSET
    pay_code: Union[Unset, None, str] = UNSET
    period: Union[Unset, int] = UNSET
    hours: Union[Unset, float] = UNSET
    rate: Union[Unset, float] = UNSET
    total: Union[Unset, float] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        employee: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.employee, Unset):
            employee = self.employee.to_dict()

        payroll_code = self.payroll_code
        pay_code = self.pay_code
        period = self.period
        hours = self.hours
        rate = self.rate
        total = self.total

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if employee is not UNSET:
            field_dict["employee"] = employee
        if payroll_code is not UNSET:
            field_dict["payrollCode"] = payroll_code
        if pay_code is not UNSET:
            field_dict["payCode"] = pay_code
        if period is not UNSET:
            field_dict["period"] = period
        if hours is not UNSET:
            field_dict["hours"] = hours
        if rate is not UNSET:
            field_dict["rate"] = rate
        if total is not UNSET:
            field_dict["total"] = total

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

        pay_code = d.pop("payCode", UNSET)

        period = d.pop("period", UNSET)

        hours = d.pop("hours", UNSET)

        rate = d.pop("rate", UNSET)

        total = d.pop("total", UNSET)

        hourly_pay_report_line = cls(
            employee=employee,
            payroll_code=payroll_code,
            pay_code=pay_code,
            period=period,
            hours=hours,
            rate=rate,
            total=total,
        )

        return hourly_pay_report_line
