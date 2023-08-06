import datetime
from typing import Any, Dict, Type, TypeVar, Union

import attr
from dateutil.parser import isoparse

from ..types import UNSET, Unset

T = TypeVar("T", bound="P11PayeLine")


@attr.s(auto_attribs=True)
class P11PayeLine:
    """Lines for the Paye Income Tax table in the P11 Detailed report

    Attributes:
        date (Union[Unset, datetime.date]): [readonly]
        period (Union[Unset, None, str]): [readonly]
        month_number (Union[Unset, None, str]): [readonly]
        week_number (Union[Unset, None, str]): [readonly]
        gross_taxable_pay (Union[Unset, float]): [readonly]
        gross_taxable_pay_ytd (Union[Unset, float]): [readonly]
        tax (Union[Unset, float]): [readonly]
        tax_ytd (Union[Unset, float]): [readonly]
        student_loan (Union[Unset, float]): [readonly]
        postgrad_loan (Union[Unset, float]): [readonly]
        tax_code (Union[Unset, None, str]): [readonly]
    """

    date: Union[Unset, datetime.date] = UNSET
    period: Union[Unset, None, str] = UNSET
    month_number: Union[Unset, None, str] = UNSET
    week_number: Union[Unset, None, str] = UNSET
    gross_taxable_pay: Union[Unset, float] = UNSET
    gross_taxable_pay_ytd: Union[Unset, float] = UNSET
    tax: Union[Unset, float] = UNSET
    tax_ytd: Union[Unset, float] = UNSET
    student_loan: Union[Unset, float] = UNSET
    postgrad_loan: Union[Unset, float] = UNSET
    tax_code: Union[Unset, None, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        date: Union[Unset, str] = UNSET
        if not isinstance(self.date, Unset):
            date = self.date.isoformat()

        period = self.period
        month_number = self.month_number
        week_number = self.week_number
        gross_taxable_pay = self.gross_taxable_pay
        gross_taxable_pay_ytd = self.gross_taxable_pay_ytd
        tax = self.tax
        tax_ytd = self.tax_ytd
        student_loan = self.student_loan
        postgrad_loan = self.postgrad_loan
        tax_code = self.tax_code

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if date is not UNSET:
            field_dict["date"] = date
        if period is not UNSET:
            field_dict["period"] = period
        if month_number is not UNSET:
            field_dict["monthNumber"] = month_number
        if week_number is not UNSET:
            field_dict["weekNumber"] = week_number
        if gross_taxable_pay is not UNSET:
            field_dict["grossTaxablePay"] = gross_taxable_pay
        if gross_taxable_pay_ytd is not UNSET:
            field_dict["grossTaxablePayYTD"] = gross_taxable_pay_ytd
        if tax is not UNSET:
            field_dict["tax"] = tax
        if tax_ytd is not UNSET:
            field_dict["taxYTD"] = tax_ytd
        if student_loan is not UNSET:
            field_dict["studentLoan"] = student_loan
        if postgrad_loan is not UNSET:
            field_dict["postgradLoan"] = postgrad_loan
        if tax_code is not UNSET:
            field_dict["taxCode"] = tax_code

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        _date = d.pop("date", UNSET)
        date: Union[Unset, datetime.date]
        if isinstance(_date, Unset):
            date = UNSET
        else:
            date = isoparse(_date).date()

        period = d.pop("period", UNSET)

        month_number = d.pop("monthNumber", UNSET)

        week_number = d.pop("weekNumber", UNSET)

        gross_taxable_pay = d.pop("grossTaxablePay", UNSET)

        gross_taxable_pay_ytd = d.pop("grossTaxablePayYTD", UNSET)

        tax = d.pop("tax", UNSET)

        tax_ytd = d.pop("taxYTD", UNSET)

        student_loan = d.pop("studentLoan", UNSET)

        postgrad_loan = d.pop("postgradLoan", UNSET)

        tax_code = d.pop("taxCode", UNSET)

        p11_paye_line = cls(
            date=date,
            period=period,
            month_number=month_number,
            week_number=week_number,
            gross_taxable_pay=gross_taxable_pay,
            gross_taxable_pay_ytd=gross_taxable_pay_ytd,
            tax=tax,
            tax_ytd=tax_ytd,
            student_loan=student_loan,
            postgrad_loan=postgrad_loan,
            tax_code=tax_code,
        )

        return p11_paye_line
