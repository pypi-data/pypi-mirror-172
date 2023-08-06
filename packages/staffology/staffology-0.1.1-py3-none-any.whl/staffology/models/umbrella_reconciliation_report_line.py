from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..models.item import Item
from ..types import UNSET, Unset

T = TypeVar("T", bound="UmbrellaReconciliationReportLine")


@attr.s(auto_attribs=True)
class UmbrellaReconciliationReportLine:
    """
    Attributes:
        employee (Union[Unset, Item]):
        period (Union[Unset, None, str]):
        payroll_code (Union[Unset, None, str]):
        department (Union[Unset, None, str]):
        total_gross (Union[Unset, float]):
        net_pay (Union[Unset, float]):
        tax (Union[Unset, float]):
        employee_ni (Union[Unset, float]):
        employer_ni (Union[Unset, float]):
        employee_pension (Union[Unset, float]):
        employer_pension (Union[Unset, float]):
        expenses (Union[Unset, float]):
        fee (Union[Unset, float]):
        app_levy (Union[Unset, float]):
        invoice_value (Union[Unset, float]):
        employee_costs (Union[Unset, float]):
        employer_costs (Union[Unset, float]):
        total (Union[Unset, float]):
    """

    employee: Union[Unset, Item] = UNSET
    period: Union[Unset, None, str] = UNSET
    payroll_code: Union[Unset, None, str] = UNSET
    department: Union[Unset, None, str] = UNSET
    total_gross: Union[Unset, float] = UNSET
    net_pay: Union[Unset, float] = UNSET
    tax: Union[Unset, float] = UNSET
    employee_ni: Union[Unset, float] = UNSET
    employer_ni: Union[Unset, float] = UNSET
    employee_pension: Union[Unset, float] = UNSET
    employer_pension: Union[Unset, float] = UNSET
    expenses: Union[Unset, float] = UNSET
    fee: Union[Unset, float] = UNSET
    app_levy: Union[Unset, float] = UNSET
    invoice_value: Union[Unset, float] = UNSET
    employee_costs: Union[Unset, float] = UNSET
    employer_costs: Union[Unset, float] = UNSET
    total: Union[Unset, float] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        employee: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.employee, Unset):
            employee = self.employee.to_dict()

        period = self.period
        payroll_code = self.payroll_code
        department = self.department
        total_gross = self.total_gross
        net_pay = self.net_pay
        tax = self.tax
        employee_ni = self.employee_ni
        employer_ni = self.employer_ni
        employee_pension = self.employee_pension
        employer_pension = self.employer_pension
        expenses = self.expenses
        fee = self.fee
        app_levy = self.app_levy
        invoice_value = self.invoice_value
        employee_costs = self.employee_costs
        employer_costs = self.employer_costs
        total = self.total

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if employee is not UNSET:
            field_dict["employee"] = employee
        if period is not UNSET:
            field_dict["period"] = period
        if payroll_code is not UNSET:
            field_dict["payrollCode"] = payroll_code
        if department is not UNSET:
            field_dict["department"] = department
        if total_gross is not UNSET:
            field_dict["totalGross"] = total_gross
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
        if expenses is not UNSET:
            field_dict["expenses"] = expenses
        if fee is not UNSET:
            field_dict["fee"] = fee
        if app_levy is not UNSET:
            field_dict["appLevy"] = app_levy
        if invoice_value is not UNSET:
            field_dict["invoiceValue"] = invoice_value
        if employee_costs is not UNSET:
            field_dict["employeeCosts"] = employee_costs
        if employer_costs is not UNSET:
            field_dict["employerCosts"] = employer_costs
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

        period = d.pop("period", UNSET)

        payroll_code = d.pop("payrollCode", UNSET)

        department = d.pop("department", UNSET)

        total_gross = d.pop("totalGross", UNSET)

        net_pay = d.pop("netPay", UNSET)

        tax = d.pop("tax", UNSET)

        employee_ni = d.pop("employeeNi", UNSET)

        employer_ni = d.pop("employerNi", UNSET)

        employee_pension = d.pop("employeePension", UNSET)

        employer_pension = d.pop("employerPension", UNSET)

        expenses = d.pop("expenses", UNSET)

        fee = d.pop("fee", UNSET)

        app_levy = d.pop("appLevy", UNSET)

        invoice_value = d.pop("invoiceValue", UNSET)

        employee_costs = d.pop("employeeCosts", UNSET)

        employer_costs = d.pop("employerCosts", UNSET)

        total = d.pop("total", UNSET)

        umbrella_reconciliation_report_line = cls(
            employee=employee,
            period=period,
            payroll_code=payroll_code,
            department=department,
            total_gross=total_gross,
            net_pay=net_pay,
            tax=tax,
            employee_ni=employee_ni,
            employer_ni=employer_ni,
            employee_pension=employee_pension,
            employer_pension=employer_pension,
            expenses=expenses,
            fee=fee,
            app_levy=app_levy,
            invoice_value=invoice_value,
            employee_costs=employee_costs,
            employer_costs=employer_costs,
            total=total,
        )

        return umbrella_reconciliation_report_line
