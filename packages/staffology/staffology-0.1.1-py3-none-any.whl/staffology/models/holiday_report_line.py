from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..models.item import Item
from ..models.leave_settings import LeaveSettings
from ..types import UNSET, Unset

T = TypeVar("T", bound="HolidayReportLine")


@attr.s(auto_attribs=True)
class HolidayReportLine:
    """
    Attributes:
        employee (Union[Unset, Item]):
        payroll_code (Union[Unset, None, str]):
        department (Union[Unset, None, str]):
        day_rate (Union[Unset, None, float]):
        leave_settings (Union[Unset, LeaveSettings]):
    """

    employee: Union[Unset, Item] = UNSET
    payroll_code: Union[Unset, None, str] = UNSET
    department: Union[Unset, None, str] = UNSET
    day_rate: Union[Unset, None, float] = UNSET
    leave_settings: Union[Unset, LeaveSettings] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        employee: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.employee, Unset):
            employee = self.employee.to_dict()

        payroll_code = self.payroll_code
        department = self.department
        day_rate = self.day_rate
        leave_settings: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.leave_settings, Unset):
            leave_settings = self.leave_settings.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if employee is not UNSET:
            field_dict["employee"] = employee
        if payroll_code is not UNSET:
            field_dict["payrollCode"] = payroll_code
        if department is not UNSET:
            field_dict["department"] = department
        if day_rate is not UNSET:
            field_dict["dayRate"] = day_rate
        if leave_settings is not UNSET:
            field_dict["leaveSettings"] = leave_settings

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

        day_rate = d.pop("dayRate", UNSET)

        _leave_settings = d.pop("leaveSettings", UNSET)
        leave_settings: Union[Unset, LeaveSettings]
        if isinstance(_leave_settings, Unset):
            leave_settings = UNSET
        else:
            leave_settings = LeaveSettings.from_dict(_leave_settings)

        holiday_report_line = cls(
            employee=employee,
            payroll_code=payroll_code,
            department=department,
            day_rate=day_rate,
            leave_settings=leave_settings,
        )

        return holiday_report_line
