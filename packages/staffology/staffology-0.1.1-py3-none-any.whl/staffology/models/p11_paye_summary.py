from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="P11PayeSummary")


@attr.s(auto_attribs=True)
class P11PayeSummary:
    """Forms the PAYE summary in the P11 Detailed report

    Attributes:
        previous_employment_pay (Union[Unset, float]): [readonly]
        previous_employment_tax (Union[Unset, float]): [readonly]
        this_employment_pay (Union[Unset, float]): [readonly]
        this_employment_tax (Union[Unset, float]): [readonly]
        total_pay_for_year (Union[Unset, float]): [readonly]
        total_tax_for_year (Union[Unset, float]): [readonly]
    """

    previous_employment_pay: Union[Unset, float] = UNSET
    previous_employment_tax: Union[Unset, float] = UNSET
    this_employment_pay: Union[Unset, float] = UNSET
    this_employment_tax: Union[Unset, float] = UNSET
    total_pay_for_year: Union[Unset, float] = UNSET
    total_tax_for_year: Union[Unset, float] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        previous_employment_pay = self.previous_employment_pay
        previous_employment_tax = self.previous_employment_tax
        this_employment_pay = self.this_employment_pay
        this_employment_tax = self.this_employment_tax
        total_pay_for_year = self.total_pay_for_year
        total_tax_for_year = self.total_tax_for_year

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if previous_employment_pay is not UNSET:
            field_dict["previousEmploymentPay"] = previous_employment_pay
        if previous_employment_tax is not UNSET:
            field_dict["previousEmploymentTax"] = previous_employment_tax
        if this_employment_pay is not UNSET:
            field_dict["thisEmploymentPay"] = this_employment_pay
        if this_employment_tax is not UNSET:
            field_dict["thisEmploymentTax"] = this_employment_tax
        if total_pay_for_year is not UNSET:
            field_dict["totalPayForYear"] = total_pay_for_year
        if total_tax_for_year is not UNSET:
            field_dict["totalTaxForYear"] = total_tax_for_year

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        previous_employment_pay = d.pop("previousEmploymentPay", UNSET)

        previous_employment_tax = d.pop("previousEmploymentTax", UNSET)

        this_employment_pay = d.pop("thisEmploymentPay", UNSET)

        this_employment_tax = d.pop("thisEmploymentTax", UNSET)

        total_pay_for_year = d.pop("totalPayForYear", UNSET)

        total_tax_for_year = d.pop("totalTaxForYear", UNSET)

        p11_paye_summary = cls(
            previous_employment_pay=previous_employment_pay,
            previous_employment_tax=previous_employment_tax,
            this_employment_pay=this_employment_pay,
            this_employment_tax=this_employment_tax,
            total_pay_for_year=total_pay_for_year,
            total_tax_for_year=total_tax_for_year,
        )

        return p11_paye_summary
