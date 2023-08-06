from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..models.item import Item
from ..models.right_to_work import RightToWork
from ..types import UNSET, Unset

T = TypeVar("T", bound="RightToWorkReportLine")


@attr.s(auto_attribs=True)
class RightToWorkReportLine:
    """
    Attributes:
        employee (Union[Unset, Item]):
        payroll_code (Union[Unset, None, str]):
        department (Union[Unset, None, str]):
        right_to_work (Union[Unset, RightToWork]):
    """

    employee: Union[Unset, Item] = UNSET
    payroll_code: Union[Unset, None, str] = UNSET
    department: Union[Unset, None, str] = UNSET
    right_to_work: Union[Unset, RightToWork] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        employee: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.employee, Unset):
            employee = self.employee.to_dict()

        payroll_code = self.payroll_code
        department = self.department
        right_to_work: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.right_to_work, Unset):
            right_to_work = self.right_to_work.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if employee is not UNSET:
            field_dict["employee"] = employee
        if payroll_code is not UNSET:
            field_dict["payrollCode"] = payroll_code
        if department is not UNSET:
            field_dict["department"] = department
        if right_to_work is not UNSET:
            field_dict["rightToWork"] = right_to_work

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

        _right_to_work = d.pop("rightToWork", UNSET)
        right_to_work: Union[Unset, RightToWork]
        if isinstance(_right_to_work, Unset):
            right_to_work = UNSET
        else:
            right_to_work = RightToWork.from_dict(_right_to_work)

        right_to_work_report_line = cls(
            employee=employee,
            payroll_code=payroll_code,
            department=department,
            right_to_work=right_to_work,
        )

        return right_to_work_report_line
