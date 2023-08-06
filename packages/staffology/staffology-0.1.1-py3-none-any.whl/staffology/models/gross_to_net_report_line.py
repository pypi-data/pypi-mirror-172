from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..models.item import Item
from ..types import UNSET, Unset

T = TypeVar("T", bound="GrossToNetReportLine")


@attr.s(auto_attribs=True)
class GrossToNetReportLine:
    """
    Attributes:
        total_gross (Union[Unset, float]):
        taxable_gross (Union[Unset, float]):
        net_pay (Union[Unset, float]):
        tax (Union[Unset, float]):
        employee_ni (Union[Unset, float]):
        employer_ni (Union[Unset, float]):
        employee_pension (Union[Unset, float]):
        employer_pension (Union[Unset, float]):
        student_or_pg_loan (Union[Unset, float]):
        statutory_payments (Union[Unset, float]):
        attachments (Union[Unset, float]):
        other_deductions (Union[Unset, float]):
        employee (Union[Unset, Item]):
        payroll_code (Union[Unset, None, str]):
        department (Union[Unset, None, str]):
    """

    total_gross: Union[Unset, float] = UNSET
    taxable_gross: Union[Unset, float] = UNSET
    net_pay: Union[Unset, float] = UNSET
    tax: Union[Unset, float] = UNSET
    employee_ni: Union[Unset, float] = UNSET
    employer_ni: Union[Unset, float] = UNSET
    employee_pension: Union[Unset, float] = UNSET
    employer_pension: Union[Unset, float] = UNSET
    student_or_pg_loan: Union[Unset, float] = UNSET
    statutory_payments: Union[Unset, float] = UNSET
    attachments: Union[Unset, float] = UNSET
    other_deductions: Union[Unset, float] = UNSET
    employee: Union[Unset, Item] = UNSET
    payroll_code: Union[Unset, None, str] = UNSET
    department: Union[Unset, None, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        total_gross = self.total_gross
        taxable_gross = self.taxable_gross
        net_pay = self.net_pay
        tax = self.tax
        employee_ni = self.employee_ni
        employer_ni = self.employer_ni
        employee_pension = self.employee_pension
        employer_pension = self.employer_pension
        student_or_pg_loan = self.student_or_pg_loan
        statutory_payments = self.statutory_payments
        attachments = self.attachments
        other_deductions = self.other_deductions
        employee: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.employee, Unset):
            employee = self.employee.to_dict()

        payroll_code = self.payroll_code
        department = self.department

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if total_gross is not UNSET:
            field_dict["totalGross"] = total_gross
        if taxable_gross is not UNSET:
            field_dict["taxableGross"] = taxable_gross
        if net_pay is not UNSET:
            field_dict["netPay"] = net_pay
        if tax is not UNSET:
            field_dict["tax"] = tax
        if employee_ni is not UNSET:
            field_dict["employeeNi"] = employee_ni
        if employer_ni is not UNSET:
            field_dict["employerNi"] = employer_ni
        if employee_pension is not UNSET:
            field_dict["employeePension"] = employee_pension
        if employer_pension is not UNSET:
            field_dict["employerPension"] = employer_pension
        if student_or_pg_loan is not UNSET:
            field_dict["studentOrPgLoan"] = student_or_pg_loan
        if statutory_payments is not UNSET:
            field_dict["statutoryPayments"] = statutory_payments
        if attachments is not UNSET:
            field_dict["attachments"] = attachments
        if other_deductions is not UNSET:
            field_dict["otherDeductions"] = other_deductions
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
        total_gross = d.pop("totalGross", UNSET)

        taxable_gross = d.pop("taxableGross", UNSET)

        net_pay = d.pop("netPay", UNSET)

        tax = d.pop("tax", UNSET)

        employee_ni = d.pop("employeeNi", UNSET)

        employer_ni = d.pop("employerNi", UNSET)

        employee_pension = d.pop("employeePension", UNSET)

        employer_pension = d.pop("employerPension", UNSET)

        student_or_pg_loan = d.pop("studentOrPgLoan", UNSET)

        statutory_payments = d.pop("statutoryPayments", UNSET)

        attachments = d.pop("attachments", UNSET)

        other_deductions = d.pop("otherDeductions", UNSET)

        _employee = d.pop("employee", UNSET)
        employee: Union[Unset, Item]
        if isinstance(_employee, Unset):
            employee = UNSET
        else:
            employee = Item.from_dict(_employee)

        payroll_code = d.pop("payrollCode", UNSET)

        department = d.pop("department", UNSET)

        gross_to_net_report_line = cls(
            total_gross=total_gross,
            taxable_gross=taxable_gross,
            net_pay=net_pay,
            tax=tax,
            employee_ni=employee_ni,
            employer_ni=employer_ni,
            employee_pension=employee_pension,
            employer_pension=employer_pension,
            student_or_pg_loan=student_or_pg_loan,
            statutory_payments=statutory_payments,
            attachments=attachments,
            other_deductions=other_deductions,
            employee=employee,
            payroll_code=payroll_code,
            department=department,
        )

        return gross_to_net_report_line
