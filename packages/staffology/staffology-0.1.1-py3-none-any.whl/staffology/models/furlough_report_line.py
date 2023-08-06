import datetime
from typing import Any, Dict, Type, TypeVar, Union

import attr
from dateutil.parser import isoparse

from ..models.item import Item
from ..types import UNSET, Unset

T = TypeVar("T", bound="FurloughReportLine")


@attr.s(auto_attribs=True)
class FurloughReportLine:
    """
    Attributes:
        employee (Union[Unset, Item]):
        employees_full_name (Union[Unset, None, str]):
        employees_nino (Union[Unset, None, str]):
        employees_payroll_reference_number (Union[Unset, None, str]):
        furloughed_days (Union[Unset, int]):
        days_in_period (Union[Unset, int]):
        hours_normally_worked (Union[Unset, None, float]):
        hours_furloughed (Union[Unset, None, float]):
        percentage_of_furloughed_days_worked (Union[Unset, float]):
        gross_pay (Union[Unset, float]):
        gross_pay_claim (Union[Unset, float]):
        ni_claim (Union[Unset, float]):
        pension_claim (Union[Unset, float]):
        total_claim (Union[Unset, float]):
        furlough_start (Union[Unset, None, datetime.date]):
        furlough_end (Union[Unset, None, datetime.date]):
        department (Union[Unset, None, str]):
    """

    employee: Union[Unset, Item] = UNSET
    employees_full_name: Union[Unset, None, str] = UNSET
    employees_nino: Union[Unset, None, str] = UNSET
    employees_payroll_reference_number: Union[Unset, None, str] = UNSET
    furloughed_days: Union[Unset, int] = UNSET
    days_in_period: Union[Unset, int] = UNSET
    hours_normally_worked: Union[Unset, None, float] = UNSET
    hours_furloughed: Union[Unset, None, float] = UNSET
    percentage_of_furloughed_days_worked: Union[Unset, float] = UNSET
    gross_pay: Union[Unset, float] = UNSET
    gross_pay_claim: Union[Unset, float] = UNSET
    ni_claim: Union[Unset, float] = UNSET
    pension_claim: Union[Unset, float] = UNSET
    total_claim: Union[Unset, float] = UNSET
    furlough_start: Union[Unset, None, datetime.date] = UNSET
    furlough_end: Union[Unset, None, datetime.date] = UNSET
    department: Union[Unset, None, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        employee: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.employee, Unset):
            employee = self.employee.to_dict()

        employees_full_name = self.employees_full_name
        employees_nino = self.employees_nino
        employees_payroll_reference_number = self.employees_payroll_reference_number
        furloughed_days = self.furloughed_days
        days_in_period = self.days_in_period
        hours_normally_worked = self.hours_normally_worked
        hours_furloughed = self.hours_furloughed
        percentage_of_furloughed_days_worked = self.percentage_of_furloughed_days_worked
        gross_pay = self.gross_pay
        gross_pay_claim = self.gross_pay_claim
        ni_claim = self.ni_claim
        pension_claim = self.pension_claim
        total_claim = self.total_claim
        furlough_start: Union[Unset, None, str] = UNSET
        if not isinstance(self.furlough_start, Unset):
            furlough_start = (
                self.furlough_start.isoformat() if self.furlough_start else None
            )

        furlough_end: Union[Unset, None, str] = UNSET
        if not isinstance(self.furlough_end, Unset):
            furlough_end = self.furlough_end.isoformat() if self.furlough_end else None

        department = self.department

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if employee is not UNSET:
            field_dict["employee"] = employee
        if employees_full_name is not UNSET:
            field_dict["employeesFullName"] = employees_full_name
        if employees_nino is not UNSET:
            field_dict["employeesNINO"] = employees_nino
        if employees_payroll_reference_number is not UNSET:
            field_dict[
                "employeesPayrollReferenceNumber"
            ] = employees_payroll_reference_number
        if furloughed_days is not UNSET:
            field_dict["furloughedDays"] = furloughed_days
        if days_in_period is not UNSET:
            field_dict["daysInPeriod"] = days_in_period
        if hours_normally_worked is not UNSET:
            field_dict["hoursNormallyWorked"] = hours_normally_worked
        if hours_furloughed is not UNSET:
            field_dict["hoursFurloughed"] = hours_furloughed
        if percentage_of_furloughed_days_worked is not UNSET:
            field_dict[
                "percentageOfFurloughedDaysWorked"
            ] = percentage_of_furloughed_days_worked
        if gross_pay is not UNSET:
            field_dict["grossPay"] = gross_pay
        if gross_pay_claim is not UNSET:
            field_dict["grossPayClaim"] = gross_pay_claim
        if ni_claim is not UNSET:
            field_dict["niClaim"] = ni_claim
        if pension_claim is not UNSET:
            field_dict["pensionClaim"] = pension_claim
        if total_claim is not UNSET:
            field_dict["totalClaim"] = total_claim
        if furlough_start is not UNSET:
            field_dict["furloughStart"] = furlough_start
        if furlough_end is not UNSET:
            field_dict["furloughEnd"] = furlough_end
        if department is not UNSET:
            field_dict["department"] = department

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

        employees_full_name = d.pop("employeesFullName", UNSET)

        employees_nino = d.pop("employeesNINO", UNSET)

        employees_payroll_reference_number = d.pop(
            "employeesPayrollReferenceNumber", UNSET
        )

        furloughed_days = d.pop("furloughedDays", UNSET)

        days_in_period = d.pop("daysInPeriod", UNSET)

        hours_normally_worked = d.pop("hoursNormallyWorked", UNSET)

        hours_furloughed = d.pop("hoursFurloughed", UNSET)

        percentage_of_furloughed_days_worked = d.pop(
            "percentageOfFurloughedDaysWorked", UNSET
        )

        gross_pay = d.pop("grossPay", UNSET)

        gross_pay_claim = d.pop("grossPayClaim", UNSET)

        ni_claim = d.pop("niClaim", UNSET)

        pension_claim = d.pop("pensionClaim", UNSET)

        total_claim = d.pop("totalClaim", UNSET)

        _furlough_start = d.pop("furloughStart", UNSET)
        furlough_start: Union[Unset, None, datetime.date]
        if _furlough_start is None:
            furlough_start = None
        elif isinstance(_furlough_start, Unset):
            furlough_start = UNSET
        else:
            furlough_start = isoparse(_furlough_start).date()

        _furlough_end = d.pop("furloughEnd", UNSET)
        furlough_end: Union[Unset, None, datetime.date]
        if _furlough_end is None:
            furlough_end = None
        elif isinstance(_furlough_end, Unset):
            furlough_end = UNSET
        else:
            furlough_end = isoparse(_furlough_end).date()

        department = d.pop("department", UNSET)

        furlough_report_line = cls(
            employee=employee,
            employees_full_name=employees_full_name,
            employees_nino=employees_nino,
            employees_payroll_reference_number=employees_payroll_reference_number,
            furloughed_days=furloughed_days,
            days_in_period=days_in_period,
            hours_normally_worked=hours_normally_worked,
            hours_furloughed=hours_furloughed,
            percentage_of_furloughed_days_worked=percentage_of_furloughed_days_worked,
            gross_pay=gross_pay,
            gross_pay_claim=gross_pay_claim,
            ni_claim=ni_claim,
            pension_claim=pension_claim,
            total_claim=total_claim,
            furlough_start=furlough_start,
            furlough_end=furlough_end,
            department=department,
        )

        return furlough_report_line
