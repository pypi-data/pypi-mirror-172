from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="P11PayeTotalsLine")


@attr.s(auto_attribs=True)
class P11PayeTotalsLine:
    """Summary line for the Paye Income Tax table in the P11 Detailed report

    Attributes:
        student_loan (Union[Unset, float]): [readonly]
        postgrad_loan (Union[Unset, float]): [readonly]
        pay (Union[Unset, float]): [readonly]
        total_pay_to_date (Union[Unset, float]): [readonly]
        tax_due_to_date (Union[Unset, float]): [readonly]
        tax_due (Union[Unset, float]): [readonly]
    """

    student_loan: Union[Unset, float] = UNSET
    postgrad_loan: Union[Unset, float] = UNSET
    pay: Union[Unset, float] = UNSET
    total_pay_to_date: Union[Unset, float] = UNSET
    tax_due_to_date: Union[Unset, float] = UNSET
    tax_due: Union[Unset, float] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        student_loan = self.student_loan
        postgrad_loan = self.postgrad_loan
        pay = self.pay
        total_pay_to_date = self.total_pay_to_date
        tax_due_to_date = self.tax_due_to_date
        tax_due = self.tax_due

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if student_loan is not UNSET:
            field_dict["studentLoan"] = student_loan
        if postgrad_loan is not UNSET:
            field_dict["postgradLoan"] = postgrad_loan
        if pay is not UNSET:
            field_dict["pay"] = pay
        if total_pay_to_date is not UNSET:
            field_dict["totalPayToDate"] = total_pay_to_date
        if tax_due_to_date is not UNSET:
            field_dict["taxDueToDate"] = tax_due_to_date
        if tax_due is not UNSET:
            field_dict["taxDue"] = tax_due

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        student_loan = d.pop("studentLoan", UNSET)

        postgrad_loan = d.pop("postgradLoan", UNSET)

        pay = d.pop("pay", UNSET)

        total_pay_to_date = d.pop("totalPayToDate", UNSET)

        tax_due_to_date = d.pop("taxDueToDate", UNSET)

        tax_due = d.pop("taxDue", UNSET)

        p11_paye_totals_line = cls(
            student_loan=student_loan,
            postgrad_loan=postgrad_loan,
            pay=pay,
            total_pay_to_date=total_pay_to_date,
            tax_due_to_date=tax_due_to_date,
            tax_due=tax_due,
        )

        return p11_paye_totals_line
