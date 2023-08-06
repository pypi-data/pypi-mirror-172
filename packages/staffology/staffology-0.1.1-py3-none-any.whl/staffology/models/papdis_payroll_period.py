import datetime
from typing import Any, Dict, List, Type, TypeVar, Union

import attr
from dateutil.parser import isoparse

from ..models.papdis_employee import PapdisEmployee
from ..types import UNSET, Unset

T = TypeVar("T", bound="PapdisPayrollPeriod")


@attr.s(auto_attribs=True)
class PapdisPayrollPeriod:
    """
    Attributes:
        pay_period_start_date (Union[Unset, datetime.date]): [readonly]
        pay_period_end_date (Union[Unset, datetime.date]): [readonly]
        contribution_deduction_date (Union[Unset, datetime.date]): [readonly]
        frequency_code (Union[Unset, None, str]): [readonly]
        tax_period (Union[Unset, int]): [readonly]
        pay_reference_start_date (Union[Unset, datetime.date]): [readonly]
        pay_reference_end_date (Union[Unset, datetime.date]): [readonly]
        employees (Union[Unset, None, List[PapdisEmployee]]): [readonly] Employees and contributions made in this period
    """

    pay_period_start_date: Union[Unset, datetime.date] = UNSET
    pay_period_end_date: Union[Unset, datetime.date] = UNSET
    contribution_deduction_date: Union[Unset, datetime.date] = UNSET
    frequency_code: Union[Unset, None, str] = UNSET
    tax_period: Union[Unset, int] = UNSET
    pay_reference_start_date: Union[Unset, datetime.date] = UNSET
    pay_reference_end_date: Union[Unset, datetime.date] = UNSET
    employees: Union[Unset, None, List[PapdisEmployee]] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        pay_period_start_date: Union[Unset, str] = UNSET
        if not isinstance(self.pay_period_start_date, Unset):
            pay_period_start_date = self.pay_period_start_date.isoformat()

        pay_period_end_date: Union[Unset, str] = UNSET
        if not isinstance(self.pay_period_end_date, Unset):
            pay_period_end_date = self.pay_period_end_date.isoformat()

        contribution_deduction_date: Union[Unset, str] = UNSET
        if not isinstance(self.contribution_deduction_date, Unset):
            contribution_deduction_date = self.contribution_deduction_date.isoformat()

        frequency_code = self.frequency_code
        tax_period = self.tax_period
        pay_reference_start_date: Union[Unset, str] = UNSET
        if not isinstance(self.pay_reference_start_date, Unset):
            pay_reference_start_date = self.pay_reference_start_date.isoformat()

        pay_reference_end_date: Union[Unset, str] = UNSET
        if not isinstance(self.pay_reference_end_date, Unset):
            pay_reference_end_date = self.pay_reference_end_date.isoformat()

        employees: Union[Unset, None, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.employees, Unset):
            if self.employees is None:
                employees = None
            else:
                employees = []
                for employees_item_data in self.employees:
                    employees_item = employees_item_data.to_dict()

                    employees.append(employees_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if pay_period_start_date is not UNSET:
            field_dict["payPeriodStartDate"] = pay_period_start_date
        if pay_period_end_date is not UNSET:
            field_dict["payPeriodEndDate"] = pay_period_end_date
        if contribution_deduction_date is not UNSET:
            field_dict["contributionDeductionDate"] = contribution_deduction_date
        if frequency_code is not UNSET:
            field_dict["frequencyCode"] = frequency_code
        if tax_period is not UNSET:
            field_dict["taxPeriod"] = tax_period
        if pay_reference_start_date is not UNSET:
            field_dict["payReferenceStartDate"] = pay_reference_start_date
        if pay_reference_end_date is not UNSET:
            field_dict["payReferenceEndDate"] = pay_reference_end_date
        if employees is not UNSET:
            field_dict["employees"] = employees

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        _pay_period_start_date = d.pop("payPeriodStartDate", UNSET)
        pay_period_start_date: Union[Unset, datetime.date]
        if isinstance(_pay_period_start_date, Unset):
            pay_period_start_date = UNSET
        else:
            pay_period_start_date = isoparse(_pay_period_start_date).date()

        _pay_period_end_date = d.pop("payPeriodEndDate", UNSET)
        pay_period_end_date: Union[Unset, datetime.date]
        if isinstance(_pay_period_end_date, Unset):
            pay_period_end_date = UNSET
        else:
            pay_period_end_date = isoparse(_pay_period_end_date).date()

        _contribution_deduction_date = d.pop("contributionDeductionDate", UNSET)
        contribution_deduction_date: Union[Unset, datetime.date]
        if isinstance(_contribution_deduction_date, Unset):
            contribution_deduction_date = UNSET
        else:
            contribution_deduction_date = isoparse(_contribution_deduction_date).date()

        frequency_code = d.pop("frequencyCode", UNSET)

        tax_period = d.pop("taxPeriod", UNSET)

        _pay_reference_start_date = d.pop("payReferenceStartDate", UNSET)
        pay_reference_start_date: Union[Unset, datetime.date]
        if isinstance(_pay_reference_start_date, Unset):
            pay_reference_start_date = UNSET
        else:
            pay_reference_start_date = isoparse(_pay_reference_start_date).date()

        _pay_reference_end_date = d.pop("payReferenceEndDate", UNSET)
        pay_reference_end_date: Union[Unset, datetime.date]
        if isinstance(_pay_reference_end_date, Unset):
            pay_reference_end_date = UNSET
        else:
            pay_reference_end_date = isoparse(_pay_reference_end_date).date()

        employees = []
        _employees = d.pop("employees", UNSET)
        for employees_item_data in _employees or []:
            employees_item = PapdisEmployee.from_dict(employees_item_data)

            employees.append(employees_item)

        papdis_payroll_period = cls(
            pay_period_start_date=pay_period_start_date,
            pay_period_end_date=pay_period_end_date,
            contribution_deduction_date=contribution_deduction_date,
            frequency_code=frequency_code,
            tax_period=tax_period,
            pay_reference_start_date=pay_reference_start_date,
            pay_reference_end_date=pay_reference_end_date,
            employees=employees,
        )

        return papdis_payroll_period
