from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="FpsEmployerPayIdChanged")


@attr.s(auto_attribs=True)
class FpsEmployerPayIdChanged:
    """
    Attributes:
        payroll_id_changed_indicator (Union[Unset, None, str]):
        old_payroll_id (Union[Unset, None, str]):
    """

    payroll_id_changed_indicator: Union[Unset, None, str] = UNSET
    old_payroll_id: Union[Unset, None, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        payroll_id_changed_indicator = self.payroll_id_changed_indicator
        old_payroll_id = self.old_payroll_id

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if payroll_id_changed_indicator is not UNSET:
            field_dict["payrollIdChangedIndicator"] = payroll_id_changed_indicator
        if old_payroll_id is not UNSET:
            field_dict["oldPayrollId"] = old_payroll_id

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        payroll_id_changed_indicator = d.pop("payrollIdChangedIndicator", UNSET)

        old_payroll_id = d.pop("oldPayrollId", UNSET)

        fps_employer_pay_id_changed = cls(
            payroll_id_changed_indicator=payroll_id_changed_indicator,
            old_payroll_id=old_payroll_id,
        )

        return fps_employer_pay_id_changed
