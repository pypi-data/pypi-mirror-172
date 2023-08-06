from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="UmbrellaPayment")


@attr.s(auto_attribs=True)
class UmbrellaPayment:
    """
    Attributes:
        payroll_code (Union[Unset, None, str]): When importing multiple UmbrellaPayments this field is used to identify
            the employee
        charge_per_timesheet (Union[Unset, None, float]): Override the settings for this employer by specifying a
            ChargePerTimeSheet.
            Or leave it as null to use the settings from the Employer
        invoice_value (Union[Unset, float]):
        maps_miles (Union[Unset, int]):
        other_expenses (Union[Unset, float]):
        number_of_timesheets (Union[Unset, int]):
        hours_worked (Union[Unset, float]):
        gross_deduction (Union[Unset, float]):
        gross_addition (Union[Unset, float]):
    """

    payroll_code: Union[Unset, None, str] = UNSET
    charge_per_timesheet: Union[Unset, None, float] = UNSET
    invoice_value: Union[Unset, float] = UNSET
    maps_miles: Union[Unset, int] = UNSET
    other_expenses: Union[Unset, float] = UNSET
    number_of_timesheets: Union[Unset, int] = UNSET
    hours_worked: Union[Unset, float] = UNSET
    gross_deduction: Union[Unset, float] = UNSET
    gross_addition: Union[Unset, float] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        payroll_code = self.payroll_code
        charge_per_timesheet = self.charge_per_timesheet
        invoice_value = self.invoice_value
        maps_miles = self.maps_miles
        other_expenses = self.other_expenses
        number_of_timesheets = self.number_of_timesheets
        hours_worked = self.hours_worked
        gross_deduction = self.gross_deduction
        gross_addition = self.gross_addition

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if payroll_code is not UNSET:
            field_dict["payrollCode"] = payroll_code
        if charge_per_timesheet is not UNSET:
            field_dict["chargePerTimesheet"] = charge_per_timesheet
        if invoice_value is not UNSET:
            field_dict["invoiceValue"] = invoice_value
        if maps_miles is not UNSET:
            field_dict["mapsMiles"] = maps_miles
        if other_expenses is not UNSET:
            field_dict["otherExpenses"] = other_expenses
        if number_of_timesheets is not UNSET:
            field_dict["numberOfTimesheets"] = number_of_timesheets
        if hours_worked is not UNSET:
            field_dict["hoursWorked"] = hours_worked
        if gross_deduction is not UNSET:
            field_dict["grossDeduction"] = gross_deduction
        if gross_addition is not UNSET:
            field_dict["grossAddition"] = gross_addition

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        payroll_code = d.pop("payrollCode", UNSET)

        charge_per_timesheet = d.pop("chargePerTimesheet", UNSET)

        invoice_value = d.pop("invoiceValue", UNSET)

        maps_miles = d.pop("mapsMiles", UNSET)

        other_expenses = d.pop("otherExpenses", UNSET)

        number_of_timesheets = d.pop("numberOfTimesheets", UNSET)

        hours_worked = d.pop("hoursWorked", UNSET)

        gross_deduction = d.pop("grossDeduction", UNSET)

        gross_addition = d.pop("grossAddition", UNSET)

        umbrella_payment = cls(
            payroll_code=payroll_code,
            charge_per_timesheet=charge_per_timesheet,
            invoice_value=invoice_value,
            maps_miles=maps_miles,
            other_expenses=other_expenses,
            number_of_timesheets=number_of_timesheets,
            hours_worked=hours_worked,
            gross_deduction=gross_deduction,
            gross_addition=gross_addition,
        )

        return umbrella_payment
