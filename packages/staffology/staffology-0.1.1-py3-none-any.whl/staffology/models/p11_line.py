import datetime
from typing import Any, Dict, List, Type, TypeVar, Union

import attr
from dateutil.parser import isoparse

from ..models.p11_ni_values import P11NiValues
from ..types import UNSET, Unset

T = TypeVar("T", bound="P11Line")


@attr.s(auto_attribs=True)
class P11Line:
    """Lines for the P11 Report

    Attributes:
        date (Union[Unset, datetime.date]): [readonly]
        period (Union[Unset, None, str]): [readonly]
        gross_taxable_pay (Union[Unset, float]): [readonly]
        gross_taxable_pay_ytd (Union[Unset, float]): [readonly]
        tax (Union[Unset, float]): [readonly]
        tax_ytd (Union[Unset, float]): [readonly]
        smp_ytd (Union[Unset, float]): [readonly]
        spp_ytd (Union[Unset, float]): [readonly]
        sap_ytd (Union[Unset, float]): [readonly]
        shpp_ytd (Union[Unset, float]): [readonly]
        spbp_ytd (Union[Unset, float]): [readonly]
        student_loan_ytd (Union[Unset, float]): [readonly]
        postgrad_loan_ytd (Union[Unset, float]): [readonly]
        ni_values (Union[Unset, None, List[P11NiValues]]): [readonly]
    """

    date: Union[Unset, datetime.date] = UNSET
    period: Union[Unset, None, str] = UNSET
    gross_taxable_pay: Union[Unset, float] = UNSET
    gross_taxable_pay_ytd: Union[Unset, float] = UNSET
    tax: Union[Unset, float] = UNSET
    tax_ytd: Union[Unset, float] = UNSET
    smp_ytd: Union[Unset, float] = UNSET
    spp_ytd: Union[Unset, float] = UNSET
    sap_ytd: Union[Unset, float] = UNSET
    shpp_ytd: Union[Unset, float] = UNSET
    spbp_ytd: Union[Unset, float] = UNSET
    student_loan_ytd: Union[Unset, float] = UNSET
    postgrad_loan_ytd: Union[Unset, float] = UNSET
    ni_values: Union[Unset, None, List[P11NiValues]] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        date: Union[Unset, str] = UNSET
        if not isinstance(self.date, Unset):
            date = self.date.isoformat()

        period = self.period
        gross_taxable_pay = self.gross_taxable_pay
        gross_taxable_pay_ytd = self.gross_taxable_pay_ytd
        tax = self.tax
        tax_ytd = self.tax_ytd
        smp_ytd = self.smp_ytd
        spp_ytd = self.spp_ytd
        sap_ytd = self.sap_ytd
        shpp_ytd = self.shpp_ytd
        spbp_ytd = self.spbp_ytd
        student_loan_ytd = self.student_loan_ytd
        postgrad_loan_ytd = self.postgrad_loan_ytd
        ni_values: Union[Unset, None, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.ni_values, Unset):
            if self.ni_values is None:
                ni_values = None
            else:
                ni_values = []
                for ni_values_item_data in self.ni_values:
                    ni_values_item = ni_values_item_data.to_dict()

                    ni_values.append(ni_values_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if date is not UNSET:
            field_dict["date"] = date
        if period is not UNSET:
            field_dict["period"] = period
        if gross_taxable_pay is not UNSET:
            field_dict["grossTaxablePay"] = gross_taxable_pay
        if gross_taxable_pay_ytd is not UNSET:
            field_dict["grossTaxablePayYTD"] = gross_taxable_pay_ytd
        if tax is not UNSET:
            field_dict["tax"] = tax
        if tax_ytd is not UNSET:
            field_dict["taxYTD"] = tax_ytd
        if smp_ytd is not UNSET:
            field_dict["smpYTD"] = smp_ytd
        if spp_ytd is not UNSET:
            field_dict["sppYTD"] = spp_ytd
        if sap_ytd is not UNSET:
            field_dict["sapYTD"] = sap_ytd
        if shpp_ytd is not UNSET:
            field_dict["shppYTD"] = shpp_ytd
        if spbp_ytd is not UNSET:
            field_dict["spbpYTD"] = spbp_ytd
        if student_loan_ytd is not UNSET:
            field_dict["studentLoanYTD"] = student_loan_ytd
        if postgrad_loan_ytd is not UNSET:
            field_dict["postgradLoanYTD"] = postgrad_loan_ytd
        if ni_values is not UNSET:
            field_dict["niValues"] = ni_values

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

        gross_taxable_pay = d.pop("grossTaxablePay", UNSET)

        gross_taxable_pay_ytd = d.pop("grossTaxablePayYTD", UNSET)

        tax = d.pop("tax", UNSET)

        tax_ytd = d.pop("taxYTD", UNSET)

        smp_ytd = d.pop("smpYTD", UNSET)

        spp_ytd = d.pop("sppYTD", UNSET)

        sap_ytd = d.pop("sapYTD", UNSET)

        shpp_ytd = d.pop("shppYTD", UNSET)

        spbp_ytd = d.pop("spbpYTD", UNSET)

        student_loan_ytd = d.pop("studentLoanYTD", UNSET)

        postgrad_loan_ytd = d.pop("postgradLoanYTD", UNSET)

        ni_values = []
        _ni_values = d.pop("niValues", UNSET)
        for ni_values_item_data in _ni_values or []:
            ni_values_item = P11NiValues.from_dict(ni_values_item_data)

            ni_values.append(ni_values_item)

        p11_line = cls(
            date=date,
            period=period,
            gross_taxable_pay=gross_taxable_pay,
            gross_taxable_pay_ytd=gross_taxable_pay_ytd,
            tax=tax,
            tax_ytd=tax_ytd,
            smp_ytd=smp_ytd,
            spp_ytd=spp_ytd,
            sap_ytd=sap_ytd,
            shpp_ytd=shpp_ytd,
            spbp_ytd=spbp_ytd,
            student_loan_ytd=student_loan_ytd,
            postgrad_loan_ytd=postgrad_loan_ytd,
            ni_values=ni_values,
        )

        return p11_line
